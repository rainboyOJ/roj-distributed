#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1748《大数计数》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# （本脚本也会自动 mkdir/chdir 到 data/，因此从 staging 目录直接 `python3 data.py` 亦可）
#
# 题意（content.md 明文）：长度为 n 的大数 S_1..S_n（S_1 为最高位，故 S_1∈1..9），
#   m 条限制 (l1,r1,l2,r2) 表示 S[l1..r1] == S[l2..r2]（长度相等）。
#   求满足全部限制的 n 位数个数 mod 1e9+7。
#   数据范围（题面【提示】）：1 <= n,m <= 1e5；保证 r1-l1 = r2-l2；
#   config.json：time 1000 ms / memory 512 MB。
#
# ---- 分层策略（10 个测试点：边界 / 小 / 中 / 大 / 顶格）----
#   点 1  边界：n=m=1，限制 "1 1 1 1"（自等）—— 答案 9（n 下限）。
#   点 2  边界：n=2,m=2，"1 1 2 2" + "1 2 1 2" —— 唯一连通块，答案 9。
#   点 3  小规模构造：n=10,m=3，"1 5 6 10"(shift 5) + 两条自等 —— 5 块，答案 90000。
#   点 4  小规模构造：n=50,m=40，20 对互不相交的位置等约束各重复一次
#         ⇒ 恰 20 次有效合并，连通块=30，答案 9*10^29（可解析推出）。
#   点 5  中等随机：n=m=2000，短区间 L∈[1,5] 且限制在 [1,n/2] 内，
#         右半 n/2 个位置未被触碰 ⇒ 答案量级巨大（非平凡）。
#   点 6  中等长区间：n=m=5000，区间长度 L∈[n/2,n]（大量高层合并 + 下放压力）。
#   点 7  大规模局部随机：n=m=50000，L∈[1,20] 且限制在 [1,n/2] 内。
#   点 8  顶格全范围随机：n=m=100000，随机长度/位置（100% 档上限）。
#   点 9  顶格 trivial：n=m=100000，全部为自等限制 ⇒ 无合并，连通块=n，
#         答案 = 9*10^(n-1)（答案量级顶格，测高次幂取模）。
#   点 10 顶格长区间：n=m=100000，全部重复 "1 50000 50001 100000"(shift 50000)
#         ⇒ 恰 n/2 个连通块，答案 = 9*10^(n/2-1)（最大区间 + 最大 m 的结构点）。
#
# ---- 数据正确性保证（生成期解析自检；**不使用任何 brute/对拍/stress**）----
#   · 逐条校验端点 1<=l1,r1,l2,r2<=n 且 r1-l1=r2-l2；
#   · 生成后断言 .in 行数 == m+1、.out 非空且恰 1 行整数、值在 [0,1e9+7)；
#   · 对**答案可解析推出**的结构点（1/2/3/4/9/10）用与 std 算法无关的构造期望断言：
#       - 点 1/2/3：由"移位合并把位置按模 d 分组"直接数出连通块数 t，
#         期望 9*10^(t-1) mod p；
#       - 点 4：20 对互不相交的位置等约束 ⇒ t = n-20 = 30；
#       - 点 9：无合并 ⇒ t=n，期望 9*10^(n-1) mod p；
#       - 点 10：shift n/2 ⇒ t = n/2，期望 9*10^(n/2-1) mod p。
#   · 随机部分固定种子，完全可复现。

import os
import sys

from cyaron import IO, randint, random  # 引入CYaRon的库

MAXN = 100000
MAXM = 100000
MOD = 10 ** 9 + 7

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(OUT_DIR, "std")
if not os.path.exists(STD):
    sys.exit("std binary not found: %s （先 g++ -O2 -std=c++17 -o std std.cpp）" % STD)

DATA_DIR = os.path.join(OUT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)


def ans_from_components(t):
    """连通块数为 t 时的答案：最高位块 9 种（1..9），其余 t-1 块各 10 种。"""
    return 9 * pow(10, t - 1, MOD) % MOD


def rand_constraint(n, lmin=1, lmax=None, region=None):
    """随机合法限制：长度 L∈[lmin,min(lmax,n)]，两区间起点在 [1,R-L+1] 内独立随机，
    其中 R = region（默认 n）。region<n 时右侧 n-R 个位置不被触碰。"""
    if lmax is None:
        lmax = n
    R = n if region is None else region
    L = randint(lmin, min(lmax, R))
    a = randint(1, R - L + 1)
    b = randint(1, R - L + 1)
    return (a, a + L - 1, b, b + L - 1)


def rand_cons_list(n, m, seed, lmin=1, lmax=None, region=None):
    random.seed(seed)
    return [rand_constraint(n, lmin, lmax, region) for _ in range(m)]


def disjoint_pairs(n, k, seed):
    """k 对互不相交的位置等约束 (a,a,b,b)：每对只并一次，总连通块减少 k。"""
    random.seed(seed)
    pos = list(range(1, n + 1))
    random.shuffle(pos)
    return [(pos[2 * i], pos[2 * i], pos[2 * i + 1], pos[2 * i + 1]) for i in range(k)]


