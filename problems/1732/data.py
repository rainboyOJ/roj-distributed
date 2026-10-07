#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1732《情报传递》分层测试数据生成器（cyaron，仓库惯例）
# ---------------------------------------------------------------------------
# 用法（先编译 std，data.py 会校验它存在；cyaron 在 std 缺失时会静默产出 0 字节 .out）：
#   g++ -O2 -std=c++17 -o std std.cpp
#   mkdir -p data && cd data && python3 ../data.py
#
# 题意：n 个人的有向电话线情报网。①要求(a,b)：a 能经 1 条或多条边走达 b（m1 条）；
#       ②要求(a,b)：a 不能走达 b（m2 条）。构造满足全部要求的图，或判定不存在。
#       输出 YES + 边数 P + P 条边（要求 P ≤ n+m+t）；无解输出 NO。
# 数据范围（题面明文）：1 ≤ n, m, t ≤ 1e5；1 ≤ a, b ≤ n；a ≠ b。
#
# ---- 分层策略（10 点，从下界 → 顶格；每点单组）----
#   点 1  边界层：题面【输入样例】逐字（n=3，①(1,2)(2,3)，②(1,3)）→ 期望 NO（回归题面样例 1）
#   点 2  边界层：题面【输入样例 2】逐字（同上但 ②(3,1)）→ 期望 YES（P=2，回归题面样例 2）
#   点 3  边界层：全下界 n=2, m=1, t=1（①(1,2)，②(2,1)）→ 期望 YES（P=1）
#   点 4  边界层：最小规模的 NO（n=2，①(1,2)(2,1) 成环，②(1,2)）→ 同 SCC 快速判定路径
#   点 5  小规模随机：n=m=t=100，层级结构 + 5 点小环（含 SCC）
#   点 6  中规模：n=m=t=1000，50 点大环；②含环内一对 → NO（走「同 SCC ⇒ 立即 NO」快速路径）
#   点 7  中大规模：n=5000, m=t=10000，200 点环；②含一条真实跨层边 (a,b) → NO
#         （走「缩点 DAG bitset 可达性 DP」判定路径，非快速路径）
#   点 8  大规模：n=30000, m=t=100000，100 层、1000 点环 → YES（P=100000 的大输出）
#   点 9  顶格层：n=100000, m=t=100000，200 层、5000 点环 → YES（P=100000，最大规模 + 大输出）
#   点 10 顶格层（最坏 NO）：n=100000 的长链（m=99999 条 1→2→…→N），t=100000；
#         其余 ② 全是 a>b 的不可达对（其 target 铺满全部 19 个 bitset 分块），唯独一条
#         ②(1,2) 是真实①边（必可达），且其 target 的 col = n-1 = 99999 落在**最后一分块**
#         ⇒ std 必须算完全部 19 个分块的可达性 DP 才判出 NO（最坏时间路径）。
#
# ---- 构造为什么是「可证」的（据此校验 std 的 YES/NO 判决，不依赖任何对拍）----
#   层级构造：给每个节点编号 level，所有①边严格从高 level 指向低 level（环内边不跨层）。
#     于是任一路径 level 严格递减 ⇒ ② 只要取 level(a) < level(b) 就**必然不可达** ⇒ 期望 YES。
#   违规构造：显式塞入一条「本身就在①要求里」的 ② 对 ⇒ 1 步可达 ⇒ 期望 NO；
#     或塞入同一环（同一 SCC）内的一对 ⇒ 期望 NO；或塞入跨层①要求对 ⇒ 期望 NO。
#   ⇒ 每个点的期望结论都由构造直接证明，生成后与 std 输出逐点比对（见 assert_*），
#     并在文件末尾用证书校验段复核（见证对 + 输出图合法性）。
#
#   ⚠ 数组/规模上限均按题面上限（n,m,t ≤ 1e5）取值，未越界；生成器全程线性（无 O(n^2) 循环）。
#   ⚠ 依任务铁律：本包**不含** brute / 对拍 / stress。正确性靠「构造可证 + 输出图验证」：
#     · YES 点：输出图 = ①边集（逐条比对），再在输出图上**独立重算可达性**（Kosaraju + Kahn
#       拓扑 + 分块大整数 bitset DP），断言全部②不可达 ⇒ 输出合法（评测器只需存在合法输出）；
#     · NO 点：断言存在②对在「①要求图」中 1 步可达（提供显式见证对），由传递性可知任何
#       合法情报网都必须满足该①要求 ⇒ 必违反② ⇒ NO 唯一正确（不需要任何搜索/对拍）。

