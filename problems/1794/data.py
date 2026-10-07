#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1794《分数》 分层测试数据生成器
#
# 用法：
#   g++ -O2 -std=c++17 -o std std.cpp
#   python3 data.py            # 结果写入 ./data/problem{1..10}.{in,out}
#   （std 路径可用环境变量 STD 覆盖；默认 ./std，回退 ./work/std）
#
# 题面数据范围（http://ybt.ssoier.cn:8088/problem_show.php?pid=1794 逐字核对）：
#   20%  : N<=100, M=100
#   20%  : N<=1000, M<=3e5
#   30%  : N<=3e5, M=10
#   100% : N,M<=3e5, 1<=T_i,X_i<=1e9, sum(T_i)<=1e12
#
# ---- 分层策略（10 个测试点，文件名 problem1..problem10）----
#   点 1  边界层：N=1,M=1，T=[1]，唯一询问 (1,1)          —— 全下界。
#   点 2  边界层：N=1,M=3，T=[1e9]，X∈{1,1e9,2}            —— 值上界 + X 两端。
#   点 3  边界层：N=2,M=6，T=[1,1]，穷尽 P∈{1,2}×X∈{1,2,3} —— 最小非平凡，可手算。
#   点 4  小规模：N=10,M=10，T∈[1,4]，X∈[1,10]               —— 可手算核对（答案非平凡）。
#   点 5  20% 子任务顶格：N=100,M=100，T∈[1,3]，X∈[1,8]。
#   点 6  20% 子任务顶格：N=1000,M=3e5，T_i 全 =1e9（sum=1e12 恰为上限），X∈[1,1e9]。
#        此档 T 远大于任何段的收益，最优恒为"不标记"（答案 0），专门压大数值/负值边界。
#   点 7  30% 子任务顶格：N=3e5,M=10，T∈[1,3]，X∈[1,1e9]（含两端）。
#   点 8  100% 顶格随机：N=3e5,M=3e5，T∈[1,2]，X 一半 [1,5]、一半 [1,1e9]。
#   点 9  100% 顶格特殊结构：N=3e5,M=3e5，T 全 1（最优=整段全标记，答案最大），X∈[1,3]。
#   点 10 100% 顶格混合：N=3e5,M=3e5，T 全 3 但随机 50 个位置置 1e9 尖峰（把数组切成
#        约 50 段），X 一半取 1e9（逼出"不覆盖 P"分支）、一半取小值；并含重复 P 与端点 P。
#
#   为什么大 T 档要单独说明：sum(T)<=1e12 且 N<=3e5 ⇒ 平均 T<=3.3e6，而长度 c 的段收益
#   上界为 C(c)-c*avgT，要为正需 c>~2*avgT，故大 T 时"标记任何数"恒亏、答案恒 0。
#   真正有区分度的顶格档必须用小 T（点 7-10），大 T 档（点 6）只覆盖数值/退化边界。
#
# 说明：不使用 cyaron 的 output_gen（避免写缓冲不 flush 产生 0 字节 .out 的隐患），
#       改为 subprocess 显式跑 std 产出 .out，并断言 .out 非空且行数 == M。

import os
import random
import shutil
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

MAXV = 10 ** 9
BIG_N = 300000
BIG_M = 300000


def find_std():
    env = os.environ.get("STD")
    cands = [env] if env else []
    cands += [os.path.join(BASE, "std"), os.path.join(BASE, "work", "std")]
    for c in cands:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    raise SystemExit("找不到 std 可执行文件，请先编译：g++ -O2 -std=c++17 -o std std.cpp")


def rnd_seq(rnd, n, lo, hi):
    """O(n) 生成 n 个 [lo,hi] 的随机整数（列表推导，无嵌套循环）。"""
    return [rnd.randint(lo, hi) for _ in range(n)]


