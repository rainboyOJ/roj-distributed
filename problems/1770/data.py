#!/usr/bin/env python3
# 一本通 1770《跳跳棋》数据生成器
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围：T<=10，1<=n,m<=100，0<=a_{i,j}<=10000。
# 子任务：5% n=1；15% n<=2；20% m<=15；5% 所有 a=1；10% 所有 a<=1；
#         75% n,m<=50 且 a<=9；100% 如上界。
#
# ⚠ cyaron 隐患规避：cyaron 的 output_gen 依赖写缓冲，若未 flush 会产出
#   0 字节 .out。本生成器 **只用 cyaron 写 .in**（写后显式 flush + close），
#   .out 一律用 subprocess 显式调用 std 生成，并断言：
#     (a) .out 非空；(b) 行数 == T；(c) 每行是整数；(d) 重跑 std 结果一致。
#
# 分层设计（10 组，.in/.out 成对）：
#   点 1-4   边界层：n=1 / m=1 / 极端权值 0 与 10000 / 多组数据；
#   点 5-6   小规模：n<=2、m<=15 子任务，含 m=1 单列、可手算；
#   点 7-8   中等规模：75% 子任务（n,m<=50, a<=9）上限；
#   点 9     大规模随机：100% 上限（T=10, n=m=100, a<=10000）；
#   点 10    顶格特殊结构：a≡1 / a∈{0,1} / a≡10000 / a≡0 / 交替极值 / 有序结构。
#
# 生成器只用列表推导式（无 O(n^2) Python 循环）。
import os
import random
import subprocess
import sys

from cyaron import IO

STD = "../std"

# ---------------- 工具 ----------------

def build(cases):
    """cases: list of (n, m, grid)；返回 .in 全文（T = len(cases)）。"""
    out = [str(len(cases))]
    for n, m, grid in cases:
        out.append("%d %d" % (n, m))
        out.extend(" ".join(map(str, row)) for row in grid)
    return "\n".join(out) + "\n"


def rand_grid(n, m, lo, hi, seed):
    rnd = random.Random(seed)
    return [[rnd.randint(lo, hi) for _ in range(m)] for _ in range(n)]


def run_point(idx, cases):
    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(build(cases))
    io.flush_buffer()
    io.close()

    in_path = "problem%d.in" % idx
    out_path = "problem%d.out" % idx
    with open(in_path, "rb") as fin:
        data = fin.read()
    # 显式用 subprocess 跑 std 产 .out（不依赖 cyaron output_gen 的写缓冲）
    p = subprocess.run([STD], input=data, stdout=subprocess.PIPE, check=True)
    with open(out_path, "wb") as fout:
        fout.write(p.stdout)
        fout.flush()
        os.fsync(fout.fileno())

    txt = p.stdout.decode().strip()
    lines = txt.split("\n") if txt else []
    assert len(p.stdout) > 0, "点%d: .out 为空" % idx
    assert len(lines) == len(cases), "点%d: .out 行数 %d != T %d" % (idx, len(lines), len(cases))
    for ln in lines:
        assert ln.strip().lstrip("-").isdigit(), "点%d: .out 非整数行 %r" % (idx, ln)

    # 重跑一致性（防缓冲/未定义行为）
    p2 = subprocess.run([STD], input=data, stdout=subprocess.PIPE, check=True)
    assert p2.stdout == p.stdout, "点%d: std 重跑结果不一致" % idx

    tn = max(c[0] for c in cases)
    tm = max(c[1] for c in cases)
    ma = max(max(max(r) for r in c[2]) for c in cases)
    print("problem%d: T=%d n<=%d m<=%d max_a=%d ans=[%s] rerun=OK"
          % (idx, len(cases), tn, tm, ma, ", ".join(lines[:4]) + ("..." if len(lines) > 4 else "")))
    return lines


# ---------------- 点 1：边界层 ----------------
# n=1,m=1, a=0：最小规模 + 最小值，答案 0
def gen1():
    return run_point(1, [(1, 1, [[0]])])


# ---------------- 点 2：边界层 ----------------
# n=1,m=1, a=10000：权值上限，答案 10000
def gen2():
    return run_point(2, [(1, 1, [[10000]])])


