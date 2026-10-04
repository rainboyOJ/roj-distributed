#!/usr/bin/env bash
# 派批循环单步：claim 10 题 -> tab 改名 -> prompt worker。
# 用法: dispatch.sh <slot> <tab_id>    例: dispatch.sh 3 wS:t4
set -u
cd ~/mycode/RBOOK_series/new_ROJ-tags
slot="$1"; tab="$2"
name="rojtag-w${slot}-g1"
out=$(python3 scripts/tagging/batch.py --worker "$name" --count 10)
if echo "$out" | grep -q '"first"'; then
  first=$(printf '%s' "$out" | python3 -c "import sys,json;print(json.load(sys.stdin)['first'])")
  pids=$(printf '%s' "$out" | python3 -c "import sys,json;print(' '.join(json.load(sys.stdin)['pids']))")
  herdr tab rename "$tab" "tag-$first" >/dev/null
  herdr agent prompt "$name" "新一批任务书：$PWD/.tmp/batch_${name}.md（批次首题 ${first}，共 10 题）。请读取并严格执行，完成后输出要点与单独一行完成标记。" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);r=d.get('result',{});a=r.get('agent',r);print('prompt:',a.get('name'),a.get('agent_status'))"
  echo "dispatched $name <- $first [$pids] tab=$tab"
else
  echo "无可派题（队列空）: $out"
fi
