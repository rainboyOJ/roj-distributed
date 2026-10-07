#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1807《区间计数》分层数据生成器
#
# 题意：D(n) 为 n 的数根（迭代各位数字和至 <10）。若 m 可写成 x*D(x)（题面写作 x*d(x)，
#       样例证实即 D(x)），称 m 是"小D喜欢的数"。多组询问 [L,R]，输出区间内喜欢的数的个数。
#       输入：第一行 T，随后 T 行每行 L R（保证 L<=R）。
# 数据范围：30%  L,R <= 10^6；100%  T <= 20，L,R <= 10^18。时限 1000ms / 256MB。
# 数组/上限安全系数：L,R 严格不超过 10^18（MAXV = 10^18），不越题面上限。
#
# 分层（10 组，从边界铺到顶格；本题为多组数据题，故每组是"若干询问"而非单个规模）：
#   1  样例层：题面【输入样例】原样 3 组询问（回归验证）
#   2  边界层：最小询问 [1,1]/[1,2]/[1,3]/[1,4]，答案 1/1/1/2（手算可验证）
#   3  小规模手算层：[1,10]→4、[1,100]→29、[100,200]→27（手算枚举验证，见 gen-report.md）
#   4  周期边界层：T=20 上限下的 81/82 边界（std 的"小值枚举 + 周期计数"分界处）
#   5  30% 档：T=20，L,R <= 10^6，随机
#   6  中间档：T=20，L,R <= 10^9，随机
#   7  100% 档：T=20，L,R <= 10^18，随机
#   8  顶格单点层：T=20，L=R=10^18 附近（极窄区间，答案 0/1）
#   9  顶格全区间层：T=20，[1,10^18] 及接近全区间（答案最大，考验计数上界）
#   10 混合极端层：T=20，最大区间 / 单点 / 相邻点 / 小值 混排（覆盖跨周期与边界回绕）
#
# 生成方式：纯 Python 写出 .in，再用 subprocess 显式调用 std 生成 .out（不使用 cyaron 的
#   output_gen，规避其写缓冲不 flush 导致 0 字节 .out 的隐患）。每个 .out 都断言：
#   文件非空、行数 == T、每行是整数、0 <= 答案 <= R-L+1；并对 1-4 号点断言手算/样例期望值。
#
# 随机性：每个随机点使用独立 random.Random(1807 + 点号)，可精确复现。
# 复杂度：所有生成均为 O(T) 次随机与写文件，无任何 O(n^2) Python 循环。

import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
WORK_DIR = os.path.join(HERE, "work")
STD = os.path.join(WORK_DIR, "std")
STD_SRC = os.path.join(HERE, "std.cpp")
MAXV = 10 ** 18

REPORT = []


def ensure_std():
    """编译 std.cpp 到 work/std（已存在则复用）。运行结束时会删除编译产物。"""
    os.makedirs(WORK_DIR, exist_ok=True)
    if not os.path.exists(STD):
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD, STD_SRC],
                       check=True, timeout=120)
    assert os.path.exists(STD), "std 编译失败"


def run_std(in_path, out_path):
    """显式用 std 产出 .out（不用 cyaron output_gen，避免缓冲不 flush 出 0 字节）。"""
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        subprocess.run([STD], stdin=fi, stdout=fo, check=True, timeout=120)
    fo_size = os.path.getsize(out_path)
    assert fo_size > 0, "%s 为空（0 字节）" % out_path


def write_case(idx, queries, expect=None, note=""):
    for (L, R) in queries:
        assert 1 <= L <= R <= MAXV, "询问越界: %d %d" % (L, R)
    in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
    out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
    with open(in_path, "w") as f:
        f.write("%d\n" % len(queries))
        for (L, R) in queries:
            f.write("%d %d\n" % (L, R))
    run_std(in_path, out_path)

    with open(out_path) as f:
        lines = [ln.strip() for ln in f if ln.strip() != ""]
    assert len(lines) == len(queries), \
        "problem%d.out 行数 %d != T %d" % (idx, len(lines), len(queries))
    vals = [int(x) for x in lines]
    for (L, R), v in zip(queries, vals):
        assert 0 <= v <= R - L + 1, "problem%d.out 答案越界: %d" % (idx, v)
    if expect is not None:
        assert vals == list(expect), \
            "problem%d.out 期望 %s 实际 %s" % (idx, list(expect), vals)

    REPORT.append((idx, len(queries), note, os.path.getsize(in_path), os.path.getsize(out_path)))
    print("problem%-2d: T=%-2d in=%-5dB out=%-4dB  %s" % (idx, len(queries),
                                                          os.path.getsize(in_path),
                                                          os.path.getsize(out_path), note))
    return vals


def rnd_query(rng, lo, hi):
    L = rng.randint(lo, hi)
    R = rng.randint(L, hi)
    return (L, R)


