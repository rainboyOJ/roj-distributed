#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1733《连续数字区间》（目标 ROJ 题号 1733）测试数据生成器
#
# 题意：给定 1..n 的一个排列 a[1..n]。称区间 [l,r] 连续，若 a[l..r] 排序后是一列
#       连续的数（等价于 max(a[l..r]) - min(a[l..r]) == r - l）。
#       m 个询问，每个给 [x_i, y_i]，输出长度最短（同长度时左端点最大）的连续
#       区间 [l_i, r_i] ⊇ [x_i, y_i]。输出 m 行，每行 l_i r_i。
#
# 输入格式：第 1 行 n；第 2 行 n 个数（1..n 的排列）；第 3 行 m；之后 m 行每行 x y。
# 数据范围（content.md / config.json / 官方 OJ 页）：
#   30% 的数据：1 <= n, m <= 1000；
#   另外 40% 的数据：y_i = x_i + 1；
#   100% 的数据：1 <= n, m <= 100000，1 <= x_i <= y_i <= n，a 为 1..n 的排列。
#   限制 time 1000 ms / memory 512 MB。
#
# ---------------------------------------------------------------------------
# 10 个测试点的分层（从最小铺到顶格，详见 gen-report.md 的分层表）
# ---------------------------------------------------------------------------
#   点  层                       设计意图
#   --  -----------------------  ------------------------------------------------------
#   1   边界层（最小规模）       n=1, m=1：排列退化为单点，答案长度 1（全最小值）
#   2   边界层（题面特殊值）     题面【输入样例】原样（n=7，3 个询问），可手算
#   3   边界层（最小非退化）     n=2, m=3 的全枚举：单点×2 + 整段三种形态
#   4   小规模随机               n=m=20 随机排列 + 混合询问（单点/短区间/全随机）
#   5   小规模·子任务结构        n=m=1000（30% 子任务上限），**全部询问 y=x+1**
#                                （40% 子任务结构，同时贴着 30% 规模上限）
#   6   中等规模随机             n=m=10000 随机排列 + 混合询问（范围中间档）
#   7   大规模随机               n=m=100000 随机排列 + 混合询问（顶格规模）
#   8   大规模·子任务结构        n=m=100000，排列按「相邻块 {2j-1,2j}」构造，全部询问
#                                y=x+1：奇数 x 的答案闭式恰为 [x,x+1]（小块短答案），
#                                偶数 x 跨块（长答案），同一份数据同时覆盖长短两类答案
#   9   顶格层·有序结构          n=m=100000，a_i=i（全部区间连续），答案闭式 (x,y)
#   10  顶格层·最坏负载结构      n=m=100000，a=[n,1,2,…,n-1]，全部询问 x=1：
#                                每个询问的答案都是 [1,n]，m 个询问全部在 i=n 结算
#                                （线段树/堆的最坏负载 + 答案区间最长）
#
# 分层清单对照：点 1-3 为边界层（最小规模 / 题面声明的特殊值 / 最小非退化全枚举）；
# 点 4-5 小规模随机（含 40% 子任务结构）；点 6 中等；点 7-8 大规模；点 9-10 顶格。
# 全部数据 n, m <= 100000、排列为 1..n、1 <= x <= y <= n，不超过题面上限；
# std.cpp 的数组按上限开 100005（>= 1e5，含安全余量）。
#
# ---------------------------------------------------------------------------
# 生成方式与自检
# ---------------------------------------------------------------------------
# - cyaron：IO(file_prefix="problem", data_id=i) + io.output_gen("../std")，在 data/ 目录下
#   运行（cd data && python3 ../data.py）；运行前必须已编译好 ../std。
#   已知坑：std 不存在时 cyaron 会静默产出 0 字节 .out —— 本文件首行 assert 拦下这个问题。
# - 生成后有回读自检（纯 O(输入长度)，无 O(n^2) 循环）：
#   (a) 重新解析每个 .in：行数、n/m 大小、排列合法性（1..n 每个数恰一次）、
#       每个询问 1 <= x <= y <= n；
#   (b) 每个 .out 非空、**行数恰为 m**、每行恰 2 个整数；
#   (c) 包含性：l <= x 且 y <= r <= n（答案必须覆盖询问，必要判据，O(m)）；
#   (d) 闭式核对（与 std 完全无关的手推答案）：点 1 -> [1,1]；点 2 -> 题面【输出样例】；
#       点 3 -> 全枚举手推；点 8 -> 奇数 x 的询问闭式为 [x,x+1]（偶数 x 不核）；
#       点 9（有序排列）-> 每个询问恰为 (x,y)；点 10 -> 全部 [1,n]。
# - 随机点用独立种子 random.seed(173300 + 点号)，可精确复现。
# - 任务约定（本轮铁律）：不写 brute/对拍/stress 脚本、生成器内不做 O(n^2) 循环，
#   因此大点的正确性由闭式结构核对 + 包含性判据 + 样例验证共同保障（见 gen-report.md）。

