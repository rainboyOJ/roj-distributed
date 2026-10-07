#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1777《寻找整数》分层测试数据生成器（cyaron）
#
# ── 题面 ──────────────────────────────────────────────────────────────────
# 输入：第一行 t（数据组数）；接下来 t 行，每行 m k。
#       数据范围：t <= 2000，0 <= m <= 10^18，1 <= k <= 64；
#       保证 10^18 以内存在满足条件的 n。
# 输出：每组一行两个整数：满足条件的某个 n（2^64-1 以内），以及满足条件的 n 的个数
#       （无穷多输出 -1）。
#
# ── 标程结论（与本目录 std.cpp 同源，见 std.cpp 头注） ─────────────────────
#   f(n) = #{x : n < x <= 2n, popcount(x) = k} = #{j : 0 <= j <= n-1, popcount(j) = k-1}。
#   设 a_i = 第 i+1 小的「popcount = k-1」的非负整数（0-indexed），则
#     m >= 1：n ∈ [a_{m-1}+1, a_m]   → 最小 n = a_{m-1}+1，个数 = a_m - a_{m-1}
#     m == 0：n ∈ [1, 2^{k-1}-1]     → 最小 n = 1，个数 = 2^{k-1}-1
#     k == 1：f(n) ≡ 1 (n>=1)        → m = 1 时无穷多（-1），m ≠ 1 无解（题面保证不出现）
#
# ── 生成策略 ──────────────────────────────────────────────────────────────
# 先随机挑一个**合法**的 n（1 <= n <= 10^18）与 k，再令 m = f(n)（用下面的 Python 闭式
# 复算器算出），这样每条询问都自动满足题面「10^18 以内存在满足条件的 n」的前提，
# 不会造出题面保证之外的无解询问（例如 k = 64 且 m >= 1 时 10^18 内其实无解）。
#
# ── 输出侧 ────────────────────────────────────────────────────────────────
# 不用 cyaron 的 io.output_gen（其内部不 flush/close 输出文件，实测会产出 0 字节 .out），
# 改为 subprocess 显式把 .in 喂给 ../std 并写 .out，随后断言：
#   ① .out 非空；② 行数 = t；③ 每行两个整数；④ 与 Python 独立复算的闭式答案逐条一致；
#   ⑤ n 落在 [1, 2^64-1] 内；⑥ 小范围恒等式自检（见 check_identity()）。
#
# 用法（在本目录下）：nice -n 19 timeout 120 python3 data.py
# 产物：data/problem1.in|out … data/problem10.in|out

import os
import random
import subprocess

from cyaron import IO

if not os.path.isdir("data"):
    os.makedirs("data")
os.chdir("data")

U64MAX = (1 << 64) - 1
M_MAX = 10 ** 18


def ensure_std():
    """../std 缺失（编译产物已清理）时从 ../std.cpp 现场编译。"""
    if not os.path.exists("../std"):
        subprocess.check_call(["g++", "-O2", "-std=c++17", "../std.cpp", "-o", "../std"])
        print("compiled ../std from ../std.cpp")


ensure_std()
random.seed(1777)

# ─────────────────────────── Python 独立复算器 ───────────────────────────

BINOM = [[0] * 65 for _ in range(65)]
for _i in range(65):
    BINOM[_i][0] = 1
    for _j in range(1, _i + 1):
        BINOM[_i][_j] = BINOM[_i - 1][_j - 1] + BINOM[_i - 1][_j]


def cnt_le(X, p):
    """#{ j : 0 <= j <= X, popcount(j) == p }（X >= 0，0 <= p <= 64）"""
    if p < 0 or X < 0:
        return 0
    res = 0
    used = 0
    for i in range(63, -1, -1):
        if (X >> i) & 1:
            need = p - used
            if 0 <= need <= i:
                res += BINOM[i][need]
            used += 1
            if used > p:
                return res
    if used == p:
        res += 1
    return res


_kth_cache = {}


def kth(m, p):
    """第 m 小（1-indexed，m >= 1）的「popcount = p」的非负整数 a_{m-1}。

    逐位贪心构造，O(64)：在第 i 位，若该位取 0，则低位任取 p-used 个 1，共 C(i,p-used) 个；
    m 不超过它则本位取 0，否则减去该数并本位取 1。
    """
    key = (m, p)
    if key in _kth_cache:
        return _kth_cache[key]
    assert 1 <= m <= BINOM[64][p], (m, p)
    X = 0
    used = 0
    for i in range(63, -1, -1):
        need = p - used
        c = BINOM[i][need] if 0 <= need <= i else 0
        if m > c:
            m -= c
            X |= 1 << i
            used += 1
    assert m == 1 and used == p, (m, p, used, X)
    _kth_cache[key] = X
    return X


_exp_cache = {}


def expected(m, k):
    """闭式答案 (n, 个数)。无解时返回 (0, 0)（题面保证不出现）。"""
    if (m, k) in _exp_cache:
        return _exp_cache[(m, k)]
    r = _expected(m, k)
    _exp_cache[(m, k)] = r
    return r


