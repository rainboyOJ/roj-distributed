#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1786《01背包》分层测试数据生成器
# ---------------------------------------------------------------------------
# 用法（在 .ybt-import/staging/1786/ 目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     nice -n 19 timeout 120 python3 data.py
# 生成 data/problem1.in/.out ... data/problem10.in/.out
#
# 题意：n 个物品（体积 s，价值 v），对容量 j = 1..m **各自独立**做一次 0/1 背包，
#       输出 m 个最大价值。
# 数据范围（题面明文）：1<=n<=1e6；1<=m<=1e5；1<=s<=300；1<=v<=1e9。
# 限制 time 7000 ms / memory 512 MB（config.json）。
#
# ---- 关于 cyaron ----
# 本仓库惯例用 cyaron.IO 写数据，但本题 n 可达 1e6 行、输出为 m 个空格分隔整数，
# 为规避任务书点名的 cyaron 隐患（output_gen 写缓冲不 flush 会产出 0 字节 .out，
# 且实测 input_write 多次调用会在续写处插入多余空格），本脚本：
#   * 用原生 open()+分块 join 写 .in（O(n) 且不做 Python 逐行 O(n^2) 循环）；
#   * 用 subprocess **显式** 跑 std 产出 .out（而不是 io.output_gen）；
#   * 生成后对每个 .out 断言：非空、恰好 1 行、恰好 m 个非负整数（本题目题面保证 m>=1，
#     不存在「无解空输出」的测试点），并对题面样例点逐字断言。
#
# ---- 分层策略（10 组，规模单调铺开：边界 → 小 → 中 → 大 → 顶格）----
#   点 1  边界最小层：n=1, m=1, s=1, v=1 —— 题面四个下界同时取到，答案 1。
#   点 2  样例层：题面输入样例 (n=4,m=9) —— .out 与题面输出样例**逐字比对**。
#   点 3  边界层（m 下界 + 体积越界物品）：m=1, n=6，含 s=300>m 的物品（任何方案都用不到）
#         与 s=1 的价值上界 v=1e9；答案 = 可容纳物品的最大价值 = 1e9。
#   点 4  边界层（s、v 上界）：m=300, n=4，含 s=300（体积顶格）与 v=1e9（价值顶格），
#         并含 s=299 以区分「恰好装满」与「差 1」。
#   点 5  小规模层：n=20, m=30, s∈[1,5], v∈[1,100] —— 可手算核对量级。
#   点 6  中规模层：n=2000, m=500, s∈[1,50], v∈[1,1e6]。
#   点 7  中规模层：n=50000, m=5000, s∈[1,300]（全体积范围）, v∈[1,1e9]。
#   点 8  大规模层：n=500000, m=50000, s∈[1,300], v∈[1,1e9]。
#   点 9  顶格层（通用）：n=1e6, m=1e5, s 均匀 [1,300], v 均匀 [1,1e9] —— 双维同时顶格，
#         300 个体积分组全部非空，是本题正解 Σ_s m log(m/s) 的通用最坏形态。
#   点 10 顶格层（极端结构）：n=1e6, m=1e5，体积只在 {1,300} 两端取值各半 ——
#         既压出「单个分组内可取到 1e5 个物品」的最长单调队列（s=1），
#         又压出「体积顶格 300、单组可用物品数最少 ⌊m/s⌋=333」的另一端。
#
#   固定随机种子，结果完全可复现。所有点的 (n,m,s,v) 均严格落在题面范围内。

import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

NMAX, MMAX, SMAX, VMAX = 10 ** 6, 10 ** 5, 300, 10 ** 9

# --------------------------------------------------------------------------
# 造点：返回 (n, m, s_array, v_array)
# --------------------------------------------------------------------------
def build():
    cases = []

    # ---- 点 1：边界最小 ----
    cases.append((1, 1, np.array([1], dtype=np.int64), np.array([1], dtype=np.int64)))

    # ---- 点 2：题面样例 ----
    cases.append((4, 9, np.array([2, 1, 3, 5], dtype=np.int64),
                  np.array([8, 1, 4, 100], dtype=np.int64)))

    # ---- 点 3：m=1 边界 + 体积越界物品 ----
    cases.append((6, 1, np.array([1, 1, 300, 2, 1, 300], dtype=np.int64),
                  np.array([1, 10 ** 9, 10 ** 9, 5, 3, 1], dtype=np.int64)))

    # ---- 点 4：s、v 上界 ----
    cases.append((4, 300, np.array([300, 1, 299, 300], dtype=np.int64),
                  np.array([10 ** 9, 1, 1, 10 ** 9], dtype=np.int64)))

    # ---- 点 5：小规模 ----
    rng = np.random.default_rng(1786005)
    n, m = 20, 30
    cases.append((n, m, rng.integers(1, 6, n), rng.integers(1, 101, n)))

    # ---- 点 6：中规模 ----
    rng = np.random.default_rng(1786006)
    n, m = 2000, 500
    cases.append((n, m, rng.integers(1, 51, n), rng.integers(1, 10 ** 6 + 1, n)))

    # ---- 点 7：中规模（全体积范围）----
    rng = np.random.default_rng(1786007)
    n, m = 50000, 5000
    cases.append((n, m, rng.integers(1, 301, n), rng.integers(1, 10 ** 9 + 1, n)))

    # ---- 点 8：大规模 ----
    rng = np.random.default_rng(1786008)
    n, m = 500000, 50000
    cases.append((n, m, rng.integers(1, 301, n), rng.integers(1, 10 ** 9 + 1, n)))

    # ---- 点 9：顶格（通用）----
    rng = np.random.default_rng(1786009)
    n, m = 10 ** 6, 10 ** 5
    cases.append((n, m, rng.integers(1, 301, n), rng.integers(1, 10 ** 9 + 1, n)))

    # ---- 点 10：顶格（体积取两端 {1,300}）----
    rng = np.random.default_rng(1786010)
    n, m = 10 ** 6, 10 ** 5
    s = np.empty(n, dtype=np.int64)
    s[0::2] = 1
    s[1::2] = 300
    cases.append((n, m, s, rng.integers(1, 10 ** 9 + 1, n)))

    return cases


