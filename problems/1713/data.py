#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1713《生成树》分层测试数据生成器（cyaron）
#
# 题意：N 个点 M 条边的无向图，对每棵生成树求"边权 gcd"，再对所有这些 gcd 求 lcm，输出该 lcm。
#
# 数据范围（题面【提示】原文）：
#   20% 的数据  M = N-1；另外 20% 的数据  M = N；
#   另外 30% 的数据  所有边权都是 2 的整数次幂；
#   100% 的数据  N ≤ 1000，M ≤ 100000，d_i ≤ 2^15-1 = 32767，ans ≤ 2^64-1。
#   （保证 s_i ≠ t_i，即无自环；允许重边。）
#
# 分层设计（10 组，从最小铺到顶格）：
#   1  边界：N=1, M=0 —— 唯一空生成树（题面 M=N-1 子任务的最小情形）；
#                    空集 lcm 约定为 1（见 gen-report.md「题面歧义」一节）。
#   2  边界：N=2, M=1，边权取题面上限 32767（全最大值 + 无环单树，答案 = 32767）。
#   3  小规模可手算：N=4 的树（M=N-1），边权 6,10,15 —— 唯一生成树，gcd=1，答案 = 1。
#   4  小规模随机可暴力对拍：N=5, M=7，权值 ∈[1,12]，含重边/环，可与 work/brute.cpp 对拍。
#   5  中等「M=N」子任务：N=1000, M=1000 单环图（环上 1000 个点 → 恰 1000 棵生成树）；
#      权值定向构造（996×210 + {105,70,42,30}）使各棵树 gcd 取到 2/3/5/7，ans = 210。
#   6  中等「2 的幂」子任务：N=300, M=5000，权值 ∈ {2^0..2^14} —— lcm(出现的幂) 由最大连通幂决定。
#   7  大规模「M=N-1」子任务：N=1000, M=999 树，权值 ∈ {15625, 31250}（gcd=15625）→ 答案 15625。
#   8  大规模随机：N=1000, M=100000（M 取题面上限），权值 1..32767 全范围随机
#      （d_i 亦取到题面上限 2^15-1）。
#   9  顶格 + 构造极限答案（逼近 ans ≤ 2^64-1 上界）：N=1000, M=100000；
#     4 张互质大权值星形生成树（32761 = 181²、32749、32719、30911）
#      + 权值 17 的连通骨架（链 1-2-...-1000）与随机填充边（保证 G_17 连通）。
#      D 的极大元 = {17, 32761, 32749, 32719, 30911}（181 | 32761，故 181 非极大元），
#      ans = lcm(D) = 17 × 32761 × 32749 × 32719 × 30911
#      = 18446636557034669317，占 2^64-1 的 99.9994%，用于检验 unsigned long long 输出
#      （另加 2 条 32767 边把 d_i 顶到题面上限；当 d | 32767 时只保留这 2 条边，
#       G_d 必不连通，故不改变 D，也不会把 7/31/151 等小因子引入答案）。
#  10  顶格 + 卡常最坏结构：N=1000, M=100000，所有边权取 27720 = 2^3·3^2·5·7·11
#      （≤ 32767 中约数最多者，τ(27720)=96），使并查集内层总代价 Σ_e τ(w_e) = 9.6e6 达最大；
#      另加 2 条 32767 的边抬 maxW 到题面上限（不构成生成树）→ 答案 = lcm(27720 的全部约数) = 27720。
#      用途：单点最大常数最坏情况（d 循环 × 高频约数桶遍历）。

import os
import random
import subprocess

from cyaron import IO

# 用法：在本目录（staging/1713/）直接运行；脚本会自动切到 data/ 子目录，
# 产物为该目录下的 problem1..10.in/.out（IO 写到 cwd，../std 即本目录标程）：
#   nice -n 19 timeout 120 python3 data.py
# 交付包已按流程清理编译产物（无 ./std）；此时脚本会用 g++ 从 std.cpp 现场编译，
# 保证「无二进制状态下仍可一键复现 10 组数据」（与 staging/1720 同做法）。
if not os.path.isdir("data"):
    os.makedirs("data")
os.chdir("data")


def ensure_std():
    """../std 缺失（已清理编译产物）时，从 ../std.cpp 现场编译。"""
    if not os.path.exists("../std"):
        subprocess.check_call(["g++", "-O2", "-std=c++17", "../std.cpp", "-o", "../std"])
        print("compiled ../std from ../std.cpp")


