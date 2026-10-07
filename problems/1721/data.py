#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1721《最小边权和》分层数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py     （std 二进制位于 ../std）
#
# 题面数据范围（content.md【数据规模】）：
#   100%：n<=150, m<=5000, q<=1000, w<=5000，且每条边的 w 两两不同；
#   另有档位：30% 满足 n<=10, m<=100；另 30% 满足 q=1；80% 满足 m<=1000；90% 满足 m<=3000。
#   题面未给 w 的下界，按常规正权理解，取 w>=1（报告"未决问题"里注明）。
#
# 分层设计（10 组，从边界铺到顶格，每组写明规模与意图）：
#   点 1   边界层：题面【输入样例】原样（答案 17/6/-1，作为 std 正确性锚点）
#   点 2   边界层：最小规模 n=1, m=0, q=1（a==b, c=0 -> 0）
#   点 3   边界层：w 上下界（1 / 5000）、自环、平行边、不可达、c=0、a==b、c 超 n 截断
#   点 4   小规模（30% 档 n<=10, m<=100）：n=10, m=100, q=1000 随机
#   点 5   q=1 档（另 30% 档）：n=150, m=5000 顶格规模 + 单询问（链结构保证可达）
#   点 6   中等（80% 档 m<=1000）：n=60, m=1000, q=1000 随机
#   点 7   中大（90% 档 m<=3000）：n=120, m=3000, q=1000 随机
#   点 8   大规模：n=150, m=4200, q=1000 随机
#   点 9   顶格层：n=150, m=5000, q=1000；w 取 1..5000 的随机双射（全体权值铺满）
#   点 10  顶格构造层：链 1->2->...->150 权 4852..5000（最大答案 733974，卡 int/卡上界）
#          余下 4851 条为"反向小权边"（权 1..4851，只能把路走长不能走短），
#          并用 c=148/149/1000/1e9 等查询打 min(c,n) 截断边界
#
# 说明：题面保证 w 两两不同，本生成器的每张图内 w 均互不相同（区分平行边靠权值不同）。

import random

from cyaron import IO

MAXN = 150
MAXM = 5000
MAXQ = 1000
MAXW = 5000


def write(idx, text):
    """写 problem{idx}.in 并用 ../std 生成 problem{idx}.out。"""
    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(text)
    io.output_gen("../std")


def build(n, edges, queries):
    lines = ["%d %d %d" % (n, len(edges), len(queries))]
    lines += ["%d %d %d" % e for e in edges]
    lines += ["%d %d %d" % t for t in queries]
    return "\n".join(lines) + "\n"


def distinct_weights(rnd, m, lo=1, hi=MAXW):
    """m 个互不相同的边权，取自 [lo, hi]（题面要求 w 两两不同）。"""
    assert m <= hi - lo + 1, (m, lo, hi)
    return rnd.sample(range(lo, hi + 1), m)


def rand_edges(rnd, n, m, weights, self_loops=True):
    """随机有向图：m 条边（可含自环/平行边：平行边权值不同即可区分）。"""
    assert len(weights) == m
    edges = []
    for i in range(m):
        u = rnd.randint(1, n)
        v = rnd.randint(1, n)
        while not self_loops and v == u:
            v = rnd.randint(1, n)
        edges.append((u, v, weights[i]))
    rnd.shuffle(edges)
    return edges


def rand_queries(rnd, q, n, c_hi=None, long_c_ratio=0.0, same_ratio=0.1):
    """随机询问 (a,b,c)：c 取自 [0, c_hi]；long_c_ratio 比例给超大 c（测截断）。"""
    if c_hi is None:
        c_hi = n
    out = []
    for _ in range(q):
        a = rnd.randint(1, n)
        b = a if rnd.random() < same_ratio else rnd.randint(1, n)
        if rnd.random() < long_c_ratio:
            c = rnd.choice([1000, 10 ** 6, 10 ** 9])
        else:
            c = rnd.randint(0, c_hi)
        out.append((a, b, c))
    return out


# ---------------- 点 1：题面样例（边界层） ----------------
def gen1():
    text = """8 9 3
1 2 1
2 3 2
3 4 3
4 5 12
5 8 7
1 6 8
6 4 9
1 7 5
7 4 4
1 4 2
1 4 3
1 4 1
"""
    write(1, text)


# ---------------- 点 2：最小规模 n=1,m=0,q=1（边界层） ----------------
def gen2():
    text = "1 0 1\n1 1 0\n"
    write(2, text)


# ---------------- 点 3：极值/特殊情形组合（边界层） ----------------
def gen3():
    """n=3：w 最小 1、w 最大 5000、自环 3->3、平行边 1->3（2500/3000）。
    期望：1->3 最小 1 条边答案 2500；2 条边时 5001 更差故仍 2500；
    c=0 一律 -1；a==b 一律 0；2->1 / 3->1 无路 -1。
    """
    n = 3
    edges = [
        (1, 2, 1),        # w 下界
        (2, 3, 5000),     # w 上界
        (1, 3, 2500),     # 平行边（与下一条同 u,v）
        (1, 3, 3000),
        (3, 3, 4000),     # 自环
    ]
    queries = [
        (1, 3, 0), (1, 3, 1), (1, 3, 2), (1, 3, 3), (1, 3, 1000), (1, 3, 10 ** 9),
        (1, 2, 0), (1, 2, 1), (1, 2, 2),
        (2, 3, 0), (2, 3, 1), (2, 3, 2),
        (1, 1, 0), (1, 1, 5), (2, 2, 1000), (3, 3, 0), (3, 3, 4),
        (2, 1, 5), (3, 1, 5), (3, 2, 5),
    ]
    write(3, build(n, edges, queries))