import os
import random
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
STD_REL = "../std"          # cyaron output_gen 相对 data/ 的路径（仓库惯例）
MAX = 100000                # 题面上限 n, m, t ≤ 1e5

# ===========================================================================
# 0. 前置校验：std 必须存在（cyaron 在 std 缺失时会「静默」产出 0 字节 .out）
# ===========================================================================
STD_ABS = os.path.join(HERE, "std")
if not (os.path.isfile(STD_ABS) and os.access(STD_ABS, os.X_OK)):
    sys.exit("[FATAL] 未找到可执行的 %s —— 先执行：g++ -O2 -std=c++17 -o std std.cpp" % STD_ABS)
print("[precheck] std 存在且可执行：%s" % STD_ABS)


# ===========================================================================
# 1. 构造器
# ===========================================================================
def level_instance(n, m1, t, nlev, ring, seed, violation=None):
    """层级构造。返回 (edges, queries, expect)。

    所有①边从高 level 指向低 level（环内边同层）；②取 level(a) < level(b) ⇒ 不可达 ⇒ YES。
    violation:
      None            -> 期望 YES
      ("scc", i, j)   -> 在环内两端 i,j 之间塞一条②（同 SCC ⇒ 必然可达）=> 期望 NO
      ("edge", idx)   -> 把②设成第 idx 条真实①边（1 步可达）=> 期望 NO
    """
    assert ring <= n and nlev >= 2 and m1 >= 1 and t >= 1
    rng = random.Random(seed)

    # level：0 号为环（最底层汇），其余节点随机分布在 1..nlev-1
    lvl = [0] * n
    for v in range(ring, n):
        lvl[v] = rng.randint(1, nlev - 1)
    nlv = [[] for _ in range(nlev)]
    for v in range(n):
        nlv[lvl[v]].append(v)

    # ---- ①边：严格跨层（高 -> 低）去重 ——
    edges = []
    seen = set()
    # 环内边：0 -> 1 -> ... -> ring-1 -> 0（ring >= 2 时构成一个大小 ring 的 SCC）
    if ring >= 2:
        for v in range(ring):
            w = (v + 1) % ring
            edges.append((v + 1, w + 1))     # 题面 1-based
            seen.add((v, w))
    # 其余边：随机选高层 u，再从更低的层里选 v
    while len(edges) < m1:
        lu = rng.randint(1, nlev - 1)
        lv = rng.randint(0, lu - 1)
        u = nlv[lu][rng.randrange(len(nlv[lu]))]
        v = nlv[lv][rng.randrange(len(nlv[lv]))]
        if u == v or (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u + 1, v + 1))
    assert len(edges) == m1

    # ---- ②查询：level(a) < level(b) ⇒ 必然不可达 ----
    queries = []
    while len(queries) < t:
        la = rng.randint(0, nlev - 2)
        lb = rng.randint(la + 1, nlev - 1)
        if not nlv[la] or not nlv[lb]:
            continue
        a = nlv[la][rng.randrange(len(nlv[la]))]
        b = nlv[lb][rng.randrange(len(nlv[lb]))]
        queries.append((a + 1, b + 1))
    assert len(queries) == t

    if violation is None:
        return edges, queries, "YES"
    if violation[0] == "scc":                       # 同 SCC 内的一对 ⇒ 可达 ⇒ NO
        i, j = violation[1], violation[2]
        assert i < ring and j < ring and i != j
        assert lvl[i] == lvl[j] == 0
        pos = t // 2
        queries[pos] = (i + 1, j + 1)
        return edges, queries, "NO"
    if violation[0] == "edge":                      # 直接取一条真实①边作② ⇒ 1 步可达 ⇒ NO
        idx = violation[1]
        pos = t // 2
        queries[pos] = edges[idx]
        return edges, queries, "NO"
    raise AssertionError("unknown violation")


