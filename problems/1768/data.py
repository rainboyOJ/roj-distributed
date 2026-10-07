#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1768《交换》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：.ybt-import/staging/1222/data.py、staging/2030/data.py、problems/5006/data.py
#
# 题意：给 n 与 {0..n-1} 的排列 p。q 是 {0..n-2} 的排列；把 q 依次当作「交换 s[q_i], s[q_i+1]」
#       施加到 s=[0,1,...,n-1] 上，若能恰好得到 p，则 q 是「优美的排列」。求优美的 q 的个数
#       （对 1e9+7 取模）。
# 数据范围（题面明文，config.json 记录）：30% 数据 n<=10；100% 数据 n<=50。
#       限制 time 1000 ms / memory 256 MB。
#
# ---- 分层策略（本题每组输入 = 一个测试点，故 10 个测试点各 1 组）----
#   点 1  边界层：n=1，p=[0] —— n 的下界（n-1=0 次交换的退化情形），答案 1。
#   点 2  边界层：n=2，p=[1,0] —— 最小非平凡规模，唯一合法情形，答案 1。
#   点 3  边界层：n=2，p=[0,1] —— 最小规模下的「答案 0」退化（p 不是 n-轮换，无解）。
#   点 4  样例层：n=3，p=[1,2,0] —— 题面【输入样例】逐字节回归，答案 1。
#   点 5  退化层：n=10，p=恒等排列 [0,1,...,9] —— 中等规模下的「答案 0」（全排列合法但无解），
#         检验区间 DP 的非法剪枝不会误报正解。
#   点 6  小规模随机：n=5，p 由随机 q 模拟得到（保证有解，答案>0）—— 可手算核对量级。
#   点 7  30% 顶格随机：n=10（30% 数据上界），p 由随机 q 模拟得到，答案为 4 位数。
#   点 8  中等规模随机：n=25，p 由随机 q 模拟得到，答案进入取模量级。
#   点 9  顶格层（结构性极端）：n=50，q=恒等排列 (0,1,...,48) —— 最后一次交换始终在最右端，
#         分解树是一条左链，答案恰为 1；检验顶格规模下「唯一解」结构不被多算。
#   点 10 顶格层（最坏/最大答案）：n=50，p 由随机 q 模拟得到，答案取模后为大数，检验
#         组合数取模与 DP 累加在最大规模下正确。
#
#   点 6/7/8/10 的 p 一律由「随机 q + 正向模拟」生成（而不是随机 p），因为随机 p 几乎必然无解
#   （合法 p 必须是特定结构的 n-轮换），那样数据会退化成一片 0、失去鉴别力。q 的随机种子固定，
#   结果完全可复现。
#
# 关于 .out 的生成：cyaron 的 output_gen 只写文件对象不主动 flush（关文件时才落盘），本脚本
#   用 `with IO(...) as io:` 保证 close/flush，并在生成后**显式读回 .out 断言非空且恰 1 行**，
#   同时断言 .in 格式合规（首行 n、次行恰 n 个整数、p 是 0..n-1 的排列）。

import os
import random
import subprocess
import sys

from cyaron import IO  # 引入CYaRon的库

MOD = 10 ** 9 + 7
STD = "../std"
DATA_DIR = "data"


def p_from_q(n, q):
    """按题面定义正向模拟：把 q 依次施加到 s=[0..n-1] 上，返回最终的 s。"""
    s = list(range(n))
    for i in q:
        s[i], s[i + 1] = s[i + 1], s[i]
    return s


def random_q(n, seed):
    rng = random.Random(seed)
    q = list(range(n - 1))
    rng.shuffle(q)
    return q


# ---------------- 10 个测试点 ----------------
# (点号, n, p, 说明)
P1 = (1, 1, [0], "边界层：n=1（n 的下界，0 次交换的退化情形），答案 1")
P2 = (2, 2, [1, 0], "边界层：n=2，最小非平凡规模，唯一合法情形，答案 1")
P3 = (3, 2, [0, 1], "边界层：n=2，p 为恒等排列（无解），答案 0 的最小退化")
P4 = (4, 3, [1, 2, 0], "样例层：题面【输入样例】逐字节回归，答案 1")
P5 = (5, 10, list(range(10)), "退化层：n=10，p 为恒等排列（合法但无解），答案 0 的规模版")
P6 = (6, 5, p_from_q(5, random_q(5, 1768006)), "小规模随机：n=5，p 由随机 q 模拟（有解）")
P7 = (7, 10, p_from_q(10, random_q(10, 1768007)),
      "30% 顶格随机：n=10（30% 数据上界），p 由随机 q 模拟")
