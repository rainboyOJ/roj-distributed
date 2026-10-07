#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一本通 1812《网格》数据生成器（10 个测试点，分层：边界/小/中/大/顶格/退化）

题面范围：T <= 20；N <= 50，W, H, D <= 500（每组四个整数 N W H D）；
          答案对 1,000,000,000 取模。

生成方式：
  * .in 用 cyaron 的 IO 写（with 语句退出时 close 会 flush，并在脚本里断言文件非空）；
  * .out **不用** cyaron 的 output_gen（其写缓冲不 flush 会产出 0 字节 .out），
    而是用 subprocess 显式跑 std，把 stdout 落到 .out，再断言
    「.out 非空」+「.out 行数 == T」+「.in 行数 == T+1」。
  * 生成器全部是 O(T) 级别的直接构造/random.randint，无任何 O(n^2) 循环。

分层意图（从最小铺到顶格，10 个点）：
  点1  边界层：N=1 单点、W=H=0 退化网格、W=0/H=0 单行单列 —— 全部可手算
  点2  小规模随机：N,W,H,D <= 10（对应 20% 档 N,W,H,D<=10）
  点3  中等规模随机：W,H,D <= 100（对应 50% 档）
  点4  N 小规模随机：N <= 5，W,H,D <= 500（对应「另 20% 数据 N<=5」档）
  点5  样例复现层：题面 6 组样例原样，逐行断言题面期望输出
  点6  大规模随机：N<=50，W,H,D<=500 全域随机
  点7  顶格层（N=2）：W=H=500，D=1/2 —— 答案最大、取模必回绕（N=2 时 D=1 答案为
       C(251001,2)=31500625500 -> mod 1e9 = 500625500，可手算校验）
  点8  顶格层（N=50）：W=H=500，D=1/2 —— N 顶格 + 网格顶格 + 组合数上标最大
  点9  大 D 稀疏层：W=H=500，D=500 —— 相邻点距离必须 >=500，答案极小或为 0
  点10 退化/混合边界层：单列/单行/1x1 网格 + N 顶格（答案 0）+ N=1 顶格网格
