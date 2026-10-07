#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1750《取数字》数据生成器

用法：
    mkdir -p data && cd data && python3 ../data.py          # 生成全部 10 组
    mkdir -p data && cd data && python3 ../data.py 10       # 只生成第 10 组

题面数据范围（content.md / ybt 1750）：
    N <= 300000, A_i <= 10^9, 且「N 个互不相同的数」=> 所有 a_i 互不相同。

安全系数：所有数组按 N*1.5 预分配；生成器全部为 O(n) 单层循环（无 O(n^2) 结构）。

⚠ cyaron 隐患规避（任务书要求）：
    1) 先校验 ../std 存在（不存在直接退出，避免 output_gen 静默产出 0 字节 .out）；
    2) .in 用 with 块写入并 flush 收尾；
    3) .out 由 subprocess 显式调用 std 产生（stdin -> stdout），
       生成后断言 .out 非空且行数 == N（本题无「无解空输出」点）。

分层设计（10 组，边界/小/中/大/顶格 + 覆盖两个子任务）：
    点 1  边界：N=1（N 下限）+ A_1=10^9（权值上限）
    点 2  边界：N=2（N 下限）+ 极值对（1 与 10^9）
    点 3  样例：题面样例 N=3, 1 2 3 -> 3 3 4
    点 4  小：N=10 随机（可手算核对）
    点 5  小：N=5000 随机（覆盖子任务「N<=5000」，占 20%）
    点 6  中：N=30000 且 A_i=i（覆盖子任务「A_i=i」，占 20%）
    点 7  中：N=50000 随机（覆盖子任务「数据随机生成」，占 30%）
    点 8  大：N=100000 锯齿/交错结构（非随机结构，值互不相同）
    点 9  大：N=200000 随机
    点 10 顶格：N=300000 随机 + 值域接近 10^9（N 上限 + A_i 上限同组出现）
"""
import os
import random
import subprocess
import sys

from cyaron import IO

DATA_ID_ALL = list(range(1, 11))
STD_PATH = "../std"


def precheck():
    if not os.path.isfile(STD_PATH):
        sys.exit("FATAL: 标程 %s 不存在，请先编译：g++ -O2 -std=c++17 -o std std.cpp" % STD_PATH)
    if not os.access(STD_PATH, os.X_OK):
        sys.exit("FATAL: %s 不可执行" % STD_PATH)


def write_case(k, arr, note):
    """写 problem<k>.in（with + flush 收尾），用 std 产出 problem<k>.out 并做非空/行数断言。"""
    n = len(arr)
    assert len(set(arr)) == n, "点 %d: 题面要求所有数互不相同" % k
    assert n >= 1 and n <= 300000, "点 %d: N 越界" % k
    assert max(arr) <= 10 ** 9 and min(arr) >= -10 ** 9, "点 %d: A_i 越界" % k

    # --- 写 .in（显式 with 块 + flush） ---
    io = IO(file_prefix="problem", data_id=k)          # 创建 problem<k>.in / .out
    io.input_write(n, "\n", " ".join(map(str, arr)), "\n")
    io.close()                                         # flush 收尾
    in_name = "problem%d.in" % k
    with open(in_name, "r") as f:
        text = f.read()
    assert text.endswith("\n"), "点 %d: .in 未正常收尾" % k
    assert len(text.split()) == n + 1, "点 %d: .in 数字个数不符" % k

    # --- subprocess 显式跑 std 产 .out ---
    res = subprocess.run([STD_PATH], input=text, capture_output=True, text=True, timeout=600)
    assert res.returncode == 0, "点 %d: std 退出码 %d, stderr=%s" % (k, res.returncode, res.stderr[:200])
    out_name = "problem%d.out" % k
    with open(out_name, "w") as f:
        f.write(res.stdout)
        f.flush()

    # --- 非空 / 行数断言（本题每点都有输出，N 行） ---
    with open(out_name, "r") as f:
        got = f.read()
    assert got.strip() != "", "点 %d: .out 为空（0 字节风险）" % k
    lines = got.strip().split("\n")
    assert len(lines) == n, "点 %d: .out 行数 %d != N=%d" % (k, len(lines), n)
    for ln in lines:
        int(ln)                                        # 全部为整数
    print("point %2d OK  N=%-7d %s  首行=%s 末行=%s" % (k, n, note, lines[0], lines[-1]))


def rand_distinct(n, lo, hi, seed):
    """O(n) 生成 n 个互不相同的整数（random.sample）。"""
    rnd = random.Random(seed)
    return rnd.sample(range(lo, hi + 1), n)


def gen1():
    write_case(1, [10 ** 9], "边界 N=1 + 权值上限")


def gen2():
    write_case(2, [1, 10 ** 9], "边界 N=2 + 极值对")


def gen3():
    write_case(3, [1, 2, 3], "题面样例（期望 3 3 4）")


def gen4():
    write_case(4, rand_distinct(10, 1, 1000, 175004), "小规模随机")


def gen5():
    write_case(5, rand_distinct(5000, 1, 10 ** 9, 175005), "子任务 N<=5000 随机")


def gen6():
    write_case(6, list(range(1, 30001)), "子任务 A_i=i")


def gen7():
    write_case(7, rand_distinct(50000, 1, 10 ** 9, 175007), "中规模随机")


def gen8():
    # 锯齿结构：奇偶位交错大小值，互不相同，非随机
    n = 100000
    arr = []
    for i in range(n):
        if i % 2 == 0:
            arr.append(1 + i // 2)
        else:
            arr.append(10 ** 9 - i // 2)
    write_case(8, arr, "大规模锯齿结构")


def gen9():
    write_case(9, rand_distinct(200000, 1, 10 ** 9, 175009), "大规模随机")


def gen10():
    write_case(10, rand_distinct(300000, 1, 10 ** 9, 175010), "顶格 N=300000 随机 + 值域顶格")


GENS = {1: gen1, 2: gen2, 3: gen3, 4: gen4, 5: gen5,
        6: gen6, 7: gen7, 8: gen8, 9: gen9, 10: gen10}


if __name__ == "__main__":
    precheck()
    ids = [int(x) for x in sys.argv[1:]] or DATA_ID_ALL
    for k in ids:
        GENS[k]()
    print("ALL DONE:", ids)