def write_in(path, n, m, s, v):
    """分块写 .in：不做逐行 Python 循环，避免 O(n^2)。"""
    assert len(s) == n and len(v) == n
    sl = s.tolist()
    vl = v.tolist()
    chunk = 200000
    with open(path, "w") as f:
        f.write("%d %d\n" % (n, m))
        for i in range(0, n, chunk):
            f.write("\n".join("%d %d" % (a, b)
                              for a, b in zip(sl[i:i + chunk], vl[i:i + chunk])))
            f.write("\n")


def main():
    if not os.path.isfile(STD):
        sys.exit("std 未编译：先运行 g++ -O2 -std=c++17 std.cpp -o std")
    os.makedirs(DATA_DIR, exist_ok=True)

    cases = build()
    assert len(cases) == 10, "必须恰好 10 个测试点"

    # 生成前自检：所有值都在题面范围内
    for idx, (n, m, s, v) in enumerate(cases, 1):
        assert 1 <= n <= NMAX, "点%d n=%d 越界" % (idx, n)
        assert 1 <= m <= MMAX, "点%d m=%d 越界" % (idx, m)
        assert len(s) == n and len(v) == n, "点%d 物品数不符" % idx
        assert s.min() >= 1 and s.max() <= SMAX, "点%d s 越界 [%d,%d]" % (idx, s.min(), s.max())
        assert v.min() >= 1 and v.max() <= VMAX, "点%d v 越界 [%d,%d]" % (idx, v.min(), v.max())

    SAMPLE_OUT = "1 8 9 9 100 101 108 109 109"

    print("%-4s %-9s %-8s %-16s %-16s %-8s %s"
          % ("点", "n", "m", "s 范围", "v 范围", "std/s", ".out 校验"))
    for idx, (n, m, s, v) in enumerate(cases, 1):
        ipath = os.path.join(DATA_DIR, "problem%d.in" % idx)
        opath = os.path.join(DATA_DIR, "problem%d.out" % idx)

        write_in(ipath, n, m, s, v)

        # 用 subprocess 显式跑 std 产 .out（绕开 cyaron output_gen 的写缓冲隐患）
        import time
        t0 = time.time()
        with open(ipath, "rb") as fin, open(opath, "wb") as fout:
            subprocess.run(["nice", "-n", "19", STD], stdin=fin, stdout=fout,
                           stderr=subprocess.PIPE, timeout=120, check=True)
        dt = time.time() - t0

        # ---- 断言 1：.out 非空、恰好 1 行、恰好 m 个非负整数 ----
        raw = open(opath, "rb").read()
        assert raw, "点%d .out 为 0 字节！" % idx
        text = raw.decode()
        lines = [ln for ln in text.split("\n") if ln.strip() != ""]
        assert len(lines) == 1, "点%d .out 行数 %d != 1" % (idx, len(lines))
        toks = lines[0].split()
        assert len(toks) == m, "点%d .out 数字个数 %d != m=%d" % (idx, len(toks), m)
        for t in toks:
            assert t.isdigit(), "点%d .out 含非整数 token %r" % (idx, t)

        # ---- 断言 2：.in 结构 ----
        with open(ipath) as f:
            head = f.readline().split()
            assert head == [str(n), str(m)], "点%d .in 首行 %r 不符" % (idx, head)

        # ---- 断言 3：样例点逐字比对 ----
        note = ""
        if idx == 2:
            assert lines[0] == SAMPLE_OUT, "点2 与题面输出样例不一致：%r" % lines[0]
            note = "题面样例逐字一致"
        elif idx == 1:
            assert toks == ["1"], "点1 期望 [1]，实得 %r" % toks
            note = "全下界，答案 1"
        elif idx == 3:
            assert toks == ["1000000000"], "点3 期望 [1000000000]，实得 %r" % toks
            note = "m=1：仅 s=1 可用，取价值上界"
        elif idx == 4:
            assert toks[0] == "1" and toks[299] == "1000000000", \
                "点4 边界不符：dp[1]=%s dp[300]=%s" % (toks[0], toks[299])
            note = "s=300/v=1e9 顶格边界正确"

        print("%-4d %-9d %-8d %-16s %-16s %-8.2f %s"
              % (idx, n, m, "[%d,%d]" % (s.min(), s.max()),
                 "[%d,%d]" % (v.min(), v.max()), dt,
                 "非空/1行/%d 个整数 ok %s" % (len(toks), note)))

    print("\n全部 10 组数据生成并通过自检 -> %s" % DATA_DIR)


if __name__ == "__main__":
    main()