ensure_std()
random.seed(1713)

# 点 9 期望答案 = lcm(17, 32761, 32749, 32719, 30911)
ANS9 = 18446636557034669317

# 全部 10 组的期望答案（回归锚点；由 std 与独立复算器 work/verify.py 双重确认）：
#   1: N=1,M=0 空生成树约定 1；2: 单边 32767；3: 唯一生成树 gcd(6,10,15)=1；
#   4: 小随机（具体值由种子 171304 钉死）；5: 定向单环图 lcm{1,2,3,5,7}=210；
#   6: 2 的幂最大连通幂 2^12=4096；7: gcd(15625,31250)=15625；
#   8: 全随机大图（种子 171308 钉死）；9: 逼近 2^64；10: lcm(27720 全部约数)=27720。
EXPECT = {
    1: 1,
    2: 32767,
    3: 1,
    4: 2,
    5: 210,
    6: 4096,
    7: 15625,
    8: 80313433200,
    9: ANS9,
    10: 27720,
}


def dump(data_id, n, m, edges, note):
    """edges: list[(u, v, w)]，写 problem<data_id>.in 并用 ../std 生成 .out。"""
    lines = ["%d %d" % (n, m)]
    lines += ["%d %d %d" % e for e in edges]
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("\n".join(lines) + "\n")
    io.output_gen("../std")
    io.close()                                 # 刷盘后自检 .out
    got = open("problem%d.out" % data_id).read().strip()
    ok = got == str(EXPECT[data_id])
    if not ok:
        raise SystemExit("problem%d answer mismatch: std=%s expect=%s"
                         % (data_id, got, EXPECT[data_id]))
    print("problem%-2d: %-56s (n=%d, m=%d) ans=%s"
          % (data_id, note, n, m, got))


def rand_tree_edges(n, wfun, rng):
    """随机树：每个点 i>=2 连到 [1,i-1] 的随机父亲。"""
    return [(i, rng.randint(1, i - 1), wfun(i)) for i in range(2, n + 1)]


# ── 1. 边界最小：N=1, M=0（空生成树） ──
dump(1, 1, 0, [], "boundary: N=1,M=0 空生成树")

# ── 2. 边界：N=2, M=1，权取上限 32767 ──
dump(2, 2, 1, [(1, 2, 32767)], "boundary: N=2 单边取 max d=32767")

# ── 3. 小规模可手算：树（M=N-1），gcd(6,10,15)=1 ──
dump(3, 4, 3, [(1, 2, 6), (2, 3, 10), (3, 4, 15)],
     "small hand-check: M=N-1 tree, gcd(6,10,15)=1 -> ans 1")

# ── 4. 小规模随机（可暴力对拍） ──
rng = random.Random(171304)
n, m = 5, 7
edges = rand_tree_edges(n, lambda i: rng.randint(1, 12), rng)   # n-1=4 条保证连通
while len(edges) < m:                                          # 补重边/自环以外的随机边
    u = rng.randint(1, n); v = rng.randint(1, n)
    if u != v:
        edges.append((u, v, rng.randint(1, 12)))
dump(4, n, m, edges, "small random, brute-forcible")

# ── 5. 中等「M=N」子任务：单环图，恰 n=1000 棵生成树（定向构造，答案 = 210） ──
#     用随机置换打乱标签，构造哈密顿环 → 生成树 = 环去掉一条边，共 1000 棵。
#     权值定向构造：996 条环边权 210 = 2·3·5·7，另 4 条分别为 105/70/42/30
#     （即 210 各缺一个素因子）。于是每棵树的 gcd 分别为
#       去 30 边 → gcd=7；去 42 → 5；去 70 → 3；去 105 → 2；去 210 → 1。
#     故 lcm(所有树的 gcd) = lcm(1,2,3,5,7) = 210，等价地 D = {1,2,3,5,7}。
#     该点专卡「试图直接枚举生成树 / 只算全局 gcd(所有边) / 只取单个 d」的实现
#     （若只算全局 gcd 会得 1，只看单棵树可能得 2/3/5/7）。
rng = random.Random(171305)
n = 1000
perm = list(range(1, n + 1))
rng.shuffle(perm)
cycle_w = [210] * (n - 4) + [105, 70, 42, 30]
rng.shuffle(cycle_w)                           # 打乱环上权值分布（打乱标签同理）
edges = [(perm[i - 1], perm[i], cycle_w[i - 1]) for i in range(1, n)]
edges.append((perm[0], perm[-1], cycle_w[-1]))
dump(5, n, len(edges), edges, "medium M=N unicyclic, per-tree gcds {1,2,3,5,7} -> ans 210")

