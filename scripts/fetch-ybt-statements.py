#!/usr/bin/env python3
"""从一本通（ybt.ssoier.cn）抓题面，在暂存区组装 ROJ 题目记录。

流水线（严格遵守 .agents/skills/add-roj-problem 的「先预览、后落地」）：

    1. stage   抓题面 → .ybt-import/staging/<ybt_pid>/（config.json + content.md + data.json + pic/）
    2. report  打印暂存区预览（题号/标题/限制/图片/ID 提议/告警），不写 problems/
    3. apply   通过确认后，原子落盘到 problems/<roj_id>/，跑图片补抓与 data.json 校验

题面解析：problem_show.php 的正文在 `pshow("…")` JS 字符串里（含 \\n \\\" \\\\ 转义
与 $…$ LaTeX），样例在 `<pre>`，图片引用形如 `<img src="/pic/1284.gif">`。
注意原站会跨 pid 引图，图片一律按引用名下载，不按 id 猜。

ID 策略：一本通题号在 problems/ 空闲就沿用；被占用则从 5000 起分配空闲号，
并把映射写进 scripts/ybt_roj_mapping.json（题目单生成脚本据此改写 ROJ 列）。

用法：
    python3 scripts/fetch-ybt-statements.py --pids 2060,2016,1414          # 抓到暂存区
    python3 scripts/fetch-ybt-statements.py --report                        # 预览
    python3 scripts/fetch-ybt-statements.py --apply                         # 落地（需先预览）
    python3 scripts/fetch-ybt-statements.py --pids … --report --fetch       # 抓并预览
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_ROOT = REPO_ROOT / ".ybt-import" / "staging"
PROBLEMS_DIR = REPO_ROOT / "problems"
CATALOG = Path(__file__).resolve().parent / "ybt_catalog.json"
MAPPING = Path(__file__).resolve().parent / "ybt_roj_mapping.json"
YBT_SHOW = "https://ybt.ssoier.cn/problem_show.php?pid={pid}"
YBT_PIC = "http://ybt.ssoier.cn:8088/"
NEW_ID_START = 5000

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

MAGIC = {
    b"\xff\xd8\xff": ".jpg",
    b"\x89PNG\r\n\x1a\n": ".png",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
}

# 章节名 → 粗粒度算法标签（只用语料里已存在的标签词）
TAG_BY_CHAPTER = [
    ("图论", ["图论"]),
    ("最短路", ["最短路"]),
    ("字符串", ["字符串"]),
    ("动态规划", ["动态规划"]),
    ("数学基础", ["数学"]),
    ("数论", ["数论"]),
    ("数据结构", ["数据结构"]),
    ("树", ["树"]),
    ("搜索", ["搜索"]),
    ("贪心", ["贪心"]),
    ("高精度", ["高精度"]),
    ("递归", ["递归"]),
    ("递推", ["递推"]),
    ("排序", ["排序"]),
]


# ------------------------------------------------------------------ 网络

def http_get(url: str) -> bytes:
    """GET；优先 urllib（老 TLS 握手失败时回退 curl）。"""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except Exception:
        result = subprocess.run(
            ["curl", "-s", "-m", "60", "-L", "-A", USER_AGENT, url],
            capture_output=True, check=True,
        )
        return result.stdout


# ------------------------------------------------------------------ 题面解析

JS_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "'": "'", "\\": "\\", "/": "/"}


def js_unescape(text: str) -> str:
    return re.sub(r"\\(.)", lambda m: JS_ESCAPES.get(m.group(1), m.group(1)), text)


IMG_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*>')
PRESHOW_RE = re.compile(r'pshow\("(.*?)"\);', re.S)
PRE_RE = re.compile(r"<pre>(.*?)</pre>", re.S)


def rewrite_images(text: str, warnings: list[str]) -> str:
    def replace(match: re.Match) -> str:
        src = html.unescape(match.group(1)).strip()
        if src.startswith(("http://", "https://", "//")):
            return f"![]({src})"
        name = src.lstrip("/")
        if not name.startswith("pic/"):
            warnings.append(f"未知图片引用：{src}")
            return f"![]({src})"
        return f"![]({name})"

    return IMG_RE.sub(replace, text)


def inline_html_to_markdown(text: str, warnings: list[str]) -> str:
    """把常见的内联 HTML 转成 Markdown；剩余结构 HTML 告警后剥除。"""
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<(code|tt)>(.*?)</\1>", lambda m: f"`{m.group(2)}`", text, flags=re.I | re.S)
    text = re.sub(r"<(b|strong)>(.*?)</\1>", lambda m: f"**{m.group(2)}**", text, flags=re.I | re.S)
    text = re.sub(r"<(i|em)>(.*?)</\1>", lambda m: f"*{m.group(2)}*", text, flags=re.I | re.S)
    text = re.sub(r"<font[^>]*>(.*?)</font>", lambda m: m.group(1), text, flags=re.I | re.S)
    text = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: m.group(1), text, flags=re.I | re.S)
    leftovers = re.findall(r"<[^>]+>", text)
    leftovers = [tag for tag in leftovers if not tag.lower().startswith("<img")]
    if leftovers:
        warnings.append(f"残留未转换 HTML：{'、'.join(sorted(set(leftovers))[:5])}")
    return re.sub(r"<[^>]+>", "", text)


def table_to_markdown(fragment: str, warnings: list[str]) -> str:
    """把一段 <table>…</table> 转成 Markdown 管道表。"""
    rows = []
    for row_match in re.finditer(r"<tr[^>]*>(.*?)</tr>", fragment, re.I | re.S):
        cells = []
        for cell_match in re.finditer(r"<(td|th)[^>]*>(.*?)</\1>", row_match.group(1), re.I | re.S):
            text = inline_html_to_markdown(cell_match.group(2), warnings)
            text = re.sub(r"\s+", " ", text.replace("|", "\\|")).strip()
            cells.append(text or " ")
        if cells:
            rows.append(cells)
    if not rows:
        warnings.append("表格解析失败，降级为纯文本")
        return re.sub(r"<[^>]+>", " ", fragment)
    width = max(len(row) for row in rows)
    rows = [row + [" "] * (width - len(row)) for row in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows[1:]]
    return "\n".join(lines)


def pshow_text_to_markdown(text: str, warnings: list[str]) -> str:
    """pshow 字符串体 → Markdown（内嵌 <pre> 样例、<table> 表格都要转）。"""
    text = rewrite_images(text, warnings)
    text = text.replace("\u00a0", " ")

    # 内嵌 <pre>…</pre> → 围栏代码块
    pieces = []
    cursor = 0
    for match in re.finditer(r"<pre[^>]*>(.*?)</pre>", text, re.I | re.S):
        pieces.append(("text", text[cursor:match.start()]))
        pieces.append(("code", html.unescape(match.group(1)).strip("\n")))
        cursor = match.end()
    pieces.append(("text", text[cursor:]))

    out: list[str] = []
    for kind, value in pieces:
        if kind == "code":
            out.append(f"```\n{value}\n```")
            continue
        value = re.sub(
            r"<table[^>]*>.*?</table>",
            lambda m: "\n\n" + table_to_markdown(m.group(0), warnings) + "\n\n",
            value, flags=re.I | re.S,
        )
        value = inline_html_to_markdown(value, warnings)
        out.append(value)
    text = "\n\n".join(chunk for chunk in out if chunk.strip())
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def section_body_to_markdown(body: str, warnings: list[str]) -> str:
    """一个 <h3>【…】</h3> 小节的 HTML → Markdown 文本。"""
    chunks: list[str] = []
    for match in PRESHOW_RE.finditer(body):
        text = js_unescape(match.group(1))
        text = html.unescape(text)
        chunks.append(pshow_text_to_markdown(text, warnings))
    for match in PRE_RE.finditer(body):
        code = html.unescape(match.group(1)).strip("\n")
        chunks.append(f"```\n{code}\n```")
    chunks = [chunk for chunk in chunks if chunk.strip()]
    if not chunks:
        # 既无 pshow 也无 <pre>：剥掉标签看剩什么
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        if text:
            chunks.append(text)
    return "\n\n".join(chunks)


SECTION_RE = re.compile(r"<h3>(【[^<]*】)</h3>(.*?)(?=<h3>|<p align=center)", re.S)
TITLE_RE = re.compile(r"<h3>(\d+)：(.*?)</h3>")
TIME_RE = re.compile(r"时间限制:\s*(\d+)\s*ms")
MEM_RE = re.compile(r"内存限制:\s*(\d+)\s*KB")


def parse_statement(page: str, pid: str, warnings: list[str]) -> dict:
    title_match = TITLE_RE.search(page)
    if not title_match or title_match.group(1) != pid:
        raise ValueError(f"题号 {pid}：题面标题行解析失败")
    title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(2))).strip()

    time_match = TIME_RE.search(page)
    mem_match = MEM_RE.search(page)
    if not time_match:
        warnings.append("未解析到时间限制")
    if not mem_match:
        warnings.append("未解析到内存限制")

    sections: list[tuple[str, str]] = []
    for match in SECTION_RE.finditer(page):
        name = html.unescape(match.group(1)).strip()
        body = section_body_to_markdown(match.group(2), warnings)
        if body:
            sections.append((name, body))
    if not sections:
        raise ValueError(f"题号 {pid}：没有解析到任何题面小节")

    return {
        "title": title,
        "time": int(time_match.group(1)) if time_match else None,
        "memory_kb": int(mem_match.group(1)) if mem_match else None,
        "sections": sections,
    }


def render_content(sections: list[tuple[str, str]]) -> str:
    blocks = [f"### {name}\n\n{body}" for name, body in sections]
    return "\n\n".join(blocks).rstrip() + "\n"


# ------------------------------------------------------------------ 图片

def sniff_extension(data: bytes) -> str | None:
    for magic, extension in MAGIC.items():
        if data.startswith(magic):
            return extension
    return None


def fetch_picture(pic_dir: Path, ref: str, warnings: list[str]) -> None:
    """按引用名下载 pic/<name>，扩展名以魔数为准（原站后缀不可信）。"""
    name = ref.split("/", 1)[1]
    stem = Path(name).stem
    existing = list(pic_dir.glob(f"{stem}.*"))
    if existing:
        return
    url = YBT_PIC + urllib.parse.quote(f"pic/{name}")
    try:
        data = http_get(url)
    except Exception as error:  # noqa: BLE001
        warnings.append(f"图片下载失败：{ref}（{error}）")
        return
    extension = sniff_extension(data)
    if not extension:
        warnings.append(f"图片内容不是图片：{ref}")
        return
    pic_dir.mkdir(parents=True, exist_ok=True)
    (pic_dir / f"{stem}{extension}").write_bytes(data)


# ------------------------------------------------------------------ 元数据

def chapter_path(pid: str) -> str | None:
    if not CATALOG.exists():
        return None
    menu = json.loads(CATALOG.read_text())["menu"].split("\n")
    path: list[str] = []
    for line in menu:
        if not line.strip():
            continue
        depth = len(line) - len(line.lstrip())
        text = line.strip()
        if re.fullmatch(r"/\{\d+/\}", text):
            if text == f"/{{{pid}/}}":
                return " / ".join(p.strip() for p in path)
            continue
        path = path[: depth // 2]
        path.append(text)
    return None


def coarse_tags(chapter: str | None) -> list[str]:
    if not chapter:
        return []
    for keyword, tags in TAG_BY_CHAPTER:
        if keyword in chapter:
            return tags
    return []


def source_label(chapter: str | None) -> str | None:
    if not chapter:
        return None
    parts = [p.strip() for p in chapter.split("/")]
    return "信息学奥赛一本通 · " + "·".join(parts[:2])


# ------------------------------------------------------------------ ID 分配

def existing_ids() -> set[str]:
    return {p.name for p in PROBLEMS_DIR.iterdir() if p.is_dir() and p.name.isdigit()}


def allocate_ids(pids: list[str]) -> dict[str, str]:
    """一本通题号空闲就沿用；被占用的按 pid 升序从 5000+ 取空闲号。"""
    taken = existing_ids()
    mapping: dict[str, str] = {}
    for pid in sorted(pids, key=int):
        if pid not in taken:
            mapping[pid] = pid
            taken.add(pid)
    for pid in sorted((p for p in pids if p not in mapping), key=int):
        candidate = NEW_ID_START
        while str(candidate) in taken:
            candidate += 1
        mapping[pid] = str(candidate)
        taken.add(str(candidate))
    return mapping


# ------------------------------------------------------------------ staging

def stage(pid: str, mapping: dict[str, str]) -> dict:
    warnings: list[str] = []
    page = http_get(YBT_SHOW.format(pid=pid)).decode("utf-8", "replace")
    parsed = parse_statement(page, pid, warnings)

    target = STAGING_ROOT / pid
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    content = render_content(parsed["sections"])
    (target / "content.md").write_text(content, encoding="utf-8")

    config: dict = {"title": parsed["title"]}
    if parsed["time"] is not None:
        config["time"] = parsed["time"]
    if parsed["memory_kb"] is not None:
        config["memory"] = max(1, math.ceil(parsed["memory_kb"] / 1024))
    tags = coarse_tags(chapter_path(pid))
    if tags:
        config["tags"] = tags
    source = source_label(chapter_path(pid))
    if source:
        config["source"] = source
    (target / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (target / "data.json").write_text('{\n  "files": []\n}\n', encoding="utf-8")

    for ref in sorted(set(re.findall(r"!\[\]\((pic/[^)]+)\)", content))):
        fetch_picture(target / "pic", ref, warnings)

    entry = {
        "ybt_pid": pid,
        "roj_id": mapping[pid],
        "title": parsed["title"],
        "time": parsed["time"],
        "memory_mb": config.get("memory"),
        "tags": config.get("tags", []),
        "source": config.get("source"),
        "sections": [name for name, _ in parsed["sections"]],
        "pictures": sorted(p.name for p in (target / "pic").glob("*")) if (target / "pic").exists() else [],
        "id_reallocated": mapping[pid] != pid,
        "warnings": warnings,
    }
    (target / "candidate.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return entry


# ------------------------------------------------------------------ report / apply

def load_candidates() -> list[dict]:
    entries = []
    if not STAGING_ROOT.exists():
        return entries
    for candidate in sorted(STAGING_ROOT.iterdir(), key=lambda p: int(p.name) if p.name.isdigit() else 0):
        meta = candidate / "candidate.json"
        if meta.exists():
            entries.append(json.loads(meta.read_text()))
    return entries


def report() -> None:
    candidates = load_candidates()
    if not candidates:
        print("暂存区为空。")
        return
    print(f"暂存区预览（{len(candidates)} 个候选，未写入 problems/）：\n")
    for entry in candidates:
        rid = entry["roj_id"]
        flag = f"（题号被占 → 新 ID {rid}）" if entry["id_reallocated"] else "（沿用一本通题号）"
        print(f"- [{entry['ybt_pid']} → {rid}] {entry['title']} {flag}")
        print(f"    限制：{entry['time']} ms / {entry['memory_mb']} MB；标签：{entry['tags'] or '[]'}；来源：{entry['source'] or '-'}")
        print(f"    小节：{'、'.join(entry['sections'])}；图片：{len(entry['pictures'])} 张")
        for warning in entry["warnings"]:
            print(f"    ⚠ {warning}")
    print("\n确认后执行：python3 scripts/fetch-ybt-statements.py --apply")


def apply_staged() -> None:
    candidates = load_candidates()
    if not candidates:
        print("暂存区为空。")
        return
    problems = PROBLEMS_DIR.resolve()
    ids_script = REPO_ROOT / ".agents/skills/add-roj-problem/scripts/find-empty-roj-id.py"
    manifest_script = REPO_ROOT / ".agents/skills/add-roj-problem/scripts/generate-data-manifest.py"

    # 落地前重扫一次，防并发撞号
    mapping_changed = False
    for entry in candidates:
        target = problems / entry["roj_id"]
        if target.exists():
            fresh = subprocess.run(
                [sys.executable, str(ids_script), "--start", str(NEW_ID_START)],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            print(f"! ID {entry['roj_id']} 已被占用，改分配 {fresh}")
            entry["roj_id"] = fresh
            entry["id_reallocated"] = entry["ybt_pid"] != fresh
            mapping_changed = True

    for entry in candidates:
        source = STAGING_ROOT / entry["ybt_pid"]
        target = problems / entry["roj_id"]
        if target.exists():
            raise SystemExit(f"拒绝覆盖已存在的 problems/{entry['roj_id']}/")
        target.mkdir(parents=True)
        # 白名单拷贝（同 .agents/skills/add-roj-problem 约定）：
        # 题面/元数据/标程/生成器/图片/公开数据；报告与验证残余物留在暂存区。
        for name in ("content.md", "content.pdf", "config.json", "data.json", "std.cpp", "data.py"):
            if (source / name).exists():
                shutil.copy2(source / name, target / name)
        for dir_name in ("pic", "data"):
            if (source / dir_name).is_dir():
                shutil.copytree(source / dir_name, target / dir_name)
        subprocess.run(
            [sys.executable, str(manifest_script), "--root", str(problems), "--problem", entry["roj_id"]],
            check=True,
        )
        print(f"✓ problems/{entry['roj_id']}/  ← 一本通 {entry['ybt_pid']}《{entry['title']}》")

    # 写/更新题号映射（题目单生成脚本用）
    mapping = json.loads(MAPPING.read_text()) if MAPPING.exists() else {}
    for entry in candidates:
        if entry["id_reallocated"] or entry["ybt_pid"] != entry["roj_id"]:
            mapping[entry["ybt_pid"]] = entry["roj_id"]
    if mapping_changed or mapping:
        MAPPING.write_text(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    # 校验范围限本次导入：存量题目的 data/ 本体在归档通道、不在本机，全库 --check 必然报 mismatch。
    check = [sys.executable, str(manifest_script), "--check"]
    for entry in candidates:
        check += ["--problem", entry["roj_id"]]
    subprocess.run(check, check=True)
    print("\n校验通过。后续：对带图题目跑 scripts/fetch-problem-images.py 补图；不要自动 git 提交。")


# ------------------------------------------------------------------ main

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pids", help="逗号分隔的一本通题号")
    parser.add_argument("--from-file", help="每行 题号\t章节\t标题 的清单文件")
    parser.add_argument("--limit", type=int, default=0, help="配合 --from-file 只取前 N 个")
    parser.add_argument("--fetch", action="store_true", help="抓取并写暂存区（--pids/--from-file 时默认抓取）")
    parser.add_argument("--report", action="store_true", help="打印暂存区预览")
    parser.add_argument("--apply", action="store_true", help="把暂存区落地到 problems/（会先打印预览）")
    args = parser.parse_args()

    pids: list[str] = []
    if args.pids:
        pids.extend(p.strip() for p in args.pids.split(",") if p.strip())
    if args.from_file:
        for line in Path(args.from_file).read_text().split("\n"):
            pid = line.split("\t", 1)[0].strip()
            if pid.isdigit():
                pids.append(pid)
    if args.limit:
        pids = pids[: args.limit]

    if pids:
        for pid in pids:
            if not pid.isdigit():
                raise SystemExit(f"非法题号：{pid}")
        # 一次性分配 ID，确定性顺序
        all_staged = sorted({*load_candidates_ids(), *pids}, key=int)
        mapping = allocate_ids(all_staged)
        for pid in pids:
            entry = stage(pid, mapping)
            flag = f"→ ROJ {entry['roj_id']}" + ("（新 ID）" if entry["id_reallocated"] else "")
            print(f"✓ 暂存 一本通 {pid}《{entry['title']}》 {flag}")
            for warning in entry["warnings"]:
                print(f"    ⚠ {warning}")

    if args.apply:
        report()
        apply_staged()
    elif args.report or not pids:
        report()
    return 0


def load_candidates_ids() -> set[str]:
    return {p.name for p in STAGING_ROOT.iterdir() if p.is_dir() and p.name.isdigit()} if STAGING_ROOT.exists() else set()


if __name__ == "__main__":
    raise SystemExit(main())
