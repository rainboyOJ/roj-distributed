#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1781《死亡之树》数据生成器（目标 ROJ 题号 1781）
#
# 题面范围：n<=10, m<=45（简单图，无重边）；分档 40% n<=10&m<=16 / 70% n<=10&m<=23 / 100% n<=10&m<=45。
# 所求 = 图中「恰好 k 个叶子」的生成树（点集=全体 n 点，按标号计数）的棵数。
# 因 n<=10，数据规模本身很小，分层按 (n, m, k, 图结构) 从边界铺到顶格。
#
# 分层设计（10 个测试点）：
#   点 1  边界层：n=2, m=1, k=2 —— 最小规模（单边，两点都是叶子），答案 1
#   点 2  边界层：n=2, m=1, k=1 —— k 不合法（度数定义下 2 点树必有 2 叶），答案 0
#   点 3  小层  ：n=3, m=3, k=2 —— 即题面【输入样例 1】，答案 3（可手算：3 条路径）
#   点 4  小层  ：n=4, m=6, k=3 —— 即题面【提示·样例输入 2】，答案 4（可手算：4 个星形）
#   点 5  小层  ：n=5, m=4, k=2 —— 稀疏树（路径，唯一生成树=自身），答案 1
#   点 6  边界层：n=6, m=4, k=2 —— 不连通（三角形+孤立边），答案 0（无生成树）
#   点 7  40% 档：n=7, m=16（该档 m 顶格）连通随机，k=3
#   点 8  70% 档：n=10, m=23（该档 n、m 均顶格）连通随机，k=4
#   点 9  顶格层：n=10, m=45, k=9 —— K10 满边，答案 10（手算：星形，选中心 10 种）
#   点 10 顶格层：n=10, m=45, k=2 —— K10 满边，答案 1814400（手算：哈密顿路 10!/2）
# 所有点满足 1<=n<=10、0<=m<=45（<=C(n,2)，无重边、无自环），k 由题面给定可为任意整数。
#
# 稳定性自检：生成后逐个读回 .out，断言为「单个整数且等于期望值」（点 7/8 期望仅断言 >0，
#   因随机图下 k 叶生成树棵数非闭式；若为 0 说明该点退化，脚本会报错以便换种子）。
#   这里 .out 由 subprocess 显式调用 ../std 产生（cyaron output_gen），非缓冲遗留，见下。
#
# 随机性：每个随机点使用独立 Random(1781 + 点号)，与调用顺序无关、可精确复现。
#
# 运行方式：先编译 std 到上一级目录（g++ -O2 -std=c++17 -o ../std std.cpp），
#          再在本目录（data/）下执行 python3 ../data.py。

import os
import random
import subprocess

from cyaron import *  # 引入 CYaRon 的库

STD = "../std"
EXPECT = {  # 可手算/闭式的点的期望答案
    1: 1,
    2: 0,
    3: 3,
    4: 4,
    5: 1,
    6: 0,
    9: 10,
    10: 1814400,
}


def norm_edges(edges):
    return set(tuple(sorted(e)) for e in edges)


def build_connected(n, m, rng):
    """构造 n 点 m 边的连通简单图：先随机生成树保证连通，再补随机边到 m 条，最后随机重标号。"""
    assert n - 1 <= m <= n * (n - 1) // 2
    order = list(range(1, n + 1))
    rng.shuffle(order)
    edges = []
    for idx in range(1, n):                       # 随机生成树：每个点随机连到已有点
        p = rng.randrange(idx)
        edges.append((order[idx], order[p]))
    used = norm_edges(edges)
    all_pairs = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    rest = [e for e in all_pairs if e not in used]
    if m > n - 1:
        edges += rng.sample(rest, m - (n - 1))    # 补边
    perm = list(range(1, n + 1))
    rng.shuffle(perm)                             # 随机重标号，避免固定形态
    edges = [(perm[a - 1], perm[b - 1]) for a, b in edges]
    rng.shuffle(edges)
    return edges


def emit(i, n, m, k, edges, note):
    """生成第 i 组数据：写 problem{i}.in，用 std 跑出 problem{i}.out，并读回自检。"""
    assert len(edges) == m and len(set(norm_edges(edges))) == m, "重边/边数不符"
    for a, b in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b, "非法边"
    # 用 with 确保 IO.close()：cyaron 的 output_gen 只 write 不 flush，
    # 不显式 close 会在断言时读到 0 字节 .out（已知隐患）。
    with IO(file_prefix="problem", data_id=i) as io:
        io.input_writeln(n, m, k)
        for a, b in edges:
            io.input_writeln(a, b)
        io.output_gen(STD)                        # 用 std 生成 .out

    inp = "problem%d.in" % i
    outp = "problem%d.out" % i
    assert os.path.exists(outp) and os.path.getsize(outp) > 0, "空 .out: %s" % outp
    with open(outp) as fh:
        lines = fh.read().split()
    assert len(lines) == 1, ".out 行数/词数异常: %r" % lines
    val = int(lines[0])
    # 复核：直接用 std 对同一输入再跑一遍，逐字节一致
    with open(inp, "rb") as fh:
        again = subprocess.run([STD], stdin=fh, capture_output=True).stdout.decode().strip()
    assert again == lines[0], "std 重跑不一致: %s vs %s" % (again, lines[0])
    if i in EXPECT:
        assert val == EXPECT[i], "点 %d 答案 %d != 期望 %d" % (i, val, EXPECT[i])
    else:
        assert val > 0, "点 %d 答案退化为 0（需换种子/参数）" % i
    print("problem%-2d: n=%-2d m=%-2d k=%-2d ans=%-9d  %s" % (i, n, m, k, val, note))


# ---------------- 点 1-6：边界/小规模（确定性） ----------------
emit(1, 2, 1, 2, [(1, 2)], "边界最小：单边，两点皆叶")
emit(2, 2, 1, 1, [(1, 2)], "边界无解：k=1 不可能（2 点树必有 2 叶）")
emit(3, 3, 3, 2, [(1, 2), (2, 3), (1, 3)], "题面样例1：K3，3 条路径")
emit(4, 4, 6, 3, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3), (2, 4)], "题面样例2：K4，4 个星形")
emit(5, 5, 4, 2, [(4, 1), (1, 5), (5, 3), (3, 2)], "稀疏树：路径（唯一生成树=自身），答案 1")
emit(6, 6, 4, 2, [(2, 5), (5, 6), (6, 2), (1, 3)], "不连通：三角形+孤立边，无生成树，答案 0")

# ---------------- 点 7-8：40% / 70% 档连通随机 ----------------
rng7 = random.Random(1781 + 7)
emit(7, 7, 16, 3, build_connected(7, 16, rng7), "40% 档 m 顶格（m=16）连通随机")
rng8 = random.Random(1781 + 8)
emit(8, 10, 23, 4, build_connected(10, 23, rng8), "70% 档 n,m 顶格（n=10,m=23）连通随机")

# ---------------- 点 9-10：100% 顶格 K10 ----------------
K10 = [(i, j) for i in range(1, 11) for j in range(i + 1, 11)]
emit(9, 10, 45, 9, list(K10), "顶格 K10：k=9 星形，手算 10")
emit(10, 10, 45, 2, list(K10), "顶格 K10：k=2 哈密顿路，手算 10!/2=1814400")

print("ALL 10 POINTS OK")
