#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1795《散步》分层测试数据生成器
# 用法（在本目录下）：python3 data.py
#   —— data.py 会按需自动编译 work/std（g++ -O2 -std=c++17），并在 data/ 下产出
#      problem1..10.in/.out；编译产物 work/std 属临时文件，生成完可删。
#
# 题意：数轴上从原点出发，n 个单位时间（每步 ±1），每次离家的时间不能超过 m，
#       n 个时间后正好回到家，求方案数 mod 1e9+7。
# 输入：一行两个整数 n, m。
# 数据范围（题面明文）：2 <= n <= 1e9，2 <= m <= 100，保证 n、m 均为偶数。
# 限制：1000 ms / 256 MB（config.json；官方页 262144 KB）。
#
# ---- 分层策略（10 个测试点，从最小铺到顶格）----
#   点 1  边界层：n=2, m=2 —— 题面下界（n、m 同时取最小），答案 2
#   点 2  边界层：n=4, m=2 —— 题面样例 1，m 取最小（单次远足长 2 的极端结构），答案 4
#   点 3  样例层：n=10, m=6 —— 题面样例 2，答案 184（与 std 交叉验证解释正确性）
#   点 4  小规模：n=100（30% 档 n 上界）, m=2 —— n 上界配最小 m（答案 2^50，短途拼接极端）
#   点 5  小规模：n=100, m=100 —— 30% 档 n 上界 + m 顶格且 m=n（约束失效，答案 C(100,50)）
#   点 6  中大规模：n=1000000, m=100 —— n 中等偏大 + m 顶格（递推阶数 d=50 最大）
#   点 7  大规模：n=100000000, m=50 —— n 大 + m 中等（d=25，验证 log n 快速幂）
#   点 8  近顶格：n=999999998, m=100 —— n 接近顶格 + m 顶格
#   点 9  顶格层：n=1000000000, m=2 —— n 顶格 + m 最小（d=1，纯快速幂 2^(5e8)）
#   点 10 顶格层：n=1000000000, m=100 —— n、m 双顶格（d=50 且 log n 最大，最慢点）
#   说明：n=1e9 为 100% 档 n 上界，m=100 为 m 上界；所有点 n、m 均为偶数，未越界。
#
# ---- 正确性自检（均为"按题面定义/另一算法"的独立模型，非暴力枚举）----
#   A) ref_state_dp：直接按题面定义做状态 DP（状态 = 当前位置 j 与本次离家已走时间 s），
#      仅用于 n<=100 的小点（点 1-5），是独立于 std 递推建模的另一直观模型。
#   B) ref_kitamasa：对 d 阶线性递推用多项式取模（Kitamasa）求第 t 项，
#      与 std 的矩阵快速幂是不同算法，覆盖全部 10 点。
#   C) 特例闭式：点 5 用 C(100,50)（m>=n 时约束失效，答案 = 所有 n 长闭路数）；
#      点 9 用 pow(2, n/2, MOD)（m=2 时答案恰为 2^(n/2)）；点 1-3 用题面/手算值。
#   任一断言失败即抛异常，不会产出可疑数据。
#
# ⚠ 生成 .out 时用 subprocess 显式调用 std 并把 stdout 直接落盘（不依赖 cyaron 缓冲），
#   随后断言 .out 非空、恰 1 行、为合法整数且等于独立模型算出的期望值。

import os
import subprocess
import sys
from math import comb

MOD = 10 ** 9 + 7
HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "work", "std")
STD_SRC = os.path.join(HERE, "std.cpp")

# 按需自动编译 std（编译产物为临时文件，不进版本库）
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
if not os.path.exists(STD) or os.path.getmtime(STD) < os.path.getmtime(STD_SRC):
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD, STD_SRC], check=True)


# ---------------- 独立模型 A：按题面定义的状态 DP ----------------
def ref_state_dp(n, m):
    """状态 (j, s)：当前在位置 j(≠0)，本次离家已走 s 步。家在 s=0。
    走到 j 后若回到 0，则该次离家用时 s+1，必须 <= m。"""
    cur = {}          # (j, s) -> 方案数
    home = 1
    for _ in range(n):
        nxt = {}
        nhome = 0
        for (j, s), v in cur.items():
            ns = s + 1
            if ns > m:
                continue
            for nj in (j + 1, j - 1):
                if nj == 0:
                    nhome = (nhome + v) % MOD
                else:
                    nxt[(nj, ns)] = (nxt.get((nj, ns), 0) + v) % MOD
        if home:
            for nj in (1, -1):
                nxt[(nj, 1)] = (nxt.get((nj, 1), 0) + home) % MOD
        cur, home = nxt, nhome
    return home


