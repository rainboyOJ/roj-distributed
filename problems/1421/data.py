#!/usr/bin/env python

# 一本通 1421 Floyd 数据生成器
# 确证数据范围（来源：题解博客【提示】节，见 content.md 文末）：
#   N<=500, 0<=M<=250000, 1<=S,T<=N, -10^9<=D<=10^9，保证无负环。
# 无负环的构造手段：
#   A. 势函数法：任取势 p[]，基础权 w>=0，实际边权 d = w + p[s] - p[t]。
#      任意环上边权和 = sum(w) >= 0，天然无负环，且 d 可正可负（覆盖负权边）。
#   B. 非负边权（链/菊花/稀疏图用，肯定无负环）。
# 分层：链 / 菊花 / 稀疏负权 / 稠密随机负权 / 顶格 worst-case（n=500 满 m=250000），
# Floyd 恒为 O(n^3)≈1.25e8 松弛，顶格组即为时间 worst-case。

import random

from cyaron import *  # 引入CYaRon的库

N_MAX = 500
M_MAX = 250000
W = 10**9


def make_edges(rng, n, m, neg=False):
    """生成 m 条有向边（允许重边/自环）。neg=True 用势函数法混入负权。"""
    p = [0] + [rng.randint(-W, W) for _ in range(n)] if neg else None
    edges = []
    for _ in range(m):
        s = rng.randint(1, n)
        t = rng.randint(1, n)
        if neg:
            w = rng.randint(0, 2 * W // 4)
            d = w + p[s] - p[t]
            # 夹回 [-1e9, 1e9]（夹断后仍 >= p[s]-p[t]，环和依然 >=0）
            d = max(-W, min(W, d))
        else:
            d = rng.randint(0, W)
        edges.append((s, t, d))
    return edges


def write_graph(io, n, edges):
    io.input_writeln(n, len(edges))
    for (s, t, d) in edges:
        io.input_writeln(s, t, d)


for i in range(1, 11):
    rng = random.Random(142100 + i)
    io = IO(file_prefix="problem", data_id=i)  # problem1.in / problem1.out

    if i == 1:
        # 最小规模：n=1, m=0
        write_graph(io, 1, [])
    elif i == 2:
        # 题面样例
        write_graph(io, 2, [(1, 2, 1), (1, 2, 3), (2, 2, 0)])
    elif i == 3:
        # 链结构：1->2->...->40，少量负权随机边
        n = 40
        edges = [(v, v + 1, rng.randint(1, W)) for v in range(1, n)]
        edges += make_edges(rng, n, 60, neg=True)
        write_graph(io, n, edges)
    elif i == 4:
        # 菊花结构：中心 1 向外辐射 + 回边，不连通部分（点 31..40 孤立）
        n = 40
        edges = []
        for v in range(2, 31):
            edges.append((1, v, rng.randint(0, W)))
            edges.append((v, 1, rng.randint(0, W)))
        # 孤立点间加一条互达边，避免整组 Dis 全相等导致 S 退化为 0
        edges.append((31, 32, rng.randint(0, W)))
        edges.append((32, 31, rng.randint(0, W)))
        write_graph(io, n, edges)
    elif i == 5:
        # 稀疏负权随机图
        n = 80
        write_graph(io, n, make_edges(rng, n, 200, neg=True))
    elif i == 6:
        # 稠密随机图（非负权），n=200 满简单边
        n = 200
        write_graph(io, n, make_edges(rng, n, n * (n - 1), neg=False))
    elif i == 7:
        # 大规模稀疏负权
        n = 500
        write_graph(io, n, make_edges(rng, n, 2000, neg=True))
    elif i == 8:
        # 大规模稠密负权，含大量重边自环
        n = 500
        write_graph(io, n, make_edges(rng, n, 120000, neg=True))
    elif i == 9:
        # 顶格：n=500, m=250000 全正权
        n = 500
        write_graph(io, n, make_edges(rng, n, 250000, neg=False))
    else:
        # 顶格 worst-case：n=500, m=250000 负权混杂（Floyd O(n^3) 上界）
        n = 500
        write_graph(io, n, make_edges(rng, n, 250000, neg=True))

    io.output_gen("../std")
