#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1756《过路费》分层数据生成器
# 生成 problem1.in/.out ... problem10.in/.out
# 用 std 跑出 .out，并断言 .out 非空、行数 == q。
import os
import random
import subprocess

from cyaron import IO

WMAX = 10 ** 9


def gen_connected(n, m, wmax, rng, chain=False):
    """返回 m 条边的列表 [(u,v,w), ...]，保证 n 个点连通。
    chain=True 时主结构为链 i-(i+1) 且权=i，其余补边权为 WMAX。"""
    edges = []
    if n == 1:
        for _ in range(m):
            edges.append((1, 1, rng.randint(0, wmax)))
        return edges

    if chain:
        for i in range(1, n):
            edges.append((i, i + 1, i))  # 链上边权 = 下标 i (1..n-1)
        extra = m - (n - 1)
        for _ in range(extra):
            u = rng.randint(1, n)
            v = rng.randint(1, n)
            while v == u:
                v = rng.randint(1, n)
            edges.append((u, v, WMAX))  # 补边权极大，不进入 MST
        return edges

    # 随机树保证连通
    for v in range(2, n + 1):
        u = rng.randint(1, v - 1)
        edges.append((u, v, rng.randint(0, wmax)))
    extra = m - (n - 1)
    for _ in range(extra):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        while v == u:
            v = rng.randint(1, n)
        edges.append((u, v, rng.randint(0, wmax)))
    rng.shuffle(edges)
    return edges


def build_text(n, edges, queries):
    out = ["%d %d" % (n, len(edges))]
    for u, v, w in edges:
        out.append("%d %d %d" % (u, v, w))
    out.append("%d" % len(queries))
    for s, t in queries:
        out.append("%d %d" % (s, t))
    return "\n".join(out) + "\n"


def rand_queries(n, q, rng, self_ratio=0.05):
    res = []
    for _ in range(q):
        if n > 1 and rng.random() < self_ratio:
            s = rng.randint(1, n)
            res.append((s, s))
        else:
            s = rng.randint(1, n)
            t = rng.randint(1, n)
            res.append((s, t))
    return res


def main():
    # 每个测试点的构造：(注释见下方分层说明)
    plans = []

    # 1 边界：n 最小、答案为 0（单点自环）
    plans.append(("边界|n=1,m=1 自环 w=0, q=1 问 (1,1)->0",
                  lambda rng: (1, [(1, 1, 0)], [(1, 1)])))

    # 2 边界：n=2，唯一道路权取最大值 1e9，含 S==T
    plans.append(("边界|n=2,m=1 w=1e9, q=3 含(1,1)->0",
                  lambda rng: (2, [(1, 2, WMAX)], [(1, 1), (1, 2), (2, 1)])))

    # 3 小规模随机（可手算量级）
    plans.append(("小随机|n=5,m=8,w<=20,q=5",
                  lambda rng: (5, gen_connected(5, 8, 20, rng), rand_queries(5, 5, rng))))

    # 4 小规模随机
    plans.append(("小随机|n=20,m=60,w<=100,q=20",
                  lambda rng: (20, gen_connected(20, 60, 100, rng), rand_queries(20, 20, rng))))

    # 5 中等随机
    plans.append(("中随机|n=500,m=3000,w<=1e9,q=500",
                  lambda rng: (500, gen_connected(500, 3000, WMAX, rng), rand_queries(500, 500, rng))))

    # 6 中等随机（小权值，大量重复权）
    plans.append(("中随机|n=1000,m=10000,w<=1000,q=1000",
                  lambda rng: (1000, gen_connected(1000, 10000, 1000, rng), rand_queries(1000, 1000, rng))))

    # 7 大规模随机
    plans.append(("大随机|n=5000,m=50000,w<=1e9,q=5000",
                  lambda rng: (5000, gen_connected(5000, 50000, WMAX, rng), rand_queries(5000, 5000, rng))))

    # 8 大规模随机
    plans.append(("大随机|n=10000,m=80000,w<=1e9,q=8000",
                  lambda rng: (10000, gen_connected(10000, 80000, WMAX, rng), rand_queries(10000, 8000, rng))))

    # 9 顶格随机
    plans.append(("顶格|n=10000,m=100000,q=10000,w<=1e9 随机图",
                  lambda rng: (10000, gen_connected(10000, 100000, WMAX, rng), rand_queries(10000, 10000, rng))))

    # 10 顶格特殊结构：链（权递增 i）+ 大量 1e9 补边，答案为 max(s,t)-1
    def plan10(rng):
        n = 10000
        m = 100000
        edges = gen_connected(n, m, WMAX, rng, chain=True)
        queries = rand_queries(n, 10000, rng)
        return n, edges, queries
    plans.append(("顶格特殊|n=10000,m=100000 链权=i+补边1e9,q=10000", plan10))

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)

    for i, (desc, fn) in enumerate(plans, 1):
        rng = random.Random(12345 + i)
        n, edges, queries = fn(rng)
        text = build_text(n, edges, queries)
        io = IO(file_prefix="problem", data_id=i)
        io.input_write(text)
        io.output_gen("../std")
        # cyaron 的 output_gen 不 flush 输出缓冲，需显式 flush 否则磁盘上可能是 0 字节
        io.output_file.flush()
        os.fsync(io.output_file.fileno())

        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        assert os.path.getsize(in_path) > 0, "empty in %d" % i
        assert os.path.getsize(out_path) > 0, "empty out %d" % i
        with open(out_path) as f:
            lines = [ln for ln in f.read().split("\n") if ln != ""]
        assert len(lines) == len(queries), \
            "out line count %d != q %d at point %d" % (len(lines), len(queries), i)
        print("point %2d | %-55s | n=%d m=%d q=%d | out_lines=%d"
              % (i, desc, n, len(edges), len(queries), len(lines)))

    print("ALL DATA GENERATED OK")


if __name__ == "__main__":
    main()
