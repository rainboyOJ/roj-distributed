#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1769《景中人》数据生成器（目标 ROJ 题号 1769）
#
# 题面（见本目录 content.md，与官方 OJ 页一致）：
#   有 n 个人在桥上，每人坐标 (x,y)。用最少数量的矩形覆盖所有人；
#   每个矩形面积不能超过 S，且矩形的一条边必须贴着下栏杆（直线 y=0）。
#   输入：第一行 T；每组数据第一行 n S，随后 n 行 x y。
#   输出：每组一行，最少矩形数。
#   数据规模：10% n<=8, x<=10, S<=20；30% n<=18, x<=700, S<=1024；
#             90% n<=90；100% T<=10, n<=100, x<=3000000, 1<=y<=S<=200000。
#
# ---- 关于 cyaron 的处置（任务书隐患项） ----
# 本生成器**不用** cyaron 的 `io.output_gen()` 产 .out（其写缓冲不 flush 会产出 0 字节 .out）。
# 做法：用 cyaron 的 IO 只写 .in（file_prefix 指向绝对路径，故与 cwd 无关），
# 写完显式 `flush_buffer()` + `close()` 强制落盘；随后用 **subprocess 显式跑 std**
# 把 stdout 重定向进 .out，最后断言 .out 非空且行数恰为 T、每行是 [1, n] 内的整数。
# （任务书明确允许「data.py 用 subprocess 显式跑 std 产 .out」这一路径。）
#
# 生成器内没有 O(n^2) 的 Python 循环：n<=100、T<=10，全部为 O(n) 线性写点。
#
# ---- 分层设计（10 个测试点，从边界铺到顶格 + 结构对抗） ----
#   点 1  边界层：T=1, n=1 最小规模（单点，答案 1）
#   点 2  边界层：3 组手算可核的小组 —— 同 x 完全重合点（列压缩）、
#         x 顶格跨度 3e6 与 S=1 的最小面积（答案 2）、嵌套结构 (0,1),(5,100),(10,1)（答案 2）
#   点 3  样例层：题面【输入样例】逐字复刻（T=1, n=6, S=4, 答案 3）
#   点 4  小规模（10% 档）：T=10, n∈[1,8], x∈[0,10], S∈[1,20]
#   点 5  中规模（30% 档）：T=10, n∈[1,18], x∈[0,700], S∈[1,1024]
#   点 6  大规模（90% 档）：T=10, n∈[1,90], x∈[0,3e6], S∈[1,2e5]
#   点 7  顶格规模：T=10, n=100（顶格人数），x 互异满区间 [0,3e6]，S 顶格 2e5
#   点 8  顶格结构对抗：T=10, n=100，S=2e5；中间少量「高峰」y=S + 两侧大量矮点，
#         复刻「嵌套矩形（大而矮 + 小而高）」这一本题唯一非平凡结构
#   点 9  顶格结构对抗：T=10, n=100，y 全 = 1，x 均匀铺满 [0,3e6] → 答案 ≈ ceil(3e6/2e5)
#   点 10 顶格列压缩对抗：T=10, n=100，把 100 个点压到 2..10 个不同 x 上（大量重合），
#         y 满量程随机 → 压测「同 x 只保留最大 y」的列压缩与 nn 分层
#
# 随机性：每点使用独立 Random(1769 + 点号)，与调用顺序无关、逐字节可复现。

from cyaron import IO  # 只用其输入写出能力（输出一律走 subprocess）

import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
OUTDIR = os.path.join(HERE, "data")

XMAX = 3000000     # 题面上限
SMAX = 200000      # 题面上限
NMAX = 100         # 题面上限
TMAX = 10          # 题面上限

SAMPLE = (6, 4, [(2, 1), (4, 1), (5, 1), (5, 4), (7, 1), (6, 4)])

SUMMARY = []


