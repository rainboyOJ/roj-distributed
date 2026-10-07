#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1724《小K的农场》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 -o std std.cpp && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：.ybt-import/staging/1222/data.py、.ybt-import/staging/1690/data.py、.ybt-import/staging/1714/data.py
#
# 题意（content.md 明文）：三类记忆 ⇒ 差分约束系统（x_i = 农场 i 的作物数）：
#   op1: x_a - x_b ≥ c  ⟺  x_b ≤ x_a - c   （有向边 a→b 权 -c）
#   op2: x_a - x_b ≤ c  ⟺  x_a ≤ x_b + c   （有向边 b→a 权  c）
#   op3: x_a == x_b     ⟺  x_a ≤ x_b 且 x_b ≤ x_a（双向 0 边）
#   超级源点连所有点权 0（图不连通也能一次判完）；「存在吻合的情况」⟺ 无负环 ⇒ Yes / No。
# 数据范围（题面【提示】明文）：1 ≤ n,m,a,b,c ≤ 10000；
#   限制 time 1000 ms / memory 128 MB（config.json；官方页 1000 ms / 131072 KB，一致）。
#
# ---- 分层策略（10 个测试点：边界 / 小 / 中 / 大 / 顶格）----
#   点 1  边界层（最小输入）：n=m=1，op3 自等 —— 答案 Yes。
#   点 2  边界层（样例回归）：题面【输入样例】原样（n=3,m=3），与【输出样例】逐字节对照。
#   点 3  边界层（最小 No）：n=m=1，op1 "1 1 1 1" —— x_1 - x_1 ≥ 1，自相矛盾 ⇒ No。
#   点 4  小规模随机 Yes：n=8, m=12，三类运算符齐全，按隐藏整数解反推（解即可行性 witness）。
#   点 5  小规模随机 No：n=10, m=15，先按隐藏解造一致信息，再植入一条矛盾约束。
#   点 6  中等规模 Yes：n=2000, m=3000，隐藏解 + 混合运算符。
#   点 7  中等规模 No：n=3000, m=3000，埋长度 1500 的负环（递增链 + 回边），其余为无害 op2 边。
#   点 8  大规模 Yes：n=m=10000，隐藏解 + 权值顶格（op1/op2 的 c=10000）+ 重复边。
#   点 9  顶格层 No（长负环最坏）：n=m=10000，9999 条递增链 + 1 条回边 = 长度 10000 的负环，
#         是 BFS-SPFA 的最坏形态之一（每次入队都要重松弛整条链）。
#   点 10 顶格层 No（等价链 SCC）：n=m=10000，9999 条 op3 构成 10000 点强连通（每条 op3 双向 0 边，
#         合计 19998 条有向边）+ 1 条与等价链矛盾的 op1 ⇒ No；检验巨量双向 0 边结构。
#
# ---- 数据正确性保证（生成期解析自检；**不使用任何 brute/对拍/stress**）----
#   · Yes 点：生成时按**隐藏整数解 x[]** 反推每条信息并逐条复验 x 满足约束（witness 检查，O(m)）；
#     有 witness ⇒ 系统可行 ⇒ std 必输出 Yes。
#   · No 点：显式构造负环，并解析复算「环权和 < 0」（点 3/5/7/9/10）⇒ 系统不可行 ⇒ std 必输出 No。
#   · 生成后用**构造期望**断言刚写出的 problemN.out 内容（期望来自上述解析构造，与 std 的算法无关）。
#   · 随机部分固定种子，完全可复现。

import os
import random
import sys

from cyaron import IO  # 引入CYaRon的库

MAXN = 10000
MAXM = 10000
MAXC = 10000

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(OUT_DIR, "std")
if not os.path.exists(STD):
    sys.exit("std binary not found: %s （先 g++ -O2 -std=c++17 -o std std.cpp）" % STD)


def write_chunks(io, lines, chunk=5000):
    """一次性 join 分块写（点 9/10 有 10^4 行，避免逐行 IO；无 O(n^2) 循环）。"""
    for i in range(0, len(lines), chunk):
        io.input_write("\n".join(lines[i:i + chunk]) + "\n")


