#!/usr/bin/env python3
# 一本通 1734《删边问题》数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 std.cpp -o std
#       mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（100%）：1<=n<=1e5，1<=m<=1e6，1<=Q<=8e5，0<=u,v<n，0<=x<m；
#   允许重边与自环；点、边均从 0 编号；输出答案 = 删边后互不可达的无序点对数 mod 1000。
# 本题规模由「n + m + Q + 输出行数」决定，故生成器对每个测试点显式校验这三项上限，
#   并在生成后断言 .in 行数与 .out 行数符合预期（防 cyaron output_gen 静默产出 0 字节 .out）。
#
# 分层设计（10 组，从小到顶格；每组注明规模与设计意图）：
#   点 1    边界层：n=m=Q=1 单点自环（全最小值，答案 0）
#   点 2    边界层：n=2 全森林（两点无边、仅自环），答案 1 的极端
#   点 3    小规模：可手算验证的多分量 + 重边 + 自环混合结构
#   点 4    小规模：n=20 生成树 + 额外边 + 副本 + 自环（结构闭式可推）
#   点 5-6  中等规模：n=1000/3000，稀疏随机图 + 树边构造（桥/非桥混合）
#   点 7-8  大规模：n=1e5 顶格；点 8 为链构造（全桥，答案 = C(n,2) 量级）
#   点 9-10 顶格层：n=m=1e5/1e6 与 Q=8e5 同时顶格；点 9 悬挂链构造（确定答案）、
#            点 10 卡常结构（链 + 海量平行边 + 自环，卡递归爆栈与按父顶点跳边的错解）
import os
import random
import sys

from cyaron import IO, randint

NMAX = 100000          # 题面上限 n
MMAX = 1000000         # 题面上限 m
QMAX = 800000          # 题面上限 Q
OUT_ROOT = ".."        # std 位于 data.py 的上一级目录
STD = os.path.join(OUT_ROOT, "std")


def require_std():
    """先校验 std 存在，避免 cyaron 在 std 缺失时静默产出 0 字节 .out。"""
    if not os.path.isfile(STD) or not os.access(STD, os.X_OK):
        sys.exit("[FATAL] std not found or not executable: %s "
                 "(run: g++ -O2 -std=c++17 std.cpp -o std)" % STD)


def check_in_file(io, data_id, n, m, Q, edges):
    """生成后校验 .in：规模合法 + 行数符合预期 + 边编号可解引用。"""
    assert 1 <= n <= NMAX, "n out of range: %d" % n
    assert 1 <= m <= MMAX, "m out of range: %d" % m
    assert 1 <= Q <= QMAX, "Q out of range: %d" % Q
    assert len(edges) == m, "edge count mismatch: %d != %d" % (len(edges), m)
    for (u, v) in edges:
        assert 0 <= u < n and 0 <= v < n, "endpoint out of range: %d %d" % (u, v)
    io.flush_buffer()  # cyaron 写文件带缓冲，读之前先落地
    path = io.input_filename
    with open(path, "r") as f:
        lines = f.read().split("\n")
    assert len(lines) >= m + Q + 1, "too few lines in %s: %d" % (path, len(lines))
    head = lines[0].split()
    assert list(map(int, head)) == [n, m, Q], "bad header %s in %s" % (head, path)
    xs = [int(lines[m + 1 + i]) for i in range(Q)]
    for x in xs:
        assert 0 <= x < m, "query out of range: %d" % x
    return xs


def check_out_file(io, data_id, Q):
    """生成后断言 .out 非空且行数正确，防止 std 静默失败留下空文件。"""
    io.output_file.flush()  # cyaron 输出文件带缓冲，读之前先落地
    path = io.output_filename
    assert os.path.getsize(path) > 0, "empty .out: %s" % path
    vals = open(path).read().split()
    assert len(vals) == Q, ".out line count %d != Q %d in %s" % (len(vals), Q, path)
    for v in vals:
        iv = int(v)
        assert 0 <= iv < 1000, "answer not in [0,1000): %s" % v


def emit(data_id, n, edges, queries):
    """构造输入并调用 std 生成输出，随后做双向校验。"""
    m, Q = len(edges), len(queries)
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("%d %d %d\n" % (n, m, Q))
    io.input_write("".join("%d %d\n" % (u, v) for (u, v) in edges))
    io.input_write("".join("%d\n" % x for x in queries))
    check_in_file(io, data_id, n, m, Q, edges)
    io.output_gen(STD)
    check_out_file(io, data_id, Q)
    print("problem%d: n=%d m=%d Q=%d OK" % (data_id, n, m, Q))


# ---------------------------------------------------------------- 点 1 边界层
# n=1（下限）、m=1（下限，单点自环 0 0）、Q=1（下限）：删自环不改变连通性，
# 无孤立点，答案 0。边界层「全最小值 + 自环」组合。
def gen1():
    edges = [(0, 0)]
    queries = [0]
    emit(1, 1, edges, queries)


