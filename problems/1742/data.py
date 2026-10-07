#!/usr/bin/env python

# 一本通 1742 导线问题 数据生成器
#
# 题意：求序列 a[1..n] 的最长严格上升子序列（LIS）长度 L；
#       若 type=1，再输出长度恰为 L 的严格上升子序列个数对 123456789 取模。
#       计数口径 = 按下标位置计数（同一取值出现在不同位置算不同方案），与两份公开题解一致。
# 范围：1<=n<=1e5，1<=电阻值<=1e5；time 1000ms / memory 256MB。
#
# 用法（仓库惯例）：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && python3 ../data.py
#
# 分层：
#   点 1-2 边界层（n=1 / n=2 极值）
#   点 3-4 小规模层（n=10，可手算）
#   点 5-6 中等规模层（n=1000，含 type=0 与「LIS<=100」子任务）
#   点 7-8 大规模层（n=5e4 / 1e5 随机）
#   点 9-10 顶格层（n=1e5 构造最坏结构：LIS 恰 100 的大方案数、重复值密集）
#
# 校验（防止 std 缺失时 cyaron 静默产出 0 字节 .out）：
#   每个点生成后立刻断言
#     .in/.out 均非空；.out 行数 == (type=1 ? 2 : 1)；长度/方案数落在合法区间；
#     对可解析构型逐字比对**解析解**（块构造 run_len^k、交替序列 H(H+1)/2 等）。

import os
import random
import sys

from cyaron import IO

MOD = 123456789
MAX_N = 100000
MAX_V = 100000

random.seed(1742)

if not os.path.exists("../std"):
    sys.exit("ERROR: ../std 不存在，请先 `g++ -O2 -std=c++17 std.cpp -o std`")


def emit(data_id, n, typ, a, expect=None, note=""):
    """写 problem<id>.in，用 std 生成 .out，并做断言校验；返回 (length, cnt)。"""
    assert 1 <= n <= MAX_N, (data_id, n)
    assert len(a) == n, (data_id, len(a))
    assert all(1 <= v <= MAX_V for v in a), (data_id, "value out of range")

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("%d %d\n" % (n, typ))
    io.input_write(" ".join(map(str, a)) + "\n")
    io.output_gen("../std")
    io.close()

    ipath = "problem%d.in" % data_id
    opath = "problem%d.out" % data_id
    assert os.path.getsize(ipath) > 0, "%s 空文件" % ipath
    assert os.path.getsize(opath) > 0, "%s 空文件（std 可能缺失/崩溃）" % opath

    txt = open(opath).read()
    assert txt.endswith("\n"), "%s 末尾缺换行" % opath
    lines = txt.split("\n")[:-1]
    want_lines = 2 if typ == 1 else 1
    assert len(lines) == want_lines, "%s 行数 %d != %d" % (opath, len(lines), want_lines)

    length = int(lines[0])
    assert 1 <= length <= n, "%s LIS 长度 %d 越界 (n=%d)" % (opath, length, n)
    cnt = None
    if typ == 1:
        cnt = int(lines[1])
        assert 1 <= cnt < MOD, "%s 方案数 %d 不在 [1, MOD)" % (opath, cnt)

    if expect is not None:
        assert (length, cnt) == expect, \
            "%s 解析解 %s，实际 (%d, %s)" % (opath, expect, length, cnt)

    print("problem%-2d n=%-6d type=%d LIS=%-6d cnt=%-11s %s"
          % (data_id, n, typ, length, "-" if cnt is None else cnt, note))
    return length, cnt


def runs_increasing(k, run_len):
    """k 个块、每块 run_len 个元素：块内严格递减，块间整体递增。

    块 r 取值 [r*run_len+1, (r+1)*run_len] 倒序排列 => 块内至多取 1 个；
    块 r 的所有取值都小于块 r+1 => 从每块各取 1 个即得严格上升的 k 元组。
    故 LIS 长度恰为 k，方案数恰为 run_len^k（按位置计数）。
    要求 k*run_len <= 1e5，取值落在 [1, 1e5]。
    """
    a = []
    for r in range(k):
        lo = r * run_len + 1
        a.extend(range(lo + run_len - 1, lo - 1, -1))
    return a


