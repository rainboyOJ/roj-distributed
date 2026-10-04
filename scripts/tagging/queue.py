#!/usr/bin/env python3
"""new_ROJ 打 tag 批次的 JSONL 队列（主 agent 的派发约束）。

queue.jsonl 每行一道题，是本批次唯一的派发来源：

    {"pid": "1069", "path": "problems/1069", "title": "乘方计算", "cohort": "missing",
     "status": "pending", "worker": null, "gen": 0, "tags": [], "jev_tags": [],
     "confidence": null, "note": "", "updated": "2026-10-04T12:00:00"}

状态机：
    pending --claim--> claimed --done--> done
                       claimed --review--> review
                       claimed --fail--> failed
    review/failed --reset--> pending

约束语义（主 agent 必须遵守）：
- 只派发 claim 返回的题，禁止绕过队列；
- 验收后必须 done / fail 落账；
- worker 崩溃、超时的 claimed 用 reset 回池；
- 所有变更走本工具（原子写 + flock），禁止手改 queue.jsonl。

用法：
    queue.py init [--root problems] [--queue scripts/tagging/queue.jsonl]
    queue.py claim --worker <name> --count <n> [--cohort missing|existing]
    queue.py done <pid> --tags "动态规划,数学" [--evidence <path>] [--jev-tags ...] [--confidence 0.9]
    queue.py review <pid> --reason "..."   queue.py fail <pid> --reason "..."
    queue.py reset <pid> [--all-claimed]   queue.py stats   queue.py show <pid>
"""

from __future__ import annotations

import argparse
import datetime
import fcntl
import json
import os
import pathlib
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_QUEUE = REPO_ROOT / "scripts" / "tagging" / "queue.jsonl"
STATUSES = ("pending", "claimed", "done", "review", "failed")


def now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


class Queue:
    """queue.jsonl 的唯一读写入口：读-改-整文件原子替换，flock 防并发。"""

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.lock_path = path.with_suffix(".lock")

    def __enter__(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = open(self.lock_path, "w")
        fcntl.flock(self._lock, fcntl.LOCK_EX)
        self.rows = self._read()
        return self

    def __exit__(self, *exc):
        self._lock.close()

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        rows = []
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise SystemExit(f"queue.jsonl 第 {number} 行不是合法 JSON：{error}")
        return rows

    def flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), prefix=".queue-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for row in sorted(self.rows, key=lambda r: r["pid"]):
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        os.replace(tmp, self.path)

    def get(self, pid: str) -> dict:
        for row in self.rows:
            if row["pid"] == pid:
                return row
        raise SystemExit(f"队列里没有 pid={pid}")

    def init(self, root: pathlib.Path) -> None:
        if self.rows:
            raise SystemExit(f"queue.jsonl 已有 {len(self.rows)} 行，拒绝覆盖；要重建请先删除文件")
        for config in sorted(root.glob("*/config.json")):
            pid = config.parent.name
            try:
                data = json.loads(config.read_text(encoding="utf-8"))
                title = data.get("title") or ""
                existing = [t for t in data.get("tags", []) if isinstance(t, str) and t.strip()]
            except Exception:
                title, existing = "", []
            self.rows.append({
                "pid": pid,
                "path": f"problems/{pid}",
                "title": str(title),
                "cohort": "existing" if existing else "missing",
                "status": "pending",
                "worker": None,
                "gen": 0,
                "tags": existing,
                "jev_tags": [],
                "confidence": None,
                "note": "",
                "updated": now(),
            })
        self.flush()
        print(f"初始化 {len(self.rows)} 题 -> {self.path}")


def cmd(args: argparse.Namespace) -> None:
    queue_path = pathlib.Path(args.queue).resolve()
    with Queue(queue_path) as q:
        if args.command == "init":
            root = pathlib.Path(args.root)
            if not root.is_absolute():
                root = REPO_ROOT / root
            q.init(root)
            return

        if args.command == "claim":
            if not args.worker:
                raise SystemExit("claim 需要 --worker")
            pool = [r for r in q.rows if r["status"] == "pending"]
            if args.cohort:
                pool = [r for r in pool if r["cohort"] == args.cohort]
            picked = pool[: args.count]
            for row in picked:
                row["status"] = "claimed"
                row["worker"] = args.worker
                row["gen"] += 1
                row["updated"] = now()
            q.flush()
            print(json.dumps({"claimed": picked}, ensure_ascii=False, indent=2))
            return

        if args.command == "show":
            print(json.dumps(q.get(args.pid), ensure_ascii=False, indent=2))
            return
        if args.command == "stats":
            counts: dict[str, int] = {}
            cohorts: dict[str, int] = {}
            for r in q.rows:
                counts[r["status"]] = counts.get(r["status"], 0) + 1
                if r["status"] != "done":
                    cohorts[r["cohort"]] = cohorts.get(r["cohort"], 0) + 1
            print(json.dumps({"total": len(q.rows), "status": counts, "not_done_by_cohort": cohorts},
                             ensure_ascii=False, indent=2))
            return

        row = q.get(args.pid)
        if args.command == "done":
            if row["status"] not in ("claimed", "review"):
                raise SystemExit(f"只有 claimed/review 能 done，当前 {row['status']}")
            tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
            if not 1 <= len(tags) <= 5:
                raise SystemExit(f"最终 tag 数必须 1~5 个，实际 {len(tags)}")
            row["tags"] = tags
            if args.jev_tags:
                row["jev_tags"] = [t.strip() for t in args.jev_tags.split(",") if t.strip()]
            if args.confidence is not None:
                row["confidence"] = args.confidence
            if args.evidence:
                row["note"] = f"evidence={args.evidence}"
            row["status"] = "done"
        elif args.command in ("review", "fail"):
            if row["status"] != "claimed":
                raise SystemExit(f"只有 claimed 能 {args.command}，当前 {row['status']}")
            row["status"] = args.command
            row["note"] = args.reason or ""
        elif args.command == "reset":
            if args.all_claimed:
                for r in q.rows:
                    if r["status"] == "claimed":
                        r["status"], r["worker"] = "pending", None
                        r["updated"] = now()
                q.flush()
                print("已把全部 claimed 回池")
                return
            if row["status"] not in ("claimed", "review", "failed"):
                raise SystemExit(f"当前状态 {row['status']} 不需要回池")
            row["status"], row["worker"] = "pending", None
        row["updated"] = now()
        q.flush()
        print(f"{args.pid} -> {row['status']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="new_ROJ tag 批次 JSONL 队列")
    parser.add_argument("command", choices=["init", "claim", "done", "review", "fail", "reset", "show", "stats"])
    parser.add_argument("pid", nargs="?")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--root", default="problems")
    parser.add_argument("--worker")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--cohort", choices=["missing", "existing"])
    parser.add_argument("--tags")
    parser.add_argument("--jev-tags")
    parser.add_argument("--confidence", type=float)
    parser.add_argument("--evidence")
    parser.add_argument("--reason")
    parser.add_argument("--all-claimed", action="store_true")
    args = parser.parse_args()
    if args.command in ("done", "review", "fail", "reset", "show") and not args.pid and not args.all_claimed:
        parser.error(f"{args.command} 需要 pid")
    cmd(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