def chain_instance(n, t, seed, violate=False):
    """长链 1→2→…→n（m1 = n-1 条边，全程只有跨 SCC 边）。链上 a 可达 b ⟺ a ≤ b。

    ②取 a > b ⇒ 链上不可达 ⇒ 保留 YES；若 violate=True，额外塞一条 ②(1,2)（一条真实的
    ①边，必然可达）⇒ 期望 NO。
    为何是 std 的最坏路径：Tarjan 对纯链的自洽编号为 col[k] = n-k+1（链头 1 的 col = scc 最大），
    故违规对 (1,2) 的 target 的 col = n-1 落在 **最后一个 bitset 分块**（分块按 col 升序）；
    其余 ② 的 target 铺满全部 19 个分块 ⇒ std 必须把 19 个分块的可达性 DP 全部算完，
    在最后一块才判出 NO（最坏时间路径，且可达性经分块 DP 传递而非直接单边）。"""
    edges = [(i, i + 1) for i in range(1, n)]
    rng = random.Random(seed)
    queries = []
    while len(queries) < t - (1 if violate else 0):
        b = rng.randint(1, n - 1)
        a = rng.randint(b + 1, n)          # a > b ⇒ 链上不可达
        queries.append((a, b))
    if violate:
        queries.append((1, 2))             # 违规：链上直接可达（col[2]=n-1，落在最后一块）
    assert all(a != b for a, b in queries)
    return edges, queries, ("NO" if violate else "YES")


# ===========================================================================
# 2. 写出 + 生成后强校验（.out 非空、行数、结构、P 上限、边集一致）
# ===========================================================================
def write_case(idx, n, edges, queries, expect, note, expect_exact=None):
    m1, m2 = len(edges), len(queries)
    assert 1 <= n <= MAX and 1 <= m1 <= MAX and 1 <= m2 <= MAX
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in queries)

    io = IO(file_prefix="problem", data_id=idx)      # problem{idx}.in / .out
    io.input_writeln(n)
    io.input_writeln(m1)
    for a, b in edges:
        io.input_writeln(a, b)
    io.input_writeln(m2)
    for a, b in queries:
        io.input_writeln(a, b)
    io.output_gen(STD_REL)                           # .out 由 std 生成
    io.input_file.flush()                            # cyaron 不自动落盘，先 flush
    if io.output_file is not None:
        io.output_file.flush()                       # .out 是带缓冲句柄，读前必须 flush

    out_path = "problem%d.out" % idx
    size = os.path.getsize(out_path)
    assert size > 0, "点 %d: .out 为 0 字节（std 缺失或崩溃）" % idx
    lines = open(out_path).read().split("\n")
    assert lines[-1] == "", "点 %d: .out 末尾缺少换行" % idx
    lines = lines[:-1]

    # ---- 结构校验 ----
    assert lines[0] in ("YES", "NO"), "点 %d: 首行既非 YES 也非 NO：%r" % (idx, lines[0])
    if lines[0] == "NO":
        assert len(lines) == 1, "点 %d: NO 输出应为单行，实际 %d 行" % (idx, len(lines))
    else:
        assert len(lines) == 2 + m1, \
            "点 %d: YES 输出应为 2+m1=%d 行，实际 %d 行" % (idx, 2 + m1, len(lines))
        P = int(lines[1])
        assert P == m1, "点 %d: 第二行 P=%d 与 m1=%d 不符" % (idx, P, m1)
        assert P <= n + m1 + m2, "点 %d: P=%d 超过 n+m+t=%d" % (idx, P, n + m1 + m2)
        got = []
        for ln in lines[2:]:
            u, v = ln.split()
            u, v = int(u), int(v)
            assert 1 <= u <= n and 1 <= v <= n, "点 %d: 输出边越界 (%d,%d)" % (idx, u, v)
            assert u != v, "点 %d: 输出自环 (%d,%d)" % (idx, u, v)
            got.append((u, v))
        # 输出边集必须与①边集逐条一致（多集相等）；且①的每条需求边都在（①由构造满足）
        from collections import Counter
        cg, ce = Counter(got), Counter(edges)
        assert cg == ce, "点 %d: 输出边集与①边集不一致" % idx
        assert all(a != b for a, b in got)

    # ---- 结论校验：与构造给出的可证期望逐点比对 ----
    assert lines[0] == expect, \
        "点 %d: std 判 %s，构造可证期望 %s" % (idx, lines[0], expect)
    if expect_exact is not None:                     # 题面样例：逐字节比对
        body = open(out_path, "rb").read()
        assert body == expect_exact, \
            "点 %d: 与题面输出不逐字节一致：%r != %r" % (idx, body, expect_exact)

    print("problem%-2d: n=%-6d m1=%-6d m2=%-6d -> %-3s (.out %d 字节 / %d 行) -- %s"
          % (idx, n, m1, m2, lines[0], size, len(lines), note))
    return lines[0]


