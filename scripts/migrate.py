#!/usr/bin/env python3
"""迁移 ROJ 题目到 new_ROJ/problems/。

只迁移白名单文件，摘除 config.json 里的 is_del 字段，
跳过 data/、data.zip、solutions/ 以及一切非白名单杂物。

用法：
    python3 scripts/migrate.py --dry-run
    python3 scripts/migrate.py
"""

import argparse
import json
import os
import re
import shutil
import sys

WHITELIST = {"content.md", "content.pdf", "config.json", "data.json", "std.cpp", "data.py"}

NON_STANDARD_DIRS = {"data", "solutions"}


def iter_problem_dirs(root):
    if not os.path.isdir(root):
        return
    for name in sorted(os.listdir(root), key=lambda s: int(s) if s.isdigit() else float("inf")):
        if not name.isdigit():
            continue
        yield name, os.path.join(root, name)


def strip_is_del(config_path, dest_path, dry_run):
    """返回 True 表示该 config 需要改写（含 is_del 字段）。"""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = f.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return False
    if not isinstance(data, dict) or "is_del" not in data:
        return False
    del data["is_del"]
    new_raw = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if not dry_run:
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(new_raw)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="/home/<user>/mycode/problems/roj")
    parser.add_argument("--dest", default="/home/<user>/mycode/new_ROJ/problems")
    parser.add_argument("--dry-run", action="store_true", help="只报告，不写任何文件")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        sys.exit(f"源目录不存在: {args.source}")

    stats = {
        "migrated": 0,
        "skipped_no_statement": 0,
        "configs_rewritten": 0,
        "files_copied": 0,
        "stray_files_skipped": 0,
    }

    for pid, src_dir in iter_problem_dirs(args.source):
        files = set(os.listdir(src_dir))
        has_statement = "content.md" in files or "content.pdf" in files
        if not has_statement:
            stats["skipped_no_statement"] += 1
            print(f"[跳过] {pid}: 无 content.md/content.pdf")
            continue

        dest_dir = os.path.join(args.dest, pid)
        if not args.dry_run:
            os.makedirs(dest_dir, exist_ok=True)

        stray = sorted(files - WHITELIST - NON_STANDARD_DIRS)
        stats["stray_files_skipped"] += len(stray)

        for name in sorted(WHITELIST & files):
            src_path = os.path.join(src_dir, name)
            dest_path = os.path.join(dest_dir, name)
            if name == "config.json" and strip_is_del(src_path, dest_path, args.dry_run):
                stats["configs_rewritten"] += 1
                print(f"  摘 is_del: {pid}/config.json")
                continue
            if not args.dry_run:
                shutil.copy2(src_path, dest_path)
            stats["files_copied"] += 1

        stats["migrated"] += 1

    print()
    print("=== 迁移报告 ===")
    print(f"源: {args.source}")
    print(f"目标: {args.dest}")
    print(f"迁移题目: {stats['migrated']}")
    print(f"跳过(无题面): {stats['skipped_no_statement']}")
    print(f"复制文件: {stats['files_copied']}")
    print(f"改写 config.json(摘 is_del): {stats['configs_rewritten']}")
    print(f"跳过的非标准文件: {stats['stray_files_skipped']}")
    print("(dry-run)" if args.dry_run else "(已写入)")


if __name__ == "__main__":
    main()
