#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 1787《保龄球》（ROJ 1787）测试数据生成器。

题意（详见 content.md / std.cpp 头注）：
  一排 n 个球瓶，第 i 个分值 a[i]（-10000..10000）。k 个球，每个球宽 w：
  一个球恰好占据「连续 w 个位置」的一段，把该段上仍立着的球瓶击倒并得到其分值之和；
  被击倒的球瓶留下空位，球可以经过空位（空位不得分）；球瓶 1 左边、球瓶 n 右边也有
  足够空位（球可以越出整排球瓶的边界）。求投完球后的最大总分。
  多组数据：第一行 t(1≤t≤10)，每组第一行 n k w，随后 n 行每行一个分值。
  数据范围：1≤n≤10000, 1≤k≤500, 1≤w≤100, -10000≤分值≤10000。

生成方式（重要工程决策）：
  * .in 用 cyaron 的 IO(file_prefix="problem", data_id=i) 写（problem{i}.in），
    io.close() 显式关闭，确保缓冲落盘；
  * .out **不用** io.output_gen，而是用 subprocess 显式运行已编译的 ../std 生成
    （cyaron 的 output_gen 若不 flush 会留下 0 字节 .out，本脚本绕开该隐患），
    并断言 .out 非空、行数 == 该点的 t。
  * 每组数据用独立随机种子 random.Random(1787 + 点号)，与调用顺序无关，可复现。

10 个测试点的分层（从最小铺到顶格，详见 gen-report.md 的分层表）：
  点  层            规模/结构                                          期望答案来源
  --  ------------  ------------------------------------------------  ----------------------
  1   边界层        t=1, n=1,k=1,w=1, a=[7]                           手算 7
  2   边界层        t=2, 题面【输入样例】原样                          手算 39 / 38
  3   边界层        t=2, 全负分值（n=10,k=3,w=5 / n=10,k=1,w=1）      手算 0 / 0（下界）
  4   边界层        t=1, n=10000,k=500,w=1, 全 +10000                 手算 5*10^6
  5   小规模随机    t=3, n∈[5,60], k∈[1,6], w∈[1,6], 分值全范围      「段划分」独立实现复算
  6   小规模随机    t=2, n∈[100,200], k∈[10,20], w∈[1,10]             「段划分」独立实现复算
  7   中等规模      t=1, n=1000, k=50, w=10, 分值全范围                O(nk) 独立 Python 参考
  8   大规模        t=1, n=5000, k=200, w=50, 分值全正                手算 = 全部之和
  9   顶格层        t=10, 每组 n=10000,k=500,w=100 随机（最大总工作量）上界检查 + std 自产
  10  顶格层最坏结构 t=10, 每组 n=10000,k=500,w=100, 负分每 2w 个一个   手算 = 全部正分之和
