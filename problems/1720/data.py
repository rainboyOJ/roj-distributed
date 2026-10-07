#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一本通 1720《均值最小环》数据生成器（CYaRon）。

题面（见 ./content.md；网络同源题面与解法见 gen-report.md §一/§二）：
  输入：第 1 行 n m；第 2..m+1 行 u v w（有向边，1<=u,v<=n，0<=w<=1e7）。
  输出：无环 -> "PaPaFish is laying egg!"；否则 -> 最小平均权值，保留 2 位小数。
  数据范围：40% n<=50, m<=5000；100% 1<=n<=1000, 1<=m<=10000, 0<=w<=1e7。
  限制：time 1000ms / memory 128MB。

分层设计（10 组：边界 → 小 → 中 → 大 → 顶格；顶格顶到题面上限）：
  1  边界层 n=1,m=1 自环 w=3                -> 3.00（最小规模；自环即环）
  2  边界层 n=2,m=1 单边顶格权值             -> 无环分支 "PaPaFish is laying egg!"
  3  边界层 题面样例 n=2,m=2                 -> 2.50（样例回归，必须一致）
  4  边界层 0 权自环/0 权 2-环/重边/长重环    -> 0.00（答案下界；不依赖自环解释也成立）
  5  小规模 n=6,m=12 随机，w<=100          -> 暴力可枚举核验
  6  小规模稠密 n=50,m=5000（40% 档 m 顶格） -> 40% 档顶格
  7  中等规模 DAG n=200,m=3000（拓扑序 i<j） -> 无环分支 PaPaFish（中等规模下的判环路径）
  8  大规模顶格 n=1000,m=10000 随机          -> 卡二分 × SPFA 常数
  9  顶格层 n=1000,m=10000 全 1e7 权         -> 10000000.00（二分上界卡点）
 10  顶格层 n=1000,m=10000 0 权短环 vs 大权长环 -> 0.00（卡只看短环/自环的实现）

用法：在仓库任意目录执行 `python3 .ybt-import/staging/1720/data.py`
      （输出固定写到 data.py 同级目录的 data/ 下；std 二进制若不在 work/std，
        本脚本会先用 g++ -O2 -std=c++17 现场编译 std.cpp，编译产物可随后删除）
