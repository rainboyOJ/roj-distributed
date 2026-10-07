#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2034《【例5.1】反序输出》数据生成器（cyaron，仓库惯例；目标 ROJ 题号 5036）
#
# 用法（在本目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
# 参考同款：problems/1000/data.py（IO(file_prefix="problem", data_id=i) + output_gen("../std")）、
#           .ybt-import/staging/2023/data.py（分层 + 生成期自检）。
#
# ---------------------------------------------------------------------------
# 题意（content.md；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2034 本轮实抓核对，
#       时间限制 1000 ms / 内存限制 65536 KB，题面与 content.md 逐字一致）：
#   【题目描述】输入 n 个数，要求程序按输入时的逆序把这 n 个数打印出来，
#               已知整数不超过 100 个。也就是说，按输入相反顺序打印这 n 个数。
#   【输入】输入一行共有 n 个数，每个数之间用空格隔开。
#   【输出】如题要求：一行，共有 n 个数，每个数之间用一个空格隔开。
#   【输入样例】1 7 3 4 5      【输出样例】5 4 3 7 1
#   config.json：time 1000 ms / memory 64 MB（官方页 65536 KB，一致）。
#
# ---------------------------------------------------------------------------
# 数据范围考证（**输入个数有界、每个数的取值无界声明**，如实记录）：
#   * 题面唯一给出的定量约束是**个数**：「已知整数不超过 100 个」 ⇒ 1 ≤ n ≤ 100。
#     输入**不单独给出 n**，n 由数据里这一行的 token 数决定（这是本题考点：读到 EOF 结束）。
#   * 题面**未声明每个数的取值范围/符号/类型**（无【提示】【数据规模】节，官方页同样没有）。
#     按仓库惯例（staging/2023、2069、2056 的先例）自定**工作范围**并如实记录：
#         主档： -10000 ≤ x ≤ 10000   的十进制整数（点数 1~9；含负数，禁前导零）
#         极值档：x ∈ {INT_MIN, INT_MAX, 0, ±10000}（点 10，覆盖「整数」的字面上限）
#     依据：① 本题算法（读入 + 逆序回显）与方法/符号/量级完全无关，任何按 int 读入的
#           正解（scanf("%d") / cin >> int）对 int32 全域都正确，故极值档**不会误杀正解**，
#           反而能逮住「用 short / 按字符比较 / 只读一位」这类退化实现；
#           ② 主档取 ±10000 与同册入门题（2023 的 0..1000、2069 的 0..10000）同一量级。
#     风险（已写入 gen-report.md）：若评测方数据实际只含小正整数，点 10 的极值仍落在
#           「整数」字面范围内、不越界；如维护者希望更保守，只需把点 10 的 EXTREME 档
#           换成主档小值，其余 9 点不受影响。
#   * 数据**必须是单行**（题面「输入一行」）：外部来源 [4]
#     （https://blog.csdn.net/strawberrytreea/article/details/124337320）用
#     `cin >> a[i]; if (getchar() == '\n') break;` 判定结束 —— 要求行末有 '\n'。
#     本生成器因此固定「单行 + 单个空格分隔 + 行末恰一个 '\n'、无行末空格」。
#
# ---------------------------------------------------------------------------
# 分层设计（10 个测试点，从最小铺到顶格；每点规模与设计意图逐条注明）：
#   点 1  边界层  n=1，[0]                     —— 最小个数；逆序退化为单元素；
#                                                「答案为 0 / 输出恰为 '0'」的极端
#   点 2  边界层  n=2，[-10000, 10000]          —— 最小非平凡规模 + 主值域两端（负/正）；
#                                                输出 "10000 -10000"（首尾互换，手算可核）
#   点 3  边界层  题面【输入样例】1 7 3 4 5      —— 题面声明的特殊值，与【输出样例】
#                                                 5 4 3 7 1 逐字节比对（生成期断言）
#   点 4  小规模随机  n ∈ [2,8]，x ∈ [-99,99]     —— 可手算验证的量级
#   点 5  中等规模随机 n=30，x ∈ [-1000,1000]     —— 范围中间档
#   点 6  中等规模随机 n=50，x ∈ [-10000,10000]   —— 主值域顶格 + 重复值自然出现
#   点 7  大规模随机  n=80，x ∈ [-10000,10000]    —— 接近个数上限
#   点 8  大规模随机  n=99（上限 −1），x ∈ [-10000,10000] 随机，强制含 0
#   点 9  顶格层   n=100（个数上限），严格递增 0,1,…,99 —— 最坏顺序结构
#                                                 （反序后须是严格递减 99,…,0；考循环方向/下标）
#   点 10 顶格层   n=100（个数上限），按 [INT_MIN, INT_MAX, 0, 10000, -10000] 循环填充
#                                                 —— 值域极端（int32 两极）+ 重复值（每值 20 次）
#                                                 + 正负交替 + 个数顶格
#   注：本题输入是无序的一行整数，不存在「多组数据/组数 T」的分层；10 个点中
#       3 个精确构造、1 个结构构造、2 个边界构造、4 个不同档位随机，无「全小随机」问题。
#
# 随机性：随机点使用固定种子（2034 + 点号），逐字节可复现。
# 自检（本文件末尾统一执行）：
#   1) Python 独立预测每组期望输出（列表反转 + 数字转字符串 + 单个空格 + '\n'，
#      与 std 的「数组下标逆序 + printf」是两条无关路径），与 problemN.out 逐字节比对；
#   2) 采样核对 10 个点的**逆序性质**（out 的 token 序列 == in 的 token 序列反转）；
#   3) 校验每组 .in 是**单行**（恰一个 '\n' 且位于末尾）、无行末空格、token 数 = 设计个数；
#   4) 校验 .in/.out 成对齐全（10 组）、样例点与题面样例逐字节一致。

