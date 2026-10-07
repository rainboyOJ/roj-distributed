#!/usr/bin/env python3
# 一本通 1699《石环》数据生成器
# 运行方式：cd data && python3 ../data.py  （std 位于上一级目录）
#
# 题目：输入多组测试数据（EOF 结束），每组一行字符串 s（小写字母，1<=|s|<=1e6，
#       组数 <=6）。输出每组一个长度为 n 的 01 串。
#
# 分层设计（10 个测试点，每个测试点内含 <=6 组字符串）：
#   点 1-2  边界层：n=1/n=2/全相同/全不同/首尾相同等极端
#   点 3-4  小规模随机：n 5~100，可手算验证
#   点 5-6  中等规模随机：n 1000/5000，范围中间档
#   点 7-8  大规模随机：n 50000/200000，接近上限
#   点 9-10 顶格层：n=1e6，随机 + 最坏结构（全相同 / 相邻全不同交替）
from cyaron import *  # noqa: F401,F403
import random

random.seed(20250629)


def rand_str(n, alpha):
    return ''.join(random.choice(alpha) for _ in range(n))


def ringy(n, alpha):
    # 相邻字符两两不同（首尾不保证不同）
    if len(alpha) < 2:
        alpha = 'ab'
    res = [random.choice(alpha)]
    for _ in range(n - 1):
        c = random.choice(alpha)
        while c == res[-1]:
            c = random.choice(alpha)
        res.append(c)
    return ''.join(res)


def alt(n, a='a', b='b'):
    # a/b 交替串，保证相邻不同
    return (a + b) * (n // 2) + (a if n % 2 else '')


# 每个测试点对应的字符串列表（每组一行）
cases = {
    1: [
        'a',          # n=1，唯一极端
        'aa',         # n=2 全相同
        'ab',         # n=2 全不同
        'aba',        # n=3 首尾相同
        'abc',        # n=3 全不同
    ],
    2: [
        'aaaa',       # n=4 全相同 -> 0001
        'aaaaa',      # n=5 全相同 -> 00001
        'abab',       # n=4 交替（题面样例）
        'brbg',       # 题面样例
        'rrrrr',      # 题面样例
    ],
    3: [
        rand_str(random.randint(5, 8), 'ab'),
        rand_str(random.randint(5, 10), 'abc'),
        ringy(random.randint(6, 12), 'ab'),
        ringy(random.randint(6, 12), 'abc'),
    ],
    4: [
        rand_str(random.randint(20, 50), 'ab'),
        rand_str(random.randint(20, 50), 'abcd'),
        ringy(random.randint(30, 60), 'abc'),
        rand_str(random.randint(40, 100), 'a'),  # 全 a，制造密集断点
    ],
    5: [
        rand_str(1000, 'ab'),
        ringy(1000, 'abc'),
        rand_str(1000, 'abcd'),
    ],
    6: [
        rand_str(5000, 'ab'),
        ringy(5000, 'abcd'),
        alt(5000),
        rand_str(5000, 'a'),
    ],
    7: [
        rand_str(50000, 'ab'),
        ringy(50000, 'abcd'),
    ],
    8: [
        rand_str(200000, 'abc'),
        ringy(200000, 'abcd'),
        alt(200000),
    ],
    9: [
        rand_str(1000000, 'abcdefghijklmnopqrstuvwxyz'),
    ],
    10: [
        'a' * 1000000,          # 全相同：单段长 2n，border 链最长，最坏结构
        alt(1000000),           # 相邻全不同：无断点，单段长 2n
    ],
}

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)  # problem1.in / problem1.out ...
    for s in cases[i]:
        io.input_writeln(s)
    io.output_gen("../std")
