#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1793《鏖战字符串》分层数据生成器（目标 ROJ 1793）
#
# 题面（content.md 摘要）：
#   第一行七个整数 n a b c d l r；第二行长度 n 的小写字符串；第三行 n 个整数 dif[i]。
#   把前缀 [1,i] 分割成若干连续子串，每段二选一删除：
#     ① 代价 a*x^2 + b （x = 段内 dif 之和）
#     ② 代价 c*x + d，当且仅当段内 maxfreq ∈ [l, r]
#   输出 n 行，第 i 行是删去前缀 [1,i] 的最少用时。
#
# 数据范围（题面「数据规模与约定」）：n<=100000，1<=a,b,c,d<=233，1<=l,r<=n，
#   0<=dif[i]<=50，全部小写字母。数组上限即题面上限（n=1e5），无安全系数放大需求
#   （题面已明确顶格 n=100000）。
#
# 分层设计（10 组：边界 2 / 小 4 / 中 2 / 大 2；每组含题面特殊结构）：
#   点 1  边界最小：n=1, dif=0
#   点 2  边界 + 常数顶格：n=2, dif 全 50, a=b=c=d=233
#   点 3  题面【输入样例】原样（n=5, "abwad"）——样例必测
#   点 4  小规模全同：n=10, 全 'a', l=r=1
#   点 5  小规模 {a,b} 随机
#   点 6  小规模随机 26 字母 + 随机 l,r
#   点 7  中等规模全同：n=2000, 全 'a', dif 全 0（全 0 权，退化结构）
#   点 8  中等规模 {a,b} 随机 + l>r（方法② 恒失效分支）
#   点 9  顶格全同：n=100000, 全 'a', dif 全 50, l=1,r=n, 常数顶格 233
#   点 10 顶格随机：n=100000, 随机 26 字母, dif 随机, l>r
#
# .out 生成方式：**用 subprocess 显式跑 std**（不依赖 cyaron output_gen 的写缓冲），
#   并断言 .out 非空、行数恰为 n、每行均为合法非负整数（本题无「无解空输出」点）。
# 随机性：每点独立 Random(1793 + 点号)，可精确复现；生成过程全 O(n)，无 Python 嵌套循环。

import os
import random
import subprocess
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

NMAX = 100000  # 题面上限

_pts = []  # (i, n, note)


def _rand_str(rng, n, charset):
    return "".join(rng.choice(charset) for _ in range(n))


def _rand_difs(rng, n, lo=0, hi=50):
    return [rng.randint(lo, hi) for _ in range(n)]


def gen(i, n, a, b, c, d, l, r, s, difs, note):
    assert len(s) == n, "problem%d: 串长 %d != n %d" % (i, len(s), n)
    assert len(difs) == n, "problem%d: dif 个数不符" % i
    assert 1 <= a <= 233 and 1 <= b <= 233 and 1 <= c <= 233 and 1 <= d <= 233
    assert 1 <= l <= n and 1 <= r <= n
    assert all(0 <= v <= 50 for v in difs)

    io = IO(file_prefix=os.path.join(DATA, "problem"), data_id=i, disable_output=True)
    io.input_write("%d %d %d %d %d %d %d" % (n, a, b, c, d, l, r), "\n", s, "\n", difs, "\n")
    io.input_file.flush()  # 关键：显式 flush，确保 subprocess 读到完整 .in
    inpath = os.path.join(DATA, "problem%d.in" % i)
    outpath = os.path.join(DATA, "problem%d.out" % i)

    with open(inpath, "rb") as fin, open(outpath, "wb") as fout:
        proc = subprocess.run([STD], stdin=fin, stdout=fout, timeout=120)
    assert proc.returncode == 0, "problem%d: std 退出码 %d" % (i, proc.returncode)

    # ---- 断言 .out 非空 / 行数 == n / 每行非负整数 ----
    with open(outpath, "r") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == n, "problem%d: .out 行数 %d != n %d" % (i, len(lines), n)
    for t in lines:
        v = int(t)
        assert v >= 0, "problem%d: 出现负答案" % i

    _pts.append((i, n, note))
    print("problem%-2d: n=%-6d l=%-6d r=%-6d -- %s" % (i, n, l, r, note))


