#!/usr/bin/env python3
"""生成 problem-sets/ybt-*.md：按 ybt.ssoier.cn 左侧分类索引整理的题目单（按篇章拆成多份）。

数据来源：https://ybt.ssoier.cn/index.php 左侧「题库全部题目分类索引」
（分类树 POST type=25 返回；题目标题 POST type=22 批量返回）。

每个子单只重写自己文件中 `<!-- ybt:generated:start/end -->` 之间的区块（本篇概览 /
目录 / 表格 / 附录 A），并刷新 frontmatter 的 items/covered 两个统计字段；
其余内容（引言、笔记）保留。要增删篇章只改下面的 SETS。

注意：引言与「数据来源」来自 TEMPLATE_HEAD / TEMPLATE_TAIL，只在文件不存在时写入。
改了模板又想刷到已有文件上，得先删掉那个文件（手工编辑过的引言会被一并丢弃）。

用法：
    python3 scripts/gen_ybt_list.py            # 用本地快照 scripts/ybt_catalog.json 生成
    python3 scripts/gen_ybt_list.py --fetch    # 先从 ybt.ssoier.cn 重新抓取快照再生成
    python3 scripts/gen_ybt_list.py --check    # 只校验对照关系与统计，不写文件

输出：problem-sets/ybt-cpp.md / ybt-basic.md / ybt-ds.md / ybt-adv.md / ybt-expert.md

ybt 的分类树是「章节标题与题目互为兄弟」的平结构，生成前会先归并成真正的
父子结构（见 adopt_orphan_leaves），否则一个节点的题目会全部堆在它自己的表格里、
各章节标题下反而没有题目。
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
MAPPING = Path(__file__).resolve().parent / "ybt_roj_mapping.json"
SETS_DIR = ROOT / "problem-sets"
PROBLEMS = ROOT / "problems"

YBT_SHOW = "https://ybt.ssoier.cn/problem_show.php?pid={pid}"
ROJ_SHOW = "/problem/{pid}"  # 站内链接：GitHub 上阅读时需补 https://roj.ac.cn 前缀

# 一本通题目单的拆分：一个顶层分类一个文件（slug 即详情页 URL）。
# 只覆盖书籍主线，不含 GESP考级 / CSPJ / CSPS 真题。
SETS = [
    {"top": "C++编程语言", "slug": "ybt-cpp", "order": 1},
    {"top": "基础算法", "slug": "ybt-basic", "order": 2},
    {"top": "数据结构基础", "slug": "ybt-ds", "order": 3},
    {"top": "算法提高篇", "slug": "ybt-adv", "order": 4},
    {"top": "高手训练篇", "slug": "ybt-expert", "order": 5},
]

# 同题号但题目不同（题号撞车）：ROJ 侧不是这道一本通题
# 1671-1681 曾因『同题号被占、易错配同名异题』被拉黑；现已落地专属题 5007-5017
# 并经 scripts/ybt_roj_mapping.json 显式锁定映射，取消拉黑（2097 保留）。
MANUAL_REJECT = ["2097"]
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


def adopt_orphan_leaves(node: Node) -> Node:
    """把「空章节节点 + 紧跟在它后面的兄弟题目」收成真正的父子结构。

    ybt 的分类树是平的：章节标题与题目是**兄弟**，题目排在自己所属章节标题后面，
    例如「一、基础算法(高手训练)」的孩子依次是
    第1章 贪心算法（空）、1671-1675、第2章 二分与三分（空）、1676-1680……
    不归并的话，一个节点的所有直属题目会全部堆在它自己的表格里，
    而每个章节标题下面空空如也（曾导致「贪心算法」下无题目）。

    只归并「后面确实跟着题目」的空章节；有真子节点的节自己成树，不抢兄弟题目。
    """
    if not node.children:
        return node
    merged: list[Node] = []
    current: Node | None = None  # 正在承接后续兄弟题目的空章节
    for child in node.children:
        if child.pid:
            (current.children if current else merged).append(child)
            continue
        adopt_orphan_leaves(child)
        merged.append(child)
        current = child if not child.children else None
    node.children = merged
    return node


def unmerged_flat_sections(node: Node, path: str, out: list[str]) -> None:
    """归并后置校验：空章节后面不应再跟着兄弟题目。"""
    siblings = node.children
    for i, child in enumerate(siblings):
        if child.pid or child.children:
            continue
        if any(x.pid for x in siblings[i + 1:]):
            out.append(f"{path}/{child.text}")
            break
    for child in node.children:
        if not child.pid:
            unmerged_flat_sections(child, f"{path}/{child.text}", out)


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

def render_section(node: Node, level: int, ctx: dict, body: list[str], toc: list[str], depth: int = 0):
    """先序遍历输出一个分类节点，正文与目录行同一次遍历产出（锚点顺序 = 目录顺序）。

    depth < 0 表示这个节点本身不进目录（用于每个子单的顶层篇章标题）。
    """
    anchor = f"sec-{ctx['sec_no']}"
    ctx["sec_no"] += 1
    if depth >= 0:
        toc.append(f"{'  ' * depth}- [{node.text}](#{anchor})")
    body.append(f'<a id="{anchor}"></a>')
    body.append(f'{"#" * level} {node.text}')
    body.append("")

    direct = [c for c in node.children if c.pid]
    if direct:
        body.append("| 序号 | 一本通题号 | 题目名称 | ROJ 收录 |")
        body.append("| ---: | --- | --- | --- |")
        for i, leaf in enumerate(direct, 1):
            pid = leaf.pid
            title = ctx["titles"].get(pid, "（标题缺失）")
            row_title = f"[{pid}]({YBT_SHOW.format(pid=pid)}) | {title}"
            rid = ctx["mapping"].get(pid, pid)
            roj = ctx["roj"].get(rid)
            ctx["rows"] += 1
            if roj is not None and same_problem(pid, title, roj):
                cell = f"[ROJ {rid}]({ROJ_SHOW.format(pid=rid)})"
                if rid != pid:
                    cell += f"（ROJ 题号 {rid}）"
                if core_title(title) != core_title(roj):
                    cell += f"（ROJ 题名：{roj}）"
                ctx["matched_rows"] += 1
            else:
                cell = "—"
                ctx["unmatched"].append(pid)
            body.append(f"| {i} | {row_title} | {cell} |")
        body.append("")

    for child in node.children:
        if not child.pid:
            render_section(child, min(level + 1, 5), ctx, body, toc, depth + 1)


# ---------------------------------------------------------------- 输出 problem-sets/ybt-*.md

REGION_START = "<!-- ybt:generated:start -->"
REGION_END = "<!-- ybt:generated:end -->"

TEMPLATE_HEAD = """---
title: 一本通 · {top}
description: 《信息学奥赛一本通（C++版）》{label}：{items} 题，本站收录 {covered}（{rate}）。
tags: [一本通, 教材配套, 刷题计划, {top}]
order: {order}
items: {items}
covered: {covered}
source: https://ybt.ssoier.cn/index.php
---

