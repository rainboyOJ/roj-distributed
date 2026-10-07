#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 一本通 1735《环上计数》（目标 ROJ 题号 1735）测试数据生成器
#
# 题意（content.md）：多组数据。每组给一张 n 个点 m 条边的无向图（点从 0 编号，
#   保证无重边、无自环，不保证连通）。求：
#     ans1 = 不在任何简单环上的边数（= 桥数）；
#     ans2 = 在至少两个简单环上的边数（= 所有「边数 > 点数」的点双连通分量边数之和）。
#   读到 "0 0" 结束；每组输出一行 "ans1 ans2"。
# 数据范围（content.md / config.json）：1 <= n <= 10000，1 <= m <= 100000；多组数据，
#   以 "0 0" 结尾；time 1000 ms / memory 32 MB。
#   注：题面显式给出 m >= 1，故不生成 m=0 的组（n=1 在无自环前提下不可达 -> 边界从 n=2,m=1 起）。
#
# ---------------------------------------------------------------------------
# 10 个测试点的分层（详见 gen-report.md 的分层表；每个 .in 内可含多组数据）
# ---------------------------------------------------------------------------
#   点  层                     规模（各组之和）             设计意图
#   --  ---------------------  --------------------------  ---------------------------------
#   1   边界层（最小规模）     8 组，n<=6                   最小可行边界 n=2,m=1；三角形/四边形/
#                                                         菱形/K2,3/“8 字”/双三角/三角+独立边，
#                                                         全部手推闭式
#   2   边界层（题面特殊值）   1 组（题面样例原样）          题面声明的特殊值，.in/.out 与题面
#                                                         逐字节一致
#   3   小规模随机             12 组，n<=14                  可手算量级；含树/星/环/双环+桥闭式
#   4   小规模·定向结构        9 组，6<=n<=10               菱形共点、共享边双环、θ 图、带弦环、
#                                                         K4、立方体、Petersen、双环+桥、混合
#   5   中等规模               6 组，n<=1003                随机 + 星/大环/带弦大环/哑铃（闭式）
#   6   中等规模·定向          6 组，n<=10000               扇形三角剖分（单块 m>n）、顶点仙人掌、
#                                                         深链树（递归压力）、随机、森林、θ 图
#   7   大规模随机             4 组，n<=10000，m<=30000    稀疏随机中间档
#   8   大规模随机(近顶格)     4 组，n=10000，m≈1e5        顶格边数随机
#   9   顶格·最坏结构          6 组，m<=1e5                 K447（最大单块）、大环、长链三角、
#                                                         共享长路径双环、菱形链、100×K44
#   10  顶格·多组满规模        6 组，总边数 ~52 万           3×满随机 + K447 + 长链树 + 扇形
#                                                         （多组重置逻辑 + 吞吐压力）
#
# 生成方式（cyaron）：
#   cd data && python3 ../data.py     # 需先 g++ -O2 -std=c++17 std.cpp -o std
#   IO(file_prefix="problem", data_id=i) + io.input_write(text) + io.output_gen("../std")
#   ⚠ 已知坑：std 不存在时 cyaron 会静默产出 0 字节 .out —— 本文件在生成前检查
#    ../std 存在，生成后逐点回读断言 .out 非空、行数 == 组数（见 verify 段）。
#
# 生成后自检（全部 O(输入长度)，无 O(n^2) 循环）：
#   (a) .in：能恰好解析出「若干组 + 结尾 0 0」，每组 1<=n<=10000、1<=m<=100000、
#       无自环、无重边、端点 < n；
#   (b) .out：非空、行数恰为组数、每行 2 个整数、0 <= ans1 + ans2 <= m_组；
#   (c) 闭式核对：每个点中「结构可手推」的组给出与 std 完全无关的期望答案
#       （K447 -> (0,99681)、单环 -> (0,0)、树/森林 -> (边数,0)、扇形 -> (0,2n-3)、
#        菱形/θ/K4/立方体/Petersen/共享长路径双环 等）。
# 随机部分使用每点独立种子 random.Random(173500 + i)，可精确复现。