def main():
    os.makedirs(DATA, exist_ok=True)
    assert os.path.exists(STD), "未找到已编译的 std（先 g++ std.cpp -o std）"
    os.chdir(HERE)  # 固定工作目录，保证相对/绝对路径一致

    # ---- 点 1：边界最小 ----
    gen(1, 1, 1, 1, 1, 1, 1, 1, "a", [0],
        "边界层：n=1 最小规模，dif=0（全零权），l=r=1")

    # ---- 点 2：边界 + 常数顶格 ----
    gen(2, 2, 233, 233, 233, 233, 1, 2, "ab", [50, 50],
        "边界层：n=2，a=b=c=d=233 常数顶格，dif 全 50（单字符权重最大）")

    # ---- 点 3：题面输入样例原样（样例必测） ----
    gen(3, 5, 1, 3, 1, 5, 1, 1, "abwad", [1, 1, 1, 1, 1],
        "题面【输入样例】原样：期望输出 4/7/8/12/13")

    # ---- 点 4：小规模全同 ----
    gen(4, 10, 1, 3, 1, 5, 1, 1, "a" * 10, [1] * 10,
        "小规模：n=10 全 'a'（题面测试点 1 结构），l=r=1")

    # ---- 点 5：小规模 {a,b} 随机 ----
    rng = random.Random(1793 + 5)
    gen(5, 10, rng.randint(1, 233), rng.randint(1, 233), rng.randint(1, 233),
        rng.randint(1, 233), 1, 2, _rand_str(rng, 10, "ab"), _rand_difs(rng, 10),
        "小规模随机：n=10 字母集 {a,b}（题面测试点 2 结构），l=1,r=2")

    # ---- 点 6：小规模 26 字母随机 ----
    rng = random.Random(1793 + 6)
    gen(6, 10, rng.randint(1, 233), rng.randint(1, 233), rng.randint(1, 233),
        rng.randint(1, 233), 3, 7, _rand_str(rng, 10, "abcdefghijklmnopqrstuvwxyz"),
        _rand_difs(rng, 10), "小规模随机：n=10 全 26 字母，l=3,r=7（区间中部）")

    # ---- 点 7：中等规模全同 + 全零权 ----
    gen(7, 2000, 1, 1, 1, 1, 1, 2000, "a" * 2000, [0] * 2000,
        "中等规模：n=2000 全 'a'，dif 全 0，l=1,r=n（方法② 全程可用）")

    # ---- 点 8：中等规模 {a,b} + l>r ----
    rng = random.Random(1793 + 8)
    gen(8, 2000, rng.randint(1, 233), rng.randint(1, 233), rng.randint(1, 233),
        rng.randint(1, 233), 1000, 500, _rand_str(rng, 2000, "ab"), _rand_difs(rng, 2000),
        "中等规模：n=2000 字母集 {a,b}，l=1000>r=500（题面测试点 15 结构，方法② 恒失效）")

    # ---- 点 9：顶格全同 + 常数顶格 ----
    gen(9, NMAX, 233, 233, 233, 233, 1, NMAX, "a" * NMAX, [50] * NMAX,
        "顶格层：n=100000 全 'a'，dif 全 50（前缀和最大 5e6），l=1,r=n，常数顶格")

    # ---- 点 10：顶格随机 + l>r ----
    rng = random.Random(1793 + 10)
    gen(10, NMAX, rng.randint(1, 233), rng.randint(1, 233), rng.randint(1, 233),
        rng.randint(1, 233), 60000, 40000,
        _rand_str(rng, NMAX, "abcdefghijklmnopqrstuvwxyz"), _rand_difs(rng, NMAX),
        "顶格层：n=100000 随机 26 字母，dif 随机 0..50，l=60000>r=40000（大 l>r 分支）")

    # ---- 汇总自检 ----
    ins = set(f for f in os.listdir(DATA) if f.endswith(".in"))
    outs = set(f for f in os.listdir(DATA) if f.endswith(".out"))
    assert ins == set("problem%d.in" % k for k in range(1, 11)), sorted(ins)
    assert outs == set("problem%d.out" % k for k in range(1, 11)), sorted(outs)
    for f in sorted(ins) + sorted(outs):
        assert os.path.getsize(os.path.join(DATA, f)) > 0, "%s 为 0 字节" % f
    print("自检通过：10 组 .in/.out 成对齐全且均非空。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
