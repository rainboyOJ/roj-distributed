#!/usr/bin/env python3
# data.py：最大利润(Maximum Profit) 测试数据生成器（cyaron）
# 用法：cd problems/1417 && python3 data.py
# 生成 data/p1.in data/p1.out ... data/p12.in data/p12.out
# 覆盖：官方两组样例、n=2 边界、全同价、严格递减（答案为负）、
#       严格递增、随机大中小数据、极端值 1 与 1e9。

import os
import random
import subprocess

from cyaron import IO

random.seed(1417)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("data", exist_ok=True)

MAX_R = 10 ** 9

STD_BIN = "/tmp/roj1417_std"
subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD_BIN, "std.cpp"], check=True)


def write_case(data_id, arr):
    io = IO(file_prefix="data/p", data_id=data_id)
    io.input_writeln(len(arr))
    for v in arr:
        io.input_writeln(v)
    io.output_gen(STD_BIN)
    io.close()
    print("p%d: n=%d" % (data_id, len(arr)))


# p1、p2：官方两组样例
write_case(1, [5, 3, 1, 3, 4, 3])
write_case(2, [4, 3, 2])

# p3：n = 2 的最小规模（升 / 降两种极端都放进同一组不行，故拆成两题）
write_case(3, [1, 1000000000])

# p4：n = 2，下降，答案恰为负
write_case(4, [1000000000, 1])

# p5：全同价，答案 0
write_case(5, [777777] * 200000)

# p6：严格递减，答案恒为 -1（最小的负利润）
write_case(6, list(range(200000, 0, -1)))

# p7：严格递增，最优是第一天买最后一天卖
write_case(7, list(range(1, 200001)))

# p8：随机大数据
write_case(8, [random.randint(1, MAX_R) for _ in range(200000)])

# p9：先高后低（答案在很靠后的位置才出现）
arr = [random.randint(10 ** 8, MAX_R) for _ in range(100000)]
arr += [random.randint(1, 1000) for _ in range(100000)]
write_case(9, arr)

# p10：锯齿形，最小值出现在中间
arr = []
for i in range(100000):
    arr.append(MAX_R - i if i % 2 == 0 else i + 1)
write_case(10, arr)

# p11：小数据随机，方便调试
write_case(11, [random.randint(1, 100) for _ in range(10)])

# p12：极端值混排：只有 1 和 1e9
write_case(12, [random.choice([1, MAX_R]) for _ in range(200000)])
