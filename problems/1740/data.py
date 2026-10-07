#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一本通 1740《星空穿越》数据生成器（cyaron）

题意：无向简单图，边带标记 c∈{0,1}（c=1 表示该通道已被经过奇数次）。安排尽量少的
行走（路径可重复经过边/点），使每条边被走过的总次数 ≡ c (mod 2)。

理论最少人数（本题核心结论，生成器用它独立校验 std 的第一行）：
    K_min = Σ_C ( |T_C| > 0 ? |T_C|/2 : [S_C ≠ ∅] )
其中 S = {c=1 的边}，C 取遍连通块，T_C = S∩C 中度数为奇数的顶点集。

数据范围（题面）：
    测试点1: n≤10,      m≤10,     T=20
    测试点2: n≤300,     m≤3000,   T=15
    测试点3: n≤2×10^5,  m≤2×10^5, T=10, c_i=1
    测试点4: n≤2×10^5,  m≤2×10^5, T=10
    总体: 0≤c_i≤1, Σn≤5×10^5, Σm≤5×10^5；a≠b，无重边。

用法（在 data/ 目录下）：
    python3 ../data.py            # 生成全部 10 组
    python3 ../data.py 1 2        # 只生成指定编号的测试点

安全措施（针对 cyaron 在 std 缺失时静默产出 0 字节 .out 的隐患）：
  * 生成前校验 ../std 存在；
  * 生成后断言 .out 非空、行数 = K+1、K 等于本文件独立算出的理论最小值、
    且每行 l 与顶点个数一致。
