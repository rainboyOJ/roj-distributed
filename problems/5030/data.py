#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 2028《【例4.14】百钱买百鸡》数据生成器（目标 ROJ 题号 5030）
#
# 题面：【题目描述】百钱买百鸡问题。鸡翁一，值钱五，鸡母一，值钱三，鸡雏三，值钱一，
#       百钱买百鸡，问鸡翁、鸡母、鸡雏各几何？
#       【输入】无    【输出】输出各种鸡翁、鸡母、鸡雏的数量，依次由小到大，
#                          每种情况各占一行，每行三个数之间用一个空格隔开。
#       限制：time 1000 ms，memory 64 MB（config.json；官方页 65536 KB）。
#
# ---------------------------------------------------------------------------
# 为什么只生成 1 组数据（无输入题的语料惯例）
# ---------------------------------------------------------------------------
#   本题**无任何输入**（题面【输入】原文只有一个「无」字），输出恒为同一个常量，
#   任何测试点的 .in 都是空文件、.out 都是同样 4 行；生成 10 个测试点只会得到
#   10 份逐字节相同的副本，既不增加覆盖也不增加区分度。
#   按任务书第 4 条「无输入的题目（输出恒定）按语料惯例只生成 1 组 problem1.in/.out
#   （参考 problems/5006/data.py），不要生成重复的空测试点」执行：只生成 problem1。
#   本仓库先例：problems/5006（Hello World，1 组）、staging/2060（同题，1 组）、
#               staging/2063（牛吃牧草，1 组）、staging/2025（体操队，1 组）。
#
#   同理，任务书要求的「点 1-2 边界 / 点 3-4 小随机 / 点 5-6 中随机 / 点 7-8 大随机 /
#   点 9-10 顶格」这五档分层在本题**没有可铺开的输入量**，不适用；它们在本包中的
#   等价落点是「答案本身的正确性验证」，全部由 work/stress.py 承担（详见 gen-report.md）：
#     - 边界/极端：解集里既有 0（鸡翁 0 只这一组，最容易漏）也有最大值（鸡雏 84 只）——
#                  见下方 BEFORE_WRITE 自检与 [3b] 逐组约束复核；
#     - 临界构造：c 必须被 3 整除；漏掉该判定的实现会多出 3 行（3 20 77 / 7 13 80 /
#                  11 6 83），已由 stress.py [4] 确认会被这一唯一测试点检出；
#     - 「顶格/最坏结构」：本实例的参数就是题面上限（恰好 100 钱 / 100 只），
#                  并且要输出**全部** 4 组解、顺序还要正确（顺序错/少一组都会判错）。
#
#   生成方式与 problems/5006/data.py 完全同构：
#     IO(file_prefix="problem", data_id=1) + io.input_write() + io.output_gen("../std")
#   可复现性：本题无随机量，重复运行输出逐字节相同（确定性，实测 md5 一致）。
#
# 用法：g++ -O2 -std=c++17 std.cpp -o std
#       mkdir -p data && cd data && python3 ../data.py

from cyaron import *  # 引入CYaRon的库

import os
import hashlib

# ---- 题面常量与闭式解（用于生成前/生成后的数学自检） ----
MONEY = 100      # 百钱
BIRDS = 100      # 百鸡
PEN_WENG = 5     # 鸡翁一，值钱五
PEN_MU = 3       # 鸡母一，值钱三
CHICK_PER_PEN = 3  # 鸡雏三，值钱一（不可拆卖 ⇒ 鸡雏数是 3 的倍数）


