#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1708《无限链计数》分层数据生成器
# 范围（题面）：n≤1000 个禁止串，t≤6，每串长度≤10。答案 ≤2^31-1 或 -1。
# 分层设计（10 组，答案谱系：正例小/中/大 + 0 + -1 混搭）：
#   点1  题面样例 t=2 {ab,ba} → 2
#   点2  题面例子 t=2 {ab} → 3
#   点3  退化 t=1 {a} → 0（无合法链）
#   点4  t=2 {aa,ab,ba} → 1（只剩全 b 链）
#   点5  t=3 禁全部跨字母双串（x≠y 共 6 个）→ 3（常值链）
#   点6  t=2 {aaa} → -1（自由度过大，无穷类）
#   点7  t=4，n=50，|s|≤6 随机（中等混合）
#   点8  顶格 t=6，n=1000，|s|≤10 随机（n 顶格）
#   点9  t=6 正例：禁 30 个跨字母双串 + 970 个冗余长串（均含跨字母对）→ 6
#   点10 顶格 t=6，n=1000，|s|=10 纯随机（长度顶格）
import random

random.seed(1708)
OUT = 'data'


def emit(i, t, strs):
    with open(f'{OUT}/problem{i}.in', 'w') as f:
        f.write(f'{t} {len(strs)}\n')
        f.write('\n'.join(strs) + ('\n' if strs else ''))
    print(f'problem{i}: t={t} n={len(strs)}')


def rnd(n, lo, hi, t):
    alpha = 'abcdefghijklmnopqrstuvwxyz'[:t]
    return [''.join(random.choice(alpha) for _ in range(random.randint(lo, hi))) for _ in range(n)]


emit(1, 2, ['ab', 'ba'])
emit(2, 2, ['ab'])
emit(3, 1, ['a'])
emit(4, 2, ['aa', 'ab', 'ba'])
cross3 = [x + y for x in 'abc' for y in 'abc' if x != y]
emit(5, 3, cross3)
emit(6, 2, ['aaa'])
emit(7, 4, rnd(50, 1, 6, 4))
emit(8, 6, rnd(1000, 1, 10, 6))
alpha6 = 'abcdef'
cross6 = [x + y for x in alpha6 for y in alpha6 if x != y]
pad = []
while len(pad) < 970:
    s = random.choice(cross6) + ''.join(random.choice(alpha6) for _ in range(random.randint(0, 8)))
    pad.append(s[:10])
emit(9, 6, cross6 + pad)
emit(10, 6, rnd(1000, 10, 10, 6))
print('done')
