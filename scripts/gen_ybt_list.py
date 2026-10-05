#!/usr/bin/env python3
"""生成 problem-sets/ybt.md 的表格区：按 ybt.ssoier.cn 左侧分类索引整理的题目单。

数据来源：https://ybt.ssoier.cn/index.php 左侧「题库全部题目分类索引」
（分类树 POST type=25 返回；题目标题 POST type=22 批量返回）。

只重写 problem-sets/ybt.md 中 `<!-- ybt:generated:start/end -->` 之间的表格区，
并刷新 frontmatter 的 items/covered 两个统计字段；其余内容（引言、笔记）保留。

用法：
    python3 scripts/gen_ybt_list.py            # 用本地快照 scripts/ybt_catalog.json 生成
    python3 scripts/gen_ybt_list.py --fetch    # 先从 ybt.ssoier.cn 重新抓取快照再生成
    python3 scripts/gen_ybt_list.py --check    # 只校验对照关系，不写文件

输出：problem-sets/ybt.md
"""

from __future__ import annotations

import datetime
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = Path(__file__).resolve().parent / "ybt_catalog.json"
OUTPUT = ROOT / "problem-sets" / "ybt.md"
PROBLEMS = ROOT / "problems"

YBT_SHOW = "https://ybt.ssoier.cn/problem_show.php?pid={pid}"
ROJ_SHOW = "/problem/{pid}"  # 站内链接：GitHub 上阅读时需补 https://roj.ac.cn 前缀

# 题目单覆盖的一本通顶层分类（不含 GESP考级 / CSPJ / CSPS 真题）
TOP_SECTIONS = ["C++编程语言", "基础算法", "数据结构基础", "算法提高篇", "高手训练篇"]

# 同题号但题目不同（题号撞车）：ROJ 侧不是这道一本通题
MANUAL_REJECT = [str(x) for x in range(1671, 1682)] + ["2097"]
# 同题号、标题差异大但经人工核对题面确认是同一道题
MANUAL_ACCEPT = ["1473", "1495", "1507", "1540", "1592"]


# ---------------------------------------------------------------- 抓取快照