def _expected(m, k):
    if k <= 0:
        return (1, -1) if m == 0 else (0, 0)
    if k == 1:
        return (1, -1) if m == 1 else (0, 0)
    p = k - 1
    if m == 0:
        return (1, (1 << p) - 1)
    if BINOM[64][p] < m + 1:
        return (0, 0)
    am1 = kth(m, p)
    am = kth(m + 1, p)
    return (am1 + 1, am - am1)


def m_of(n, k):
    """f(n)：区间 (n, 2n] 中 popcount = k 的个数（= 题面的 m）"""
    return cnt_le(n - 1, k - 1)


# 手算锚点：钉死复算器本身（防止「std 与复算器同错」）
ANCHORS = {
    (1, 2): (2, 1),                       # 题面样例
    (0, 2): (1, 1),                       # n=1：区间 (1,2] 只有 2，popcount=1 ≠ 2
    (0, 3): (1, 3),                       # n ∈ [1,3]
    (2, 2): (3, 2),                       # n ∈ [3,4]
    (3, 2): (5, 4),                       # n ∈ [5,8]
    (1, 1): (1, -1),                      # k=1 无穷多
    (0, 64): (1, (1 << 63) - 1),          # n ∈ [1, 2^63-1]
    (0, 63): (1, (1 << 62) - 1),
}
for _q, _e in ANCHORS.items():
    _g = expected(*_q)
    assert _g == _e, ("anchor mismatch", _q, _g, _e)


def check_identity(N=3000):
    """三项自检（均为小规模 O(NK) 推导验证，非暴力搜索/对拍文件）：
    ① 恒等式 f(n) = #{x∈(n,2n] : popcount(x)=k} == #{j<n : popcount(j)=k-1}（前缀和）；
    ② 贪心 kth(m,p) == 直接枚举出的第 m 个 popcount=p 的数；
    ③ 闭式答案回到定义：m_of(n,k)==m 且 n 最小、n+1（个数>1 时）仍满足。
    """
    LIM = max(2 * N + 1, 1 << 14)
    pc = [bin(i).count("1") for i in range(LIM + 1)]
    pre = [[0] * 70 for _ in range(2 * N + 2)]
    for i in range(2 * N + 1):
        row, nxt = pre[i], pre[i + 1]
        for k in range(70):
            nxt[k] = row[k] + (1 if pc[i] == k else 0)
    for n in range(1, N + 1):
        for k in range(1, 14):
            direct = pre[2 * n + 1][k] - pre[n + 1][k]
            assert direct == pre[n][k - 1], ("identity", n, k, direct, pre[n][k - 1])

    for p in range(1, 7):
        arr = [j for j in range(1 << 14) if pc[j] == p]
        for idx in range(1, min(len(arr), 60) + 1):
            assert kth(idx, p) == arr[idx - 1], ("kth", idx, p, kth(idx, p), arr[idx - 1])

    for k in range(1, 11):
        for m in range(0, 500):
            n, c = expected(m, k)
            if (n, c) == (0, 0):
                continue          # 10^18 内无解（题面保证不出现），跳过
            assert m_of(n, k) == m, ("expected-n", m, k, n, m_of(n, k))
            if n > 1:
                assert m_of(n - 1, k) == m - 1, ("minimality", m, k, n)
            if c > 1:
                assert m_of(n + 1, k) == m, ("count", m, k, n)
    print("self-check OK: identity(n<=%d,k<=13) + greedy-kth + closed-form-vs-definition" % N)


# ─────────────────────────── 写点 & 断言 ───────────────────────────

def write_case(data_id, queries, note):
    assert 1 <= len(queries) <= 2000, (data_id, len(queries))
    for (m, k) in queries:
        assert 0 <= m <= M_MAX and 1 <= k <= 64, (data_id, m, k)
        e = expected(m, k)
        assert e != (0, 0), ("造出题面保证之外的无解询问", data_id, m, k)
        assert 1 <= e[0] <= U64MAX

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(str(len(queries)) + "\n" + "\n".join("%d %d" % q for q in queries) + "\n")
    io.flush_buffer()

    inp = "problem%d.in" % data_id
    outp = "problem%d.out" % data_id
    with open(inp, "rb") as f:
        data = f.read()
    # 断言 .in 落盘正确（t 行 + t 组）
    head = data.decode().split("\n")
    assert head[0].strip() == str(len(queries)), (data_id, head[0])
    assert len([x for x in head[1:] if x.strip()]) == len(queries), data_id

    proc = subprocess.run(["../std"], input=data, stdout=subprocess.PIPE, check=True)
    out = proc.stdout
    with open(outp, "wb") as f:
        f.write(out)

    assert os.path.getsize(outp) > 0, ("空 .out", outp)
    toks = out.decode().split()
    assert len(toks) == 2 * len(queries), ("行/字段数不符", data_id, len(toks))
    for i, (m, k) in enumerate(queries):
        g1, g2 = int(toks[2 * i]), int(toks[2 * i + 1])
        e1, e2 = expected(m, k)
        assert g1 == e1 and g2 == e2, ("答案不符", data_id, i, (m, k), (g1, g2), (e1, e2))
        assert 1 <= g1 <= U64MAX
    print("problem%d.in/.out  t=%-4d  %s" % (data_id, len(queries), note))
    return inp, outp