from cyaron import *  # 引入CYaRon的库

import os
import random

INT_MIN = -2147483648
INT_MAX = 2147483647

SAMPLE_IN = [1, 7, 3, 4, 5]           # 题面【输入样例】
SAMPLE_OUT = "5 4 3 7 1\n"            # 题面【输出样例】

# ---------------------------------------------------------------------------
# 构造 10 组（vals 列表；note 写设计意图）
# ---------------------------------------------------------------------------
cases = []  # [(data_id, vals, note)]


def add(data_id, vals, note):
    assert 1 <= len(vals) <= 100, "点 %d：个数 %d 超出题面上限 1..100" % (data_id, len(vals))
    assert data_id == len(cases) + 1, "data_id 必须连续递增"
    for v in vals:
        assert INT_MIN <= v <= INT_MAX, "值 %r 超出 int32" % v
    cases.append((data_id, vals, note))


# ---- 点 1-2：边界层 ----
add(1, [0],
    "边界层：n=1（最小个数），值取下界 0 —— 逆序退化为单元素，输出恰为 '0'（答案为 0 的极端）")
add(2, [-10000, 10000],
    "边界层：n=2（最小非平凡规模），主值域两端 -10000/10000 —— 输出 '10000 -10000'，手算可核")

# ---- 点 3：题面特殊值（样例） ----
add(3, list(SAMPLE_IN),
    "边界层：题面【输入样例】1 7 3 4 5（题面唯一声明的特殊值），期望输出须逐字节等于 '5 4 3 7 1\\n'")

# ---- 点 4：小规模随机（可手算） ----
random.seed(2034 + 4)
add(4, [random.randint(-99, 99) for _ in range(random.randint(2, 8))],
    "小规模随机：n∈[2,8]，x∈[-99,99] —— 可手算验证的量级")

# ---- 点 5-6：中等规模随机 ----
random.seed(2034 + 5)
add(5, [random.randint(-1000, 1000) for _ in range(30)],
    "中等规模随机：n=30，x∈[-1000,1000] —— 范围中间档")
