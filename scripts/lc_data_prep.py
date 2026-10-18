#!/usr/bin/env python3
"""lc_data_prep.py — 第二轮任务卡生成器（主线程专用）。

读 batch.json（batch2 + pilot5）+ SPJ 三档表 /tmp/lc-import/round2/spj_tiers.json，
为 252 题生成 /tmp/lc-import/round2/<roj_id>-<lc_id>/task-card.json。

用法：python3 scripts/lc_data_prep.py
"""
import json
import sys
import tomllib
from pathlib import Path

LC_ROOT = Path.home() / "mycode/RBOOK_series/library-checker-problems"
OUT = Path("/tmp/lc-import/round2")
TIERS = OUT / "spj_tiers.json"


def load_cards():
    cards = []
    for f in ("/tmp/lc-import/batch2/batch.json", "/tmp/lc-import/pilot5/batch.json"):
        p = Path(f)
        if p.exists():
            cards += json.load(open(p))
    return cards


def expected_cases(lc_path: Path):
    """info.toml [[tests]] 期望 case 数（剔除 example*）。"""
    info = tomllib.loads((lc_path / "info.toml").read_text())
    total = 0
    for t in info.get("tests", []):
        if Path(t["name"]).stem.startswith("example"):
            continue
        total += int(t["number"])
    return total


def main() -> int:
    if not TIERS.exists():
        print(f"ERROR 缺三档表 {TIERS}", file=sys.stderr)
        return 1
    tiers = json.load(open(TIERS))  # {roj_id: "diff"|"spj"}

    n = 0
    for card in load_cards():
        roj_id = str(card["roj_id"])
        lc_id = card["lc_id"]
        lc_path = Path(card["lc_path"])  # 相对 LC_ROOT
        tier = tiers.get(roj_id)
        if tier is None:
            print(f"ERROR {roj_id} 缺档位", file=sys.stderr)
            return 1
        d = OUT / f"{roj_id}-{lc_id}"
        d.mkdir(parents=True, exist_ok=True)
        json.dump({
            "roj_id": int(roj_id),
            "lc_id": lc_id,
            "lc_path": str(lc_path),
            "spj_tier": tier,
            "checker_path": str(LC_ROOT / lc_path / "checker.cpp"),
            "expected_cases": expected_cases(LC_ROOT / lc_path),
            "note": "example* 不落盘；其余 case 按文件名字典序 -> 1..N",
        }, open(d / "task-card.json", "w"), ensure_ascii=False, indent=2)
        n += 1
    print(f"生成任务卡 {n} 张 -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