import os
import random
import sys

from cyaron import IO

N_MAX = 10000
M_MAX = 100000

# 题面【输入样例】原样（点 2 使用）
SAMPLE_TEXT = ("8 10\n"
               "0 1\n1 2\n2 3\n3 0\n3 4\n4 5\n5 6\n6 7\n7 4\n5 7\n"
               "0 0\n")
SAMPLE_ANSWER = (1, 5)


# ---------------------------------------------------------------------------
# 图构造小工具（全部 O(m)）
# ---------------------------------------------------------------------------

def random_simple_graph(n, m, rng):
    """n 个点 m 条边的无重边无自环随机图（set 去重，期望 O(m)）。"""
    if m > n * (n - 1) // 2:
        raise ValueError("m 超过完全图边数")
    seen = set()
    edges = []
    while len(edges) < m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        if u > v:
            u, v = v, u
        key = u * n + v
        if key in seen:
            continue
        seen.add(key)
        edges.append((u, v))
    return edges


def path_edges(n, base=0):
    return [(base + i, base + i + 1) for i in range(n - 1)]


def cycle_edges(n, base=0):
    return [(base + i, base + (i + 1) % n) for i in range(n)] if n >= 3 else []


def star_edges(n):
    return [(0, i) for i in range(1, n)]


def triangle_chain(n_tri, base=0):
    """n_tri 个三角形依次共享一个割点：三角形 j 用点 (2j, 2j+1, 2j+2)。"""
    e = []
    for j in range(n_tri):
        a, b, c = base + 2 * j, base + 2 * j + 1, base + 2 * j + 2
        e += [(a, b), (b, c), (a, c)]
    return e


def diamond_edges(a, b, c, d):
    """菱形（K4 去掉一条边）：点 a,b,c,d，缺边 (c,d)。5 条边，5>4 -> 整块计入 ans2。"""
    return [(a, b), (a, c), (b, c), (a, d), (b, d)]


def diamond_chain(k, base=0):
    """k 个菱形共享割点串成链：第 j 个与第 j+1 个共享一个顶点。"""
    e = []
    cur = base
    for _ in range(k):
        e += diamond_edges(cur, cur + 1, cur + 2, cur + 3)
        cur += 3                      # 共享最后一个点
    return e


def fan_triangles(n):
    """扇形三角剖分：0 为扇心，三角形 (0,i,i+1)，i=1..n-2。整图 m=2n-3 单块。"""
    return [(0, i) for i in range(1, n)] + [(i, i + 1) for i in range(1, n - 1)]


def complete_graph(n, base=0):
    e = []
    for u in range(n):
        for v in range(u + 1, n):
            e.append((base + u, base + v))
    return e


def cube_edges():
    """立方体 Q3：8 点 12 边（3-连通 -> 每条边 >=2 环）。"""
    e = []
    for i in range(4):                # 上下两个四边 + 4 条竖边
        e.append((i, (i + 1) % 4))
        e.append((4 + i, 4 + (i + 1) % 4))
        e.append((i, 4 + i))
    return e


def petersen_edges():
    """Petersen 图：10 点 15 边（3-连通 -> 每条边 >=2 环）。"""
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, 5 + i) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return outer + spokes + inner


def theta_edges(a, b, c):
    """θ 图：0 与 1 之间三条内部不相交路径，边长 a,b,c。点数 = a+b+c-1，边数 = a+b+c。"""
    e = []
    cur = 2
    for length in (a, b, c):
        prev = 0
        for _ in range(length - 1):
            e.append((prev, cur))
            prev = cur
            cur += 1
        e.append((prev, 1))
    return e


def groups_to_text(groups):
    """groups: [(n, edges), ...] -> 'n m' + m 行 + 结尾 '0 0'。"""
    out = []
    for n, edges in groups:
        out.append("%d %d" % (n, len(edges)))
        for u, v in edges:
            out.append("%d %d" % (u, v))
    out.append("0 0")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# 各测试点构造：返回 (note, groups, closed)