# ---------------- 点 4：小规模（30% 档 n<=10, m<=100） ----------------
def gen4():
    rnd = random.Random(1721040)
    n, m, q = 10, 100, MAXQ
    edges = rand_edges(rnd, n, m, distinct_weights(rnd, m))
    queries = rand_queries(rnd, q, n, c_hi=n, long_c_ratio=0.05)
    write(4, build(n, edges, queries))


# ---------------- 点 5：q=1 档（顶格 n/m + 单询问） ----------------
def gen5():
    rnd = random.Random(1721050)
    n, m, q = MAXN, MAXM, 1
    perm = list(range(1, n + 1))
    rnd.shuffle(perm)
    ws = distinct_weights(rnd, m)
    # 随机标签下的链，保证 perm[0] -> perm[-1] 可达（q=1 单询问有解）
    edges = [(perm[i - 1], perm[i], ws[i - 1]) for i in range(1, n)]
    edges += [(rnd.randint(1, n), rnd.randint(1, n), ws[i]) for i in range(n - 1, m)]
    rnd.shuffle(edges)
    queries = [(perm[0], perm[-1], n)]
    write(5, build(n, edges, queries))


# ---------------- 点 6：中等（80% 档 m<=1000） ----------------
def gen6():
    rnd = random.Random(1721060)
    n, m, q = 60, 1000, MAXQ
    edges = rand_edges(rnd, n, m, distinct_weights(rnd, m))
    queries = rand_queries(rnd, q, n, c_hi=n, long_c_ratio=0.1)
    write(6, build(n, edges, queries))


# ---------------- 点 7：中大（90% 档 m<=3000） ----------------
def gen7():
    rnd = random.Random(1721070)
    n, m, q = 120, 3000, MAXQ
    edges = rand_edges(rnd, n, m, distinct_weights(rnd, m))
    queries = rand_queries(rnd, q, n, c_hi=n, long_c_ratio=0.1)
    write(7, build(n, edges, queries))


# ---------------- 点 8：大规模（n=150, m=4200） ----------------
def gen8():
    rnd = random.Random(1721080)
    n, m, q = MAXN, 4200, MAXQ
    edges = rand_edges(rnd, n, m, distinct_weights(rnd, m))
    queries = rand_queries(rnd, q, n, c_hi=n, long_c_ratio=0.1)
    write(8, build(n, edges, queries))


# ---------------- 点 9：顶格层（n/m/q 三顶格，w 铺满 1..5000） ----------------
def gen9():
    rnd = random.Random(1721090)
    n, m, q = MAXN, MAXM, MAXQ
    ws = distinct_weights(rnd, m)          # 1..5000 的随机双射
    edges = [(i, i + 1, ws[i - 1]) for i in range(1, n)]   # 前 149 条权值给链（保证 1->150 可达）
    edges += [(rnd.randint(1, n), rnd.randint(1, n), ws[i]) for i in range(n - 1, m)]
    rnd.shuffle(edges)
    queries = rand_queries(rnd, q, n, c_hi=n, long_c_ratio=0.15, same_ratio=0.15)
    # 钉死几条边界询问：a=1,b=150 长度上界 n-1=149，c 从 0 到超大
    queries[0] = (1, n, 0)
    queries[1] = (1, n, 148)
    queries[2] = (1, n, 149)
    queries[3] = (1, n, 10 ** 9)
    write(9, build(n, edges, queries))


# ---------------- 点 10：顶格构造层（最大答案 + 卡时 + 截断边界） ----------------
def gen10():
    """链 1->2->...->150，权依次 4852..5000（非降序，全长 149 条边）。
    路径权和 = sum(4852..5000) = 733974（接近理论上界 149*5000=745000，卡 int 实现）。
    其余 4851 条边全部取"反向小权"（u>v, 权 1..4851）：任何从点 1 出发的走路第一步
    必是 1->2(w=4852)，此后非降序只允许 >=4852 的链边，故 (1,150) 的最小答案就是
    733974（c>=149），c=148 时 -1 —— 答案可人工核对。
    """
    rnd = random.Random(1721100)
    n = MAXN
    edges = [(i, i + 1, 4851 + i) for i in range(1, n)]    # 149 条：4852..5000
    small = list(range(1, 4852))
    rnd.shuffle(small)
    k = 0
    while len(edges) < MAXM:
        u = rnd.randint(2, n)
        v = rnd.randint(1, u - 1)                          # 只造反向边
        edges.append((u, v, small[k]))
        k += 1
    rnd.shuffle(edges)
    queries = [
        (1, n, 148), (1, n, 149), (1, n, 150), (1, n, 1000), (1, n, 10 ** 9),
        (2, n, 147), (2, n, 148), (2, n, 1000),
        (1, n - 1, 1), (1, n - 1, n - 1), (1, n - 1, n),
        (1, 1, 0), (1, 1, n), (n, n, 3), (n, 1, 0), (n, 1, n),
    ]
    queries += rand_queries(rnd, MAXQ - len(queries), n, c_hi=n,
                            long_c_ratio=0.1, same_ratio=0.1)
    assert len(edges) == MAXM and len(queries) == MAXQ
    write(10, build(n, edges, queries))


if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
        print("%s done" % g.__name__)
