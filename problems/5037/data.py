#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2035《【例5.2】平移数据》数据生成器（cyaron，仓库惯例；目标 ROJ 题号 5037）
#
# 用法（在本目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
# 参考同款：problems/1000/data.py（IO(file_prefix="problem", data_id=i) + output_gen("../std")）、
#           .ybt-import/staging/2030（分层 + 生成期独立真值自检）。
#
# ---------------------------------------------------------------------------
# 题意（content.md；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2035 本轮实抓核对，
#       时间限制 1000 ms / 内存限制 65536 KB，题面与 content.md 逐字一致）：
#   【题目描述】将 a 数组中第一个元素移到数组末尾，其余数据依次往前平移一个位置。
#   【输入】第一行为数组 a 的元素个数（数组元素个数小于 50）；第二行为 n 个小于 1000 的正整数。
#   【输出】平移后的数组元素，每个数用一个空格隔开。
#   【输入样例】10 / "1 2 3 4 5 6 7 8 9 10"
#   【输出样例】"2 3 4 5 6 7 8 9 10 1"
#   config.json：time 1000 ms / memory 64 MB（官方页 65536 KB，一致）。
#
# ---------------------------------------------------------------------------
# 数据范围（题面全部定量约束，逐条落到生成器断言）：
#   * 1 <= n <= 49（题面「数组元素个数小于 50」；n 是严格小于 50 的个数 ⇒ 上限 49）。
#   * 每个元素 x 满足 1 <= x <= 999（题面「n 个小于 1000 的**正整数**」⇒ 下界 1、上界 999）。
#   * 单组输入（无组数 T）：第一行 n，第二行 n 个数，空格分隔。
#   * 题面无歧义（描述/输入/输出/样例齐全且样例自洽），未触发任务书的「停下报告」条件。
#
# ---------------------------------------------------------------------------
# 分层设计（10 个测试点，从最小铺到顶格；每点规模与设计意图逐条注明）
#
#   为什么边界层占点 1-4：任务书「边界层」清单点名要求覆盖 n=1 / n=2 / 全最小值 / 全最大值 /
#   答案为 0 或 1 的极端 / 题面声明的特殊值，而本题每个测试点只能承载「一组 (n, 数组)」，
#   这些是互斥的输入，2 个点装不下，故按 staging/2030 的先例把边界层扩为点 1-4（清单 100% 覆盖），
#   后续层次顺延（小规模 5-6、中等 7、大规模 8、顶格 9-10），规模仍严格单调铺到题面上限。
#
#   点 1  边界层  n=1，[1]                    —— 最小 n + 最小正整数值 1（全最小值）；
#                                               平移退化为恒等（答案为 1 的极端）；抓 n=1 的循环边界
#   点 2  边界层  n=2，[999, 1]                —— 最小非平凡规模 + 值域两端（上界 999 / 下界 1）；
#                                               期望输出 "1 999"（首尾互换，手算可核）
#   点 3  边界层  题面【输入样例】n=10，1..10   —— 题面唯一声明的特殊值；
#                                               期望输出须逐字节等于 "2 3 4 5 6 7 8 9 10 1\n"（生成期断言）
#   点 4  边界层  n=49（n 顶格），全 999        —— n 上限 + 值上限（全最大值）+ 全相等结构
#                                               （元素全同，抓 off-by-one / 越界 / 只改前 n-1 个的写法）
#   点 5  小规模随机  n=3，x∈[1,999]           —— 可手算验证的量级（3 个元素，全体平移一目了然）
#   点 6  小规模随机  n=8，x∈[1,20]            —— 小值域 ⇒ 重复值与相等元素密集；
#                                               首元素 1 = 最小值且可能重复出现（抓「按值查找首元素」的错法）
#   点 7  中等规模随机 n=25，x∈[1,999]          —— 范围中间档：值域全覆盖 + 元素数中等
#   点 8  大规模随机  n=45（上限 −4），x∈[1,999] —— 接近 n 上限；首元素强制 999（值上界）+
#                                               其余随机（首元素是全局唯一最大值）
#   点 9  顶格层  n=49（题面上限），严格递增 1,2,…,49
#                                             —— 最坏正序结构：答案必须恰为 "2 3 … 49 1"（生成期断言），
#                                               抓「首元素没挪到末尾 / 循环少跑一次」
#   点 10 顶格层  n=49（题面上限），严格递减 999,998,…,951
#                                             —— 最坏逆序结构 + 值域上端极端（全部 ≥951，4 位数不会越界但
#                                               贴近上界）；首元素 999 是全局唯一最大值，抓「先覆盖 a[0] 再取
#                                               首元素」的顺序错误
#   注：本题单组输入，不存在「组数 T 分层」；10 个点无重复（n 序列 1,2,10,49,3,8,25,45,49,49 中
#       内容各不相同），点 6 起规模/结构逐级放大，**不存在「10 个点全是小随机」**。
#
# 随机性：随机点使用固定种子（2035 + 点号 + 显式列表），与 cyaron/Python 版本解耦，逐字节可复现。
# 自检（本文件末尾统一执行）：
#   1) Python 独立预测每组期望输出（列表左旋一位 + 数字转字符串 + 单个空格 + '\n'，
#      与 std 的「数组原地左移 + printf」是两条无关路径），与 problemN.out 逐字节比对；
#   2) 校验每组 .in 形态：第一行 n、第二行恰 n 个 token、单个空格分隔、行末恰一个 '\n'、无行末空格；
#   3) 校验范围：1 <= n <= 49、1 <= x <= 999（题面全部定量约束）；
#   4) 点 3 的 .out 与题面【输出样例】逐字节一致；点 9 的 .out 与手算结果逐字节一致；
#   5) .in/.out 成对齐全（10 组）。

