#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1747《奶牛排队》数据生成器（cyaron，仓库惯例）
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围：第一行 N（2 <= N <= 100000），随后 N 行每行一个身高（1 <= 身高 <= 2^32-1）。
# 输出：一行，符合条件的最多奶牛数（0 或 >= 2，绝不会是 1）。
#
# 分层设计（10 组）：
#   点 1-2   边界层：最小规模 N=2，分别取"有解(答案2)"与"无解(答案0)"
#   点 3-4   边界层：题面样例；N=1000 全相等（同时取身高上限 2^32-1，答案 0）
#   点 5     小规模随机：N=10，可手算
#   点 6-7   中等规模：N=1e4 递增(答案 N) / 递减(答案 0)
#   点 8     大规模随机：N=1e5，值域顶到 2^32-1
#   点 9-10  顶格层：N=1e5 递增(答案 N) / 值域 [1,3] 大量重复（卡相等判断）
#
# 注：本目录的 data.py 需先编译好标程：g++ -O2 -std=c++17 -o std std.cpp
#     （生成结束会校验 .out 非空且恰为一行合法答案，防止 cyaron 在 std 缺失时
#      静默产出 0 字节 .out。）

from cyaron import *

import os
import random
import sys

MAXV = 2 ** 32 - 1  # 身高上限
rnd = random.Random(17470000 + 1747)  # 固定种子，可复现

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
if not (os.path.isfile(STD) and os.access(STD, os.X_OK)):
    sys.stderr.write(
        "FATAL: 标程 %s 不存在或不可执行，先执行：g++ -O2 -std=c++17 -o std std.cpp\n" % STD
    )
    sys.exit(1)


def text(n, vals):
    """N + 每行一个身高。"""
    assert len(vals) == n, (len(vals), n)
    assert all(1 <= v <= MAXV for v in vals), "身高越界"
    return str(n) + "\n" + "".join("%d\n" % v for v in vals)


# 期望答案（已知可严格手推的点，None 表示由 std 计算）
EXPECT = {
    1: 2,        # [1,2]
    2: 0,        # [2,1]
    3: 4,        # 题面样例
    4: 0,        # 全相等
    6: 10000,    # 严格递增
    7: 0,        # 严格递减
    9: 100000,   # 严格递增
}

results = []
for i in range(1, 11):
    # ---- 点 1｜边界层：最小规模 N=2，a=[1,2] -> 1 最小、2 最大，答案 2 ----
    if i == 1:
        n, vals = 2, [1, 2]

    # ---- 点 2｜边界层：最小规模 N=2，a=[2,1] -> B 不高于 A，无解，答案 0 ----
    elif i == 2:
        n, vals = 2, [2, 1]

    # ---- 点 3｜边界层：题面样例 N=5，答案 4 ----
    elif i == 3:
        n, vals = 5, [1, 2, 3, 4, 1]

    # ---- 点 4｜边界层：N=1000 全相等且取身高上限 2^32-1；中间必与 A/B 相同，答案 0 ----
    elif i == 4:
        n, vals = 1000, [MAXV] * 1000

    # ---- 点 5｜小规模随机：N=10，值域 [1,4]（含重复），可手算核对 ----
    elif i == 5:
        n = 10
        vals = [rnd.randint(1, 4) for _ in range(n)]

    # ---- 点 6｜中等规模：N=1e4 严格递增 1..N，整段合法，答案 N ----
    elif i == 6:
        n = 10000
        vals = list(range(1, n + 1))

    # ---- 点 7｜中等规模：N=1e4 严格递减，任何区间 a[l] 都不是最小，答案 0 ----
    elif i == 7:
        n = 10000
        vals = list(range(n, 0, -1))

    # ---- 点 8｜大规模随机：N=1e5，值域顶到 2^32-1（末位置强制取上限，覆盖极值）----
    elif i == 8:
        n = 100000
        vals = [rnd.randint(1, MAXV) for _ in range(n)]
        vals[-1] = MAXV

    # ---- 点 9｜顶格层：N=1e5 严格递增，答案 N（最大规模 + 最长合法区间）----
    elif i == 9:
        n = 100000
        vals = list(range(1, n + 1))

    # ---- 点 10｜顶格层：N=1e5，值域仅 [1,3] 大量重复，压相等/并列的处理 ----
    else:
        n = 100000
        vals = [rnd.randint(1, 3) for _ in range(n)]

    io = IO(file_prefix="problem", data_id=i)
    io.input_write(text(n, vals))
    io.output_gen("../std")
    # cyaron 的 output_gen 把结果写进带缓冲的 Python 文件对象且**不主动 flush**，
    # 直接读盘会看到 0 字节（这正是题面警告的"静默 0 字节 .out"隐患），必须手动 flush。
    io.input_file.flush()
    io.output_file.flush()

    # ---- 校验 std 输出：必须存在、非空、恰一行、合法非负整数 ----
    out_path = "problem%d.out" % i
    if not os.path.exists(out_path):
        sys.exit("FATAL: %s 未生成（std 缺失或崩溃）" % out_path)
    size = os.path.getsize(out_path)
    if size == 0:
        sys.exit("FATAL: %s 为 0 字节（cyaron 在 std 缺失时会静默如此）" % out_path)
    with open(out_path, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip() != ""]
    if len(lines) != 1:
        sys.exit("FATAL: %s 期望 1 行答案，实际 %d 行" % (out_path, len(lines)))
    got = int(lines[0])
    if not (0 <= got <= n):
        sys.exit("FATAL: %s 答案 %d 超出 [0, n=%d]" % (out_path, got, n))
    if got == 1:
        sys.exit("FATAL: %s 答案为 1，违反题面（答案只可能是 0 或 >=2）" % out_path)
    if EXPECT.get(i) is not None and got != EXPECT[i]:
        sys.exit("FATAL: %s 答案 %d 与手推期望 %d 不符" % (out_path, got, EXPECT[i]))

    results.append((i, n, got))
    print("problem%d.in/.out  n=%-6d ans=%-6d %s" % (i, n, got, "OK" if EXPECT.get(i) is not None else "-"))

print("\n全部 10 组生成完毕，.out 均非空且合法。")
