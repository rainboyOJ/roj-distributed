#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1776《最大值》 —— 测试数据生成器（分层 10 组）

题面范围: 1<=T<=6, 2<=n<=10^5, 1<=A_i<2^20, c∈{1,2,3}（c=1→and, c=2→xor, c=3→or）

用法:
    nice -n 19 timeout 120 python3 data.py

产物:
    data/problem1.in/.out ... data/problem10.in/.out

工程约束（按任务书）:
  * 不写、不跑任何 brute/对拍/stress —— 只做「std 输出 + 手推期望值/结构性断言」的验证；
  * 生成器全程单层 O(n) 列表推导，无 O(n^2) Python 循环；
  * .out 由 subprocess 显式调用 ./std 产生（不用 cyaron 的 output_gen，避免写缓冲未 flush
    导致 0 字节 .out 的隐患），并断言 .out 非空、行数 == T、每行是非负整数；
  * 所有耗时命令用 nice -n 19 timeout 120 包裹。
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

MAXV = (1 << 20) - 1          # 题面 A_i < 2^20 → 值域顶格 1048575
NMAX = 100000                 # 题面 n 上限
TMAX = 6                      # 题面 T 上限

# ---------------------------------------------------------------- 生成原语

def rand_vals(rnd, n, lo, hi):
    """单层 O(n) 生成 n 个 [lo,hi] 的随机整数（无嵌套循环）"""
    return [rnd.randint(lo, hi) for _ in range(n)]


def cases_summary(cases):
    return "; ".join("n=%d c=%d max=%d" % (n, c, max(v)) for (n, c, v) in cases)


# ---------------------------------------------------------------- 10 个测试点