"""
import os
import random
import subprocess
import sys

from cyaron import Graph, IO, randint

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD_PATH = os.path.join(HERE, "work", "std")
STD_SRC = os.path.join(HERE, "std.cpp")


def ensure_std():
    """确保 work/std 存在：不在则由 std.cpp 现场编译（编译产物属于临时构建物）。"""
    if os.path.exists(STD_PATH):
        return
    if not os.path.exists(STD_SRC):
        sys.exit("std.cpp not found: %s" % STD_SRC)
    os.makedirs(os.path.dirname(STD_PATH), exist_ok=True)
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD_PATH, STD_SRC],
                   check=True)
    print("compiled std: %s -> %s" % (STD_SRC, STD_PATH))


ensure_std()

random.seed(1720)   # 固定随机种子，保证可复现

N_MAX = 1000
M_MAX = 10000
W_MAX = 10 ** 7


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------
def emit(case, n, edges, note):
    """写出 data/problem{case}.in，并用 std 生成同名 .out，返回答案字符串。"""
    os.makedirs(DATA_DIR, exist_ok=True)
    io = IO(os.path.join(DATA_DIR, "problem%d.in" % case),
            os.path.join(DATA_DIR, "problem%d.out" % case))
    io.input_writeln(n, len(edges))
    for (u, v, w) in edges:
        io.input_writeln(u, v, w)
    io.output_gen(STD_PATH)
    io.output_file.flush()   # output_gen 的结果可能还在缓冲区，读前先落盘
    with open(os.path.join(DATA_DIR, "problem%d.out" % case)) as f:
        ans = f.read().strip()
    print("problem%-2d: n=%-5d m=%-6d ans=%-25s -- %s"
          % (case, n, len(edges), ans, note))
    return ans


def has_cycle(n, edges):
    """三色标记 DFS 判有向图是否有环。"""
    adj = [[] for _ in range(n + 1)]
    for (u, v, w) in edges:
        adj[u].append(v)
    color = [0] * (n + 1)

    def dfs(s):
        stack = [(s, 0)]
        color[s] = 1
        while stack:
            u, i = stack.pop()
            if i < len(adj[u]):
                stack.append((u, i + 1))
                v = adj[u][i]
                if color[v] == 1:
                    return True
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, 0))
            else:
                color[u] = 2
        return False

    for s in range(1, n + 1):
        if color[s] == 0 and dfs(s):
            return True
    return False


def random_edges(n, m, wmax, ensure_cycle=True):
    """cyaron Graph.graph 生成 n 点 m 边随机有向图（允许自环/重边/0 权）。

    ensure_cycle=True 时若随机图恰好无环，则把一个顶点的出边改成自环（保持 m 不变），
    保证该组数据走"有环"分支（否则 1000 点 10000 边的随机图仍可能是 DAG）。
    """
    g = Graph.graph(n, m, directed=True, self_loop=True, repeated_edges=True,
                    weight_limit=(0, wmax))
    edges = [(e.start, e.end, e.weight) for e in g.iterate_edges()]
    if ensure_cycle and not has_cycle(n, edges):
        i = randint(0, len(edges) - 1)
        u = edges[i][0]
        edges[i] = (u, u, edges[i][2])
    return edges


# --------------------------------------------------------------------------
# 数据分层
# --------------------------------------------------------------------------
# ---- 点 1：边界层，最小规模 n=1（自环） ----
emit(1, 1, [(1, 1, 3)], "边界层：n=1,m=1 自环 w=3 → 3.00（最小规模，自环即环）")

# ---- 点 2：边界层，无环分支（n=2,m=1 顶格权值） ----
emit(2, 2, [(1, 2, W_MAX)], "边界层：n=2,m=1 单边（顶格权值）→ 无环分支 PaPaFish")

# ---- 点 3：边界层，题面样例 ----
emit(3, 2, [(1, 2, 2), (2, 1, 3)], "边界层：题面样例 → 2.50")

# ---- 点 4：边界层，答案下界 0.00（0 权环；不依赖自环解释也成立） ----
emit(4, 4,
     [(1, 2, 0), (2, 1, 0),                         # 0 权 2-环 → 答案 0.00
      (3, 3, 0), (3, 3, 0),                         # 0 权自环 + 重边（自环边界）
      (1, 3, W_MAX), (3, 4, W_MAX), (4, 1, W_MAX)], # 大权长环竞争（卡只看短环的实现）
     "边界层：0 权 2-环/0 权自环/重边/长重环 → 0.00")

# ---- 点 5：小规模随机，权值小（可暴力枚举全部简单环，人也可手算核验） ----
emit(5, 6, random_edges(6, 12, 100), "小规模随机：n=6,m=12,w<=100（可暴力枚举核验）")

# ---- 点 6：小规模稠密，40% 档 m 顶格 ----
emit(6, 50, random_edges(50, 5000, W_MAX), "小规模稠密：n=50,m=5000（40% 档 m 顶格）")

# ---- 点 7：中等规模 DAG（只能 i<j 连边，必无环）→ 走无环分支 ----
e7 = []
for _ in range(3000):
    u = randint(1, 199)
    v = randint(u + 1, 200)          # 保证 u < v → 不可能有环
    e7.append((u, v, randint(0, W_MAX)))
emit(7, 200, e7, "中等规模 DAG：n=200,m=3000 拓扑序连边 → 无环分支 PaPaFish")

# ---- 点 8：大规模顶格随机（卡二分 × SPFA） ----
emit(8, N_MAX, random_edges(N_MAX, M_MAX, W_MAX),
     "大规模顶格随机：n=1000,m=10000（卡二分×SPFA 常数）")

# ---- 点 9：顶格层，全部边权 1e7（二分上界卡点） ----
e9 = [(i, i + 1, W_MAX) for i in range(1, N_MAX)] + [(N_MAX, 1, W_MAX)]
e9 += [(randint(1, N_MAX), randint(1, N_MAX), W_MAX) for _ in range(M_MAX - len(e9))]
random.shuffle(e9)
emit(9, N_MAX, e9[:M_MAX], "顶格层：n=1000,m=10000 全 1e7 权 → 10000000.00（二分上界）")

# ---- 点 10：顶格层，0 权短环 vs 大权长环竞争（卡只看短环/自环的实现） ----
e10 = [(1, 2, 0), (2, 1, 0)]                             # 0 权 2-环 → 答案 0.00
e10 += [(i, i + 1, W_MAX) for i in range(2, N_MAX)]      # 大权长环（长度与短环不同）
e10 += [(N_MAX, 3, W_MAX)]
e10 += [(randint(1, N_MAX), randint(1, N_MAX), randint(0, W_MAX))
        for _ in range(M_MAX - len(e10))]
random.shuffle(e10)
emit(10, N_MAX, e10[:M_MAX],
     "顶格层：0 权 2-环 + 大权长环竞争 → 0.00（卡只看短环/自环的实现）")

print("\n10 cases written to %s" % DATA_DIR)