"""

import math
import os
import random
import subprocess
import sys

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

MAXN, MAXK, MAXW, MAXV = 10000, 500, 100, 10000

# 题面【输入样例】（t=2）
SAMPLE_TESTS = [
    (9, 2, 3, [2, 8, 5, 1, 9, 6, 9, 3, 2]),
    (9, 3, 3, [2, 8, -5, 3, 5, 8, 4, 8, -6]),
]


# ==========================================================================
# 独立参考实现 A：「段划分」形式（与 std 的「按球扫描」DP 是**不同**的建模）
# ==========================================================================
# 一个球的窗口是「连续 w 个位置」的一段，故 k 个球能覆盖的位置集合 = k 个长度 w 的
# 区间的并；把它在（左右都补了空位的）延长线上取极大连通段，每段的长度必 ≥ w。
# 落在球瓶范围内的那些段：整段都在行内 ⇒ 长度 ≥ w；贴左端（从位置 1 开始）或贴右端
# （到位置 n 结束）的段可以短于 w（球有一部分在界外空位上）。
# 覆盖一行内 [l,r] 这一段所需的最少球数 = ceil((r-l+1)/w)。
# 于是问题化为：在 1..n 上选若干互不相交、且满足「长度 ≥ w 或贴边界」的段，总球数 ≤ k，
# 最大化段内分值之和。这个 O(n^2 k) 的 DP 与 std 的 O(nk) 递推是两种独立写法。
def ref_runs(a, n, k, w):
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + a[i]
    NEG = float("-inf")
    D = [[NEG] * (k + 1) for _ in range(n + 1)]   # D[i][j]：1..i 内用至多 j 个球
    for j in range(k + 1):
        D[0][j] = 0
    for i in range(1, n + 1):
        for j in range(k + 1):
            best = D[i - 1][j]                    # 位置 i 不覆盖
            for l in range(1, i + 1):
                L = i - l + 1
                if not (L >= w or l == 1 or i == n):
                    continue                      # 行中间的短段不合法
                c = (L + w - 1) // w
                if c > j:
                    continue
                v = D[l - 1][j - c] + P[i] - P[l - 1]
                if v > best:
                    best = v
            D[i][j] = best
    return D[n][k]


# ==========================================================================
# 独立参考实现 B：与 std 同一递推的独立 Python 写法（用于中等规模点，O(k·n)）
#   A[i] = 第 j 个球窗口右端点恰为 i 时的最优值（重叠转移只能从 A 来：上一球窗口
#          覆盖 [p-w+1,p] ⊇ [i-w+1,p]，所以本球压住的位置确实已打空）
#   B[i] = 所有窗口右端点 ≤ i 时的最优值（至多 j 个球）
# ==========================================================================
def ref_dp(a, n, k, w):
    N = n + w - 1
    P = [0] * (N + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + a[i]
    for i in range(n + 1, N + 1):
        P[i] = P[n]
    NEG = float("-inf")
    prevA = [NEG] * (N + 1)
    prevB = [0] * (N + 1)
    for _ in range(k):
        curA = [NEG] * (N + 1)
        curB = [0] * (N + 1)
        for i in range(1, N + 1):
            lo = max(0, i - w + 1)
            best = max([prevA[p] - P[p] for p in range(lo, i)] + [NEG])
            best = best + P[i] if best != NEG else NEG
            q = max(0, i - w)
            best = max(best, prevB[q] + P[i] - P[q])
            curA[i] = best
            curB[i] = max(curB[i - 1], best)
        prevA, prevB = curA, curB
    return prevB[N]


# ==========================================================================
# 10 个测试点的构造
# ==========================================================================
def build_point(i):
    """返回 (tests, note, expected)；tests 为 [(n,k,w,[a1..an]), ...]，
    expected 为手算/结构可确定的答案列表（None 表示由参考实现复算）。"""
    if i == 1:                                    # 边界层：最小规模
        return ([(1, 1, 1, [7])],
                "边界层：最小规模 n=1,k=1,w=1，唯一球瓶 +7 -> 7",
                [7])

    if i == 2:                                    # 边界层：题面样例原样
        return (list(SAMPLE_TESTS),
                "边界层：题面【输入样例】原样（t=2）-> 39 / 38（题面声明的特殊值）",
                [39, 38])

    if i == 3:                                    # 边界层：答案为 0 的下界
        return ([(10, 3, 5, [-MAXV] * 10), (10, 1, 1, [-1] * 10)],
                "边界层：全负分值（t=2）-> 0 / 0（把球扔进空位，答案 0 是最小可能值）",
                [0, 0])

    if i == 4:                                    # 边界层：w=1 最小宽度 + 全最大分值
        vals = [MAXV] * MAXN
        return ([(MAXN, MAXK, 1, vals)],
                "边界层：w=1（最小宽度）+ 全为最大分值，k=500<n=10000 -> 恰取 500 个球瓶 = 5*10^6",
                [MAXK * MAXV])

    if i == 5:                                    # 小规模随机（可复算）
        rnd = random.Random(1787 + 5)
        tests = []
        for _ in range(3):
            n = rnd.randint(5, 60)
            k = rnd.randint(1, 6)
            w = rnd.randint(1, 6)
            tests.append((n, k, w, [rnd.randint(-MAXV, MAXV) for _ in range(n)]))
        return (tests,
                "小规模随机（t=3）：n∈[5,60], k∈[1,6], w∈[1,6]，分值全范围 -> 「段划分」独立实现复算",
                None)

    if i == 6:                                    # 小规模随机（稍大，仍可 O(n^2 k) 复算）
        rnd = random.Random(1787 + 6)
        tests = []
        for _ in range(2):
            n = rnd.randint(100, 200)
            k = rnd.randint(10, 20)
            w = rnd.randint(1, 10)
            tests.append((n, k, w, [rnd.randint(-MAXV, MAXV) for _ in range(n)]))
        return (tests,
                "小规模随机（t=2）：n∈[100,200], k∈[10,20], w∈[1,10] -> 「段划分」独立实现复算",
                None)

    if i == 7:                                    # 中等规模
        rnd = random.Random(1787 + 7)
        tests = [(1000, 50, 10, [rnd.randint(-MAXV, MAXV) for _ in range(1000)])]
        return (tests,
                "中等规模：n=1000, k=50, w=10，分值全范围 -> O(nk) 独立 Python 参考复算",
                None)

    if i == 8:                                    # 大规模（全正 => 可铺满，答案=总和）
        rnd = random.Random(1787 + 8)
        vals = [rnd.randint(1, MAXV) for _ in range(5000)]
        return ([(5000, 200, 50, vals)],
                "大规模：n=5000, k=200, w=50，分值全正且 k*w=10000≥n -> 能覆盖全部球瓶，答案=总和",
                [sum(vals)])

    if i == 9:                                    # 顶格层：最大总工作量
        rnd = random.Random(1787 + 9)
        tests = []
        for _ in range(10):
            tests.append((MAXN, MAXK, MAXW,
                          [rnd.randint(-MAXV, MAXV) for _ in range(MAXN)]))
        return (tests,
                "顶格层：t=10，每组 n=10000,k=500,w=100 顶格随机（t·k·(n+w) 最大总工作量）"
                " -> 上界检查（0 ≤ 答案 ≤ 全部正分之和）+ std 自产",
                None)

    # 点 10：顶格层 + 最坏结构（负分球瓶每 2w 个一个）
    rnd = random.Random(1787 + 10)
    tests = []
    for t in range(10):
        n, k, w = MAXN, MAXK, MAXW
        vals = []
        for pos in range(1, n + 1):
            if pos % (2 * w) == w:                # 位置 ≡ w (mod 2w) -> 负分
                vals.append(-MAXV)
            elif t % 2 == 0:
                vals.append(MAXV)
            else:
                vals.append(rnd.randint(1, MAXV))
        tests.append((n, k, w, vals))
    exp = [sum(v for v in vals if v > 0) for (_, _, _, vals) in tests]
    return (tests,
            "顶格层最坏结构：t=10，n=10000,k=500,w=100；负分球瓶每 2w=200 个一个"
            "（位置 ≡ w mod 2w），其余为正 -> 最优解必须用「左溢出」+「重叠复用上一球留下的"
            "空位」才能一个负分都不吃，答案=全部正分之和",
            exp)


# ==========================================================================
# 生成 + 自检
# ==========================================================================
def write_in(path, tests):
    """用 cyaron 写 .in（problem{i}.in），显式 close 保证落盘。"""
    io = IO(input_file=path, disable_output=True)
    io.input_writeln(len(tests))
    for (n, k, w, vals) in tests:
        io.input_writeln(n, k, w)
        io.input_writeln(*vals, separator="\n")   # 题面格式：每行一个分值
    io.close()


def run_std(in_path, out_path):
    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        r = subprocess.run([STD], stdin=fin, stdout=fout, timeout=120)
    return r.returncode


def main():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(STD):
        print("请先编译标程：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std", file=sys.stderr)
        raise SystemExit(2)

    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    rows = []
    for i in range(1, 11):
        tests, note, exp = build_point(i)
        in_path = os.path.join(DATA, "problem%d.in" % i)
        out_path = os.path.join(DATA, "problem%d.out" % i)
        write_in(in_path, tests)
        rc = run_std(in_path, out_path)
        check(rc == 0, "点 %d：std 退出码 %s" % (i, rc))

        raw_out = open(out_path, "r", encoding="utf-8").read()
        check(len(raw_out.strip()) > 0, "点 %d：.out 为空" % i)
        got = [int(x) for x in raw_out.split()]
        check(len(got) == len(tests),
              "点 %d：.out 行数 %d != 测试组数 %d" % (i, len(got), len(tests)))

        # ---- 回读 .in 并严格解析：确认格式与构造完全一致（防缓冲/换行问题）----
        toks = open(in_path, "r", encoding="utf-8").read().split()
        pos = 0
        check(int(toks[pos]) == len(tests), "点 %d：.in 首行 t 不符" % i)
        pos += 1
        for (n, k, w, vals) in tests:
            check((int(toks[pos]), int(toks[pos + 1]), int(toks[pos + 2])) == (n, k, w),
                  "点 %d：.in 中 n k w 不符" % i)
            pos += 3
            seg = [int(x) for x in toks[pos:pos + n]]
            check(seg == vals, "点 %d：.in 中分值序列不符" % i)
            pos += n
        check(pos == len(toks), "点 %d：.in 尾部有多余 token" % i)

        # ---- 参考实现复算（按规模选择）----
        if exp is not None:
            want, how = list(exp), "手算/结构"
            check(got == want, "点 %d：std 输出 %s != 期望 %s（%s）" % (i, got, want, how))
        elif i in (5, 6):
            want = [ref_runs([0] + vals, n, k, w) for (n, k, w, vals) in tests]
            check(got == want, "点 %d：std 输出 %s != 「段划分」独立实现 %s" % (i, got, want))
        elif i == 7:
            n, k, w, vals = tests[0]
            want = [ref_dp([0] + vals, n, k, w)]
            check(got == want, "点 %d：std 输出 %s != O(nk) 独立参考 %s" % (i, got, want))
        else:                                     # 点 9：只有上界可验
            for idx, (n, k, w, vals) in enumerate(tests):
                ub = sum(v for v in vals if v > 0)
                check(0 <= got[idx] <= ub,
                      "点 %d 第 %d 组：答案 %d 越界 [0, %d]" % (i, idx + 1, got[idx], ub))

        # ---- 分层结构性断言 ----
        t_in = len(tests)
        if i == 1:
            check(tests == [(1, 1, 1, [7])], "点 1 不是最小规模")
        elif i == 2:
            check([(n, k, w, v) for (n, k, w, v) in tests] == SAMPLE_TESTS,
                  "点 2 不是题面样例原样")
        elif i == 3:
            check(all(all(v < 0 for v in vals) for (_, _, _, vals) in tests),
                  "点 3 应为全负分值")
        elif i == 4:
            check(all(n == MAXN and k == MAXK and w == 1 and min(vals) == MAXV
                      for (n, k, w, vals) in tests), "点 4 结构不符")
        elif i == 8:
            check(all(min(vals) > 0 for (_, _, _, vals) in tests), "点 8 应为全正")
        elif i == 10:
            for (n, k, w, vals) in tests:
                for pos in range(1, n + 1):
                    if pos % (2 * w) == w:
                        check(vals[pos - 1] < 0, "点 10 位置 %d 应为负分" % pos)
                    else:
                        check(vals[pos - 1] > 0, "点 10 位置 %d 应为正分" % pos)
        for (n, k, w, vals) in tests:
            check(1 <= n <= MAXN and 1 <= k <= MAXK and 1 <= w <= MAXW,
                  "点 %d：n/k/w 越界" % i)
            check(len(vals) == n, "点 %d：分值个数 != n" % i)
            check(all(-MAXV <= v <= MAXV for v in vals), "点 %d：分值越界" % i)

        rows.append((i, t_in, note, got[0] if got else None,
                     os.path.getsize(in_path), os.path.getsize(out_path)))

    print("%-4s %-4s %-62s %-12s %-9s %-9s" %
          ("点", "t", "设计意图", "首组答案", ".in 字节", ".out 字节"))
    for (i, t_in, note, first, szin, szout) in rows:
        print("%-4d %-4d %-62s %-12s %-9d %-9d" % (i, t_in, note, first, szin, szout))

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对且非空，行数 == t，"
          "分层结构断言 + 手算期望值 + 独立参考实现复算 均一致。")


if __name__ == "__main__":
    main()
