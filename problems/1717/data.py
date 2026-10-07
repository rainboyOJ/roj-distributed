#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1717《负环》分层测试数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 -o std std.cpp && mkdir -p data && cd data && python3 ../data.py
#
# 题意：给 n 个点 m 条边、无重边无自环的带权有向图，求点数最少的负环所含点数，无负环输出 0。
# 题面数据范围（config.json / content.md）：
#   2 <= n <= 300；0 <= m <= n*(n-1)；|w_i| <= 10^4；time 2000 ms / memory 256 MB。
#   20% 数据：n<=7, m<=10；60% 数据：n<=150, m<=2000。
#
# ---- 分层策略（10 组，单图单测）----
#   点 1  边界层：n=2, m=0 —— 最小规模 + 无负环（答案 0 的退化下界）。
#   点 2  边界层：n=2, m=2 —— 最小答案（2 点负环，答案 2）。
#   点 3  样例层：题面样例（n=4, m=8）—— 答案 4，标程已核对。
#   点 4  样例层：同型经典题 BZOJ 4773 样例（n=3, m=6）—— 答案 2，标程已核对。
#   点 5  小规模层（20% 数据上限）：n=7, m=10 —— 植入 3 点负环 + 随机补边，答案 3 量级。
#   点 6  中规模随机层：n=150, m=2000（60% 数据上限）—— 随机权值，负环极短（2~3）。
#   点 7  中规模顶格长环层：n=150, m=2000 —— 140 边负环（-1/边）+ 1860 条正权弦（>=150），
#         任何含正权弦的简单环权 >= -140+150 > 0，答案精确为 140（跨 2^7 位边界）。
#   点 8  顶格 n 稀疏长环层：n=300, m=300 —— 唯一 300 点负环（-1e4/边），答案精确为 300（答案上限）。
#   点 9  顶格密度无负环层：n=300, m=300*299=89700 全正权 —— 答案 0（最坏规模 + 无解分支）。
#   点 10 顶格密度跨界层：n=300, m=89700 —— 257 边负环（-1/边），其余边全为 +257；
#         简单环含 r>=1 条正权弦时权 >= 257r-257 >= 0，r=0 时只能是整环 -257 < 0，
#         答案精确为 257（恰好越过 2^8=256，压满倍增位数边界）。
#
# 全部数据固定随机种子，可复现；严格满足 0<=m<=n(n-1)、无重边、无自环、|w|<=1e4。

import random
from cyaron import IO

random.seed(1717)

MAXW = 10 ** 4


def write_case(data_id, n, edges):
    """edges: list of (u, v, w)，1-based 点编号。"""
    lines = [f"{n} {len(edges)}"]
    lines += [f"{u} {v} {w}" for (u, v, w) in edges]
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("\n".join(lines) + "\n")
    io.output_gen("../std")


def rand_distinct_edges(n, m, forbidden=(), wlo=1, whi=MAXW):
    """无自环、无重边；forbidden 为不可再用的边，接受 (u,v) 或 (u,v,w) 形式。"""
    forbidden = set((e[0], e[1]) for e in forbidden)
    edges = []
    used = set(forbidden)
    guard = 0
    while len(edges) < m:
        guard += 1
        if guard > 200 * max(m, 1) + 1000:
            raise RuntimeError("edge sampling failed")
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u == v or (u, v) in used:
            continue
        used.add((u, v))
        edges.append((u, v, random.randint(wlo, whi)))
    return edges


# 1. 边界最小：n=2, m=0 -> 0
write_case(1, 2, [])

# 2. 边界最小负环：n=2, m=2, 双向各 -1 -> 2
write_case(2, 2, [(1, 2, -1), (2, 1, -1)])

# 3. 题面样例 -> 4
write_case(3, 4, [
    (1, 2, 10), (2, 1, -3), (1, 3, -1), (3, 1, 10),
    (2, 4, 10), (4, 2, 1), (3, 4, 0), (4, 3, 3),
])

# 4. 同型经典题 BZOJ 4773 样例 -> 2
write_case(4, 3, [
    (1, 2, -2), (2, 1, 1), (2, 3, -10),
    (3, 2, 10), (3, 1, -10), (1, 3, 10),
])

# 5. 20% 数据上限：n=7, m=10，植入 3 点负环（1->3->5->1）后随机补边
plant5 = [(1, 3, -5), (3, 5, -5), (5, 1, -5)]
rest5 = rand_distinct_edges(7, 10 - len(plant5), forbidden=plant5, wlo=-10, whi=10)
assert len(set((u, v) for u, v, w in plant5 + rest5)) == 10  # 无重边自检
write_case(5, 7, plant5 + rest5)

# 6. 60% 数据上限随机：n=150, m=2000（权值混合，负环极短）
write_case(6, 150, rand_distinct_edges(150, 2000, wlo=-1000, whi=1000))

# 7. 60% 上限 + 长负环：n=150, m=2000，140 边负环 + 1860 条正权弦
L7 = 140
cycle7 = [(i, i % L7 + 1, -1) for i in range(1, L7 + 1)]
chords7 = rand_distinct_edges(150, 2000 - L7, forbidden=cycle7, wlo=150, whi=MAXW)
write_case(7, 150, cycle7 + chords7)
assert len(set((u, v) for u, v, w in cycle7 + chords7)) == 2000  # 无重边自检

# 8. 顶格 n 稀疏长环：n=300, m=300，唯一 300 点负环 -> 300
write_case(8, 300, [(i, i % 300 + 1, -MAXW) for i in range(1, 301)])

# 9. 顶格密度无负环：n=300，全正权完全有向图（89700 条边）-> 0
edges9 = [(u, v, random.randint(1, MAXW))
          for u in range(1, 301) for v in range(1, 301) if u != v]
write_case(9, 300, edges9)

# 10. 顶格密度跨界：n=300 完全有向图，257 边负环（-1/边），其余边 +257 -> 257
L10 = 257
neg10 = set((i, i % L10 + 1) for i in range(1, L10 + 1))
edges10 = []
for u in range(1, 301):
    for v in range(1, 301):
        if u == v:
            continue
        edges10.append((u, v, -1 if (u, v) in neg10 else 257))
write_case(10, 300, edges10)