def main():
    ensure_std()
    os.makedirs(DATA_DIR, exist_ok=True)

    # ---- 点 1：题面【输入样例】原样（回归验证） ----
    write_case(1, [(1, 5), (3, 9), (8, 8)], expect=[2, 2, 0],
               note="样例层：题面【输入样例】原样，期望 2 2 0")

    # ---- 点 2：边界层，最小询问（手算：喜欢的数依次为 1,4,9,10,...） ----
    write_case(2, [(1, 1), (1, 2), (1, 3), (1, 4)], expect=[1, 1, 1, 2],
               note="边界层：最小询问 [1,1]..[1,4]，手算 1 1 1 2")

    # ---- 点 3：小规模手算层 ----
    write_case(3, [(1, 10), (1, 100), (100, 200)], expect=[4, 29, 27],
               note="小规模手算层：[1,10]=4 [1,100]=29 [100,200]=27")

    # ---- 点 4：周期边界层（81/82 是 std 小值枚举与周期计数的分界） ----
    q4 = [(1, 81), (1, 82), (82, 82), (1, 100), (82, 100), (81, 82),
          (2, 81), (80, 82), (1, 22680), (22681, 45360), (1, 45361), (22680, 22680),
          (1, 81), (82, 162), (162, 162), (1, 1000), (83, 83), (22679, 22681),
          (1, 1), (100, 200)]
    v4 = write_case(4, q4, note="周期边界层：81/82 分界与整周期 22680 对齐")
    # 区间可加性自检（手算无关的结构性一致）：[1,100] - [1,81] == [82,100]
    assert v4[3] - v4[0] == v4[4], "点 4 区间可加性自检失败: %d-%d != %d" % (v4[3], v4[0], v4[4])
    assert v4[1] - v4[0] == v4[2], "点 4 边界自检失败"

    # ---- 点 5：30% 档，L,R <= 10^6 ----
    rng = random.Random(1807 + 5)
    write_case(5, [rnd_query(rng, 1, 10 ** 6) for _ in range(20)],
               note="30% 档：T=20，L,R <= 10^6 随机")

    # ---- 点 6：中间档，L,R <= 10^9 ----
    rng = random.Random(1807 + 6)
    write_case(6, [rnd_query(rng, 1, 10 ** 9) for _ in range(20)],
               note="中间档：T=20，L,R <= 10^9 随机")

    # ---- 点 7：100% 档，L,R <= 10^18 ----
    rng = random.Random(1807 + 7)
    write_case(7, [rnd_query(rng, 1, MAXV) for _ in range(20)],
               note="100% 档：T=20，L,R <= 10^18 随机")

    # ---- 点 8：顶格单点层，L=R 在 10^18 附近 ----
    rng = random.Random(1807 + 8)
    q8 = [(MAXV, MAXV)]
    for _ in range(19):
        p = rng.randint(MAXV - 10 ** 6, MAXV)
        q8.append((p, p))
    write_case(8, q8, note="顶格单点层：L=R 在 10^18 附近（答案 0/1）")

    # ---- 点 9：顶格全区间层 ----
    q9 = [(1, MAXV)]
    rng = random.Random(1807 + 9)
    for _ in range(19):
        q9.append((rng.randint(1, 1000), MAXV - rng.randint(0, 1000)))
    write_case(9, q9, note="顶格全区间层：答案最大档（含 [1,10^18]）")

    # ---- 点 10：混合极端层 ----
    rng = random.Random(1807 + 10)
    q10 = [
        (1, MAXV), (1, MAXV - 1), (2, MAXV), (MAXV - 1, MAXV), (MAXV, MAXV),
        (1, 1), (1, 9), (9, 9), (10, 10), (81, 81), (82, 82), (81, 82),
        (MAXV // 2, MAXV // 2), (MAXV // 2, MAXV // 2 + 1),
        (MAXV - 10 ** 9, MAXV), (10 ** 18 - 10 ** 9, 10 ** 18 - 10 ** 9 + 10 ** 6),
        (1, 10 ** 9), (10 ** 9, 10 ** 18), (999999999999999999, MAXV),
        (1, 22680),
    ]
    q10 = [(L, R) for (L, R) in q10 if L <= R]
    v10 = write_case(10, q10, note="混合极端层：最大区间/单点/相邻/小值/跨周期混排")
    # 结构性自检：[1,10^18] - [1,10^18-1] == [10^18,10^18]
    assert v10[0] - v10[1] == v10[4], "点 10 区间可加性自检失败"

    # ---- 汇总 ----
    print("\n共生成 %d 个测试点（data/problem1.in/.out .. problem10.in/.out）" % len(REPORT))
    print("总 in 字节 = %d，总 out 字节 = %d" % (sum(r[3] for r in REPORT), sum(r[4] for r in REPORT)))
    print("全部断言通过（非空 / 行数 == T / 答案范围 / 样例与手算期望 / 区间可加性）。")

    # 清理编译产物（只留 std.cpp / data.py / data/ / gen-report.md）
    import shutil
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    print("已清理编译产物 work/")


if __name__ == "__main__":
    sys.exit(main())