def _post(url: str, data: str) -> str:
    """POST 一个表单；优先 urllib，失败（如老 TLS）时回退到 curl。"""
    try:
        import urllib.request

        req = urllib.request.Request(
            url,
            data=data.encode(),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8-sig")
    except Exception:
        out = subprocess.run(
            [
                "curl", "-s", "-m", "60", "-X", "POST", url,
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-H", "X-Requested-With: XMLHttpRequest",
                "--data", data,
            ],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.lstrip("\ufeff")


def fetch_catalog() -> dict:
    menu = _post("https://ybt.ssoier.cn/index.php", "type=25")
    pids = re.findall(r"/\{(\d+)/\}", menu)
    unique = list(dict.fromkeys(pids))
    titles: dict[str, str] = {}
    for i in range(0, len(unique), 150):
        batch = ",".join(unique[i:i + 150])
        resp = _post("https://ybt.ssoier.cn/user_ac_list.php", f"type=22&pids={batch}")
        for item in resp.split("|||"):
            q = item.strip().split("`")
            if len(q) >= 2 and q[0].isdigit():
                titles[q[0]] = q[1]
        print(f"  抓取标题 {len(titles)}/{len(unique)}", file=sys.stderr)
    missing = [p for p in unique if p not in titles]
    if missing:
        print(f"  警告：{len(missing)} 个题号未取到标题：{missing}", file=sys.stderr)
    return {
        "source": "https://ybt.ssoier.cn/index.php",
        "fetched": datetime.date.today().isoformat(),
        "menu": menu,
        "titles": titles,
    }


# ---------------------------------------------------------------- 解析分类树

class Node:
    def __init__(self, depth: int, text: str = "", pid: str = ""):
        self.depth = depth
        self.text = text
        self.pid = pid          # 非空表示这是题目叶子
        self.children: list[Node] = []


def parse_tree(menu: str) -> list[Node]:
    roots: list[Node] = []
    stack: list[Node] = []
    for line in menu.split("\n"):
        if not line.strip():
            continue
        depth = len(line) - len(line.lstrip())
        text = line.strip()
        pid = ""
        m = re.fullmatch(r"/\{(\d+)/\}", text)
        if m:
            pid = m.group(1)
            text = ""
        node = Node(depth, text, pid)
        while stack and stack[-1].depth >= depth:
            stack.pop()
        (stack[-1].children if stack else roots).append(node)
        stack.append(node)
    return roots


# ---------------------------------------------------------------- ROJ 对照

def core_title(t: str) -> str:
    """去掉【例题x】【xxNOIP…】「一本通 1.1 例 2」usaco-x.y.z 之类的修饰，只留题名主体。

    括号里是中文的（如（Noip1999）、(Produce)）一并去掉；只含罗马数字/数字的
    （如（II））保留，以便区分《高精度乘法（II）》与《高精度乘法》这类题。
    """
    t = re.sub(r"【.*?】|「.*?」|\[.*?\]", "", t)
    t = re.sub(r"[（(]([^）)]*)[）)]",
               lambda m: "" if re.search(r"[\u4e00-\u9fff]", m.group(1)) else m.group(0),
               t)
    t = re.sub(r"usaco-[\d.]+", "", t, flags=re.I)
    return re.sub(r"\s+", "", t).strip()


def load_roj_titles() -> dict[str, str]:
    out = {}
    for d in sorted(PROBLEMS.iterdir()):
        cfg = d / "config.json"
        if cfg.exists():
            try:
                out[d.name] = json.loads(cfg.read_text())["title"]
            except Exception:
                pass
    return out


def same_problem(ybt_id: str, ybt_title: str, roj_title: str) -> bool:
    if roj_title.lower().startswith("usaco-"):
        return False
    if ybt_id in MANUAL_REJECT:
        return False
    if ybt_id in MANUAL_ACCEPT:
        return True
    a, b = core_title(ybt_title), core_title(roj_title)
    if a and a == b:
        return True
    if a and b:
        return difflib.SequenceMatcher(None, a, b).ratio() >= 0.5
    return False


NOIP_YBT = re.compile(r"【\s*(\d{2})\s*(NOIP|CSP[JJS]*)\s*(普及组|提高组)?\s*】")
NOIP_ROJ = re.compile(r"\[\s*(?:noip|csp)[ _-]?(\d{4})[ _-]?(普及|提高|junior|senior)?\s*\]", re.I)


def contest_year(text: str, side: str) -> tuple[str, str] | None:
    """抽出 (年份, 组别) 便于核对『同题异号』是否同一道真题。"""
    if side == "ybt":
        m = NOIP_YBT.search(text)
        if not m:
            return None
        year = "20" + m.group(1)
        grp = (m.group(3) or "")[:2]
    else:
        m = NOIP_ROJ.search(text)
        if not m:
            return None
        year = m.group(1)
        g = (m.group(2) or "").lower()
        grp = {"普及": "普及", "提高": "提高", "junior": "普及", "senior": "提高"}.get(g, "")
    return year, grp


def cross_matches(ybt_id: str, ybt_title: str, roj_titles: dict[str, str]) -> list[tuple[str, str, str]]:
    """返回 [(roj_id, roj_title, 依据)]：ROJ 中『同题不同编号』的候选。"""
    out = []
    ycore = core_title(ybt_title)
    if len(ycore) < 2:
        return []
    yct = contest_year(ybt_title, "ybt")
    for rid, rtitle in roj_titles.items():
        if rid == ybt_id or len(core_title(rtitle)) < 2:
            continue
        if core_title(rtitle) != ycore:
            continue
        rct = contest_year(rtitle, "roj")
        if yct and rct:
            if yct[0] == rct[0] and (not yct[1] or not rct[1] or yct[1] == rct[1]):
                out.append((rid, rtitle, f"同一场真题（{yct[0]}）且同名"))
            continue
        out.append((rid, rtitle, "题目同名"))
    return out


# ---------------------------------------------------------------- 生成 Markdown

def walk(node: Node, level: int, ctx: dict, out: list[str]):
    """输出一个分类节点及其子分类。"""
    anchor = f"sec-{ctx['sec_no']}"
    ctx["sec_no"] += 1
    out.append(f'<a id="{anchor}"></a>')
    out.append(f'{"#" * level} {node.text}')
    out.append("")

    direct = [c for c in node.children if c.pid]
    if direct:
        out.append("| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |")
        out.append("| ---: | --- | --- | --- |")
        for i, leaf in enumerate(direct, 1):
            pid = leaf.pid
            title = ctx["titles"].get(pid, "（标题缺失）")
            row_title = f"[{pid}]({YBT_SHOW.format(pid=pid)}) | {title}"
            roj = ctx["roj"].get(pid)
            ctx["rows"] += 1
            if roj is not None and same_problem(pid, title, roj):
                cell = f"[ROJ {pid}]({ROJ_SHOW.format(pid=pid)})"
                if core_title(title) != core_title(roj):
                    cell += f"（ROJ 题名：{roj}）"
                ctx["matched_rows"] += 1
            else:
                cell = "—"
                ctx["unmatched"].append(pid)
            out.append(f"| {i} | {row_title} | {cell} |")
        out.append("")

    for child in node.children:
        if not child.pid:
            walk(child, min(level + 1, 5), ctx, out)


def toc_line(node: Node, anchor_prefix: str, counter: list[int], depth: int = 0) -> list[str]:
    lines = []
    for child in node.children:
        if child.pid:
            continue
        anchor = f"{anchor_prefix}-{counter[0]}"
        counter[0] += 1
        # walk() 中的锚点编号按先序遍历，这里按同样顺序计数
        lines.append(f"{'  ' * depth}- [{child.text}](#{anchor})")
    return lines


def count_sections(nodes: list[Node]) -> int:
    n = 0
    for node in nodes:
        if not node.pid:
            n += 1 + count_sections(node.children)
    return n
# ---------------------------------------------------------------- 输出 problem-sets/ybt.md

REGION_START = "<!-- ybt:generated:start -->"
REGION_END = "<!-- ybt:generated:end -->"

TEMPLATE_HEAD = """---
title: 一本通（ybt.ssoier.cn）题目单
description: 按《信息学奥赛一本通（C++版）》在线题库分类索引整理的刷题清单，覆盖 C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇，逐题标注 ROJ 收录情况。
tags: [一本通, 教材配套, 刷题计划]
order: 1
items: {items}
covered: {covered}
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理，覆盖书籍主线五大部分（不含 GESP 考级、CSP-J/S 真题），可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。
"""

TEMPLATE_TAIL = """
## 数据来源与更新

- 分类树与题目标题抓取自 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php)（快照：`scripts/ybt_catalog.json`）；ROJ 收录情况取自本仓库 `problems/*/config.json`。
- 表格区（`<!-- ybt:generated:start -->` 与 `<!-- ybt:generated:end -->` 之间）由 `python3 scripts/gen_ybt_list.py` 重新生成，引言、笔记等区块外内容可手工修改。
"""


def generate() -> dict:
    catalog = json.loads(CATALOG.read_text())
    titles = catalog["titles"]
    roots = parse_tree(catalog["menu"])
    by_name = {n.text: n for n in roots}

    roj_titles = load_roj_titles()
    ctx = {
        "titles": titles,
        "roj": roj_titles,
        "rows": 0,
        "matched_rows": 0,
        "unmatched": [],
        "sec_no": 0,
    }

    body: list[str] = []
    toc: list[str] = []
    counter = [0]
    per_top: list[tuple[str, int, int]] = []

    for top in TOP_SECTIONS:
        node = by_name.get(top)
        if node is None:
            print(f"警告：快照中找不到分类「{top}」", file=sys.stderr)
            continue
        n_sections = count_sections(node.children) + 1
        anchor = f"sec-{counter[0]}"
        toc.append(f"- [{top}](#{anchor})")
        sub_counter = [counter[0] + 1]
        for child in node.children:
            if child.pid:
                continue
            a = f"sec-{sub_counter[0]}"
            sub_counter[0] += 1 + count_sections(child.children)
            toc.append(f"  - [{child.text}](#{a})")
        counter[0] += n_sections

        before_rows, before_matched = ctx["rows"], ctx["matched_rows"]
        walk(node, 2, ctx, body)
        n_rows = ctx["rows"] - before_rows
        per_top.append((top, n_rows, ctx["matched_rows"] - before_matched))

    total = ctx["rows"]
    matched = ctx["matched_rows"]

    # 附录 A：同题异号（只看正文中未出现同题号收录的题）
    found: dict[str, list[tuple[str, str, str]]] = {}
    for pid in dict.fromkeys(ctx["unmatched"]):
        title = titles.get(pid, "")
        hits = cross_matches(pid, title, roj_titles)
        if hits:
            found[pid] = hits

    def appendix_rows(verified: bool) -> list[str]:
        rows = []
        for pid in sorted(found, key=int):
            hits = [h for h in found[pid] if (h[2] != "题目同名") == verified]
            if not hits:
                continue
            links = "、".join(
                f"[ROJ {rid}]({ROJ_SHOW.format(pid=rid)})（{rtitle}）" for rid, rtitle, _ in hits
            )
            why = "；".join(dict.fromkeys(w for _, _, w in hits))
            title = titles.get(pid, "")
            rows.append(
                f"| [{pid}]({YBT_SHOW.format(pid=pid)}) | {title} | {links} | {why} |"
            )
        return rows

    region: list[str] = []
    region.append("## 收录情况总览")
    region.append("")
    region.append("| 分类 | 题目数 | ROJ 已收录 | 收录率 |")
    region.append("| --- | ---: | ---: | ---: |")
    for top, n, m in per_top:
        rate = f"{m / n * 100:.0f}%" if n else "—"
        region.append(f"| {top} | {n} | {m} | {rate} |")
    region.append(f"| **合计** | **{total}** | **{matched}** | **{matched / total * 100:.0f}%** |")
    region.append("")
    region.append("## 目录")
    region.append("")
    region.extend(toc)
    region.append("- [附录 A：同题异号对照](#appendix-a)")
    region.append("")
    region.extend(body)

    region.append('<a id="appendix-a"></a>')
    region.append("## 附录 A：同题异号对照")
    region.append("")
    region.append(
        "下表的题目在 ROJ 中没有同题号的记录，但 ROJ 的其他题号下可能有同一道题"
        "（同一道经典题被多个题库收录、题号各不相同）。做题时任选其一即可。"
    )
    region.append("")
    region.append("### A.1 已核对（同一场真题，年份与组别一致）")
    region.append("")
    rows = appendix_rows(verified=True)
    if rows:
        region.append("| 一本通题号 | 题目名称 | ROJ 中的同题 | 依据 |")
        region.append("| --- | --- | --- | --- |")
        region.extend(rows)
    else:
        region.append("（无）")
    region.append("")
    region.append("### A.2 待核对（题目同名）")
    region.append("")
    region.append("同名不等于同题（比如两本书里都有叫「最大公约数」的题），刷题前请先对照题面。")
    region.append("")
    rows = appendix_rows(verified=False)
    if rows:
        region.append("| 一本通题号 | 题目名称 | ROJ 中的同题 | 依据 |")
        region.append("| --- | --- | --- | --- |")
        region.extend(rows)
    else:
        region.append("（无）")
    region.append("")

    return {"region": "\n".join(region).rstrip() + "\n", "items": total, "covered": matched}


def set_frontmatter_values(text: str, updates: dict[str, int]) -> str:
    """更新 frontmatter 中的 items/covered；不存在则插入，其余字段原样保留。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{OUTPUT} 缺少 frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise SystemExit(f"{OUTPUT} frontmatter 未闭合")

    remaining = dict(updates)
    for i in range(1, end):
        for key in list(remaining):
            if re.match(rf"^{re.escape(key)}\s*:", lines[i]):
                lines[i] = f"{key}: {remaining.pop(key)}"
    for key in list(remaining):
        lines.insert(end, f"{key}: {remaining.pop(key)}")
        end += 1
    return "\n".join(lines)


def upsert_problem_set(region: str, items: int, covered: int) -> str:
    if OUTPUT.exists():
        text = OUTPUT.read_text()
    else:
        text = (
            TEMPLATE_HEAD.format(items=items, covered=covered)
            + "\n" + REGION_START + "\n" + REGION_END + "\n"
            + TEMPLATE_TAIL
        )

    start = text.find(REGION_START)
    end = text.find(REGION_END)
    if start < 0 or end < start:
        raise SystemExit(f"{OUTPUT} 缺少生成区块标记 {REGION_START} / {REGION_END}")
    text = text[: start + len(REGION_START)] + "\n\n" + region.rstrip() + "\n\n" + text[end:]
    return set_frontmatter_values(text, {"items": items, "covered": covered})


def main() -> int:
    args = set(sys.argv[1:])
    if "--fetch" in args:
        print("抓取 ybt.ssoier.cn 快照 ...", file=sys.stderr)
        CATALOG.write_text(json.dumps(fetch_catalog(), ensure_ascii=False, indent=1))
        print(f"已写入 {CATALOG}", file=sys.stderr)
    result = generate()
    if "--check" in args:
        print(result["region"][:2000])
        print(f"items={result['items']} covered={result['covered']}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    text = upsert_problem_set(result["region"], result["items"], result["covered"])
    OUTPUT.write_text(text)
    print(f"已生成 {OUTPUT}（{len(text)} 字节，items={result['items']} covered={result['covered']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
