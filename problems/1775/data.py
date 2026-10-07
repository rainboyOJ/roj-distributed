#!/usr/bin/env python3
# 一本通 1775《梦中漫步》数据生成器
# 用法：mkdir -p data && python3 data.py   （std 需先编译到 ../std 或 ./std）
#
# 题面数据范围（content.md）：N<=100000, Q<=100000。
#   20% N<=10；40% N<=1000；另有 20% 保证是链。
# 数组/规模一律按题面上限（1e5）开，安全系数：所有随机树/查询严格落在 [1,N]。
#
# ⚠ cyaron 的 io.output_gen 若写缓冲不 flush 可能产出 0 字节 .out，
#   故本脚本不用 cyaron 写输出：直接 subprocess 跑 std 抓 stdout 写 .out，
#   并断言 .out 非空、行数恰为 Q（本题每组均有 Q 行答案，无空输出点）。
#
# 分层设计（10 组）：
#   1-2   边界层：N=1 / N=2 最小规模；
#   3     小规模随机：N=10（20% 档上限），可手算核对；
#   4-5   中规模：N=1000（40% 档），链 / 随机树；
#   6-7   大规模结构：N=Q=1e5，链（最大深度，卡递归爆栈）/ 菊花（最大度）；
#   8-10  顶格：N=Q=1e5，随机树 / 完全二叉树 / 毛毛虫，随机与顶格查询。
import os
import random
import subprocess
import sys

STD = os.environ.get("STD", "./std")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def random_tree(n, rng):
    """随机树：i 的父亲在 [1,i-1] 中随机。"""
    edges = [(rng.randint(1, i - 1), i) for i in range(2, n + 1)]
    return edges


def chain(n):
    return [(i - 1, i) for i in range(2, n + 1)]


def star(n):
    return [(1, i) for i in range(2, n + 1)]


def binary(n):
    return [(i // 2, i) for i in range(2, n + 1)]


def caterpillar(n):
    """毛毛虫：主干长度 n//2，主干每点挂一个叶子。"""
    half = n // 2
    edges = [(i - 1, i) for i in range(2, half + 1)]
    for i in range(1, half + 1):
        if half + i <= n:
            edges.append((i, half + i))
    return edges


def rand_queries(n, q, rng):
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]


def deep_queries(n, q, rng):
    """偏向根/叶的查询，尽量拉长路径。"""
    out = []
    for _ in range(q):
        out.append((1, n) if rng.randint(0, 1) else (rng.randint(1, n), rng.randint(1, n)))
    return out


def write_case(idx, n, q, edges, queries):
    os.makedirs(DATA_DIR, exist_ok=True)
    in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
    out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
    lines = ["%d %d" % (n, q)]
    for u, v in edges:
        lines.append("%d %d" % (u, v))
    for u, v in queries:
        lines.append("%d %d" % (u, v))
    with open(in_path, "w") as fo:
        fo.write("\n".join(lines) + "\n")
    # 显式跑 std 产出 .out（不用 cyaron 缓冲写）
    with open(in_path, "rb") as fi:
        res = subprocess.run([STD], stdin=fi, stdout=subprocess.PIPE, timeout=120)
    assert res.returncode == 0, "std 在 problem%d 上非 0 退出" % idx
    data = res.stdout
    assert len(data) > 0, "problem%d.out 为空（0 字节）！" % idx
    with open(out_path, "wb") as fo:
        fo.write(data)
    # 断言行数 == Q，且每行都是合法整数
    text = data.decode().strip("\n")
    rows = text.split("\n") if text else []
    assert len(rows) == q, "problem%d.out 行数 %d != Q=%d" % (idx, len(rows), q)
    for r in rows:
        int(r)
    print("problem%d: N=%d Q=%d edges=%d -> out_lines=%d OK" % (idx, n, q, len(edges), len(rows)))


def main():
    # 点 1：边界 N=1，Q=1，无解边，查询 1 1 -> 0
    write_case(1, 1, 1, [], [(1, 1)])

    # 点 2：边界 N=2，Q=2，双向查询
    write_case(2, 2, 2, chain(2), [(1, 2), (2, 1)])

    # 点 3：小规模随机 N=Q=10（20% 档上限），固定种子可复现
    rng = random.Random(177503)
    write_case(3, 10, 10, random_tree(10, rng), rand_queries(10, 10, rng))

    # 点 4：中规模链 N=Q=1000（40% 档，链性质）
    rng = random.Random(177504)
    write_case(4, 1000, 1000, chain(1000), rand_queries(1000, 1000, rng))

    # 点 5：中规模随机树 N=Q=1000（40% 档，一般树）
    rng = random.Random(177505)
    write_case(5, 1000, 1000, random_tree(1000, rng), rand_queries(1000, 1000, rng))

    # 点 6：大规模链 N=Q=1e5（最大深度，卡递归爆栈 / 卡 LCA 深度差）
    rng = random.Random(177506)
    write_case(6, 100000, 100000, chain(100000), rand_queries(100000, 100000, rng))

    # 点 7：大规模菊花 N=Q=1e5（最大度，根连接所有点）
    rng = random.Random(177507)
    write_case(7, 100000, 100000, star(100000), rand_queries(100000, 100000, rng))

    # 点 8：顶格随机树 N=Q=1e5
    rng = random.Random(177508)
    write_case(8, 100000, 100000, random_tree(100000, rng), rand_queries(100000, 100000, rng))

    # 点 9：顶格完全二叉树 N=Q=1e5，偏向根-叶长路径查询
    rng = random.Random(177509)
    write_case(9, 100000, 100000, binary(100000), deep_queries(100000, 100000, rng))

    # 点 10：顶格毛毛虫 N=Q=1e5，长路径 + 侧枝混合
    rng = random.Random(177510)
    write_case(10, 100000, 100000, caterpillar(100000), deep_queries(100000, 100000, rng))


if __name__ == "__main__":
    main()
    print("ALL 10 CASES OK")