from cyaron import *  # 引入CYaRon的库

import os
import random

N_MAX = 49          # 题面「数组元素个数小于 50」
X_MIN, X_MAX = 1, 999  # 题面「小于 1000 的正整数」

SAMPLE_N = 10
SAMPLE_IN = list(range(1, 11))       # 题面【输入样例】
SAMPLE_OUT = "2 3 4 5 6 7 8 9 10 1\n"  # 题面【输出样例】

# ---------------------------------------------------------------------------
# 构造 10 组（n, vals, note）
# ---------------------------------------------------------------------------
cases = []  # [(data_id, vals, note)]


def add(data_id, vals, note):
    n = len(vals)
    assert 1 <= n <= N_MAX, "点 %d：n=%d 超出题面上限 1..%d" % (data_id, n, N_MAX)
    for v in vals:
        assert X_MIN <= v <= X_MAX, "点 %d：值 %r 超出题面范围 %d..%d" % (data_id, v, X_MIN, X_MAX)
    assert data_id == len(cases) + 1, "data_id 必须连续递增"
    cases.append((data_id, vals, note))


# ---- 点 1-4：边界层（清单 100% 覆盖，见文件头说明） ----
add(1, [X_MIN],
    "边界层：n=1（最小 n）+ 值 1（最小正整数）—— 平移退化为恒等（答案为 1 的极端）")
add(2, [X_MAX, X_MIN],
    "边界层：n=2（最小非平凡规模）+ 值域两端 999/1 —— 期望输出 '1 999'，手算可核")
add(3, list(SAMPLE_IN),
    "边界层：题面【输入样例】n=10，1..10（题面唯一声明的特殊值），期望输出须逐字节等于 %r" % SAMPLE_OUT)
add(4, [X_MAX] * N_MAX,
    "边界层：n=49（n 顶格）+ 全 999（值上限，全最大值）+ 全相等结构")

# ---- 点 5-6：小规模随机 ----
random.seed(2035 + 5)
add(5, [random.randint(X_MIN, X_MAX) for _ in range(3)],
    "小规模随机：n=3，x∈[1,999] —— 可手算验证的量级")
random.seed(2035 + 6)
v6 = [random.randint(1, 20) for _ in range(8)]
v6[5] = v6[0]  # 强制「首元素的值在后文重复出现」——抓「按值删除首元素的所有出现」的错法
add(6, v6,
    "小规模随机：n=8，x∈[1,20] —— 小值域 ⇒ 重复值/相等元素密集；"
    "且首元素的值在后文重复出现（抓「按值删除/全删」实现）")

# ---- 点 7：中等规模随机 ----
random.seed(2035 + 7)
add(7, [random.randint(X_MIN, X_MAX) for _ in range(25)],
    "中等规模随机：n=25，x∈[1,999] —— 范围中间档，值域全覆盖")

