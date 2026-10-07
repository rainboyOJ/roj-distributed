#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1764《社会送温暖》分层测试数据生成器（目标 ROJ 1764）
#
# 用法：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（【提示】明文）：
#     1 <= n, q <= 1e5 ; 1 <= P <= 1e7 ; 0 <= A_i, d, a <= 2^31
#     20% n,q<=1000 ; 40% n,q<=10000 ; 另有 30% 树是一条链。
#
# 说明：本脚本 **不用** cyaron 的 output_gen（其写缓冲不 flush 会产出 0 字节 .out），
#       而是用 subprocess 显式运行 std 产出 .out，并断言 .out 行数 == 询问次数
#       （有询问时 .out 必须非空、每行必须是整数）。
#
# ---- 分层策略（10 组，从最小铺到顶格）----
#   点 1  样例层：题面【输入样例】原样（n=q=5, P=29311），可对答案 15488。
#   点 2  边界层：n=1（无边的退化树）+ P=1（任意模 1 恒 0）+ 三种操作各一。
#   点 3  边界/小：n=10, q=20, P=6（偶数合数，检验“不能对 2 求逆元”的取模正确性），
#         五种操作全覆盖，含 u=v、u=1/v=n 边界。
#   点 4  小规模链：n=q=1000（20% 子任务上限），P=997（奇素数），值域小，便于手算量级。
#   点 5  小规模随机树：n=q=1000（20% 子任务上限），P=1e7（题面上限），值域 2^31。
#   点 6  中等随机树：n=q=10000（40% 子任务上限），P=1000000（偶数合数），值域 2^31。
#   点 7  中等链·询问为主：n=q=10000，P=9999991，询问占比 0.8（输出量大）。
#   点 8  大·多链段：n=q=1e5，完全二叉树（路径拆成 O(log n) 段，压 HLD），P=1e7，值域 2^31。
#   点 9  顶格随机树：n=q=1e5，P=1e7，a/d/A_i 全部取 2^31（值域顶格）。
#   点 10 顶格链：n=q=1e5 单链（30% 子任务性质 + 最深结构），P=1e7，a/d/A_i 全部取 2^31。
#
# 随机性：每点使用独立 Random(176400 + 点号)，与调用顺序无关、可精确复现。

import os
import random
import subprocess

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")

A_MAX = 1 << 31        # 2^31 = 2147483648（题面上限）
P_MAX = 10 ** 7        # 题面上限

STATS = []             # (idx, n, q, nq, note)