按《信息学奥赛一本通（C++版）》在线题库 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php) 左侧「题库全部题目分类索引」整理的 **{label}**，可对照原书顺序刷题。

## 怎么用这份单子

- **一本通题号** 链接到一本通原题页；**ROJ 收录** 列是站内链接，在本站点开直接看题面；
- ROJ 列为 `—` 表示 ROJ 暂未收录这道题（仍可去一本通原站做）；
- 括号里标注「ROJ 题名」的，表示 ROJ 侧题目名称与一本通不同（多为改名/换译），题面是同一道题；
- **附录 A** 列出 ROJ 中『同题不同编号』的情况，分「已核对」「待核对」两档可信度；
- 一本通题目单共 5 篇（C++编程语言 / 基础算法 / 数据结构基础 / 算法提高篇 / 高手训练篇），可在[题目单列表](/problem-sets)里切换；勾选进度在站内按题号全局共享，跨篇不会丢；
- 在 GitHub 上阅读时，`/problem/…` 是站内路径，需补上 `https://roj.ac.cn` 前缀才能点开。
"""

TEMPLATE_TAIL = """
## 数据来源与更新

- 分类树与题目标题抓取自 [ybt.ssoier.cn](https://ybt.ssoier.cn/index.php)（快照：`scripts/ybt_catalog.json`）；ROJ 收录情况取自本仓库 `problems/*/config.json`。
- 表格区（`<!-- ybt:generated:start -->` 与 `<!-- ybt:generated:end -->` 之间）由 `python3 scripts/gen_ybt_list.py` 重新生成，引言、笔记等区块外内容可手工修改。
"""


def build_set(spec: dict, by_name: dict, titles: dict, roj_titles: dict, mapping: dict) -> dict:
    """渲染一个篇章，返回它的正文、目录与统计。"""
    node = by_name.get(spec["top"])
    if node is None:
        raise SystemExit(f"快照中找不到分类「{spec['top']}」，检查 scripts/ybt_catalog.json 或 SETS 配置")
    ctx = {
        "titles": titles,
        "roj": roj_titles,
        "mapping": mapping,
        "rows": 0,
        "matched_rows": 0,
        "unmatched": [],
        "sec_no": 0,
    }
    body: list[str] = []
    toc: list[str] = []
    render_section(node, 2, ctx, body, toc, depth=-1)
    return {
        "spec": spec,
        "body": body,
        "toc": toc,
        "items": ctx["rows"],
        "covered": ctx["matched_rows"],
        "unmatched": ctx["unmatched"],
        "titles": titles,
        "roj": roj_titles,
    }


def appendix_rows(entry: dict, verified: bool) -> list[str]:
    """附录 A 的行：只保留归属于本篇章、且命中指定可信度档的题号。"""
    rows = []
    for pid in sorted(dict.fromkeys(entry["unmatched"]), key=int):
        hits = [
            h for h in cross_matches(pid, entry["titles"].get(pid, ""), entry["roj"])
            if (h[2] != "题目同名") == verified
        ]
        if not hits:
            continue
        links = "、".join(
            f"[ROJ {rid}]({ROJ_SHOW.format(pid=rid)})（{rtitle}）" for rid, rtitle, _ in hits
        )
        why = "；".join(dict.fromkeys(w for _, _, w in hits))
        rows.append(f"| [{pid}]({YBT_SHOW.format(pid=pid)}) | {entry['titles'].get(pid, '')} | {links} | {why} |")
    return rows


def set_region(entry: dict, total_items: int, total_sets: int) -> str:
    """一个子单的生成区块（本篇概览 + 目录 + 正文 + 附录 A）。"""
    spec, items, covered = entry["spec"], entry["items"], entry["covered"]
    rate = f"{covered / items * 100:.0f}%" if items else "—"

    region = ["## 本篇概览", ""]
    region.append(
        f"本篇 {items} 题，本站收录 {covered}（{rate}）；一本通题目单共 {total_sets} 篇、{total_items} 题。"
    )
    region.append("")
    region.append("## 目录")
    region.append("")
    region.extend(entry["toc"])
    region.append("- [附录 A：同题异号对照](#appendix-a)")
    region.append("")
    region.extend(entry["body"])

    region.append('<a id="appendix-a"></a>')
    region.append("## 附录 A：同题异号对照")
    region.append("")
    region.append(
        "下表的题目在本篇中没有同题号的记录，但 ROJ 的其他题号下可能有同一道题"
        "（同一道经典题被多个题库收录、题号各不相同）。做题时任选其一即可。"
    )
    region.append("")
    region.append("### A.1 已核对（同一场真题，年份与组别一致）")
    region.append("")
    rows = appendix_rows(entry, verified=True)
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
    rows = appendix_rows(entry, verified=False)
    if rows:
        region.append("| 一本通题号 | 题目名称 | ROJ 中的同题 | 依据 |")
        region.append("| --- | --- | --- | --- |")
        region.extend(rows)
    else:
        region.append("（无）")
    region.append("")
    return "\n".join(region).rstrip() + "\n"


def generate() -> list[dict]:
    catalog = json.loads(CATALOG.read_text())
    titles = catalog["titles"]
    by_name = {n.text: n for n in parse_tree(catalog["menu"])}
    for top in [s["top"] for s in SETS]:
        node = by_name.get(top)
        if node is None:
            raise SystemExit(f"快照中找不到分类「{top}」，检查 scripts/ybt_catalog.json 或 SETS 配置")
        adopt_orphan_leaves(node)

    flat = []
    for top in [s["top"] for s in SETS]:
        unmerged_flat_sections(by_name[top], top, flat)
    if flat:
        raise SystemExit("分类树归并未完成，以下章节的题目无法归属：" + "、".join(flat))

    roj_titles = load_roj_titles()
    mapping = json.loads(MAPPING.read_text()) if MAPPING.exists() else {}

    entries = [build_set(spec, by_name, titles, roj_titles, mapping) for spec in SETS]
    total_items = sum(e["items"] for e in entries)
    for entry in entries:
        spec, items, covered = entry["spec"], entry["items"], entry["covered"]
        rate = f"{covered / items * 100:.0f}%" if items else "—"
        # 「算法提高篇」「高手训练篇」本身已带「篇」字，不要再补一个
        label = spec["top"] if spec["top"].endswith("篇") else spec["top"] + "篇"
        entry["head"] = TEMPLATE_HEAD.format(
            top=spec["top"], label=label, items=items, covered=covered, rate=rate, order=spec["order"]
        )
        entry["region"] = set_region(entry, total_items, len(entries))
    return entries


def set_frontmatter_values(path: Path, text: str, updates: dict[str, int]) -> str:
    """更新 frontmatter 中的 items/covered；不存在则插入，其余字段原样保留。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path} 缺少 frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise SystemExit(f"{path} frontmatter 未闭合")

    remaining = dict(updates)
    for i in range(1, end):
        for key in list(remaining):
            if re.match(rf"^{re.escape(key)}\s*:", lines[i]):
                lines[i] = f"{key}: {remaining.pop(key)}"
    for key in list(remaining):
        lines.insert(end, f"{key}: {remaining.pop(key)}")
        end += 1
    return "\n".join(lines)