# ---- 点 8：大规模随机（接近上限） ----
random.seed(2035 + 8)
v8 = [random.randint(X_MIN, X_MAX) for _ in range(45)]
v8[0] = X_MAX  # 首元素取值上界（且为唯一最大值，抓「先覆盖 a[0]」的顺序错误）
add(8, v8,
    "大规模随机：n=45（上限-4），首元素强制 999，其余 x∈[1,999] —— 接近 n 上限")

# ---- 点 9-10：顶格层（题面上限 + 最坏结构） ----
add(9, list(range(1, N_MAX + 1)),
    "顶格层：n=49（题面上限），严格递增 1..49 —— 最坏正序结构，答案须恰为 '2 3 ... 49 1'")
add(10, list(range(999, 999 - N_MAX, -1)),
    "顶格层：n=49（题面上限），严格递减 999..951 —— 最坏逆序结构 + 值域上端极端，首元素 999 唯一最大")

# ---------------------------------------------------------------------------
# 生成
# ---------------------------------------------------------------------------
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"

print("== 生成 %d 组数据 ==" % len(cases))
for data_id, vals, note in cases:
    io = IO(file_prefix="problem", data_id=data_id)  # problem{i}.in / problem{i}.out
    io.input_write(len(vals), "\n")                  # 第一行：元素个数 n
    io.input_writeln(*vals)                          # 第二行：n 个元素（空格分隔 + 行末 '\n'）
    io.output_gen("../std")
    io.close()
    with open("problem%d.in" % data_id, "rb") as f:
        in_bytes = f.read()
    with open("problem%d.out" % data_id, "rb") as f:
        out_bytes = f.read()

    # ---- 自检 2/3：.in 形态与范围 ----
    assert in_bytes.endswith(b"\n"), "点 %d：.in 行末缺少换行" % data_id
    lines = in_bytes[:-1].split(b"\n")
    assert len(lines) == 2, "点 %d：.in 应为两行，实际 %d 行" % (data_id, len(lines))
    head, body = lines
    assert head.strip() == head and b"  " not in head, "点 %d：.in 第一行形态异常" % data_id
    assert body.strip() == body and b"  " not in body, "点 %d：.in 第二行含多余空格" % data_id
    assert head.decode().isdigit(), "点 %d：.in 第一行不是正整数" % data_id
    n_in = int(head.decode())
    tok = body.decode().split(" ")
    assert n_in == len(vals), "点 %d：.in 的 n=%d 与设计 %d 不符" % (data_id, n_in, len(vals))
    assert tok == [str(v) for v in vals], "点 %d：.in 元素与设计不符" % data_id
    assert 1 <= n_in <= N_MAX, "点 %d：n 越界" % data_id
    for v in vals:
        assert X_MIN <= v <= X_MAX, "点 %d：值越界" % data_id

    # ---- 自检 1：Python 独立预测（左旋一位） ----
    expect = (" ".join(str(v) for v in vals[1:] + vals[:1]) + "\n").encode()
    assert out_bytes == expect, "点 %d：.out 期望 %r，实际 %r" % (data_id, expect, out_bytes)
    assert not out_bytes[:-1].endswith(b" ") and b"  " not in out_bytes[:-1], \
        "点 %d：.out 存在多余空格" % data_id
    assert len(out_bytes[:-1].split(b" ")) == n_in, "点 %d：.out 元素个数不是 n" % data_id

    print("problem%-2d: n=%-3d 首值=%-4s 末值=%-4s -- %s"
          % (data_id, n_in, vals[0], vals[-1], note))

# ---- 自检 4：样例点 / 顶格结构点与手算结果逐字节一致 ----
with open("problem3.out", "rb") as f:
    got = f.read()
assert got.decode() == SAMPLE_OUT, "problem3 输出 %r 与题面【输出样例】%r 不一致" % (got.decode(), SAMPLE_OUT)
with open("problem9.out", "rb") as f:
    got9 = f.read()
assert got9.decode() == " ".join(str(v) for v in list(range(2, 50)) + [1]) + "\n", \
    "problem9 输出 %r 与手算左旋结果不一致" % got9.decode()

print()
print("自检通过：10 组 .in/.out 成对齐全；每组 .in = 第一行 n + 第二行 n 个元素（行末一个 '\\n'、"
      "无行末空格）；每组 .out == Python 独立预测（左旋一位），且无多余空格。")
print("          点 3 与题面样例逐字节一致：problem3.out = %r" % SAMPLE_OUT)
print("          点 9（顶格递增 n=49）输出与手算一致：2 3 ... 49 1")
