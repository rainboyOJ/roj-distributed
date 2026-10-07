#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1801《异或》分层测试数据生成器

用法（在 .ybt-import/staging/1801/ 下）：
    nice -n 19 timeout 120 g++ -O2 -std=c++17 -o std std.cpp
    nice -n 19 timeout 120 python3 data.py
产物：data/problem1.in + data/problem1.out ... data/problem10.in + data/problem10.out

关于 .out 的产生方式（避开 cyaron output_gen 写缓冲不 flush 的坑）：
    本脚本**不使用 cyaron**，输入直接写盘并 flush；随后用 subprocess 显式调用 std
    （`nice -n 19 timeout 120 ./std < problemN.in > problemN.out`）生成 .out，
    再逐点断言：.out 非空、恰好 1 行、内容为非负整数；对"手算/题面样例"的测试点
    逐值比对期望；并对全部 10 点断言答案随 n 单调不减（合法不变量，非暴力）。

题意：给定正整数 n，求 [1,n] 内满足 gcd(a,b) = a xor b 的**无序**数对 (a,b) 个数。
输入：一行一个正整数 n。输出：一行一个正整数（答案）。
数据规模（content.md）：30% n<=1000；60% n<=10^5；100% n<=10^7。

分层策略（10 个测试点，从小到大铺到顶格；本题单文件单整数，故每点一个 n）：
    problem1  n=1         边界层（最小 n，无合法数对 -> 0）
    problem2  n=3         题面样例层（content.md 样例 3 -> 1）
    problem3  n=30        小规模手算层（手工枚举 31 对，独立校验 -> 31）
    problem4  n=1000      30% 数据上限
    problem5  n=65536     2^16（幂次边界，小规模）
    problem6  n=100000    60% 数据上限
    problem7  n=1000000   10^6（大规模）
    problem8  n=1048576   2^20（幂次边界，大规模）
    problem9  n=9999999   10^7-1（近顶格）
    problem10 n=10000000  100% 数据上限（顶格）