# ===========================================================================
# 3. 十个测试点
# ===========================================================================
rows = []

# ---- 点 1：题面输入样例（逐字）→ 期望 NO ----
s1_edges = [(1, 2), (2, 3)]
s1_q = [(1, 3)]
assert s1_q[0] == (1, 3)
rows.append(write_case(1, 3, s1_edges, s1_q, "NO",
                       "边界层：题面【输入样例】逐字（②要求 1 可达 3，与①链矛盾）",
                       expect_exact=b"NO\n"))

# ---- 点 2：题面输入样例 2（逐字）→ 期望 YES，P=2 ----
rows.append(write_case(2, 3, s1_edges, [(3, 1)], "YES",
                       "边界层：题面【输入样例2】逐字（②要求 3 不可达 1）",
                       expect_exact=b"YES\n2\n1 2\n2 3\n"))

# ---- 点 3：全下界 n=2, m=1, t=1 ----
rows.append(write_case(3, 2, [(1, 2)], [(2, 1)], "YES",
                       "边界层：n,m,t 全取题面下界 n=2,m=1,t=1（a≠b 约束下最小 n）"))

# ---- 点 4：最小规模 NO（2 点环，同 SCC 快速路径）----
rows.append(write_case(4, 2, [(1, 2), (2, 1)], [(1, 2)], "NO",
                       "边界层：最小规模无解，①②在 2 点环上矛盾（同 SCC ⇒ 立即 NO）"))

# ---- 点 5：小规模随机 n=m=t=100 ----
e5, q5, x5 = level_instance(100, 100, 100, nlev=10, ring=5, seed=173205)
rows.append(write_case(5, 100, e5, q5, x5,
                       "小规模随机：n=m=t=100，10 层 + 5 点小环（层级边只向低层，②全取低层->高层）"))

# ---- 点 6：中规模，同 SCC 快速路径 NO ----
e6, q6, x6 = level_instance(1000, 1000, 1000, nlev=20, ring=50, seed=173206,
                            violation=("scc", 3, 40))
rows.append(write_case(6, 1000, e6, q6, x6,
                       "中规模：n=m=t=1000，20 层 + 50 点大环；②含环内一对 ⇒ NO（同 SCC 快速判定）"))

# ---- 点 7：中大规模，DP 判定路径 NO（②取一条真实跨层边）----
e7, q7, x7 = level_instance(5000, 10000, 10000, nlev=50, ring=200, seed=173207,
                            violation=("edge", 1234))
rows.append(write_case(7, 5000, e7, q7, x7,
                       "中大规模：n=5000,m=t=10000，50 层 + 200 点环；②含一条真实跨层边 ⇒ NO"
                       "（不同 SCC，走 bitset 可达性 DP 判定）"))

# ---- 点 8：大规模 YES ----
e8, q8, x8 = level_instance(30000, 100000, 100000, nlev=100, ring=1000, seed=173208)
rows.append(write_case(8, 30000, e8, q8, x8,
                       "大规模：n=30000，m=t=100000，100 层 + 1000 点环 ⇒ YES，P=100000"))

# ---- 点 9：顶格 YES（m=t=1e5，n=1e5，大环）----
e9, q9, x9 = level_instance(MAX, MAX, MAX, nlev=200, ring=5000, seed=173209)
rows.append(write_case(9, MAX, e9, q9, x9,
                       "顶格层：n=m=t=100000，200 层 + 5000 点环 ⇒ YES，P=100000（最大规模 + 大输出）"))

