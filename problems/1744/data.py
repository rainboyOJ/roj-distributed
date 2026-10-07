#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1744《跳台阶》分层数据生成器
# 范围（题面）：1≤N≤5e5，0<H_i≤1e9。
# 分层（10 组）：
#   p1  n=1 边界（最小）            p2  题面样例 n=3 [1,3,1]
#   p3  n=2 极值（相等/两极）      p4  小随机 n=20
#   p5  n=5000 随机（50% 档）      p6  n=5e4 随机
#   p7  n=2e5 随机                 p8  n=5e5 严格递增（单调最坏）
#   p9  n=5e5 全相等（退化）       p10 n=5e5 两极锯齿（TV 最坏）
import random
random.seed(1744)

def emit(name, H):
    with open(f'data/{name}.in', 'w') as f:
        f.write(str(len(H)) + '\n')
        f.write(' '.join(map(str, H)) + '\n')
    print(name, 'n=', len(H))

emit('problem1', [5])
emit('problem2', [1, 3, 1])
emit('problem3', [10**9, 10**9])
emit('problem4', [random.randint(1, 10**9) for _ in range(20)])
emit('problem5', [random.randint(1, 10**9) for _ in range(5000)])
emit('problem6', [random.randint(1, 10**9) for _ in range(50000)])
emit('problem7', [random.randint(1, 10**9) for _ in range(200000)])
emit('problem8', [int(1 + i * (10**9 - 1) / (500000 - 1)) for i in range(500000)])
emit('problem9', [123456789] * 500000)
emit('problem10', [10**9 if i % 2 == 0 else 1 for i in range(500000)])
print('done')
