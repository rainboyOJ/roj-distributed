#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1696《前缀和》 分层数据生成器
# 题意：给一个字符串 s，求所有长度为偶数的前缀在 s 中出现的次数之和（可重叠）。
# 数据范围：|s| <= 200000。答案上界约 n^2/4，long long 可容纳。
# 分层（10 组，从边界铺到顶格）：
#   1-2   边界层：n=1（无偶数前缀，答案 0）、n=2 全同（偶数前缀出现 1 次）
#   3-4   小规模随机：可手算验证
#   5-6   中等规模随机
#   7-8   大规模随机：接近上限
#   9-10  顶格层：n=200000，全同 / 近乎全同（最大 border 链，答案最大，卡时结构）

from cyaron import *


def gen_all_same(n, ch='a'):
    return ch * n


def gen_random(n, charset):
    s = []
    for _ in range(n):
        s.append(charset[randint(0, len(charset) - 1)])
    return ''.join(s)


def gen_all_same_tail_noise(n, ch='a'):
    # 顶格卡时结构：前面全部相同，末尾塞一个不同字符，
    # 前缀函数几乎每个位置都要回退，退化成最坏情况的 KMP。
    if n <= 1:
        return ch * n
    return ch * (n - 1) + 'b'


def write_case(i, s):
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_write(s)
    io.output_gen("../std")  # 用已编译的标程生成答案


# 点 1：边界，n=1，答案 0
write_case(1, 'a')
# 点 2：边界，n=2 全同，长度为 2 的前缀只出现 1 次
write_case(2, 'aa')
# 点 3：小规模随机，n=5，小字符集
write_case(3, gen_random(5, 'ab'))
# 点 4：小规模随机，n=12，小字符集，可手算
write_case(4, gen_random(12, 'abc'))
# 点 5：中等规模随机，n=1000
write_case(5, gen_random(1000, 'abc'))
# 点 6：中等规模随机，n=5000，字符集稍大，减少偶然重复
write_case(6, gen_random(5000, 'abcdefgh'))
# 点 7：大规模随机，n=100000
write_case(7, gen_random(100000, 'abcdefgh'))
# 点 8：大规模随机，n=150000
write_case(8, gen_random(150000, 'abcdefghijkl'))
# 点 9：顶格层，n=200000 全同（border 链最长，出现次数和最大）
write_case(9, gen_all_same(200000, 'a'))
# 点 10：顶格层，n=200000 前全同末尾加异字符（KMP 最坏回退结构）
write_case(10, gen_all_same_tail_noise(200000, 'a'))