random.seed(2034 + 6)
add(6, [random.randint(-10000, 10000) for _ in range(50)],
    "中等规模随机：n=50，x∈[-10000,10000] —— 主值域顶格，重复值自然出现")

# ---- 点 7-8：大规模随机 ----
random.seed(2034 + 7)
add(7, [random.randint(-10000, 10000) for _ in range(80)],
    "大规模随机：n=80，x∈[-10000,10000] —— 接近个数上限")
random.seed(2034 + 8)
v8 = [random.randint(-10000, 10000) for _ in range(99)]
v8[0] = 0  # 强制出现 0（「值为 0」的边界元素）
add(8, v8,
    "大规模随机：n=99（上限-1），x∈[-10000,10000]，强制含 0 —— 逼近顶格")

# ---- 点 9-10：顶格层 ----
add(9, list(range(0, 100)),
    "顶格层：n=100（个数上限），严格递增 0..99 —— 最坏顺序结构，反序后须为严格递减 99..0")
add(10, [ [INT_MIN, INT_MAX, 0, 10000, -10000][i % 5] for i in range(100) ],
    "顶格层：n=100（个数上限），值按 INT_MIN/INT_MAX/0/10000/-10000 循环 —— "
    "int32 两极 + 重复值（每值 20 次）+ 正负交替")

# ---------------------------------------------------------------------------
# 生成
# ---------------------------------------------------------------------------
assert os.path.exists("../std"), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"

print("== 生成 %d 组数据 ==" % len(cases))
for data_id, vals, note in cases:
    io = IO(file_prefix="problem", data_id=data_id)  # problem{i}.in / problem{i}.out
    io.input_writeln(*vals)                          # 单行 + 空格分隔 + 行末 '\n'
    io.output_gen("../std")
    io.close()
    with open("problem%d.in" % data_id, "rb") as f:
        in_bytes = f.read()
    with open("problem%d.out" % data_id, "rb") as f:
        out_bytes = f.read()

    # ---- 自检 3：.in 必须是单行、无行末空格、token 数正确、可复现 ----
    assert in_bytes.endswith(b"\n"), "点 %d：.in 行末缺少换行" % data_id
    assert in_bytes.count(b"\n") == 1, "点 %d：.in 不是单行" % data_id
    line = in_bytes[:-1]
    assert line.strip() == line and line != b"", "点 %d：.in 含行首/行末空格" % data_id
    assert b"  " not in line, "点 %d：.in 存在连续空格" % data_id
    in_tok = line.decode().split(" ")
    assert in_tok == [str(v) for v in vals], \
        "点 %d：.in 的 token 与设计不符：%r" % (data_id, in_tok)

    # ---- 自检 1/2：Python 独立预测 + 逆序性质 ----
    expect = (" ".join(str(v) for v in reversed(vals)) + "\n").encode()
    assert out_bytes == expect, \
        "点 %d：.out 期望 %r，实际 %r" % (data_id, expect, out_bytes)
    out_tok = out_bytes.decode().split()
    assert out_tok == list(reversed(in_tok)), "点 %d：输出不是输入的逆序" % data_id
    assert not out_bytes[:-1].endswith(b" ") and b"  " not in out_bytes[:-1], \
        "点 %d：.out 存在多余空格" % data_id

    print("problem%-2d: n=%-3d 首值=%-12s 末值=%-12s -- %s"
          % (data_id, len(vals), vals[0], vals[-1], note))

# ---- 自检 4：样例点与题面样例逐字节一致 ----
with open("problem3.out", "rb") as f:
    got = f.read()
assert got.decode() == SAMPLE_OUT, \
    "problem3 输出 %r 与题面【输出样例】%r 不一致" % (got.decode(), SAMPLE_OUT)

print()
print("自检通过：10 组 .in/.out 成对齐全；每组 .in 均为单行（行末一个 '\\n'、无行末空格）；")
print("          每组 .out == Python 独立预测 == .in 的 token 反转，且无多余空格。")
print("          点 3 与题面样例逐字节一致：problem3.out = %r" % SAMPLE_OUT)