# ---------------- 点 3：边界层（n=1 子任务） ----------------
# n=1, m=100（m 上限），随机权值：答案 = min_j a[1][j]
def gen3():
    return run_point(3, [(1, 100, rand_grid(1, 100, 0, 10000, 177003))])


# ---------------- 点 4：边界层（多组 + n=1） ----------------
# T=10，每组 n=1, m=100，0/10000 交替：卡 "n=1 特判" 与多组数据
def gen4():
    cases = []
    for t in range(10):
        row = [[0 if (j + t) % 2 == 0 else 10000 for j in range(100)]]
        cases.append((1, 100, row))
    return run_point(4, cases)


# ---------------- 点 5：小规模（n<=2 子任务） ----------------
# T=1, n=2, m=2：与样例同量级，可手算
def gen5():
    return run_point(5, [(2, 2, [[1, 2], [3, 4]])])


# ---------------- 点 6：小规模（m<=15 / m=1 子任务） ----------------
# T=6：n<=2 随机；m<=15 随机；单列 m=1（n=100）与单行 n=1（m=1）
def gen6():
    cases = []
    cases.append((2, 2, rand_grid(2, 2, 0, 9, 177061)))
    cases.append((2, 15, rand_grid(2, 15, 0, 9, 177062)))
    cases.append((5, 15, rand_grid(5, 15, 0, 10000, 177063)))
    cases.append((100, 1, rand_grid(100, 1, 0, 10000, 177064)))   # 单列：无横向可走
    cases.append((1, 1, [[7]]))
    cases.append((50, 15, rand_grid(50, 15, 0, 9, 177066)))
    return run_point(6, cases)


# ---------------- 点 7：中等规模（75% 子任务上限） ----------------
# T=5，n=50, m=15, a∈[0,9]
def gen7():
    cases = [rand_grid(50, 15, 0, 9, 177070 + t) for t in range(5)]
    return run_point(7, [(50, 15, g) for g in cases])


# ---------------- 点 8：中等规模（75% 子任务顶格） ----------------
# T=10，n=50, m=50, a∈[0,9]：T 上限 + 该子任务规模上限
def gen8():
    cases = [rand_grid(50, 50, 0, 9, 177080 + t) for t in range(10)]
    return run_point(8, [(50, 50, g) for g in cases])


# ---------------- 点 9：大规模随机（100% 顶格） ----------------
# T=10, n=m=100, a∈[0,10000] 随机
def gen9():
    cases = [rand_grid(100, 100, 0, 10000, 177090 + t) for t in range(10)]
    return run_point(9, [(100, 100, g) for g in cases])


# ---------------- 点 10：顶格特殊结构（卡常/子任务覆盖） ----------------
# T=10, n=m=100，10 种结构，覆盖 a≡1（5%）、a∈{0,1}（10%）、极值、
# 交替极值（放大 Bob 造墙收益）、有序结构等
def gen10():
    n = m = 100
    cases = []
    cases.append((n, m, [[1] * m for _ in range(n)]))                              # a≡1 子任务
    rnd = random.Random(177101)
    cases.append((n, m, [[rnd.randint(0, 1) for _ in range(m)] for _ in range(n)]))  # a<=1 子任务
    cases.append((n, m, [[10000] * m for _ in range(n)]))                           # 全上限
    cases.append((n, m, [[0] * m for _ in range(n)]))                               # 全 0
    cases.append((n, m, [[0 if (i + j) % 2 == 0 else 10000 for j in range(m)] for i in range(n)]))
    cases.append((n, m, [[j * 100 for j in range(m)] for _ in range(n)]))            # 行内递增
    cases.append((n, m, [[i * 100 for _ in range(m)] for i in range(n)]))            # 行间递增
    cases.append((n, m, [[(i * j) % 10001 for j in range(m)] for i in range(n)]))    # 对角结构
    rnd2 = random.Random(177109)
    cases.append((n, m, [[rnd2.choice([0, 1, 9999, 10000]) for _ in range(m)] for _ in range(n)]))
    cases.append((n, m, [[10000 - (i * 100 + j) % 10001 for j in range(m)] for i in range(n)]))
    return run_point(10, cases)


if __name__ == "__main__":
    assert os.path.exists(STD), "请先编译 std：g++ -O2 -std=c++17 std.cpp -o std"
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    print("ALL 10 POINTS OK (.in/.out 成对，行数=T，非空，std 重跑一致)")