#   groups: [(n, edges)]；closed: 与 groups 等长的期望答案列表（None 表示不核）
# ---------------------------------------------------------------------------

def build_point(i):
    rng = random.Random(173500 + i)

    # ---------------- 点 1：边界层 · 最小规模（全部手推闭式） ----------------
    if i == 1:
        tri = [(0, 1), (1, 2), (0, 2)]
        g = [
            (2, [(0, 1)]),                             # 最小可行规模（题面 m>=1）：单边桥
            (3, tri),                                  # 三角形：0 0
            (4, cycle_edges(4)),                       # 四边形：0 0
            (4, diamond_edges(0, 1, 2, 3)),            # 菱形：整块 5 条边 >=2 环
            (5, [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]),  # K2,3：0 6
            (5, tri + [(0, 3), (3, 4), (0, 4)]),       # “8 字”双三角共享点：0 0
            (6, tri + [(3, 4), (4, 5), (3, 5)]),       # 两个不相交三角形：0 0
            (6, tri + [(3, 4)]),                       # 三角形 + 一条独立边：1 0
        ]
        closed = [(1, 0), (0, 0), (0, 0), (0, 5), (0, 6), (0, 0), (0, 0), (1, 0)]
        return ("边界层：最小规模 8 组（n=2,m=1；三角形/四边形/菱形/K2,3/8 字/双三角/三角+独立边），全部手推闭式",
                g, closed)

    # ---------------- 点 2：边界层 · 题面样例原样 ----------------
    if i == 2:
        g = [(8, [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7), (7, 4), (5, 7)])]
        return ("边界层：题面【输入样例】原样（n=8, m=10），.in/.out 与题面逐字节一致",
                g, [SAMPLE_ANSWER])

    # ---------------- 点 3：小规模随机（12 组，含闭式树/星/环） ----------------
    if i == 3:
        g, closed = [], []
        for _ in range(6):                             # 6 组小随机
            n = rng.randint(2, 12)
            m = rng.randint(1, min(n * (n - 1) // 2, 20))
            g.append((n, random_simple_graph(n, m, rng)))
            closed.append(None)
        g.append((12, path_edges(12)))                 # 树：11 条桥
        closed.append((11, 0))
        g.append((10, star_edges(10)))                 # 星：9 条桥
        closed.append((9, 0))
        # 两个三角形 + 一条连接桥 + 孤立点：ans1=1, ans2=0
        g.append((7, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)]))
        closed.append((1, 0))
        g.append((14, path_edges(14)))                 # 深链树：13 0
        closed.append((13, 0))
        g.append((12, cycle_edges(12)))                # 单环：0 0
        closed.append((0, 0))
        g.append((12, cycle_edges(4) + cycle_edges(4, 4) + cycle_edges(4, 8)))  # 三个不相交 4 环
        closed.append((0, 0))
        return ("小规模随机：6 组 n<=12 随机图 + 树/星/桥接/深链/单环/三环 6 组（闭式核对）",
                g, closed)

    # ---------------- 点 4：小规模 · 定向结构（全部闭式） ----------------
    if i == 4:
        g1 = diamond_edges(0, 1, 2, 3) + diamond_edges(0, 4, 5, 6)        # 两菱形共点 -> 0 10
        # 两个 4 环共享边 (1,2)：0-1-2-3-0 与 1-2-4-5-1 -> 单块 m=7>n=6
        g2 = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 5), (5, 1)]
        g3 = theta_edges(2, 3, 4)                                         # θ 图 n=8,m=9 -> 0 9
        g4 = cycle_edges(6) + [(0, 3)]                                    # 6 环+弦 -> 0 7
        g5 = complete_graph(4)                                            # K4 -> 0 6
        g6 = cube_edges()                                                 # 立方体 -> 0 12
        g7 = petersen_edges()                                             # Petersen -> 0 15
        g8 = cycle_edges(4) + [(0, 4)] + cycle_edges(3, 4)                # 双环+桥 -> 1 0
        g9 = [(0, 1), (1, 2), (0, 2), (2, 3)] + diamond_edges(3, 4, 5, 6)  # 三角+桥+菱形 -> 1 5
        g = [
            (7, g1), (6, g2), (8, g3), (6, g4), (4, g5), (8, g6), (10, g7),
            (7, g8), (7, g9),
        ]
        closed = [(0, 10), (0, 7), (0, 9), (0, 7), (0, 6), (0, 12), (0, 15), (1, 0), (1, 5)]
        return ("小规模·定向结构：菱形共点、共享边双环、θ 图、带弦环、K4、立方体、Petersen、双环+桥、三角+桥+菱形（全部手推闭式）",
                g, closed)

    # ---------------- 点 5：中等规模（n<=1003，6 组） ----------------
    if i == 5:
        # 哑铃：500 环（点 0..499）+ 3 个中转点 500..502 + 503..1002 的 500 环，
        # 4 条连接边全为桥 -> n=1003, m=1004, ans=(4,0)
        g6 = (cycle_edges(500) + cycle_edges(500, 503) +
              [(0, 500), (500, 501), (501, 502), (502, 503)])
        g = [
            (1000, random_simple_graph(1000, 1500, rng)),
            (1000, random_simple_graph(1000, 5000, rng)),
            (1000, star_edges(1000)),                                   # 999 0
            (1000, cycle_edges(1000)),                                  # 0 0
            (1000, cycle_edges(1000) + [(0, 500)]),                     # 单块 m=n+1 -> 0 1001
            (1003, g6),                                                 # 4 0
        ]
        closed = [None, None, (999, 0), (0, 0), (0, 1001), (4, 0)]
        return ("中等规模：n=1000 随机 2 组 + 星/大环/带弦大环/哑铃（闭式核对）", g, closed)

    # ---------------- 点 6：中等规模 · 定向（n=10000 为主，6 组） ----------------
    if i == 6:
        g = [
            (10000, fan_triangles(10000)),                    # 扇形单块 m=19997 -> 0 19997
            (10000, triangle_chain(4999)),                    # 顶点仙人掌（9999 点 + 孤立点）
            (10000, path_edges(10000)),                       # 深链树（迭代 Tarjan 压力）
            (10000, random_simple_graph(10000, 15000, rng)),
            (10000, path_edges(100, 0) + path_edges(100, 100) + path_edges(9800, 200)),  # 森林
            (9001, theta_edges(3000, 3000, 3002)),            # θ 图单块 m=n+1 -> 0 9002
        ]
        closed = [(0, 19997), (0, 0), (9999, 0), None, (99 + 99 + 9799, 0), (0, 9002)]
        return ("中等规模·定向：扇形单块、顶点仙人掌、深链树、随机、森林、长 θ 图（闭式核对）",
                g, closed)

    # ---------------- 点 7：大规模随机（n=10000，4 组） ----------------
    if i == 7:
        g = [
            (10000, random_simple_graph(10000, 20000, rng)),
            (10000, random_simple_graph(10000, 10000, rng)),
            (5000, random_simple_graph(5000, 10000, rng)),
            (10000, random_simple_graph(10000, 30000, rng)),
        ]
        return ("大规模随机：n=10000，m=1e4/2e4/3e4 共 4 组（稀疏档）", g, [None] * 4)

    # ---------------- 点 8：大规模随机（近顶格 m，4 组） ----------------
    if i == 8:
        g = [
            (10000, random_simple_graph(10000, M_MAX, rng)),
            (10000, random_simple_graph(10000, 50000, rng)),
            (10000, random_simple_graph(10000, M_MAX, rng)),
            (10000, random_simple_graph(10000, 99999, rng)),
        ]
        return ("大规模随机：n=10000，m 逼近上限 (1e5/5e4/1e5/99999) 共 4 组", g, [None] * 4)

    # ---------------- 点 9：顶格 · 最坏结构（6 组） ----------------
    if i == 9:
        # 共享长路径的双环：共享路径 0-1-...-4999（4999 边）；环 A 加 (4999,0)，
        # 环 B 走 4999-5000-...-7999-0（3001 边）-> n=8000, m=8001 单块
        shared = [(u, u + 1) for u in range(4999)]
        two_cycles = (shared + [(4999, 0)] + [(4999, 5000)] +
                      [(u, u + 1) for u in range(5000, 7999)] + [(7999, 0)])
        g = [
            (447, complete_graph(447)),                       # K447：m=99681 单块 -> 0 99681
            (10000, cycle_edges(10000)),                      # 大环 -> 0 0
            (6667, triangle_chain(3333)),                     # 3333 个三角长链 -> 0 0
            (8000, two_cycles),                               # 共享长路径双环 -> 0 8001
            (3001, diamond_chain(1000)),                      # 1000 菱形链 -> 0 5000
            (4400, sum((complete_graph(44, 44 * j) for j in range(100)), [])),  # 100 个 K44
        ]
        closed = [(0, 99681), (0, 0), (0, 0), (0, 8001), (0, 5000), (0, 94600)]
        return ("顶格·最坏结构：K447 单大块、大环、长链三角、共享长路径双环、菱形链、100×K44（闭式核对）",
                g, closed)

    # ---------------- 点 10：顶格 · 多组满规模（6 组） ----------------
    if i == 10:
        g = [
            (10000, random_simple_graph(10000, M_MAX, rng)),
            (10000, random_simple_graph(10000, M_MAX, rng)),
            (10000, random_simple_graph(10000, M_MAX, rng)),
            (447, complete_graph(447)),                       # 0 99681
            (10000, path_edges(10000)),                       # 9999 0
            (10000, fan_triangles(10000)),                    # 0 19997
        ]
        closed = [None, None, None, (0, 99681), (9999, 0), (0, 19997)]
        return ("顶格·多组满规模：3 组满随机 + K447 + 长链树 + 扇形（多组重置 + 吞吐压力）",
                g, closed)

    raise ValueError("未知测试点编号 %d" % i)


