#!/usr/bin/env python3
"""派批辅助：为一个 worker 生成单批（10 题）任务书。

唯一派发来源仍是 queue.py：本脚本只做 `queue.py claim` + 任务书生成，
返回批次首题号（用于 tab 命名）与任务书路径。

    batch.py --worker rojtag-w1 [--count 10] [--cohort missing|existing]
输出：.tmp/batch_<worker>.md
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
QUEUE = REPO_ROOT / "scripts" / "tagging" / "queue.py"
DRAFTS = REPO_ROOT / ".tmp" / "tag_drafts.json"

TEMPLATE = """# 批次任务书：new_ROJ 题目打 tag（批次首题 {first}，共 {n} 题）

工作目录：{root}
你是本批次唯一写手。一次完成下列 {n} 道题的 tag 定稿，除下述文件外不得改动任何文件，
不得 git commit / git push。子任务不得再派生子 agent。

## 每题流程

1. 读 `problems/<id>/content.md`（题面）与 `problems/<id>/config.json`（现状）。
2. 读 `.tmp/tag_drafts.json` 中该题 jev 草案（candidates 的 p 是"需要该 tag"的概率，confidence 是主类别置信度）。
3. 读 `scripts/tagging/vocabulary.json` 定规范词（只允许写 `tag` 字段的规范词本身，不许写别名）。
4. 定最终 tag 并落盘：
   - `missing` cohort（现无有效 tag）：写 **2~3 个算法 tag**（全部为规范词）；
   - `existing` cohort（已有 tag）：把别名/大小写归并到规范词（见词表 aliases），语义不变，可补缺；
     来源/难度类旧 tag（比赛题目/比赛/牛客/rbook/2023/noip/普及/模板）保留原样；
   - 置信度 <0.7 或候选相互冲突的题：自己读题定夺，可以推翻 jev；
   - 写 `config.json` 时保留其它字段与既有键序（只动 tags）：
     `python3 -c "import json;d=json.load(open(p));d['tags']=[...];json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)"`
5. 写 `problems/<id>/tag-report.md`，内容三行起：
   - `最终 tag：<tag1>、<tag2>`
   - `理由：一句话`
   - `与 jev：<一致|推翻>（jev 建议 <top3 与 p>，置信度 <confidence>）`
     判定规则：最终 tag 与 jev 中 p≥0.5 的候选有交集记「一致」，否则记「推翻」。

## 本批题目

| pid | cohort | 现有 tag | 标题 |
|-----|--------|----------|------|
{rows}

## 交付

全部 {n} 题完成后，回复一段简短要点（每题最终 tag 一览、推翻 jev 的题号及原因），
最后一行单独一行输出完成标记（严格使用本批首题号）：

    DONE {first}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="派批辅助（queue.py claim + 任务书生成）")
    parser.add_argument("--worker", required=True)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--cohort", choices=["missing", "existing"])
    args = parser.parse_args()

    cmd = [sys.executable, str(QUEUE), "claim", "--worker", args.worker, "--count", str(args.count)]
    if args.cohort:
        cmd += ["--cohort", args.cohort]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    if out.returncode != 0:
        print(out.stdout + out.stderr, file=sys.stderr)
        return out.returncode
    claimed = json.loads(out.stdout)["claimed"]
    if not claimed:
        print("队列已空，无可派题")
        return 2

    drafts = {}
    if DRAFTS.exists():
        drafts = {d["pid"]: d for d in json.loads(DRAFTS.read_text(encoding="utf-8"))["drafts"]}
    rows = []
    for row in claimed:
        pdir = REPO_ROOT / row["path"]
        try:
            cfg = json.loads((pdir / "config.json").read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            cfg = {}
        existing = [t for t in (cfg.get("tags") or []) if isinstance(t, str) and t.strip()]
        extra = "、".join(existing) if existing else "（无）"
        rows.append(f"| {row['pid']} | {row['cohort']} | {extra} | {row['title'] or cfg.get('title', '')} |")
    first = claimed[0]["pid"]
    task = TEMPLATE.format(first=first, n=len(claimed), root=str(REPO_ROOT), rows="\n".join(rows))
    task_path = REPO_ROOT / ".tmp" / f"batch_{args.worker}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(task, encoding="utf-8")
    # 附上本批 jev 摘要，方便 worker 快速定位
    lines = ["\n## jev 草案速查（完整数据在 .tmp/tag_drafts.json）\n"]
    for row in claimed:
        d = drafts.get(row["pid"])
        if d:
            top = "、".join(f"{c['tag']}({c['p']})" for c in d["candidates"][:5])
            lines.append(f"- {row['pid']}：类别 {d['category']}，置信度 {d['confidence']}，候选 {top}")
    task_path.write_text(task + "\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"first": first, "count": len(claimed),
                      "pids": [r["pid"] for r in claimed], "task": str(task_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
