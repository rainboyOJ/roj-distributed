#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1804《最大真因数》分层测试数据生成器
#
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：.ybt-import/staging/1222/data.py、1671/data.py（cyaron 写 .in）。
#
# 题意：给定 l, r（1<=l<=r），求 [l,r] 内所有**合数**的最大真因数之和。
#       合数 n 的最大真因数 = n / spf(n)（spf 为最小质因子）。
# 数据范围（题面【数据规模与约定】子任务表，r 上限 5×10^9）：
#   点 1  r<=100          点 2  r<=1000        点 3  r<=10^4        点 4  r<=10^5
#   点 5  r<=5×10^6       点 6  r<=10^7        点 7  r<=10^9 且 r-l<=10^6
#   点 8  r<=5×10^9       点 9  r<=10^9        点 10 r<=5×10^9
#
# ---- 分层策略（10 组，每组一行 l r；规模从最小铺到顶格，逐点贴合子任务上限）----
#   点 1  边界层：l=1（下界）+ r=100（子任务 1 上限），最小规模。
#   点 2  小规模：r=1000（子任务 2 上限），并回归**题面样例 2**（101 1000 -> 163446）。
#   点 3  小规模：r=10^4（子任务 3 上限）。
#   点 4  中等规模：r=10^5（子任务 4 上限）。
#   点 5  大规模：r=5×10^6（子任务 5 上限，r 顶格）。
#   点 6  大规模：r=10^7（子任务 6 上限，r 顶格）。
#   点 7  大值窄区间：180208 975313（子任务 7：r<=10^9 且 r-l=795105<=10^6），
#         并回归**题面样例 3**（-> 151642139152）。
#   点 8  顶格（最大前缀区间）：1 5000000000（子任务 8/10：r=5×10^9 取满、l=1 取最小
#         => 区间最宽，是 std 的最大规模点）。
#   点 9  顶格（大范围）：1 1000000000（子任务 9：r<=10^9，l=1 最大前缀区间）。
#   点 10 顶格（双端近上限）：2500000000 5000000000（子任务 10：l,r 均贴近 5×10^9），
#         并回归**题面样例 5**（-> 3094668961678105770）。
#
#   题面样例 1（1 10）与样例 4（339762200 340762189）不单独占点，已在 gen-report.md
#   的「样例验证」一节逐条用 std 复算通过（与题面输出逐字节一致）。
#
# ⚠ cyaron 的 output_gen 曾出现「写缓冲未 flush -> 0 字节 .out」的隐患；
#   本生成器**不用 output_gen**：.in 由 cyaron 写后显式 flush+close，
#   .out 一律用 subprocess 显式跑 std 产出，并断言 .out 非空、行数恰为 1（本题恒有解）。

import os
import subprocess
import sys

from cyaron import IO  # 引入 CYaRon 的库

STD = "../std"          # 由 `g++ -O2 -std=c++17 std.cpp -o std` 生成（相对 data/ 目录）
R_MAX = 5 * 10 ** 9     # 题面 r 上限

# (点号, l, r, 说明)
CASES = [
    (1, 1, 100, "边界层：l=1 下界 + r=100（子任务 1 上限），最小规模"),
    (2, 101, 1000, "小规模：r=1000（子任务 2 上限）；题面样例 2 回归 -> 163446"),
    (3, 1, 10000, "小规模：r=10^4（子任务 3 上限）"),
    (4, 1, 100000, "中等规模：r=10^5（子任务 4 上限）"),
    (5, 1, 5000000, "大规模：r=5×10^6（子任务 5 上限，r 顶格）"),
    (6, 1, 10000000, "大规模：r=10^7（子任务 6 上限，r 顶格）"),
    (7, 180208, 975313, "大值窄区间：r<=10^9 且 r-l<=10^6（子任务 7）；题面样例 3 回归 -> 151642139152"),
    (8, 1, 5000000000, "顶格（最大前缀区间）：r=5×10^9 取满、l=1 最小（子任务 8/10），std 最大规模点"),
    (9, 1, 1000000000, "顶格（大范围）：r<=10^9（子任务 9），l=1 最大前缀区间"),
    (10, 2500000000, 5000000000, "顶格（双端近上限）：l,r 均贴近 5×10^9（子任务 10）；题面样例 5 回归 -> 3094668961678105770"),
]

