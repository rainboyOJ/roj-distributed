#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一本通 1759《采访计划》（目标 ROJ 题号 1759）测试数据生成器。

题意：n 个星球，长者 i 的名单 B_i ⊆ {1..i-1}（元素互不重复）。长者 i 管辖球长 i；
      对 j != i：i 管辖 j <=> (∀k∈B_i, k 管辖 j)；B_i = ∅ 时 S_i = {i}。
      m 个询问，每次给一个长者集合 T，求 |∪_{i∈T} S_i|（即被至少一位 T 中长者
      直接或间接管辖的球长个数）。标程解法（森林 + 虚树恒等式）见 std.cpp 头注。

数据范围（题面【数据规模及约定】）：
      n, m <= 200000；Σ|B_i| <= 2000000；询问中 Σsz_i <= 2000000。
      时间 2000 ms，内存 128 MB。

运行方式（cwd 必须是 data/ 目录，std 编译产物放在上一级）：
      cd .ybt-import/staging/1759/data && nice -n 19 timeout 120 python3 ../data.py

【关于 .out 的生成方式（重要）】
      本生成器**不使用** cyaron 的 IO.output_gen（该接口在写缓冲未 flush 时可能产出
      0 字节 .out），而是先显式写好 .in（显式 with/close），再用 subprocess 显式把
      std 的 stdout 重定向到 .out 文件，随后逐点断言：
        * std 退出码为 0；
        * .out 文件非空；
        * .out 行数恰等于该点的 m；
        * 有解析式的点（1/2/3/4/5/7/9/10）逐行与解析式结果比对；
        * 无解析式的点（6/8）校验每行答案落在 [1, n] 内。
      （本生成器按父任务铁律**不含**任何 brute/对拍/stress 程序，故随机大点的
        正确性只由「题面样例 + 上述解析式结构点」间接保证，详见 gen-report.md。）

分层（10 个点，从最小铺到顶格；每点用独立 Random(1759 + 点号)，可精确复现）：
      点 1  边界层：n=1（最小规模，B_1=∅），1 个询问
      点 2  边界层：n=2（最小非平凡），三种询问（单元素 / 全集合）
      点 3  题面【输入样例】原样（题面唯一声明值，可手算核对）
      点 4  小规模：20 个长度 5 的链段（n=100，深度 4）——解析式：段内 [段首, 最大元素]
      点 5  小规模：星形（n=200，B_i={1}）——解析式：1∈T ? |T| : |T|+1
      点 6  中规模：多树随机（n=5000，每 3 个点一个树根，约 1667 棵树）——覆盖跨树计数
      点 7  中规模：单链（n=20000，深度 19999）——解析式：max(T)
      点 8  大规模随机：n=m=200000，Σ|B|≈1e6，Σsz≈1e6
      点 9  顶格（深脊 + 宽 B 结构）：n=m=200000，Σ|B|=1999999（顶格），Σsz=2e6（顶格）；
            前 100000 个点构成深链（深度 1e5），其余 100000 个点的 B 取链上连续的 19 个点
            （⇒ 每个 B 都有 19 个元素、走集合 LCA 合并，且深度仍约 1e5）
            —— 大而深且多元素的顶格压力点
      点 10 顶格最坏结构：单链 n=200000（深度 199999，LCA 最坏）+ m=200000 个
            大小恰为 10 的询问（Σsz=2e6 顶格）——解析式：max(T)