"""

import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

NMAX = 10 ** 7  # content.md：100% 数据 n <= 10^7

# ------------------------------------------------- 手算 / 题面样例 期望值（独立于 std）
# 推导依据（不含任何暴力枚举程序，均为手工枚举）：
#   gcd(a,b)=a xor b 时必有 gcd(a,b) = a-b = a xor b =: c，等价于 c|a 且 (a & c)==0，
#   b = a+c。据此手工列出 n<=30 的全部数对：
#     n=1  ：无数对                                   -> 0
#     n=3  ：(2,3)                                    -> 1（题面样例）
#     n=30 ：g=1 共 14 对(2..28 的偶数 a)，
#            g=2 共 7 对(4,8,...,28)，g=3 共 2 对(12,24)，g=4 共 3 对(8,16,24)，
#            g=5 共 1 对(10,15)，g=6 共 1 对(24,30)，g=8 共 1 对(16,24)，
#            g=9 共 1 对(18,27)，g=10 共 1 对(20,30) -> 31
GOLDEN = [
    (1, 0, "最小 n：无合法数对"),
    (3, 1, "题面样例：只有 (2,3) 满足"),
    (30, 31, "手工枚举（按 c=gcd 分层计数）"),
]

# ---------------------------------------------------------------- 测试点定义
# (idx, n, 备注, 期望值或 None)
def build_cases():
    return [
        (1, 1, "边界层：n=1（最小输入，答案 0）", 0),
        (2, 3, "题面样例层：n=3（content.md 样例 3 -> 1）", 1),
        (3, 30, "小规模手算层：n=30（手工枚举 31 对）", 31),
        (4, 1000, "30% 数据上限：n=1000", None),
        (5, 65536, "小规模幂次边界：n=2^16", None),
        (6, 100000, "60% 数据上限：n=1e5", None),
        (7, 1000000, "大规模：n=1e6", None),
        (8, 1048576, "大规模幂次边界：n=2^20", None),
        (9, 9999999, "近顶格：n=1e7-1", None),
        (10, NMAX, "顶格：n=1e7（100% 数据上限）", None),
    ]


def write_in(path, n):
    # 直接写盘 + with 收尾 flush/close，避免缓冲未落盘
    with open(path, "w", encoding="ascii") as f:
        f.write("%d\n" % n)
    # 回读断言：单行、内容恰为 n
    with open(path, "r", encoding="ascii") as f:
        lines = f.read().split("\n")
    assert lines[-1] == "" and len(lines) == 2, "%s 应为 1 行 + 结尾换行" % path
    assert int(lines[0]) == n, "%s 内容 %r != n=%d" % (path, lines[0], n)
    return os.path.getsize(path)


def run_std(in_path, out_path):
    t0 = time.time()
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        # 耗时命令统一 nice -n 19 timeout 120 包裹
        subprocess.run(["nice", "-n", "19", "timeout", "120", STD],
                       stdin=fi, stdout=fo, check=True)
    return time.time() - t0


def verify(out_path, n, expect):
    size = os.path.getsize(out_path)
    assert size > 0, "%s 为空文件（.out 必须非空）" % out_path
    with open(out_path, "r", encoding="ascii") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 1, "%s 行数 %d != 1（本题单行输出）" % (out_path, len(lines))
    s = lines[0].strip()
    assert s.lstrip("-").isdigit(), "%s 非整数: %r" % (out_path, s)
    v = int(s)
    assert v >= 0, "%s 答案为负: %d" % (out_path, v)
    if expect is not None:
        assert v == expect, "%s (n=%d) 期望 %d 实得 %d" % (out_path, n, expect, v)
    return v, size


def main():
    if not os.path.isfile(STD):
        print("缺少可执行 std，请先编译：nice -n 19 timeout 120 g++ -O2 -std=c++17 -o std std.cpp",
              file=sys.stderr)
        return 1
    os.makedirs(DATA_DIR, exist_ok=True)
    cases = build_cases()
    assert len(cases) == 10, "必须恰好 10 个测试点"

    rows = []
    answers = []
    for idx, n, note, expect in cases:
        in_path = os.path.join(DATA_DIR, "problem%d.in" % idx)
        out_path = os.path.join(DATA_DIR, "problem%d.out" % idx)
        t0 = time.time()
        in_size = write_in(in_path, n)
        t_gen = time.time() - t0
        t_std = run_std(in_path, out_path)
        ans, out_size = verify(out_path, n, expect)
        answers.append(ans)
        rows.append((idx, n, in_size, out_size, t_gen, t_std, ans, note))
        print("problem%-2d n=%-9d in=%-4d out=%-4d gen=%5.3fs std=%6.3fs ans=%-9d  %s"
              % (idx, n, in_size, out_size, t_gen, t_std, ans, note))

    # 不变量：答案随 n 单调不减（合法性质，非暴力）
    for i in range(1, len(answers)):
        assert answers[i] >= answers[i - 1], \
            "答案非单调：n=%d 得 %d < 前点 %d" % (cases[i][1], answers[i], answers[i - 1])
    # 手算/样例期望再次确认（在 GOLDEN 表内的点必须命中）
    for n, e, _why in GOLDEN:
        idx = next(i for i, c in enumerate(cases) if c[1] == n)
        assert answers[idx] == e, "GOLDEN n=%d 期望 %d 实得 %d" % (n, e, answers[idx])

    # data.json（与仓库其它 staging 目录同格式）
    files = []
    for idx in range(1, 11):
        for ext in ("in", "out"):
            p = "problem%d.%s" % (idx, ext)
            files.append({"path": p, "size": os.path.getsize(os.path.join(DATA_DIR, p))})
    with open(os.path.join(HERE, "data.json"), "w", encoding="utf-8") as f:
        json.dump({"files": files}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("\n全部 10 点生成 + 校验通过（非空/单行/非负/单调/GOLDEN 命中）；"
          "data.json 已更新（%d 个文件）。" % len(files))
    print("答案序列：", answers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
