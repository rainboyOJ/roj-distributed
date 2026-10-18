#!/usr/bin/env python3
"""lc_data_stage.py — 第二轮测试数据落盘工具（lc-data-worker 专用）。

按任务卡把 LC 生成产物 <lc_path>/in|out 映射落盘到 problems/<id>/data/：
  - 剔除 example* case；其余按文件名字典序编号 1..N（.in/.out 同步映射）
  - 单文件 >100MiB 拒绝（SKILL 硬规定）
  - 调 generate-data-manifest.py 更新 data.json
  - 写映射表 /tmp/lc-import/round2/<roj_id>.map

用法：python3 scripts/lc_data_stage.py --card /tmp/lc-import/round2/<roj_id>-<lc_id>/task-card.json
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 100 * 1024 * 1024  # 100 MiB
REPO = Path(__file__).resolve().parent.parent
LC_ROOT = Path.home() / "mycode/RBOOK_series/library-checker-problems"
MANIFEST = REPO / ".agents/skills/add-roj-problem/scripts/generate-data-manifest.py"
MAP_DIR = Path("/tmp/lc-import/round2")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card", required=True)
    args = ap.parse_args()

    card = json.load(open(args.card))
    roj_id = str(card["roj_id"])
    lc_path = LC_ROOT / card["lc_path"]
    in_dir, out_dir = lc_path / "in", lc_path / "out"
    data_dir = REPO / "problems" / roj_id / "data"

    ins = sorted(p for p in in_dir.glob("*.in") if not p.stem.startswith("example"))
    if not ins:
        print(f"ERROR 无非 example 测试点: {in_dir}", file=sys.stderr)
        return 1

    # 100MiB 护栏：裁掉超限 case（用户政策 2026：trim），.in/.out 任一超限即整点剔除
    kept, trimmed = [], []
    for in_path in ins:
        out_path = out_dir / (in_path.stem + ".out")
        if (in_path.stat().st_size > MAX_BYTES
                or (out_path.exists() and out_path.stat().st_size > MAX_BYTES)):
            trimmed.append(in_path.name)
        else:
            kept.append(in_path)
    ins = kept

    # 落盘：重建 data/，.in/.out 同编号
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True)
    mapping = []
    for k, in_path in enumerate(ins, start=1):
        out_path = out_dir / (in_path.stem + ".out")
        if not out_path.exists():
            print(f"ERROR 缺期望输出: {out_path}", file=sys.stderr)
            return 1
        shutil.copyfile(in_path, data_dir / f"{k}.in")
        shutil.copyfile(out_path, data_dir / f"{k}.out")
        mapping.append((k, in_path.name, in_path.stat().st_size, out_path.stat().st_size))

    # data.json
    r = subprocess.run([sys.executable, str(MANIFEST), "--root", "problems",
                        "--problem", roj_id], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERROR manifest 失败: {r.stderr}", file=sys.stderr)
        return 1

    # 映射表
    MAP_DIR.mkdir(parents=True, exist_ok=True)
    with open(MAP_DIR / f"{roj_id}.map", "w") as f:
        f.write(f"# roj_id={roj_id} lc_id={card['lc_id']} cases={len(ins)} trimmed={len(trimmed)}\n")
        for name in trimmed:
            f.write(f"# TRIMMED(>100MiB)\t{name}\n")
        for k, name, sin, sout in mapping:
            f.write(f"{k}\t{name}\tin={sin}\tout={sout}\n")

    total_mb = sum(m[2] + m[3] for m in mapping) / 1024 / 1024
    print(f"STAGED roj_id={roj_id} cases={len(ins)} size={total_mb:.1f}MB trimmed={len(trimmed)}[{','.join(trimmed)}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