# ── 点 1 边界层：最小规模 n=1，type=0（只输出一行） ─────────────────────
emit(1, 1, 0, [1], expect=(1, None), note="边界：n=1 / 电阻最小值 / type=0 单行输出")

# ── 点 2 边界层：n=2，电阻最小与上限，严格上升 ─────────────────────────
emit(2, 2, 1, [1, MAX_V], expect=(2, 1), note="边界：n=2 / 电阻 1 与上限 1e5")

# ── 点 3 小规模层（20% 子任务 n<=10）：取值 {1..4} 随机，重复密集 ───────
random.seed(174203)
emit(3, 10, 1, [random.randint(1, 4) for _ in range(10)],
     note="小规模：n=10 随机，取值 1..4 重复值多")

# ── 点 4 小规模层：n=10 严格递减 => LIS=1，方案数恰为 n=10 ─────────────
emit(4, 10, 1, list(range(10, 0, -1)), expect=(1, 10),
     note="小规模手算：严格递减，LIS=1，方案数=n=10")

# ── 点 5 中等规模层（40% 子任务 n<=1000）+ type=0 子任务 ───────────────
random.seed(174205)
L5, _ = emit(5, 1000, 0, [random.randint(1, MAX_V) for _ in range(1000)],
             note="中等：n=1000 随机 1..1e5，type=0")
assert 40 <= L5 <= 150, L5  # 随机 LIS 的期望量级约 2*sqrt(n) ~ 63

# ── 点 6 中等规模层：n=1000，取值 1..60 => LIS<=60（「不超过100」子任务） ─
random.seed(174206)
L6, _ = emit(6, 1000, 1, [random.randint(1, 60) for _ in range(1000)],
             note="中等：n=1000 取值 1..60，LIS<=60，重复值密集")
assert L6 <= 60, L6  # 严格上升子序列长度不超过不同取值个数

# ── 点 7 大规模层：n=50000 随机，接近上限的随机结构 ────────────────────
random.seed(174207)
L7, _ = emit(7, 50000, 1, [random.randint(1, MAX_V) for _ in range(50000)],
             note="大规模：n=50000 随机 1..1e5")
assert 300 <= L7 <= 700, L7

# ── 点 8 大规模层：n=1e5 随机，顶格随机数据 ────────────────────────────
random.seed(174208)
L8, _ = emit(8, MAX_N, 1, [random.randint(1, MAX_V) for _ in range(MAX_N)],
             note="大规模：n=1e5 随机 1..1e5（顶格随机）")
assert 400 <= L8 <= 1000, L8

# ── 点 9 顶格层：100 块 × 1000（块内递减、块间递增）=> LIS 恰 100 ───────
#     方案数 = 1000^100 mod 123456789，压大方案数的取模路径；
#     同时精确覆盖「最多能通过不超过 100 条导线」子任务。
emit(9, MAX_N, 1, runs_increasing(100, 1000),
     expect=(100, pow(1000, 100, MOD)),
     note="顶格：n=1e5 块构造，LIS 恰 100，方案数 1000^100 mod M")

# ── 点 10 顶格层：交替 1,2 => LIS=2，方案数 = H+(H-1)+...+1 = H(H+1)/2 ──
#     1 在 0-based 偶数下标（H 个），2 在奇数下标（H 个）；第 m 个 1 之后
#     有 H-m 个 2，故长度 2 的方案数为 H(H+1)/2，是 MOD 的十余倍量级，
#     专门压 64 位累加 + 取模，以及重复值合并（同 rank 同长度累加）路径。
H = MAX_N // 2
alt = [1 + (i & 1) for i in range(MAX_N)]
assert alt[0] == 1 and alt[1] == 2
emit(10, MAX_N, 1, alt, expect=(2, (H * (H + 1) // 2) % MOD),
     note="顶格：n=1e5 交替 1/2，LIS=2，重复值密集，方案数 H(H+1)/2 mod M")

print("OK: 10 组数据全部生成并通过断言校验")
