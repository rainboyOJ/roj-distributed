#!/usr/bin/env python3
# 一本通 1767《字符合并》数据生成器
# 用法：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（content.md 表格）：2<=k<=8，w_i 随规模从 <=1e5 到 <=1e9，
#   0<=c_i<=1, w_i>=1；n 上限 300（数据编号 0..19）。本题为经典题
#   [HAOI2016] 字符合并（洛谷 P3736 / BZOJ4565）同源。
#
# 分层设计（10 组，覆盖边界/小/中/大/顶格，且答案量级含 0、单次合并、长链、最大分数）：
#   点 1-2  边界层：n 下限、恰好一次合并、k 上限、权值顶格；
#   点 3-5  小规模：表点 0/1 规模、无解（n<k）档；
#   点 6-7  中等规模：表点 4/8 规模，k=3 长合并链；
#   点 8    大规模：表点 15（n=200,k=8）；
#   点 9-10 顶格层：n=300 顶格 + w 顶格，考察 long long（答案可达 ~7.4e10）。
#
# .out 生成方式：显式用 subprocess 跑 std 产出，随后断言 .out 非空、恰为一行整数，
#   并核对 .in 行数（1 行 "n k" + 1 行 a + 2^k 行表），避免 cyaron 写缓冲不 flush 导致 0 字节 .out。
import os
import re
import subprocess
import sys

from cyaron import IO, randint, random

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")

SUMMARY = []


