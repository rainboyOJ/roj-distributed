#!/usr/bin/env bash
# 巡检脚本：打印每个活跃 worker 的状态、完成标记与文件进度。
# 用法: inspect.sh [worker 后缀...]（默认 rojtag-w1-g1 .. rojtag-w6-g1）
set -u
cd "${WORKTREE:?请设置 WORKTREE 为 new_ROJ-tags 工作树路径}"
workers=("$@")
if [ ${#workers[@]} -eq 0 ]; then
  for w in 1 2 3 4 5 6; do workers+=("rojtag-w$w-g1"); done
fi
for name in "${workers[@]}"; do
  task=".tmp/batch_${name}.md"
  status=$(herdr agent get "$name" 2>/dev/null | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); r=d.get('result',{}); a=r.get('agent',r)
    print(a.get('agent_status','?'))
except Exception:
    print('gone')")
  done_mark=$(herdr agent read "$name" --source recent-unwrapped --lines 160 2>/dev/null | grep -oE 'DONE +[0-9A-Za-z]+' | tail -1)
  if [ -f "$task" ]; then
    pids=$(grep -oE '^\| [0-9]+ \|' "$task" | grep -oE '[0-9]+' | tr '\n' ' ')
    n=0; total=0
    for p in $pids; do
      total=$((total+1))
      if [ -f "problems/$p/tag-report.md" ]; then n=$((n+1)); fi
    done
  else
    pids=""; n=0; total=0
  fi
  echo "$name | status=$status | DONE=${done_mark:-<无>} | 报告 $n/$total | pids: $pids"
done
