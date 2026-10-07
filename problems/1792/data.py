#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1792 小P的牧场 —— 数据生成脚本
分层造 10 组 problem1.in/.out ... problem10.in/.out。
用 std（本目录已编译的 ./std）显式产出 .out，并断言 .out 非空且恰为 1 行整数。
禁止 brute/对拍/stress；生成过程无 O(n^2) Python 循环。
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
MAXB = 10000  # a_i, b_i <= 10000


def rand_ints(n, lo, hi, rng):
    """返回长度为 n 的随机整数列表（走 C 实现的 random.choices，快）。"""
    return rng.choices(range(lo, hi + 1), k=n)


def write_case(idx, n, a, b):
    assert len(a) == n and len(b) == n
    inp = os.path.join(HERE, "problem%d.in" % idx)
    out = os.path.join(HERE, "problem%d.out" % idx)
    with open(inp, "w") as fp:
        fp.write("%d\n" % n)
        fp.write(" ".join(map(str, a)))
        fp.write("\n")
        fp.write(" ".join(map(str, b)))
        fp.write("\n")
    # 显式跑 std 产出 .out（不依赖 cyaron 写缓冲）
    with open(inp, "rb") as fin:
        res = subprocess.run([STD], stdin=fin, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=120)
    assert res.returncode == 0, "std 非零退出 case %d: %s" % (idx, res.stderr[:200])
    data = res.stdout.decode().strip()
    assert data, "case %d: std 输出为空" % idx
    lines = [l for l in data.splitlines() if l.strip() != ""]
    assert len(lines) == 1, "case %d: 期望 1 行输出，实得 %d 行" % (idx, len(lines))
    assert lines[0].lstrip("-").isdigit(), "case %d: 输出非整数 %r" % (idx, lines[0])
    with open(out, "w") as fp:
        fp.write(lines[0] + "\n")
    return int(lines[0])


def ensure_std():
    src = os.path.join(HERE, "std.cpp")
    if (not os.path.exists(STD)) or os.path.getmtime(STD) < os.path.getmtime(src):
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD, src], check=True)


def main():
    ensure_std()
    rng = random.Random(20240517)
    plan = []

    # 1) 边界：n=1
    plan.append((1, 1, [7], [3]))

    # 2) 小：n=2
    plan.append((2, 2, [5, 1], [2, 9]))

    # 3) 20% 边界：n=10 随机
    plan.append((3, 10, rand_ints(10, 1, 20, rng), rand_ints(10, 1, 20, rng)))

    # 4) 40% 边界：n=1000 随机（值域顶格）
    plan.append((4, 1000, rand_ints(1000, 1, MAXB, rng), rand_ints(1000, 1, MAXB, rng)))

    # 5) 70% 边界：n=100000 随机
    plan.append((5, 100000, rand_ints(100000, 1, MAXB, rng), rand_ints(100000, 1, MAXB, rng)))

    # 6) 100% 规模：n=1000000 随机
    plan.append((6, 1000000, rand_ints(1000000, 1, MAXB, rng), rand_ints(1000000, 1, MAXB, rng)))

    # 7) 顶格值：n=1000000, a=b=10000（只建 1 站，答案接近上界）
    plan.append((7, 1000000, [MAXB] * 1000000, [MAXB] * 1000000))

    # 8) 最小值：n=1000000, a=b=1（每点建站，答案小）
    plan.append((8, 1000000, [1] * 1000000, [1] * 1000000))

    # 9) 每点建站：n=1000000, a=1, b=10000
    plan.append((9, 1000000, [1] * 1000000, [MAXB] * 1000000))

    # 10) 混合顶格：n=1000000, b=10000, a 随机（大答案、测 long long 与凸壳切换）
    plan.append((10, 1000000, rand_ints(1000000, 1, MAXB, rng), [MAXB] * 1000000))

    # 手算微样例校验 std（非 brute，仅固定已知答案）
    micro = [
        ("1\n7\n3\n", 7),
        ("2\n5 1\n2 9\n", 3),
        ("3\n1 100 1\n10 10 10\n", 12),
        ("3\n10 10 10\n1 1 1\n", 13),
        ("4\n2 4 2 4\n3 1 4 2\n", 9),
    ]
    for text, exp in micro:
        r = subprocess.run([STD], input=text.encode(), stdout=subprocess.PIPE, timeout=60)
        got = int(r.stdout.decode().strip())
        assert got == exp, "微样例失配: 期望 %d 实得 %d (in=%r)" % (exp, got, text)

    for idx, n, a, b in plan:
        ans = write_case(idx, n, a, b)
        print("problem%d.in  n=%-8d ans=%d" % (idx, n, ans))
    print("OK: 10 组数据已生成并校验")


if __name__ == "__main__":
    sys.exit(main())