import os
import random
import sys

from cyaron import *  # 引入CYaRon的库

N_MAX = 100000          # 题面上限：n <= 1e5
M_MAX = 100000          # 题面上限：m <= 1e5

# 题面【输入样例】原样（点 2）
SAMPLE_N = 7
SAMPLE_PERM = [3, 1, 7, 5, 6, 4, 2]
SAMPLE_QUERIES = [(3, 6), (7, 7), (1, 3)]
SAMPLE_ANSWER = [(3, 6), (7, 7), (1, 7)]   # 题面【输出样例】


def random_perm(n, rng):
    """1..n 的随机排列（O(n)）。"""
    p = list(range(1, n + 1))
    rng.shuffle(p)
    return p


def random_queries(n, m, rng):
    """m 个随机询问 (x, y)，1 <= x <= y <= n（O(m)）。"""
    qs = []
    for _ in range(m):
        x = rng.randint(1, n)
        y = rng.randint(x, n)
        qs.append((x, y))
    return qs


def mixed_queries(n, m, rng):
    """混合询问：约 1/3 单点 (x=y)、1/3 短区间（长度 1..20）、1/3 全随机区间。

    单点/短区间的答案通常较短、全随机区间的答案通常很长（随机排列下几乎跨满
    整个数组），两类混排使同一份数据同时覆盖「短答案」与「长答案」的求解路径。
    """
    qs = []
    for k in range(m):
        r = k % 3
        if r == 0:
            x = rng.randint(1, n)
            qs.append((x, x))
        elif r == 1:
            x = rng.randint(1, n)
            qs.append((x, min(n, x + rng.randint(1, 20))))
        else:
            x = rng.randint(1, n)
            qs.append((x, rng.randint(x, n)))
    return qs


def adjacent_queries(n, m, rng):
    """m 个 y = x+1 的询问（40% 子任务结构，O(m)）。"""
    return [(x, x + 1) for x in (rng.randint(1, n - 1) for _ in range(m))]


