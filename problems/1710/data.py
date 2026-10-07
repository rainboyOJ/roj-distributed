#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1710《构造完全图》分层测试数据生成器（cyaron）
#
# 题意：给定一棵树 T（N 个点，N-1 条边），求 T 能扩展出的边权和最小的完全图 G，
#       即：以 T 为唯一最小生成树的完全图的最小边权和。
#
# 数据范围（题面【数据规模】）：100%: N <= 100000，1 <= D_i <= 100000。
#   答案量级：最坏 Σ_{k=1}^{n-1} (k-1)*(10^5+1) + (n-1)*10^5 ≈ 5e14，需 long long。
#
# 分层设计（10 组，全部不超过题面上限）：
#   1  边界：n=1（唯一退化情形：无树边，完全图无边 -> 答案 0）
#   2  边界：n=2，D=1（最小规模 + 最小权值 -> 答案 1）
#   3  题面样例原样：n=4，星形，D∈{1,1,2} -> 答案 12（与【输出样例】逐字对齐）
#   4  小规模可手算/可暴力：n=10，随机树 + 权值含重复/边界值(1 与 1e5 各若干)
#   5  中等随机：n=1000，随机树，D 随机 [1,1e5]
#   6  中等随机：n=10000，随机树，D 随机 [1,1e5]（范围中间档）
#   7  大规模随机：n=100000，随机树（点编号随机置换），D 随机 [1,1e5]，边序打乱（卡排序）
#   8  大规模最坏结构：n=100000，链（合并块大小 1,2,3,... 最坏），D 全 1e5（顶格、全相等）
#      -> 存在闭式解 (D+1)*C(n,2)-(n-1)，用于解析级独立复算
#   9  顶格最坏结构：n=100000，星形（中心 1 连所有点），D 在输入中严格递减 1e5..2（逆序卡排序）
#  10  顶格 + 卡常：n=100000，随机树，D 随机 {1, 1e5} 两极（大量重复权值，卡排序/并查集）
#
# 生成方式：cyaron IO(file_prefix="problem", data_id=i) + io.output_gen("../std")。
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py

import random

from cyaron import IO

random.seed(20251005)

MAXN = 100000
MAXD = 100000


def rand_tree_edges(n, rng, mode="random", relabel=False):
    """返回 (u,v) 边列表（点编号 1..n），mode: random / chain / star。
    relabel=True 时对点编号做随机置换（打破 father<i 的结构规律）。"""
    edges = []
    if mode == "chain":
        for i in range(1, n):
            edges.append((i, i + 1))
    elif mode == "star":
        for i in range(2, n + 1):
            edges.append((1, i))
    else:  # random：每个点 i 随机接到 [1, i-1] 的父亲上（保证是树）
        for i in range(2, n + 1):
            edges.append((rng.randint(1, i - 1), i))
    if relabel and n > 1:
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        mp = {i + 1: perm[i] for i in range(n)}
        edges = [(mp[u], mp[v]) for u, v in edges]
    return edges


def build_case(data_id, n, edges, weights, rng, shuffle_edges=True):
    """edges: [(u,v)] 长度 n-1；weights: 长度 n-1 的权值列表。
    输出 problem{data_id}.in 并调用 std 生成 .out。"""
    triples = [(u, v, w) for (u, v), w in zip(edges, weights)]
    if shuffle_edges:
        rng.shuffle(triples)
    body = "\n".join("%d %d %d" % t for t in triples)
    text = "%d\n" % n + (body + "\n" if body else "")

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(text)
    io.output_gen("../std")
    return text


def main():
    # ---- 1. 边界：n=1（退化，无树边） ----
    build_case(1, 1, [], [], random, shuffle_edges=False)

    # ---- 2. 边界：n=2，D=1（最小规模 + 最小权值） ----
    build_case(2, 2, [(1, 2)], [1], random, shuffle_edges=False)

    # ---- 3. 题面样例原样（n=4，星形） ----
    build_case(3, 4, [(1, 2), (1, 3), (1, 4)], [1, 1, 2], random, shuffle_edges=False)

    # ---- 4. 小规模：n=10，含重复值与权值两端（可暴力验证） ----
    e4 = rand_tree_edges(10, random)
    w4 = [1, 1, 2, 3, 100000, 100000, 50, 50, 7]
    assert len(w4) == len(e4)
    build_case(4, 10, e4, w4, random)

    # ---- 5. 中等：n=1000 随机树，D ∈ [1,1e5] ----
    e5 = rand_tree_edges(1000, random)
    w5 = [random.randint(1, MAXD) for _ in range(999)]
    build_case(5, 1000, e5, w5, random)

    # ---- 6. 中等：n=10000 随机树，D ∈ [1,1e5] ----
    e6 = rand_tree_edges(10000, random)
    w6 = [random.randint(1, MAXD) for _ in range(9999)]
    build_case(6, 10000, e6, w6, random)

    # ---- 7. 大规模：n=1e5 随机树（点编号随机置换，边序打乱），D ∈ [1,1e5] ----
    e7 = rand_tree_edges(MAXN, random, relabel=True)
    w7 = [random.randint(1, MAXD) for _ in range(MAXN - 1)]
    build_case(7, MAXN, e7, w7, random)

    # ---- 8. 大规模最坏结构：n=1e5 链，D 全 1e5（顶格） ----
    e8 = rand_tree_edges(MAXN, random, mode="chain")
    w8 = [MAXD] * (MAXN - 1)
    build_case(8, MAXN, e8, w8, random)

    # ---- 9. 顶格最坏结构：n=1e5 星形，权值在输入中严格递减 1e5..2（逆序卡排序） ----
    e9 = rand_tree_edges(MAXN, random, mode="star")
    w9 = [MAXD - i for i in range(MAXN - 1)]  # 100000, 99999, ..., 2（逆序输入）
    build_case(9, MAXN, e9, w9, random, shuffle_edges=False)

    # ---- 10. 顶格卡常：n=1e5 随机树，D ∈ {1,1e5}（大量重复权值） ----
    e10 = rand_tree_edges(MAXN, random)
    w10 = [random.choice((1, MAXD)) for _ in range(MAXN - 1)]
    build_case(10, MAXN, e10, w10, random)

    print("all 10 cases generated")


if __name__ == "__main__":
    main()
