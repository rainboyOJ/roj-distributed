#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1731《最大流》分层测试数据生成器（cyaron）
#
# 用法（在本题目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std          # 必须先编译 std
#     mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（content.md）：
#     2 <= n <= 3000，0 <= m <= floor(3n/2)；无重边、无自环；每个点的度数 <= 3。
#     输入：第一行 n m，接下来 m 行每行 x y；输出一行一个整数（所有点对 i<j 间
#     最大流之和）。
#     子任务：30% n,m<=50；另 10% 所有点度数 <= 2；另 30% 度数为 3 的点数 <= 5。
#
# 【分层设计】一个测试点 = 一张图：无多组数据、无随机权值，输出由图的形状唯一决定。
#   故分层 = 按规模（n、m）与结构分档：边界下限 -> 小 -> 中 -> 大 -> 顶格，并逐档
#   对准题面三个子任务。除点 6（随机 3-正则）外全部采用**答案可闭式推导**的构造，
#   每组都带独立可校验的期望答案；点 6 用「答案上界 + 结构性质」双重校验。
#
#   点 1  n=2,  m=0    边界下限：两个孤立点 — 答案 0（m 下界）
#   点 2  n=2,  m=1    边界下限：一条边 — 答案 1（n 下界、最小非零答案）
#   点 3  n=6,  m=8    【提示】样例输入 2 原样 — 答案 36（题面给出，回归校准）
#   点 4  n=8,  m=7    树（度全 <= 2）：路径 P8 — 所有点对流 = 1，答案 C(8,2)=28
#   点 5  n=20, m=21   小混合（4 个分量）：K4(流3) + C5 + C6(流2) + P5(流1)，
#                      同一批数据内 0/1/2/3 四种点对最大流齐备 — 答案 78
#   点 6  n=50, m=75   30% 子任务上界（n,m <= 50）：随机 3-正则图 — 答案 3*C(50,2)
#                      = 3675（上界 + 3-边连通性双重校验，见下）
#   点 7  n=600,m=600  10% 子任务（度全 <= 2）：单个环 C600 — 所有点对流 = 2
#   点 8  n=1000,m=1000 另一 30% 子任务（度 3 的点 <= 5）：路径 P1000 + 弦(100,900)，
#                      度 3 的点恰 2 个 — 环上点对流 2、其余 1
#   点 9  n=3000,m=3000 大“毛虫”连通图（n 顶格）：环 C1000，每个环点挂一条长度 2 的
#                      树腿（1000 条）— 环上点对流 2、其余点对流 1，答案 4998000
#   点 10 n=3000,m=4500 顶格构造（n,m 双顶格）：棱柱 C1500 x K2（3-正则 3-边连通）
#                      — 所有点对流 = 3，答案 = 3*C(3000,2) = 13495500（答案上界）
#
# 【期望答案的闭式依据】（最大流 = 最小割；deg <= 3 故任意点对流量 ∈ {0,1,2,3}）
#   (a) 树/路径 P_k：任意点对流 = 1（连通给出 >= 1；每条边都是割边给出 <= 1）。
#   (b) 环 C_k (k>=3)：任意点对流 = 2 —— 两条弧给出 2 条边不相交路径（>= 2）；
#       任一点度为 2，其两条关联边构成大小 2 的割（<= 2）。
#   (c) K4 与棱柱 C_k x K2 (k>=3)：均为 3-正则且 3-边连通 => 任意点对流 = 3
#       （>= 3 来自 3-边连通，<= 3 来自端点度 = 3）。
#   (d) 细分棱柱 = 把 C_k x K2 (k>=3) 的竖棱 top[0]-bot[0] 换成 top[0]-x-bot[0]：
#       * 原 2k 个顶点度仍为 3；对任意割 S，δ(S) 的边数与原棱柱相同（只把一条竖棱
#         一分为二）=> 原顶点间边连通度仍为 3 => 流量 = 3；
#       * x 的度为 2（这 2 条边即为隔断 x 的割）=> x 与任一原顶点流量 = 2。
#   (e) 桥（割边）与度 2 连接器：任何 u-v 流可分解为边不相交简单路径，简单路径
#       不会两次穿过同一条割边，故割边对流量贡献为 0。因此用桥/度 2 单点连接器
#       串起来的块：块内流量完全不变，跨块点对流量恰为 1（块间通路唯一）。
#       （度 2 连接器 c 的两条边都是割边，故 c 与任一点对流 = 1。）
#   (f) 不同连通分量之间无通路 => 流量 0；分量之间无公共边，互不影响。
#   (g) 弦图（点 8）：P_n 加弦 (100,900) 只形成一个简单环（点 100..900）。
#       环上点对：公共简单环 => >= 2；环内非弦端点度 = 2 => <= 2 => 恰为 2。
#       其余点对：至少一端在树枝上且该端唯一外向通路 => 恰为 1。
#   (h) 通用上界（点 6 用）：任意点对流量 <= min(deg(u), deg(v)) <= 3。故
#       3-正则图上答案必 <= 3*C(n,2)；若再独立验证图是 3-边连通的，则答案恰等于
#       3*C(n,2)，即由**上界 + 结构性质**钉死，无需另写求解程序。
#
# 【生成器复杂度】全部线性：构造件为一次遍历；随机 3-正则图用桩配对（O(n)）；
#   Python 侧 3-边连通校验为 O(m^2 * (n+m)) 但只在 n=50 的小点上做（见 point6），
#   实测 < 1s；无任何 O(n^2) Python 循环。
#
# 【自检】生成前断言 std 已编译存在（cyaron 在 std 缺失时不报错，而是静默产出
#   0 字节 .out，故必须前置校验）；生成后逐点断言 .in 结构合法（n/m 范围、无自环、
#   无重边、度 <= 3、行数与边表一致、边集与设计一致）、.out 非空且恰一行非负整数，
#   并核对该点的闭式期望答案。

