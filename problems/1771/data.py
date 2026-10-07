#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data.py  --  一本通 1771《仓库选址》测试数据生成

分层策略(10 组, 覆盖 边界 / 小 / 中 / 大 / 顶格):
  组号  n        M     树形     边权范围   说明
  01    1        0     -        -          最小边界(单点, 答案恒 0)
  02    2        15    链       1..1000    最小非平凡 + 最大 M
  03    6        0     随机     1..10      对应题面测试点 1
  04    100      5     随机     1..1000    对应测试点 2
  05    2000     9     链       1..5       对应测试点 3 + 深链(测非递归)
  06    50000    0     随机     1..1000    对应测试点 4/5
  07    50000    6     完全二叉树 1..500     对应测试点 7 + 平衡树形
  08    100000   10    随机     1..60      对应测试点 8
  09    100000   13    菊花     1..1000    对应测试点 9 + 星形边界
  10    100000   15    随机     1..60      对应测试点 10(顶格: 最大 n, 最大 M)

要点:
  * 纯 Python 线性生成, 无 O(n^2) 循环; 节点做随机重标号, 避免标签与结构相关。
  * 用 subprocess 显式运行 std 产出 .out(不依赖 cyaron 缓冲), 并断言 .out 非空、
    行数 == n、答案非负且 <= 2e9。
"""

import os
import random
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(BASE, "std")
OUTDIR = os.path.join(BASE, "data")

random.seed(0xC0FFEE)

GROUPS = [
    dict(n=1,      M=0,  shape="none",   cmin=1, cmax=1),
    dict(n=2,      M=15, shape="path",   cmin=1, cmax=1000),
    dict(n=6,      M=0,  shape="random", cmin=1, cmax=10),
    dict(n=100,    M=5,  shape="random", cmin=1, cmax=1000),
    dict(n=2000,   M=9,  shape="path",   cmin=1, cmax=5),
    dict(n=50000,  M=0,  shape="random", cmin=1, cmax=1000),
    dict(n=50000,  M=6,  shape="binary", cmin=1, cmax=500),
    dict(n=100000, M=10, shape="random", cmin=1, cmax=60),
    dict(n=100000, M=13, shape="star",   cmin=1, cmax=1000),
    dict(n=100000, M=15, shape="random", cmin=1, cmax=60),
]


def gen_edges(n, shape, cmin, cmax):
    """线性时间生成 n-1 条边 (1-indexed)。"""
    edges = []
    if n <= 1:
        return edges
    if shape == "random":                       # 每点挂到前面随机点 -> 期望深度 O(log n)
        for i in range(2, n + 1):
            p = random.randint(1, i - 1)
            edges.append((p, i, random.randint(cmin, cmax)))
    elif shape == "path":
        for i in range(2, n + 1):
            edges.append((i - 1, i, random.randint(cmin, cmax)))
    elif shape == "star":
        for i in range(2, n + 1):
            edges.append((1, i, random.randint(cmin, cmax)))
    elif shape == "binary":
        for i in range(2, n + 1):
            edges.append((i // 2, i, random.randint(cmin, cmax)))
    else:
        raise ValueError("unknown shape: %s" % shape)

    # 随机重标号, 打散结构与编号的关系
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    lab = [0] * (n + 1)
    for i, p in enumerate(perm, start=1):
        lab[i] = p
    return [(lab[a], lab[b], c) for (a, b, c) in edges]


def write_in(path, n, M, edges):
    with open(path, "w") as f:
        f.write("%d %d\n" % (n, M))
        f.write("".join("%d %d %d\n" % e for e in edges))


def main():
    if not os.path.exists(STD):
        print("ERROR: std binary not found: %s (先编译 std.cpp)" % STD, file=sys.stderr)
        sys.exit(2)
    os.makedirs(OUTDIR, exist_ok=True)

    total_t0 = time.time()
    print("idx  n        M    shape    c-range     maxans       std_time  out_lines")
    for idx, gr in enumerate(GROUPS, 1):
        n, M = gr["n"], gr["M"]
        edges = gen_edges(n, gr["shape"], gr["cmin"], gr["cmax"])
        ipath = os.path.join(OUTDIR, "%d.in" % idx)
        opath = os.path.join(OUTDIR, "%d.out" % idx)
        write_in(ipath, n, M, edges)

        with open(ipath, "rb") as fi, open(opath, "wb") as fo:
            t0 = time.time()
            r = subprocess.run([STD], stdin=fi, stdout=fo)
            dt = time.time() - t0
        assert r.returncode == 0, "std 运行失败, 组 %d" % idx

        with open(opath) as f:
            toks = f.read().split()
        # .out 校验: 行数必须 == n, 且全部为非负整数
        assert len(toks) == n, "组 %d: .out 行数 %d != n %d" % (idx, len(toks), n)
        vals = [int(x) for x in toks]
        mx = max(vals)
        assert mx <= 2_000_000_000, "组 %d: 最大答案 %d 超过 2e9" % (idx, mx)
        assert min(vals) >= 0, "组 %d: 出现负数答案" % idx

        print("%-4d %-8d %-4d %-8s %-11s %-11d %.3fs    %d"
              % (idx, n, M, gr["shape"], "%d-%d" % (gr["cmin"], gr["cmax"]),
                 mx, dt, len(toks)))

    print("ALL OK, total %.2fs" % (time.time() - total_t0))


if __name__ == "__main__":
    main()
