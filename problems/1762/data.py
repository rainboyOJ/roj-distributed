#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1762《与非》 数据生成器（分层 10 组）

题面数据范围（content.md【提示】）：
    30%: 1<=n,m<=1000
    10%: k=1
    20%: k=2
    100%: 1<=n,m<=10^5, 1<=k<=32, 0<=w[i]<2^k

用法：
    g++-16 -O2 -std=c++17 std.cpp -o std        # 仓库 macOS 上 /usr/bin/g++ 是 clang，无 bits/stdc++.h
    mkdir -p data && cd data && python3 ../data.py

注意（cyaron 隐患规避）：
    本脚本不用 io.output_gen()，而是用 subprocess 显式把 .in 喂给 ../std 生成 .out，
    写完后 flush/close，并断言 .out 非空且行数 == 该点 Query 操作条数
    （本题每组至少 1 个 Query，故不存在合法的空输出点）。

分层设计（10 组，规模自小到大铺到顶格）：
    点 1-2   边界层：n,m 下限 / k 上下限 / 权值上下限 / 答案顶格
    点 3     样例层：题面样例原样复现
    点 4-6   小/中规模随机：k=2 档、k=8、k=32 全覆盖
    点 7-8   大规模：随机树 / 纯链（卡 HLD 方向与长路径）
    点 9-10  顶格层：n=m=10^5 卡常结构
