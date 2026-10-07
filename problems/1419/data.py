#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一本通 1419《SPFA(II)》数据生成器
#
# 题意：给定有向连通图，求 1 到 n 的最短路（单源最短路，终点固定为 n）。
# 数据范围（来源：https://blog.csdn.net/lybc2019/article/details/128441900）：
#     1 ≤ S,T ≤ N ≤ 20000,  M ≤ 40000,  -1e9 ≤ D ≤ 1e9
#     保证图中没有负环，且 1 可以到达 n。
#
# 分层设计（10 组）：
#   点 1-2  边界层：最小规模 n=2；样例含自环/负权；单条 -1e9 极小权边
#   点 3-4  小规模随机：可手算验证的量级（正向 DAG + 保证 1→n 链）
#   点 5-6  中等规模随机：n=2000 / 5000
#   点 7   链结构：n=20000 全链，边权 -1e9（测 long long 大负路径）
#   点 8   菊花结构：n=20000，1 指向所有其它点
#   点 9   顶格层：n=20000, m=40000 随机正向 DAG（含保证 1→n 链）
#   点 10  卡 SPFA 的 worst-case：HDU 4889 构造（DAG，指数级松弛）
#
# 说明：随机点均为「正向边」（u<v）构成 DAG，天然不含负环，且每点都附加
#       1→2→…→n 链保证 1 可达 n。所有边权均在 [-1e9, 1e9] 内。

from cyaron import IO  # 引入CYaRon的库
import random

random.seed(1419)  # 固定种子，便于复现

MAXN = 20000
MAXM = 40000
WMAX = 10 ** 9


def write_case(i, n, edges, note):
    """写出第 i 组：n 个点、len(edges) 条边（edges 为 (s,t,d) 列表）。"""
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(n, len(edges))
    for s, t, d in edges:
        io.input_writeln(s, t, d)
    io.output_gen("../std")
    print("problem%d: n=%d m=%d -- %s" % (i, n, len(edges), note))


def rand_w():
    return random.randint(-WMAX, WMAX)


def dag_edges(n, extra):
    """返回 (edges, )：先加 1→2→…→n 链保证可达，再加 extra 条正向随机边。

    所有边均满足 u < v，故整个图为 DAG，必然不含负环。
    """
    edges = [(u, u + 1, rand_w()) for u in range(1, n)]
    for _ in range(extra):
        u = random.randint(1, n - 1)
        v = random.randint(u + 1, n)
        edges.append((u, v, rand_w()))
    return edges


# ---- 点 1-2：边界层 ----
# 点 1：等价于题面样例（含自环 2->2 与重边），答案 -1
write_case(1, 2, [(1, 2, 1), (1, 2, -1), (2, 2, 0)],
           "边界层：题面样例（自环+重边+负权），答案 -1")

# 点 2：单条极小权边，答案 -1e9（负权下界）
write_case(2, 2, [(1, 2, -WMAX)],
           "边界层：单边 -1e9，答案 -1000000000（负权下界）")

# ---- 点 3-4：小规模随机（可手算验证） ----
# 点 3：n=5，链 + 5 条正向随机边，权 [-20,20]
random.seed(1419)
n = 5
edges = [(u, u + 1, random.randint(-20, 20)) for u in range(1, n)]
for _ in range(5):
    u = random.randint(1, n - 1)
    v = random.randint(u + 1, n)
    edges.append((u, v, random.randint(-20, 20)))
write_case(3, n, edges, "小规模随机：n=5，正向DAG，权[-20,20]，可手算")

# 点 4：n=10，链 + 15 条正向随机边，权 [-100,100]
n = 10
edges = [(u, u + 1, random.randint(-100, 100)) for u in range(1, n)]
for _ in range(15):
    u = random.randint(1, n - 1)
    v = random.randint(u + 1, n)
    edges.append((u, v, random.randint(-100, 100)))
write_case(4, n, edges, "小规模随机：n=10，正向DAG，权[-100,100]")

# ---- 点 5-6：中等规模随机 ----
# 点 5：n=2000，m≈4000（链 1999 + 随机 2001）
n = 2000
edges = dag_edges(n, 2001)
write_case(5, n, edges, "中等规模随机：n=2000，m≈4000，权[-1e9,1e9]")

# 点 6：n=5000，m≈10000（链 4999 + 随机 5001）
n = 5000
edges = dag_edges(n, 5001)
write_case(6, n, edges, "中等规模随机：n=5000，m≈10000，权[-1e9,1e9]")

# ---- 点 7：链结构 ----
# 点 7：n=20000 全链，每条边权 -1e9，答案 = -(n-1)*1e9 = -19999000000000
n = MAXN
edges = [(u, u + 1, -WMAX) for u in range(1, n)]
write_case(7, n, edges,
           "链结构：n=20000 全链，边权 -1e9，答案 -19999e9（测 long long）")

# ---- 点 8：菊花结构 ----
# 点 8：n=20000，1 指向所有其它点（有向菊花），答案 = 出边权最小值
n = MAXN
edges = [(1, v, rand_w()) for v in range(2, n + 1)]
write_case(8, n, edges, "菊花结构：n=20000，1 指向所有点，答案=出边权最小值")

# ---- 点 9：顶格层 ----
# 点 9：n=20000, m=40000 顶格随机（链 19999 + 随机 20001），保证可达、无负环
n = MAXN
edges = dag_edges(n, MAXM - (n - 1))
write_case(9, n, edges, "顶格层：n=20000,m=40000 随机正向DAG")

# ---- 点 10：卡 SPFA 的 worst-case（HDU 4889 构造） ----
# HDU 4889 的卡 SPFA 构造：T 层链 + 跳跃边，产生 2^T 量级松弛。
# 所有边均正向（DAG），无负环；T=22 时 n=45, m=66，松弛量约 2^22≈4.2e6，
# 对 SPFA 是显著压力但 std 仍可在 1s 内跑完。
T = 22
n = 2 * T + 1
edges = []
for k in range(T):
    edges.append((2 * k + 1, 2 * k + 2, 0))
    edges.append((2 * k + 2, 2 * k + 3, -(1 << (T - k))))
    edges.append((2 * k + 1, 2 * k + 3, -(1 << (T - k - 1))))
write_case(10, n, edges,
           "卡SPFA worst-case：HDU4889构造，n=%d,m=%d，指数级松弛" % (n, len(edges)))