P8 = (8, 25, p_from_q(25, random_q(25, 1768008)), "中等规模随机：n=25，p 由随机 q 模拟")
P9 = (9, 50, p_from_q(50, list(range(49))),
      "顶格层（结构性极端）：n=50，q 为恒等排列，分解树退化成左链，答案恰为 1")
P10 = (10, 50, p_from_q(50, random_q(50, 1768010)),
       "顶格层（最大规模随机）：n=50，p 由随机 q 模拟，答案为取模后的大数")

CASES = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]

# ---------------- 自检 1：题面范围 + p 是合法排列 ----------------
for idx, n, p, _note in CASES:
    assert 1 <= n <= 50, "点 %d：n=%d 超出题面范围 1<=n<=50" % (idx, n)
    assert len(p) == n, "点 %d：p 长度 %d != n=%d" % (idx, len(p), n)
    assert sorted(p) == list(range(n)), "点 %d：p 不是 {0..n-1} 的排列" % idx
assert len(CASES) == 10, "必须恰好 10 个测试点"

# ---------------- 生成 + 自检 2：格式与 .out 非空 ----------------
# 约定：从 staging 目录 `python3 data.py`，或从 data 目录 `python3 ../data.py`，两种方式都支持
if os.path.basename(os.getcwd()) != DATA_DIR:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.chdir(DATA_DIR)
summary = []
for idx, n, p, note in CASES:
    with IO(file_prefix="problem", data_id=idx) as io:
        io.input_writeln(n)                 # 第一行：n
        io.input_writeln(*p)                # 第二行：n 个整数，空格分开
        io.output_gen(STD)                  # .out 由 std 生成（with 退出时 close -> flush）

    # 自检 2a：.in 格式合规
    in_name, out_name = "problem%d.in" % idx, "problem%d.out" % idx
    raw_in = open(in_name, "rb").read()
    assert raw_in, "点 %d：.in 为空" % idx
    lines = raw_in.decode().split("\n")
    assert lines[0].strip() == str(n), "点 %d：.in 首行 %r != n=%d" % (idx, lines[0], n)
    assert len(lines) >= 2 and len(lines[1].split()) == n, \
        "点 %d：.in 第二行整数个数 != n" % idx

    # 自检 2b：.out 非空且恰 1 行、答案在 [0,MOD)
    raw_out = open(out_name, "rb").read()
    assert raw_out, "点 %d：.out 为 0 字节（cyaron flush 隐患）" % idx
    olines = [ln for ln in raw_out.decode().split("\n") if ln != ""]
    assert len(olines) == 1, "点 %d：.out 行数 %d != 1" % (idx, len(olines))
    ans = int(olines[0])
    assert 0 <= ans < MOD, "点 %d：答案 %d 越界" % (idx, ans)
    summary.append((idx, n, ans, note))

# ---------------- 自检 3：样例点必须逐字节等于题面输出 ----------------
sample_out = open("problem4.out", "rb").read().decode()
assert sample_out.strip() == "1", "点 4（题面样例）输出 %r != 1" % sample_out
# 点 1/2 的最小情形也可独立验证
assert open("problem1.out", "rb").read().decode().strip() == "1", "点 1 输出应为 1"
assert open("problem2.out", "rb").read().decode().strip() == "1", "点 2 输出应为 1"
assert open("problem3.out", "rb").read().decode().strip() == "0", "点 3 输出应为 0"
assert open("problem5.out", "rb").read().decode().strip() == "0", "点 5 输出应为 0"
assert open("problem9.out", "rb").read().decode().strip() == "1", "点 9 输出应为 1"

# ---------------- 自检 4：答案不能退化成「一片 0」（数据有鉴别力）----------------
nonzero = [s for s in summary if s[2] != 0]
assert len(nonzero) >= 6, "非零答案点只有 %d 个，数据鉴别力不足" % len(nonzero)

print("各点概览（点号 | n | 答案 | 说明）：")
for idx, n, ans, note in summary:
    print("problem%-2d: n=%-2d ans=%-11d %s" % (idx, n, ans, note))
print("生成完成：10 个测试点，.in/.out 成对齐全，.out 均非空且恰 1 行；"
      "非零答案点 %d/10。" % len(nonzero))
