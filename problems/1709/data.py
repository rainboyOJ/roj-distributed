#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1709《寻找好串》分层数据生成器
# 范围（题面）：1≤n≤10000，每串非空、长度≤30、小写字母。
# 分层设计（10 组）：
#   点1  边界：n=1，单字符 "a"（|P|=1，答案 1）
#   点2  边界：n=1，"abc"（纯链，|P|=3）
#   点3  边界：n=3 全同串+前缀嵌套（重串/嵌套 stress）
#   点4  小规模：n=20，|s|≤5，小字母表随机
#   点5  中等：n=500，|s|≤15 随机
#   点6  中等：n=2000，|s|≤20（50% 档）
#   点7  大规模：n=10000，|s|=30，26 字母全随机（|P|≈3e5，答案≈9e10，64 位）
#   点8  顶格：n=10000，|s|=30，2 字母（前缀高度共享，fail 树深）
#   点9  顶格退化：n=10000 全为 "a"×30（|P|=30，答案极小）
#   点10 顶格混合：随机 + 周期串 + 重复串（后缀/前缀重叠对抗）
import random

random.seed(1709)
OUT = 'data'


def emit(i, strs):
    with open(f'{OUT}/problem{i}.in', 'w') as f:
        f.write(str(len(strs)) + '\n')
        f.write('\n'.join(strs) + '\n')
    print(f'problem{i}: n={len(strs)}')


def rnd(n, lo, hi, alpha):
    return [''.join(random.choice(alpha) for _ in range(random.randint(lo, hi))) for _ in range(n)]


emit(1, ['a'])
emit(2, ['abc'])
emit(3, ['a', 'a', 'ab'])
emit(4, rnd(20, 1, 5, 'ab'))
emit(5, rnd(500, 1, 15, 'abcdefghij'))
emit(6, rnd(2000, 5, 20, 'abcdefghijklmnop'))
emit(7, rnd(10000, 30, 30, 'abcdefghijklmnopqrstuvwxyz'))
emit(8, rnd(10000, 30, 30, 'ab'))
emit(9, ['a' * 30] * 10000)
mix = []
for k in range(4000):
    mix.append(''.join(random.choice('ab') for _ in range(30)))
for k in range(3000):
    unit = ''.join(random.choice('abc') for _ in range(random.randint(1, 4)))
    mix.append((unit * 20)[:30])
mix += ['abcabcabcabcabcabcabcabcabcab'] * 2000
mix += rnd(1000, 1, 30, 'abcd')
random.shuffle(mix)
emit(10, mix)
print('done')