def emit(data_id, n, k, a, table):
    """写 problem{id}.in，用 std 产出 problem{id}.out，并做完整性断言。"""
    assert len(a) == n, f"点{data_id}: a 长度 {len(a)} != n={n}"
    assert len(table) == (1 << k), f"点{data_id}: 表行数 {len(table)} != 2^k={1 << k}"

    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(n, k, "\n")
    io.input_write(*a, "\n")
    for c, w in table:
        io.input_write(c, w, "\n")
    io.flush_buffer()

    in_path = f"problem{data_id}.in"
    out_path = f"problem{data_id}.out"

    # 核对 .in 行数
    with open(in_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == 2 + (1 << k), f"点{data_id}: .in 行数 {len(lines)} != {2 + (1 << k)}"
    assert lines[0].split() == [str(n), str(k)], f"点{data_id}: 首行 {lines[0]!r}"
    assert len(lines[1].split()) == n, f"点{data_id}: 第二行数字个数错误"

    # 显式跑 std 产 .out（subprocess 直接重定向，规避写缓冲问题）
    with open(in_path) as fin, open(out_path, "w") as fout:
        proc = subprocess.run([STD], stdin=fin, stdout=fout, timeout=60)
    assert proc.returncode == 0, f"点{data_id}: std 退出码 {proc.returncode}"

    data = open(out_path).read()
    assert data.strip() != "", f"点{data_id}: .out 为空（0 字节）"
    assert len(data.splitlines()) == 1, f"点{data_id}: .out 行数 != 1"
    assert re.fullmatch(r"-?\d+", data.strip()), f"点{data_id}: .out 非整数 {data!r}"

    ans = int(data.strip())
    SUMMARY.append((data_id, n, k, len(a), max(a), min(a), max(w for _, w in table), ans))
    print(f"problem{data_id}: n={n} k={k} w_max={max(w for _, w in table)} ans={ans} OK")
    return ans


def rand_table(k, wmax, c_mode="random", w_mode="random"):
    table = []
    for i in range(1 << k):
        if c_mode == "all1":
            c = 1
        elif c_mode == "all0":
            c = 0
        else:
            c = randint(0, 1)
        if w_mode == "max":
            w = wmax
        else:
            w = randint(1, wmax)
        table.append((c, w))
    return table


def rand_str(n, mode="random"):
    if mode == "zeros":
        return [0] * n
    if mode == "ones":
        return [1] * n
    if mode == "alt":
        return [i & 1 for i in range(n)]
    return [randint(0, 1) for _ in range(n)]


# ---------------- 点 1：边界层 ----------------
# n=1（n 下限），k=2：无法进行任何合并，答案恒为 0。
def gen1():
    random.seed(176701)
    n, k = 1, 2
    a = rand_str(n)
    emit(1, n, k, a, rand_table(k, 10 ** 5))


# ---------------- 点 2：边界层 ----------------
# n=k=8：整串恰好只能合并一次，答案 = w[整串二进制值]；k 取上限 8，w 顶格 1e9。
def gen2():
    random.seed(176702)
    n, k = 8, 8
    a = rand_str(n)
    table = rand_table(k, 10 ** 9)
    val = 0
    for b in a:
        val = val * 2 + b
    ans = emit(2, n, k, a, table)
    assert ans == table[val][1], f"点2: 单次合并答案应为 {table[val][1]}，实得 {ans}"


# ---------------- 点 3：小规模 ----------------
# 表点 0 规模：n=10, k=2（k 最小，最多合并 9 次），w<=1e5。
def gen3():
    random.seed(176703)
    n, k = 10, 2
    a = rand_str(n)
    emit(3, n, k, a, rand_table(k, 10 ** 5))


# ---------------- 点 4：小规模 ----------------
# 表点 1 规模：n=15, k=3，c 全 1（合并只产生 1，形成长合并链），w<=1e5。
def gen4():
    random.seed(176704)
    n, k = 15, 3
    a = rand_str(n, "alt")
    emit(4, n, k, a, rand_table(k, 10 ** 5, c_mode="all1"))


# ---------------- 点 5：小规模（无解档） ----------------
# n=5 < k=8：无法合并任意 k 个相邻字符，答案恒为 0（k 上限 + 无解边界）。
def gen5():
    random.seed(176705)
    n, k = 5, 8
    a = rand_str(n)
    ans = emit(5, n, k, a, rand_table(k, 10 ** 6))
    assert ans == 0, f"点5: n<k 应无解答 0，实得 {ans}"


# ---------------- 点 6：中等规模 ----------------
# 表点 4 规模：n=50, k=5, w<=1e6。
def gen6():
    random.seed(176706)
    n, k = 50, 5
    a = rand_str(n)
    emit(6, n, k, a, rand_table(k, 10 ** 6))


# ---------------- 点 7：中等规模 ----------------
# 表点 8 规模：n=100, k=3（合并次数多，区间 DP 层数深），w<=1e7。
def gen7():
    random.seed(176707)
    n, k = 100, 3
    a = rand_str(n)
    emit(7, n, k, a, rand_table(k, 10 ** 7))


# ---------------- 点 8：大规模 ----------------
# 表点 15 规模：n=200, k=8（2^k=256 行表），w<=1e8。
def gen8():
    random.seed(176708)
    n, k = 200, 8
    a = rand_str(n)
    emit(8, n, k, a, rand_table(k, 10 ** 8))


# ---------------- 点 9：顶格层 ----------------
# 表点 16 规模：n=300 顶格, k=5, w 全取 1e9（分数最大，考 long long，答案约 7.4e10）。
def gen9():
    random.seed(176709)
    n, k = 300, 5
    a = rand_str(n)
    emit(9, n, k, a, rand_table(k, 10 ** 9, w_mode="max"))


# ---------------- 点 10：顶格层 ----------------
# 表点 19 规模：n=300, k=8 双顶格，w 全 1e9，c 随机；最大数据点（std 须限时可跑完）。
def gen10():
    random.seed(176710)
    n, k = 300, 8
    a = rand_str(n, "alt")
    emit(10, n, k, a, rand_table(k, 10 ** 9, w_mode="max"))


GENS = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]

if __name__ == "__main__":
    if not os.path.exists(STD):
        sys.exit("找不到 std，请先 g++ -O2 -std=c++17 std.cpp -o std")
    for g in GENS:
        g()
    print("ALL 10 PAIRS OK")
