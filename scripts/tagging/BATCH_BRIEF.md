# 主任务书：new_ROJ 题目打 tag 批次（roj-tagging）

你是本批次主 agent，负责建工具、派题、监督、独立验收和按批提交。批次只有主 agent → worker 两层。

## 基本参数

- 仓库（git worktree）：`~/mycode/RBOOK_series/new_ROJ-tags`，分支 `problem-tags`（基线 `a0d0386`）
- 目标：1253 道题的 `problems/<id>/config.json` 补齐/规范 `tags` 字段
  - `missing` 963 题（无 tag 或空 tag 或非法 JSON）：打 2~3 个算法 tag
  - `existing` 290 题（已有 tag）：同义归并到规范词（如 `DFS→深度优先搜索`、`dp→动态规划`、`Trie→字典树`），可补缺，不改语义
- 唯一 workspace：（本任务书由派发器注入实际 ID）
- 并发 6；worker 模型 `real-mimo/mimo-v2.6-pro`，启动命令：
  `herdr agent start <name> --kind pi --pane <pane> -- --no-session --no-extensions --model real-mimo/mimo-v2.6-pro`
- worker tab 名 = 当前批次首题号（如 `tag-1069`）；agent 名 `<批次>-w<槽>-g<代次>`
- 提交授权：**按批 commit（每批 10 题一个 commit），禁止 push**；全量验证通过后由派发器决定推送
- 协议必读（绝对路径）：
  - `~/mycode/RBOOK_series/rbook_new_problem_solutions/.agents/skills/rbook-problem-batch-launch/SKILL.md`
  - `~/mycode/RBOOK_series/rbook_new_problem_solutions/.agents/skills/rbook-problem-batch-launch/references/supervision.md`

## 本批三条硬约束（先记住）

1. **队列约束**：唯一派发来源是 `scripts/tagging/queue.jsonl`，只能派发 `queue.py claim` 返回的题；验收后必须 `queue.py done|fail|review` 落账；worker 崩溃用 `reset` 回池；禁止手改 queue.jsonl。已实现：`scripts/tagging/queue.py`（init/claim/done/review/fail/reset/show/stats，flock+原子写，用法见文件头注释）。
2. **连续推进**：禁止在队列未清空时结束回合；每轮（≤4 个批次）结束必须在同一回合里立刻发起下一轮。只有队列空、全槽异常、或需要用户决策时才能停下。
3. **巡检纪律**：单次工具调用阻塞 ≤90 秒；完成标记容错匹配（`grep -oE 'DONE +[0-9A-Za-z]+'`，pane 渲染输出带缩进）；禁止 1200 秒级长阻塞 watch。

## Phase A：建工具（scripts/tagging/ 下，先做完再派工）

### A1. vocabulary.json（规范词表）

约 80 个规范 tag，格式：

```json
{"tags": [{"tag": "深度优先搜索", "definition": "DFS 递归/显式栈遍历状态空间",
           "aliases": ["DFS", "深度优先搜索", "dfs"], "parent": "搜索"}]}
```

- 数据源：new_ROJ 既有 179 词（`queue.py init` 前先扫 `problems/*/config.json` 的 tags）
  + rbook 高频词（参考 `~/mycode/RBOOK_series/rbook_new_problem_solutions/problems/`，其 tags 字段高频词：动态规划/模拟/字符串/数学/贪心/图论/枚举/排序/思维/计数/前缀和/最短路/数论/位运算/背包/搜索/递归/递推/并查集/构造/二分/树/BFS/DFS/矩阵/线段树/栈/堆/树状数组/二分答案/双指针/倍增/单调队列/状态压缩/最小生成树/拓扑排序/高精度/差分/剪枝/记忆化搜索/LCA/背包/二叉树/队列…）
- 只收**算法/技术类**词；来源类（`比赛题目/牛客/rbook`）与难度类（`普及`）不进词表：新题不打这类 tag，存量保留原样
- definition 一句话（jev criteria 用）；aliases 用于归并与校验

