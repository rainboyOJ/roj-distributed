#!/usr/bin/env bash
# 在 judge 镜像内编译 LC checker（产出 Linux ELF，供 --checker 使用）。
# 用法: scripts/lc_build_checker.sh <checker.cpp> <输出名>
set -euo pipefail
SRC="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
NAME="$2"
LC_ROOT="$HOME/mycode/RBOOK_series/library-checker-problems"
OUT="/tmp/lc-import/round2/checker-bin"
mkdir -p "$OUT"
docker run --rm -v "$LC_ROOT:$LC_ROOT:ro" -v "$OUT:$OUT" roj-local-judge-lite \
  g++ -O2 -std=c++17 -I "$LC_ROOT/common" -o "$OUT/$NAME" "$SRC"
echo "$OUT/$NAME"