"""
import os
import random
import subprocess
import sys
from math import comb

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD_SRC = os.path.join(HERE, "std.cpp")
STD_BIN = os.path.join(HERE, "std")
MOD = 10 ** 9


def ensure_std():
    """编译 std.cpp（若二进制不存在或比源码旧），返回二进制路径。"""
    need = True
    if os.path.exists(STD_BIN):
        need = os.path.getmtime(STD_BIN) < os.path.getmtime(STD_SRC)
    if need:
        subprocess.run(
            ["g++", "-O2", "-std=c++17", "-o", STD_BIN, STD_SRC],
            check=True, timeout=120,
        )
    return STD_BIN


def write_case(i, cases, note=""):
    """第 i 组：写 data/problem{i}.in，跑 std 产 data/problem{i}.out，并做完整性断言。"""
    assert 1 <= len(cases) <= 20, "T 必须落在 [1,20]"
    for (n, w, h, d) in cases:
        assert 1 <= n <= 50 and 0 <= w <= 500 and 0 <= h <= 500 and 1 <= d <= 500

    inp = os.path.join(DATA_DIR, "problem%d.in" % i)
    outp = os.path.join(DATA_DIR, "problem%d.out" % i)

    # --- 写 .in（cyaron IO，with 退出即 close/flush）---
    with IO(input_file=inp, disable_output=True) as io:
        io.input_writeln(len(cases))
        for (n, w, h, d) in cases:
            io.input_writeln(n, w, h, d)

    # --- 完整性断言（.in）---
    assert os.path.exists(inp) and os.path.getsize(inp) > 0, "点%d .in 为空/不存在" % i
    in_lines = open(inp, "r").read().split("\n")
    in_lines = [ln for ln in in_lines if ln.strip() != ""]
    assert len(in_lines) == len(cases) + 1, \
        "点%d .in 行数 %d != T+1=%d" % (i, len(in_lines), len(cases) + 1)
    assert int(in_lines[0].split()[0]) == len(cases), "点%d .in 首行 T 不符" % i

    # --- 用 subprocess 显式跑 std 产 .out（不用 output_gen，规避缓冲不 flush）---
    with open(inp, "rb") as fin, open(outp, "wb") as fout:
        r = subprocess.run([STD_BIN], stdin=fin, stdout=fout, timeout=120)
    assert r.returncode == 0, "点%d std 退出码 %d" % (i, r.returncode)

    # --- 完整性断言（.out）---
    assert os.path.exists(outp) and os.path.getsize(outp) > 0, "点%d .out 为 0 字节/不存在" % i
    out_tokens = open(outp, "r").read().split()
    assert len(out_tokens) == len(cases), \
        "点%d .out 行数 %d != T=%d" % (i, len(out_tokens), len(cases))
    for tok in out_tokens:
        assert tok.isdigit() and 0 <= int(tok) < MOD, "点%d 输出 %s 不是 [0,1e9) 内整数" % (i, tok)
    print("  点%-2d T=%-3d %s  -> 前几个答案: %s" %
          (i, len(cases), note, " ".join(out_tokens[:4])))
    return [int(t) for t in out_tokens]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    ensure_std()
    rnd = random.Random(1812025)

    # ---------- 点1：边界最小层（全部可手算） ----------
    # N=1 在 1x1 退化网格（W=H=0）: 1 个格点 -> 1 种；
    # N=1 在 501x501 顶格网格: 251001 种；
    # N=2 在 2x1（W=1,H=0）与 1x2（W=0,H=1）单行/单列: 各 1 种（距离 1 >= 1）。
    p1 = [(1, 0, 0, 1), (1, 500, 500, 500), (2, 1, 0, 1), (2, 0, 1, 1)]
    got1 = write_case(1, p1, "边界最小层(手算)")
    assert got1 == [1, 251001, 1, 1], "点1 手算期望 [1,251001,1,1]，实得 %s" % got1

    # ---------- 点2：小规模随机（N,W,H,D<=10，对应 20% 档） ----------
    # 取 N<=10 且网格 >=4，D<=3，使正解非 0 与 0 解混合出现。
    p2 = []
    for _ in range(20):
        p2.append((rnd.randint(1, 10), rnd.randint(4, 10),
                   rnd.randint(4, 10), rnd.randint(1, 3)))
    write_case(2, p2, "小规模随机 N,W,H,D<=10")

    # ---------- 点3：中等规模随机（W,H,D<=100，对应 50% 档） ----------
    p3 = []
    for _ in range(20):
        p3.append((rnd.randint(1, 20), rnd.randint(20, 100),
                   rnd.randint(20, 100), rnd.randint(1, 5)))
    write_case(3, p3, "中等随机 W,H,D<=100")

    # ---------- 点4：N<=5 随机（对应「另 20% 数据 N<=5」，W,H,D 顶格） ----------
    p4 = []
    for _ in range(20):
        p4.append((rnd.randint(1, 5), rnd.randint(1, 500),
                   rnd.randint(1, 500), rnd.randint(1, 500)))
    write_case(4, p4, "N<=5 随机 W,H,D<=500")

    # ---------- 点5：题面样例原样复现（T=6），逐行断言期望输出 ----------
    p5 = [(2, 4, 4, 1), (13, 36, 48, 5), (5, 5, 5, 1),
          (50, 49, 49, 1), (6, 5, 5, 2), (10, 55, 75, 5)]
    exp5 = [300, 2, 88, 102, 0, 490260662]
    got5 = write_case(5, p5, "题面样例复现")
    assert got5 == exp5, "点5 样例期望 %s，实得 %s" % (exp5, got5)

    # ---------- 点6：大规模随机（N<=50，W,H,D<=500 全域） ----------
    p6 = []
    for _ in range(20):
        p6.append((rnd.randint(1, 50), rnd.randint(100, 500),
                   rnd.randint(100, 500), rnd.randint(1, 10)))
    write_case(6, p6, "大规模全域随机")

    # ---------- 点7：顶格层 N=2（答案最大 + 取模回绕） ----------
    # N=2 且 D=1 时任意两不同格点都合法，答案 = C(501*501, 2) = 31500625500
    #   -> mod 1e9 = 500625500（手算校验）；D=2 时排除相邻近点，答案不同。
    p7 = [(2, 500, 500, 1)] * 10 + [(2, 500, 500, 2)] * 10
    got7 = write_case(7, p7, "顶格 N=2 W=H=500 D=1/2")
    exp7a = (501 * 501) * (501 * 501 - 1) // 2 % MOD
    assert exp7a == 500625500, "手算 C(251001,2) mod 1e9 应为 500625500，实得 %d" % exp7a
    assert got7[0] == exp7a, "点7 D=1 期望 %d，实得 %d" % (exp7a, got7[0])
    assert got7[10] < got7[0] and got7[10] > 0, "点7 D=2 应比 D=1 小且为正"

    # ---------- 点8：顶格层 N=50（N 顶格 + 网格顶格） ----------
    p8 = [(50, 500, 500, 1)] * 10 + [(50, 500, 500, 2)] * 10
    got8 = write_case(8, p8, "顶格 N=50 W=H=500 D=1/2")
    assert all(v > 0 for v in got8), "点8 顶格 N=50/D=1,2 答案应均非 0"

    # ---------- 点9：大 D 稀疏层（D=500 顶格，多数为 0） ----------
    p9 = [(2, 500, 500, 500), (3, 500, 500, 500), (4, 500, 500, 500),
          (5, 500, 500, 500), (6, 500, 500, 500), (7, 500, 500, 500),
          (10, 500, 500, 500), (50, 500, 500, 500),
          (50, 499, 499, 500), (50, 1, 500, 500),
          (2, 500, 499, 500), (2, 499, 500, 500), (3, 500, 499, 500),
          (5, 250, 250, 500), (10, 500, 500, 499), (20, 500, 500, 500),
          (2, 1, 500, 500), (3, 500, 500, 499), (4, 499, 499, 500),
          (2, 500, 500, 499)]
    got9 = write_case(9, p9, "大 D=500 稀疏/无解层")
    assert got9[7] == 0 and got9[8] == 0 and got9[9] == 0 and got9[15] == 0, \
        "点9 大 N + D=500 应为 0，实得 %s" % got9
    assert got9[0] > 0, "点9 N=2,D=500 应为正（对角线方向可取）"

    # ---------- 点10：退化网格/混合边界层（全部可手算） ----------
    # 单列(W=0)/单行(H=0)/1x1 网格；退化网格只有唯一一条直线，答案 = C(点数, N)；
    # N 超过网格点数 -> 0；N=1 -> 格点数。
    p10 = [(1, 0, 0, 1),         # N=1, 1x1 网格: 1
           (1, 0, 0, 500),       # N=1: 1
           (1, 500, 500, 1),     # N=1: 251001
           (50, 0, 500, 1),      # 单列 501 点任取 50: C(501,50)
           (50, 500, 0, 1),      # 单行 501 点任取 50: C(501,50)
           (50, 1, 1, 1),        # 4 点 < 50: 0
           (50, 0, 49, 1),       # 单列恰 50 点全取: 1
           (50, 49, 0, 1),       # 单行恰 50 点全取: 1
           (2, 0, 0, 1),         # 1 点 < 2: 0
           (3, 0, 2, 1),         # 单列 3 点全取: 1
           (2, 1, 1, 1),         # 2x2 网格任取 2 点: C(4,2)=6
           (2, 1, 1, 2),         # 2x2 最大距离 sqrt(2)<2: 0
           (2, 0, 500, 1),       # 单列 501 点任取 2: C(501,2)
           (1, 0, 500, 500),     # N=1: 501
           (1, 500, 0, 500),     # N=1: 501
           (2, 500, 0, 1),       # 单行 501 点任取 2: C(501,2)
           (3, 0, 499, 1),       # 单列 500 点任取 3: C(500,3)
           (4, 3, 0, 1),         # 单行恰 4 点全取: 1
           (3, 1, 0, 1),         # 2 点 < 3: 0
           (50, 0, 500, 500)]    # 单列需跨度 49*500=24500 > 500: 0
    got10 = write_case(10, p10, "退化网格/混合边界层")
    c501_50 = comb(501, 50) % MOD
    exp10 = [1, 1, 251001, c501_50, c501_50, 0, 1, 1, 0, 1,
             6, 0, comb(501, 2), 501, 501, comb(501, 2),
             comb(500, 3), 1, 0, 0]
    for k, v in enumerate(exp10):
        assert got10[k] == v, "点10 第%d组 (%s) 期望 %d，实得 %d" % (
            k + 1, p10[k], v, got10[k])

    # ---------- 总检查 ----------
    names = sorted(os.listdir(DATA_DIR))
    for i in range(1, 11):
        for suf in (".in", ".out"):
            f = os.path.join(DATA_DIR, "problem%d%s" % (i, suf))
            assert os.path.exists(f) and os.path.getsize(f) > 0, "缺文件或空文件: " + f
    assert len(names) == 20, "data/ 下应恰有 20 个文件，实得 %d: %s" % (len(names), names)
    print("OK: data/problem1..10.in/.out 全部生成且通过完整性断言")


if __name__ == "__main__":
    sys.exit(main())