def build_points():
    """返回 [(点号, 分层说明, [(n, c, vals, expect_or_None, extra_check)], 备注)]"""
    points = []

    # 1 边界层: 最小规模 + 最小取值 → 答案 1（AND 的最小可能正答案）
    points.append((1, "边界层 n=2 最小规模/最小取值", [(2, 1, [1, 1], 1, None)]))

    # 2 边界层: XOR 最小答案 0（两个顶格相同值）
    points.append((2, "边界层 XOR 答案下界 0", [(2, 2, [MAXV, MAXV], 0, None)]))

    # 3 边界层: OR 答案上界（顶格值）
    points.append((3, "边界层 OR 答案上界 2^20-1", [(2, 3, [MAXV, 1], MAXV, None)]))

    # 4 样例层: 题面样例逐字复现（必须与题面输出 5/7/13 一致）
    points.append((4, "样例层（题面样例）", [
        (5, 1, [1, 4, 5, 7, 9], 5, None),
        (5, 2, [2, 3, 4, 5, 7], 7, None),
        (5, 3, [9, 5, 4, 2, 1], 13, None),
    ]))

    # 5 小规模层: 3 个可手算的定向小例 + 3 个可手算的小随机
    #    其中 {10,5,12} 是「最大元素不在最优或对中」的定向反例（10|5=15 > 12|10=14），
    #    专门用来毙掉「最大值与次大值配对」的错解。
    rnd5 = random.Random(1776 + 5)
    pts5 = [
        (3, 3, [10, 5, 12], 15, None),
        (3, 1, [12, 10, 5], 8, None),
        (3, 2, [12, 10, 5], 15, None),
    ]
    for c in (1, 2, 3):
        n = rnd5.randint(2, 50)
        pts5.append((n, c, rand_vals(rnd5, n, 1, 1023), None, None))
    points.append((5, "小规模层 n<=50, A<=1023（含定向反例）", pts5))

    # 6 中规模层: n=1000, A<=1024（覆盖「A<=1024」子任务），每算子 2 组
    rnd6 = random.Random(1776 + 6)
    pts6 = []
    for c in (1, 1, 2, 2, 3, 3):
        pts6.append((1000, c, rand_vals(rnd6, 1000, 1, 1024), None, None))
    points.append((6, "中规模层 n=1000, A<=1024", pts6))

    # 7 中大规模层: n=10000, A<2^20，每算子 2 组
    rnd7 = random.Random(1776 + 7)
    pts7 = []
    for c in (1, 1, 2, 2, 3, 3):
        pts7.append((10000, c, rand_vals(rnd7, 10000, 1, MAXV), None, None))
    points.append((7, "中大规模层 n=10000, A<2^20", pts7))

    # 8 大规模层: n 顶格 1e5，AND 专项（c 恒为 1 的子任务），6 种结构
    rnd8 = random.Random(1776 + 8)
    pts8 = [
        (NMAX, 1, [MAXV] * NMAX, MAXV, None),                                   # 全顶格值 → AND 顶格
        (NMAX, 1, [MAXV] + rand_vals(rnd8, NMAX - 1, 1, MAXV >> 1), None,
         ("lt", 1 << 19)),                                                      # 仅 1 个含 bit19 → 该位必被舍弃
        (NMAX, 1, rand_vals(rnd8, NMAX, 1, MAXV), None, None),                   # 全域随机
        (NMAX, 1, [1] * NMAX, 1, None),                                          # 全 1 → 答案 1
        (NMAX, 1, rand_vals(rnd8, NMAX, 1 << 19, MAXV), None, ("ge", 1 << 19)),  # 全部含 bit19
        (NMAX, 1, rand_vals(rnd8, NMAX, 1, 1023), None, ("le", 1023)),           # 小值域
    ]
    points.append((8, "大规模层 n=1e5 AND 专项", pts8))

    # 9 大规模层: n 顶格 1e5，XOR 专项（c 恒为 2 的子任务），6 种结构
    rnd9 = random.Random(1776 + 9)
    half9 = rand_vals(rnd9, NMAX // 2, 1, MAXV >> 1)
    comp9 = []
    for x in half9:                       # 互补对 (x, MAXV^x) → 每对异或均为顶格值
        comp9.append(x)
        comp9.append(MAXV ^ x)
    pts9 = [
        (NMAX, 2, rand_vals(rnd9, NMAX, 1, MAXV), None, None),                   # 全域随机
        (NMAX, 2, [MAXV] * NMAX, 0, None),                                       # 全同值 → 答案 0
        (NMAX, 2, comp9, MAXV, None),                                            # 互补对 → 答案顶格
        (NMAX, 2, rand_vals(rnd9, NMAX, 1 << 19, MAXV), None, ("lt", 1 << 19)),  # 全部含 bit19 → 异或该位为 0
        (NMAX, 2, rand_vals(rnd9, NMAX, 1, 1023), None, ("le", 1023)),           # 小值域
        (NMAX, 2, [12345] * NMAX, 0, None),                                      # 全同值（非顶格）
    ]
    points.append((9, "大规模层 n=1e5 XOR 专项", pts9))

    # 10 顶格层: n 与值域双顶格，OR 专项（c 恒为 3 的子任务），6 种结构
    rnd10 = random.Random(1776 + 10)
    pts10 = [
        (NMAX, 3, rand_vals(rnd10, NMAX, 1, MAXV), None, None),                  # 全域随机
        (NMAX, 3, [MAXV] * NMAX, MAXV, None),                                    # 全顶格值
        (NMAX, 3, [MAXV] + rand_vals(rnd10, NMAX - 1, 1, MAXV >> 1), MAXV, None),# 顶格值参与 → OR 顶格
        (NMAX, 3, rand_vals(rnd10, NMAX, 1, (1 << 19) - 1), None, ("lt", 1 << 19)),  # 全体无 bit19：高位必被舍弃，最坏结构
        (NMAX, 3, [1] * NMAX, 1, None),                                          # 全 1 → 答案 1
        (NMAX, 3, rand_vals(rnd10, NMAX, 1, 1023), None, ("le", 1023)),          # 小值域
    ]
    points.append((10, "顶格层 n=1e5 且 A 顶格, OR 专项", pts10))

    return points


# ---------------------------------------------------------------- 写出 + 校验

def write_in(path, cases):
    lines = [str(len(cases))]
    for (n, c, vals, _expect, _extra) in cases:
        assert len(vals) == n, "值个数与 n 不符"
        assert 2 <= n <= NMAX, "n 越界"
        assert c in (1, 2, 3), "c 越界"
        assert all(1 <= v <= MAXV for v in vals), "A_i 越界"
        lines.append("%d %d" % (n, c))
        lines.append(" ".join(map(str, vals)))
    text = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(text)
    return len(cases)


def run_std(in_path, out_path):
    """显式调用 std 生成 .out（nice -n 19 timeout 120 包裹）"""
    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        subprocess.run(["nice", "-n", "19", "timeout", "120", STD],
                       stdin=fin, stdout=fout, stderr=subprocess.PIPE, check=True)
    fout_size = os.path.getsize(out_path)
    assert fout_size > 0, "%s 为空（0 字节 .out）" % out_path
    return fout_size


def check_out(in_path, out_path, cases):
    """断言: 行数 == T、每行为非负整数、结构性范围、以及手推期望值"""
    with open(out_path) as f:
        out_lines = [ln.strip() for ln in f if ln.strip() != ""]
    assert len(out_lines) == len(cases), \
        "%s 输出行数 %d != T=%d" % (out_path, len(out_lines), len(cases))
    ans = []
    for k, (ln, (n, c, vals, expect, extra)) in enumerate(zip(out_lines, cases)):
        assert ln.lstrip("-").isdigit(), "%s 第 %d 行不是整数: %r" % (out_path, k + 1, ln)
        x = int(ln)
        assert x >= 0, "答案不可能为负"
        hi = max(vals).bit_length() - 1
        assert x <= (1 << (hi + 1)) - 1, "答案超出值域位数"
        if c == 1:
            assert x <= max(vals), "AND 结果不可能大于最大值"
        elif c == 3:
            assert x >= max(vals), "OR 结果不可能小于最大值"
        if expect is not None:
            assert x == expect, "%s 第 %d 行 = %d, 手推期望 %d" % (out_path, k + 1, x, expect)
        if extra is not None:
            kind, bound = extra
            if kind == "lt":
                assert x < bound, "%s 第 %d 行 = %d, 期望 < %d" % (out_path, k + 1, x, bound)
            elif kind == "le":
                assert x <= bound, "%s 第 %d 行 = %d, 期望 <= %d" % (out_path, k + 1, x, bound)
            elif kind == "ge":
                assert x >= bound, "%s 第 %d 行 = %d, 期望 >= %d" % (out_path, k + 1, x, bound)
        ans.append(x)
    return ans


def main():
    assert os.path.exists(STD), "先编译 std: g++ -O2 -std=c++17 std.cpp -o std"
    os.makedirs(DATA_DIR, exist_ok=True)

    points = build_points()
    assert len(points) == 10, "必须 10 个测试点"

    rows = []
    for idx, layer, cases, in points:
        in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
        out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
        T = write_in(in_path, cases)
        assert T <= TMAX, "T 越界"

        # 结构自检: .in 行数 == 1 + 2T（第一行 T，之后每组两行）
        with open(in_path) as f:
            n_lines = sum(1 for _ in f)
        assert n_lines == 1 + 2 * T, "%s 行数 %d != %d" % (in_path, n_lines, 1 + 2 * T)

        size = run_std(in_path, out_path)
        ans = check_out(in_path, out_path, cases)
        rows.append((idx, layer, T, in_path, size, ans))
        print("[point %2d] %-38s T=%d  %8.1f KB  ans=%s"
              % (idx, layer, T, size / 1024.0, ans))

    # 汇总自检: .in/.out 成对齐全
    ins = sorted((f for f in os.listdir(DATA_DIR) if f.endswith(".in")),
                 key=lambda f: int(f[len("problem"):-len(".in")]))
    outs = sorted((f for f in os.listdir(DATA_DIR) if f.endswith(".out")),
                  key=lambda f: int(f[len("problem"):-len(".out")]))
    assert len(ins) == 10 and len(outs) == 10, "数据文件不成对: %d in / %d out" % (len(ins), len(outs))
    assert ins == ["problem%d.in" % i for i in range(1, 11)], ins
    assert outs == ["problem%d.out" % i for i in range(1, 11)], outs
    print("OK: 10 组数据全部生成并通过结构/范围/手推期望断言")


if __name__ == "__main__":
    sys.exit(main())