def emit(idx, cases, note):
    """cases: [(n, S, [(x,y), ...]), ...] -> data/problem{idx}.in/.out，并做完整性断言。"""
    os.makedirs(OUTDIR, exist_ok=True)
    io = IO(file_prefix=os.path.join(OUTDIR, "problem"), data_id=idx, disable_output=True)
    io.input_writeln(len(cases))
    for (n, S, pts) in cases:
        assert n == len(pts), "点%d：n 与点数不符" % idx
        io.input_writeln(n, S)
        for (x, y) in pts:
            io.input_writeln(x, y)
    io.flush_buffer()          # 显式 flush，避免 0 字节 .in
    io.close()

    inp = os.path.join(OUTDIR, "problem%d.in" % idx)
    outp = os.path.join(OUTDIR, "problem%d.out" % idx)

    # ---- 显式用 subprocess 跑 std 产 .out（不用 cyaron 的 output_gen） ----
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        subprocess.run([STD], stdin=fi, stdout=fo, check=True)

    # ---- 断言：.in / .out 非空、行数符合预期、值域合法 ----
    raw_in = open(inp, "r").read()
    assert raw_in.strip(), "点%d：.in 为空（疑似写缓冲未 flush）" % idx
    lines = raw_in.split("\n")
    assert lines[-1] == "", "点%d：.in 末尾缺换行" % idx
    lines = lines[:-1]

    raw_out = open(outp, "r").read()
    assert raw_out.strip(), "点%d：.out 为空" % idx
    outs = raw_out.strip().split("\n")
    assert len(outs) == len(cases), \
        "点%d：.out 行数 %d != 组数 %d" % (idx, len(outs), len(cases))

    exp_lines = 1 + sum(1 + n for (n, _S, _p) in cases)
    assert len(lines) == exp_lines, \
        "点%d：.in 行数 %d != 预期 %d" % (idx, len(lines), exp_lines)
    assert 1 <= len(cases) <= TMAX, "点%d：T 越界" % idx

    # 逐组校验输入值域 + 输出合理性
    p = 1
    for ci, (n, S, pts) in enumerate(cases):
        assert lines[p].split() == [str(n), str(S)], "点%d 组%d：n S 行不符" % (idx, ci + 1)
        p += 1
        assert 1 <= n <= NMAX and 1 <= S <= SMAX, "点%d 组%d：n/S 越界" % (idx, ci + 1)
        for (x, y) in pts:
            assert lines[p].split() == [str(x), str(y)], "点%d 组%d：点行不符" % (idx, ci + 1)
            p += 1
            assert 0 <= x <= XMAX, "点%d 组%d：x 越界" % (idx, ci + 1)
            assert 1 <= y <= S, "点%d 组%d：y 越界（题面 1<=y<=S）" % (idx, ci + 1)
        ans = int(outs[ci])
        assert 1 <= ans <= n, "点%d 组%d：答案 %d 不在 [1,n]" % (idx, ci + 1, ans)
    assert p == len(lines), "点%d：解析行数与实际不符" % idx

    SUMMARY.append((idx, len(cases), note, [int(v) for v in outs]))
    print("problem%-2d: T=%-2d 答案=%-28s -- %s"
          % (idx, len(cases), str([int(v) for v in outs]), note))


def rnd_pts(rng, n, xlo, xhi, S, ylo=1, distinct_x=False):
    """n 个随机点；distinct_x=True 时 x 互异（满区间取样）。"""
    if distinct_x:
        xs = rng.sample(range(xlo, xhi + 1), n)
    else:
        xs = [rng.randint(xlo, xhi) for _ in range(n)]
    return [(x, rng.randint(ylo, S)) for x in xs]


# ---- 点 1：边界层，最小规模 ----
emit(1, [(1, 1, [(0, 1)])],
     "边界层：T=1, n=1 最小规模（x=0, y=S=1），答案 1")

# ---- 点 2：边界层，3 组手算可核的小组 ----
emit(2, [
    (2, SMAX, [(0, SMAX), (0, SMAX)]),          # 同 x 完全重合 → 列压缩成 1 列 → 1
    (2, 1, [(0, 1), (XMAX, 1)]),                # 宽度顶格 3e6，S=1 → 1*3e6 > 1 → 2
    (3, 100, [(0, 1), (5, 100), (10, 1)]),      # 嵌套：整跨 [0,10]x[0,10] 面积 100 + 高峰 1 条 → 2
], "边界层：重合点/顶格宽度/嵌套结构（手算 1,2,2）")

# ---- 点 3：题面样例逐字复刻 ----
emit(3, [SAMPLE], "样例层：题面【输入样例】逐字复刻，答案 3")