# ---------------- 各点限制表 ----------------
# 点 1：n=1,m=1 自等
C1, N1, M1 = [(1, 1, 1, 1)], 1, 1
# 点 2：n=2,m=2
C2, N2, M2 = [(1, 1, 2, 2), (1, 2, 1, 2)], 2, 2
# 点 3：n=10,m=3，shift 5 + 两条自等
C3, N3, M3 = [(1, 5, 6, 10), (1, 1, 1, 1), (3, 3, 3, 3)], 10, 3
# 点 4：小规模构造：20 对互不相交的位置等约束，各重复一次凑 m=40
N4, M4 = 50, 40
_p4 = disjoint_pairs(N4, 20, 174804)
C4 = _p4 + _p4
# 点 5：中等随机（短区间 + 局部区域 [1,n/2]）
N5, M5 = 2000, 2000
C5 = rand_cons_list(N5, M5, 174805, lmin=1, lmax=5, region=N5 // 2)
# 点 6：中等长区间（L∈[n/2,n]）
N6, M6 = 5000, 5000
C6 = rand_cons_list(N6, M6, 174806, lmin=N6 // 2, lmax=N6)
# 点 7：大规模局部随机（L∈[1,20] 且限制在 [1,n/2]）
N7, M7 = 50000, 50000
C7 = rand_cons_list(N7, M7, 174807, lmin=1, lmax=20, region=N7 // 2)
# 点 8：顶格全范围随机
N8, M8 = 100000, 100000
C8 = rand_cons_list(N8, M8, 174808)
# 点 9：顶格 trivial（全自等，无合并）
N9, M9 = 100000, 100000
C9 = [(i, i, i, i) for i in range(1, N9 + 1)]
# 点 10：顶格长区间（全部重复 shift n/2）
N10, M10 = 100000, 100000
_c10 = (1, N10 // 2, N10 // 2 + 1, N10)
C10 = [_c10] * M10

CASES = [
    (1,  N1,  C1,  ans_from_components(1),            "边界：n=m=1 自等 ⇒ 1 块 ⇒ 9"),
    (2,  N2,  C2,  ans_from_components(1),            "边界：n=2 唯一连通块 ⇒ 9"),
    (3,  N3,  C3,  ans_from_components(5),            "小规模：n=10 shift5 ⇒ 5 块 ⇒ 90000"),
    (4,  N4,  C4,  ans_from_components(N4 - 20),      "小规模：20 对不相交位置等 ⇒ 30 块"),
    (5,  N5,  C5,  None,                              "中等随机 n=m=2000 (L<=5, 区域[1,n/2])"),
    (6,  N6,  C6,  None,                              "中等长区间 n=m=5000 (L∈[n/2,n])"),
    (7,  N7,  C7,  None,                              "大规模局部随机 n=m=50000 (L<=20, [1,n/2])"),
    (8,  N8,  C8,  None,                              "顶格全范围随机 n=m=100000"),
    (9,  N9,  C9,  ans_from_components(N9),           "顶格 trivial n=m=100000 ⇒ 无合并，n 块"),
    (10, N10, C10, ans_from_components(N10 // 2),     "顶格长区间 n=m=100000 shift50000 ⇒ n/2 块"),
]
assert len(CASES) == 10

# ---------------- 逐条范围复核 + 写出 ----------------
for cid, n, cons, expect, note in CASES:
    m = len(cons)
    assert 1 <= n <= MAXN, "点 %d n 越界" % cid
    assert 1 <= m <= MAXM, "点 %d m 越界" % cid
    for (l1, r1, l2, r2) in cons:
        assert 1 <= l1 <= r1 <= n and 1 <= l2 <= r2 <= n, \
            "点 %d 端点越界 (%d,%d,%d,%d)" % (cid, l1, r1, l2, r2)
        assert r1 - l1 == r2 - l2, \
            "点 %d 区间长度不等 (%d,%d,%d,%d)" % (cid, l1, r1, l2, r2)

    lines = ["%d %d" % (n, m)]
    lines += ["%d %d %d %d" % c for c in cons]
    text = "\n".join(lines) + "\n"

    io = IO(file_prefix="problem", data_id=cid)   # problem{cid}.in / problem{cid}.out
    io.input_write(text)
    io.output_gen(STD)                            # .out 由 std 现跑
    io.close()                                    # 刷新句柄，确保 .in/.out 落盘

    # .in 行数自检
    with open("problem%d.in" % cid) as f:
        got_lines = sum(1 for _ in f)
    assert got_lines == m + 1, "点 %d：.in 行数 %d ≠ m+1=%d" % (cid, got_lines, m + 1)

    # .out 非空 / 行数 / 值域自检（无解空输出点不存在，本题恒有解）
    with open("problem%d.out" % cid) as f:
        out = f.read()
    assert out.strip() != "", "点 %d：.out 为空" % cid
    assert out.count("\n") == 1 and out.endswith("\n"), "点 %d：.out 行数异常 %r" % (cid, out)
    val = int(out.strip())
    assert 0 <= val < MOD, "点 %d：.out 越界 %d" % (cid, val)

    # 结构点用构造期望断言（与 std 算法无关）
    if expect is not None:
        assert val == expect, "点 %d：std 输出 %d ≠ 构造期望 %d（%s）" % (cid, val, expect, note)

    print("%-10s n=%-6d m=%-6d ans=%-10d expect=%-10s  %s"
          % ("problem%d" % cid, n, m, val, str(expect) if expect is not None else "-", note))

print("done: 10 组 .in/.out 已生成于 %s（结构点与构造期望一致，随机点通过格式/值域自检）" % DATA_DIR)
