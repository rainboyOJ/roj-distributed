#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1718《益智游戏》分层测试数据生成器（cyaron）
#
# 题意：正权有向图。小P 走 A→B 的最短路，小R 走 C→D 的最短路，每回合可移动或休息；
#       两人同时同点得一次奖励且每点最多一次。求最大奖励数；不可达输出 -1。
# 模型（见 std.cpp 头注）：4 次 Dijkstra 求 dA/dB/dC/dD，取「同时在两条最短路上」的
#       节点与边，答案为该公共最短路 DAG 上的最长节点链。
#
# 数据范围（题面【数据规模及约定】）：
#   30%: n<=50；60%: n<=1000, m<=5000；100%: n<=50000, m<=200000, 1<=l_i<=5*10^8。
#   答案上界 n=50000；距离和可达 49999*5*10^8 ≈ 2.5*10^13，标程必须 64 位。
#
# 分层设计（10 组，全部不超过题面上限）：
#   1  题面样例原样（n=5,m=5）-> 期望 2
#   2  边界：n=2 最小规模，单边权 5*10^8（权值顶格），且 C 到不了 D
#      （R 方向不可达分支）-> 期望 -1
#   3  边界：A==B（P 原地不动）链 1..8，C=1,D=8 -> 期望 1
#   4  边界：A 到不了 B -> 期望 -1
#   5  边界：两条互不相交的链（外加 5*10^8 重边填充），公共点为空 -> 期望 0
#   6  30% 档「双通道等长最短路」：脊线 n=49（25 脊点，段权 2）+ 24 个绕行点
#      （两段各权 1，与直连等长），故存在大量等长最短路，两人同绕同一绕行点也能相遇
#      -> 期望 49 = n（考察「同一先后顺序即可对齐」这一结论），m=120 大权填充
#   7  60% 档同构放大：k=500 脊点，n=999、m=5000 -> 期望 999
#   8  60% 档且答案大：链权 1 + 重边(5*10^8)填充；A=1,B=1000,C=1,D=500 -> 期望 500
#   9  顶格「等长双通道」：脊线 k=25000 段权 2 + 25000 个绕行点（两段各权 1，等长），
#      n=49999、m=200000（含 12.5 万条大权填充边，权值 >=1e5 不干扰最短路）
#      A=B 取最后脊点 25000 -> 期望 n=49999（答案顶到节点数上界，
#      大量等长最短路共享全部节点，四人重合/重复计数风险最大）
#  10  顶格 + 64 位：链 1..50000 边权全 5*10^8 + 随机回边；A=1,B=50000,C=1,D=50000
#      -> 期望 50000（n 同时是 node 数上界与答案上界）
#      同时 dA[B]=49999*5*10^8≈2.5*10^13 触发 64 位，回边使 4 次 Dijkstra 有大量松弛
#
# 生成方式：cyaron IO(file_prefix="problem", data_id=i) + io.output_gen("../std")。
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py

import random
from cyaron import IO

random.seed(20251006)

MAXN = 50000
MAXM = 200000
MAXW = 500000000  # 5*10^8


def emit(data_id, n, edges, A, B, C, D):
    """把 n/m 与 m 条边、四个起终点写成 problem{data_id}.in，并用 std 生成 .out"""
    io = IO(file_prefix="problem", data_id=data_id)
    out = ["%d %d" % (n, len(edges))]
    for x, y, w in edges:
        out.append("%d %d %d" % (x, y, w))
    out.append("%d %d %d %d" % (A, B, C, D))
    io.input_write("\n".join(out) + "\n")
    io.output_gen("../std")
    return len(edges)


def cycle_edges(n):
    return [(i, i % n + 1) for i in range(1, n + 1)]


def detour_graph(k, w_spine, w_side):
    """脊线 + 绕行结构：节点 1..k 为脊点，相邻脊点 j->j+1 权 w_spine；
    绕行点 k+j 提供 j -> k+j -> j+1 两段各权 w_side 的等长替代路。
    n = 2k-1（节点 1..2k-1 全部用上）。当 2*w_side == w_spine 时两条走法严格等长，
    于是「两人同走同一个绕行点」也构成合法相遇，答案为全部 2k-1 个节点。"""
    edges = []
    n = 2 * k - 1
    for j in range(1, k):
        edges.append((j, j + 1, w_spine))
        d = k + j
        edges.append((j, d, w_side))
        edges.append((d, j + 1, w_side))
    return n, edges


