#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1817《染色游戏》分层测试数据生成器（10 个点，每点单组数据）
# 用法：cd .ybt-import/staging/1817 && python3 data.py
#       （脚本会先编译 std.cpp -> ./std，再把 problem1..10.in/.out 写进 ./data/）
#
# 题意：N 个点的树，Alice/Bob 轮流给未染色点染红/蓝（Alice 先手，每步必染一个），
#       直至无点可染；K_A/K_B = 红/蓝连通块数，求双方最优下的 K_A - K_B。
# 数据范围（题面明文）：N <= 100000；40% N <= 20；另有 10% 保证是链。时限 1000ms / 256MB。
# 输入格式：第一行 N，随后 N-1 行 u v（题面写「接下来 N 行」为笔误，样例均为 N-1 行，以样例为准）。
# 输出格式：一行一个整数。
#
# ---- 分层策略（单组数据题：按 N 与树形分层；文件命名严格 problem1..problem10）----
#   点 1  边界层：N=1 —— 题面下界，无边的退化树（输入仅一行 "1"），答案 1（可手算）。
#   点 2  边界层：N=2 —— 单边最小非平凡树，答案 0（可手算）。
#   点 3  样例层：N=4 星 —— 题面样例 1，期望 1。
#   点 4  样例层：N=5 星 —— 题面样例 2，期望 -1。
#   点 5  小规模层：N=20 随机树（固定种子）—— 40% 子任务上界。
#   点 6  链层（10% 子任务）：N=1000 链。
#   点 7  大规模结构化层：N=50000 完全二叉树（i 连 i//2），度数 1/2/3 混合。
#   点 8  顶格链层：N=100000 链（N 顶格 + 链形，10% 子任务的最坏规模）。
#   点 9  顶格极端层：N=100000 星（单点度 99999，答案绝对值最大的一类结构）。
#   点 10 顶格随机层：N=100000 随机树（随机父亲，固定种子）。
#
# 生成与自检约定：
#   * 生成器全部 O(N) 循环（无 O(n^2) 写法）；.in 用纯 Python 一次写盘。
#   * .out 由 subprocess 显式跑 ./std 生成（规避 cyaron output_gen 写缓冲不 flush
#     导致 0 字节 .out 的隐患），随后逐点断言：
#       - .in 非空、行数 = N（1 行 N + N-1 行边）、每边 1<=u,v<=N 且 u!=v；
#       - .out 非空、恰好 1 行、内容为整数；
#       - 手算点（1/2/3/4）答案与期望一致；
#       - 全部 10 点与「度数排序交替求和」公式的独立 Python 复算一致（文件完整性校验）。
#   * 数组规模：std 用 vector 动态开 N+1，无固定上限；N 严格取题面上限 100000（无越界探针）。

import os
import random
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

os.makedirs(DATA, exist_ok=True)


def ensure_std():
    """./std 缺失时现场编译（交付包收尾会删除二进制）。"""
    if os.path.exists(STD):
        return
    for cxx in ("g++", "g++-16", "g++-14", "clang++"):
        try:
            subprocess.check_call([cxx, "-O2", "-std=c++17", "std.cpp", "-o", "std"],
                                  cwd=HERE)
            print("compiled std with %s" % cxx)
            return
        except (OSError, subprocess.CalledProcessError):
            continue
    sys.exit("无法编译 std.cpp（尝试过 g++/g++-16/g++-14/clang++）")


# ---------------- 树形构造器（全部 O(N)） ----------------
def gen_chain(n):
    return [(i, i + 1) for i in range(1, n)]


def gen_star(n):
    return [(1, i) for i in range(2, n + 1)]


def gen_random(n, rng):
    return [(rng.randint(1, i - 1), i) for i in range(2, n + 1)]


def gen_bintree(n):
    return [(i // 2, i) for i in range(2, n + 1)]


# ---------------- 写盘 / 跑 std / 校验 ----------------
def write_in(idx, n, edges):
    assert len(edges) == max(0, n - 1), "点 %d 边数应为 N-1" % idx
    lines = [str(n)]
    lines += ["%d %d" % e for e in edges]
    path = os.path.join(DATA, "problem%d.in" % idx)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def run_std(idx, in_path):
    out_path = os.path.join(DATA, "problem%d.out" % idx)
    t0 = time.time()
    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        subprocess.run([STD], stdin=fin, stdout=fout, check=True, timeout=60)
    cost = time.time() - t0
    raw = open(out_path).read()
    assert raw.strip() != "", "problem%d.out 为空（0 字节或纯空白）" % idx
    toks = raw.split()
    assert len(toks) == 1 and re.fullmatch(r"-?\d+", toks[0]), \
        "problem%d.out 应为恰好 1 行整数，实际 %r" % (idx, raw[:80])
    return int(toks[0]), cost


def formula_expected(n, edges):
    """独立复算（度数升序交替求和公式，非博弈暴力）：与 std 输出互为文件级校验。"""
    deg = [0] * (n + 1)
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    d = sorted(deg[1:])
    s = sum(d[i] if i % 2 else -d[i] for i in range(n))
    return s // 2 + (n & 1)


# ---------------- 10 个测试点 ----------------
rng5 = random.Random(181705)
rng10 = random.Random(181710)

CASES = [
    (1, 1, [], 1, "边界层：N=1 退化树（无边的下界），手算答案 1"),
    (2, 2, gen_chain(2), 0, "边界层：N=2 单边最小非平凡树，手算答案 0"),
    (3, 4, gen_star(4), 1, "样例层：题面样例 1（N=4 星）"),
    (4, 5, gen_star(5), -1, "样例层：题面样例 2（N=5 星）"),
    (5, 20, gen_random(20, rng5), None, "小规模层：N=20 随机树（40% 子任务上界）"),
    (6, 1000, gen_chain(1000), None, "链层：N=1000 链（10% 子任务）"),
    (7, 50000, gen_bintree(50000), None, "大规模结构化层：N=50000 完全二叉树"),
    (8, 100000, gen_chain(100000), None, "顶格链层：N=100000 链"),
    (9, 100000, gen_star(100000), None, "顶格极端层：N=100000 星（最大度数 99999）"),
    (10, 100000, gen_random(100000, rng10), None, "顶格随机层：N=100000 随机树"),
]

assert len(CASES) == 10, "必须恰好 10 个测试点"

ensure_std()

print("点号  N       边数    答案      std耗时   说明")
results = {}
for idx, n, edges, want, note in CASES:
    in_path = write_in(idx, n, edges)
    got, cost = run_std(idx, in_path)
    exp = formula_expected(n, edges)
    assert got == exp, "点 %d: std=%d 与公式复算=%d 不一致" % (idx, got, exp)
    if want is not None:
        assert got == want, "点 %d: std=%d 与手算期望=%d 不一致" % (idx, got, want)
    # .in 结构自检
    with open(in_path) as f:
        toks = f.read().split()
    assert len(toks) == 1 + 2 * max(0, n - 1), "点 %d .in 行/词数异常" % idx
    assert int(toks[0]) == n, "点 %d .in 首行 N 不符" % idx
    us = [int(x) for x in toks[1::2]]
    vs = [int(x) for x in toks[2::2]]
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in zip(us, vs)), \
        "点 %d .in 含越界/自环边" % idx
    results[idx] = got
    print("%-4d %-8d %-7d %-8d %.3fs     %s" % (idx, n, len(edges), got, cost, note))

print("\n全部 10 点：.in/.out 非空、格式与行数校验通过；手算点 1-4 与独立公式复算 10/10 一致。")
print("答案清单:", {k: results[k] for k in sorted(results)})
