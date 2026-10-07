#!/usr/bin/env python
# 一本通 1772《动漫排序》测试数据生成器
#
# 用法（在本题目录下）：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && python3 ../data.py
#
# 数据范围（题面）：T 组数据；每组 n <= 1000（30%: n<=10，60%: n<=100，100%: n<=1000）；
#   每行给出 tot 与该点的 tot 个孩子编号（顺序即喜爱度降序，也就是必须满足的相对顺序）。
# 分层：1-2 边界；3 题面样例；4-5 小规模（30% 档）；6-7 中等（60% 档）；8 大规模随机（100% 档）；
#   9 顶格最坏结构（深链）；10 顶格多组混合（T=5, sum n = 5000）。
#
# 说明：答案 mod 10007（质数）且 n <= 1000 < 10007，组合数因子均非零，故答案恒不为 0，
#   不存在「答案为 0」的边界点，用「答案为 1」的极端结构（链/星）替代。

import os
import random
import subprocess
import sys

from cyaron import *  # 引入CYaRon的库

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
MAXN = 1000  # 题面上限


def build_tree(n, mode, rng):
    """构造 n 个点、以 1 为根的树，返回 children 列表（下标 1..n）。

    mode: chain 链 / star 菊花 / binary 完全二叉树 / deep 深窄随机 / random 随机
    """
    ch = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        if mode == "chain":
            p = v - 1
        elif mode == "star":
            p = 1
        elif mode == "binary":
            p = v // 2
        elif mode == "deep":
            p = rng.randint(max(1, v - 3), v - 1)  # 偏向深链
        else:
            p = rng.randint(1, v - 1)  # 均匀随机树（期望深度 O(log n)）
        ch[p].append(v)
    for v in range(1, n + 1):
        rng.shuffle(ch[v])  # 孩子的喜爱度顺序本身是任意的
    return ch


def write_case(io, ch):
    n = len(ch) - 1
    io.input_writeln(n)
    for v in range(1, n + 1):
        io.input_writeln([len(ch[v])] + list(ch[v]))


def run_std(in_path):
    with open(in_path, "rb") as f:
        proc = subprocess.run([STD], stdin=f, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError("std failed on %s: rc=%d err=%s"
                           % (in_path, proc.returncode, proc.stderr[:300]))
    return proc.stdout.decode().strip()


# ---- 每个测试点的构造方案：(说明, [ (n, mode, seed), ... ]) ----
PLAN = [
    ("边界最小：T=1, n=1（单点树，答案恒为 1）", [(1, "chain", 1)]),
    ("边界最小非平凡：T=1, n=2 链 1->2（答案 1）", [(2, "chain", 2)]),
    ("题面样例：T=1, n=5（期望输出 2）", [(5, "sample", 3)]),
    ("小规模随机（30% 档）：T=1, n=10", [(10, "random", 11)]),
    ("小规模多组（30% 档）：T=3, n=10 随机/星/链", [(10, "random", 21),
                                                    (10, "star", 22),
                                                    (10, "chain", 23)]),
    ("中等规模随机（60% 档）：T=1, n=100", [(100, "random", 31)]),
    ("中等规模（60% 档）：T=2, n=100 随机 + 完全二叉树",
     [(100, "random", 41), (100, "binary", 42)]),
    ("大规模随机（100% 档）：T=1, n=1000 均匀随机树", [(1000, "random", 51)]),
    ("顶格最坏结构：T=1, n=1000 深链（深度 1000，考察非递归/栈安全）",
     [(1000, "chain", 61)]),
    ("顶格多组混合：T=5, 每组 n=1000（随机/星/链/完全二叉树/深窄随机，sum n=5000）",
     [(1000, "random", 71), (1000, "star", 72), (1000, "chain", 73),
      (1000, "binary", 74), (1000, "deep", 75)]),
]


def main():
    if not os.path.exists(STD):
        print("std not found, compile first: g++ -O2 -std=c++17 std.cpp -o std", file=sys.stderr)
        return 1

    for i, (desc, cases) in enumerate(PLAN, start=1):
        io = IO(file_prefix="problem", data_id=i)
        rng = random.Random(1000 + i)
        io.input_writeln(len(cases))  # 第一行 T：数据组数
        for (n, mode, seed) in cases:
            if mode == "sample":
                # 题面【输入样例】原样
                io.input_writeln(5)
                io.input_writeln([3, 4, 3, 2])
                io.input_writeln([0])
                io.input_writeln([1, 5])
                io.input_writeln([0])
                io.input_writeln([0])
                continue
            write_case(io, build_tree(n, mode, rng))
        io.flush_buffer()

        in_path = "problem%d.in" % i
        out_path = "problem%d.out" % i
        assert os.path.getsize(in_path) > 0, "%s is empty" % in_path

        text = run_std(in_path)
        lines = [ln for ln in text.split("\n") if ln != ""]
        # 断言：无解空输出点不存在，行数必须等于数据组数，且每行都是合法答案
        assert len(lines) == len(cases), \
            "%s: expected %d answer lines, got %d" % (out_path, len(cases), len(lines))
        for ln in lines:
            assert ln.isdigit() and 0 <= int(ln) < 10007, "%s: bad answer %r" % (out_path, ln)
        assert os.path.getsize(in_path) > 0

        io.output_write("\n".join(lines) + "\n")
        io.close()

        assert os.path.getsize(out_path) > 0, "%s is empty (flush problem?)" % out_path
        print("problem%d: %-6s cases=%d in=%dB out=%dB -> %s"
              % (i, "", len(cases), os.path.getsize(in_path), os.path.getsize(out_path),
                 " ".join(lines[:6])))
        print("    # %s" % desc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
