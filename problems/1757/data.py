#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1757《避难向导》分层测试数据生成器
# ---------------------------------------------------------------------------
# 用法：
#   nice -n 19 g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && nice -n 19 timeout 600 python3 ../data.py
#
# 题意：树 n 点（1 号首都），边带权；叶子（度=1）称边境城市。
#   d_i = i 到最远边境城市的距离；S_i = (d_i + a) * b mod c。
#   m 次询问 (x,y,q)：x→y 唯一路径上离 x 最近且 S>=q 的城市编号，无则 -1。
#
# 数据范围（题面【数据规模及提示】）：
#   0 < x_i, y_i <= n；a, b, c, q_i <= 1,000,000；n <= 100,000；m <= 300,000。
#   子任务：1-5 n,m<=100（a,b,c<10000）；6-7 n,m<=1000；8-10 n<=1e5,m<=100；
#          11-12 n<=1e5,m<=1e4；13-15 n<=1e5,m<=1e5 且所有 y_i 相等；
#          16-20 n<=1e5,m<=3e5。
#   限制 time 1000 ms / memory 128 MB（config.json）。
#
# ---- 分层策略（10 组，覆盖 边界/小/中/大/顶格）----
#   点 1  边界层：n=1（退化：无边，唯一城市度 0；按各公开实现约定 d_1=0），m=1。
#   点 2  边界层：n=2（最小非退化树，两点皆为边境城市），m=2。
#   点 3  边界层/回归：题面【输入样例】原样（n=7,m=6,a=5,b=6,c=20），逐字节回归。
#   点 4  小规模：n=m=100，随机树，a,b,c<10000（子任务 1-5）。
#   点 5  小规模 + 最坏深度：n=m=100，链（深度 99），a,b,c<10000。
#   点 6  中等规模：n=m=1000，随机树（子任务 6-7）。
#   点 7  中等规模 + 最坏深度：n=m=1000，链（深度 999）。
#   点 8  大规模 n / 小 m：n=100000, m=100，随机树（子任务 8-10）。
#   点 9  子任务 13-15：n=100000, m=100000，所有 y_i 相等，链结构（最深）。
#   点 10 顶格：n=100000, m=300000，随机树，边权/参数/q 全顶格 1e6（子任务 16-20）。
#
# 生成要点：
#   * 全部 O(n) / O(m) 线性构造，无 O(n^2) 的 Python 循环。
#   * 固定随机种子，冷启动两次结果一致。
#   * .out 一律用 subprocess 显式跑 std 产出（规避 cyaron output_gen 写缓冲不 flush
#     导致 0 字节 .out 的坑），并断言 .in 非空、.out 行数 == m。
# ---------------------------------------------------------------------------
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
DATA = os.path.join(HERE, "data")

MAXW = 10 ** 6          # 边权顶格（题面未给上界，取与参数同量级的 1e6，压 64 位中间量）
MAXP = 10 ** 6          # a, b, c, q 顶格


def rand_tree(n, rng, maxw, shuffle_edges=True):
    """O(n) 随机树（随机递归树 + 随机重标号），返回边表。"""
    if n <= 1:
        return []
    lab = list(range(1, n + 1))
    rng.shuffle(lab)
    edges = []
    for i in range(2, n + 1):
        p = rng.randint(1, i - 1)
        u, v = lab[p - 1], lab[i - 1]
        edges.append((u, v, rng.randint(1, maxw)))
    if shuffle_edges:
        rng.shuffle(edges)
    return edges


def chain(n, rng, maxw):
    """O(n) 链 1-2-...-n（最坏深度，压 LCA / 倍增）。"""
    return [(i - 1, i, rng.randint(1, maxw)) for i in range(2, n + 1)]


def gen_queries(m, n, rng, maxq, fix_y=None):
    """O(m) 询问。fix_y 给定则所有 y_i 相等（子任务 13-15）。"""
    out = []
    for _ in range(m):
        x = rng.randint(1, n)
        y = fix_y if fix_y is not None else rng.randint(1, n)
        out.append((x, y, rng.randint(1, maxq)))
    return out


