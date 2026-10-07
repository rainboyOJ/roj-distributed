#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1761《最小割》数据生成器（ROJ 题号 1761）
#
# 题面（见同目录 content.md）：
#   给无向无权简单图 G（N 个点 M 条边，无重边无自环），T 是 G 的一棵生成树。
#   求「恰好只含 T 中一条边」的最小割的边数（即删去这些边后图不连通的两部分，
#   且这些边中恰好有一条属于 T）。
#   输入：第一行 T0（数据组数，T0<=5）；每组第一行 N M（N<=20000, M<=200000），
#         随后 N-1 行是 T 的树边，再随后 M-N+1 行是 G 中不在 T 中的边。
#   输出：每组一行，答案。
#
# 数据范围（题面【提示】）：100% 数据 N<=20000，M<=200000；组数 T0<=5。
#   本生成器按题面上限生成，不做任何"缩水上限"（点数/边数/组数均顶到题面上限）。
#
# 分层设计（10 组，边界 → 小 → 中 → 大 → 顶格）：
#   点 1  边界最小：T0=1, N=2, M=1（T 只有一条边、无非树边）→ 答案恒为 1（手算断言）
#   点 2  边界最小+1：T0=1, N=3, M=3（链 1-2-3 + 非树边 1-3）→ 答案恒为 2（手算断言）
#   点 3  小规模随机：N=20, M=40（随机树 + 随机非树边）
#   点 4  小规模稠密：N=60, M=600（接近完全图密度，割往往很小）
#   点 5  中等随机树：N=500, M=3000
#   点 6  中等深链树：N=2000, M=20000（树为链，深度 2000，压 LCA 深度处理）
#   点 7  大星形树：N=5000, M=50000（树为星，深度 1，割结构退化）
#   点 8  顶格链树：N=20000, M=200000（树为链，深度 20000，最坏深度 + 顶格规模）
#   点 9  顶格随机树：N=20000, M=200000（随机父节点树，顶格规模）
#   点 10 多组顶格：T0=5，每组 N=20000, M=200000（合计 10^6 条边，压满组数×规模）
#        —— 5 组分别用 链 / 星 / 随机树 / 链(重标号) / 随机树(重标号)，覆盖结构多样性
#
# 覆盖点说明：
#   - 组数分层：T0=1（点 1-9）与 T0=5 顶格（点 10）两端都覆盖。
#   - 树形状：链（深、LCA 最坏）/ 星（浅）/ 随机（一般）三类全覆盖。
#   - 非树边数量：0（点 1，答案退化为 1）/ 1（点 2）/ 大量（其余）。
#   - 节点标号：部分测试点做随机重标号，避免"父节点编号必小于子节点"这类
#     只在标号有序时才成立的错误实现蒙对。
#
# 实现要点（针对 cyaron output_gen 不 flush 的隐患）：
#   - **不使用** IO.output_gen()，改为把 .in 写盘后由 subprocess 显式调用 work/std，
#     stdout 重定向写入 .out，再断言 .out 非空且行数 == 组数（本题每组必有解，
#     不存在无解空输出点），并逐行断言答案为 >=1 的整数。
#   - 随机性：每个测试点使用独立的 random.Random(1761 + 点号)，可精确复现。
#   - 生成复杂度：大点用 O(M) 的随机采样 + set 去重（拒绝采样），小点用
#     itertools.combinations（C 层实现）枚举候选边后随机采样，**无 O(n^2) Python 循环**。

import itertools
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "work", "std")

MAXN = 20000     # 题面上限：点数
MAXM = 200000    # 题面上限：边数
MAXT = 5         # 题面上限：组数


def build_tree(n, shape, rng):
    """生成一棵 n 点生成树的边表（编号 1..n），按 shape 选择形状。"""
    edges = []
    if shape == "chain":
        for i in range(2, n + 1):
            edges.append((i - 1, i))
    elif shape == "star":
        for i in range(2, n + 1):
            edges.append((1, i))
    elif shape == "random":
        for i in range(2, n + 1):
            edges.append((rng.randint(1, i - 1), i))
    else:
        raise ValueError("unknown shape: %s" % shape)
    return edges


def relabel(edges, n, rng):
    """随机重标号：把 1..n 随机置换，避免标号有序被错误实现利用。"""
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    return [(perm[u - 1], perm[v - 1]) for (u, v) in edges]


def extra_edges(n, tree_edges, need, rng):
    """生成 need 条不在 T 中、无重边无自环的边（1<=u,v<=n）。"""
    tree_set = set((min(u, v), max(u, v)) for (u, v) in tree_edges)
    assert need >= 0, "非树边条数不能为负（需 M >= N-1）"
    if need == 0:
        return []
    max_pairs = n * (n - 1) // 2
    assert len(tree_set) + need <= max_pairs, \
        "M 超出简单图上限 N(N-1)/2"
    out = []
    if n <= 200:
        # 小规模：枚举全部候选对（itertools.combinations 为 C 层实现，无 Python O(n^2) 循环）
        avail = [(u, v) for (u, v) in itertools.combinations(range(1, n + 1), 2)
                 if (u, v) not in tree_set]
        out = rng.sample(avail, need)
    else:
        seen = set(tree_set)
        while len(out) < need:
            u = rng.randint(1, n)
            v = rng.randint(1, n)
            if u == v:
                continue
            key = (min(u, v), max(u, v))
            if key in seen:
                continue
            seen.add(key)
            out.append(key)
    assert len(out) == need
    for (u, v) in out:
        assert u != v and (min(u, v), max(u, v)) not in tree_set
    return out


