#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 2125《查找文献》数据生成器（cyaron，仓库惯例）
# 用法：mkdir -p data && cd data && python3 ../data.py
# 数据范围（题面）：n <= 1e5, m <= 1e6，有向边 X->Y，从 1 号点出发
#   输出 DFS / BFS 遍历序（邻接点按编号升序访问，只输出可达点）。
# 分层设计：边界层(1-2) / 小规模随机(3-4) / 中等规模随机(5-6) /
#           大规模随机(7-8) / 顶格最坏结构(9-10，链、菊花、卡常输入序)。

from cyaron import *
import random

rnd = random.Random(21250000 + 2125)  # 固定种子，可复现


def edges_text(n, edges):
    """把 (n, m) 与边表写成输入文本，m 自动等于 len(edges)。"""
    lines = ["{} {}".format(n, len(edges))]
    lines += ["{} {}".format(x, y) for x, y in edges]
    return "\n".join(lines) + "\n"


def rand_edges(n, m, lo, hi, allow_self=True):
    """在 [lo, hi] 范围内随机 m 条有向边（允许重边，allow_self 控制自环）。"""
    out = []
    for _ in range(m):
        x = rnd.randint(lo, hi)
        y = rnd.randint(lo, hi)
        if not allow_self and x == y:
            y = lo + (y - lo + 1) % (hi - lo + 1)
        out.append((x, y))
    return out


for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out

    # ---- 点 1｜边界层：全最小值。n=1, m=0，答案恰好只有 "1"（答案长度=1 的极端）----
    if i == 1:
        n, edges = 1, []

    # ---- 点 2｜边界层：n=2 最小非平凡 + 题面特殊声明（1 号点可被别的文章引用）。
    #      边 1->2, 2->1 构成最小环，DFS=BFS=1 2 ----
    elif i == 2:
        n, edges = 2, [(1, 2), (2, 1)]

    # ---- 点 3｜小规模随机：n=20, m=30，可手算验证量级。
    #      前 3 条边保证从 1 出发有分支（否则可能退化为答案只有 1）----
    elif i == 3:
        n = 20
        edges = [(1, rnd.randint(2, n)) for _ in range(3)]
        edges += rand_edges(n, 27, 1, n, allow_self=False)

    # ---- 点 4｜小规模随机：n=80, m=200，故意含自环 / 重边 / 指向 1 的边 ----
    elif i == 4:
        n = 80
        edges = rand_edges(n, 196, 1, n, allow_self=True) + [(1, 1), (2, 2), (5, 1), (7, 1)]
        rnd.shuffle(edges)

    # ---- 点 5｜中等规模随机：n=5000, m=5e4（范围中间档）----
    elif i == 5:
        n = 5000
        edges = rand_edges(n, 50000, 1, n)

    # ---- 点 6｜中等规模随机：n=1e4, m=2e5（中间档偏密）----
    elif i == 6:
        n = 10000
        edges = rand_edges(n, 200000, 1, n)

    # ---- 点 7｜大规模随机：n=1e5, m=5e5（接近上限）。
    #      边只在 [1,7e4] 与 [7e4+1,n] 两个块内部，后 3e4 个点从 1 不可达，
    #      考察“只输出可达点”（答案长度 7e4 < n）----
    elif i == 7:
        n = 100000
        edges = rand_edges(n, 350000, 1, 70000) + rand_edges(n, 150000, 70001, 100000)

    # ---- 点 8｜大规模随机：n=1e5, m=1e6（顶格边数随机图），边顺序随机打乱 ----
    elif i == 8:
        n = 100000
        edges = rand_edges(n, 1000000, 1, n)
        rnd.shuffle(edges)

    # ---- 点 9｜顶格最坏结构（链）：n=1e5, m=1e6。
    #      主链 1->2->...->n，DFS 深度顶格（最坏递归/栈深度），
    #      再补随机边至 1e6（随机边会指向前面的点，形成大量回边/重边）----
    elif i == 9:
        n = 100000
        edges = [(x, x + 1) for x in range(1, n)]
        edges += rand_edges(n, 1000000 - len(edges), 1, n)

    # ---- 点 10｜顶格最坏结构（菊花 + 卡常输入序）：n=1e5, m=1e6。
    #      1 号点指向全部其余点（出度 99999，最大出度排序压力），
    #      其余随机边补至 1e6，全部边按 x 逆序输入（打乱输入顺序卡常）----
    elif i == 10:
        n = 100000
        edges = [(1, y) for y in range(2, n + 1)]
        edges += rand_edges(n, 1000000 - len(edges), 2, n)
        edges.sort(key=lambda e: -e[0])

    io.input_write(edges_text(n, edges))
    io.output_gen("../std")
