#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1420《Dijkastra(II)》数据生成器
#
# 题面（自网络题解重建，三来源交叉验证一致）：
#   输入：第一行 n m；接下来 m 行 s t d（无向边）。
#   输出：1 到 n 的最短距离（一个整数）。
#   数据范围（有来源依据，非臆造）：N≤200000, M≤400000, 1≤S,T≤N, 0≤D≤10^9。
#
# 分层设计（图结构分层：链/菊花/随机/顶格 + 卡堆优化的稠密图）：
#   点 1    边界层：n=1（输出 0）、n=2 最小边权
#   点 2    边界层：n=2 顶格权值 1e9（验证 long long）
#   点 3-4  小规模随机（可手算验证量级），含重边/自环/0权（复刻样例特征）
#   点 5-6  中等规模随机：链结构 / 菊花结构
#   点 7-8  大规模：卡堆优化的稠密图（n=1e5, m=4e5 稠密随机 + 干扰边）、
#           顶格链（n=2e5, m=4e5，全是 1e9 权 → 距离和 2e14 顶格卡 long long）
#   点 9-10 顶格层：n=200000, m=400000 顶格随机大图 + 菊花顶格
#
# 时间限制 1000 ms / 内存 131072 KB（128 MB）：std 堆优化 Dijkstra
# O((N+M)logN)，邻接表 2*4e5*12B ≈ 10 MB，实际运行 < 200 ms。

from cyaron import *  # 引入CYaRon的库
import random

random.seed(1420)  # 固定随机种子，可复现

NMAX = 200000
MMAX = 400000
DMAX = 10 ** 9


def write_case(i, n, edges, note):
    """edges: list of (s, t, d)。写成 problem{i}.in 并用 ../std 生成 .out。"""
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(n, len(edges))
    for (s, t, d) in edges:
        io.input_writeln(s, t, d)
    io.output_gen("../std")
    with open("problem%d.out" % i) as f:
        ans = f.read().strip()
    print("problem%-2d: n=%-6d m=%-6d ans=%s -- %s" % (i, n, len(edges), ans, note))
    return ans


def rand_connected(n, extra, wmax):
    """随机连通无向图：随机生成树 + extra 条随机边（允许重边/自环）。"""
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    edges = []
    for i in range(1, n):
        u = perm[i]
        v = perm[random.randrange(0, i)]
        edges.append((u, v, random.randint(0, wmax)))
    for _ in range(extra):
        u = random.randint(1, n)
        v = random.randint(1, n)
        edges.append((u, v, random.randint(0, wmax)))
    return edges


def chain(n, extra_ratio, wmax):
    """链结构：1-2-3-...-n 主链 + 随机短边（跳跃链接，权值偏大保证主链是最短路）。"""
    edges = []
    for i in range(1, n):
        edges.append((i, i + 1, random.randint(0, wmax // 10)))
    extra = extra_ratio
    for _ in range(extra):
        u = random.randint(1, n)
        v = min(n, u + random.randint(2, 10))
        if u == v:
            v = min(n, v + 1)
        edges.append((u, v, random.randint(wmax // 2, wmax)))
    return edges


def flower(n, m, wmax):
    """菊花结构：中心 1（或 n）连所有点 + 补足随机边（短路边多、答案多为 2 跳）。"""
    edges = []
    center = 1
    for v in range(2, n + 1):
        edges.append((center, v, random.randint(0, wmax)))
    # 补足到 m 条：随机叶间边（偏小权值，制造“经中心转一跳”竞争）
    while len(edges) < m:
        u = random.randint(2, n)
        v = random.randint(2, n)
        edges.append((u, v, random.randint(0, wmax // 4)))
    return edges[:m]


# ---- 点 1：边界层 n=1（图只有 1 个点，最短路为 0；m=0） ----
write_case(1, 1, [], "边界层：n=1, m=0，答案 0（1 到自身）")

# ---- 点 2：边界层 n=2，顶格权值 1e9（验证 long long 距离） ----
write_case(2, 2, [(1, 2, DMAX)], "边界层：n=2 顶格权值 d=1e9，答案 1000000000")

# ---- 点 3：小规模随机（可手算验证），复刻样例特征：重边 + 自环 + 0 权 ----
# 手算：1-2 权 1，1-2 权 3（重边），2-2 权 0（自环），3 为孤立点由 2-3 连通
write_case(3, 3, [(1, 2, 1), (1, 2, 3), (2, 2, 0), (2, 3, 7), (1, 3, 100)],
           "小规模随机：重边+自环+0权（复刻样例特征），手算答案 8（1-2-3）")

# ---- 点 4：小规模随机（n=10, m=25 可手算量级，稠密小图） ----
write_case(4, 10, rand_connected(10, 16, 1000),
           "小规模随机：n=10 稠密小图，含重边/自环")

# ---- 点 5：中等规模链结构（n=5000, m≈15000） ----
write_case(5, 5000, chain(5000, 10000, DMAX // 100),
           "中等规模：链结构+跳跃干扰边，主链为最短路")

# ---- 点 6：中等规模菊花结构（n=5000, m=20000） ----
write_case(6, 5000, flower(5000, 20000, DMAX // 100),
           "中等规模：菊花结构（中心 1 直连所有点）")

# ---- 点 7：卡堆优化的稠密图（n=100000, m=400000 顶格边数） ----
# 稠密随机 + 大量重复更新：边权集中在小区间，堆中产生大量 decrease-key 堆项
dense_edges = rand_connected(100000, 400000 - 99999, DMAX // 10)
write_case(7, 100000, dense_edges,
           "大规模：卡堆优化稠密图 n=1e5, m=4e5 顶格边数，权值小区间密集更新")

# ---- 点 8：顶格链（n=200000, m=400000，主链权值 1e9 顶格） ----
# 主链 n-1 条边权 1e9 → dis[n] = 199999 * 1e9 ≈ 2e14，卡 long long 距离
long_chain = chain(200000, 400000 - 199999, DMAX)
# 把主链边权强制为顶格 1e9
for i in range(199999):
    long_chain[i] = (i + 1, i + 2, DMAX)
write_case(8, 200000, long_chain,
           "大规模顶格链：n=2e5, m=4e5，主链全 1e9 权 → 答案 199999*1e9≈2e14 卡 long long")

# ---- 点 9：顶格随机大图（n=200000, m=400000 顶格） ----
write_case(9, 200000, rand_connected(200000, 400000 - 199999, DMAX),
           "顶格层：n=2e5, m=4e5 顶格随机连通图，权值全区间 0..1e9")

# ---- 点 10：顶格菊花（n=200000, m=400000 顶格，中心直连） ----
write_case(10, 200000, flower(200000, 400000, DMAX),
           "顶格层：菊花结构 n=2e5, m=4e5，中心 1 直连全部点+叶间边")
