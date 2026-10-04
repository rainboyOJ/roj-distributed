#!/usr/bin/env python3
"""批次统计：算该批与 jev 的一致/推翻数（供 commit message body 与最终报表）。

口径（两套都输出，commit 用 top3 口径）：
  top3 一致：最终 tag 与 jev 候选前 3 有交集
  p50 一致：最终 tag 与 jev 中 p≥0.5 的候选有交集（任务书里给 worker 的判定规则）

    batch_stats.py 1010 1011 ...   # 或 --file pid列表文件
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DRAFTS = REPO_ROOT / ".tmp" / "tag_drafts.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pids", nargs="*")
    parser.add_argument("--file")
    args = parser.parse_args()
    pids = list(args.pids)
    if args.file:
        pids += [l.strip() for l in pathlib.Path(args.file).read_text(encoding="utf-8").splitlines() if l.strip()]
    drafts = {d["pid"]: d for d in json.loads(DRAFTS.read_text(encoding="utf-8"))["drafts"]}
    top3_ok = p50_ok = total = 0
    overturned = []
    for pid in pids:
        cfg = json.loads((REPO_ROOT / "problems" / pid / "config.json").read_text(encoding="utf-8"))
        final = [t for t in (cfg.get("tags") or []) if isinstance(t, str)]
        d = drafts.get(pid) or {}
        cands = d.get("candidates") or []
        top3 = [c["tag"] for c in cands[:3]]
        p50 = [c["tag"] for c in cands if c["p"] >= 0.5]
        total += 1
        t3 = bool(set(final) & set(top3))
        p5 = bool(set(final) & set(p50))
        top3_ok += t3
        p50_ok += p5
        if not t3:
            overturned.append((pid, final, top3))
    print(f"total={total} top3一致={top3_ok} top3推翻={total - top3_ok} p50一致={p50_ok} p50推翻={total - p50_ok}")
    for pid, final, top3 in overturned:
        print(f"  推翻 {pid}: final={final} jev_top3={top3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
