#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1749《矩阵求和》分层测试数据生成器
# 运行：cd data && python3 ../data.py      （std 在上一级目录，io.output_gen("../std")）
#
# ---------------------------------------------------------------------------
# 题面数据范围（content.md【提示】）：
#   30%  N <= 50
#   50%  N <= 3000
#   100% N <= 100000，0 <= A_i, B_i <= 10^7
# 输入：第 1 行 N；第 2 行 N 个整数 A；第 3 行 N 个整数 B。
# 输出：一行 N 个整数 F[1..N] mod 1e9+7。
# 时限 1000 ms / 内存 128 MB（config.json）。
#
# 标程思路（详见 std.cpp 头注与 gen-report.md）：
#   C_ij = (A_i + i)(B_j + j) = X_i * Y_j，X,Y > 0 ⇒
#   F[k] = (所有长度 k 的 X 窗最大值之和) * (所有长度 k 的 Y 窗最大值之和)。
#   故数据设计重点：值域两端、大量并列值（单调栈去重口径）、单调结构（栈深极端）、
#   顶格 N=1e5 的随机与全等结构。
#
# 分层设计（10 个测试点，由边界铺到顶格；每点独立种子，逐字节可复现）：
#   点 1  N=1       边界层：最小值 A=B=[0]（答案 F[1]=1，已用闭式核对）
#   点 2  N=2       边界层：值域顶格 A=B=[1e7,1e7]（答案用闭式核对）
#   点 3  N=10      小规模随机：值域 0..20（可手算/小规模核对量级）
#   点 4  N=50      小规模全相等：A 全 7、B 全 3（题面 30% 档；最坏并列，
#                   考察「最右最大值」去重口径）
#   点 5  N=3000    中等规模随机：值域 0..1e7（题面 50% 档 N<=3000）
#   点 6  N=3000    中等规模结构化：A 严格递增、B 严格递减 ⇒ X 严格递增、Y 严格递减
#                   （单调栈退化为单侧最长链，栈深极端）
#   点 7  N=90000   大规模 + 大量重复：值域 0..1000（海量并列，压力集中在计数口径）
#   点 8  N=100000  顶格随机：值域 0..1e7（上限 N 的随机最坏期望）
#   点 9  N=100000  顶格全最大值：A=B 全 1e7（答案数值量级最大，X 严格递增）
#   点 10 N=100000  顶格全等结构：A_i=B_i=1e7-i ⇒ X_i=Y_i≡1e7 全相等
#                   （单调栈退化到 O(n) 单链 + 全并列，计数口径最坏）
# ---------------------------------------------------------------------------
import os
import random
import subprocess
import sys
import time

from cyaron import IO

MOD = 10 ** 9 + 7
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STD = os.path.join(BASE_DIR, "std")
MAXV = 10 ** 7
MAXN = 100000