# ---------------- 树的生成（全部 O(n)） ----------------
def gen_tree(n, kind, rnd):
    """返回 n-1 条边 (u,v)，节点编号 1..n。"""
    edges = []
    if kind == "chain":
        for i in range(2, n + 1):
            edges.append((i - 1, i))
    elif kind == "star":
        for i in range(2, n + 1):
            edges.append((1, i))
    elif kind == "bin":              # 完全二叉树（堆形）
        for i in range(2, n + 1):
            edges.append((i // 2, i))
    elif kind == "random":           # 随机递归树
        for i in range(2, n + 1):
            edges.append((rnd.randint(1, i - 1), i))
    else:
        raise ValueError(kind)
    if kind in ("random", "bin"):
        # 随机重标号，去掉“父<子”的结构偏置
        perm = list(range(1, n + 1))
        rnd.shuffle(perm)
        perm = [0] + perm
        edges = [(perm[u], perm[v]) for (u, v) in edges]
    return edges


# ---------------- 操作序列 ----------------
def gen_ops(q, n, rnd, p_query, vmax, boundary=False):
    """生成 q 条操作；返回 (lines, 询问条数)。"""
    lines = []
    nq = 0
    for i in range(q):
        if boundary and i < 6:       # 前若干条强制边界（u=v / 端点）
            u, v = [(1, n), (n, 1), (1, 1), (n, n), (n // 2, n), (1, n // 2)][i]
            op = (1, 2, 3, 4, 5, 1)[i]
        else:
            op = 5 if rnd.random() < p_query else rnd.randint(1, 4)
            u = rnd.randint(1, n)
            v = rnd.randint(1, n)
        if op == 5:
            lines.append("5 %d %d" % (u, v))
            nq += 1
        elif op in (1, 3):
            lines.append("%d %d %d %d %d" % (op, u, v, rnd.randint(0, vmax), rnd.randint(0, vmax)))
        else:
            lines.append("%d %d %d %d" % (op, u, v, rnd.randint(0, vmax)))
    return lines, nq


# ---------------- 输出 ----------------
def emit(idx, n, q, P, edges, init, ops, nq, note):
    # 询问数一律以最终 ops 为准（调用方可能改写若干条 op）
    nq = sum(1 for o in ops if o[0] == "5")
    assert len(edges) == n - 1, "point %d: 边数 %d != n-1" % (idx, len(edges))
    assert len(init) == n, "point %d: 初值个数 != n" % idx
    assert len(ops) == q, "point %d: 操作数 != q" % idx
    assert 1 <= P <= P_MAX, "point %d: P 越界" % idx
    for x in init:
        assert 0 <= x <= A_MAX, "point %d: A_i 越界" % idx

    lines = ["%d %d %d" % (n, q, P)]
    lines += ["%d %d" % (u, v) for (u, v) in edges]
    lines += [" ".join(str(x) for x in init)]
    lines += ops
    content = "\n".join(lines) + "\n"

    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(content)
    io.close()

    inpath = "problem%d.in" % idx
    outpath = "problem%d.out" % idx
    with open(inpath) as fin, open(outpath, "w") as fout:
        subprocess.run([STD], stdin=fin, stdout=fout, check=True)

    with open(outpath) as f:
        out = f.read()
    outlines = out.split("\n")
    if outlines and outlines[-1] == "":
        outlines.pop()
    assert len(outlines) == nq, \
        "point %d: .out 行数 %d != 询问数 %d" % (idx, len(outlines), nq)
    if nq > 0:
        assert len(outlines) > 0, "point %d: 有询问但 .out 为空" % idx
    for x in outlines:
        int(x)                      # 每行必须为整数

    STATS.append((idx, n, q, nq, note))
    print("problem%-2d: n=%-6d q=%-6d P=%-8d 询问=%-6d  %s" % (idx, n, q, P, nq, note))


# ---------------- 各测试点 ----------------
def main():
    assert os.path.exists(STD), "未找到 std，请先编译：g++ -O2 -std=c++17 std.cpp -o std"

    # ---- 点 1：题面样例 ----
    sample_edges = [(1, 3), (5, 3), (4, 3), (3, 2)]
    sample_init = [24701, 12247, 27130, 27071, 4060]
    sample_ops = ["4 5 1 27096", "4 2 3 17348", "3 1 2 8785 8918",
                  "5 3 5", "4 2 1 2936"]
    emit(1, 5, 5, 29311, sample_edges, sample_init, sample_ops, 1,
         "样例层：题面【输入样例】原样，答案应为 15488")

    # ---- 点 2：边界（n=1 无边 + P=1） ----
    emit(2, 1, 3, 1, [], [A_MAX],
         ["3 1 1 100 200", "5 1 1", "1 1 1 5 7"], 1,
         "边界层：n=1 退化树（无边）+ P=1（模 1 恒 0）+ 单点操作")

    # ---- 点 3：边界/小规模（P=6 偶数合数，五种操作全覆盖） ----
    rnd = random.Random(176403)
    n, q = 10, 20
    edges = gen_tree(n, "random", rnd)
    init = [rnd.randint(0, A_MAX) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.35, A_MAX, boundary=True)
    emit(3, n, q, 6, edges, init, ops, nq,
         "边界/小：n=10,q=20,P=6（偶数合数，检验不可对 2 求逆），五种操作全覆盖")

    # ---- 点 4：小规模链（20% 子任务上限，P=997） ----
    rnd = random.Random(176404)
    n = q = 1000
    edges = gen_tree(n, "chain", rnd)
    init = [rnd.randint(0, 10000) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.4, 10000)
    emit(4, n, q, 997, edges, init, ops, nq,
         "小规模链：n=q=1000（20% 子任务上限），P=997，值域 1e4")

    # ---- 点 5：小规模随机树（20% 子任务上限，P=1e7，值域 2^31） ----
    rnd = random.Random(176405)
    n = q = 1000
    edges = gen_tree(n, "random", rnd)
    init = [rnd.randint(0, A_MAX) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.3, A_MAX)
    emit(5, n, q, P_MAX, edges, init, ops, nq,
         "小规模随机树：n=q=1000，P=1e7（题面上限），值域 2^31")

    # ---- 点 6：中等随机树（40% 子任务上限，P=1000000 偶数合数） ----
    rnd = random.Random(176406)
    n = q = 10000
    edges = gen_tree(n, "random", rnd)
    init = [rnd.randint(0, A_MAX) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.35, A_MAX)
    emit(6, n, q, 1000000, edges, init, ops, nq,
         "中等随机树：n=q=10000（40% 子任务上限），P=1000000（偶数合数），值域 2^31")

    # ---- 点 7：中等链·询问为主 ----
    rnd = random.Random(176407)
    n = q = 10000
    edges = gen_tree(n, "chain", rnd)
    init = [rnd.randint(0, A_MAX) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.8, A_MAX)
    emit(7, n, q, 9999991, edges, init, ops, nq,
         "中等链·询问为主：n=q=10000，询问占比 0.8，输出量大")

    # ---- 点 8：大·多链段（完全二叉树） ----
    rnd = random.Random(176408)
    n = q = 100000
    edges = gen_tree(n, "bin", rnd)
    init = [rnd.randint(0, A_MAX) for _ in range(n)]
    ops, nq = gen_ops(q, n, rnd, 0.4, A_MAX)
    emit(8, n, q, P_MAX, edges, init, ops, nq,
         "大·多链段：n=q=1e5 完全二叉树（路径拆 O(log n) 段），P=1e7，值域 2^31")

    # ---- 点 9：顶格随机树（值域全部取满 2^31） ----
    rnd = random.Random(176409)
    n = q = 100000
    edges = gen_tree(n, "random", rnd)
    init = [A_MAX] * n
    ops, nq = gen_ops(q, n, rnd, 0.3, A_MAX)
    # 强制 a=d=2^31 的顶格操作若干
    ops[0] = "1 1 %d %d %d" % (n, A_MAX, A_MAX)
    ops[1] = "3 %d 1 %d %d" % (n, A_MAX, A_MAX)
    ops[2] = "2 %d 1 %d" % (n, A_MAX)
    ops[3] = "4 1 %d %d" % (n, A_MAX)
    emit(9, n, q, P_MAX, edges, init, ops, nq,
         "顶格随机树：n=q=1e5，A_i/a/d 全部取 2^31（值域顶格），P=1e7")

    # ---- 点 10：顶格链（30% 子任务性质 + 最深结构） ----
    rnd = random.Random(176410)
    n = q = 100000
    edges = gen_tree(n, "chain", rnd)
    init = [A_MAX] * n
    ops, nq = gen_ops(q, n, rnd, 0.5, A_MAX)
    ops[0] = "1 1 %d %d %d" % (n, A_MAX, A_MAX)
    ops[1] = "4 %d 1 %d" % (n, A_MAX)
    emit(10, n, q, P_MAX, edges, init, ops, nq,
         "顶格链：n=q=1e5 单链（30% 子任务性质，最深结构），A_i/a/d=2^31，P=1e7")

    print("\n共 %d 个测试点；全部 .out 行数与询问数一致、非空且为整数。" % len(STATS))


if __name__ == "__main__":
    main()
