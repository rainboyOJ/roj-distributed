#!/usr/bin/env python3
"""tag 验收门禁 + 报表（new_ROJ tag 批次）。

校验（逐题）：
  1. config.json 是合法 JSON；
  2. tags 是 1~5 个非空字符串；
  3. 每个 tag ∈ 规范词表（vocabulary.json 的规范词），或属于保留的来源/难度类旧 tag；
     只写别名（如 Trie）不算归并完成，须写规范词（字典树）；
  4. missing cohort 每题恰好 2~3 个 tag；
  5. 无重复（归并到规范词后去重比较）。

报表：tag 分布 top30、每题 tag 数分布、按 cohort 的完成率（读 queue.jsonl）。

用法：
    validate_tags.py                      # 全量
    validate_tags.py --pids 1069 1070     # 只查指定题（Phase C 批验收）
    validate_tags.py --pids-file batch.txt
退出码：0 全部通过；1 有失败项（列出 pid+原因）。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
VOCAB_PATH = REPO_ROOT / "scripts" / "tagging" / "vocabulary.json"
QUEUE_PATH = REPO_ROOT / "scripts" / "tagging" / "queue.jsonl"


def load_vocab():
    data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    canonical = {t["tag"] for t in data["tags"]}
    alias2canon = {}
    for t in data["tags"]:
        for a in t["aliases"]:
            alias2canon[a] = t["tag"]
    preserved = set(data.get("preserved_source_difficulty_tags") or [])
    return canonical, alias2canon, preserved


def load_queue() -> dict[str, dict]:
    if not QUEUE_PATH.exists():
        return {}
    rows = {}
    for line in QUEUE_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["pid"]] = row
    return rows


def check_one(pid: str, pdir: pathlib.Path, canonical, alias2canon, preserved, cohort) -> list[str]:
    problems: list[str] = []
    config_path = pdir / "config.json"
    if not config_path.exists():
        return [f"{pdir}/config.json 不存在"]
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as error:  # noqa: BLE001
        return [f"非法 JSON：{error}"]
    tags = cfg.get("tags")
    if not isinstance(tags, list):
        return ["缺 tags 字段或不是数组"]
    if not 1 <= len(tags) <= 5:
        problems.append(f"tag 数量 {len(tags)} 超出 1~5")
    for t in tags:
        if not isinstance(t, str) or not t.strip():
            problems.append(f"tag 非非空字符串：{t!r}")
            continue
        t = t.strip()
        if t in canonical:
            continue
        if t in preserved:
            continue
        if t in alias2canon:
            problems.append(f"未归并到规范词：{t!r} 应写成 {alias2canon[t]!r}")
        else:
            problems.append(f"不在规范词表：{t!r}")
    norm = [alias2canon.get(t.strip(), t.strip()) for t in tags if isinstance(t, str) and t.strip()]
    dup = [t for t, c in collections.Counter(norm).items() if c > 1]
    if dup:
        problems.append(f"归并后重复：{dup}")
    if cohort == "missing":
        # 2~3 个指算法 tag；保留的来源/难度类旧 tag（如 2023/rbook）不计入
        n_algo = sum(1 for t in tags
                     if isinstance(t, str) and t.strip() and t.strip() not in preserved)
        if not 2 <= n_algo <= 3:
            problems.append(f"missing cohort 要求 2~3 个算法 tag（不含保留的来源/难度 tag），实际 {n_algo}")
    return problems


def report(pid_rows: list[tuple[str, dict]], queue: dict[str, dict], failures: list[tuple[str, str]]) -> None:
    dist: collections.Counter = collections.Counter()
    count_dist: collections.Counter = collections.Counter()
    for pid, cfg in pid_rows:
        tags = [t for t in (cfg.get("tags") or []) if isinstance(t, str) and t.strip()]
        count_dist[len(tags)] += 1
        for t in tags:
            dist[t.strip()] += 1
    print("== tag 分布 top30 ==")
    for tag, n in dist.most_common(30):
        print(f"  {n:5d}  {tag}")
    print("== 每题 tag 数分布 ==")
    for k in sorted(count_dist):
        print(f"  {k} 个 tag: {count_dist[k]} 题")
    if queue:
        print("== 按 cohort 完成率（队列） ==")
        stat: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
        for row in queue.values():
            stat[row["cohort"]][row["status"]] += 1
        for cohort in sorted(stat):
            total = sum(stat[cohort].values())
            done = stat[cohort]["done"]
            print(f"  {cohort}: done {done}/{total} ({done / total:.1%})  明细 {dict(stat[cohort])}")
    print(f"== 校验: 通过 {len(pid_rows) - len({p for p, _ in failures})} / 失败 {len({p for p, _ in failures})} ==")
    for pid, reason in failures:
        print(f"  [FAIL] {pid}: {reason}")


def main() -> int:
    parser = argparse.ArgumentParser(description="new_ROJ tag 验收门禁")
    parser.add_argument("--pids", nargs="*")
    parser.add_argument("--pids-file")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    canonical, alias2canon, preserved = load_vocab()
    queue = load_queue()

    if args.pids_file:
        pids = [l.strip() for l in pathlib.Path(args.pids_file).read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        pids = args.pids or sorted(p.parent.name for p in (REPO_ROOT / "problems").glob("*/config.json"))

    pid_rows, failures = [], []
    for pid in pids:
        pdir = REPO_ROOT / "problems" / pid
        cohort = (queue.get(pid) or {}).get("cohort")
        try:
            cfg = json.loads((pdir / "config.json").read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            cfg = {}
        pid_rows.append((pid, cfg))
        for problem in check_one(pid, pdir, canonical, alias2canon, preserved, cohort):
            failures.append((pid, problem))

    if not args.quiet:
        report(pid_rows, queue, failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