def build_point(i):
    """返回 (n, perm, queries, note, closed_form)：

    closed_form 为 None 或「与询问一一对应的期望答案」列表（手推闭式，与 std 无关）。
    """
    rng = random.Random(173300 + i)   # 每个点独立种子，可复现

    # ---------------- 点 1：边界层 · 最小规模 ----------------
    if i == 1:
        return (1, [1], [(1, 1)],
                "边界层：n=1, m=1（全最小值；排列退化为单点，答案长度 1）",
                [(1, 1)])

    # ---------------- 点 2：边界层 · 题面样例原样 ----------------
    if i == 2:
        return (SAMPLE_N, SAMPLE_PERM, SAMPLE_QUERIES,
                "边界层：题面【输入样例】原样（题面声明的特殊值，可手算）",
                SAMPLE_ANSWER)

    # ---------------- 点 3：边界层 · 最小非退化（n=2 全枚举） ----------------
    if i == 3:
        # 排列取 [2,1]（逆序）；查询枚举全部 3 种合法形态。
        # 手推：a=[2,1]，[1,1]={2} 连续、[2,2]={1} 连续、[1,2]={2,1} 连续；
        # 因长度最短优先，三个询问答案分别为 [1,1]、[2,2]、[1,2]。
        return (2, [2, 1], [(1, 1), (2, 2), (1, 2)],
                "边界层：n=2, m=3 全枚举（单点×2 + 整段，最小非退化规模）",
                [(1, 1), (2, 2), (1, 2)])

    # ---------------- 点 4：小规模随机（可手算量级） ----------------
    if i == 4:
        n = m = 20
        return (n, random_perm(n, rng), mixed_queries(n, m, rng),
                "小规模随机：n=m=20，随机排列 + 混合询问（单点/短区间/全随机，可手算量级）",
                None)

    # ---------------- 点 5：小规模·子任务结构（y=x+1，贴着 30% 上限） ----------------
    if i == 5:
        n = m = 1000
        return (n, random_perm(n, rng), adjacent_queries(n, m, rng),
                "小规模·子任务结构：n=m=1000（30% 上限），全部询问 y=x+1（40% 子任务）",
                None)

    # ---------------- 点 6：中等规模随机 ----------------
    if i == 6:
        n = m = 10000
        return (n, random_perm(n, rng), mixed_queries(n, m, rng),
                "中等规模随机：n=m=10000，范围中间档",
                None)

    # ---------------- 点 7：大规模随机（顶格规模） ----------------
    if i == 7:
        n = m = N_MAX
        return (n, random_perm(n, rng), mixed_queries(n, m, rng),
                "大规模随机：n=m=100000（顶格），随机排列 + 混合询问",
                None)

    # ---------------- 点 8：大规模·子任务结构（y=x+1 顶格 + 块结构） ----------------
    if i == 8:
        n = m = N_MAX
        # 排列按块构造：块 j 占位置 (2j-1, 2j)，含值 {2j-1, 2j}（块内随机调序）。
        # 于是块内两位置的值恰为两个连续值 -> 奇数 x 的询问 (x, x+1) 答案闭式 [x, x+1]；
        # 偶数 x 的询问跨块，答案通常很长。全部询问仍满足 y = x+1（40% 子任务顶格）。
        perm = []
        for j in range(n // 2):
            blk = [2 * j + 1, 2 * j + 2]
            rng.shuffle(blk)
            perm.extend(blk)
        qs = adjacent_queries(n, m, rng)
        # 闭式：奇数 x -> (x, x+1)；偶数 x 不核（None）。
        closed = [((x, x + 1) if x % 2 == 1 else None) for (x, _) in qs]
        return (n, perm, qs,
                "大规模·子任务结构：n=m=100000，块排列 {2j-1,2j}，全部询问 y=x+1"
                "（奇数 x 答案闭式 [x,x+1]）",
                closed)

    # ---------------- 点 9：顶格层 · 有序结构 ----------------
    if i == 9:
        n = m = N_MAX
        perm = list(range(1, n + 1))          # a_i = i：任何区间都连续
        qs = random_queries(n, m, rng)
        # 手推闭式：有序排列下 [x,y] 本身连续，且必须包含位置 x..y，
        # 任何长度等于 y-x 的区间只能是 [x,y] -> 答案恒为 (x, y)。
        return (n, perm, qs,
                "顶格层·有序结构：n=m=100000，a_i=i（全部区间连续），答案闭式 (x,y)",
                list(qs))

    # ---------------- 点 10：顶格层 · 最坏负载结构 ----------------
    if i == 10:
        n = m = N_MAX
        perm = [n] + list(range(1, n))        # a = [n, 1, 2, ..., n-1]
        qs = [(1, rng.randint(2, n)) for _ in range(m)]
        # 手推闭式：a[1]=n，其余位置是 1,2,…,n-1。任何覆盖位置 1..y（y>=2）的区间
        # 必有 l=1、r>=y，其值集为 {n} ∪ {1..r-1}，连续当且仅当 r=n。
        # 故所有询问答案恒为 [1,n]（答案区间最长 + m 个询问全部在 i=n 结算，
        # 是线段树/优先队列的最坏负载形态）。
        return (n, perm, qs,
                "顶格层·最坏负载：n=m=100000，a=[n,1..n-1]，全部询问 x=1 -> 答案恒 [1,n]",
                [(1, n)] * m)

    raise ValueError("未知测试点编号：%d" % i)


def write_input(io, n, perm, queries):
    """按题面格式写输入：n / 排列 / m / m 行询问。

    整串一次写入且 separator=""（cyaron 默认会在两次 input_write 的参数之间插空格，
    那会破坏点 2「.in 与题面【输入样例】逐字节一致」的核对）。O(输入长度)。
    """
    m = len(queries)
    text = (str(n) + "\n" +
            " ".join(map(str, perm)) + "\n" +
            str(m) + "\n" +
            "\n".join("%d %d" % (x, y) for (x, y) in queries) + "\n")
    io.input_write(text, separator="")


def check_in(text, n, perm, queries, idx, problems):
    """回读自检：结构、排列合法性、询问范围。O(输入长度)。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()                            # 末尾换行
    m = len(queries)
    if len(lines) != 3 + m:
        problems.append("点 %d：.in 行数 %d != %d" % (idx, len(lines), 3 + m))
        return None
    if lines[0].strip() != str(n):
        problems.append("点 %d：n 读出 %r != %d" % (idx, lines[0], n))
    got_perm = list(map(int, lines[1].split()))
    if sorted(got_perm) != list(range(1, n + 1)):
        problems.append("点 %d：第 2 行不是 1..n 的合法排列" % idx)
    if lines[2].strip() != str(m):
        problems.append("点 %d：m 读出 %r != %d" % (idx, lines[2], m))
    got_q = []
    for j in range(m):
        parts = lines[3 + j].split()
        if len(parts) != 2:
            problems.append("点 %d：第 %d 个询问不是 2 个数" % (idx, j + 1))
            continue
        x, y = map(int, parts)
        if not (1 <= x <= y <= n):
            problems.append("点 %d：询问 %d 越界：%d %d" % (idx, j + 1, x, y))
        got_q.append((x, y))
    if got_q != list(queries):
        problems.append("点 %d：读回的询问与构造不一致" % idx)
    return got_q


def check_out(text, queries, idx, problems):
    """回读自检：.out 非空、行数恰为 m、每行 2 个数、包含性 l<=x 且 y<=r<=n。O(m)。"""
    m = len(queries)
    if text == "":
        problems.append("点 %d：.out 为空（cyaron 静默空输出的坑！）" % idx)
        return None
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) != m:
        problems.append("点 %d：.out 行数 %d != m=%d" % (idx, len(lines), m))
        return None
    ans = []
    for j, ln in enumerate(lines):
        parts = ln.split()
        if len(parts) != 2:
            problems.append("点 %d：.out 第 %d 行不是 2 个数" % (idx, j + 1))
            continue
        l, r = map(int, parts)
        x, y = queries[j]
        if not (1 <= l <= x and y <= r <= n_of(idx)):
            problems.append("点 %d：答案 %d %d 未包含询问 %d %d" % (idx, l, r, x, y))
        ans.append((l, r))
    return ans


_N_CACHE = {}


def n_of(idx):
    return _N_CACHE[idx]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")

    # cyaron 的坑：std 不存在时 output_gen 会把 0 字节输出静默写进 .out
    if not os.path.exists("../std"):
        print("错误：../std 不存在，请先编译（g++ -O2 -std=c++17 std.cpp -o std）", file=sys.stderr)
        raise SystemExit(2)

    plan = {}
    problems = []
    for i in range(1, 11):
        n, perm, queries, note, closed = build_point(i)
        _N_CACHE[i] = n
        plan[i] = (n, perm, queries, note, closed)
        io = IO(file_prefix="problem", data_id=i)   # problemI.in / problemI.out
        write_input(io, n, perm, queries)
        io.output_gen("../std")                    # 运行 ../std 生成 .out
        io.close()                                 # 刷盘（文件名模式不会被删除）

    print("点 |    n |    m |         .in |        .out | 输出形态 / 设计意图")
    print("---+------+------+------------+------------+------------------------------------------")
    for i in range(1, 11):
        n, perm, queries, note, closed = plan[i]
        m = len(queries)
        in_path = os.path.join(data_dir, "problem%d.in" % i)
        out_path = os.path.join(data_dir, "problem%d.out" % i)
        raw_in = open(in_path, "r", encoding="utf-8", newline="").read()
        raw_out = open(out_path, "r", encoding="utf-8", newline="").read()

        got_q = check_in(raw_in, n, perm, queries, i, problems)
        ans = check_out(raw_out, queries, i, problems)

        # (d) 闭式核对（与 std 无关的手推答案；列表可含 None 表示该询问不核）
        if closed is not None and ans is not None:
            bad = next((j for j in range(len(closed))
                        if closed[j] is not None and ans[j] != closed[j]), None)
            if bad is not None:
                problems.append("点 %d：闭式核对失败，第 %d 项 %r != %r"
                                % (i, bad + 1, ans[bad], closed[bad]))

        # 点 2 额外逐字节核对：.in 即题面【输入样例】原文
        if i == 2:
            want = "7\n3 1 7 5 6 4 2\n3\n3 6\n7 7\n1 3\n"
            if raw_in != want:
                problems.append("点 2：.in 与题面【输入样例】不一致：%r" % raw_in)
            if raw_out != "3 6\n7 7\n1 7\n":
                problems.append("点 2：.out 与题面【输出样例】不一致：%r" % raw_out)

        stat = ""
        if ans:
            lens = [r - l + 1 for (l, r) in ans]
            stat = "答案长度 min %d / avg %.1f / max %d" % (
                min(lens), sum(lens) / float(len(lens)), max(lens))
        print("%2d | %5d | %5d | %10d | %10d | %s" % (
            i, n, m, len(raw_in.encode("utf-8")), len(raw_out.encode("utf-8")), stat))
        print("   |       |       |            |            | %s" % note)

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检全部通过：10/10 组 .in/.out 成对；.out 非空且行数 = m；")
    print("            排列合法性 / 询问范围 / 答案包含性 / 闭式核对（点 1,2,3,9,10）均一致。")


if __name__ == "__main__":
    main()