def build_cases():
    cases = []

    # 点 1：n=1 退化边界
    cases.append(dict(idx=1, n=1, m=1, a=1, b=1, c=1000,
                      edges=[], queries=[(1, 1, 1)],
                      note="边界层：n=1 退化（无边，d_1=0），m=1"))

    # 点 2：n=2 最小非退化
    r2 = random.Random(175702)
    cases.append(dict(idx=2, n=2, m=2, a=3, b=7, c=9999,
                      edges=[(1, 2, 1000000)],
                      queries=[(1, 2, 1), (2, 1, 999999)],
                      note="边界层：n=2 最小非退化树（两点皆边境），边权顶格 1e6"))

    # 点 3：题面样例原样（回归）
    cases.append(dict(
        idx=3, n=7, m=6, a=5, b=6, c=20,
        edges=[(1, 2, 4), (2, 4, 2), (2, 5, 3), (1, 3, 5), (3, 6, 6), (6, 7, 7)],
        queries=[(7, 5, 15), (3, 4, 5), (5, 4, 2), (4, 5, 2), (6, 6, 10), (3, 5, 19)],
        note="边界层/回归：题面【输入样例】原样，逐字节回归"))

    # 点 4：小规模随机树
    r4 = random.Random(175704)
    cases.append(dict(idx=4, n=100, m=100, a=9999, b=9998, c=9997,
                      edges=rand_tree(100, r4, 9999),
                      queries=gen_queries(100, 100, r4, 9999),
                      note="小规模：n=m=100 随机树，a,b,c<10000"))

    # 点 5：小规模链（最坏深度）
    r5 = random.Random(175705)
    cases.append(dict(idx=5, n=100, m=100, a=1, b=9973, c=10000 - 1,
                      edges=chain(100, r5, 9999),
                      queries=gen_queries(100, 100, r5, 9999),
                      note="小规模+最坏深度：n=m=100 链（深度 99），a,b,c<10000"))

    # 点 6：中等规模随机树
    r6 = random.Random(175706)
    cases.append(dict(idx=6, n=1000, m=1000, a=123456, b=654321, c=1000000,
                      edges=rand_tree(1000, r6, MAXW),
                      queries=gen_queries(1000, 1000, r6, MAXP),
                      note="中等规模：n=m=1000 随机树"))

    # 点 7：中等规模链（最坏深度）
    r7 = random.Random(175707)
    cases.append(dict(idx=7, n=1000, m=1000, a=1, b=1, c=1000000,
                      edges=chain(1000, r7, MAXW),
                      queries=gen_queries(1000, 1000, r7, MAXP),
                      note="中等规模+最坏深度：n=m=1000 链（深度 999）"))

    # 点 8：大 n 小 m
    r8 = random.Random(175708)
    cases.append(dict(idx=8, n=100000, m=100, a=999983, b=999979, c=999961,
                      edges=rand_tree(100000, r8, MAXW),
                      queries=gen_queries(100, 100000, r8, MAXP),
                      note="大规模 n / 小 m：n=100000, m=100 随机树（子任务 8-10）"))

    # 点 9：所有 y_i 相等 + 链
    r9 = random.Random(175709)
    cases.append(dict(idx=9, n=100000, m=100000, a=999999, b=999998, c=999997,
                      edges=chain(100000, r9, MAXW),
                      queries=gen_queries(100000, 100000, r9, MAXP, fix_y=100000),
                      note="子任务 13-15：n=m=100000，所有 y_i=100000，链结构（最深）"))

    # 点 10：顶格
    r10 = random.Random(175710)
    cases.append(dict(idx=10, n=100000, m=300000, a=999999, b=999983, c=1000000,
                      edges=rand_tree(100000, r10, MAXW),
                      queries=gen_queries(300000, 100000, r10, MAXP),
                      note="顶格：n=100000, m=300000 随机树，边权/参数/q 全顶格 1e6（子任务 16-20）"))

    return cases


def write_case(c):
    os.makedirs(DATA, exist_ok=True)
    inpath = os.path.join(DATA, "problem%d.in" % c["idx"])
    outpath = os.path.join(DATA, "problem%d.out" % c["idx"])

    n, m = c["n"], c["m"]
    assert len(c["edges"]) == n - 1, "点 %d 边数 %d != n-1" % (c["idx"], len(c["edges"]))
    assert len(c["queries"]) == m, "点 %d 询问数 %d != m" % (c["idx"], len(c["queries"]))
    for (u, v, w) in c["edges"]:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW
    for (x, y, q) in c["queries"]:
        assert 1 <= x <= n and 1 <= y <= n and 1 <= q <= MAXP

    with open(inpath, "w", buffering=1 << 20) as f:
        f.write("%d %d %d %d %d\n" % (n, m, c["a"], c["b"], c["c"]))
        f.write("".join("%d %d %d\n" % e for e in c["edges"]))
        f.write("".join("%d %d %d\n" % t for t in c["queries"]))

    insize = os.path.getsize(inpath)
    assert insize > 0, "点 %d 的 .in 为空！" % c["idx"]

    with open(inpath, "rb") as fin, open(outpath, "wb") as fout:
        subprocess.run([STD], stdin=fin, stdout=fout, check=True, timeout=120)

    outsize = os.path.getsize(outpath)
    assert outsize > 0, "点 %d 的 .out 为 0 字节（std 写缓冲未 flush？）" % c["idx"]
    with open(outpath, "rb") as f:
        lines = f.read().split(b"\n")
    assert lines and lines[-1] == b"", "点 %d 的 .out 末行无换行" % c["idx"]
    lines = lines[:-1]
    assert len(lines) == m, "点 %d 的 .out 行数 %d != m=%d" % (c["idx"], len(lines), m)
    for ln in lines:
        assert ln.lstrip(b"-").isdigit() and (ln == b"-1" or ln.isdigit()), \
            "点 %d 的 .out 含非法行 %r" % (c["idx"], ln)

    # 非退化自检：至少有一个非 -1 答案；m>=2 时答案至少 2 种
    neg = sum(1 for ln in lines if ln == b"-1")
    assert neg < m, "点 %d 的 .out 全为 -1（参数退化，无区分度）" % c["idx"]
    if m >= 2:
        assert len(set(lines)) >= 2, "点 %d 的 .out 答案单一（无区分度）" % c["idx"]
    # b 与 c 不应成倍数关系，否则 S 恒为 0
    assert c["b"] % c["c"] != 0, "点 %d 的 b 是 c 的倍数 → S 恒为 0" % c["idx"]

    print("problem%-2d: n=%-6d m=%-6d in=%dB out=%dB -- %s"
          % (c["idx"], n, m, insize, outsize, c["note"]))


def main():
    if not os.path.exists(STD):
        print("ERROR: 未找到标程 %s，请先编译 std.cpp" % STD, file=sys.stderr)
        sys.exit(1)
    cases = build_cases()
    assert len(cases) == 10, "必须恰好 10 个测试点"
    assert sorted(c["idx"] for c in cases) == list(range(1, 11))
    for c in cases:
        write_case(c)
    print("OK: 10 组分层数据生成完毕（.in/.out 成对，行数已断言）")


if __name__ == "__main__":
    main()