# ---------------------------------------------------------------- 点 2 边界层
# n=2 下限、两点之间无边（m=1 为自环）→ 图完全不连通：T0=1（点对 (0,1)）；
# 删自环后仍是 1，答案 1。覆盖「完全不可达」的分量与自环边界。
def gen2():
    edges = [(1, 1)]
    queries = [0]
    emit(2, 2, edges, queries)


# ---------------------------------------------------------------- 点 3 小规模
# n=10, m=12, Q=12：可手算验证的规模，覆盖多分量 + 重边 + 自环混合物。
#   分量 {0,1,2,3}：平行边 (0,1)x2（非桥）+ 桥 1-2（子树 {2,3}，s=2）+ 桥 2-3（s=1）；
#   分量 {4,5,6}：三角形（无桥）+ 自环 (5,5)；
#   分量 {7}：孤立点 + 自环 (7,7)；
#   分量 {8,9}：平行边 (8,9)x2（非桥）+ 自环 (9,9)。
#   T0 = C(10,2) - C(4,2) - C(3,2) - 0 - C(2,2) = 45-6-3-1 = 35；
#   故期望答案：边 2 → 35+2*2=39，边 3 → 35+1*3=38，其余 → 35。
def gen3():
    edges = [
        (0, 1), (0, 1),              # 平行边：都不算桥
        (1, 2), (2, 3),              # 桥：s=2 / s=1（分量大小 4）
        (4, 5), (5, 6), (6, 4),      # 三角形：3 条均非桥
        (5, 5),                      # 自环
        (7, 7),                      # 孤立点的自环
        (8, 9), (8, 9),              # 平行边：均非桥
        (9, 9),                      # 自环
    ]
    queries = list(range(len(edges)))
    emit(3, 10, edges, queries)


# ---------------------------------------------------------------- 点 4 小规模
# n=20：随机生成树（19 条）+ 3 条随机额外边 + 1 条自环 + 1 条树边副本 = 24 条边，Q=24。
# 小规模、结构完全可闭式推导：桥 = 未被任何额外边/副本覆盖的树边（答案 = s*(20-s) mod 1000），
# 其余边（额外边/自环/副本）删去不改变连通性（答案 0）；同时覆盖 T0=0 时的全部分支。
def gen4():
    random.seed(173404)
    n = 20
    tree = [(i, randint(0, i - 1)) for i in range(1, n)]   # 随机生成树，19 条
    extras = [(randint(0, n - 1), randint(0, n - 1)) for _ in range(3)]
    dup = tree[randint(0, len(tree) - 1)]                 # 树边的副本（平行边，非桥）
    edges = tree + extras + [(0, 0), dup]                 # + 自环
    queries = list(range(len(edges)))
    random.shuffle(queries)
    emit(4, n, edges, queries)


# ---------------------------------------------------------------- 点 5 中等规模随机
# n=1000, m=1300：深随机树（父节点取 i 往前 1..5 层内随机，子树大小分布宽）
# + 约 300 条随机额外边（稀疏，大量树边仍为桥，子树大小 s 覆盖多种取值）。
# 树边中未被额外边覆盖的仍是桥，因此「桥 / 非桥」两类询问大量混合出现，
# 且子树大小 s 覆盖较大范围（答案不再集中于 0/999），中档规模下覆盖完整分支。
def gen5():
    random.seed(173405)
    n, m = 1000, 1300
    edges = [(i, randint(max(0, i - 5), i - 1)) for i in range(1, n)]   # 深随机树
    while len(edges) < m:
        edges.append((randint(0, n - 1), randint(0, n - 1)))
    queries = list(range(m))
    random.shuffle(queries)
    emit(5, n, edges, queries)


# ---------------------------------------------------------------- 点 6 中等规模随机
# n=3000, m=4000, Q=100000：深随机树（父取 i 往前 1..8 层内随机，子树大小分布宽）
# + 约 1000 条随机额外边（大量树边仍为桥）。
# 询问数远大于边数（重复询问同一条边），答案 = s*(3000-s) mod 1000 按 s 取值丰富，
# 可验证「子树大小 s 与 s*(C-s)」在 n=3000 连通块上的各种取值。
def gen6():
    random.seed(173406)
    n, m, Q = 3000, 4000, 100000
    edges = [(i, randint(max(0, i - 8), i - 1)) for i in range(1, n)]   # 深随机树
    while len(edges) < m:
        edges.append((randint(0, n - 1), randint(0, n - 1)))
    queries = [randint(0, m - 1) for _ in range(Q)]
    emit(6, n, edges, queries)