# ---- 点 10：顶格 NO（长链最坏路径：算完所有分块才判出）----
e10, q10, x10 = chain_instance(MAX, MAX, seed=173210, violate=True)
rows.append(write_case(10, MAX, e10, q10, x10,
                       "顶格层（最坏 NO）：n=t=100000 长链（m=99999），②的 target 铺满全部分块，"
                       "违规对 (1,2) 落在最后一个分块 ⇒ std 必须算完 19 个分块的可达性 DP 才判 NO"))

# ===========================================================================
# 4. 证书校验：①边集 = 输出边集 & 断言②在①图中的可达性（线性，非搜索）
# ---------------------------------------------------------------------------
# 本段独立于 std：只用「Kosaraju SCC + Kahn 拓扑 + 分块大整数 bitset DP」在 .in 的①图上
# 重算可达性（O(n + m1 + m2)，无任何枚举/搜索/对拍）：
#   · 对每条 ① 要求：必须可达 ⇒ 若不可达说明构造自相矛盾（断言失败）；
#   · 对每条 ② ：YES 点须不可达（⇒ 输出合法）；NO 点须存在一条**一步可达**的见证对
#     ⇒ 记入 CERT 并由「传递性」证明该点 NO 唯一正确。
# ===========================================================================
BITS = 4096


def parse_in(idx):
    it = iter(open("problem%d.in" % idx, "rb").read().split())
    n = int(next(it)); m1 = int(next(it))
    edges = [(int(next(it)), int(next(it))) for _ in range(m1)]
    m2 = int(next(it))
    qs = [(int(next(it)), int(next(it))) for _ in range(m2)]
    assert next(it, None) is None, "点 %d 输入有尾部多余数据" % idx
    return n, edges, qs


def kosaraju(n, adj, radj):
    comp = [-1] * n
    seen = bytearray(n)
    order = []
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = 1
        stack = [(s, 0)]
        while stack:
            u, i = stack.pop()
            if i < len(adj[u]):
                stack.append((u, i + 1))
                v = adj[u][i]
                if not seen[v]:
                    seen[v] = 1
                    stack.append((v, 0))
            else:
                order.append(u)
    C = 0
    for s in reversed(order):
        if comp[s] != -1:
            continue
        comp[s] = C
        stack = [s]
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = C
                    stack.append(v)
        C += 1
    return comp, C