# ── 6. 中等「边权都是 2 的幂」子任务 ──
rng = random.Random(171306)
n, m = 300, 5000
edges = rand_tree_edges(n, lambda i: 1 << rng.randint(0, 14), rng)
while len(edges) < m:
    u = rng.randint(1, n); v = rng.randint(1, n)
    if u != v:
        edges.append((u, v, 1 << rng.randint(0, 14)))
dump(6, n, m, edges, "medium powers of two")

# ── 7. 大规模「M=N-1」子任务：树，权值 15625/31250，gcd=15625 ──
rng = random.Random(171307)
n = 1000
edges = rand_tree_edges(n, lambda i: rng.choice([15625, 31250]), rng)
dump(7, n, n - 1, edges, "large M=N-1 tree, gcd=15625")

# ── 8. 大规模随机，M 取上限 100000 ──
rng = random.Random(171308)
n, m = 1000, 100000
edges = rand_tree_edges(n, lambda i: rng.randint(1, 32767), rng)
while len(edges) < m:
    u = rng.randint(1, n); v = rng.randint(1, n)
    if u != v:
        edges.append((u, v, rng.randint(1, 32767)))
dump(8, n, m, edges, "large random, M=max")

# ── 9. 顶格构造：逼近 ans 上界 2^64-1 ──
#     4 张互质大权值星形生成树 + 权值 17 的连通骨架（链）+ 随机填充（全为 17）。
#     G_w 连通 ⇒ w ∈ D（w 为 4 个大权值之一与 17）；G_d 连通的 d 只可能是
#     {1, 17, 181, 32761, 32749, 32719, 30911} 的子集（其余 d 使 G_d 边数不足），
#     故 ans = lcm(17, 32761, 32749, 32719, 30911) = 18446636557034669317
#     （占 2^64-1 的 99.9994%）。
rng = random.Random(171309)
n, m = 1000, 100000
BIGW = [32761, 32749, 32719, 30911]            # 两两互质、且均与 17 互质的大权值
SKELETON_W = 17                                # 连通骨架权重（其余边全为它，不引入新因子）
edges = []
for w in BIGW:
    for v in range(2, n + 1):
        edges.append((1, v, w))                # 星形生成树，999 条边，保证 G_w 连通
for v in range(2, n + 1):
    edges.append((v - 1, v, SKELETON_W))       # SKELETON_W 的连通骨架，保证 G_w 对该 w 连通
SCAFFOLD = len(edges)                          # 4*999 + 999 = 4995
FILL = m - 2 - SCAFFOLD                        # 留 2 条给 32767
while len(edges) < SCAFFOLD + FILL:            # 其余用 SKELETON_W 随机填充（不引入新的可行 d）
    u = rng.randint(1, n)
    v = rng.randint(1, n)
    if u != v:
        edges.append((u, v, SKELETON_W))
while len(edges) < m:                          # 2 条 32767：把 d_i 顶到题面上限；仅这 2 条边不可能连通
    u = rng.randint(1, n)
    v = rng.randint(1, n)
    if u != v:
        edges.append((u, v, 32767))
dump(9, n, len(edges), edges, "bespoke near-2^64 answer, d=max")

# ── 10. 顶格卡常：约数最多的权值 27720（τ=96）+ 2 条 32767 抬 maxW ──
n, m = 1000, 100000
HIGH_DIV = 27720                               # = 2^3*3^2*5*7*11，τ(27720)=96（≤32767 内最多）
edges = []
for i in range(2, n + 1):
    edges.append((i, i - 1, HIGH_DIV))         # 生成树骨架，保证连通
while len(edges) < m - 2:
    u = (len(edges) % n) + 1
    edges.append((u, (u % n) + 1, HIGH_DIV))
while len(edges) < m:
    edges.append((1, 2, 32767))
dump(10, n, len(edges), edges, "top worst-case divisor count (tau=96), d=max")