# ---------------------------------------------------------------------------
# 生成后自检
# ---------------------------------------------------------------------------

def parse_input(text):
    """解析 .in：返回 (groups, problems)。groups = [(n, m, edges)]；结尾必须恰为 0 0。"""
    problems = []
    toks = text.split()
    pos = 0
    groups = []
    terminator = False
    while pos < len(toks):
        if pos + 1 >= len(toks):
            problems.append("词数不足，无法读出 n m")
            break
        n, m = int(toks[pos]), int(toks[pos + 1])
        pos += 2
        if n == 0 and m == 0:
            terminator = True
            if pos != len(toks):
                problems.append("0 0 之后还有多余内容")
            break
        if not (1 <= n <= N_MAX):
            problems.append("n=%d 越界" % n)
        if not (1 <= m <= M_MAX):
            problems.append("m=%d 越界" % m)
        if pos + 2 * m > len(toks):
            problems.append("第 %d 组边数不足" % (len(groups) + 1))
            break
        edges = []
        for _ in range(m):
            u, v = int(toks[pos]), int(toks[pos + 1])
            pos += 2
            if not (0 <= u < n and 0 <= v < n):
                problems.append("边 (%d,%d) 端点越界（n=%d）" % (u, v, n))
            if u == v:
                problems.append("出现自环 (%d,%d)" % (u, v))
            if u > v:
                u, v = v, u
            edges.append((u, v))
        if len(set(edges)) != m:
            problems.append("第 %d 组出现重边" % (len(groups) + 1))
        groups.append((n, m, edges))
    if not terminator:
        problems.append("缺少结尾 0 0")
    return groups, problems


