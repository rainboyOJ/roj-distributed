#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2029《【例4.15】水仙花数》数据生成器（目标 ROJ 题号 5031）
#
# 题面：求 100~999 中的水仙花数。若三位数 ABC 满足 ABC = A^3 + B^3 + C^3，
#       则称 ABC 为水仙花数。例如 153：1^3+5^3+3^3 = 1+125+27 = 153。
#   【输入】无（【输入样例】为占位文字「无」）；
#   【输出】由小到大输出满足条件的数，每个数占一行。
#   限制：time 1000 ms / memory 64 MB（config.json；官方页 65536 KB，两者一致）。
#
# ---------------------------------------------------------------------------
# 为什么只生成 1 组数据（无输入题的处理，语料惯例）
# ---------------------------------------------------------------------------
#   本题**无任何输入**：任何测试点的 .in 都是空文件、.out 恒为同一份固定输出
#   （153/370/371/407），10 个测试点内容会完全雷同（既不增加覆盖也不增加区分度）。
#   按任务书「无输入的题目（输出恒定）按语料惯例只生成 1 组 problem1.in/.out
#   （参考 problems/5006/data.py）」执行：只生成 problem1。
#   语料先例：problems/5006（Hello World，1 组）、staging/2060（同题，1 组）、
#   staging/2025（例4.11 体操队，1 组）。
#
#   通用分层清单在本题目下的**等价落点**（如实说明，不是省略）：
#   - 「点 1-2 边界层（全最小/全最大/答案为 0 或 1 的极端/特殊值）」不适用（无输入量），
#     等价对象是**答案集合本身的两端**：最小水仙花数 153（下界侧）与最大水仙花数 407
#     （上界侧），以及题面声明的特殊值 153（题面举例的数）；均由本文件末尾的自检 +
#     work/ 下的独立枚举复核覆盖。
#   - 「点 3-8 小/中/大规模随机」不适用：没有输入量可供铺开规模。
#   - 「点 9-10 顶格层（最坏结构）」的等价物是**全域穷举**：把 100..999 全枚举一遍
#     验证恰有 4 解（无遗漏/无多解），等价于规模上的「顶格」。
#   - 「多组数据的组数分层」不适用：本题连单组输入都没有。
#
# 生成方式：IO(file_prefix="problem", data_id=1) + io.output_gen("../std")，
#   与 problems/5006/data.py、staging/2060/data.py 完全一致。
# 可复现性：本题无随机量，重复运行结果逐字节相同（确定性）。
#
# 自检（文件末尾）：
#   1) 用 Python 独立重算答案集合（逐位枚举 A∈[1,9], B,C∈[0,9]），断言恰为 {153,370,371,407}；
#   2) 断言 100..999 中再无其他解（穷举），且 153 是其中最小者、407 是最大者；
#   3) 生成后**再核对**落地文件：problem1.in 为空文件、problem1.out 恰为期望字节串
#      （防止漏编译 ../std 时 cyaron 静默产出空 .out 的坑）。

from cyaron import *  # 引入CYaRon的库

import os

# ---- Python 独立参照：逐位枚举（与 std 的「扫描 + 取商取余」是两条独立路径） ----
solution = []
for _a in range(1, 10):        # 百位
    for _b in range(0, 10):    # 十位
        for _c in range(0, 10):  # 个位
            _n = _a * 100 + _b * 10 + _c
            if _a ** 3 + _b ** 3 + _c ** 3 == _n:
                solution.append(_n)
solution.sort()

EXPECT = "".join("%d\n" % n for n in solution).encode()

# 参考来源核对：8 篇一本通 2029 题解全部给出答案 {153, 370, 371, 407}
# （其中 https://blog.csdn.net/lwx3289765163/article/details/121340145 直接写死这四个数）
assert solution == [153, 370, 371, 407], "闭式/穷举答案应为 [153,370,371,407]，实际 %r" % solution
# 边界断言：最小解 153（题面举例值）、最大解 407，且二者都落在题面区间 100..999 内
assert solution[0] == 153 and solution[-1] == 407
assert all(100 <= n <= 999 for n in solution)
# 全域穷举断言：100..999 内的水仙花数总数恰为 4（针对「取位/循环边界」类错误）
assert len(solution) == 4

print("Python 独立参照：100~999 的水仙花数 = %s（共 %d 个）" % (solution, len(solution)))

# ---- 生成唯一的 1 组数据 ----
# 无输入：problem1.in 保持为空文件；problem1.out 由 std 生成（应为 "153\n370\n371\n407\n"）。
# 注意：io.output_gen 依赖同目录已编译好的 ../std（先 g++ -O2 -std=c++17 std.cpp -o std）。
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"
io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
io.input_write()                           # 无输入 => 空 .in
io.output_gen("../std")                    # 由 std 产出 .out

# ---- 落地核对：防止 std 未编译 / 输出异常时的静默错误 ----
# 先关闭 IO 把输出缓冲刷盘（命名文件不会被删除，见 cyaron IO.close 的实现）。
io.close()
with open("problem1.in", "rb") as f:
    in_bytes = f.read()
with open("problem1.out", "rb") as f:
    out_bytes = f.read()
assert in_bytes == b"", "problem1.in 应为空文件，实际 %r" % in_bytes
assert out_bytes == EXPECT, \
    "problem1.out 应为 %r，实际 %r" % (EXPECT, out_bytes)

print("problem1: 无输入 -> 期望输出 %r" % EXPECT.decode().replace("\n", "\\n"))
print("自检通过：100~999 恰有 4 个水仙花数 {153,370,371,407}（153 最小、407 最大）；")
print("           落地核对：problem1.in = 空文件（0 字节），problem1.out = %r" % out_bytes)
