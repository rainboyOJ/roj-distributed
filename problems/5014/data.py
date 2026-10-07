#!/usr/bin/env python
# 一本通 1678《独木桥》测试数据生成器（cyaron 惯例）
#
# 题面数据范围：1 <= n,q <= 2*10^5，0 <= k_i < n，0 <= p_i,t_i <= 1e9，d_i in {0,1}
# 输出：problem1.in/.out ~ problem10.in/.out（10 个测试点，分层覆盖）
#
# 分层设计（详见 gen-report.md）：
#   点 1    边界层：n=1（最小 n），p=0（最小 p），t=0/1e9-1/1e9（最小与最大 t）
#   点 2    边界层：n=2 相邻对撞（距离 1，相遇临界）+ t=0 + 顶格 t
#   点 3-4  小规模随机：n,q<=10，p,t<=10（20% 档，可手算）；点 4 全同向（d_i 均相同档）
#   点 5-6  中等规模随机：n=1000（n<=1000 档）；点 5 另含 t<=100 档
#   点 7-8  大规模随机：n=q=2*10^5，p,t 全域；点 8 位置挤在 ~1e6 宽窄段
#   点 9-10 顶格层：n=q=2*10^5 顶格 + 最坏结构
#           点 9：连续位置 0..n-1 + 交错朝向 0101..（相遇次数最多的结构）
#           点 10：顶格 p（挤在 [1e9-n, 1e9]）+ 前半全右后半全左（中央大量对撞）
#                  + t 一半取 1e9 顶格（检验 long long），一半取 [0,2n] 密集相遇时刻

import random
from cyaron import *

N_MAX = 200000
Q_MAX = 200000
P_MAX = 10 ** 9
T_MAX = 10 ** 9


def make_io(idx, n, ps, ds, qs):
    """按题面格式写入一个测试点并调用 ../std 生成 .out"""
    io = IO(file_prefix="problem", data_id=idx)
    io.input_writeln(n)
    io.input_writeln(ps)
    io.input_writeln(ds)
    io.input_writeln(len(qs))
    for k, t in qs:
        io.input_writeln(k, t)
    io.output_gen("../std")
    return io


def rand_positions(rng, n, pmax):
    return rng.sample(range(0, pmax + 1), n)   # 互异整数


def rand_dirs(rng, n):
    return [rng.randint(0, 1) for _ in range(n)]


def rand_queries(rng, n, q, tmax):
    return [(rng.randrange(n), rng.randint(0, tmax)) for _ in range(q)]


def main():
    # ---------- 点 1：边界层（n=1 / p=0 / t=0 与 t=1e9） ----------
    # 最小 n；最小 p；t 取 0、1、1e9-1、1e9（含顶格），向右朝向。
    make_io(1, 1, [0], [1], [(0, 0), (0, 1), (0, 10**9), (0, 10**9 - 1)])

    # ---------- 点 2：边界层（n=2 相邻对撞 / t=0 / 顶格 t） ----------
    # 位置 {0,1}（最近距离），朝向相向：t=1 时恰在相遇折返的临界附近；
    # t=0 验证零时刻；t=1e9 与 1e9-1 顶格（此时答案出现 -999999999 等负坐标，
    # 检验负数输出与 long long）。
    qs = []
    for t in (0, 1, 2, 3, 5, 10**9, 10**9 - 1):
        qs.append((0, t))
        qs.append((1, t))
    make_io(2, 2, [0, 1], [1, 0], qs)

    # ---------- 点 3：小规模随机（20% 档 n,p,t<=10，可手算） ----------
    rng = random.Random(16780003)
    n = rng.randint(1, 10)
    ps = rand_positions(rng, n, 10)
    ds = rand_dirs(rng, n)
    qs = rand_queries(rng, n, rng.randint(1, 10), 10)
    make_io(3, n, ps, ds, qs)

    # ---------- 点 4：小规模随机 + 全同向档（d_i 均相同）+ q<=10 档 ----------
    rng = random.Random(16780004)
    n = rng.randint(2, 10)
    ps = rand_positions(rng, n, 10)
    ds = [1] * n                       # 全向右：永不相遇
    qs = rand_queries(rng, n, rng.randint(1, 10), 10)
    make_io(4, n, ps, ds, qs)

    # ---------- 点 5：中等规模随机（n<=1000 档）+ t<=100 档 ----------
    rng = random.Random(16780005)
    n = 1000
    ps = rand_positions(rng, n, 10 ** 6)
    ds = rand_dirs(rng, n)
    qs = rand_queries(rng, n, 1000, 100)     # 另 15% 档：t<=100
    make_io(5, n, ps, ds, qs)

    # ---------- 点 6：中等规模随机（n=1000，全域 p,t） ----------
    rng = random.Random(16780006)
    n = 1000
    ps = rand_positions(rng, n, P_MAX)
    ds = rand_dirs(rng, n)
    qs = rand_queries(rng, n, 1000, T_MAX)
    make_io(6, n, ps, ds, qs)

    # ---------- 点 7：大规模随机（n,q=2*10^5，全域 p,t） ----------
    rng = random.Random(16780007)
    n = N_MAX
    ps = rand_positions(rng, n, P_MAX)
    ds = rand_dirs(rng, n)
    qs = rand_queries(rng, n, Q_MAX, T_MAX)
    make_io(7, n, ps, ds, qs)

    # ---------- 点 8：大规模随机（位置挤在 ~1e6 宽窄段，密度高） ----------
    rng = random.Random(16780008)
    n = N_MAX
    ps = rng.sample(range(P_MAX - 5 * n, P_MAX + 1), n)   # 互异、挤在窄段且贴顶格
    ds = rand_dirs(rng, n)
    qs = rand_queries(rng, n, Q_MAX, T_MAX)
    make_io(8, n, ps, ds, qs)

    # ---------- 点 9：顶格 + 最坏结构（连续位置 + 交错朝向） ----------
    # p = 0,1,...,n-1（最密），朝向 0101... 交错 => 相邻相向对几乎立即相遇，
    # 是相遇/折返最多的最坏结构；n,q 均取题面上限，t 全域随机。
    rng = random.Random(16780009)
    n = N_MAX
    ps = list(range(n))
    ds = [i & 1 for i in range(n)]
    qs = rand_queries(rng, n, Q_MAX, T_MAX)
    make_io(9, n, ps, ds, qs)

    # ---------- 点 10：顶格 + 最坏结构（窄区间顶格 p + 对撞带 + 顶格 t） ----------
    # 位置挤在 [P_MAX-n, P_MAX]（p 顶格），前一半全向右、后一半全向左：
    # 中央形成大量相向相遇；t 一半取 1e9 顶格（检验 long long 与极端位移），
    # 一半取 [0, 2n] 内的局部时刻（相遇最密集时段）。
    rng = random.Random(16780010)
    n = N_MAX
    ps = list(range(P_MAX - n + 1, P_MAX + 1))
    ds = [1] * (n // 2) + [0] * (n - n // 2)
    qs = []
    for i in range(Q_MAX):
        if i % 2 == 0:
            t = T_MAX
        else:
            t = rng.randint(0, 2 * n)
        qs.append((rng.randrange(n), t))
    make_io(10, n, ps, ds, qs)


if __name__ == "__main__":
    main()