"""
import os
import random
import subprocess

random.seed(20261762)

# 说明：本脚本不依赖 cyaron 的缓冲式 IO（input_write / output_gen）。
# cyaron 的 input_write 在进程结束前不一定 flush，会让 std 读到空的 .in，
# output_gen 同理可能产出 0 字节 .out。这里直接 open() 写 .in（with 关闭即落盘），
# 再用 subprocess 显式跑 std 写 .out，最后断言 .out 非空且行数正确。
# 文件命名沿用仓库惯例：problem{i}.in / problem{i}.out

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")


def build_content(n, m, k, weights, edges, ops):
    """拼装 .in 文本；ops 为已格式化的操作行列表。返回 (content, n_query)。"""
    assert len(weights) == n, (len(weights), n)
    assert len(edges) == n - 1, (len(edges), n)
    assert len(ops) == m, (len(ops), m)
    for w in weights:
        assert 0 <= w < (1 << k), w
    lines = ["%d %d %d" % (n, m, k), " ".join(map(str, weights))]
    lines += ["%d %d" % (a, b) for (a, b) in edges]
    lines += ops
    nq = sum(1 for s in ops if s[0] == 'Q')
    return "\n".join(lines) + "\n", nq


def gen_ops(m, n, k, replace_p=0.5, rng=None):
    """随机操作序列；Query 保证 1<=x<y<=n（n>=2 时），Replace 的 y 取 [0,2^k)。"""
    rng = rng or random
    ops = []
    for _ in range(m):
        if n >= 2 and rng.random() >= replace_p:
            x = rng.randint(1, n - 1)
            y = rng.randint(x + 1, n)
            ops.append("Query %d %d" % (x, y))
        else:
            ops.append("Replace %d %d" % (rng.randint(1, n), rng.randint(0, (1 << k) - 1)))
    return ops


def emit(data_id, content, n_query):
    """写 .in 并显式用 std 生成 .out，断言非空且行数符合预期。"""
    inp = os.path.join(DATA_DIR, "problem%d.in" % data_id)
    outp = os.path.join(DATA_DIR, "problem%d.out" % data_id)
    with open(inp, "w") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    with open(inp, "r") as fi, open(outp, "w") as fo:
        subprocess.run([STD], stdin=fi, stdout=fo, check=True)
        fo.flush()
        os.fsync(fo.fileno())
    size = os.path.getsize(outp)
    assert size > 0, "problem%d.out 为空（0 字节）" % data_id
    with open(outp, "r") as f:
        nl = sum(1 for _ in f)
    assert nl == n_query, "problem%d.out 行数 %d != Query 条数 %d" % (data_id, nl, n_query)
    return size, nl


# --------------------------------------------------------------------------
# 点 1：边界层 —— n=m=1 下限、k=32 上限、w=2^32-1 上限、x=y 退化路径
#   路径只有 1 个点：f(1) = 0 nand w = 2^k-1 = 4294967295
# --------------------------------------------------------------------------
def gen1():
    n, m, k = 1, 1, 32
    weights = [2 ** 32 - 1]
    content, nq = build_content(n, m, k, weights, [], ["Query 1 1"])
    return content, nq


# --------------------------------------------------------------------------
# 点 2：边界层 —— k=1 下限、权值全 0、正反两个方向的 Query + Replace
#   k=1: nand(0,0)=1, nand(1,0)=1 → 两个方向答案都是 1
# --------------------------------------------------------------------------
def gen2():
    n, m, k = 2, 3, 1
    weights = [0, 0]
    edges = [(1, 2)]
    ops = ["Query 1 2", "Query 2 1", "Replace 1 1"]
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 3：样例层 —— content.md【输入样例】原样（答案 4 / 7）
# --------------------------------------------------------------------------
def gen3():
    n, m, k = 3, 3, 3
    weights = [2, 7, 3]
    edges = [(1, 2), (2, 3)]
    ops = ["Query 2 3", "Replace 1 3", "Query 1 1"]
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 4：小规模随机 —— k=2（题面 20% 档），n=m=20，可手算/调试
# --------------------------------------------------------------------------
def gen4():
    n, m, k = 20, 20, 2
    weights = [random.randint(0, 3) for _ in range(n)]
    edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    ops = gen_ops(m, n, k, replace_p=0.5)
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 5：中规模随机 —— k=32，n=m=1000（题面 30% 档上限），混合操作
# --------------------------------------------------------------------------
def gen5():
    n, m, k = 1000, 1000, 32
    weights = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    ops = gen_ops(m, n, k, replace_p=0.5)
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 6：中规模 —— k=8，n=m=5000，全 Query（无修改），随机树
# --------------------------------------------------------------------------
def gen6():
    n, m, k = 5000, 5000, 8
    weights = [random.randint(0, 255) for _ in range(n)]
    edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    ops = gen_ops(m, n, k, replace_p=0.0)
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 7：大规模随机 —— n=m=10^5 顶格，k=32，随机树，Query/Replace 各半
# --------------------------------------------------------------------------
def gen7():
    n, m, k = 100000, 100000, 32
    weights = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    ops = gen_ops(m, n, k, replace_p=0.5)
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 8：大规模构造 —— 纯链 1-2-...-n（n=m=10^5），路径长度顶格，
#   专卡「方向拼错」（x 侧需反向复合）与长路径；权值随机
# --------------------------------------------------------------------------
def gen8():
    n, m, k = 100000, 100000, 32
    weights = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    edges = [(i, i + 1) for i in range(1, n)]
    ops = gen_ops(m, n, k, replace_p=0.3)
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 9：顶格层 —— n=m=10^5，k=32，毛毛虫树（链 + 每节挂叶），
#   全 Query 且一律取「最深两叶之间」（路径最长）；权值取 {0, 2^32-1} 极端交替
# --------------------------------------------------------------------------
def gen9():
    n, m, k = 100000, 100000, 32
    half = n // 2
    weights = [(2 ** 32 - 1) if (i % 2) else 0 for i in range(n)]
    edges = []
    for i in range(1, half):          # 链 1..half
        edges.append((i, i + 1))
    leaves = []
    for i in range(half + 1, n + 1):  # 每个链节挂一片叶
        edges.append((i - half, i))
        leaves.append(i)
    assert len(edges) == n - 1, len(edges)
    ops = []
    L = len(leaves)
    for _ in range(m):
        i1 = random.randrange(L)
        i2 = random.randrange(L - 1)          # O(1) 取两个不同下标，避免 index() 造成 O(n^2)
        if i2 >= i1:
            i2 += 1
        a, b = leaves[i1], leaves[i2]
        if a > b:
            a, b = b, a
        ops.append("Query %d %d" % (a, b))
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


# --------------------------------------------------------------------------
# 点 10：顶格卡常 —— n=m=10^5，k=32，完全二叉树（重链浅、跨链多），
#   Replace/Query 交替，Query 取最深的两片叶（跨多条链，考验两侧拼接）
# --------------------------------------------------------------------------
def gen10():
    n, m, k = 100000, 100000, 32
    weights = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
    edges = [(i // 2, i) for i in range(2, n + 1)]
    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[i // 2] + 1
    maxd = max(depth)
    deep = [i for i in range(1, n + 1) if depth[i] >= maxd - 1]
    ops = []
    L = len(deep)
    for j in range(m):
        if j % 2 == 0:
            i1 = random.randrange(L)
            i2 = random.randrange(L - 1)
            if i2 >= i1:
                i2 += 1
            a, b = deep[i1], deep[i2]
            if a > b:
                a, b = b, a
            ops.append("Query %d %d" % (a, b))
        else:
            ops.append("Replace %d %d" % (random.randint(1, n), random.randint(0, 2 ** 32 - 1)))
    content, nq = build_content(n, m, k, weights, edges, ops)
    return content, nq


GENS = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.chdir(DATA_DIR)
    for i, g in enumerate(GENS, 1):
        content, nq = g()
        size, nl = emit(i, content, nq)
        head = content.split("\n")[0]
        print("problem%d: header='%s' queries=%d out_lines=%d out_bytes=%d OK"
              % (i, head, nq, nl, size))
    print("ALL %d CASES OK" % len(GENS))