def rand_q(rs, n_lo, n_hi, k_lo, k_hi):
    """随机挑合法 n、k，再反推 m = f(n)"""
    n = rs.randint(n_lo, n_hi)
    k = rs.randint(k_lo, k_hi)
    return (m_of(n, k), k)


def build(rs, t, n_lo, n_hi, k_lo, k_hi, specials=()):
    qs = list(specials)
    while len(qs) < t:
        qs.append(rand_q(rs, n_lo, n_hi, k_lo, k_hi))
    rs.shuffle(qs)
    return qs[:t]


rs = random.Random(1777)
check_identity()

# 点 1：题面样例（唯一一组，用于样例回归）
inp, outp = write_case(1, [(1, 2)], "题面样例 t=1, (m,k)=(1,2) → 期望 2 1")
with open(outp) as f:
    assert f.read().strip() == "2 1", "样例输出必须为 2 1"
print("  ↑ 题面样例回归通过：std 输出 \"2 1\"")

# 点 2：边界层 —— 全部极端取值（m=0 各档 k、k=1 的 -1、k=64 的最大个数、最小 n）
write_case(2, [
    (0, 2), (0, 3), (0, 10), (0, 32), (0, 40), (0, 50), (0, 60), (0, 62), (0, 63), (0, 64),
    (1, 1), (1, 2), (2, 2), (3, 2), (1, 3), (1, 4),
], "边界层：m=0 全档 k（含 k=64 → 个数 2^63-1）、k=1 → -1、最小 m")

# 点 3：小规模随机（可手算量级）
write_case(3, build(rs, 10, 1, 1000, 1, 10),
           "小规模随机：n ∈ [1,1000], k ∈ [1,10], t=10")

# 点 4：小规模随机（含 k=1 的 -1 分支）
write_case(4, build(rs, 50, 1, 20000, 1, 16),
           "小规模随机：n ∈ [1,2e4], k ∈ [1,16], t=50")

# 点 5：中等规模随机
write_case(5, build(rs, 200, 1, 10 ** 6, 1, 24),
           "中等规模：n ∈ [1,1e6], k ∈ [1,24], t=200")

# 点 6：中等规模随机（t 上探）
write_case(6, build(rs, 500, 1, 10 ** 9, 1, 40),
           "中等规模：n ∈ [1,1e9], k ∈ [1,40], t=500")

# 点 7：大规模随机
write_case(7, build(rs, 1000, 1, 10 ** 15, 1, 55),
           "大规模：n ∈ [1,1e15], k ∈ [1,55], t=1000")

# 点 8：大规模随机（n 顶到 1e18，k 覆盖到 64）
write_case(8, build(rs, 1500, 1, 10 ** 18, 1, 64, specials=[(0, 64), (1, 1), (0, 63)]),
           "大规模：n ∈ [1,1e18], k ∈ [1,64], t=1500（含 k=64 只有 m=0 有解）")

# 点 9：顶格层 —— t=2000，n 靠近 1e18，m 逼近「10^18 内可解」的最大值
N9 = 10 ** 18
qs9 = [(m_of(N9 - i, 31), 31) for i in range(1, 60)]           # p=30 → m ≈ C(60,30) 量级（最大 m）
qs9 += [(0, 64), (0, 63), (1, 1)]
write_case(9, build(rs, 2000, 10 ** 17, N9, 1, 64, specials=qs9),
           "顶格：t=2000, n ∈ [1e17,1e18], k 全覆盖；含 m 最大的 k=31 与 2^63-1 量级个数")

# 点 10：顶格最坏结构 —— 全部取 m 极大的 k=31 与「个数最大」的 k=2 / k=64
qs10 = [(m_of(N9, 31), 31)] * 1200                              # 同一询问重复 1200 次：m ≈ 1.18e17（最大）
qs10 += [(m_of(N9, 2), 2)] * 400                                # p=1：a_{m-1}=2^{m-1}，个数 = 2^{m-1}（巨大）
qs10 += [(0, 64)] * 200                                         # 个数 = 2^63-1（unsigned 上界附近）
qs10 += [(0, 63), (0, 62), (1, 1), (m_of(N9 - 1, 64), 64)]
write_case(10, build(rs, 2000, 10 ** 17, N9, 1, 64, specials=qs10),
           "顶格最坏：t=2000，k=31 的最大 m、k=2 的 2^58 量级个数、k=64 的 2^63-1 个数")

print("\n全部 10 组数据生成 + 断言通过（答案与 Python 独立闭式逐条一致）")