### A2. jev_tags.py（jev 直连打分，不走任何 proxy）

- 端点：`POST https://api.typesafe.ai/v1/systemone`
- 认证：`Authorization: Bearer <key>`；key 取自 `~/.typesafe/jev-lgp888.keys`（10 个 key，逐行；轮换/并发用；**绝不打印 key**）
- 请求体：`{"state": "<题面文本>", "model": "jev-latest", "questions": {<key>: {"type": "noul|choice|score", "instructions": "...", "criteria": {...}}}}`
  - `noul` = 是/否概率（criteria 里写 true/false 含义）；`choice` = 多选一（criteria 是 {选项: 说明}，最多 255 项）；`score` = 分级（criteria 是数组）
- 响应：`answers.<key>.noul`（0~1）、`answers.<key>.choice` + `probabilities` + `confidence`
- 每题一次调用：1 个 `choice`（主类别）+ 8~12 个 `noul`（候选 tag，按粗分类筛出的候选）；state 用 `config.json` 的 title + `content.md` 的【题目描述】+【输入】【输出】段
- 韧性：422/429/529 退避重试（指数退避，≤5 次）；key 轮换；单 key 连续失败 3 次换下一个；全 key 失败才报告暂停
- 输出：`.tmp/tag_drafts.json`，每题 `{pid, title, category, candidates: [{tag, p}], confidence}`
- 先用 5 题干跑验证（LIS 类题 `is_dp` 应 ≥0.8），再全量跑

### A3. validate_tags.py（验收门禁）

- 校验：`config.json` 是合法 JSON；`tags` 是 1~5 个字符串；全部 ∈ 规范词表（或属于保留的来源/难度类旧 tag）；`missing` cohort 每题 2~3 个；无重复（归并后）
- 报表：分布 top30、每题 tag 数分布、按 cohort 的完成率；退出码非 0 = 有失败项（列 pid+原因）

### A4. 先修数据

`problems/8009/config.json`、`problems/8012/config.json` 是非法 JSON（本次发现），先最小修复（还原 title/time/memory 等字段，不顺手加别的）。

## Phase B：jev 全量初判

`queue.py init` 入队（1253 行）→ `jev_tags.py` 全量出 draft → 在状态文件里记录每题 jev 建议与置信度。

## Phase C：worker 批次（每批 10 题）

派题（只能从 `queue.py claim --worker <name> --count 10` 返回的题派）：

- worker 任务：读 `content.md` + jev draft + `vocabulary.json`，定最终 2~3 个 tag
  - 低置信（confidence < 0.7）或多标签冲突的题：自己读题定夺，可推翻 jev
  - `existing` 题：按 aliases 归并到规范词，语义不变；来源/难度类旧 tag 保留
  - 写 `problems/<id>/config.json` 的 `tags`（**保留其它字段与既有顺序**），report 写 `problems/<id>/tag-report.md`（最终 tag、理由一句、与 jev 是否一致）
- 交付：报告要点 + `DONE <批次号>`（单独一行）
- 你独立验收：跑 `validate_tags.py`（只查该批）+ 抽 2 题读 config.json 与报告 → `queue.py done` 落账 → 按批 commit
  - commit message：`feat(tags): <pid1>-<pid10> 补充/规范算法标签`，只暂存该批 10 个 config.json + 10 个 tag-report.md
  - 不通过：`queue.py review|fail` + 具体返修意见给同一 worker

## Phase D：收尾（队列清空后）

1. `validate_tags.py` 全量（必须 exit 0）+ 分布报表
2. `npm run` 无相关测试；如 web 有测试则跑 `web` 的测试（`cd web && npm test`，失败则报告不修）
3. 汇报：完成/异常/待复核计数、每 cohort 完成率、tag 分布 top30、与 jev 不一致的题数、重启次数
4. **不 push**（派发器决定）；workspace 与 tab 保留

## 与 jev 不一致的统计要求

每批 commit 时在 message body 记：`jev一致 x/y，推翻 n`；最终报表汇总——这决定后面要不要调词表。