# ---------------- 自检 1：分层合法（组数、范围、r 上限、l<=r）----------------
assert len(CASES) == 10, "必须恰好 10 个测试点"
assert [c[0] for c in CASES] == list(range(1, 11)), "点号须为 1..10"
for idx, l, r, _note in CASES:
    assert 1 <= l <= r <= R_MAX, "点 %d 越界: l=%d r=%d" % (idx, l, r)


def run_std(l, r):
    """显式用 std 跑出输出（规避 cyaron output_gen 的缓冲隐患）。"""
    proc = subprocess.run(
        [STD], input=("%d %d\n" % (l, r)).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert proc.returncode == 0, "std 退出码 %d: %s" % (proc.returncode, proc.stderr.decode())
    return proc.stdout.decode()


def main():
    if not os.path.exists(STD):
        sys.exit("找不到 %s，请先编译 std.cpp（g++ -O2 -std=c++17 std.cpp -o std）" % STD)

    answers = {}
    for idx, l, r, note in CASES:
        # 1) 写 .in（cyaron），显式 flush + close
        io = IO(file_prefix="problem", data_id=idx, disable_output=True)
        io.input_writeln(l, r)
        io.input_file.flush()
        io.input_file.close()
        in_name = "problem%d.in" % idx
        assert os.path.getsize(in_name) > 0, "%s 为空" % in_name

        # 2) 显式用 std 产 .out
        out = run_std(l, r)
        out_name = "problem%d.out" % idx
        with open(out_name, "w") as f:
            f.write(out)
            f.flush()
            os.fsync(f.fileno())

        # 3) 断言 .out 非空、行数恰为 1（本题恒有解，输出单个整数）
        size = os.path.getsize(out_name)
        assert size > 0, "%s 为 0 字节（std 未产出输出）" % out_name
        lines = [ln for ln in out.splitlines() if ln.strip() != ""]
        assert len(lines) == 1, "%s 行数 %d != 1" % (out_name, len(lines))
        assert lines[0].lstrip("-").isdigit(), "%s 输出非整数: %r" % (out_name, lines[0])
        answers[idx] = int(lines[0])

    # 自检 2：答案单调性 —— 均为 l=1 时，r 越大前缀区间答案必非降。
    #   按 r 从小到大排：点 1(100) < 3(1e4) < 4(1e5) < 5(5e6) < 6(1e7) < 9(1e9) < 8(5e9)
    l1_by_r = [1, 3, 4, 5, 6, 9, 8]
    assert all(CASES[i - 1][1] == 1 for i in l1_by_r), "自检 2 假设这些点 l=1"
    assert [CASES[i - 1][2] for i in l1_by_r] == sorted(CASES[i - 1][2] for i in l1_by_r)
    vals = [answers[i] for i in l1_by_r]
    assert vals == sorted(vals), "l=1 前缀答案未随 r 单调非降: %s" % vals

    # 自检 3：与题面样例逐字节对照（嵌在数据里的样例点）
    sample_expect = {2: 163446, 7: 151642139152, 10: 3094668961678105770}
    for idx, exp in sample_expect.items():
        assert answers[idx] == exp, "点 %d 与题面样例不符: got %d expect %d" % (idx, answers[idx], exp)

    # ---------------- 概览输出 ----------------
    print("点  l                 r                  r-l            答案")
    for idx, l, r, _note in CASES:
        print("problem%-2d  %-16d %-16d %-14d %d" % (idx, l, r, r - l, answers[idx]))
    print("生成完毕：10 组 problem1..10.in/.out 成对齐全，.out 均非空且单行。")


if __name__ == "__main__":
    main()
