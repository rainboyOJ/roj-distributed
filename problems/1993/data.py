#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1993 开关switch 分层数据生成器
# 数据范围：2 ≤ N ≤ 100000，1 ≤ M ≤ 100000，c ∈ {0,1}，1 ≤ a ≤ b ≤ N
from cyaron import *

def gen_ops(io, n, m, q_ratio=0.5, full_ratio=0.0, single_ratio=0.0):
    """生成 m 个操作；q_ratio 为查询(c=1)概率；full_ratio 为全区间 [1,n] 概率；
    single_ratio 为单点区间概率。保证至少有一个查询。"""
    has_q = False
    for i in range(m):
        last = (i == m - 1)
        r = random.random()
        if (r < q_ratio) or (last and not has_q):
            c = 1
            has_q = True
        else:
            c = 0
        r2 = random.random()
        if r2 < full_ratio:
            a, b = 1, n
        elif r2 < full_ratio + single_ratio:
            a = b = randint(1, n)
        else:
            a = randint(1, n)
            b = randint(a, n)
        io.input_write(c, a, b)

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)

    if i == 1:
        # 点1 边界层：N=2（最小 N），M=1（最小 M），唯一一个查询，答案为 0
        n, m = 2, 1
        io.input_write(n, m)
        io.input_write(1, 1, 2)

    elif i == 2:
        # 点2 边界层：N=2，全部区间均为 [1,2]，先开全区间再查，答案顶格 N
        n, m = 2, 5
        io.input_write(n, m)
        io.input_write(0, 1, 2)   # 全开
        io.input_write(1, 1, 2)   # -> 2
        io.input_write(0, 1, 1)   # 关掉 1 号
        io.input_write(1, 1, 2)   # -> 1
        io.input_write(1, 2, 2)   # -> 0

    elif i == 3:
        # 点3 小规模随机：N=10, M=20，含单点操作，可手算验证
        n, m = 10, 20
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.5, single_ratio=0.3)

    elif i == 4:
        # 点4 小规模随机：N=50, M=50，翻转偏多
        n, m = 50, 50
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.3)

    elif i == 5:
        # 点5 中等规模随机：N=1000, M=1000
        n, m = 1000, 1000
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.5)

    elif i == 6:
        # 点6 中等规模随机：N=10000, M=10000
        n, m = 10000, 10000
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.5)

    elif i == 7:
        # 点7 大规模随机：N=100000（顶格）, M=50000，混合操作
        n, m = 100000, 50000
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.5)

    elif i == 8:
        # 点8 大规模随机：N=100000, M=100000（双顶格），均匀随机区间
        n, m = 100000, 100000
        io.input_write(n, m)
        gen_ops(io, n, m, q_ratio=0.5)

    elif i == 9:
        # 点9 顶格构造：N=M=100000，全部为全区间 [1,N] 操作——翻转/查询交替，
        # 卡懒标记下传与 pushup 的最坏情形（答案在 0 与 N 之间交替）
        n, m = 100000, 100000
        io.input_write(n, m)
        for k in range(m):
            io.input_write(k % 2, 1, n)
        # 保证至少有一个查询：m 为偶数时 k%2==1 出现 50000 次，天然满足

    elif i == 10:
        # 点10 顶格构造：N=M=100000，交替「单点翻转 + 单点查询」与小区间，
        # 区间长度 1~10，考验递归深度与常数；结尾一次全区间查询
        n, m = 100000, 100000
        io.input_write(n, m)
        for k in range(m - 1):
            c = k % 2
            a = randint(1, n)
            b = min(n, a + randint(0, 9))
            io.input_write(c, a, b)
        io.input_write(1, 1, n)

    io.output_gen("../std")
