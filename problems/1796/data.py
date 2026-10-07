#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1796《斐波那契串》 分层测试数据生成器
# ---------------------------------------------------------------------------
# 用法（在 staging/1796/ 下）：
#   g++ -O2 -std=c++17 std.cpp -o work/std
#   python3 data.py
# 产出：data/problem1.in/.out ... data/problem10.in/.out
#
# 题面范围：N <= 1e9，M <= 10000，P <= 1e9，T 为长度 M 的 0/1 串。
# 铁律遵守：不使用 cyaron 的 output_gen（其写缓冲不 flush 易产 0 字节 .out），
#           改为 subprocess 显式跑 std 生成 .out，并断言 .out 非空且恰 1 行；
#           本文件不含任何 O(n^2) 的 Python 循环；无 brute/对拍/stress。
#
# 分层（10 组，从边界/小/中/大/顶格 铺开）：
#   1  样例层          N=7, M=3, P=100, T="101"          （题面原样例，期望 8）
#   2  边界最小        N=0, M=1, P=2                     （N 下界，单字符）
#   3  取模边界        N=1, M=1, P=1                     （P 下界，mod 1 => 0）
#   4  无出现边界      N=10, M=100, P=999983             （M > |S[10]|=89 => 0）
#   5  小规模          N=20, M=5, P=1000                 （30% 档 N<=20）
#   6  中规模          N=1000, M=50, P=1e9
#   7  中大规模        N=1e5, M=200, P=1e9               （60% 档边界 N<=1e5,M<=200）
#   8  大规模          N=1e9, M=1, P=1e9, T="1"          （N 顶格 + 单字符，退化为斐波那契计数）
#   9  大规模顶格      N=1e9, M=10000, P=1e9, T=斐波那契词前 10000 字符（保证出现>=1次）
#   10 顶格退化        N=1e9, M=10000, P=999999937, T="0"*10000（最大 M + 全零，极可能 0）
# ---------------------------------------------------------------------------
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "work", "std")


def fibword_prefix(n):
    """无限斐波那契词（S[0]="0",S[1]="1",S[i]=S[i-2]+S[i-1]）的前 n 个字符。"""
    a, b = "0", "1"
    while len(a) < n:
        a, b = b, a + b
    return a[:n]


def rand_bits(n, seed):
    import random
    return "".join(random.Random(seed).choices("01", k=n))


# (编号, 说明, N, M, P, T, 期望答案或 None)
FW = fibword_prefix(1200)  # 斐波那契词长前缀，供截取「必然出现」的因子
CASES = [
    (1, "样例层：题面原样例", 7, 3, 100, "101", 8),
    (2, "边界最小：N=0,M=1（N 下界 + 单字符）", 0, 1, 2, "0", None),
    (3, "取模边界：P=1（mod 1 恒为 0）", 1, 1, 1, "1", 0),
    (4, "无出现边界：M=100 > |S[10]|=89", 10, 100, 999983, rand_bits(100, 179604), 0),
    (5, "小规模：N=20,M=5（30% 档），T 为出现因子", 20, 5, 1000, FW[100:105], None),
    (6, "中规模：N=1000,M=50，T 为出现因子", 1000, 50, 1000000000, FW[300:350], None),
    (7, "中大规模：N=1e5,M=200（60% 档边界），T 为出现因子", 100000, 200, 1000000000, FW[1000:1200], None),
    (8, "大规模：N=1e9,M=1（N 顶格 + 单字符）", 1000000000, 1, 1000000000, "1", None),
    (9, "大规模顶格：N=1e9,M=10000, T=斐波那契词前缀（保证出现）",
     1000000000, 10000, 1000000000, fibword_prefix(10000), None),
    (10, "顶格退化：N=1e9,M=10000, T=全零", 1000000000, 10000, 999999937, "0" * 10000, None),
]

assert len(CASES) == 10

if not os.path.exists(STD):
    sys.exit("缺少 std 可执行文件：%s（先编译：g++ -O2 -std=c++17 std.cpp -o work/std）" % STD)

os.makedirs(DATA, exist_ok=True)

print("== 一本通 1796 分层数据生成 ==")
for idx, note, N, M, P, T, exp in CASES:
    assert 0 <= N <= 10 ** 9, "N 越界"
    assert 1 <= M <= 10000, "M 越界"
    assert 1 <= P <= 10 ** 9, "P 越界"
    assert len(T) == M, "T 长度与 M 不符"
    assert set(T) <= {"0", "1"}, "T 含非 0/1 字符"

    in_path = os.path.join(DATA, "problem%d.in" % idx)
    out_path = os.path.join(DATA, "problem%d.out" % idx)
    with open(in_path, "w", encoding="ascii") as fh:
        fh.write("%d %d %d\n" % (N, M, P))
        fh.write(T + "\n")
        fh.flush()
        os.fsync(fh.fileno())

    with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
        r = subprocess.run([STD], stdin=fin, stdout=fout, timeout=60)
    assert r.returncode == 0, "std 运行失败 problem%d (rc=%d)" % (idx, r.returncode)

    raw = open(out_path, "rb").read()
    assert len(raw) > 0, "problem%d.out 为空（0 字节）" % idx
    lines = [ln for ln in raw.decode().splitlines() if ln.strip() != ""]
    assert len(lines) == 1, "problem%d.out 行数异常：%r" % (idx, lines)
    ans = int(lines[0])
    assert 0 <= ans < P, "problem%d.out 答案 %d 不在 [0,P)" % (idx, ans)
    if exp is not None:
        assert ans == exp, "problem%d 期望 %d 实得 %d" % (idx, exp, ans)

    print("problem%-2d: N=%-10d M=%-5d P=%-10d T=%s%s  答=%-10d | %s"
          % (idx, N, M, P,
             (T if len(T) <= 16 else T[:16] + "..."),
             " " * 3, ans, note))

print("全部 10 组 .in/.out 生成完毕，均非空且各 1 行。")
