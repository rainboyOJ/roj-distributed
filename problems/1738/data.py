#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1738《圆桌聚会》分层数据生成器
# 范围（题面）：多组数据，每行一个 n（1≤n≤5×10^5）。
# 分层设计（10 组，按 n 与组数双维度铺开）：
#   点1  n=1（题面样例1）
#   点2  n=4（题面样例2）
#   点3  n=2..30 全枚举（小批量）
#   点4  n=2^k（k=0..18，题面 30% 专项档）
#   点5  20 组随机 n≤100
#   点6  10 组随机 n≤5000
#   点7  20 组随机 n∈[4e5,5e5]（大规模批量）
#   点8  对抗值：5e5 附近素数 + 2^k±1（卡退化构造）
#   点9  n=5e5 单组（规模顶格）
#   点10 30 组混合（含重复 5e5，多测负载顶格）
import random
random.seed(1738)

def emit(name, ns):
    with open(f'data/{name}.in', 'w') as f:
        f.write('\n'.join(map(str, ns)) + '\n')
    print(name, '组数:', len(ns), '总规模:', sum(2*n for n in ns))

emit('problem1', [1])
emit('problem2', [4])
emit('problem3', list(range(2, 31)))
emit('problem4', [2**k for k in range(0, 19)])
emit('problem5', [random.randint(1, 100) for _ in range(20)])
emit('problem6', [random.randint(1, 5000) for _ in range(10)])
emit('problem7', [random.randint(200000, 300000) for _ in range(6)])
emit('problem8', [499999, 499993, 99991, 262143, 131073, 32769])
emit('problem9', [500000])
emit('problem10', [500000, 500000] + [random.randint(10000, 100000) for _ in range(10)])
print('done')
