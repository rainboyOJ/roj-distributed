#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1730《二分图》分层数据生成器
# 范围（题面）：1≤n≤300，1≤m≤1500，n≤m。邻接矩阵按行给 '0/1' 串。
# 分层设计（10 组）：
#   点1  题面样例1（完美匹配唯一性受限）
#   点2  题面样例2（无完美匹配 → 全 1）
#   点3  题面样例3（三角结构唯一完美匹配）
#   点4  小规模 n=3,m=5 随机
#   点5  中规模 n=30,m=60 随机稠密
#   点6  中大规模 n=100,m=200 随机
#   点7  大规模 n=300,m=600 随机（n 顶格）
#   点8  顶格 n=300,m=1500 稀疏随机（m 顶格）
#   点9  顶格 n=300,m=1500 完全二分 + 空列（边数顶格 300×300，答案全 0 + 空列 1）
#   点10 顶格 n=300,m=1500 对抗混合：唯一匹配骨架 + 大量交错环/尾缀（0/1 混排）
import random

random.seed(1730)
OUT = 'data'


def emit(i, n, m, grid):
    with open(f'{OUT}/problem{i}.in', 'w') as f:
        f.write(f'{n} {m}\n')
        f.write('\n'.join(grid) + '\n')
    ones = sum(r.count('1') for r in grid)
    print(f'problem{i}: n={n} m={m} edges={ones}')


def rnd(n, m, p):
    return [''.join('1' if random.random() < p else '0' for _ in range(m)) for _ in range(n)]


emit(1, 4, 4, ['1111', '1000', '1111', '1111'])
emit(2, 4, 5, ['10000'] * 4)
emit(3, 4, 4, ['1111', '1110', '1100', '1000'])
emit(4, 3, 5, rnd(3, 5, 0.5))
emit(5, 30, 60, rnd(30, 60, 0.5))
emit(6, 100, 200, rnd(100, 200, 0.4))
emit(7, 300, 600, rnd(300, 600, 0.3))
emit(8, 300, 1500, rnd(300, 1500, 0.05))
g9 = ['1' * 300 + '0' * 1200 for _ in range(300)]
emit(9, 300, 1500, g9)
g10 = []
for i in range(300):
    row = ['0'] * 1500
    for j in range(300):          # 三角骨架：唯一完美匹配
        if j <= i:
            row[j] = '1'
    for j in range(300, 1500):    # 尾缀随机：制造交错环与自由点结构
        if random.random() < 0.02:
            row[j] = '1'
    g10.append(''.join(row))
emit(10, 300, 1500, g10)
print('done')
