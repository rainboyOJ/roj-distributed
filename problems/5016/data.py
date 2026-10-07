#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1680《序列》 数据生成器（cyaron）
# 数据范围：1 <= N <= 1e9，1 <= T <= 2000。
# 每组数据：第一行 T，接下来 T 行每行一个整数 N。
# 10 个测试点按规模分层，从最小铺到顶格。

from cyaron import *

# 预计算 Golomb 序列（用于获取"块边界"代表性值）
def build_golomb(limit):
    a = [0, 1, 2]   # a[v] = v 在序列中出现次数
    S = [0, 1, 3]   # S[v] = last(v) = sum a[1..v]
    n = 2
    while S[n] < limit:
        gn = a[n]
        a.append(1 + a[n + 1 - a[gn]])
        n += 1
        S.append(S[n - 1] + a[n])
    return a, S, n

_a, _S, _K = build_golomb(10**9 + 10)
# 覆盖所有 N<=1e9 所需的块号上限（last(K) 首次 >= 1e9）
KMAX = _K

# 代表性块号（N 取这些值时 last(N) 恰好是块末尾，易触发边界 bug）
BLOCK_KS = [1, 2, 3, 10, 100, 1000, 10000, 100000, KMAX]

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)

    if i == 1:
        # 点1 边界层：T=1，N=1（最小规模）
        T = 1
        vals = [1]
    elif i == 2:
        # 点2 边界层：小值 + 块边界，覆盖答案为 0/1 的极端与小特殊值
        T = 6
        vals = [1, 2, 3, 4, 5, 6]
    elif i == 3:
        # 点3 小规模随机：N in [1,100]，可手算验证
        T = 20
        vals = [randint(1, 100) for _ in range(T)]
    elif i == 4:
        # 点4 小规模随机 + 边界：N in [1,1000]
        T = 30
        vals = [randint(1, 1000) for _ in range(T - 5)]
        vals += [1000, 100, 10, 2, 1]
    elif i == 5:
        # 点5 中等规模随机：N in [1e4, 1e6]
        T = 100
        vals = [randint(10**4, 10**6) for _ in range(T)]
    elif i == 6:
        # 点6 中等规模随机：N in [1e6, 1e7]
        T = 200
        vals = [randint(10**6, 10**7) for _ in range(T)]
    elif i == 7:
        # 点7 大规模随机：N in [1e7, 1e8]
        T = 500
        vals = [randint(10**7, 10**8) for _ in range(T)]
    elif i == 8:
        # 点8 大规模随机：N in [1e8, 1e9]
        T = 1000
        vals = [randint(10**8, 10**9) for _ in range(T)]
    elif i == 9:
        # 点9 顶格层：N 全取上限 1e9，T 取上限 2000（最坏结构：全最大值）
        T = 2000
        vals = [10**9 for _ in range(T)]
    else:
        # 点10 顶格层：混合最大值与块边界附近值，T=2000
        T = 2000
        base = [10**9, 10**9 - 1, 999999999, KMAX, KMAX - 1]
        vals = [base[j % len(base)] for j in range(T)]

    io.input_writeln(T)
    for v in vals:
        io.input_writeln(v)
    io.output_gen("../std")
