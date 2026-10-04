#!/usr/bin/env python3
"""批次落账：queue.py done + 精确暂存本批文件 + 按批 commit（禁 push）。

仅在主 agent 独立验收通过后调用：
    batch_close.py --first 1010 --last 1019 --pids 1010 1011 ... 1019

- 对每题跑 queue.py done（tags 取 config.json，jev 数据取 .tmp/tag_drafts.json）
- git add 仅本批 10 个 config.json + 10 个 tag-report.md
- commit message: `feat(tags): <first>-<last> 补充/规范算法标签`，body: `jev一致 x/y，推翻 n`
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DRAFTS = REPO_ROOT / ".tmp" / "tag_drafts.json"


def run(cmd: list[str]) -> str:
    out = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"命令失败: {' '.join(cmd)}\n{out.stdout}{out.stderr}")
    return out.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", required=True)
    parser.add_argument("--last", required=True)
    parser.add_argument("--pids", nargs="+", required=True)
    args = parser.parse_args()
    drafts = {d["pid"]: d for d in json.loads(DRAFTS.read_text(encoding="utf-8"))["drafts"]}

    top3_ok = 0
    paths: list[str] = []
    for pid in args.pids:
        cfg_path = REPO_ROOT / "problems" / pid / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        tags = [t for t in (cfg.get("tags") or []) if isinstance(t, str) and t.strip()]
        d = drafts.get(pid) or {}
        cands = d.get("candidates") or []
        jev_tags = [c["tag"] for c in cands[:3]]
        if set(tags) & set(jev_tags):
            top3_ok += 1
        cmd = [sys.executable, str(REPO_ROOT / "scripts" / "tagging" / "queue.py"), "done", pid,
               "--tags", ",".join(tags)]
        if jev_tags:
            cmd += ["--jev-tags", ",".join(jev_tags)]
        if d.get("confidence") is not None:
            cmd += ["--confidence", str(d["confidence"])]
        cmd += ["--evidence", f"problems/{pid}/tag-report.md"]
        run(cmd)
        paths.append(f"problems/{pid}/config.json")
        paths.append(f"problems/{pid}/tag-report.md")

    total = len(args.pids)
    body = f"jev一致 {top3_ok}/{total}，推翻 {total - top3_ok}"
    run(["git", "add", "--"] + paths)
    run(["git", "commit", "-m", f"feat(tags): {args.first}-{args.last} 补充/规范算法标签", "-m", body])
    print(run(["git", "log", "--oneline", "-1"]).strip())
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