def make_case(n, m, shape, rng, shuffle_labels=False):
    """返回 (n, m, tree_edges, non_tree_edges)。"""
    assert 1 <= n <= MAXN, "N 超出题面上限"
    assert n - 1 <= m <= MAXM, "M 必须满足 N-1 <= M <= 200000"
    assert m <= n * (n - 1) // 2, "M 超出简单图上限 N(N-1)/2"
    tree = build_tree(n, shape, rng)
    if shuffle_labels:
        tree = relabel(tree, n, rng)
    non = extra_edges(n, tree, m - (n - 1), rng)
    if shuffle_labels:
        rng.shuffle(tree)
        rng.shuffle(non)
    return n, m, tree, non


def gen(idx, cases, note):
    """写 data/problem{idx}.in，用 std 显式产出 .out，并断言 .out 合法。"""
    rng = random.Random(1761 + idx)
    os.makedirs(DATA_DIR, exist_ok=True)
    in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
    out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)

    built = []
    for (n, m, shape, shuffle_labels) in cases:
        built.append(make_case(n, m, shape, rng, shuffle_labels))

    lines = ["%d" % len(built)]
    for (n, m, tree, non) in built:
        lines.append("%d %d" % (n, m))
        for (u, v) in tree:
            lines.append("%d %d" % (u, v))
        for (u, v) in non:
            lines.append("%d %d" % (u, v))
    with open(in_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    # 显式跑 std 产出 .out（规避 cyaron output_gen 不 flush 的 0 字节隐患）
    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        subprocess.run([STD], stdin=fin, stdout=fout, check=True)

    assert os.path.getsize(in_path) > 0, "problem%d.in 为空" % idx
    assert os.path.getsize(out_path) > 0, "problem%d.out 为空（本题每组必有解）" % idx
    with open(out_path) as f:
        outs = [ln.strip() for ln in f if ln.strip() != ""]
    assert len(outs) == len(built), \
        "problem%d.out 行数 %d != 组数 %d" % (idx, len(outs), len(built))
    for s in outs:
        assert s.lstrip("-").isdigit(), "problem%d.out 出现非整数行: %r" % (idx, s)
        assert int(s) >= 1, "problem%d.out 出现 <1 的答案: %s" % (idx, s)

    total_edges = sum(c[1] for c in built)
    print("problem%-2d: T0=%-2d N=%-6s M=%-7s 合计边=%-8d 答案=%s  -- %s"
          % (idx, len(built),
             "/".join(str(c[0]) for c in built[:5]),
             "/".join(str(c[1]) for c in built[:5]),
             total_edges, ",".join(outs), note))
    return outs


def main():
    if not os.path.exists(STD):
        sys.exit("未找到标程可执行文件 %s（请先编译 std.cpp 到 work/std）" % STD)

    # ---- 点 1-2：边界层（手算可断言的极小结构） ----
    o1 = gen(1, [(2, 1, "chain", False)],
             "边界最小：N=2,M=1，T 仅一条边且无非树边 → 割只能是 {1-2}，答案 1")
    assert o1 == ["1"], "点 1 期望答案 1，实得 %s" % o1

    o2 = gen(2, [(3, 3, "chain", False)],
             "边界最小+1：N=3 三角形（链 1-2-3 + 非树边 1-3）→ 最小割 2（如 {2-3,1-3}）")
    assert o2 == ["2"], "点 2 期望答案 2，实得 %s" % o2

    # ---- 点 3-4：小规模 ----
    gen(3, [(20, 40, "random", False)],
        "小规模随机：N=20,M=40，随机树 + 随机非树边")
    gen(4, [(60, 600, "random", False)],
        "小规模稠密：N=60,M=600（接近完全图，割通常很小）")

    # ---- 点 5-7：中等规模（形状分层：随机 / 深链 / 星） ----
    gen(5, [(500, 3000, "random", False)],
        "中等随机树：N=500,M=3000")
    gen(6, [(2000, 20000, "chain", False)],
        "中等深链树：N=2000,M=20000，树深度 2000（压 LCA 深度处理）")
    gen(7, [(5000, 50000, "star", False)],
        "大星形树：N=5000,M=50000，深度 1（割结构退化）")

    # ---- 点 8-9：顶格规模 ----
    gen(8, [(MAXN, MAXM, "chain", False)],
        "顶格链树：N=20000,M=200000，深度 20000（最坏深度 + 顶格规模）")
    gen(9, [(MAXN, MAXM, "random", True)],
        "顶格随机树：N=20000,M=200000，随机重标号")

    # ---- 点 10：组数顶格（T0=5，每组均顶格规模，合计 10^6 条边） ----
    gen(10, [(MAXN, MAXM, "chain", False),
             (MAXN, MAXM, "star", False),
             (MAXN, MAXM, "random", False),
             (MAXN, MAXM, "chain", True),
             (MAXN, MAXM, "random", True)],
        "组数顶格：T0=5，每组 N=20000,M=200000（链/星/随机/链重标号/随机重标号）")

    print("全部 10 组数据生成完毕，.out 行数/取值/非空断言全部通过。")


if __name__ == "__main__":
    main()