"""

import os
import random
import subprocess
import sys

STD = os.path.abspath("../std")

MAXN = 200000
SUMB = 2000000  # Σ|B_i| 上限
SUMQ = 2000000  # 询问 Σsz_i 上限

stats = []  # (点号, n, m, Σ|B|, Σsz, 说明)


def open_in(i):
    return open("problem%d.in" % i, "w")


def run_std(i):
    """显式 subprocess 跑 std 产出 .out，并返回 .out 的全部 token。"""
    inp = "problem%d.in" % i
    outp = "problem%d.out" % i
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        proc = subprocess.run([STD], stdin=fi, stdout=fo, timeout=120)
    assert proc.returncode == 0, "problem%d: std 退出码 %d" % (i, proc.returncode)
    size = os.path.getsize(outp)
    assert size > 0, "problem%d: .out 为 0 字节！" % i
    with open(outp) as fo:
        return fo.read().split()


def verify(i, m, n, exp=None):
    toks = run_std(i)
    assert len(toks) == m, "problem%d: .out 行数 %d != m=%d" % (i, len(toks), m)
    vals = [int(t) for t in toks]
    if exp is not None:
        assert len(exp) == m
        bad = [k for k in range(m) if vals[k] != exp[k]]
        assert not bad, "problem%d: 第 %s 行与解析式不符（%s vs %s）" % (
            i, bad[:5], [vals[k] for k in bad[:5]], [exp[k] for k in bad[:5]])
    else:
        assert all(1 <= v <= n for v in vals), "problem%d: 答案越出 [1,n]" % i
    return vals


def w(f, k, s):
    f.write("%d %s\n" % (k, " ".join(map(str, s))))


# --------------------------------------------------------------------------
# 各结构生成器：返回该点的解析式期望答案（无解析式返回 None）
# --------------------------------------------------------------------------
def gen_sample(i):
    """点 3：题面【输入样例】原样。"""
    with open_in(i) as f:
        f.write("7\n0\n1 1\n1 1\n1 2\n2 2 3\n0\n2 2 6\n3\n")
        f.write("2 2 3\n2 3 5\n2 4 5\n")
    return [3, 3, 4]


def gen_blocks(i, n, L, m, seed):
    """点 4：每 L 个点一条链（B_i={i-1}，段首 B=∅）。
    解析式：被触及的段贡献 (段内最大元素 - 段首 + 1)。"""
    rng = random.Random(seed)
    starts = list(range(1, n + 1, L))
    exp = []
    with open_in(i) as f:
        f.write("%d\n" % n)
        for x in range(1, n + 1):
            f.write("0\n" if (x - 1) % L == 0 else "1 %d\n" % (x - 1))
        f.write("%d\n" % m)
        for _ in range(m):
            k = rng.randint(1, 6)
            s = rng.sample(range(1, n + 1), k)
            w(f, k, s)
            tot = 0
            for st in starts:
                hi = min(st + L - 1, n)
                blk = [v for v in s if st <= v <= hi]
                if blk:
                    tot += max(blk) - st + 1
            exp.append(tot)
    return exp


def gen_star(i, n, m, seed):
    """点 5：星形 B_i={1}（i>=2）。解析式：1∈T ? |T| : |T|+1。"""
    rng = random.Random(seed)
    exp = []
    with open_in(i) as f:
        f.write("%d\n0\n" % n)
        for _ in range(2, n + 1):
            f.write("1 1\n")
        f.write("%d\n" % m)
        for _ in range(m):
            k = rng.randint(1, min(10, n))
            s = rng.sample(range(1, n + 1), k)
            w(f, k, s)
            exp.append(k if 1 in s else k + 1)
    return exp


def gen_chain(i, n, m, qsz, seed):
    """点 7 / 10：单链 B_i={i-1}。S_i={1..i}，解析式：max(T)。"""
    rng = random.Random(seed)
    exp = []
    with open_in(i) as f:
        f.write("%d\n0\n" % n)
        for x in range(2, n + 1):
            f.write("1 %d\n" % (x - 1))
        f.write("%d\n" % m)
        for _ in range(m):
            k = qsz if isinstance(qsz, int) else rng.randint(1, qsz)
            s = rng.sample(range(1, n + 1), k)
            w(f, k, s)
            exp.append(max(s))
    return exp


def gen_multitree(i, n, m, seed):
    """点 6：多树随机（每 3 个点放一个树根），无解析式。"""
    rng = random.Random(seed)
    with open_in(i) as f:
        f.write("%d\n0\n" % n)
        for x in range(2, n + 1):
            if x % 3 == 0:
                f.write("0\n")
            else:
                f.write("1 %d\n" % rng.randint(1, x - 1))
        f.write("%d\n" % m)
        for _ in range(m):
            k = rng.randint(1, min(10, n))
            w(f, k, rng.sample(range(1, n + 1), k))
    return None


def gen_random(i, n, m, sumb, sumq, maxb, maxq, seed):
    """点 8 / 9：随机稀疏/顶格，无解析式。严格保证 Σ|B| <= sumb、Σsz <= sumq。"""
    rng = random.Random(seed)
    rb = sumb
    with open_in(i) as f:
        f.write("%d\n0\n" % n)
        for x in range(2, n + 1):
            k = min(rng.randint(0, maxb), rb, x - 1)
            if k > 0:
                rb -= k
                w(f, k, rng.sample(range(1, x), k))
            else:
                f.write("0\n")
        f.write("%d\n" % m)
        rem = sumq - m  # 每个询问预留 1 个元素，其余额度随机分配
        for _ in range(m):
            e = rng.randint(0, min(maxq - 1, rem)) if rem > 0 else 0
            rem -= e
            w(f, 1 + e, rng.sample(range(1, n + 1), 1 + e))
    return None


def gen_spine_fans(i, n, D, fanb, m, maxq, seed):
    """点 9：前 D 个点构成深链（B_x={x-1}），其余点 B 取链上连续的 fanb 个点
    {D-fanb+1..D}（这些点两两可比，集合 LCA = 其中最浅者 A=D-fanb+1，故 fan 点的
    深度仍约 D-fanb，且每个 B 都有 fanb 个元素 ⇒ 同时压「深链」与「多元素集合 LCA」）。

    解析式（本点的期望答案，生成时同步算出用于校验）：
      S_1..S_D 为链：S_j = {1..j}；S_x（fan 点 x>D）= {1..A} ∪ {x}。
      设 T 中脊点最大值为 P（无脊点为 0）、fan 点个数为 c（fan 点均 > D > A），则
        答案 = max(P, (A if c>0 else 0)) + c。
    严格保证 Σ|B| <= SUMB、Σsz <= SUMQ。"""
    rng = random.Random(seed)
    A = D - fanb + 1  # fan 点的父亲（= 链上最浅的那个）
    exp = []
    with open_in(i) as f:
        f.write("%d\n0\n" % n)
        for x in range(2, D + 1):
            f.write("1 %d\n" % (x - 1))
        for x in range(D + 1, n + 1):
            w(f, fanb, range(A, D + 1))
        f.write("%d\n" % m)
        rem = SUMQ - m
        for _ in range(m):
            e = rng.randint(0, min(maxq - 1, rem)) if rem > 0 else 0
            rem -= e
            s = rng.sample(range(1, n + 1), 1 + e)
            w(f, 1 + e, s)
            spine = [v for v in s if v <= D]
            c = len(s) - len(spine)
            hi = max(spine) if spine else 0
            if c:
                hi = max(hi, A)
            exp.append(hi + c)
    return exp


# --------------------------------------------------------------------------
# 逐点生成 + 校验
# --------------------------------------------------------------------------
def measure(i, m):
    """统计该点 .in 的 n、Σ|B|、Σsz（读文件统计，用于报告与上限断言）。"""
    n = sumb = sumq = 0
    with open("problem%d.in" % i) as f:
        n = int(f.readline())
        for _ in range(n):
            p = f.readline().split()
            sumb += int(p[0])
        m2 = int(f.readline())
        assert m2 == m, "problem%d: 文件里的 m=%d 与预期 %d 不符" % (i, m2, m)
        for _ in range(m):
            sumq += int(f.readline().split()[0])
    assert n <= MAXN, "problem%d: n 超上限" % i
    assert m <= MAXN, "problem%d: m 超上限" % i
    assert sumb <= SUMB, "problem%d: Σ|B|=%d 超上限" % (i, sumb)
    assert sumq <= SUMQ, "problem%d: Σsz=%d 超上限" % (i, sumq)
    return n, sumb, sumq


def do(i, m, note, exp, n):
    vals = verify(i, m, n, exp)
    nn, sumb, sumq = measure(i, m)
    stats.append((i, nn, m, sumb, sumq, note))
    print("problem%-2d ok  n=%-6d m=%-6d Σ|B|=%-7d Σsz=%-7d  -- %s"
          % (i, nn, m, sumb, sumq, note))
    return vals


def main():
    assert os.path.exists(STD), "找不到标程可执行文件 %s（请先在上一级 g++ 编译 std.cpp）" % STD

    # 点 1：n=1 最小规模
    with open_in(1) as f:
        f.write("1\n0\n1\n1 1\n")
    do(1, 1, "边界层：n=1 最小规模（B_1=∅），单询问 {1} -> 1", [1], 1)

    # 点 2：n=2 最小非平凡
    with open_in(2) as f:
        f.write("2\n0\n1 1\n3\n1 1\n1 2\n2 1 2\n")
    do(2, 3, "边界层：n=2 最小非平凡；询问 {1}/{2}/{1,2} -> 1/2/2", [1, 2, 2], 2)

    # 点 3：题面样例
    exp = gen_sample(3)
    do(3, 3, "题面【输入样例】原样 -> 3/3/4（题面声明值，可手算）", exp, 7)

    # 点 4：小规模链段
    exp = gen_blocks(4, 100, 5, 100, 1759 + 4)
    do(4, 100, "小规模：20 条长度 5 的链段（n=100，深度 4），解析式=段内 [段首,max]", exp, 100)

    # 点 5：小规模星形
    exp = gen_star(5, 200, 200, 1759 + 5)
    do(5, 200, "小规模：星形 B_i={1}（n=200），解析式=1∈T?|T|:|T|+1", exp, 200)

    # 点 6：中规模多树随机（无解析式）
    gen_multitree(6, 5000, 5000, 1759 + 6)
    do(6, 5000, "中规模：多树随机（n=5000，约 1667 棵树），覆盖跨树计数", None, 5000)

    # 点 7：中规模单链（深度 19999）
    exp = gen_chain(7, 20000, 20000, 10, 1759 + 7)
    do(7, 20000, "中规模：单链 n=20000（深度 19999），解析式=max(T)", exp, 20000)

    # 点 8：大规模随机（Σ|B|≈1e6，Σsz≈1e6）
    gen_random(8, 200000, 200000, 1000000, 1000000, 10, 10, 1759 + 8)
    do(8, 200000, "大规模随机：n=m=2e5，Σ|B|≈1e6，Σsz≈1e6", None, 200000)

    # 点 9：顶格深脊 + 宽 B 结构（Σ|B|=1999999，Σsz=2e6）
    exp = gen_spine_fans(9, 200000, 100000, 19, 200000, 20, 1759 + 9)
    do(9, 200000, "顶格：深链 1e5 + 1e5 个 fan 点（每个 |B|=19，深度仍 ~1e5），Σ|B|≈2e6 顶格、Σsz=2e6 顶格",
       exp, 200000)

    # 点 10：顶格单链（深度 199999）+ 每询问 10 个元素（Σsz=2e6 顶格）
    exp = gen_chain(10, 200000, 200000, 10, 1759 + 10)
    do(10, 200000, "顶格最坏结构：单链 n=2e5（深度 199999）+ m=2e5 个 size=10 询问", exp, 200000)

    print("\n全部 10 个点生成并校验通过：.in/.out 成对齐全、非空、行数正确。")
    print("分层汇总：")
    for i, n, m, sumb, sumq, note in stats:
        print("  点%-2d n=%-6d m=%-6d Σ|B|=%-7d Σsz=%-7d %s" % (i, n, m, sumb, sumq, note))


if __name__ == "__main__":
    main()
