#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1813《图的计数》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
#
# 题意：n 个点 m 条边的有向图（可含重边/自环），1 -> n 的最短路长度恰为 n-1（「至少 n-1」），
#       求方案数 mod 1e9+7。公式 ans = (n-2)! * C(A+m-n, m-n+1)，A = n^2 - (n-1)(n-2)/2；
#       m < n-1（n>=2）无解 -> 0；n=1 特判 -> 1。详见 std.cpp 头注（含 4 个来源 URL）。
#
# 数据范围（题面明文，content.md）：
#   30%：n<=5,  m<=10；60%：n<=80, m<=3000；100%：1<=n<=10000, 1<=m<=50000。
#   限制 time 1000 ms / memory 256 MB（config.json）。本题单组输入（每点一个 (n,m) 对）。
#
# ---- 分层策略（边界 / 小 / 中 / 大 / 顶格，10 个点）----
#   点 1  边界层：题面样例 (2,2) -> 4，逐字节回归；
#   点 2  边界层：n 下界 (1,1) -> 1（n=1 特判分支）；
#   点 3  边界层：无解最小规模 (3,1)（m < n-1）-> 0；
#   点 4  边界层：无解顶格 n (10000,9998)（m = n-2，差 1）-> 0；
#   点 5  小规模：k=0 且 (n-2)!>1 的最小非平凡 (4,3) -> 2（可手算：2 条哈密顿链）；
#   点 6  小规模：30% 数据顶格 (5,10)；
#   点 7  中等规模：60% 数据顶格 (80,3000)；
#   点 8  中-大规模：60% 与 100% 之间的过渡 (1000,20000)（k 大、A 大）；
#   点 9  顶格层：n 顶格 + k=0（9999 = n-1）(10000,9999)，答案 = 9998! mod p；
#   点 10 顶格层：双顶格 (10000,50000)，k=40001 最大，同时压满 n 与 m。
#
# 生成方式（按任务书要求规避 cyaron output_gen 的写缓冲隐患）：
#   .in 用 cyaron 写出后显式 flush 并断言非空；.out 用 subprocess 显式跑 ../std 产出，
#   随后断言 .out 非空、恰好 1 行、且与独立的 Python 真值逐字节一致（无空输出点）。
#   Python 真值：k<=5000 用精确 math.comb；k>5000 用逐因子模乘（O(k)，无 O(n^2) 循环）。

import math
import os
import subprocess
import sys

from cyaron import IO  # 引入CYaRon的库

MOD = 10**9 + 7
STD = "../std"

# ---------------- 分层点表：(点号, n, m, 层次说明) ----------------
CASES = [
    (1, 2, 2, "边界层：题面样例 (2,2) -> 4，逐字节回归"),
    (2, 1, 1, "边界层：n 下界 (1,1) -> 1（n=1 特判：1 个点的 m 条自环图唯一）"),
    (3, 3, 1, "边界层：无解最小规模 (3,1)（m<n-1）-> 0"),
    (4, 10000, 9998, "边界层：无解且 n 顶格 (10000,9998)（m=n-2，差 1）-> 0"),
    (5, 4, 3, "小规模：k=0 且 (n-2)!=2 的最小非平凡 (4,3) -> 2（可手算）"),
    (6, 5, 10, "小规模：30% 数据顶格 (n<=5, m<=10)"),
    (7, 80, 3000, "中等规模：60% 数据顶格 (n<=80, m<=3000)"),
    (8, 1000, 20000, "中-大规模：60% 与 100% 之间的过渡（k=19001、A=501499 均大）"),
    (9, 10000, 9999, "顶格层：n 顶格且 k=0（m=n-1），答案 = 9998! mod p"),
    (10, 10000, 50000, "顶格层：双顶格 (n,m 同时压满)，k=40001 最大"),
]

N_MAX, M_MAX = 10000, 50000  # 题面上限