"""
import os
import random
import sys
from itertools import combinations

from cyaron import IO

# ── 安全校验：std 必须存在（cyaron output_gen 缺 std 时会静默产出 0 字节 .out）──
STD_PATH = "../std"
if not os.path.exists(STD_PATH):
    raise SystemExit("FATAL: %s 不存在，请先 g++ -O2 -std=c++17 std.cpp -o std" % STD_PATH)

MAX_N = 200000          # 单组 n 上限
MAX_M = 200000          # 单组 m 上限
SUM_N = 500000          # Σn 上限
SUM_M = 500000          # Σm 上限

# ───────────────────────── 分层规模表（10 组）─────────────────────────
LAYERS = {
    1: (20, "边界层：n≤10,m≤10,T=20；m=0/单边/全0/全1/欧拉/星形/匹配/多连通块"),
    2: (15, "边界层：n≤300,m≤3000,T=15；长链/大星形/全0/匹配/随机树的结构极值"),
    3: (15, "小规模随机：n≤300, m≤3000, c 随机/全1/稀疏"),
    4: (15, "小规模随机：n≤60 稠密图、多连通块、完全图边界"),
    5: (10, "中等规模：10×(n=5e4,m=5e4)，随机 c（Σn=Σm=5e5）"),
    6: (10, "全 c=1 顶格（题面第3测试点 sub-task 的极限版）：2×(n=m=2e5 全1) + 8×12500"),
    7: (10, "大规模：长链 n=2e5 全1（K=1 单路径）+ 长链稀疏 + 8×中等随机"),
    8: (10, "大规模·结构混合：大星形(大K)/大随机图/链森林/全0/多连通块"),
    9: (10, "顶格随机：2×(n=m=2e5 全1) + 8×(n=m=12500)（Σn=Σm=5e5）"),
    10: (10, "顶格·最坏结构：链2e5(单条长路径) + 星形2e5(K=1e5 最多路径数) + 混合"),
}


# ───────────────────────── 独立校验：理论最少人数 ─────────────────────────
def kmim(n, edges):
    """并查集 + 度奇偶统计，独立计算 K_min。"""
    p = list(range(n + 1))

    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    pdeg = [0] * (n + 1)
    for (a, b, c) in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            p[ra] = rb
        pdeg[a] ^= c
        pdeg[b] ^= c
    nT, hasS = {}, {}
    for (a, b, c) in edges:
        if c:
            hasS[find(a)] = True
    for v in range(1, n + 1):
        if pdeg[v]:
            r = find(v)
            nT[r] = nT.get(r, 0) + 1
    total = 0
    for r, cnt in nT.items():
        total += cnt // 2 if cnt > 0 else 0
    for r in hasS:
        if nT.get(r, 0) == 0:
            total += 1
    return total


# ───────────────────────── 工具 ─────────────────────────
def pick_c(cpat, rng):
    if cpat == "one":
        return 1
    if cpat == "zero":
        return 0
    if cpat == "few":
        return 1 if rng.random() < 0.08 else 0
    return rng.randint(0, 1)  # "rand50"


def relabel(n, edges, rng):
    """随机标签置换，去掉生成结构的编号痕迹；输出仍保证 a<b 排序。"""
    lab = list(range(1, n + 1))
    rng.shuffle(lab)
    lab = [0] + lab
    out = []
    for (a, b, c) in edges:
        x, y = lab[a], lab[b]
        out.append((x, y, c) if x < y else (y, x, c))
    return out


# ───────────────────────── 结构构造器 ─────────────────────────
def st_chain(n, cp, rng):
    return [(i, i + 1, pick_c(cp, rng)) for i in range(1, n)]


def st_star(n, cp, rng):
    return [(1, v, pick_c(cp, rng)) for v in range(2, n + 1)]


def st_matching(n, cp, rng):
    return [(2 * i - 1, 2 * i, pick_c(cp, rng)) for i in range(1, n // 2 + 1)]


def st_clique(k, cp, rng):
    return [(a, b, pick_c(cp, rng)) for a, b in combinations(range(1, k + 1), 2)]


def st_forest_chains(n, L, cp, rng):
    """n 个点拆成若干条长度 L 的链（剩余点孤立）。"""
    out, v = [], 1
    while v + L - 1 <= n:
        out += [(v + i, v + i + 1, pick_c(cp, rng)) for i in range(L - 1)]
        v += L
    return out


def st_rand_tree(n, cp, rng):
    return [(i, rng.randint(1, i - 1), pick_c(cp, rng)) for i in range(2, n + 1)]


def st_tree_plus(n, m, cp, rng):
    """连通图：随机树 + (m-n+1) 条额外随机边（无重边）。要求 n-1 <= m。"""
    if m < n - 1:
        raise ValueError("tree_plus 需要 m >= n-1")
    edges = st_rand_tree(n, cp, rng)
    # 注意：随机树的边是 (i, rand(1,i-1))，键必须归一到 (min,max) 才能正确去重
    used = {(min(a, b), max(a, b)) for (a, b, _) in edges}
    need = m - (n - 1)
    while need > 0:
        a, b = rng.randint(1, n), rng.randint(1, n)
        if a == b:
            continue
        key = (a, b) if a < b else (b, a)
        if key in used:
            continue
        used.add(key)
        edges.append((key[0], key[1], pick_c(cp, rng)))
        need -= 1
    return edges


def st_rand_graph(n, m, cp, rng):
    """随机简单图（可不连通）。稀疏用拒绝采样；稠密/接近完全图时枚举取子集。

    注意：枚举所有点对的稠密分支仅在 n ≤ 200 时启用（最多 19900 对），
    避免任何大 n 下的 O(n²) Python 循环。
    """
    if m <= 0:
        return []
    total = n * (n - 1) // 2
    if m > total:
        raise ValueError("m=%d 超过完全图边数 %d" % (m, total))
    if m * 3 <= total:
        used = set()
        while len(used) < m:
            a, b = rng.randint(1, n), rng.randint(1, n)
            if a == b:
                continue
            used.add((a, b) if a < b else (b, a))
        return [(a, b, pick_c(cp, rng)) for (a, b) in used]
    assert n <= 200, "稠密采样仅支持 n<=200（避免 O(n^2) 枚举）"
    allp = list(combinations(range(1, n + 1), 2))
    rng.shuffle(allp)
    return [(a, b, pick_c(cp, rng)) for (a, b) in allp[:m]]


# ───────────────────────── 各组 case 规格 ─────────────────────────
def build_case_specs(t, rng):
    specs = []

    def add(n, edges, note):
        specs.append((n, relabel(n, edges, rng) if edges else [], note))

    if t == 1:
        add(1, [], "n=1,m=0 空图 → K=0")
        add(2, [], "n=2,m=0 无边 → K=0")
        add(2, [(1, 2, 1)], "单边 c=1 → K=1")
        add(2, [(1, 2, 0)], "单边 c=0 → K=0")
        add(5, st_chain(5, "one", rng), "链全1：T={1,5} → K=1")
        add(5, st_chain(5, "zero", rng), "链全0 → K=0")
        add(3, st_clique(3, "one", rng), "三角全1：全偶度且 S≠∅ → K=1(欧拉)")
        add(4, st_star(4, "one", rng), "星形全1：T=全部4点 → K=2")
        add(5, [(1, 2, 1), (3, 4, 1)], "两条不连通单边 → K=2")
        add(6, [(1, 2, 1), (3, 4, 1), (5, 6, 1)], "三条不连通单边 → K=3")
        add(5, st_clique(5, "one", rng), "K5 全1(m=10)：全偶度 → K=1")
        add(6, st_clique(4, "one", rng), "K4 全1 + 2 个孤立点 → K=1")
        add(10, st_chain(10, "one", rng), "10 点链全1 → K=1, l=10")
        add(10, st_star(10, "one", rng), "10 点星全1 → K=5")
        add(7, st_forest_chains(7, 3, "one", rng), "两条长度3的链全1 → K=2")
        add(10, st_clique(5, "zero", rng), "K5 全0 → K=0")
        add(10, st_rand_graph(10, 10, "rand50", rng), "n=m=10 随机 c")
        add(10, st_rand_graph(10, 10, "one", rng), "n=m=10 全1")
        add(9, st_rand_tree(9, "rand50", rng), "n=9 随机树随机 c")
        add(8, st_star(8, "few", rng), "8 点星形 c 稀疏为1")
    elif t == 2:
        add(300, st_chain(300, "one", rng), "n=300 长链全1 → K=1, l=300")
        add(300, st_chain(300, "zero", rng), "n=300 长链全0 → K=0")
        add(300, st_star(300, "one", rng), "n=300 星形全1 → K=150")
        add(300, st_star(300, "zero", rng), "n=300 星形全0 → K=0")
        add(300, st_matching(300, "one", rng), "n=300 150 条匹配边全1 → K=150")
        add(300, st_chain(300, "one", rng)[:-1], "n=300 链去掉末边：T={1,299} → K=1")
        add(300, st_rand_tree(300, "one", rng), "n=300 随机树全1，K=|T|/2")
        add(300, st_rand_tree(300, "rand50", rng), "n=300 随机树随机 c")
        add(300, st_rand_graph(300, 3000, "rand50", rng), "n=300,m=3000 随机 c")
        add(300, st_rand_graph(300, 3000, "one", rng), "n=300,m=3000 全1")
        add(300, st_rand_graph(300, 3000, "zero", rng), "n=300,m=3000 全0 → K=0")
        add(300, [(1, 2, 1)], "单边 + 298 个孤立点 → K=1")
        add(300, st_tree_plus(300, 500, "one", rng), "连通图(树+201边)全1")
        add(300, st_forest_chains(300, 10, "one", rng), "30 条长度10的链全1 → K=30")
        add(300, st_rand_graph(300, 299, "few", rng), "森林规模稀疏，c 少量为1")
    elif t == 3:
        for i in range(15):
            n = rng.randint(10, 300)
            mmax = min(3000, n * (n - 1) // 2)
            m = rng.randint(min(n - 1, mmax), mmax)
            cp = ["rand50", "one", "few"][i % 3]
            add(n, st_rand_graph(n, m, cp, rng), "随机 n=%d m=%d c=%s" % (n, m, cp))
    elif t == 4:
        for i in range(15):
            n = rng.randint(2, 60)
            mmax = min(3000, n * (n - 1) // 2)
            if i % 3 == 0:
                m = max(mmax // 2, n - 1) if mmax >= n - 1 else mmax
                add(n, st_tree_plus(n, min(m, mmax), "rand50", rng),
                    "连通稠密 n=%d m=%d" % (n, min(m, mmax)))
            elif i % 3 == 1:
                add(n, st_rand_graph(n, mmax, "one", rng), "完全图 n=%d 全1" % n)
            else:
                add(n, st_rand_graph(n, max(0, mmax - rng.randint(1, 3)), "rand50", rng),
                    "近完全图 n=%d" % n)
    elif t == 5:
        for i in range(10):
            n = m = 50000
            cp = ["rand50", "one", "few"][i % 3]
            if i % 4 == 0:
                add(n, st_tree_plus(n, m, cp, rng), "连通 n=m=5e4 c=%s" % cp)
            else:
                add(n, st_rand_graph(n, m, cp, rng), "随机 n=m=5e4 c=%s" % cp)
    elif t == 6:
        # 对应题面第 3 个测试点（c_i=1 子任务，n≤2e5, m=2e5, T=10）的顶格版本
        for i in range(2):
            add(200000, st_rand_graph(200000, 200000, "one", rng),
                "顶格 n=m=2e5 全1 随机（第%d组）" % (i + 1))
        for i in range(8):
            n = m = 12500
            if i % 2 == 0:
                add(n, st_tree_plus(n, m, "one", rng), "连通 n=m=12500 全1")
            else:
                add(n, st_rand_graph(n, m, "one", rng), "随机 n=m=12500 全1")
    elif t == 7:
        add(200000, st_chain(200000, "one", rng), "n=2e5 链全1 → K=1，单路径 l=2e5")
        add(200000, st_chain(200000, "few", rng), "n=2e5 链稀疏c → K 中等")
        for i in range(8):
            n = m = 12500
            cp = ["rand50", "one", "few"][i % 3]
            add(n, st_rand_graph(n, m, cp, rng), "随机 n=m=12500 c=%s" % cp)
    elif t == 8:
        add(100000, st_star(100000, "one", rng), "n=1e5 星全1 → K=5e4（大 K）")
        add(100000, st_rand_graph(100000, 100000, "rand50", rng), "随机 n=m=1e5")
        add(50000, st_matching(50000, "one", rng), "n=5e4 匹配全1 → K=2.5e4")
        add(50000, st_forest_chains(50000, 5, "one", rng), "n=5e4 链森林全1")
        for i in range(6):
            n = m = 33333
            cp = ["rand50", "one", "few", "zero"][i % 4]
            if i % 3 == 0:
                add(n, st_tree_plus(n, m, cp, rng), "连通 n=m=33333 c=%s" % cp)
            else:
                add(n, st_rand_graph(n, m, cp, rng), "随机 n=m=33333 c=%s" % cp)
    elif t == 9:
        for i in range(2):
            add(200000, st_rand_graph(200000, 200000, "one", rng),
                "顶格 n=m=2e5 全1 随机（第%d组）" % (i + 1))
        for i in range(8):
            n = m = 12500
            cp = ["rand50", "one", "few"][i % 3]
            add(n, st_rand_graph(n, m, cp, rng), "随机 n=m=12500 c=%s" % cp)
    elif t == 10:
        add(200000, st_chain(200000, "one", rng),
            "链 n=2e5 全1 → K=1，单条路径 l=2e5（长行/输出缓冲压力）")
        add(200000, st_star(200000, "one", rng),
            "星 n=2e5 全1 → K=1e5（最多路径条数）")
        for i in range(8):
            n = m = 12500
            cp = ["rand50", "one", "few"][i % 3]
            add(n, st_rand_graph(n, m, cp, rng), "随机 n=m=12500 c=%s" % cp)
    else:
        raise ValueError("未知测试点 %d" % t)
    return specs


def gen_point(t, rng):
    t_count, note = LAYERS[t]
    specs = build_case_specs(t, rng)
    if len(specs) != t_count:
        raise SystemExit("测试点 %d: case 数 %d != 题面 T=%d" % (t, len(specs), t_count))
    # 每题点各自的规模上限（按题面表）
    cap_n, cap_m = (10, 10) if t == 1 else (300, 3000) if t == 2 else (MAX_N, MAX_M)
    sum_n = sum(n for (n, _, _) in specs)
    sum_m = sum(len(e) for (_, e, _) in specs)
    assert sum_n <= SUM_N, "Σn=%d 超上限 %d" % (sum_n, SUM_N)
    assert sum_m <= SUM_M, "Σm=%d 超上限 %d" % (sum_m, SUM_M)
    for (n, e, _) in specs:
        assert n <= cap_n, "点%d: 单组 n=%d 超该点上限 %d" % (t, n, cap_n)
        assert len(e) <= cap_m, "点%d: 单组 m=%d 超该点上限 %d" % (t, len(e), cap_m)
        assert len({(a, b) for (a, b, _) in e}) == len(e), "存在重边"
        assert all(1 <= a < b <= n for (a, b, _) in e), "边端点越界/顺序错"
        assert all(c in (0, 1) for (_, _, c) in e), "c 取值超范围"

    io = IO(file_prefix="problem", data_id=t)
    text = [str(t_count)]
    for (n, edges, _) in specs:
        text.append("%d %d" % (n, len(edges)))
        text += ["%d %d %d" % e for e in edges]
    io.input_write("\n".join(text) + "\n")

    exp_ks = [kmim(n, e) for (n, e, _) in specs]
    io.output_gen(STD_PATH)
    # cyaron 的 output_file 是带缓冲的文件对象，必须先 flush 再校验
    io.output_file.flush()
    io.input_file.flush()

    outp = "problem%d.out" % t
    assert os.path.exists(outp), "%s 未生成" % outp
    assert os.path.getsize(outp) > 0, "%s 为空（std 未产出？）" % outp
    # 逐 case 校验结构：每个 case 为 "K" + K 行路径
    with open(outp, "r") as f:
        lines = f.read().split("\n")
    li = 0
    tot_l = 0
    for ci, exp_k in enumerate(exp_ks):
        while li < len(lines) and lines[li].strip() == "":
            li += 1
        assert li < len(lines), "%s: case %d 缺少 K 行" % (outp, ci)
        got_k = int(lines[li].strip())
        li += 1
        assert got_k == exp_k, "%s: case %d std K=%d != 理论 K_min=%d" % (outp, ci, got_k, exp_k)
        for pi in range(got_k):
            assert li < len(lines), "%s: case %d 路径行不足" % (outp, ci)
            p = lines[li].split()
            li += 1
            assert len(p) >= 2, "%s: 路径格式错误 %r" % (outp, lines[li - 1][:60])
            lv = int(p[0])
            assert lv >= 1, "%s: 出现 l=0 的非法路径" % outp
            assert lv == len(p) - 1, "%s: l 与顶点数不符: %r" % (outp, lines[li - 1][:60])
            for x in p[1:]:
                assert 1 <= int(x) <= specs[ci][0], "%s: 顶点编号越界" % outp
            tot_l += lv
    left = [x for x in lines[li:] if x.strip() != ""]
    assert not left, "%s: 多出 %d 行输出" % (outp, len(left))
    assert tot_l <= 5000000, "%s: Σl=%d 超过题面限制 5e6" % (outp, tot_l)
    print("[point %2d] T=%2d Σn=%-7d Σm=%-7d ΣK=%-7d Σl=%-8d | %s"
          % (t, t_count, sum_n, sum_m, sum(exp_ks), tot_l, note))


def main():
    which = [int(x) for x in sys.argv[1:]] or list(range(1, 11))
    rng = random.Random(1740)
    for t in which:
        gen_point(t, rng)


main()