def parse_output(text, ngroups):
    """解析 .out：返回 (answers, problems)。"""
    problems = []
    if text == "":
        problems.append(".out 为空（cyaron 在 std 缺失时静默产 0 字节的坑）")
        return None, problems
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) != ngroups:
        problems.append(".out 行数 %d != 组数 %d" % (len(lines), ngroups))
        return None, problems
    answers = []
    for j, ln in enumerate(lines):
        parts = ln.split()
        if len(parts) != 2:
            problems.append(".out 第 %d 行不是 2 个整数：%r" % (j + 1, ln))
            continue
        answers.append((int(parts[0]), int(parts[1])))
    return answers, problems


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    # ⚠ cyaron 的坑：std 缺失时 output_gen 静默产出 0 字节 .out
    if not os.path.exists("../std"):
        print("错误：../std 不存在，请先编译（g++ -O2 -std=c++17 std.cpp -o std）", file=sys.stderr)
        raise SystemExit(2)

    plans = {}
    for i in range(1, 11):
        plans[i] = build_point(i)                       # (note, groups, closed)

    # 生成（写 .in + 运行 ../std 得 .out）
    for i in range(1, 11):
        note, groups, closed = plans[i]
        text = groups_to_text(groups)
        io = IO(file_prefix="problem", data_id=i)
        io.input_write(text, separator="")
        io.output_gen("../std")
        io.close()

    problems = []
    n_closed = 0
    print("点 | 组数 |  Σn |    Σm |          .in |        .out | 说明")
    print("---+------+-----+-------+-------------+-------------+------------------------------")
    for i in range(1, 11):
        note, groups, closed = plans[i]
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        got_groups, probs = parse_input(raw_in)
        for p in probs:
            problems.append("点 %d：%s" % (i, p))
        if len(got_groups) != len(groups):
            problems.append("点 %d：读回组数 %d != 构造组数 %d" % (i, len(got_groups), len(groups)))
        for j, (n, edges) in enumerate(groups):         # 与构造逐组核对 n、边集
            if j >= len(got_groups):
                break
            gn, gm, gedges = got_groups[j]
            if gn != n or gm != len(edges):
                problems.append("点 %d 第 %d 组：读回 n,m=%d,%d != %d,%d"
                                % (i, j + 1, gn, gm, n, len(edges)))
            elif sorted(gedges) != sorted((u, v) if u <= v else (v, u) for (u, v) in edges):
                problems.append("点 %d 第 %d 组：边集与构造不一致" % (i, j + 1))

        answers, probs = parse_output(raw_out, len(groups))
        for p in probs:
            problems.append("点 %d：%s" % (i, p))
        if answers is not None:
            for j, (n, edges) in enumerate(groups):
                a1, a2 = answers[j]
                if a1 < 0 or a2 < 0:
                    problems.append("点 %d 第 %d 组：负答案 %d %d" % (i, j + 1, a1, a2))
                if a1 + a2 > len(edges):
                    problems.append("点 %d 第 %d 组：ans1+ans2=%d > m=%d"
                                    % (i, j + 1, a1 + a2, len(edges)))
                exp = closed[j]
                if exp is not None:
                    n_closed += 1
                    if (a1, a2) != exp:
                        problems.append("点 %d 第 %d 组：闭式核对失败 %d %d != %d %d"
                                        % (i, j + 1, a1, a2, exp[0], exp[1]))

        # 点 2：.in/.out 与题面样例逐字节一致
        if i == 2:
            if raw_in != SAMPLE_TEXT:
                problems.append("点 2：.in 与题面样例不一致：%r" % raw_in)
            if raw_out != "%d %d\n" % SAMPLE_ANSWER:
                problems.append("点 2：.out 与题面样例不一致：%r" % raw_out)

        sn = sum(n for (n, _e) in groups)
        sm = sum(len(e) for (_n, e) in groups)
        print("%2d | %4d | %3d | %5d | %11d | %11d | %s"
              % (i, len(groups), sn, sm, len(raw_in.encode("utf-8")),
                 len(raw_out.encode("utf-8")), note))

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 点 .in/.out 成对；.in 结构/范围(1<=n<=1e4,1<=m<=1e5)/无重边无自环；")
    print("            .out 非空且行数 = 组数；ans1+ans2 <= m；闭式核对（共 %d 组）全部一致。" % n_closed)


if __name__ == "__main__":
    main()
