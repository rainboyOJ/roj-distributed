#!/usr/bin/env python
# 一本通 1688《最优路径》数据生成器
# 题面范围：多组数据；2<=n<=100000, 1<=m<=200000, 1<=a_i,b_i<=n, 1<=c_i<=1e9
# 10 个测试点分层（题面未给单点组数上限，主流量此类题惯例为 sum(m) 受限或 T 很小；
# 保守取 T<=10 且每组不顶格，仅点 10 用 T=10 大组；详见 gen-report.md 风险点）

from cyaron import *  # 引入 CYaRon 的库
from random import Random  # cyaron 未导出 Random 类，从标准库取

CMAX = 10 ** 9

def gen_connected(rnd, n, m, cmin=1, cmax=CMAX, dup_color_ratio=0.0, dup_color=1):
    """生成保证 1..n 连通的无向图（先铺随机生成树链再补随机边），返回边列表。"""
    perm = list(range(1, n + 1))
    rnd.shuffle(perm)  # 保证 1 在某个位置，链连接所有点 => 连通
    edges = []
    for i in range(n - 1):
        c = dup_color if rnd.random() < dup_color_ratio else rnd.randint(cmin, cmax)
        edges.append((perm[i], perm[i + 1], c))
    while len(edges) < m:
        if rnd.random() < 0.1 and edges:  # 少量重边
            a, b, _ = rnd.choice(edges)
            c = dup_color if rnd.random() < dup_color_ratio else rnd.randint(cmin, cmax)
            edges.append((a, b, c))
        else:
            a, b = rnd.randint(1, n), rnd.randint(1, n)
            c = dup_color if rnd.random() < dup_color_ratio else rnd.randint(cmin, cmax)
            edges.append((a, b, c))
    return edges

def write_case(io, n, m, edges):
    io.input_writeln([n, m])
    for a, b, c in edges:
        io.input_writeln([a, b, c])

def one_test(i, T, casegen, comment):
    """生成一个测试点：T 组数据，casegen(rnd) -> (n, m, edges)"""
    print("# test %d: %s" % (i, comment))
    io = IO(file_prefix="problem", data_id=i)
    rnd = Random(i * 19260817 + 998244353)
    io.input_writeln(T)
    for _ in range(T):
        n, m, edges = casegen(rnd)
        write_case(io, n, m, edges)
    io.output_gen("../std")

# ---------------- 分层生成 ----------------

# 点 1【边界层】n=2 最小点数 + m=1 最小边数 + 颜色顶格 1e9；答案 1 条边
one_test(1, 1, lambda rnd: (2, 1, [(1, 2, CMAX)]),
         "边界: n=2,m=1,c=1e9, 答案长度 1")

# 点 2【边界层】n=2 全部重边（题面允许重边），各种颜色含最小/最大，取最小色
one_test(2, 1, lambda rnd: (2, 5, [(1, 2, CMAX), (1, 2, 3), (1, 2, CMAX - 1), (1, 2, 1), (1, 2, 999999999)]),
         "边界: n=2 五条重边, 取最小颜色 1")

# 点 3【小规模随机】n,m 极小（n<=6, m<=10），可手算验证；含自环
def c3(rnd):
    n = rnd.randint(2, 6)
    m = rnd.randint(1, 10)
    edges = gen_connected(rnd, n, m)
    return n, m, edges
one_test(3, 3, c3, "小规模随机: T=3, n<=6, m<=10, 连通图(含重边/自环可能)")

# 点 4【小规模随机】同量级另一批随机，颜色集中于 {1,2} 制造大量同色并列路径（卡贪心）
def c4(rnd):
    n = rnd.randint(4, 8)
    m = rnd.randint(5, 14)
    edges = gen_connected(rnd, n, m, cmin=1, cmax=2)
    return n, m, edges
one_test(4, 3, c4, "小规模随机: 颜色仅 {1,2}, 大量并列最优路径")

# 点 5【中等规模随机】n~1000, m~2000
def c5(rnd):
    n = rnd.randint(800, 1200)
    m = min(200000, rnd.randint(1600, 2400))
    edges = gen_connected(rnd, n, m)
    return n, m, edges
one_test(5, 2, c5, "中等规模随机: n~1000, m~2000")

# 点 6【中等规模随机】n~20000, m~40000, 部分同色
def c6(rnd):
    n = rnd.randint(15000, 25000)
    m = min(200000, rnd.randint(30000, 50000))
    edges = gen_connected(rnd, n, m, dup_color_ratio=0.3)
    return n, m, edges
one_test(6, 2, c6, "中等规模随机: n~20000, m~40000, 30% 同色边")

# 点 7【大规模随机】n~60000, m~120000
def c7(rnd):
    n = rnd.randint(50000, 70000)
    m = rnd.randint(100000, 140000)
    edges = gen_connected(rnd, n, m)
    return n, m, edges
one_test(7, 1, c7, "大规模随机: n~60000, m~120000")

# 点 8【大规模随机】n 顶格 100000, m~180000, 高比例同色
def c8(rnd):
    n = 100000
    m = 180000
    edges = gen_connected(rnd, n, m, dup_color_ratio=0.5)
    return n, m, edges
one_test(8, 1, c8, "大规模随机: n=100000 顶格, m=180000, 50% 同色边")

# 点 9【顶格层】最坏结构：长链 n=100000（dist 顶格 n-1=99999），m=200000 顶格：
# 主链为 1-2-3-...-n（颜色随机），其余边为链上相邻点间的重边（不缩短 dist，
# 但邻接表变长，验证两遍 BFS + 逐层扫描的线性复杂度），混入少量自环。
def c9(rnd):
    n = 100000
    m = 200000
    edges = []
    for i in range(1, n):
        edges.append((i, i + 1, rnd.randint(1, CMAX)))
    while len(edges) < m:
        a = rnd.randint(1, n - 1)
        if rnd.random() < 0.05:
            edges.append((a, a, rnd.randint(1, CMAX)))  # 自环：std 应忽略
        else:
            edges.append((a, a + 1, rnd.randint(1, CMAX)))  # 相邻重边，不缩短 dist
    return n, m, edges
one_test(9, 1, c9, "顶格: n=1e5 长链 dist=99999, m=2e5 海量重边卡邻接表")

# 点 10【顶格层】T=10 组大随机（多组数据顶格），每组 n=100000, m=200000 全顶格
def c10(rnd):
    n = 100000
    m = 200000
    edges = gen_connected(rnd, n, m, dup_color_ratio=0.2)
    return n, m, edges
one_test(10, 10, c10, "顶格: T=10 组, 每组 n=1e5, m=2e5, 20% 同色")
