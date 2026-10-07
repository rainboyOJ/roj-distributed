#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2025《【例4.11】体操队》数据生成器（目标 ROJ 题号 5027）
#
# 题面：校体操队排成每行 2、3、4、5、6 人时都多出 1 人，排成每行 7 人时正好不多，
#       求校体操队至少多少人。
#       输入：无（【输入】原文「如题述，无。」）；输出：一个整数，唯一确定。
#       限制：time 1000 ms，memory 64 MB（config.json）。
#
# ---------------------------------------------------------------------------
# 为什么只生成 1 组数据（无输入题的处理，语料惯例）
# ---------------------------------------------------------------------------
#   本题**无任何输入**，任何测试点的输入都是空、输出恒为同一个整数，
#   10 个测试点内容会完全雷同（既不增加覆盖也不增加区分度）。
#   按任务书「无输入的题目（输出恒定）按语料惯例只生成 1 组 problem1.in/.out
#   （参考 problems/5006/data.py）」执行：只生成 problem1。
#   语料中同类先例：problems/5006（Hello World，1 组）、staging/2060（同题，1 组）。
#
#   通用分层清单在此题下的**等价落点**（不是省略，而是转移到「答案本身」的验证）：
#   - 「边界/极端/临界构造」的对象不再是输入，而是**答案 301 的最小性与正确性**：
#       下界侧：所有 n < 301 均不满足条件（301-1 = 300 是最后一个失败候选）；
#       命中侧：301 满足全部 5 个余数条件且被 7 整除（301 = 7 × 43）；
#       周期侧：301 ≡ 301 (mod 420)，420 = lcm(60, 7)，之后解为 721、1141、…
#     以上三侧均由本文件末尾的自检 + work/ 下的独立暴力枚举实测确认（见 gen-report.md）。
#   - 「10 个点从最小铺到顶格」不适用：无输入量可供铺开规模。
#   - 「多组数据的组数分层」不适用：本题连单组输入都没有。
#
# 生成方式：IO(file_prefix="problem", data_id=1) + io.output_gen("../std")，
#   与 problems/5006/data.py、staging/2060/data.py 完全一致。
# 可复现性：本题无随机量，重复运行结果逐字节相同（确定性）。
#
# 自检（文件末尾）：先用闭式解 + 穷举断言答案的最小性，生成后**再核对**
#   problem1.in 是空文件、problem1.out 恰为 "301\n"（防止漏编译 ../std 时
#   cyaron 静默产出空 .out 的坑）。

from cyaron import *  # 引入CYaRon的库

import os
import math

# ---- 题面条件与闭式解（用于生成后的数学自检） ----
# 条件：n % k == 1 (k=2..6) 且 n % 7 == 0，求最小正整数 n。
# 记 L = lcm(2,3,4,5,6) = 60，则 n ≡ 1 (mod 60)；在 1, 61, 121, 181, 241, 301, …
# 中首个 7 的倍数是 301（301 = 7 × 43）。解集周期 = lcm(60,7) = 420。
L = math.lcm(2, 3, 4, 5, 6)          # = 60
PERIOD = math.lcm(L, 7)              # = 420


def satisfies(n):
    """题面条件的直译：每行 2..6 人都多出 1 人，且每行 7 人正好。"""
    return all(n % k == 1 for k in range(2, 7)) and n % 7 == 0


def first_solution():
    """闭式解：n = 60k+1 中首个被 7 整除者。"""
    k = 0
    while True:
        n = L * k + 1
        if n % 7 == 0:
            return n
        k += 1


ANSWER = first_solution()            # 预期 301
assert ANSWER == 301, "闭式解应为 301"
assert satisfies(ANSWER), "301 必须满足全部条件"

# ---- 生成唯一的 1 组数据 ----
# 无输入：problem1.in 保持为空文件；problem1.out 由 std 生成（应为 "301\n"）。
# 注意：io.output_gen 依赖同目录已编译好的 ../std（先 g++ -O2 -std=c++17 std.cpp -o std）。
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"
io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
io.input_write()
io.output_gen("../std")

# ---- 自检 ----
# 1) 全 1..300 不满足（301 是首个命中 ⇒ 「至少」语义成立）；
# 2) 301 满足全部条件；
# 3) 解集周期 420，下一解 721 也满足且 420 < 721 内无其他解（抽查）。
assert all(not satisfies(n) for n in range(1, ANSWER)), "存在比 301 更小的解（最小性被破坏）"
assert satisfies(ANSWER)
assert satisfies(ANSWER + PERIOD) and ANSWER + PERIOD == 721
assert all((not satisfies(n)) for n in range(ANSWER + 1, ANSWER + PERIOD)), "301 与 721 之间不应有解"

# 4) 落地文件核对：.in 必须为空、.out 必须恰为 "301\n"（防止 std 未编译时的静默空输出）
#    先关闭 IO 把输出缓冲刷盘（命名文件不会被删除，见 cyaron IO.close 的实现）。
io.close()
with open("problem1.in", "rb") as f:
    in_bytes = f.read()
with open("problem1.out", "rb") as f:
    out_bytes = f.read()
assert in_bytes == b"", "problem1.in 应为空文件，实际 %r" % in_bytes
assert out_bytes == b"301\n", "problem1.out 应为 b'301\\n'，实际 %r" % out_bytes

print("problem1: 无输入 -> 期望输出 %d" % ANSWER)
print("自检通过：1..300 全不满足；%d 满足 n%%k==1 (k=2..6) 且 n%%7==0；" % ANSWER)
print("           下一解 %d = %d + %d（420 = lcm(60,7)）；" % (ANSWER + PERIOD, ANSWER, PERIOD))
print("           落地核对：problem1.in = 空文件，problem1.out = %r" % out_bytes)
