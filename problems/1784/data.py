#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1784《山谷》数据生成器
#
# 输入格式（多组数据，读到 EOF；题面保证"数据不超过 5 组"）：
#   每组：第 1 行 "n m"，接下来 n 行每行 m 个字符（'.' 或 'X'）
# 输出：每组一行答案（mod 998244353）。
# 数据范围：1<=n<=4，1<=m<=7（N=nm<=28），组数<=5。
#
# 分层（10 个测试点，见 gen-report.md 的分层表）：
#   点 1    最小边界层（N<=2，含 1x1 的两种答案 1/0）
#   点 2    题面样例层（必须复现 2 / 6）
#   点 3    30% 层（nm<=9）小规模随机
#   点 4    另外 30% 层（每个格子的闭八邻域内至少一个 X，且 X 独立 -> 答案非 0）
#   点 5-7  中规模层（3x4 / 3x5 / 4x4 / 4x5）
#   点 8    顶格层 4x7：X = 单个角格（"T ⊇ X 的独立超集"最多 4749 个，最坏枚举量）
#   点 9    顶格层 4x7：X = 最大独立集（8 格）/ X 全空（答案 0）
#   点 10   顶格层 4x7：7 格大独立集 / 相邻 X 非独立（答案 0）/ 全空（答案 0）
#
# 说明：本文件不写任何 brute/对拍/stress；只用 std 产出 .out。
# .out 一律用 subprocess 显式跑 ../std 生成（不依赖 cyaron 的 output_gen 写缓冲），
# 并对每个点断言 .out 非空、行数 == 组数；点 2 额外断言等于题面样例 2 / 6。

import os
import random
import subprocess
import sys

from cyaron import IO

STD = "../std"
NMAX, MMAX = 4, 7
MAXGROUPS = 5  # 题面：数据不超过 5 组

POINTS = []  # (i, groups, note)  groups: list[(n, m, [row,...])]


# ---------------------------------------------------------------- 工具函数
def closed_nbhd(n, m, i, j):
    """(i,j) 的闭八邻域（含自身）。"""
    return {(a, b)
            for a in range(max(0, i - 1), min(n, i + 2))
            for b in range(max(0, j - 1), min(m, j + 2))}


def is_independent(chosen):
    """国王图意义下的独立集：任意两格切比雪夫距离 >= 2。"""
    ch = list(chosen)
    for x in range(len(ch)):
        for y in range(x + 1, len(ch)):
            if max(abs(ch[x][0] - ch[y][0]), abs(ch[x][1] - ch[y][1])) <= 1:
                return False
    return True


def is_dominating(n, m, chosen):
    """每个格子的闭八邻域内至少有一个 X（题面"另外 30%"的特征）。"""
    return all(closed_nbhd(n, m, i, j) & chosen for i in range(n) for j in range(m))


def rand_independent(n, m, p, rng):
    """随机独立集：随机顺序贪心加入（与已选格子不相邻才加）。"""
    cells = [(i, j) for i in range(n) for j in range(m)]
    rng.shuffle(cells)
    chosen = set()
    for (i, j) in cells:
        if rng.random() < p and all(max(abs(i - a), abs(j - b)) > 1 for (a, b) in chosen):
            chosen.add((i, j))
    return chosen


def grid(n, m, chosen):
    return ["".join('X' if (i, j) in chosen else '.' for j in range(m)) for i in range(n)]


def full_independent(n, m, rng, p):
    """随机独立集，若为空则强制放一个随机格（保证 X 非空）。"""
    ch = rand_independent(n, m, p, rng)
    if not ch:
        ch = {(rng.randrange(n), rng.randrange(m))}
    return ch


def add_point(i, groups, note):
    assert 1 <= len(groups) <= MAXGROUPS, "点 %d 组数 %d 超出题面上限 5" % (i, len(groups))
    for (n, m, rows) in groups:
        assert 1 <= n <= NMAX and 1 <= m <= MMAX, "点 %d 尺寸越界 %dx%d" % (i, n, m)
        assert len(rows) == n and all(len(r) == m for r in rows)
        assert all(c in '.X' for r in rows for c in r)
    POINTS.append((i, groups, note))


# ---------------------------------------------------------------- 各点构造
# 点 1：最小边界层
add_point(1, [
    (1, 1, ["X"]),      # 单格无邻居：恒为山谷 -> 1
    (1, 1, ["."]),      # 单格必须为山谷，X 为空 -> 0（边界退化）
    (1, 2, ["X."]),     # X 在左：X < 右 -> 1
    (2, 1, [".", "X"]),  # X 在下：X < 上 -> 1
], "最小边界层：N<=2，含 1x1 的两种答案（1 与 0）与 1x2 / 2x1")

# 点 2：题面样例层（断言 == 2 / 6）
add_point(2, [
    (1, 3, ["X.X"]),
    (2, 2, ["X.", ".."]),
], "题面样例层：题面【输入样例】原样两组，输出必须为 2 / 6")

# 点 3：30% 层 nm<=9 小规模随机
rng = random.Random(1784 * 10 + 3)
g3 = []
for (n, m) in [(1, 3), (2, 3), (3, 3), (3, 2), (2, 2)]:
    assert n * m <= 9
    ch = full_independent(n, m, rng, 0.55)
    g3.append((n, m, grid(n, m, ch)))
add_point(3, g3, "30% 层（nm<=9）：小规模随机独立 X")

