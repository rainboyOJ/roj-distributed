#!/usr/bin/env python3
# data.py：区间最大利润 测试数据生成器（cyaron）
# 用法：cd problems/1820 && python3 data.py
# 生成 data/p1.in data/p1.out ... data/p12.in data/p12.out

import os
import random
import subprocess

from cyaron import IO

random.seed(1820)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("data", exist_ok=True)

MAX_A = 10 ** 9

STD_BIN = "/tmp/roj1820_std"
subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD_BIN, "std.cpp"], check=True)


def write_case(data_id, arr, queries):
    io = IO(file_prefix="data/p", data_id=data_id)
    io.input_writeln(len(arr), len(queries))
    io.input_writeln(*arr)
    for l, r in queries:
        io.input_writeln(l, r)
    io.output_gen(STD_BIN)
    io.close()
    print("p%d: n=%d q=%d" % (data_id, len(arr), len(queries)))


def rand_queries(n, q, max_len=None):
    """随机询问，可限制区间最大长度。"""
    qs = []
    for _ in range(q):
        l = random.randint(1, n - 1)
        r = random.randint(l + 1, n)
        if max_len is not None and r - l + 1 > max_len:
            r = min(n, l + max_len - 1)
        qs.append((l, r))
    return qs


# p1：题面样例
write_case(1, [5, 3, 1, 3, 4, 3], [(1, 6), (1, 4), (3, 6), (4, 5)])

# p2：小数据随机，方便手算调试
arr = [random.randint(1, 100) for _ in range(10)]
write_case(2, arr, rand_queries(10, 10))

# p3：n = 2，只有一个区间，升与降都覆盖到需要两组
write_case(3, [1, MAX_A], [(1, 2)])

# p4：n = 2 下降，答案为负
write_case(4, [MAX_A, 1], [(1, 2)])

# p5：全同价，答案恒为 0
arr = [777777] * 100000
write_case(5, arr, rand_queries(100000, 100000))

# p6：严格递减，答案恒为 -1（最小的负利润）
arr = list(range(100000, 0, -1))
write_case(6, arr, rand_queries(100000, 100000))

# p7：严格递增，答案是区间两端之差
arr = list(range(1, 100001))
write_case(7, arr, rand_queries(100000, 100000))

# p8：随机大数据，全长度随机询问
arr = [random.randint(1, MAX_A) for _ in range(100000)]
write_case(8, arr, rand_queries(100000, 100000))

# p9：只有短区间询问（长度 2~10），考验边界与合并
arr = [random.randint(1, MAX_A) for _ in range(100000)]
write_case(9, arr, rand_queries(100000, 100000, max_len=10))

# p10：多种区间长度混合（短/中/长各占三分之一），考验不同规模的合并
arr = [random.randint(1, MAX_A) for _ in range(100000)]
qs = []
for _ in range(100000):
    bucket = random.random()
    if bucket < 0.34:
        length = random.randint(2, 100)          # 短
    elif bucket < 0.67:
        length = random.randint(100, 5000)       # 中
    else:
        length = random.randint(5000, 100000)    # 长
    l = random.randint(1, 100000 - length + 1)
    qs.append((l, l + length - 1))
write_case(10, arr, qs)

# p11：先高后低（答案在区间靠后的位置才出现）
arr = [random.randint(10 ** 8, MAX_A) for _ in range(50000)]
arr += [random.randint(1, 1000) for _ in range(50000)]
write_case(11, arr, rand_queries(100000, 100000))

# p12：极端值混排，只有 1 和 1e9
arr = [random.choice([1, MAX_A]) for _ in range(100000)]
write_case(12, arr, rand_queries(100000, 100000))
