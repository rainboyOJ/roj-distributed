#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1758《连通能力》分层数据生成器
#   生成 data/problem1.in/.out ... data/problem10.in/.out
#   .out 由 subprocess 显式调用 std 生成（不用 cyaron.output_gen，避免写缓冲不 flush
#   导致 0 字节 .out），并断言 .out 非空且行数 == N。
import os
import random
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

WMAX = 10000  # 题面 w 上限


# ---------------------------------------------------------------- 输入写出 --
def write_case(path, n, edges):
    """edges 为可迭代的 (u,v,w)，逐个写出，不整体驻留内存（N 可达 1e6）。"""
    with open(path, "w") as f:
        f.write("%d\n" % n)
        buf = []
        for u, v, w in edges:
            buf.append("%d %d %d\n" % (u, v, w))
            if len(buf) >= 200000:
                f.write("".join(buf))
                del buf[:]
        if buf:
            f.write("".join(buf))


# ------------------------------------------------------------ 树的构造方式 --
def edges_star(n, rng):
    """星形：所有边与 1 号点相连（20% 子任务特征）。"""
    for v in range(2, n + 1):
        yield (1, v, rng.randint(1, WMAX))


def edges_random(n, rng, wmax=WMAX):
    """随机递归树：parent(v) 均匀取自 [1, v-1]，再随机打乱标号。"""
    if n <= 1:
        return
    perm = list(range(n + 1))
    tail = perm[1:]
    rng.shuffle(tail)
    perm[1:] = tail
    for v in range(2, n + 1):
        u = rng.randint(1, v - 1)
        yield (perm[u], perm[v], rng.randint(1, wmax))


def edges_deep_random(n, rng, chain_p=0.5, wmax=WMAX):
    """偏深的随机树：以 chain_p 概率挂在上一个点，否则随机挂（深度大、有分支）。"""
    if n <= 1:
        return
    for v in range(2, n + 1):
        u = v - 1 if rng.random() < chain_p else rng.randint(1, v - 1)
        yield (u, v, rng.randint(1, wmax))


def edges_chain(n, rng, wmax=WMAX, w=None):
    """链 1-2-...-n，边权统一 w（或 wmax）。"""
    if n <= 1:
        return
    for v in range(2, n + 1):
        yield (v - 1, v, w if w is not None else rng.randint(1, wmax))


# ------------------------------------------------------------------ 分层表 --
# (层次描述, n, 生成函数)
PLANS = [
    ("边界 N=1 单点（无输入边，输出 0）",              1,      lambda r: edges_chain(1, r)),
    ("边界 N=2 单边权取下限/上限 w=10000",             2,      lambda r: edges_chain(2, r, w=WMAX)),
    ("样例 题面样例（精确比对题面输出）",                5,      lambda r: iter([(1, 2, 1), (1, 3, 3), (3, 4, 2), (3, 5, 1)])),
    ("小   N=10 随机树 w<=10",                        10,     lambda r: edges_random(10, r, wmax=10)),
    ("小星 N=300 星形（20% 子任务）w<=10000",          300,    lambda r: edges_star(300, r)),
    ("中   N=300 随机树（40% 子任务）",                300,    lambda r: edges_random(300, r)),
    ("中深 N=4000 偏深随机树（60% 子任务）",            4000,   lambda r: edges_deep_random(4000, r, 0.5)),
    ("大   N=100000 随机树（80% 子任务）",             100000, lambda r: edges_random(100000, r)),
    ("顶格 N=1000000 随机树 + 随机重标号（100% 子任务）", 1000000, lambda r: edges_random(1000000, r)),
    ("顶格 N=1000000 深链 w=10000（距离 1e10，测 long long 与无递归）",
     1000000, lambda r: edges_chain(1000000, r, w=WMAX)),
]

SAMPLE_EXPECT = "4\n0\n2\n0\n0\n"


def main():
    os.makedirs(DATA, exist_ok=True)

    # ---- 准备 std 可执行文件（无则编译到临时目录，不留编译产物）----
    tmpdir = None
    std = os.path.join(BASE, "std")
    if not (os.path.isfile(std) and os.access(std, os.X_OK)):
        tmpdir = tempfile.mkdtemp(prefix="std1758_")
        std = os.path.join(tmpdir, "std")
        subprocess.run(["g++", "-O2", "-o", std, os.path.join(BASE, "std.cpp")],
                       check=True)
    print("std =", std)

    try:
        for i, (desc, n, gen) in enumerate(PLANS, 1):
            rng = random.Random(12345 + i)
            in_path = os.path.join(DATA, "problem%d.in" % i)
            out_path = os.path.join(DATA, "problem%d.out" % i)

            write_case(in_path, n, gen(rng))

            with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
                subprocess.run([std], stdin=fi, stdout=fo, check=True)

            # ---- 断言 ----
            assert os.path.getsize(in_path) > 0, "empty .in at %d" % i
            assert os.path.getsize(out_path) > 0, "empty .out at %d" % i
            with open(out_path) as f:
                lines = [ln for ln in f.read().split("\n") if ln != ""]
            assert len(lines) == n, \
                "point %d: out lines %d != N %d" % (i, len(lines), n)
            assert all(ln.lstrip("-").isdigit() for ln in lines), \
                "point %d: non-numeric output" % i
            if i == 3:
                got = "\n".join(lines) + "\n"
                assert got == SAMPLE_EXPECT, \
                    "point 3 sample mismatch:\n%s" % got

            print("point %2d | %-52s | N=%-7d | in=%-9d out_lines=%d"
                  % (i, desc, n, os.path.getsize(in_path), len(lines)))
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)

    print("ALL DATA GENERATED OK")


if __name__ == "__main__":
    sys.exit(main())
