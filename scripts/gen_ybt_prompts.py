#!/usr/bin/env python3
"""为暂存区里未完成的题目批量生成子代理任务书 .ybt-import/prompts/<pid>.md。

任务书规范（用户要求）：
  1. 网络搜索本题的 C++ 解法/题解，改编为 std.cpp（注明来源 URL）；
  2. 测试数据按题面声明的取值范围**分层**生成：边界/小/中/大/顶格，不允许全小随机；
  3. 非水题写暴力参照实现与 std 对拍（≥100 组小数据）；
  4. 产出 gen-report.md 汇报。

用法：
    python3 scripts/gen_ybt_prompts.py            # 为所有未完成题目生成任务书
    python3 scripts/gen_ybt_prompts.py 2061 2062  # 只为指定题目生成
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_ROOT = REPO_ROOT / ".ybt-import" / "staging"
PROMPT_ROOT = REPO_ROOT / ".ybt-import" / "prompts"

TEMPLATE = """\
# 任务：为一本通 {pid}《{title}》编写标程与分层测试数据

仓库根目录：`{repo}`
暂存目录：`.ybt-import/staging/{pid}/`（已含 content.md 题面、config.json、data.json、candidate.json）
目标 ROJ 题号：{roj_id}（落地由主控脚本完成，**你不要动 problems/ 目录**）

## 约束
- 只允许创建/修改 `.ybt-import/staging/{pid}/` 内的文件；禁止任何 git 操作；禁止改动其他目录。
- 工具链：g++（C++17）、python3（已装 cyaron）。可用 web_search 搜索网络资料。
- std 必须自己编译验证后再使用，不得盲抄网络代码。

## 步骤
1. 读 `.ybt-import/staging/{pid}/content.md` 与 `config.json`，明确题意、输入输出格式、
   **数据范围**（每个输入量的取值范围、数据组数）与限制（time/memory）。
2. **网络搜索本题的 C++ 解法**：
   - 查询关键词建议：「一本通 {pid} {title} 题解」「信息学奥赛一本通 {title} 参考代码」
     「{title} 题解 C++」，可换搜洛谷/LOJ/CSDN/博客园；
   - 把搜到的思路或 AC 代码**改写**为 `std.cpp`（C++17，stdin→stdout，
     风格参考 `problems/1000/std.cpp`），文件头部注释写明参考来源 URL；
   - 多个来源结论冲突时以题面为准；题面本身有歧义时在报告里指出并停下。
3. **样例验证**：把题面【输入样例】喂给编译后的 std，输出必须与【输出样例】一致
   （忽略行末空白/浮点误差按题面约定）。不一致必须修 std。
4. 写 `data.py`：仓库惯例的 cyaron 生成器（参考 `problems/1000/data.py`），
   产出 `problem1.in/problem1.out` … `problem10.in/problem10.out`，
   用 `IO(file_prefix="problem", data_id=i)` 与 `io.output_gen("../std")`。
   **数据分层（必须执行）**：按题面数据范围把 10 个测试点从最小铺到顶格，至少覆盖：
   - 点 1-2 **边界层**：n=1 / n=2 / 全最小值 / 全最大值 / 答案为 0 或 1 的极端 / 题面声明的特殊值；
   - 点 3-4 **小规模随机**：可手算验证的量级；
   - 点 5-6 **中等规模随机**：范围中间档；
   - 点 7-8 **大规模随机**：接近上限；
   - 点 9-10 **顶格层**：取题面上限，随机或按题型构造最坏结构
     （有序/逆序、链、全相等、重复值、卡常结构、极端权值等，按题型选择）。
   每个测试点在 `data.py` 里注释写明规模与设计意图；
   **不允许 10 个点全是小随机数据**；多组数据的题目按组数分层，规模不能超过题面上限。
   **无输入的题目**（输出恒定）按语料惯例只生成 **1 组** `problem1.in/.out`
   （参考 `problems/5006/data.py`），不要生成重复的空测试点。
5. **对拍**（非水题必须做）：写 `work/brute.cpp` 暴力/朴素参照实现，
   随机小数据 **≥100 组**对拍 std，全部一致后在 gen-report.md 记录对拍结论。
   `work/brute.cpp` 保留不删。（纯模拟/公式直算的水题可免对拍，报告中说明理由。）
6. 生成数据：`g++ -O2 -std=c++17 std.cpp -o std`，然后 `mkdir -p data && cd data && python3 ../data.py`。
7. **自查**：`data/` 下 .in/.out 成对齐全（常规题 10 组，无输入题 1 组）；抽查 2 组人工核对输出合理性；
   确认最大数据规模符合 config.json 的 time/memory 限制（std 跑最大点 < 1s）。
8. 写 `gen-report.md`：题意摘要、标程来源 URL、样例验证结论、
   每组数据的层次/规模/设计意图表、对拍结果、风险点。
9. 清理编译产物（`std` 等二进制），只留 std.cpp、data.py、data/、work/、gen-report.md。

完成后回复只需四行：`gen-report.md` 路径、标程来源 URL、样例与对拍结论、数据文件清单。
"""


def main() -> int:
    pids = sys.argv[1:]
    if not pids:
        pids = sorted(
            d.name for d in STAGING_ROOT.iterdir()
            if d.is_dir() and not (d / "gen-report.md").exists()
        )
    written = []
    for pid in pids:
        staging = STAGING_ROOT / pid
        if not staging.is_dir():
            print(f"✗ {pid}: 暂存区不存在，跳过（题面未抓到，需先补题面）")
            continue
        if (staging / "gen-report.md").exists():
            continue
        cand = {}
        cand_path = staging / "candidate.json"
        if cand_path.exists():
            cand = json.loads(cand_path.read_text())
        title = cand.get("title") or "未知标题"
        roj_id = cand.get("roj_id") or "待分配"
        PROMPT_ROOT.mkdir(parents=True, exist_ok=True)
        (PROMPT_ROOT / f"{pid}.md").write_text(
            TEMPLATE.format(pid=pid, title=title, roj_id=roj_id, repo=REPO_ROOT),
            encoding="utf-8",
        )
        written.append(pid)
    print(f"✓ 生成 {len(written)} 份任务书：{', '.join(written[:20])}{' …' if len(written) > 20 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