def expected(n, m):
    """独立于 C++ 的 Python 真值（同一公式，独立实现）。"""
    if n <= 1:
        return 1 % MOD
    if m < n - 1:
        return 0
    A = n * n - (n - 1) * (n - 2) // 2
    k = m - n + 1
    if k <= 5000:  # 精确组合数（math.comb 为 C 实现，仅小 k 用）
        comb = math.comb(A + k - 1, k) % MOD
    else:          # 大 k：逐因子模乘 + 逆元（O(k)）
        num = den = 1
        for i in range(k):
            num = num * ((A + k - 1 - i) % MOD) % MOD
            den = den * (k - i) % MOD
        comb = num * pow(den, MOD - 2, MOD) % MOD
    return math.factorial(n - 2) % MOD * comb % MOD


# ---------------- 自检 1：范围与层次 ----------------
assert len(CASES) == 10, "必须恰好 10 个测试点"
assert [c[0] for c in CASES] == list(range(1, 11)), "点号必须为 1..10"
for idx, n, m, _note in CASES:
    assert 1 <= n <= N_MAX and 1 <= m <= M_MAX, "点 %d 的 (n,m)=(%d,%d) 越界" % (idx, n, m)
# 题面 30% / 60% / 100% 三档边界必须各被顶格覆盖
assert (5, 10) in [(n, m) for _, n, m, _ in CASES], "缺 30% 顶格 (5,10)"
assert (80, 3000) in [(n, m) for _, n, m, _ in CASES], "缺 60% 顶格 (80,3000)"
assert (10000, 50000) in [(n, m) for _, n, m, _ in CASES], "缺 100% 顶格 (10000,50000)"
assert (2, 2) in [(n, m) for _, n, m, _ in CASES], "缺题面样例 (2,2)"

# ---------------- 生成 + 自检 2/3 ----------------
rows = []
for idx, n, m, note in CASES:
    in_path = "problem%d.in" % idx
    out_path = "problem%d.out" % idx

    io = IO(file_prefix="problem", data_id=idx, disable_output=True)
    io.input_writeln(n, m)   # 单组输入：一行两个整数
    io.flush_buffer()        # 显式 flush，规避 cyaron 写缓冲隐患
    io.close()
    assert os.path.getsize(in_path) > 0, "%s 为空（写缓冲未落盘）" % in_path

    # 显式用 subprocess 跑 std 产 .out（不依赖 cyaron output_gen）
    with open(in_path) as fi, open(out_path, "w") as fo:
        rc = subprocess.run([STD], stdin=fi, stdout=fo).returncode
    assert rc == 0, "%s 运行 std 失败 rc=%d" % (idx, rc)

    # 自检 2：.in 恰好 2 个整数；.out 非空、恰好 1 行、1 个整数且在 [0,MOD)
    toks = open(in_path).read().split()
    assert toks == [str(n), str(m)], "点 %d .in 内容异常: %r" % (idx, toks)
    out_lines = open(out_path).read().split("\n")
    assert out_lines[-1] == "" and len(out_lines) == 2, "点 %d .out 行数异常" % idx
    val = int(out_lines[0])
    assert 0 <= val < MOD, "点 %d .out 值越界" % idx

    # 自检 3：与 Python 独立真值逐字节一致
    exp = expected(n, m)
    assert val == exp, "点 %d (%d,%d): std=%d 期望=%d" % (idx, n, m, val, exp)
    rows.append((idx, n, m, val, note, os.path.getsize(in_path), os.path.getsize(out_path)))

# ---------------- 概览输出 ----------------
print("分层概览（n/m 均在上限内；k = m-n+1 为可自由放置的边数）：")
for idx, n, m, val, note, sz_i, sz_o in rows:
    k = m - n + 1
    print("problem%-2d: n=%-5d m=%-5d k=%-6s ans=%-10d (.in %dB / .out %dB) -- %s"
          % (idx, n, m, k if k >= 0 else "无解", val, sz_i, sz_o, note))
print("自检通过：10 组 .in/.out 成对齐全、非空、单行输出，且与 Python 独立真值逐字节一致。")