# 点 4：另外 30% 层：每个格子的闭八邻域至少一个 X（且 X 独立）
dom_cases = [
    (2, 2, {(0, 0)}),
    (3, 3, {(0, 0), (0, 2), (2, 0), (2, 2)}),
    (4, 7, {(0, 0), (0, 3), (0, 6), (3, 1), (3, 4), (3, 6)}),
]
g4 = []
for (n, m, ch) in dom_cases:
    assert is_independent(ch), "支配层样例必须 X 独立"
    assert is_dominating(n, m, ch), "支配层样例必须每个闭八邻域含 X"
    g4.append((n, m, grid(n, m, ch)))
add_point(4, g4, "另外 30% 层：每个格子闭八邻域至少 1 个 X（且 X 独立，答案非 0）")

# 点 5-7：中规模层
for (i, (n, m), cnt) in [(5, (3, 4), 4), (6, (4, 4), 5), (7, (4, 5), 5)]:
    rng = random.Random(1784 * 10 + i)
    gs = []
    for t in range(cnt):
        p = [0.35, 0.55, 0.8, 0.2][t % 4]
        ch = full_independent(n, m, rng, p)
        gs.append((n, m, grid(n, m, ch)))
    add_point(i, gs, "中规模层 %dx%d：不同密度随机独立 X" % (n, m))

# 点 8：顶格 4x7，X = 单个角格（独立超集最多，最坏枚举量）
rng = random.Random(1784 * 10 + 8)
g8 = [
    (4, 7, grid(4, 7, {(0, 0)})),
    (4, 7, grid(4, 7, {(3, 6)})),
    (4, 7, grid(4, 7, full_independent(4, 7, rng, 0.15))),
]
add_point(8, g8, "顶格层 4x7：X=单角格（最坏枚举量）+ 稀疏随机")

# 点 9：顶格 4x7，最大独立集 / X 全空
max_ind = {(0, 0), (0, 2), (0, 4), (0, 6), (2, 0), (2, 2), (2, 4), (2, 6)}
assert is_independent(max_ind) and len(max_ind) == 8
g9 = [
    (4, 7, grid(4, 7, max_ind)),
    (4, 7, grid(4, 7, set())),
]
add_point(9, g9, "顶格层 4x7：X=8 格最大独立集（|T| 取最大 k）+ X 全空（答案 0）")

# 点 10：顶格 4x7，7 格大独立集 / 相邻 X（非独立 -> 0）
big7 = {(0, 0), (0, 2), (0, 4), (0, 6), (2, 1), (2, 3), (2, 5)}
assert is_independent(big7) and len(big7) == 7
adj2 = {(1, 1), (1, 2)}   # 相邻两格 -> 非独立 -> 答案 0
assert not is_independent(adj2)
rng = random.Random(1784 * 10 + 10)
g10 = [
    (4, 7, grid(4, 7, big7)),
    (4, 7, grid(4, 7, adj2)),
    (4, 7, grid(4, 7, full_independent(4, 7, rng, 0.6))),
]
add_point(10, g10, "顶格层 4x7：7 格大独立集 / 相邻 X 非独立(0) / 高密度随机")

assert len(POINTS) == 10 and [p[0] for p in POINTS] == list(range(1, 11))


# ---------------------------------------------------------------- 写出数据
def emit(i, groups):
    io = IO(file_prefix="problem", data_id=i)
    text = ""
    for (n, m, rows) in groups:
        text += "%d %d\n" % (n, m)
        text += "\n".join(rows) + "\n"
    io.input_write(text)
    io.flush_buffer()

    inpath = "problem%d.in" % i
    outpath = "problem%d.out" % i
    assert os.path.getsize(inpath) > 0, "%s 为空" % inpath
    # 写缓冲隐患防护：回读并核对内容
    with open(inpath, "r") as f:
        assert f.read() == text, "%s 内容与预期不一致（写缓冲未落盘）" % inpath

    # 显式 subprocess 跑 std 产 .out（不依赖 cyaron output_gen）
    with open(inpath, "rb") as fin:
        r = subprocess.run([STD], stdin=fin, capture_output=True, timeout=120)
    assert r.returncode == 0, "std 在 %s 上返回 %d" % (inpath, r.returncode)
    out = r.stdout.decode()
    lines = [ln.strip() for ln in out.split("\n") if ln.strip() != ""]
    assert len(lines) == len(groups), \
        "%s 行数 %d != 组数 %d" % (outpath, len(lines), len(groups))
    assert all(ln.isdigit() and 0 <= int(ln) < 998244353 for ln in lines), \
        "%s 输出非法（应为 [0,998244353) 内整数）" % outpath
    with open(outpath, "w") as f:
        f.write("\n".join(lines) + "\n")
    return lines


print("%-4s %-22s %-6s %s" % ("点", "分层说明", "组数", "输出"))
for (i, groups, note) in POINTS:
    lines = emit(i, groups)
    print("%-4d %-22s %-6d %s" % (i, note, len(groups), " ".join(lines)))

# 题面样例断言
sample_out = [ln.strip() for ln in open("problem2.out") if ln.strip()]
assert sample_out == ["2", "6"], "题面样例验证失败：%s != ['2','6']" % sample_out
print("样例验证通过：problem2.out == 2 / 6（题面【输出样例】）")

# 数据规模与分层自检
for (i, groups, note) in POINTS:
    for (n, m, rows) in groups:
        assert n <= NMAX and m <= MMAX
    if i == 3:
        assert all(n * m <= 9 for (n, m, _) in groups), "点 3 必须满足 nm<=9"
    if i == 4:
        for (n, m, rows) in groups:
            ch = {(a, b) for a in range(n) for b in range(m) if rows[a][b] == 'X'}
            assert is_dominating(n, m, ch) and is_independent(ch)
print("自检通过：10 个点全部落盘，.out 非空且行数 == 组数，尺寸/分层特征符合题面约束。")
sys.stdout.flush()
