#!/usr/bin/env python3
"""Library Checker 题目导入预处理（阶段 0）。

把 LC 仓库里的一道题嚼碎成 worker 任务卡：展开 @{param.X}、抽取并生成样例、
确定 ROJ ID、输出 task-card.json + statement_en.md + example_XX.in/out。
worker 只消费这些产物，不再接触 LC 仓库本身。

用法:
  python3 scripts/lc_import_prep.py \
      --lc-root ~/mycode/RBOOK_series/library-checker-problems \
      --roj-root . --out /tmp/lc-import/pilot5 \
      data_structure/unionfind string/zalgorithm ...
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---- 全系列统一口径（沿 problems/1415 先例；第二轮出数据后再按规模调整） ----
TIME_MS = 10000
MEMORY_MB = 1024

KEYWORDS = {
    "statement": "Statement",
    "constraints": "Constraints",
    "input": "Input",
    "output": "Output",
    "sample": "Sample",
}

# 中文标题与标签（标签必须取自 ROJ 现有标签词表）；后续批次在此扩充
CN_META = {
    "unionfind": ("并查集", ["数据结构", "并查集"]),
    "point_add_range_sum": ("单点加区间求和", ["数据结构", "树状数组"]),
    "staticrmq": ("静态区间最小值", ["数据结构", "倍增"]),
    "zalgorithm": ("Z 算法", ["字符串"]),
    "lca": ("最近公共祖先", ["图论", "树", "LCA"]),
}


def parse_info(text: str) -> dict:
    """解析 info.toml：title/timelimit/[params]，3.11+ 用 tomllib，否则走最小解析。"""
    try:
        import tomllib
        return tomllib.loads(text)
    except ImportError:
        pass
    info = {"params": {}}
    section = ""
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("["):
            section = s.strip("[]").strip()
            continue
        m = re.match(r"([\w.]+)\s*=\s*(.+)", s)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw[0] in "'\"":
            val = raw[1:-1]
        elif re.match(r"^-?[\d_]+$", raw):
            val = int(raw.replace("_", ""))
        else:
            val = float(raw)
        if section == "params":
            info["params"][key] = val
        else:
            info[key] = val
    return info


def expand_statement(task_md: str, params: dict, samples_md: str) -> str:
    """task.md → 中间题面：取英文、去日文、展开参数与关键字、嵌入样例块。"""
    text = task_md
    # 日文块整体移除，lang 标记清掉（英文块保留在原位）
    text = re.sub(r"@{lang\.ja}.*?@{lang\.end}", "", text, flags=re.S)
    text = text.replace("@{lang.en}", "").replace("@{lang.end}", "")

    def param_sub(m):
        name = m.group(1)
        if name not in params:
            raise KeyError(f"task.md 引用了未定义的参数 {name}")
        return str(params[name])

    text = re.sub(r"@{param\.(\w+)}", param_sub, text)
    for kw, en in KEYWORDS.items():
        text = text.replace(f"@{{keyword.{kw}}}", en)

    def example_sub(m):
        name = m.group(1)
        if name not in samples_md:
            raise KeyError(f"task.md 引用了不存在的样例 {name}")
        return samples_md[name]

    text = re.sub(r"@{example\.(\w+)}", example_sub, text)
    leftover = re.findall(r"@\{[\w.]+", text)
    if leftover:
        raise ValueError(f"模板变量残留未展开: {sorted(set(leftover))}")
    return text


def sample_block(idx: int, in_text: str, out_text: str) -> str:
    n = "" if idx == 0 else str(idx + 1)
    return (
        f"### 【输入样例{n}】\n\n```\n{in_text.rstrip()}\n```\n\n"
        f"### 【输出样例{n}】\n\n```\n{out_text.rstrip()}\n```\n"
    )


def build_problem(lc_prob_dir: Path, repo_root: Path, roj_id: int, out_dir: Path) -> dict:
    name = lc_prob_dir.name
    info = parse_info((lc_prob_dir / "info.toml").read_text(encoding="utf-8"))

    # 样例：编译标程，跑 gen/example_*.in
    example_ins = sorted((lc_prob_dir / "gen").glob("example_*.in"))
    if not example_ins:
        raise ValueError(f"{name}: gen/ 里没有 example_*.in")
    bin_dir = out_dir / "_bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    exe = bin_dir / name
    src = lc_prob_dir / "sol" / "correct.cpp"
    subprocess.run(
        ["c++", "-O2", "-std=c++17", "-o", str(exe), str(src)],
        check=True, capture_output=True,
    )

    samples_md = {}
    examples = []
    for idx, in_path in enumerate(example_ins):
        in_text = in_path.read_text(encoding="utf-8")
        proc = subprocess.run(
            [str(exe)], input=in_text.encode(), capture_output=True,
            timeout=60, check=True,
        )
        out_text = proc.stdout.decode()
        examples.append({
            "in_file": str(in_path),
            "out_file": str(in_path.with_suffix(".out")),
            "in_text": in_text,
            "out_text": out_text,
        })
        samples_md[in_path.stem] = sample_block(idx, in_text, out_text)

    statement = expand_statement(
        (lc_prob_dir / "task.md").read_text(encoding="utf-8"),
        info.get("params", {}),
        samples_md,
    )

    checker_head = (lc_prob_dir / "checker.cpp").read_text(encoding="utf-8")[:400]
    judge = "diff" if "wcmp" in checker_head else "special-judge"

    title_cn, tags = CN_META.get(name, (info.get("title", name), []))
    card_dir = out_dir / f"{roj_id}-{name}"
    card_dir.mkdir(parents=True, exist_ok=True)

    # 样例落盘为独立文件 + 内嵌题面
    example_refs = []
    for ex in examples:
        stem = Path(ex["in_file"]).stem
        (card_dir / f"{stem}.in").write_text(ex["in_text"], encoding="utf-8")
        (card_dir / f"{stem}.out").write_text(ex["out_text"], encoding="utf-8")
        example_refs.append({
            "in": str(card_dir / f"{stem}.in"),
            "out": str(card_dir / f"{stem}.out"),
        })
    (card_dir / "statement_en.md").write_text(statement, encoding="utf-8")

    card = {
        "roj_id": roj_id,
        "lc_id": name,
        "lc_path": str(lc_prob_dir),
        "repo_root": str(repo_root),
        "title_cn": title_cn,
        "title_en": info.get("title", name),
        "time_ms": TIME_MS,
        "memory_mb": MEMORY_MB,
        "tags": tags,
        "source": f"Library Checker (yosupo06) - {name}",
        "source_line": f"Library Checker（yosupo06） {name}",
        "judge": judge,
        "statement_en": str(card_dir / "statement_en.md"),
        "std_cpp": str(src),
        "examples": example_refs,
    }
    (card_dir / "task-card.json").write_text(
        json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return card


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lc-root", required=True, type=Path)
    ap.add_argument("--roj-root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--start-id", type=int, default=30000)
    ap.add_argument("problems", nargs="+", help="LC 相对路径，如 data_structure/unionfind")
    args = ap.parse_args()

    # 确定性排序 + 去重 + 存在性检查
    rels = sorted(set(args.problems))
    for rel in rels:
        if not (args.lc_root / rel / "info.toml").is_file():
            print(f"错误：{rel} 不是 LC 题目目录", file=sys.stderr)
            return 1

    # ID 连续分配（跳过已占用目录）
    used = {int(p.name) for p in (args.roj_root / "problems").iterdir()
            if p.is_dir() and p.name.isdigit()}
    ids, next_id = [], args.start_id
    for _ in rels:
        while next_id in used:
            next_id += 1
        ids.append(next_id)
        used.add(next_id)
        next_id += 1

    args.out.mkdir(parents=True, exist_ok=True)
    cards = []
    for rel, roj_id in zip(rels, ids):
        card = build_problem(args.lc_root / rel, args.roj_root.resolve(), roj_id, args.out)
        cards.append(card)
        print(f"#{roj_id}  {card['lc_id']:<24} → {card['title_cn']}"
              f"  [{card['judge']}]  样例 {len(card['examples'])} 组")

    (args.out / "batch.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n任务卡已生成：{args.out}/batch.json（{len(cards)} 题）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