# ---------------- 独立模型 B：Kitamasa（多项式取模）----------------
def _coeffs(d):
    """c[1..d]，c[j] = f(2j) = 2*Catalan(j-1)"""
    c = [0] * (d + 1)
    for j in range(1, d + 1):
        c[j] = (2 * (comb(2 * (j - 1), j - 1) // j)) % MOD
    return c


def ref_kitamasa(n, m):
    """h(t) = sum_{j=1..d} c[j] h(t-j)，t = n/2，d = m/2；用 x^t mod P(x) 求。"""
    d = m // 2
    t = n // 2
    c = _coeffs(d)
    # 初值 h(0..d-1)
    h = [0] * d
    h[0] = 1
    for i in range(1, d):
        s = 0
        for j in range(1, min(i, d) + 1):
            s += c[j] * h[i - j]
        h[i] = s % MOD

    def polymul(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai:
                for k, bk in enumerate(b):
                    if bk:
                        r[i + k] = (r[i + k] + ai * bk) % MOD
        for i in range(len(r) - 1, d - 1, -1):
            v = r[i]
            if v:
                r[i] = 0
                for j in range(1, d + 1):
                    r[i - j] = (r[i - j] + v * c[j]) % MOD
        return r[:d]

    res = [1] + [0] * (d - 1)          # 1
    if d == 1:
        base = [c[1] % MOD]            # x ≡ c1 (mod x - c1)
    else:
        base = [0] * d
        base[1] = 1                    # x
    e = t
    while e:
        if e & 1:
            res = polymul(res, base)
        base = polymul(base, base)
        e >>= 1
    return sum(res[i] * h[i] for i in range(d)) % MOD


# ---------------- 测试点设计 ----------------
CASES = [
    (1, 2, 2, "边界层：n、m 同时取题面下界（最小规模，答案 2）"),
    (2, 4, 2, "边界层：题面样例 1，m 取最小（全是长 2 短途的极端结构，答案 4）"),
    (3, 10, 6, "样例层：题面样例 2（答案 184，锁定题意解释）"),
    (4, 100, 2, "小规模：30% 档 n 上界 100 + m 最小 2（答案 2^50）"),
    (5, 100, 100, "小规模：30% 档 n 上界 + m 顶格且 m=n（约束失效，答案 C(100,50)）"),
    (6, 1000000, 100, "中大规模：n=1e6 + m 顶格（d=50 最大阶数）"),
    (7, 100000000, 50, "大规模：n=1e8 + m 中等（d=25）"),
    (8, 999999998, 100, "近顶格：n 接近 1e9 + m 顶格"),
    (9, 1000000000, 2, "顶格层：n 顶格 + m 最小（d=1，答案 2^(5e8)）"),
    (10, 1000000000, 100, "顶格层：n、m 双顶格（d=50 且 log n 最大，最慢点）"),
]

assert len(CASES) == 10, "必须恰好 10 个测试点"

# ---------------- 逐点生成 + 自检 ----------------
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
os.chdir(os.path.join(HERE, "data"))

print("std =", STD)
for idx, n, m, note in CASES:
    assert n % 2 == 0 and m % 2 == 0, "点 %d: n、m 必须为偶数" % idx
    assert 2 <= n <= 10 ** 9, "点 %d: n 越界" % idx
    assert 2 <= m <= 100, "点 %d: m 越界" % idx

    inpath = "problem%d.in" % idx
    outpath = "problem%d.out" % idx
    with open(inpath, "w") as f:
        f.write("%d %d\n" % (n, m))

    # 显式 subprocess 跑 std，stdout 直接落盘（规避 cyaron 缓冲/0 字节问题）
    with open(outpath, "wb") as fo, open(inpath, "rb") as fi:
        r = subprocess.run([STD], stdin=fi, stdout=fo, stderr=subprocess.PIPE, timeout=120)
    assert r.returncode == 0, "点 %d: std 返回 %d, stderr=%s" % (idx, r.returncode, r.stderr[:300])

    raw = open(outpath, "rb").read()
    assert len(raw) > 0, "点 %d: .out 为空（0 字节）" % idx
    text = raw.decode().strip()
    lines = text.split("\n")
    assert len(lines) == 1, "点 %d: .out 应恰 1 行，实得 %d 行" % (idx, len(lines))
    assert lines[0].isdigit(), "点 %d: .out 非整数: %r" % (idx, lines[0])
    got = int(lines[0])
    assert 0 <= got < MOD, "点 %d: 答案超出 mod 范围" % idx

    # 独立模型 B（全部点）
    exp_k = ref_kitamasa(n, m)
    assert got == exp_k, "点 %d (n=%d,m=%d): std=%d, Kitamasa=%d" % (idx, n, m, got, exp_k)

    # 独立模型 A（n<=100 的小点，另一直观建模）
    if n <= 100:
        exp_dp = ref_state_dp(n, m)
        assert got == exp_dp, "点 %d (n=%d,m=%d): std=%d, 状态DP=%d" % (idx, n, m, got, exp_dp)

    # 特例闭式
    if idx == 1:
        assert got == 2
    if idx == 2:
        assert got == 4, "样例 1 应输出 4"
    if idx == 3:
        assert got == 184, "样例 2 应输出 184"
    if idx == 5:
        assert got == comb(100, 50) % MOD, "m>=n 时应等于 C(n, n/2)"
    if idx == 9:
        assert got == pow(2, n // 2, MOD), "m=2 时应等于 2^(n/2)"

    print("problem%-2d: n=%-10d m=%-4d ans=%-10d  %s" % (idx, n, m, got, note))

print("ALL 10 CASES OK (subprocess std + Kitamasa + 状态DP + 闭式自检全部一致)")
