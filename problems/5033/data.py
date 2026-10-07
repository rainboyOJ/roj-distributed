#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2031《【例4.17】四位完全平方数》数据生成器（目标 ROJ 题号 5033）
#
# 题面：输出所有形如 aabb 的四位完全平方数（即前两位数字相等，后两位数字也相等）。
#   【输入】无（【输入样例】为占位文字「无」）；
#   【输出】由小到大输出，每个数占一行。
#   限制：time 1000 ms / memory 64 MB（config.json；官方页 65536 KB，两者一致）。
#   答案：7744 = 88^2，且是**唯一**解（见下方独立穷举与来源核对）。
#
# ---------------------------------------------------------------------------
# 为什么只生成 1 组数据（无输入题的处理，语料惯例）
# ---------------------------------------------------------------------------
#   本题**无任何输入**：任何测试点的 .in 都是空文件、.out 恒为同一份固定输出
#   （只有 7744 一个数），10 个测试点内容会完全雷同（既不增加覆盖也不增加区分度）。
#   按任务书「无输入的题目（输出恒定）按语料惯例只生成 1 组 problem1.in/.out
#   （参考 problems/5006/data.py）」执行：只生成 problem1。
#   语料先例：problems/5006（Hello World，1 组）、staging/2025（例4.11 体操队，1 组）、
#   staging/2029（例4.15 水仙花数，1 组）。
#
#   通用分层清单在本题目下的**等价落点**（如实说明，不是省略）：
#   - 「点 1-2 边界层（全最小/全最大/答案为 0 或 1 的极端/题面特殊值）」不适用（无输入量），
#     等价对象是**答案集合的边界**：候选区间两端 1000（=aabb 的最小可能，非解）与 9999
#     （aabb 的最大可能，非解）、平方根区间两端 32^2=1024 与 99^2=9801（均非 aabb 形）、
#     以及唯一解 7744 的邻域（7700、7743、7745、7799 均非解）。
#   - 「点 3-8 小/中/大规模随机」不适用：没有输入量可供铺开规模。
#   - 「点 9-10 顶格层（最坏结构）」的等价物是**全域穷举**：
#     把 [1000,9999] 的全部 9000 个数、以及全部 90 个 aabb 形候选（a∈[1,9], b∈[0,9]）
#     都过一遍，验证解集恰为 {7744}（无遗漏、无多解），等价于规模上的「顶格」。
#   - 「多组数据的组数分层」不适用：本题连单组输入都没有。
#
# 生成方式：IO(file_prefix="problem", data_id=1) + io.output_gen("../std")，
#   与 problems/5006/data.py、staging/2025/data.py、staging/2029/data.py 完全一致。
# 可复现性：本题无随机量，重复运行结果逐字节相同（确定性）。
#
# 自检（文件末尾）：
#   1) Python 独立参照：构造全部 90 个 aabb 形候选，逐个数判定完全平方；
#   2) 全域穷举：扫 [1000,9999] 全部 9000 个数（数字字符串判 aabb + isqrt 判平方），
#      断言两路结果一致且恰为 [7744]，并断言 7744 = 88^2；
#   3) 边界断言：1000 / 9999 / 1024 / 9801 / 7700 / 7743 / 7745 / 7799 均非解；
#   4) 生成后**再核对**落地文件：problem1.in 为空文件、problem1.out 恰为 b"7744\n"
#      （防止漏编译 ../std 时 cyaron 静默产出空 .out 的坑）。

from cyaron import *  # 引入CYaRon的库

import math
import os

# ---- 参照路径 1：构造全部 aabb 形候选（a∈[1,9] 首位非 0，b∈[0,9]），判完全平方 ----
AABB_CANDIDATES = [a * 1100 + b * 11 for a in range(1, 10) for b in range(0, 10)]
ALL_AABB = sorted(AABB_CANDIDATES)
assert len(ALL_AABB) == 90, "aabb 形四位数（1000~9999，首位非 0）应恰有 90 个"


def is_perfect_square(n):
    """整数平方根判定（无浮点）。"""
    r = math.isqrt(n)
    return r * r == n, r


solution = [n for n in ALL_AABB if is_perfect_square(n)[0]]
assert solution == [7744], "aabb 四位完全平方数应恰为 [7744]，实际 %r" % solution
assert is_perfect_square(7744) == (True, 88), "7744 应为 88 的平方"

# ---- 参照路径 2：全域穷举 [1000,9999]（完全不同代码路径：字符串数位 + isqrt） ----
exhaustive = []
for n in range(1000, 10000):
    s = "%04d" % n
    if s[0] == s[1] and s[2] == s[3] and is_perfect_square(n)[0]:
        exhaustive.append(n)
assert exhaustive == solution == [7744], \
    "全域穷举与 aabb 构造两条路径结论必须一致且为 [7744]，实际 %r" % exhaustive

# ---- 边界/临界断言 ----
# 候选区间两端与平方根区间两端、唯一解邻域：全部必须非解（防「端点/取整」类错误）
boundary_non_solutions = [
    1000,   # aabb 候选区间最小数（a=1,b=0），非完全平方
    9999,   # aabb 候选区间最大数（a=9,b=9），非完全平方
    1024,   # 四位平方数区间的下端点 32^2（不是 aabb 形）
    9801,   # 四位平方数区间的上端点 99^2（不是 aabb 形）
    7700, 7743, 7745, 7799,  # 唯一解 7744 的左右邻域
]
for n in boundary_non_solutions:
    assert not is_perfect_square(n)[0] or ("%04d" % n)[0] != ("%04d" % n)[1], \
        "边界候选 %d 不应是解" % n
assert [n for n in boundary_non_solutions if n in exhaustive] == [], \
    "边界候选不得出现在解集中"
assert 31 * 31 == 961 and 100 * 100 == 10000, "平方根区间 [32,99] 的两侧端点依据"
assert is_perfect_square(961)[0] and is_perfect_square(10000)[0], \
    "961 与 10000 是完全平方但不在四位区间内，std 不得输出"
assert not (961 in exhaustive) and not (10000 in exhaustive)

# 参考来源核对：9 篇一本通 2031 题解全部给出唯一解 7744 = 88^2（其中
# https://blog.csdn.net/chinajsczlymyc/article/details/122741152 的代码注释直接写明答案 7744）。

EXPECT = "".join("%d\n" % n for n in solution).encode()  # b"7744\n"
assert EXPECT == b"7744\n"

print("Python 独立参照（aabb 构造）：%r（共 %d 个）" % (solution, len(solution)))
print("Python 独立参照（全域穷举 1000~9999）：%r（共 %d 个）" % (exhaustive, len(exhaustive)))
print("边界断言：1000/9999/1024/9801/7700/7743/7745/7799 均非解；961、10000 不得被输出")

# ---- 生成唯一的 1 组数据 ----
# 无输入：problem1.in 保持为空文件；problem1.out 由 std 生成（应为 "7744\n"）。
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
assert out_bytes == EXPECT, "problem1.out 应为 %r，实际 %r" % (EXPECT, out_bytes)

print("problem1: 无输入 -> 期望输出 %r" % EXPECT.decode().replace("\n", "\\n"))
print("自检通过：aabb 四位完全平方数恰为 {7744}（7744 = 88^2，且为唯一解）；")
print("           落地核对：problem1.in = 空文件（0 字节），problem1.out = %r" % out_bytes)