def check_std():
    """⚠ cyaron 的 output_gen 在 std 缺失时会静默产出 0 字节 .out，必须先校验。"""
    if not os.path.isfile(STD):
        sys.exit("[FATAL] 标程不存在：%s（先 g++ -O2 -std=c++17 std.cpp -o std）" % STD)
    if not os.access(STD, os.X_OK):
        sys.exit("[FATAL] 标程不可执行：%s" % STD)
    # 冒烟测试：n=1 必须输出 "1"
    r = subprocess.run([STD], input="1\n0\n0\n", capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or r.stdout.strip() != "1":
        sys.exit("[FATAL] 标程冒烟测试失败：rc=%s out=%r" % (r.returncode, r.stdout))


def gen(idx, n, A, B, note, expect=None):
    """生成第 idx 组数据并校验产物。expect 为手工/闭式推出的期望输出（可选）。"""
    assert len(A) == n, "A 长度 %d != n %d" % (len(A), n)
    assert len(B) == n, "B 长度 %d != n %d" % (len(B), n)
    assert all(0 <= v <= MAXV for v in A) and all(0 <= v <= MAXV for v in B), "值域越界"
    assert 1 <= n <= MAXN, "n 越界"

    t0 = time.time()
    # 必须用 with 收尾：cyaron 的 IO 缓冲要 close 时才落盘，
    # 否则下面从另一个句柄读 .out 会看到 0 字节（易误判为 std 缺失）。
    with IO(file_prefix="problem", data_id=idx) as io:
        io.input_writeln(n)
        io.input_writeln(" ".join(map(str, A)))
        io.input_writeln(" ".join(map(str, B)))
        io.output_gen("../std")
    dt = time.time() - t0

    inp = os.path.join(DATA_DIR, "problem%d.in" % idx)
    outp = os.path.join(DATA_DIR, "problem%d.out" % idx)

    # ---- 输入文件校验 ----
    with open(inp, "r") as f:
        lines = f.read().split("\n")
    lines = [ln for ln in lines if ln.strip() != ""]
    assert len(lines) == 3, "点%d .in 行数 %d != 3" % (idx, len(lines))
    assert lines[0].strip() == str(n), "点%d .in 首行 != n" % idx
    assert len(lines[1].split()) == n and len(lines[2].split()) == n, "点%d .in 数组长度错" % idx

    # ---- 输出文件校验（防 output_gen 静默产出空文件）----
    if not os.path.exists(outp):
        sys.exit("[FATAL] 点%d 缺少 .out" % idx)
    size = os.path.getsize(outp)
    if size == 0:
        sys.exit("[FATAL] 点%d .out 为 0 字节（std 缺失或崩溃？）" % idx)
    with open(outp, "r") as f:
        raw = f.read()
    body = raw.rstrip("\n")
    assert "\n" not in body, "点%d .out 不是单行输出" % idx
    toks = body.split()
    assert len(toks) == n, "点%d .out 数字个数 %d != n %d" % (idx, len(toks), n)
    vals = [int(t) for t in toks]
    assert all(0 <= v < MOD for v in vals), "点%d .out 存在越界值" % idx

    if expect is not None:
        got = " ".join(map(str, vals))
        assert got == expect, "点%d 闭式期望不符\n got: %s\n exp: %s" % (idx, got[:200], expect[:200])

    print("点%-2d N=%-6d %-40s %.2fs  首值=%s 末值=%s" % (
        idx, n, note, dt, vals[0], vals[-1]))


def rnd_list(rng, n, lo, hi):
    return [rng.randint(lo, hi) for _ in range(n)]


def main():
    check_std()
    os.makedirs(DATA_DIR, exist_ok=True)
    os.chdir(DATA_DIR)

    # 点 1：边界最小。X=Y=[1] ⇒ F[1]=1
    gen(1, 1, [0], [0], "边界层 N=1 最小值", expect="1")

    # 点 2：边界最大（值域顶格）。X=Y=[10000001,10000002]
    #   S[1]=20000003, S[2]=10000002 ⇒ F[1]=20000003^2, F[2]=10000002^2 (mod 1e9+7)
    exp2 = "%d %d" % ((20000003 ** 2) % MOD, (10000002 ** 2) % MOD)
    gen(2, 2, [MAXV, MAXV], [MAXV, MAXV], "边界层 N=2 值域顶格", expect=exp2)

    # 点 3：小规模随机（值域 0..20，可手算核对量级）
    rng = random.Random(174900 + 3)
    gen(3, 10, rnd_list(rng, 10, 0, 20), rnd_list(rng, 10, 0, 20), "小规模随机 N=10 值域[0,20]")

    # 点 4：小规模全相等（最坏并列，考察去重口径）
    gen(4, 50, [7] * 50, [3] * 50, "小规模全相等 N=50 A≡7 B≡3")

    # 点 5：中等规模随机（题面 50% 档 N<=3000）
    rng = random.Random(174900 + 5)
    gen(5, 3000, rnd_list(rng, 3000, 0, MAXV), rnd_list(rng, 3000, 0, MAXV),
        "中等随机 N=3000 值域[0,1e7]")

    # 点 6：中等规模结构化，A 严格递增 / B 严格递减（单调栈退化单侧长链）
    n6 = 3000
    A6 = [(i - 1) * 3333 for i in range(1, n6 + 1)]
    B6 = [MAXV - (i - 1) * 3333 for i in range(1, n6 + 1)]
    gen(6, n6, A6, B6, "中等结构化 N=3000 A递增/B递减")

    # 点 7：大规模 + 海量重复值（值域 0..1000）
    rng = random.Random(174900 + 7)
    gen(7, 90000, rnd_list(rng, 90000, 0, 1000), rnd_list(rng, 90000, 0, 1000),
        "大规模重复 N=90000 值域[0,1000]")

    # 点 8：顶格随机（N 上限 + 值域上限）
    rng = random.Random(174900 + 8)
    gen(8, MAXN, rnd_list(rng, MAXN, 0, MAXV), rnd_list(rng, MAXN, 0, MAXV),
        "顶格随机 N=1e5 值域[0,1e7]")

    # 点 9：顶格全最大值（答案数值量级最大）
    gen(9, MAXN, [MAXV] * MAXN, [MAXV] * MAXN, "顶格全最大 N=1e5 A≡B≡1e7")

    # 点 10：顶格全等结构（X_i=Y_i≡1e7 全相等 ⇒ 全并列 + 单调栈单链）
    A10 = [MAXV - i for i in range(1, MAXN + 1)]
    gen(10, MAXN, A10, list(A10), "顶格全等 N=1e5 A_i=B_i=1e7-i")

    # ---- 总清单核对 ----
    missing = []
    for i in range(1, 11):
        for ext in (".in", ".out"):
            p = "problem%d%s" % (i, ext)
            if not os.path.exists(p) or os.path.getsize(p) == 0:
                missing.append(p)
    if missing:
        sys.exit("[FATAL] 缺失/空文件：%s" % missing)
    print("OK: 10 组 .in/.out 全部非空且格式校验通过")


if __name__ == "__main__":
    main()
