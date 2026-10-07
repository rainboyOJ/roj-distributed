#!/usr/bin/env python3
# 2124《图的遍历》分层数据生成器（cyaron）
# 用法：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && python3 ../data.py
# 产出：data/problem1.in / problem1.out ... problem10.in / problem10.out
# 题面数据范围：1 <= N, M <= 1e5（单组数据）。
# 分层策略：边界层(1-2) -> 小规模随机(3-4) -> 中等规模随机(5-6) -> 大规模随机(7-8)
#           -> 顶格层(9-10)；图结构覆盖 链 / 菊花 / 随机图 / 顶格卡常。

from cyaron import *  # 引入 CYaRon 的库

import random

random.seed(2124)  # 固定种子，保证数据可复现


def write_graph(io, n, edges):
    """写入一张有向图：首行 N M，随后每行一条边 u v（与题面输入格式一致）。"""
    io.input_writeln(n, len(edges))
    for u, v in edges:
        io.input_writeln(u, v)


def rand_edges(n, m, self_loop=False, repeated=True):
    """随机有向边 m 条。repeated=False 时不允许重边（自环按 self_loop 开关）。"""
    if not repeated:
        cap = n * (n - 1) if not self_loop else n * n
        assert m <= cap, "simple graph edge overflow: %d > %d" % (m, cap)
    edges = []
    used = set()
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if not self_loop and u == v:
            continue
        if not repeated and (u, v) in used:
            continue
        used.add((u, v))
        edges.append((u, v))
    return edges


for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out

    if i == 1:
        # 点1 边界层：全最小值 N=M=1，含题面未禁止的自环特例；期望输出 "1"。
        n, edges = 1, [(1, 1)]
    elif i == 2:
        # 点2 边界层：N=2 最小非平凡图；A(1)=1 是答案的最小可能值（答案极小极端），
        # 边 (2,1) 反向，1 无法到达 2；期望输出 "1 2"。
        n, edges = 2, [(2, 1)]
    elif i == 3:
        # 点3 小规模随机：N=12, M=15 简单有向图，可手工 BFS 逐点核对。
        n = 12
        edges = rand_edges(n, 15, self_loop=False, repeated=False)
    elif i == 4:
        # 点4 小规模随机：N=80, M=200 稀疏随机有向图（手算量级上界）。
        n = 80
        edges = rand_edges(n, 200, self_loop=False, repeated=False)
    elif i == 5:
        # 点5 中等规模随机：N=2000, M=5000，对应提示中 60% 数据档位的规模。
        n = 2000
        edges = rand_edges(n, 5000, self_loop=False, repeated=False)
    elif i == 6:
        # 点6 中等规模菊花：N=5000, M=5199。
        # 结构：所有点 -> 中心 N（逆向菊花），全部答案都等于 N（答案全相等），
        # 再混入 200 条随机边打破单一结构。
        n = 5000
        edges = [(v, n) for v in range(1, n)]           # 花瓣连向中心
        edges += rand_edges(n, 200, self_loop=False, repeated=False)
    elif i == 7:
        # 点7 大规模随机：N=50000, M=80000，接近上限的随机有向图。
        n = 50000
        edges = rand_edges(n, 80000, self_loop=False, repeated=True)
    elif i == 8:
        # 点8 大规模随机：N=90000, M=100000（M 顶格、N 接近上限），随机稠密图。
        n = 90000
        edges = rand_edges(n, 100000, self_loop=False, repeated=True)
    elif i == 9:
        # 点9 顶格-链：N 顶格 100000，链边 M=99999，正向链 1->2->...->N。
        # 结构最坏：DFS 递归深度达 1e5（卡递归实现），且答案全部等于 N（全相等）。
        n = 100000
        edges = [(v, v + 1) for v in range(1, n)]
    else:
        # 点10 顶格-卡常：N=100000, M=100000 同时取题面上限，
        # 随机有向图并允许重边（题面未禁，覆盖重复值），压测规模与常数。
        n = 100000
        edges = rand_edges(n, 100000, self_loop=False, repeated=True)

    write_graph(io, n, edges)
    io.output_gen("../std")  # 用编译好的标程生成 .out