# ---------------------------------------------------------------- 点 7 大规模随机
# n=100000（顶格）, m=100000, Q=800000（顶格）：n 顶格 + Q 顶格，
# 深随机树（父取 i-randint(1,16)，桥多且子树大小分布宽）+ 1 条随机边；
# 询问覆盖每条边并额外随机重复询问。
def gen7():
    random.seed(173407)
    n, m, Q = 100000, 100000, 800000
    edges = []
    for i in range(1, n):
        edges.append((randint(max(0, i - 16), i - 1), i))   # 深随机树（根 0 方向）
    # 再补 m-(n-1) 条随机边（n-1=99999，剩 1 条）
    while len(edges) < m:
        edges.append((randint(0, n - 1), randint(0, n - 1)))
    queries = list(range(m)) + [randint(0, m - 1) for _ in range(Q - m)]
    random.shuffle(queries)
    emit(7, n, edges, queries)


# ---------------------------------------------------------------- 点 8 大规模
# n=100000（顶格）, m=99999 —— 恰为一棵**链**（0-1-2-...-n-1），Q=300000。
# 链上每条边都是桥，答案 = s*(n-s) 的确定值（最大近 n^2/4 = 2.5e9，模 1000 后分布散），
# 专门检验「子树大小 s 与 s*(C-s)」在最大连通块上的正确性。
def gen8():
    n, m, Q = 100000, 99999, 300000
    edges = [(i - 1, i) for i in range(1, n)]
    queries = [(i * 7) % m for i in range(Q)]   # 覆盖不同位置（含近两端）
    emit(8, n, edges, queries)


# ---------------------------------------------------------------- 点 9 顶格层
# n=100000（顶格）, m=1000000（顶格）, Q=800000（顶格）。
# 结构：90000 点稠密核（990000 条随机边，几乎必然无桥）+ 1000 条
#   长度 10 的悬挂链，每条用 1 条「附着边」挂到核上（共 1000+9000 条边）。
# 图连通（T0=0）。悬挂部分的答案形状完全确定：
#   附着边切开 s=10 的子树 → 10*(n-10) mod 1000 = 900；链内边 s=9..1 → s*(n-s) mod 1000
#   依次 919,936,951,964,975,984,991,996,999（互不相同），是「顶格 IO + 确定答案」的测试点；
#   核心区的随机边可能残留少量桥（答案由核心区子树结构决定），不做手算。
def gen9():
    random.seed(173409)
    n, m, Q = 100000, 1000000, 800000
    core = 90000                 # 核心点数
    chains, clen = 1000, 10      # 悬挂链数 / 每条链点数
    assert core + chains * clen == n
    edges = [(i, randint(0, i - 1)) for i in range(1, core)]      # 核心随机生成树（保证连通）
    while len(edges) < 990000:
        edges.append((randint(0, core - 1), randint(0, core - 1)))  # 稠密核：无桥
    for c in range(chains):
        base = core + c * clen
        edges.append((randint(0, core - 1), base))          # 附着边（桥）
        for j in range(clen - 1):
            edges.append((base + j, base + j + 1))          # 链内边（桥）
    assert len(edges) == m, len(edges)
    # 询问：前 10000 条覆盖全部分量边（1 附着 + 9 链内）× 1000 条链，其余随机
    pendant_ids = list(range(990000, m))
    queries = list(pendant_ids)
    queries += [randint(0, m - 1) for _ in range(Q - len(pendant_ids))]
    random.shuffle(queries)
    emit(9, n, edges, queries)


# ---------------------------------------------------------------- 点 10 顶格层（卡常）
# n=100000（顶格）, m=1000000（顶格）, Q=800000（顶格）：卡常/极值结构：
#   边 0..n-2 构成链 0-1-2-...-99999（DFS 深度最大结构，卡递归爆栈的错解）；
#   随后 999998 条全为 (0,1) 的重边（与边 0 平行，故这几条全部不是桥，
#   且可以卡「按父顶点跳过」而非按父边编号跳过的错解）；最后 2 条自环。
#   桥集合 = 边 1..99998（链上除首边外全部）；询问覆盖所有桥 + 重复随机询问。
def gen10():
    n, m, Q = 100000, 1000000, 800000
    chain = n - 1                              # 链边数，编号 0..chain-1
    edges = [(i - 1, i) for i in range(1, n)]  # 0-1-2-...-99999 链
    while len(edges) < m - 2:
        edges.append((0, 1))                   # 与边 0 平行的海量重边
    edges.append((0, 0))                       # 自环
    edges.append((n - 1, n - 1))               # 自环
    assert len(edges) == m, len(edges)
    queries = list(range(1, chain))            # 覆盖链上每条桥（边 0 是平行边，不是桥）
    extra = Q - len(queries)
    mrand = [i for i in range(m) if i != 0]    # 额外询问尽量不重复问边 0
    queries += [mrand[(i * 97) % len(mrand)] for i in range(extra)]
    emit(10, n, edges, queries)


def main():
    require_std()
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    print("ALL 10 GROUPS GENERATED")


if __name__ == "__main__":
    main()
