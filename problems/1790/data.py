#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一本通 1790《序列划分》分层数据生成器。

分层（10 组，文件名固定 problem1.in/.out … problem10.in/.out）：
  1  边界最小：n=1，a=b=1，m=1                        → 答案 1
  2  边界最大单点：n=2，a=[2e9,1]，b=[2e9,1]，m=2e9   → 答案 2000000001（手算）
  3  小规模随机：n=1000，a,b∈[1,100]
  4  小规模 + 特殊性质2 min(b)>max(a)：n=1000        （此时条件①恒成立，全部切点合法）
  5  小规模 + 特殊性质1 a 严格递减：n=1000
  6  中等规模随机：n=20000，a∈[1,1e6]，b∈[1,2e9]
  7  中等规模 + min(b)>max(a)：n=20000
  8  大规模 + a 严格递减 + b 顶格：n=100000
  9  大规模随机（题面「a_i、b_i 在 [1,1e9] 内均匀随机」）：n=100000
  10 顶格：n=100000，a 严格递减（2e9→1e5），b=2e9，m=1e12

m 的取法：先按题面把序列压成「原子段」（相邻合法切点之间），
  记 C = max a（最粗划分的 Σmax(a)）、F = Σ_原子段 max(a)（最细划分的 Σmax(a)）。
  合法划分要求 C ≤ m；取 m = clamp(C + (min(F,1e12)-C)*frac, C, 1e12)，
  使答案非平凡（既不是必须全切开、也不是只能合成一段）。
  若 F==C（只有一个原子段）则 m=C。

输出用 subprocess 显式跑 ../std 生成，并断言 .out 非空且恰好一行。
"""

import os
import random
import subprocess

from cyaron import IO  # 仓库惯例：cyaron 生成输入

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
MAXM = 10 ** 12
BIG = 2 * 10 ** 9


def atom_stats(a, b):
    """返回 (C, F)：C = max a；F = Σ 原子段 max a（原子段由合法切点划分）。

    合法切点 c ⟺ min_{i≤c} b_i > max_{j>c} a_j（题面条件①的等价形式）。
    纯 O(n) 循环，无平方级操作。
    """
    n = len(a)
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = a[i] if a[i] > suf[i + 1] else suf[i + 1]
    F = 0
    cur = 0
    cnt = 0
    premin = 1 << 62
    for i in range(n):
        if a[i] > cur:
            cur = a[i]
        if b[i] < premin:
            premin = b[i]
        last = (i == n - 1)
        if last or premin > suf[i + 1]:
            F += cur
            cur = 0
            cnt += 1
    return max(a), F, cnt


def pick_m(a, b, frac):
    C, F, _ = atom_stats(a, b)
    hi = min(F, MAXM)
    if hi <= C:
        return C
    return int(C + (hi - C) * frac)


def emit(idx, a, b, m, note):
    n = len(a)
    atoms = atom_stats(a, b)[2]
    io = IO(file_prefix="problem", data_id=idx)
    parts = ["%d %d" % (n, m)]
    parts.extend("%d %d" % (a[i], b[i]) for i in range(n))
    io.input_write("\n".join(parts) + "\n")
    io.input_file.flush()                      # cyaron 写缓冲：显式 flush，避免 .in 尚未落盘
    os.fsync(io.input_file.fileno())
    inp = os.path.join(os.getcwd(), "problem%d.in" % idx)
    outp = os.path.join(os.getcwd(), "problem%d.out" % idx)
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        subprocess.run([STD], stdin=fi, stdout=fo, check=True)
    with open(outp) as f:
        text = f.read()
    lines = text.strip().split("\n")
    assert text.strip() != "", "problem%d.out 为空" % idx
    assert len(lines) == 1, "problem%d.out 行数异常: %d" % (idx, len(lines))
    assert lines[0].lstrip("-").isdigit(), "problem%d.out 非整数: %r" % (idx, lines[0])
    print("problem%d  n=%-6d m=%-14d 原子段=%-6d ans=%-16s %s"
          % (idx, n, m, atoms, lines[0], note))


def main():
    random.seed(20240518)
    assert os.path.exists(STD), "请先编译 std"

    # ---- 1 边界最小：n=1，a=b=1，m=1 ----
    emit(1, [1], [1], 1, "边界 n=1 最小取值，答案 1")

    # ---- 2 边界最大：n=2，权值顶格，m=max(a) ----
    # 切点 c=1 合法（min b = 2e9 > max a[2..2] = 1），但切开后 Σmax(a) = 2e9+1 > m，
    # 只能合成一段 → 答案 = b1+b2 = 2000000001（手算）。
    emit(2, [BIG, 1], [BIG, 1], BIG, "边界 n=2 顶格权值（手算 2000000001）")

    # ---- 3 题面样例：n=4，m=6，答案 9 ----
    emit(3, [4, 3, 2, 2], [3, 5, 5, 4], 6, "题面样例，答案 9")

    # ---- 4 小规模随机：n=1000，a,b∈[1,100] ----
    n = 1000
    a = [random.randint(1, 100) for _ in range(n)]
    b = [random.randint(1, 100) for _ in range(n)]
    emit(4, a, b, pick_m(a, b, 0.5), "小规模随机 a,b∈[1,100]")

    # ---- 5 小规模 + 特殊性质2 min(b)>max(a)（条件①恒成立，全部切点合法） ----
    n = 1000
    a = [random.randint(1, 500) for _ in range(n)]
    b = [random.randint(501, 1000) for _ in range(n)]
    emit(5, a, b, pick_m(a, b, 0.6), "小规模 min(b)>max(a)")

    # ---- 6 小规模 + 特殊性质1 a 严格递减 ----
    n = 1000
    a = [10 ** 9 - 10 ** 6 * (i + 1) for i in range(n)]
    b = [random.randint(1, 10 ** 9) for _ in range(n)]
    emit(6, a, b, pick_m(a, b, 0.5), "小规模 a 严格递减")

    # ---- 7 中等规模随机：n=20000，a 量级小 / b 量级大（合法切点较多） ----
    n = 20000
    a = [random.randint(1, 10 ** 6) for _ in range(n)]
    b = [random.randint(1, 2 * 10 ** 9) for _ in range(n)]
    emit(7, a, b, pick_m(a, b, 0.5), "中等随机 a∈[1,1e6] b∈[1,2e9]")

    # ---- 8 中等规模 + min(b)>max(a)：n=20000 ----
    n = 20000
    a = [random.randint(1, 10 ** 9) for _ in range(n)]
    b = [random.randint(10 ** 9 + 1, 2 * 10 ** 9) for _ in range(n)]
    emit(8, a, b, pick_m(a, b, 0.5), "中等 min(b)>max(a)")

    # ---- 9 大规模随机（题面：a_i、b_i 在 [1,1e9] 内均匀随机）：n=100000 ----
    n = 100000
    a = [random.randint(1, 10 ** 9) for _ in range(n)]
    b = [random.randint(1, 10 ** 9) for _ in range(n)]
    emit(9, a, b, pick_m(a, b, 0.5), "大 a,b 均匀随机 [1,1e9]")

    # ---- 10 顶格：n=1e5，a 严格递减（2e9→1e5），b=2e9，m=1e12 ----
    n = 100000
    a = [BIG - 2 * (i + 1) for i in range(n)]
    b = [BIG] * n
    emit(10, a, b, MAXM, "顶格 n=1e5 a 递减 b=2e9 m=1e12")


if __name__ == "__main__":
    main()
