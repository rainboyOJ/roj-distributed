#!/usr/bin/env python
# 1695《独特的树叶》数据生成器（cyaron 惯例，产出到本目录：problem1.in/.out ... problem10.in/.out）
#
# 题意：树 A（n 点）加一个叶子、重编号后得到树 B（n+1 点），求 B 中“多余的叶子”的最小编号。
# 范围：1 <= n <= 1e5，单组数据。
#
# 生成思路（分层，覆盖边界/小/中/大/顶格）：
#   点 1  n=1（最小规模：A 为空树，B 为单边，答案=1）
#   点 2  n=2（次小：B 为 3 点链/星，多答案 tie-break）
#   点 3  小随机 n∈[3,20]，构造强制“新叶编号为 1”（答案=1 的极端）
#   点 4  小随机 n∈[3,20]，全随机标签（可手算验证量级）
#   点 5  中随机 n∈[500,2000]，星形（全等子树、同构歧义最多的哈希对抗结构）
#   点 6  中随机 n∈[500,2000]，随机树
#   点 7  大随机 n=1e5，随机树
#   点 8  大随机 n=1e5，完全二叉树（海量相同子树，卡单哈希）
#   点 9  顶格 n=1e5，链 + 叶（最坏深度的换根 DP；若 std 用递归会爆栈）
#   点 10 顶格 n=1e5，“双扫帚/毛毛虫”结构（路径+两端簇状叶子，相同子树极多，
#          且故意把新叶标签随机，答案不固定，检验 tie-break 正确性）

import random
import os
from cyaron import *

MAXN = 100000


def build_parent_array(n, mode, rng):
    """返回 par[2..n]，A 的树以 1..n 标号（生成用），mode 决定树形态。"""
    par = [0] * (n + 1)
    if mode == "random":  # 随机树
        for v in range(2, n + 1):
            par[v] = rng.randint(1, v - 1)
    elif mode == "star":  # 星形：中心挂 n-1 个叶子（所有子树同构）
        for v in range(2, n + 1):
            par[v] = 1
    elif mode == "path":  # 链（最坏深度）
        for v in range(2, n + 1):
            par[v] = v - 1
    elif mode == "balanced":  # 完全二叉树（大量相同子树）
        for v in range(2, n + 1):
            par[v] = v // 2
    elif mode == "caterpillar":  # 毛毛虫：主链 + 随机挂叶
        spine = min(n, max(2, (n + 1) // 2))
        for v in range(2, spine + 1):
            par[v] = v - 1
        for v in range(spine + 1, n + 1):
            par[v] = rng.randint(1, spine)
    elif mode == "broom":  # 扫帚：短链 + 末端大星
        spine = max(1, n // 3)
        for v in range(2, spine + 1):
            par[v] = v - 1
        for v in range(spine + 1, n + 1):
            par[v] = spine
    elif mode == "broom2":  # 长链 + 随机挂叶在链两端附近（双扫帚）
        spine = max(2, n // 2)
        for v in range(2, spine + 1):
            par[v] = v - 1
        for v in range(spine + 1, n + 1):
            par[v] = rng.choice([1, spine])
    else:
        raise ValueError(mode)
    return par


def make_case(n, mode, seed, force_y_min=False, attach="leaf"):
    """生成一组完整数据：返回 (A边列表, B边列表)。
    force_y_min: 新叶标签强制为 1（构造答案=1 的极端）。
    attach: 新叶挂在 A 的哪个点上（'leaf'=随机叶子, 'random'=随机点）。"""
    rng = random.Random(seed)
    par = build_parent_array(n, mode, rng)
    A = [(par[v], v) for v in range(2, n + 1)]
    if n == 1:
        A = []
    # 选挂新叶的位置
    if n == 1:
        p = 1
    else:
        deg = [0] * (n + 1)
        for u, v in A:
            deg[u] += 1
            deg[v] += 1
        if attach == "leaf":
            leaves = [v for v in range(1, n + 1) if deg[v] <= 1]
        else:
            leaves = list(range(1, n + 1))
        p = rng.choice(leaves)
    # 标签重排
    labels = list(range(1, n + 2))
    rng.shuffle(labels)
    if force_y_min:
        y = 1
        sigma = labels[:n + 1]
        sigma = [l for l in sigma if l != 1]  # 去掉 1，剩 n 个标签
        if len(sigma) != n:  # 保险（不应发生）
            sigma = [l for l in range(2, n + 2)]
            rng.shuffle(sigma)
    else:
        sigma = labels[:n]
        y = labels[n]
    B = [(sigma[u - 1], sigma[v - 1]) for (u, v) in A]
    if n >= 1:
        B.append((sigma[p - 1] if n >= 1 else 1, y) if n > 1 else (sigma[0], y))
    rng.shuffle(B)
    return A, B


def emit(io, n, A, B):
    lines = [str(n)]
    for u, v in A:
        lines.append("%d %d" % (u, v))
    for u, v in B:
        lines.append("%d %d" % (u, v))
    io.input_writeln("\n".join(lines))


# ---------- 10 个分层测试点 ----------
CASES = [
    # (n, mode, seed, force_y_min, attach, 说明)
    (1, "random", 1001, False, "leaf", "点1: n=1 最小规模（A 空树，B 单边，答案 1）"),
    (2, "random", 1002, False, "leaf", "点2: n=2 边界（B 为 3 点结构，多答案 tie-break）"),
    (8, "random", 1003, True, "leaf", "点3: 小规模，新叶强制编号 1（答案=1 极端 + tie-break）"),
    (20, "random", 1004, False, "leaf", "点4: 小规模随机（可手算验证量级）"),
    (1000, "star", 1005, False, "leaf", "点5: 中等规模星形（所有子树同构，同构歧义最多）"),
    (2000, "random", 1006, False, "leaf", "点6: 中等规模随机树"),
    (MAXN, "random", 1007, False, "leaf", "点7: 顶格随机树"),
    (MAXN, "balanced", 1008, False, "leaf", "点8: 顶格完全二叉树（海量相同子树，卡单哈希）"),
    (MAXN, "path", 1009, False, "leaf", "点9: 顶格链（最坏深度换根 DP，卡递归爆栈）"),
    (MAXN, "broom2", 1010, False, "random", "点10: 顶格双扫帚（链+两端簇叶，相同子树极多且答案不固定）"),
]

for i, (n, mode, seed, fy, at, _desc) in enumerate(CASES, 1):
    io = IO(file_prefix="problem", data_id=i)
    A, B = make_case(n, mode, seed, force_y_min=fy, attach=at)
    emit(io, n, A, B)
    io.output_gen("../std")
    print("problem%d.in generated (n=%d, %s)" % (i, n, mode))