def upsert_problem_set(path: Path, region: str, head: str, items: int, covered: int) -> str:
    if path.exists():
        text = path.read_text()
    else:
        text = head + "\n" + REGION_START + "\n" + REGION_END + "\n" + TEMPLATE_TAIL

    start = text.find(REGION_START)
    end = text.find(REGION_END)
    if start < 0 or end < start:
        raise SystemExit(f"{path} 缺少生成区块标记 {REGION_START} / {REGION_END}")
    text = text[: start + len(REGION_START)] + "\n\n" + region.rstrip() + "\n\n" + text[end:]
    return set_frontmatter_values(path, text, {"items": items, "covered": covered})


def main() -> int:
    args = set(sys.argv[1:])
    if "--fetch" in args:
        print("抓取 ybt.ssoier.cn 快照 ...", file=sys.stderr)
        CATALOG.write_text(json.dumps(fetch_catalog(), ensure_ascii=False, indent=1))
        print(f"已写入 {CATALOG}", file=sys.stderr)
    entries = generate()

    if "--check" in args:
        for entry in entries:
            print(f"{entry['spec']['slug']}.md  items={entry['items']} covered={entry['covered']}")
        print(
            f"合计 items={sum(e['items'] for e in entries)} "
            f"covered={sum(e['covered'] for e in entries)}"
        )
        return 0

    SETS_DIR.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        path = SETS_DIR / f"{entry['spec']['slug']}.md"
        text = upsert_problem_set(path, entry["region"], entry["head"], entry["items"], entry["covered"])
        path.write_text(text)
        print(f"已生成 {path}（{len(text.encode())} 字节，items={entry['items']} covered={entry['covered']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