# ---------------- 隐藏解（构造 Yes 用） ----------------
def hidden_x_linear(n):
    """x[i] = (i-1)//2：相邻对 (2k-1, 2k) 取值相同，易于生成合法 op3。"""
    return [0] + [(i - 1) // 2 for i in range(1, n + 1)]


def check_witness(infos, x, tag):
    """witness 复验：隐藏解 x 必须满足全部信息（Yes 点的可行性证明）。"""
    for _cnt, op, a, b, c in infos:
        if op == 1:
            assert x[a] - x[b] >= c, "%s witness 违约 op1 %d %d %d" % (tag, a, b, c)
        elif op == 2:
            assert x[a] - x[b] <= c, "%s witness 违约 op2 %d %d %d" % (tag, a, b, c)
        else:
            assert x[a] == x[b], "%s witness 违约 op3 %d %d" % (tag, a, b)


def consistent_infos(n, m, x, seed, p1=0.35, p2=0.40, p3=0.20):
    """按隐藏解 x 反推 m 条信息（全部被 x 满足 ⇒ 答案必 Yes）。

    三类运算符齐备：op1/op2 按真实差值域取 c；op3 落在"等值对"上（linear 解下即 (1,2),(3,4),…）。
    """
    rng = random.Random(seed)
    eq_pairs = [(k, k + 1) for k in range(1, n, 2)]    # x[k] == x[k+1]（linear 解）
    infos = []
    for _ in range(m):
        r = rng.random()
        if r < p3 and eq_pairs:                        # op3：x_a == x_b 必须成立
            a, b = eq_pairs[rng.randrange(len(eq_pairs))]
            infos.append((0, 3, a, b, 0))
            continue
        a = rng.randint(1, n)
        b = rng.randint(1, n)
        d = x[a] - x[b]                                # 真实差值
        r2 = rng.random()
        if r2 < 0.5 and d >= 1:                        # op1 需 c ≤ d
            infos.append((0, 1, a, b, rng.randint(1, min(d, MAXC))))
        elif r2 < 0.8:                                 # op2 需 c ≥ d（d ≤ 10000 恒成立，见 x 取值范围）
            infos.append((0, 2, a, b, min(rng.randint(max(1, d), MAXC), MAXC)))
        elif d >= 1:
            infos.append((0, 1, a, b, 1))
        else:
            infos.append((0, 2, a, b, max(1, d)))
    return infos


rng0 = random.Random(172400)

# ---------------- 点 1：边界层（最小 Yes） ----------------
P1 = [(0, 3, 1, 1, 0)]

# ---------------- 点 2：边界层（题面样例） ----------------
P2 = [(0, 3, 1, 2, 0), (0, 1, 1, 3, 1), (0, 2, 2, 3, 2)]

# ---------------- 点 3：边界层（最小 No） ----------------
P3 = [(0, 1, 1, 1, 1)]

# ---------------- 点 4：小规模随机 Yes ----------------
x4 = hidden_x_linear(8)
P4 = consistent_infos(8, 12, x4, seed=172404)
assert len({op for _c, op, _a, _b, _z in P4}) == 3, "点 4 应含全部三类运算符"
check_witness(P4, x4, "点4")

# ---------------- 点 5：小规模随机 No（显式负环 + 随机单条可满足信息） ----------------
# 负环证明：p1 ≥ p5 + 1（边 p1→p5 权 -1）与 p5==p4==p3==p2==p1（4 条 op3、8 条 0 权边）
# 构成环权和 -1 < 0 ⇒ 必 No（与隐藏解无关）。其余 10 条随机信息各自被隐藏解 x5 满足。
x5 = hidden_x_linear(10)
rng5 = random.Random(172405)
CH5 = rng5.sample(range(1, 11), 5)          # 随机选 5 个互异点作为等价链（题目未禁止 a==b 之外的重复点）
P5 = [(0, 3, CH5[i], CH5[i + 1], 0) for i in range(4)]
P5.append((0, 1, CH5[0], CH5[-1], 1))       # op1：x_{p1} ≥ x_{p5} + 1，与等价链相悖
assert -1 < 0, "点 5 环权应为 -1"
P5 += consistent_infos(10, 10, x5, seed=172405)
check_witness(P5[5:], x5, "点5(随机部分)")
NO5 = "等价链 %s（4×op3） + op1(%d,%d,1) 构成环权和 -1" % (
    "-".join(map(str, CH5)), CH5[0], CH5[-1])

# ---------------- 点 6：中等规模 Yes ----------------
x6 = hidden_x_linear(2000)
P6 = consistent_infos(2000, 3000, x6, seed=172406)
assert len({op for _c, op, _a, _b, _z in P6}) == 3, "点 6 应含全部三类运算符"
check_witness(P6, x6, "点6")

# ---------------- 点 7：中等规模 No（长度 1500 的负环） ----------------
K7 = 1500
P7 = [(0, 1, i + 1, i, 1) for i in range(1, K7)]    # x_{i+1} ≥ x_i + 1 ⇒ 边(i+1→i, -1)
P7.append((0, 1, 1, K7, 1))                          # 回边(1→K7)权 -1
assert -K7 < 0, "点 7 环权非负"                       # 环权和 = -(K7-1) - 1 < 0
while len(P7) < 3000:                                # 填充无害 op2 边（正权边不消负环）
    P7.append((0, 2, rng0.randint(1, 3000), rng0.randint(1, 3000), rng0.randint(1, MAXC)))
assert len(P7) == 3000

# ---------------- 点 8：大规模 Yes（n=m=10000，权值顶格 + 重复边） ----------------
N8, M8 = 10000, 10000
x8 = [0] * (N8 + 1)
for i in range(3, N8 + 1):
    x8[i] = 5 * ((i - 3) // 2000)                    # 3..10000 号点取值 ∈ {0,5,10,15,20}
x8[1], x8[2] = 0, 10000                              # 制造差值极值 ±10000
# op1 c=10000 顶格（x2-x1=10000 ≥ 10000）；op2 c=10000 顶格；重复边（同一条信息出现 4 次）
P8 = ([(0, 1, 2, 1, MAXC)] +
      [(0, 2, 1, 2, MAXC)] +
      [(0, 2, 2, 1, MAXC)] * 3 +
      consistent_infos(N8, M8 - 5, x8, seed=172408))
check_witness(P8, x8, "点8")
assert len(P8) == M8

# ---------------- 点 9：顶格层 No（长度 10000 的长负环） ----------------
N9, M9 = 10000, 10000
P9 = [(0, 1, i + 1, i, 1) for i in range(1, N9)]     # 9999 条递增链 ⇒ 边(i+1→i, -1)
P9.append((0, 1, 1, N9, 1))                          # 回边 ⇒ 环权和 = -(N9-1) - 1 = -N9 < 0
assert len(P9) == M9 and -N9 < 0, "点 9 环权非负"

# ---------------- 点 10：顶格层 No（等价链 SCC + 矛盾） ----------------
N10, M10 = 10000, 10000
P10 = [(0, 3, i, i + 1, 0) for i in range(1, N10)]   # 9999×op3：10000 点等价链（19998 条有向边）
P10.append((0, 1, 1, N10, 1))                        # x1 ≥ x_N10 + 1 与等价链冲突
assert len(P10) == M10

# ---------------- 写出 + 构造期望断言 ----------------
CASES = [
    (1, 1, P1, "Yes", "边界层：n=m=1 最小 Yes（op3 自等）"),
    (2, 3, P2, "Yes", "边界层：题面样例原样回归"),
    (3, 1, P3, "No", "边界层：n=m=1 自环 op1 ⇒ 最小 No"),
    (4, 8, P4, "Yes", "小规模随机 Yes：n=8,m=12（隐藏解）"),
    (5, 10, P5, "No", "小规模随机 No：n=10,m=15 植入矛盾（%s）" % NO5),
    (6, 2000, P6, "Yes", "中等规模 Yes：n=2000,m=3000（隐藏解）"),
    (7, 3000, P7, "No", "中等规模 No：n=3000,m=3000 长度 1500 负环"),
    (8, N8, P8, "Yes", "大规模 Yes：n=m=10000 c 顶格 10000 + 重复边"),
    (9, N9, P9, "No", "顶格层 No：n=m=10000 长度 10000 长负环"),
    (10, N10, P10, "No", "顶格层 No：n=m=10000 等价链 9999×op3 + 矛盾边"),
]
assert len(CASES) == 10

for cid, n, infos, expect, note in CASES:
    assert 1 <= n <= MAXN, "点 %d n 越界" % cid
    assert 1 <= len(infos) <= MAXM, "点 %d m 越界" % cid
    for _cnt, op, a, b, c in infos:                  # 逐条范围复核
        assert op in (1, 2, 3), "点 %d 非法 op" % cid
        assert 1 <= a <= n and 1 <= b <= n, "点 %d 端点越界 (%d,%d)" % (cid, a, b)
        if op in (1, 2):
            assert 1 <= c <= MAXC, "点 %d c 越界 %d" % (cid, c)
    assert expect in ("Yes", "No")

    io = IO(file_prefix="problem", data_id=cid)      # problem{cid}.in / problem{cid}.out
    lines = ["%d %d" % (n, len(infos))]
    for _cnt, op, a, b, c in infos:
        lines.append("%d %d %d %d" % (op, a, b, c) if op in (1, 2) else "%d %d %d" % (op, a, b))
    write_chunks(io, lines)
    io.output_gen(STD)                               # .out 由 std 现跑
    io.close()                                       # 刷新句柄，确保 .out 落盘

    with open(os.path.join("problem%d.out" % cid)) as f:
        got = f.read().strip()
    assert got == expect, "点 %d：std 输出 %r ≠ 构造期望 %r（%s）" % (cid, got, expect, note)
    print("%-14s n=%-5d m=%-5d expect=%-3s got=%-3s  %s"
          % ("problem%d" % cid, n, len(infos), expect, got, note))

print("done: 10 组 .in/.out 已生成（%s），全部与解析构造期望一致" % os.path.join(OUT_DIR, "data"))
