#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 1992《书架book》数据生成器（洛谷 P2596 / BZOJ1861 [ZJOI2006]书架 同源）
#
# 题意：n 本书从上到下堆成一列（初始编号排列 p_i），m 条命令：
#   Top S / Bottom S / Insert S T / Ask S / Query S
# 输出：每条 Ask / Query 一行一个整数。
#
# 数据范围（题面·洛谷 P2596 官方）：
#     3 <= n, m <= 8e4；p_i 为 1~n 的排列；1 <= S <= n；T ∈ {-1,0,1}；
#     保证顶部书不会被 Insert S -1、底部书不会被 Insert S 1。
#
# 分层设计（10 个测试点，单组数据，按 n、m 量级与操作结构分层）：
#   点 1-2   边界层：n=m=3（题面下界）；n=3 且命令覆盖全 5 种（最小完备操作集）
#   点 3-4   小规模随机：n,m ∈ [4,60]，可手算/暴力验证量级
#   点 5-6   中等规模随机：n,m ∈ [2000,20000]，范围中间档
#   点 7-8   大规模随机：n,m ∈ [50000,79999]，接近上限
#   点 9-10  顶格层：n=m=8e4 顶格 + 最坏结构（点 10 全部 Insert 操作，
#            交替 -1/+1 卡 splay/交换路径；点 9 均匀混合 5 种操作）
from cyaron import *  # 引入CYaRon的库
import random

random.seed(1992)

MAXN = 80000  # 题面 n, m 上限


def gen_ops(rng, n, m, mode):
    """按 mode 生成 m 条合法命令，返回 (初始书架, 命令列表)。
    模拟书架以保证 Insert 的合法性（顶部不 -1、底部不 +1）。"""
    shelf = list(range(1, n + 1))
    rng.shuffle(shelf)
    initial = shelf[:]                    # 初始排列（写入输入第二行）
    pos = {v: i for i, v in enumerate(shelf)}  # 0-based

    def sync(a, b):  # 交换位置 a、b 上的书后同步 pos
        shelf[a], shelf[b] = shelf[b], shelf[a]
        pos[shelf[a]] = a
        pos[shelf[b]] = b

    def move(v, to_front):
        i = pos[v]
        shelf.pop(i)
        if to_front:
            shelf.insert(0, v)
        else:
            shelf.append(v)
        for j in range(n):
            pos[shelf[j]] = j

    ops = []
    kinds = ["Top", "Bottom", "Insert", "Ask", "Query"]
    for step in range(m):
        if mode == "all5":      # 均匀混合 5 种
            k = kinds[rng.randint(0, 4)]
        elif mode == "insert":  # 全部 Insert（交替 ±1）为主，每 50 步插入一次查询
            k = "Ask" if step % 50 == 25 else ("Query" if step % 50 == 49 else "Insert")
        elif mode == "query":   # 以查询为主
            k = "Ask" if rng.random() < 0.5 else "Query"
        else:                   # 默认混合，Insert 偏多
            r = rng.random()
            k = "Insert" if r < 0.5 else kinds[rng.randint(0, 4)]
        s = rng.randint(1, n)
        if k == "Top":
            ops.append("Top %d" % s)
            move(s, True)
        elif k == "Bottom":
            ops.append("Bottom %d" % s)
            move(s, False)
        elif k == "Insert":
            cands = [0]
            x = pos[s]
            if x > 0:
                cands.append(-1)
            if x < n - 1:
                cands.append(1)
            if mode == "insert":
                t = rng.choice([c for c in cands if c != 0] or [0])
            else:
                t = rng.choice(cands)
            ops.append("Insert %d %d" % (s, t))
            x = pos[s]
            if t != 0:
                sync(x, x + t)
        elif k == "Ask":
            ops.append("Ask %d" % s)
        else:
            ops.append("Query %d" % s)
    return initial, ops


def write_case(i, n, m, mode, note):
    rng = random.Random(19920000 + i)  # 每点独立种子，可复现
    shelf, ops = gen_ops(rng, n, m, mode)
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(n, m)
    io.input_writeln(" ".join(map(str, shelf)))
    io.input_write("\n".join(ops) + "\n")
    io.output_gen("../std")
    print("problem%d: n=%d m=%d mode=%s -- %s" % (i, n, m, mode, note))


# ---- 点 1-2：边界层 ----
# 点 1：题面下界 n=m=3；含 Ask/Query（含答案 0/1 极端）与全 5 种操作中的 4 种
write_case(1, 3, 3, "all5", "边界层：n=m=3（题面下界），操作均匀含查询")

# 点 2：n=3，m=12，5 种操作全覆盖 + 顶/底 Insert 边界（顶部不 -1、底部不 +1）
write_case(2, 3, 12, "all5", "边界层：n=3 全 5 种操作，含 Insert 边界合法性与答案 0 极端")

# ---- 点 3-4：小规模随机 ----
write_case(3, 12, 25, "mix", "小规模随机：n=12,m=25，可暴力对拍量级")
write_case(4, 60, 80, "mix", "小规模随机：n=60,m=80")

# ---- 点 5-6：中等规模随机 ----
write_case(5, 2000, 3000, "mix", "中等规模随机：n=2e3,m=3e3")
write_case(6, 10000, 20000, "mix", "中等规模随机：n=1e4,m=2e4，范围中间档")

# ---- 点 7-8：大规模随机（接近上限） ----
write_case(7, 50000, 60000, "all5", "大规模随机：n=5e4,m=6e4，5 种操作均匀")
write_case(8, 79999, 79999, "query", "大规模随机：n=m=79999，查询为主（输出量大）")

# ---- 点 9-10：顶格层 ----
# 点 9：n=m=8e4 顶格，5 种操作均匀混合（含大量 Top/Bottom 的子树整体搬移）
write_case(9, MAXN, MAXN, "all5", "顶格层：n=m=8e4，全维度顶格随机")

# 点 10：n=m=8e4 顶格 + 最坏结构：以全 Insert（交替 -1/+1）为主持续卡 splay 路径，
#        每 50 步夹一次 Ask/Query，保证输出非空且验证持续扰动下的正确性
write_case(10, MAXN, MAXN, "insert", "顶格层最坏结构：Insert 交替 ±1 为主，每 50 步一次查询")