def build_case(i):
    """返回 (N, T, queries[list of (P,X)])。"""
    if i == 1:
        return 1, [1], [(1, 1)]
    if i == 2:
        return 1, [MAXV], [(1, 1), (1, MAXV), (1, 2)]
    if i == 3:
        return 2, [1, 1], [(p, x) for p in (1, 2) for x in (1, 2, 3)]
    if i == 4:
        rnd = random.Random(179404)
        N, M = 10, 10
        T = rnd_seq(rnd, N, 1, 4)
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, 10)
        return N, T, list(zip(P, X))
    if i == 5:
        rnd = random.Random(179405)
        N, M = 100, 100
        T = rnd_seq(rnd, N, 1, 3)
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, 8)
        return N, T, list(zip(P, X))
    if i == 6:
        rnd = random.Random(179406)
        N, M = 1000, BIG_M
        T = [MAXV] * N                       # sum(T) = 1e12 恰为上限
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, MAXV)
        X[0] = 1
        X[1] = MAXV
        return N, T, list(zip(P, X))
    if i == 7:
        rnd = random.Random(179407)
        N, M = BIG_N, 10
        T = rnd_seq(rnd, N, 1, 3)
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, MAXV)
        P[0], P[1] = 1, N
        X[0], X[1] = 1, MAXV
        return N, T, list(zip(P, X))
    if i == 8:
        rnd = random.Random(179408)
        N, M = BIG_N, BIG_M
        T = rnd_seq(rnd, N, 1, 2)
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, MAXV)
        for k in range(0, M, 2):             # 一半查询用小 X（最优会标记长段）
            X[k] = rnd.randint(1, 5)
        P[0], P[1], P[2] = 1, N, N // 2
        X[0], X[1], X[2] = 1, MAXV, 1
        return N, T, list(zip(P, X))
    if i == 9:
        rnd = random.Random(179409)
        N, M = BIG_N, BIG_M
        T = [1] * N                          # 全标记最优，答案最大
        P = rnd_seq(rnd, M, 1, N)
        X = rnd_seq(rnd, M, 1, 3)
        P[0], X[0] = 1, 1
        P[1], X[1] = N, MAXV
        return N, T, list(zip(P, X))
    # i == 10
    rnd = random.Random(179410)
    N, M = BIG_N, BIG_M
    T = [3] * N
    spikes = rnd.sample(range(N), 50)          # 50 个 1e9 尖峰，把数组切成约 50 段
    for p in spikes:
        T[p] = MAXV
    P = rnd_seq(rnd, M, 1, N)
    X = rnd_seq(rnd, M, 1, MAXV)
    # 一半查询逼出"不覆盖 P"分支（X 巨大），一半小值
    for k in range(0, M, 2):
        X[k] = rnd.randint(1, 4)
    P[0], X[0] = 1, MAXV
    P[1], X[1] = N, 1
    P[2], X[2] = N // 2, N // 2       # 重复 P
    P[3], X[3] = spikes[0] + 1, MAXV  # 尖峰旁（段边界）
    P[4], X[4] = spikes[1] + 1, 1
    return N, T, list(zip(P, X))


def write_input(path, N, T, queries):
    parts = [str(N), " ".join(map(str, T)), str(len(queries))]
    parts.extend("%d %d" % (p, x) for p, x in queries)
    with open(path, "w") as f:
        f.write("\n".join(parts))
        f.write("\n")


def run_std(std, in_path, out_path):
    cmd = []
    if shutil.which("nice"):
        cmd += ["nice", "-n", "19"]
    cmd += [std]
    t0 = time.time()
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        r = subprocess.run(cmd, stdin=fi, stdout=fo, stderr=subprocess.PIPE, timeout=120)
    dt = time.time() - t0
    if r.returncode != 0:
        raise SystemExit("std 运行失败 rc=%d err=%s" % (r.returncode, r.stderr[:500]))
    return dt


def main():
    std = find_std()
    os.makedirs(DATA, exist_ok=True)
    total = 0.0
    for i in range(1, 11):
        N, T, queries = build_case(i)
        M = len(queries)
        assert 1 <= N <= BIG_N, (i, N)
        assert 1 <= M <= BIG_M, (i, M)
        assert all(1 <= t <= MAXV for t in T), i
        assert all(1 <= p <= N for p, _ in queries), i
        assert all(1 <= x <= MAXV for _, x in queries), i
        assert sum(T) <= 10 ** 12, (i, sum(T))
        in_path = os.path.join(DATA, "problem%d.in" % i)
        out_path = os.path.join(DATA, "problem%d.out" % i)
        write_input(in_path, N, T, queries)
        dt = run_std(std, in_path, out_path)
        total += dt
        # ---- 断言 .out 合法：非空且行数 == M ----
        size = os.path.getsize(out_path)
        assert size > 0, "problem%d.out 为空！" % i
        with open(out_path) as f:
            lines = f.read().split("\n")
        while lines and lines[-1] == "":
            lines.pop()
        assert len(lines) == M, "problem%d.out 行数 %d != M=%d" % (i, len(lines), M)
        for ln in lines:
            int(ln)  # 必须都是整数
        print("problem%-2d  N=%-7d M=%-7d sumT=%-13d  std=%.3fs  out_lines=%d  OK"
              % (i, N, M, sum(T), dt, len(lines)))
    print("全部 10 组生成完成，std 累计耗时 %.3fs" % total)


if __name__ == "__main__":
    main()
