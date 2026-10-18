#!/usr/bin/env python3
# data.py：「区间最大和」测试数据生成器（cyaron）
# 用法：cd problems/3004 && python3 data.py
# 生成 data/p1.in data/p1.out ... data/p10.in data/p10.out
# 共 10 组：2 组小数据 + 8 组 N = Q = 1e5 的大数据，覆盖各种分布与边界。
# 随机参数固定种子，可重现。

import os
import random
import subprocess

from cyaron import IO

random.seed(3004)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("data", exist_ok=True)

MAX_A = 10 ** 9

# 先编译标程，用它生成每个测试点的 .out
STD_BIN = "/tmp/roj3004_std"
subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD_BIN, "std.cpp"], check=True)


def write_case(data_id, arr, queries):
    """写入一组测试数据：一个完整的输入文件 + 标程生成的输出文件。"""
    io = IO(file_prefix="data/p", data_id=data_id)
    io.input_writeln(len(arr), len(queries))
    io.input_writeln(*arr)
    for t in queries:
        io.input_writeln(t)
    io.output_gen(STD_BIN)
    io.close()
    print("p%d: n=%d q=%d" % (data_id, len(arr), len(queries)))


def rand_array(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def uniform_queries(q, lo, hi):
    # 询问 T 均匀取 [lo, hi]，题面保证 0 <= T <= sum(A)
    return [random.randint(lo, hi) for _ in range(q)]


# p1：极端小数据，A 只有一个数，T 取 0 和 sum 的边界
write_case(1, [1], [0, 0, 1, 1])

# p2：小数据，方便手算调试
small = rand_array(10, 1, 100)
write_case(2, small, uniform_queries(10, 0, sum(small)))

# p3：均匀随机，A 与 T 都随机
arr = rand_array(100000, 1, MAX_A)
write_case(3, arr, uniform_queries(100000, 0, sum(arr)))

# p4：A 全为 1（前缀和最密，答案铺满整个 [0, n]）
arr = [1] * 100000
write_case(4, arr, uniform_queries(100000, 0, 100000))

# p5：A 全为 1e9（sum 最大到 1e14，考验 long long）
arr = [MAX_A] * 100000
write_case(5, arr, uniform_queries(100000, 0, 100000 * MAX_A))

# p6：边界询问：T 取前缀和本身或前缀和减 1，专打 "最后一个 <= T" 的 off-by-one
arr = rand_array(100000, 1, MAX_A)
pre = [0]
for a in arr:
    pre.append(pre[-1] + a)
qs = []
for _ in range(100000):
    k = random.randint(1, 100000)
    if random.random() < 0.5:
        qs.append(pre[k])      # 恰好能跳到 k
    else:
        qs.append(pre[k] - 1)  # 只能跳到 k-1
write_case(6, arr, qs)

# p7：A 单调递增
arr = [1 + (MAX_A - 1) * i // 99999 for i in range(100000)]
write_case(7, arr, uniform_queries(100000, 0, sum(arr)))

# p8：A 单调递减
arr = [MAX_A - (MAX_A - 1) * i // 99999 for i in range(100000)]
write_case(8, arr, uniform_queries(100000, 0, sum(arr)))

# p9：T 偏小（答案集中在 0 附近），混入大量 T = 0
arr = rand_array(100000, 1, MAX_A)
qs = uniform_queries(90000, 0, sum(arr) // 10) + [0] * 10000
random.shuffle(qs)
write_case(9, arr, qs)

# p10：T 偏大（答案集中在 n 附近），混入大量 T = sum
arr = rand_array(100000, 1, MAX_A)
qs = uniform_queries(90000, sum(arr) * 9 // 10, sum(arr)) + [sum(arr)] * 10000
random.shuffle(qs)
write_case(10, arr, qs)