def add_random_edges(edges, used, cnt, n, wmin=1, wmax=MAXW, forward=None):
    """补 cnt 条不重复随机边；(x,y) 已存在则重抽。
    forward=True 只取 x<y，forward=False 只取 x>y，None 则不限制（仍排除自环）。"""
    added = 0
    tries = 0
    while added < cnt and tries < cnt * 20:
        tries += 1
        if forward is True:
            x = random.randint(1, n - 1)
            y = random.randint(x + 1, n)
        elif forward is False:
            x = random.randint(2, n)
            y = random.randint(1, x - 1)
        else:
            x = random.randint(1, n)
            y = random.randint(1, n)
            if x == y:
                continue
        if (x, y) in used:
            continue
        used.add((x, y))
        edges.append((x, y, random.randint(wmin, wmax)))
        added += 1
    return added


def main():
    # ---- 1. 题面样例原样 ----
    sample = [(1, 2, 1), (2, 3, 2), (3, 4, 4), (5, 2, 3), (5, 3, 5)]
    emit(1, 5, sample, 1, 3, 5, 4)  # 期望 2

    # ---- 2. 边界：n=2，权值顶格 5*10^8，C 到不了 D ----
    emit(2, 2, [(1, 2, MAXW)], 1, 2, 2, 1)  # 期望 -1（R 不可达）

    # ---- 3. 边界：A==B（P 原地不动） ----
    e3 = [(i, i + 1, random.randint(1, 10)) for i in range(1, 8)]
    emit(3, 8, e3, 1, 1, 1, 8)  # 期望 1（只有节点 1 两人都会经过）

    # ---- 4. 边界：A 到不了 B ----
    e4 = [(1, 2, 3), (2, 3, 4), (4, 5, 5), (5, 3, 6)]
    emit(4, 5, e4, 1, 5, 4, 3)  # 期望 -1

    # ---- 5. 边界：两条互不相交的链，公共点为空 ----
    n5 = 50
    e5 = [(i, i + 1, random.randint(1, 5)) for i in range(1, 25)]
    e5 += [(i, i + 1, random.randint(1, 5)) for i in range(26, 50)]
    used5 = set((x, y) for x, y, _ in e5)
    add_random_edges(e5, used5, 60, n5, wmin=MAXW, wmax=MAXW)  # 重边填充，无法形成捷径
    emit(5, n5, e5, 1, 25, 26, 50)  # 期望 0

    # ---- 6. 30% 档：脊线 k=25，n=49，等长绕行 + 大权填充 -> 期望 49 ----
    n6, e6 = detour_graph(25, 2, 1)
    used6 = set((x, y) for x, y, _ in e6)
    add_random_edges(e6, used6, 120 - len(e6), n6, wmin=MAXW, wmax=MAXW)
    random.shuffle(e6)
    emit(6, n6, e6, 1, 25, 1, 25)  # 期望 49（A=B 的脊线两端）

    # ---- 7. 60% 档：同构放大到 k=500，n=999、m=5000 -> 期望 999 ----
    n7, e7 = detour_graph(500, 2, 1)
    used7 = set((x, y) for x, y, _ in e7)
    add_random_edges(e7, used7, 5000 - len(e7), n7, wmin=MAXW, wmax=MAXW)
    random.shuffle(e7)
    emit(7, n7, e7, 1, 500, 1, 500)  # 期望 999

    # ---- 8. 60% 档且答案大：链权 1 + 重边 5*10^8 填充 ----
    n8 = 1000
    e8 = [(i, i + 1, 1) for i in range(1, n8)]
    used8 = set((x, y) for x, y, _ in e8)
    add_random_edges(e8, used8, 5000 - (n8 - 1), n8, wmin=MAXW, wmax=MAXW)
    random.shuffle(e8)
    emit(8, n8, e8, 1, n8, 1, 500)  # 期望 500（公共前缀 1..500）

    # ---- 9. 顶格等长双通道：k=25000，n=49999、m=200000 -> 期望 49999 ----
    n9, e9 = detour_graph(25000, 2, 1)
    used9 = set((x, y) for x, y, _ in e9)
    add_random_edges(e9, used9, MAXM - len(e9), n9, wmin=100000, wmax=MAXW)
    random.shuffle(e9)
    emit(9, n9, e9, 1, 25000, 1, 25000)  # 期望 49999 = n（端点为最后脊点）

    # ---- 10. 顶格 + 64 位：链权 5*10^8 + 回边 ----
    n10 = MAXN
    e10 = [(i, i + 1, MAXW) for i in range(1, n10)]
    used10 = set((x, y) for x, y, _ in e10)
    add_random_edges(e10, used10, MAXM - (n10 - 1), n10, forward=False)
    random.shuffle(e10)
    emit(10, n10, e10, 1, n10, 1, n10)  # 期望 50000，dA[B]=49999*5*10^8

    print("all 10 cases generated")


if __name__ == "__main__":
    main()