# ---- 点 4：小规模（10% 档） ----
rng = random.Random(1769 + 4)
cases4 = []
for _ in range(10):
    n = rng.randint(1, 8)
    S = rng.randint(1, 20)
    cases4.append((n, S, rnd_pts(rng, n, 0, 10, S)))
emit(4, cases4, "小规模（10% 档）：T=10, n∈[1,8], x∈[0,10], S∈[1,20]")

# ---- 点 5：中规模（30% 档） ----
rng = random.Random(1769 + 5)
cases5 = []
for _ in range(10):
    n = rng.randint(1, 18)
    S = rng.randint(1, 1024)
    cases5.append((n, S, rnd_pts(rng, n, 0, 700, S)))
emit(5, cases5, "中规模（30% 档）：T=10, n∈[1,18], x∈[0,700], S∈[1,1024]")

# ---- 点 6：大规模（90% 档） ----
rng = random.Random(1769 + 6)
cases6 = []
for _ in range(10):
    n = rng.randint(1, 90)
    S = rng.randint(1, SMAX)
    cases6.append((n, S, rnd_pts(rng, n, 0, XMAX, S)))
emit(6, cases6, "大规模（90% 档）：T=10, n∈[1,90], x∈[0,3e6], S∈[1,2e5]")

# ---- 点 7：顶格规模（n=100, x 互异, S 顶格；y 量程交替满量程/小量程） ----
rng = random.Random(1769 + 7)
cases7 = []
for t in range(10):
    xs = rng.sample(range(0, XMAX + 1), NMAX)
    yhi = SMAX if t % 2 == 0 else 5   # 交替：满量程（几乎每点一矩形） / 小量程（可合并）
    cases7.append((NMAX, SMAX, [(x, rng.randint(1, yhi)) for x in xs]))
emit(7, cases7,
     "顶格规模：T=10, n=100 顶格, x 互异铺满 [0,3e6], S=2e5 顶格；y 满量程与小量程交替")

# ---- 点 8：顶格结构对抗（中间高峰 + 两侧矮点，嵌套形态） ----
rng = random.Random(1769 + 8)
cases8 = []
for t in range(10):
    xs = sorted(rng.sample(range(0, XMAX + 1), NMAX))
    tall = set(rng.sample(range(NMAX), 10))          # 10 个高峰（y=S）
    pts = [(x, SMAX if i in tall else rng.randint(1, 100)) for i, x in enumerate(xs)]
    cases8.append((NMAX, SMAX, pts))
emit(8, cases8,
     "顶格结构对抗：T=10, n=100, S=2e5；10 个高峰 y=S + 90 个矮点 y∈[1,100]（嵌套矩形形态）")

# ---- 点 9：顶格结构对抗（全矮点 + x 均匀铺满） ----
rng = random.Random(1769 + 9)
cases9 = []
for t in range(10):
    xs = sorted(rng.sample(range(0, XMAX + 1), NMAX))
    cases9.append((NMAX, SMAX, [(x, 1) for x in xs]))
emit(9, cases9,
     "顶格结构对抗：T=10, n=100, y 全=1, x 均匀铺满 [0,3e6] → 答案≈ceil(3e6/2e5)")

# ---- 点 10：顶格列压缩对抗（100 点压到 2..10 个 x 上） ----
rng = random.Random(1769 + 10)
cases10 = []
for t in range(10):
    k = 2 + (t % 9)                                    # 不同 x 的个数 ∈ [2,10]
    xs_pool = sorted(rng.sample(range(0, XMAX + 1), k))
    pts = [(xs_pool[rng.randrange(k)], rng.randint(1, SMAX)) for _ in range(NMAX)]
    cases10.append((NMAX, SMAX, pts))
emit(10, cases10,
     "顶格列压缩对抗：T=10, n=100，100 点压到 2..10 个不同 x（大量重合），y 满量程随机")

# ---- 全局自检 ----
assert len(SUMMARY) == 10, "应有 10 个测试点"
for (idx, tt, note, outs) in SUMMARY:
    assert len(outs) == tt
print("自检通过：10 个测试点 .in/.out 均非空、行数符合预期、值域合法、答案均在 [1,n]。")