def reach_info(n, edges, qs):
    """返回 (ok_edges, hit_qs, wit)：①每条是否可达、②每条是否可达、②一步见证。"""
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    eset = set()
    for a, b in edges:
        adj[a - 1].append(b - 1)
        radj[b - 1].append(a - 1)
        eset.add((a, b))
    comp, C = kosaraju(n, adj, radj)
    succ = [[] for _ in range(C)]
    indeg = [0] * C
    for a, b in edges:
        ca, cb = comp[a - 1], comp[b - 1]
        if ca != cb:
            succ[ca].append(cb)
            indeg[cb] += 1
    dq = [c for c in range(C) if indeg[c] == 0]
    topo = []
    while dq:
        c = dq.pop()
        topo.append(c)
        for d in succ[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                dq.append(d)
    assert len(topo) == C, "缩点图仍有环（SCC 计算有误）"
    rtop = topo[::-1]

    def solve(targets):
        """返回 res[k] = 第 k 个 (src,tgt) 对是否可达（**按 k 索引**，不按分块顺序）。"""
        res = [False] * len(targets)
        for lo in range(0, C, BITS):
            hi = min(C, lo + BITS)
            rows = [0] * C
            for c in rtop:
                m = (1 << (c - lo)) if lo <= c < hi else 0
                for d in succ[c]:
                    m |= rows[d]
                rows[c] = m
            for k, (cs, ct) in enumerate(targets):
                if lo <= ct < hi:
                    res[k] = bool((rows[cs] >> (ct - lo)) & 1)
        return res

    ec = [(comp[a - 1], comp[b - 1]) for a, b in edges]
    qc = [(comp[a - 1], comp[b - 1]) for a, b in qs]
    ok_edges = solve(ec)
    hit_qs = solve(qc)
    # ---- 见证（NO 点用）：三类可人工核对的可达证书 ----
    #   1) ②对本身即①要求 ⇒ 1 步可达；
    #   2) ②两端同属①图的一个 SCC ⇒ 绕环 + ①边多步可达；
    #   3) 其余：线性 BFS 从 a 重建一条①边构成的 a⇝b 路径（O(n+m1)，非搜索/枚举）。
    def bfs_path(a0, b0):
        par = {a0: 0}
        stack = [a0]
        while stack:
            u = stack.pop()
            for v in adj[u - 1]:
                v1 = v + 1
                if v1 not in par:
                    par[v1] = u
                    if v1 == b0:
                        path = [b0]
                        while path[-1] != a0:
                            path.append(par[path[-1]])
                        return path[::-1]
                    stack.append(v1)
        return None

    wit = []
    for k in range(len(qs)):
        a, b = qs[k]
        if (a, b) in eset:
            wit.append((a, b, "②对本身即①要求（1 步可达）"))
        elif qc[k][0] == qc[k][1]:
            wit.append((a, b, "②两端同属①图的一个 SCC"))
        elif hit_qs[k] and n <= 10000:
            path = bfs_path(a, b)
            assert path, "点内②判为可达但 BFS 找不到路径（实现矛盾）"
            wit.append((a, b, "①图上的可达路径 " + "→".join(map(str, path))))
        elif hit_qs[k]:
            wit.append((a, b, "在①图中可达（独立可达性 DP 判定，传递闭包）"))
        else:
            wit.append(None)
    return ok_edges, hit_qs, wit


def certificate_check(idx, expect):
    n, edges, qs = parse_in(idx)
    out_path = "problem%d.out" % idx
    lines = open(out_path).read().split("\n")
    assert lines[-1] == "", "点 %d: .out 末尾缺换行" % idx
    lines = lines[:-1]
    m1, m2 = len(edges), len(qs)
    ok_edges, hit_qs, wit = reach_info(n, edges, qs)
    assert all(ok_edges), "点 %d: 有①要求在①图中不可达（构造矛盾）" % idx
    assert any(hit_qs) == (expect == "NO"), \
        "点 %d: 独立可达性重算与期望判决不一致" % idx
    if expect == "YES":
        assert not any(hit_qs), "点 %d: 存在②在①图中可达（YES 判错）" % idx
        assert lines[0] == "YES" and int(lines[1]) == m1, "点 %d: P 行异常" % idx
        got = [tuple(int(x) for x in ln.split()) for ln in lines[2:]]
        from collections import Counter
        assert Counter(got) == Counter(edges), "点 %d: 输出边集 ≠ ①边集" % idx
        # 输出图正是①图，上面已证全部②不可达 ⇒ 该输出合法（评测器判 AC）
        return "-", "输出图=①边集且全部②不可达 ⇒ 合法"
    else:
        assert lines == ["NO"], "点 %d: NO 点输出应为单行 NO" % idx
        ks = [k for k in range(m2) if wit[k] is not None]
        assert ks, "点 %d: NO 但未给出可人工核对的可达见证②对" % idx
        w = wit[ks[0]]
        return w, "②%s 可达见证：%s ⇒ 任何合法网必违反 ⇒ NO 唯一" % ((w[0], w[1]), w[2])


print("\n====== 证书校验（独立 Kosaraju+Kahn+分块 bitset，仅线性可达性，无搜索/对拍）======")
CERT = {}
for i in range(1, 11):
    w, note = certificate_check(i, rows[i - 1])
    CERT[i] = (rows[i - 1], w, note)
    print("  problem%-2d 判 %-3s 证书 %-12s %s" % (i, rows[i - 1], str(w), note))
assert len(rows) == 10, "必须恰好 10 个测试点"
assert rows[0] == "NO" and rows[1] == "YES" and rows[9] == "NO"
print("\n分层自检通过：10 点齐全（YES %d 个 / NO %d 个）；下界点 3、样例点 1-2、"
      "顶格点 9-10 均按构造可证结论 + 证书校验通过。" % (rows.count("YES"), rows.count("NO")))
print("规模梯度 n: 3,3,2,2,100,1000,5000,30000,100000,100000")