import os
import random

from cyaron import IO

N_MAX = 3000
M_OVER_N = 3          # m <= floor(3n/2)


# ==========================================================================
# 建图器
# ==========================================================================
class Builder:
    """按题面约束（度 <= 3、无重边自环）建图；登记「块」与「分量」。

    块 = 一组点 + 该组内部所有点对的流量之和（闭式给定）。
    分量 = 块的列表；同分量内跨块点对流 = 1，跨分量 = 0。
    """

    def __init__(self, n):
        self.n = n
        self.edges = set()
        self.deg = [0] * (n + 1)
        self.blocks = []              # [(size, internal_flow_sum, comp_key)]

    def add(self, a, b):
        assert a != b, f"自环 {a}"
        key = (a, b) if a < b else (b, a)
        assert key not in self.edges, f"重边 {key}"
        assert self.deg[a] < 3 and self.deg[b] < 3, f"端点 {a}/{b} 度数已满 3"
        self.edges.add(key)
        self.deg[a] += 1
        self.deg[b] += 1

    def block(self, size, internal_flow_sum, comp=None):
        """登记一个块；comp 为分量标识（同标识的块在同一连通分量）。

        comp 为 None 时新开一个自动标识。返回该块的标识。
        """
        if comp is None:
            comp = len(self.blocks)          # 自动标识：唯一即可
        self.blocks.append((size, internal_flow_sum, comp))
        return comp

    def answer(self):
        """闭式期望答案：块内流量和 + 同分量内跨块点对 * 1。"""
        total = sum(s for _, s, _ in self.blocks)
        by_comp = {}
        for size, _s, comp in self.blocks:
            by_comp.setdefault(comp, []).append(size)
        for sizes in by_comp.values():
            size = sum(sizes)
            inside = sum(k * (k - 1) // 2 for k in sizes)
            total += size * (size - 1) // 2 - inside
        return total


# ==========================================================================
# 构造件：均返回节点列表，并按闭式登记块
# ==========================================================================
def add_path(b, start, k, comp=None):
    """路径 P_k：任意点对流 = 1 => 块内和 C(k,2)。"""
    nodes = list(range(start, start + k))
    for i in range(k - 1):
        b.add(nodes[i], nodes[i + 1])
    b.block(k, k * (k - 1) // 2, comp)
    return nodes


def add_cycle(b, start, k, comp=None):
    """环 C_k (k>=3)：任意点对流 = 2 => 块内和 2*C(k,2)。"""
    nodes = list(range(start, start + k))
    for i in range(k):
        b.add(nodes[i], nodes[(i + 1) % k])
    b.block(k, 2 * k * (k - 1) // 2, comp)
    return nodes


def add_k4(b, start, comp=None):
    """K4：3-正则 3-边连通 => 任意点对流 = 3 => 块内和 18。"""
    nodes = list(range(start, start + 4))
    for i in range(4):
        for j in range(i + 1, 4):
            b.add(nodes[i], nodes[j])
    b.block(4, 18, comp)
    return nodes


def add_prism(b, start, k, comp=None):
    """棱柱 C_k x K2 (k>=3)：3-正则 3-边连通 => 任意点对流 = 3（2k 点、3k 边）。"""
    top = list(range(start, start + k))
    bot = list(range(start + k, start + 2 * k))
    for i in range(k):
        j = (i + 1) % k
        b.add(top[i], top[j])           # 上圈
        b.add(bot[i], bot[j])           # 下圈
        b.add(top[i], bot[i])           # 竖棱
    n = 2 * k
    b.block(n, 3 * n * (n - 1) // 2, comp)
    return top + bot


def add_subdivided_prism(b, start, k, comp=None):
    """细分棱柱：竖棱 top[0]-bot[0] 换成 top[0]-x-bot[0]（x = start+2k，度 2）。

    原 2k 点间流量 = 3；x 与原点流量 = 2 => 块内和 = 3*C(2k,2) + 2*(2k)。
    返回 (x, 全部节点)。
    """
    top = list(range(start, start + k))
    bot = list(range(start + k, start + 2 * k))
    x = start + 2 * k
    for i in range(k):
        j = (i + 1) % k
        b.add(top[i], top[j])
        b.add(bot[i], bot[j])
    b.add(top[0], x)
    b.add(x, bot[0])
    for i in range(1, k):
        b.add(top[i], bot[i])
    origin = 2 * k
    b.block(origin + 1, 3 * origin * (origin - 1) // 2 + 2 * origin, comp)
    return x, top + bot + [x]


def add_chorded_path(b, start, n, p=100, q=900, comp=None):
    """路径 P_n 加弦 (p,q)：环上点对流 = 2，其余 = 1。

    环 = 节点 p..q（cyc = q-p+1 个）；块内和 = 2*C(cyc,2) + (C(n,2) - C(cyc,2))。
    """
    nodes = list(range(start, start + n))
    for i in range(n - 1):
        b.add(nodes[i], nodes[i + 1])
    b.add(nodes[p - 1], nodes[q - 1])
    cyc = q - p + 1
    total = n * (n - 1) // 2
    b.block(n, 2 * cyc * (cyc - 1) // 2 + (total - cyc * (cyc - 1) // 2), comp)
    return nodes


def rand_regular3(n, rng, max_attempts=2000):
    """随机 3-正则简单图（n 偶）：3n 个桩随机配对，O(n)/轮。返回边集。"""
    assert n % 2 == 0, "3-正则图要求 n 为偶数"
    for _ in range(max_attempts):
        stubs = [v for v in range(1, n + 1) for _ in range(3)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, 3 * n, 2):
            a, c = stubs[i], stubs[i + 1]
            key = (a, c) if a < c else (c, a)
            if a == c or key in edges:
                ok = False
                break
            edges.add(key)
        if ok:
            return edges
    raise RuntimeError("随机 3-正则图生成失败（重试次数耗尽）")


def check_3_edge_connected(n, edges):
    """独立校验：图是否 3-边连通（删任意 2 条边仍连通）。

    仅在 n=50 的小图上使用：C(75,2)=2775 对边 × 一次 BFS，实测 < 1s。
    这是**结构性质校验**（不是对拍/暴力求解答案），与「答案上界 3*C(n,2)」一起
    把随机点的答案钉死为 3*C(n,2)。
    """
    edge_list = sorted(edges)
    m = len(edge_list)
    adj = [[] for _ in range(n + 1)]
    for a, c in edge_list:
        adj[a].append(c)
        adj[c].append(a)

    def connected(banned):
        seen = [False] * (n + 1)
        stack = [1]
        seen[1] = True
        cnt = 1
        while stack:
            u = stack.pop()
            for v in adj[u]:
                key = (u, v) if u < v else (v, u)
                if key in banned or seen[v]:
                    continue
                seen[v] = True
                cnt += 1
                stack.append(v)
        return cnt == n

    for i in range(m):
        for j in range(i + 1, m):
            if not connected({edge_list[i], edge_list[j]}):
                return False
    return True


# ==========================================================================
# 十组数据：每个 case 返回 (n, edges, expect, note)
# ==========================================================================
def case1():
    """边界下限：n=2, m=0，两个孤立点 — 答案 0。"""
    b = Builder(2)
    b.block(1, 0)                 # 孤立点 1
    b.block(1, 0)                 # 孤立点 2
    return b.n, b.edges, b.answer(), "n,m 下界；答案 0"

def case2():
    """边界下限：n=2, m=1，一条边 — 答案 1（n 下界、最小非零答案）。"""
    b = Builder(2)
    b.add(1, 2)
    b.block(2, 1)
    return b.n, b.edges, b.answer(), "n 下界；最小非零答案 1"

def case3():
    """【提示】样例输入 2 原样 — 答案 36（题面给出，回归校准）。"""
    b = Builder(6)
    for x, y in [(1, 3), (2, 3), (4, 1), (5, 6), (2, 6), (5, 1), (6, 4), (5, 3)]:
        b.add(x, y)
    b.block(6, 36)
    return b.n, b.edges, b.answer(), "题面样例 2 原样（答案 36）"

def case4():
    """树（度全 <= 2）：路径 P8 — 所有点对流 = 1，答案 C(8,2) = 28。"""
    b = Builder(8)
    add_path(b, 1, 8)
    return b.n, b.edges, b.answer(), "10% 子任务结构（度全 2）；树"

def case5():
    """小混合 n=20（4 分量）：K4(3) + C5(2) + C6(2) + P5(1) — 流量 0/1/2/3 齐备。"""
    b = Builder(20)
    add_k4(b, 1)                  # 点 1..4
    add_cycle(b, 5, 5)            # 点 5..9
    add_cycle(b, 10, 6)           # 点 10..15
    add_path(b, 16, 5)            # 点 16..20
    return b.n, b.edges, b.answer(), "一张图内 0/1/2/3 四种流量齐备"

def case6():
    """30% 子任务上界（n,m <= 50）：随机 3-正则 n=50, m=75 — 答案 3675。"""
    rng = random.Random(173106)
    edges = rand_regular3(50, rng)
    assert len(edges) == 75, len(edges)
    assert check_3_edge_connected(50, edges), "随机图非 3-边连通，需换种子"
    # 3-正则 => 任意点对流量 <= min(deg)=3；3-边连通 => >= 3 => 恰好全部为 3。
    return 50, edges, 3 * 50 * 49 // 2, "随机 3-正则；3-边连通 + 上界双校验"

def case7():
    """10% 子任务（所有点度数 <= 2）：单个环 C600 — 所有点对流 = 2。"""
    b = Builder(600)
    add_cycle(b, 1, 600)
    return b.n, b.edges, b.answer(), "10% 子任务（度全 <= 2）；大环"

def case8():
    """另一 30% 子任务（度 3 的点 <= 5）：P1000 + 弦(100,900) — 度 3 点恰 2 个。"""
    b = Builder(1000)
    add_chorded_path(b, 1, 1000, 100, 900)
    return b.n, b.edges, b.answer(), "30% 子任务（度 3 的点 = 2 <= 5）；混合 1/2"

def case9():
    """大混合（n=3000 顶格，单个连通图）：细分棱柱 x2 + C1238 + P1700，用 3 条桥串成块树。

    块树（无环）：prism1 — C1238 — prism2，且 C1238 — P1700。
    桥分别挂在环上 3 个不同顶点（各使该点度数 2 -> 3），其余环点度仍为 2。
    依据 (e)：桥是割边，任何块内点对的简单路径不可能两次穿过同一条割边，
    故块内流量不变；块间只有唯一通路 => 跨块点对流恰为 1。
    块内：细分棱柱原点间 3 / 细分点 x 与原点是 2 / 环上 2 / 路径 1。
    n = 2*31 + 1238 + 1700 = 3000；m = 2*46 + 1238 + 1699 + 3 = 3032 <= 4500。
    """
    b = Builder(3000)
    comp = 0
    p1x, _n1 = add_subdivided_prism(b, 1, 15, comp)              # 点 1..31
    cyc = add_cycle(b, 32, 1238, comp)                          # 点 32..1269
    p2x, _n2 = add_subdivided_prism(b, 1270, 15, comp)          # 点 1270..1300
    pth = add_path(b, 1301, 1700, comp)                         # 点 1301..3000
    b.add(p1x, cyc[0])                                          # 桥（挂在环点 32）
    b.add(p2x, cyc[618])                                        # 桥（挂在环点 650）
    b.add(cyc[1237], pth[0])                                    # 桥（挂在环点 1269）
    assert b.n == 3000, b.n
    assert len(b.edges) == 3032, len(b.edges)
    return b.n, b.edges, b.answer(), "单个连通块树；块内 3/2/1、跨块 1"


def case10():
    """顶格（n,m 双顶格）：棱柱 C1500 x K2（3-正则 3-边连通）— 所有点对流 = 3。

    答案 = 3*C(3000,2) = 13495500，即本题答案理论上界（最坏答案值）。
    """
    b = Builder(3000)
    add_prism(b, 1, 1500)
    assert len(b.edges) == 4500, len(b.edges)
    return b.n, b.edges, b.answer(), "n,m 顶格；答案取理论最大值"


CASES = [case1, case2, case3, case4, case5, case6, case7, case8, case9, case10]


# ==========================================================================
# 写出 + 结构与输出自检
# ==========================================================================
def write_graph(io, n, edges):
    io.input_writeln(n, len(edges))
    for u, v in sorted(edges):
        x, y = (u, v) if u < v else (v, u)
        io.input_writeln(x, y)


def self_check(in_path, out_path, n, edges, expect):
    """断言 .in 结构合法 + .out 非空单行非负整数，并核对闭式期望答案。"""
    assert os.path.exists(in_path), f"{in_path} 不存在"
    assert os.path.exists(out_path), f"{out_path} 不存在"

    with open(in_path) as f:
        lines = [ln.split() for ln in f.read().split("\n") if ln.strip()]
    assert len(lines) == len(edges) + 1, f"{in_path} 行数不符：{len(lines)} != {len(edges)}+1"
    assert len(lines[0]) == 2, f"{in_path} 首行格式错"
    hn, hm = int(lines[0][0]), int(lines[0][1])
    assert 2 <= hn <= N_MAX, f"{in_path} n={hn} 越界"
    assert hn == n, f"{in_path} n={hn} != 设计值 {n}"
    assert 0 <= hm <= M_OVER_N * hn // 2, f"{in_path} m={hm} 越界"
    assert hm == len(edges), f"{in_path} m={hm} != 边表行数 {len(edges)}"

    deg = [0] * (hn + 1)
    seen = set()
    for k, e in enumerate(lines[1:], start=1):
        assert len(e) == 2, f"{in_path} 第 {k+1} 行格式错"
        x, y = int(e[0]), int(e[1])
        assert 1 <= x <= hn and 1 <= y <= hn, f"{in_path} 端点越界"
        assert x != y, f"{in_path} 存在自环 {x}"
        key = (x, y) if x < y else (y, x)
        assert key not in seen, f"{in_path} 存在重边 {key}"
        seen.add(key)
        deg[x] += 1
        deg[y] += 1
    assert max(deg) <= 3, f"{in_path} 存在度数 > 3 的点"
    norm = {(a, c) if a < c else (c, a) for a, c in edges}
    assert seen == norm, f"{in_path} 边集与设计不一致"

    body = open(out_path).read()
    assert len(body.strip()) > 0, f"⚠ {out_path} 为 0 字节/空白（std 未产出）"
    out_lines = [ln for ln in body.strip().split("\n") if ln.strip()]
    assert len(out_lines) == 1, f"{out_path} 应恰 1 行，实为 {len(out_lines)} 行"
    val = out_lines[0].strip()
    assert val.isdigit(), f"{out_path} 非非负整数：{val!r}"
    v = int(val)
    assert v == expect, f"{out_path} 答案 {v} != 闭式期望 {expect}"
    assert v <= 3 * (hn * (hn - 1) // 2), f"{out_path} 答案超过理论上界"
    return v, max(deg)


def main():
    std_path = "../std"
    assert os.path.exists(std_path), (
        "std 未编译：请先执行  g++ -O2 -std=c++17 std.cpp -o std  "
        "（cyaron 在 std 缺失时不会报错，而是静默产出 0 字节 .out）"
    )

    results = []
    for idx, fn in enumerate(CASES, start=1):
        n, edges, expect, note = fn()
        assert len(edges) <= M_OVER_N * n // 2, f"点 {idx}: m 超上界"
        io = IO(file_prefix="problem", data_id=idx)
        write_graph(io, n, edges)
        io.output_gen(std_path)
        io.output_file.flush()          # cyaron 输出带缓冲，读取前必须刷盘
        in_path, out_path = f"problem{idx}.in", f"problem{idx}.out"
        val, maxdeg = self_check(in_path, out_path, n, edges, expect)
        results.append((idx, n, len(edges), maxdeg, val, expect, note))

    print("=" * 100)
    print(f"{'点':>3} {'n':>6} {'m':>6} {'maxdeg':>7} {'std 答案':>12} {'闭式期望':>12} "
          f"{'校验':>5}  说明")
    for idx, n, m, maxdeg, val, expect, note in results:
        tag = "OK" if val == expect else "FAIL"
        print(f"{idx:>3} {n:>6} {m:>6} {maxdeg:>7} {val:>12} {expect:>12} {tag:>5}  {note}")
    print("=" * 100)
    print("SELF-CHECK OK: 10/10 组 .in 结构合法（n/m 范围、无自环、无重边、度<=3、"
          "行数与边表一致、边集与设计一致），.out 均非空且恰 1 行非负整数，"
          "全部等于该组闭式期望答案且不超过理论上界 3*C(n,2)。")


if __name__ == "__main__":
    main()