def solutions_direct():
    """题面定义直译（不做任何化简）：穷举鸡翁 a、鸡母 b，鸡雏 c 由「百鸡」定出。"""
    out = []
    for a in range(0, MONEY // PEN_WENG + 1):        # 0..20
        for b in range(0, MONEY // PEN_MU + 1):      # 0..33
            c = BIRDS - a - b
            if c < 0:
                continue
            if c % CHICK_PER_PEN != 0:               # 鸡雏必须三只一钱地买
                continue
            if PEN_WENG * a + PEN_MU * b + c // CHICK_PER_PEN == MONEY:
                out.append((a, b, c))
    return out


def solutions_algebraic():
    """独立闭式解：5a+3b+c/3=100 且 a+b+c=100 ⇒ ×3 得 14a+8b=200 ⇒ 7a+4b=100。"""
    out = []
    for a in range(0, 15):
        num = 100 - 7 * a
        if num < 0 or num % 4 != 0:
            continue
        b = num // 4
        c = BIRDS - a - b
        if c >= 0:
            out.append((a, b, c))
    return out


EXPECTED = [(0, 25, 75), (4, 18, 78), (8, 11, 81), (12, 4, 84)]

# 生成前自检：两条独立路径（枚举 / 消元闭式）必须都得到这 4 组解
assert solutions_direct() == EXPECTED, "枚举结果异常：%s" % solutions_direct()
assert solutions_algebraic() == EXPECTED, "闭式解异常：%s" % solutions_algebraic()
# 逐组复核题面两条约束 + 顺序（鸡翁严格递增 ⇒ 满足「依次由小到大」）
for (a, b, c) in EXPECTED:
    assert a + b + c == BIRDS, "百鸡约束被破坏：%s" % ((a, b, c),)
    assert c % CHICK_PER_PEN == 0 and PEN_WENG * a + PEN_MU * b + c // CHICK_PER_PEN == MONEY, \
        "百钱约束被破坏：%s" % ((a, b, c),)
assert [t[0] for t in EXPECTED] == sorted(t[0] for t in EXPECTED), "鸡翁未递增"
# 最关键的一处「边界」：`0 25 75` 这一组的鸡翁是 0（边界/极端），
# 鸡雏 84 是三列中最大数（另一个端点）；确认解集两个端点都被覆盖。
assert EXPECTED[0][0] == 0, "应包含鸡翁 0 这只下界解"
assert max(t[2] for t in EXPECTED) == 84 and EXPECTED[-1][2] == 84, "应包含鸡雏上界解"

# ---- 生成唯一的 1 组数据 ----
# 无输入 ⇒ problem1.in 是空文件；problem1.out 由 std 实时产出。
# 前置断言 ../std 已编译：否则 cyaron 会静默产出空 .out（本包实测过该坑）。
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"

io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
io.input_write()                           # 无输入：写空内容
io.output_gen("../std")                    # 输出 = 标程 stdout

# ---- 生成后落地核对（防止漏编译 / 静默空输出的坑） ----
# 先把 IO 的输出缓冲刷盘（命名文件不会被删除），再逐字节读回。
io.close()
with open("problem1.in", "rb") as f:
    in_bytes = f.read()
with open("problem1.out", "rb") as f:
    out_bytes = f.read()

assert in_bytes == b"", "problem1.in 应为空文件，实际 %r" % in_bytes
expect_out = "".join("%d %d %d\n" % t for t in EXPECTED).encode()
assert out_bytes == expect_out, "problem1.out 期望 %r，实际 %r" % (expect_out, out_bytes)
# 反向确认：这一唯一测试点能检出常见错误答案（写死成别的常量会被逮住）
for wrong in (b"", b"0 25 75\n", expect_out + b"16 0 84\n", b"301\n", b"10\n"):
    assert wrong != out_bytes, "错误答案 %r 竟与正式输出相同" % wrong

print("problem1: 无输入（空 .in） -> 期望输出 4 行、共 %d 字节" % len(out_bytes))
print("  md5(in)  = %s" % hashlib.md5(in_bytes).hexdigest())
print("  md5(out) = %s" % hashlib.md5(out_bytes).hexdigest())
print("  解集（两条独立推导一致，且逐组通过题面约束复核）：")
for t in EXPECTED:
    print("    %d %d %d    (%d*5 + %d*3 + %d/3 = %d 钱，共 %d 只)"
          % (t[0], t[1], t[2], t[0], t[1], t[2],
             PEN_WENG * t[0] + PEN_MU * t[1] + t[2] // CHICK_PER_PEN, sum(t)))
print("自检通过：枚举解 == 闭式解 == std 输出（%d 组解，鸡翁递增，含端点 0 与 84）" % len(EXPECTED))
