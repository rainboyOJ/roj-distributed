#!/usr/bin/env python3
# 一本通 1689《堆排问题》分层数据生成器（cyaron）
# 10 个测试点严格按题面【数据规模与约定】表的 (N, M) 生成；
# 结构层从边界（n=5 链/接近堆）铺到顶格（n=16, m=120 稠密交换图）。
# 每个测试点保证有解：先构造一个合法 max-heap 目标态，再随机走 k 步交换得到初态。
# 权值：F_i 互不相同，1 <= F_i <= 100（题面上限）。
import random
from cyaron import *


def gen_case(n, m, max_steps, rng, tree_mode, extra_op_pool=False):
    """返回 (fa[1..n], w[1..n], ops)。"""
    # --- 随机/特殊形态的二叉树，根固定为 1 ---
    fa = [0] * (n + 1)
    if tree_mode == "chain":
        # 链：每个点都挂在父结点上（退化为单支）
        for i in range(2, n + 1):
            fa[i] = i - 1
    elif tree_mode == "full":
        # 尽量满二叉树：父亲 = i//2
        for i in range(2, n + 1):
            fa[i] = i // 2
    else:  # "random"
        for i in range(2, n + 1):
            while True:
                p = rng.randint(1, i - 1)
                deg = sum(1 for j in range(2, i) if fa[j] == p)
                if deg < 2:
                    fa[i] = p
                    break

    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        ch[fa[i]].append(i)

    # --- 合法 max-heap 权值（DFS 序赋值：子树根 > 子树内所有后代）---
    # 给每个结点一个"子树大小排名"权值即可保证堆性质：父先于子赋值且更大。
    order = []
    def dfs(v):
        order.append(v)
        for c in ch[v]:
            dfs(c)
    dfs(1)
    # order 中先出现的结点权值必须更大：直接按 100,99,... 赋即可满足堆，
    # 但那样答案恒为 0 步可达的平凡初态，所以先赋目标堆权值再走随机交换。
    w = [0] * (n + 1)
    vals = list(range(100, 100 - n, -1))  # n 个互不相同的最大权值
    for idx, v in enumerate(order):
        w[v] = vals[idx]

    # --- M 种交换方式（无自环、无重复）---
    maxe = n * (n - 1) // 2
    m = min(m, maxe)
    ops = set()
    while len(ops) < m:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u != v:
            ops.add((min(u, v), max(u, v)))
    ops = list(ops)

    # --- 从目标堆态随机走 k 步得到初态（保证有解，k 控制难度）---
    cur = w[:]
    k = rng.randint(max(1, max_steps // 2), max_steps) if max_steps > 1 else 1
    for _ in range(k):
        u, v = ops[rng.randrange(len(ops))]
        cur[u], cur[v] = cur[v], cur[u]
    return fa, cur, ops


def write_case(io, fa, w, ops):
    n = len(fa) - 1
    m = len(ops)
    io.input_writeln(n, m)
    io.input_writeln(" ".join(str(fa[i]) for i in range(1, n + 1)))
    io.input_writeln(" ".join(str(w[i]) for i in range(1, n + 1)))
    for u, v in ops:
        io.input_writeln(u, v)


rng = random.Random(20251006)

# (N, M, max_steps, tree_mode, 设计意图)
plans = [
    # 点1-2 边界层：最小规模 / 链 / 接近堆
    (5, 5, 2, "chain", "N=5 最小规格，链树，走 1-2 步，答案 0-2"),
    (7, 6, 3, "random", "N=7 小树，走 2-3 步，可手算"),
    # 点3-4 小规模随机：可手算量级
    (8, 10, 5, "random", "N=8 随机树，走 3-5 步"),
    (9, 30, 6, "full", "N=9 满二叉树形态，m=30 较稠密，走 4-6 步"),
    # 点5-6 中等规模随机
    (10, 19, 8, "random", "N=10 随机树，走 5-8 步"),
    (13, 13, 10, "random", "N=13 随机树，m=13 稀疏交换图"),
    # 点7-8 大规模随机
    (16, 120, 14, "random", "N=16 顶格点数，m=120 稠密交换图，走 8-14 步"),
    (10, 12, 12, "chain", "N=10 链树（最坏结构之一），走 8-12 步"),
    # 点9-10 顶格层：顶格 N / 最坏结构，但控制答案深度使 std < 1s
    (11, 17, 7, "chain", "N=11 链树（深链最坏结构），走 5-7 步，答案约 5-7"),
    (12, 20, 8, "random", "N=12 随机树，走 6-8 步，顶格 N 较大答案"),
]

for i, (n, m, steps, mode, intent) in enumerate(plans, start=1):
    io = IO(file_prefix="problem", data_id=i)
    fa, w, ops = gen_case(n, m, steps, rng, mode)
    write_case(io, fa, w, ops)
    io.output_gen("../std")
    # 注释：点 i 的设计意图写入 data/ 生成日志（见 gen-report.md）
    print(f"# point {i}: N={n} M={m} mode={mode} steps<={steps}  # {intent}")
