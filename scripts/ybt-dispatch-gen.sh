#!/usr/bin/env bash
# 派发一本通自产子代理：每个题一个 herdr tab，pi 一次性任务（无扩展、无会话）。
#
# 用法：bash scripts/ybt-dispatch-gen.sh <pid> [pid...]   # 需已存在 .ybt-import/prompts/<pid>.md
# 约定：模型固定 small-sheep/deepseek-v4.1-flash（不要用 zzzxin）；任务书模板见 prompts/ 目录。
# 回收：子代理完成并通过复核（样例验证 + 数据齐全）后，必须关闭它占用的 tab（herdr tab close <tab_id>），不要滞留槽位。
set -euo pipefail

MODEL="small-sheep/deepseek-v4.1-flash"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

for pid in "$@"; do
  prompt="$REPO_ROOT/.ybt-import/prompts/$pid.md"
  if [ ! -f "$prompt" ]; then
    echo "缺少任务书：$prompt" >&2
    exit 1
  fi
  pane=$(cd "$REPO_ROOT" && herdr tab create --cwd "$REPO_ROOT" --label "ybt-gen-$pid" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['root_pane']['pane_id'])")
  (cd "$REPO_ROOT" && herdr pane run "$pane" \
    "pi -ne --no-session --model $MODEL @.ybt-import/prompts/$pid.md \"按照上面的任务说明执行，完成后按任务书末尾要求汇报。\"")
  echo "$pid -> $pane ($MODEL)"
done
