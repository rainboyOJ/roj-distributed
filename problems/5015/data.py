#!/usr/bin/env python3
# 一本通 1679《子集》分层数据生成器
# 数据范围：n <= 2e5，0 <= a_i <= 1e6
# 分层：1-2 边界层 / 3-4 小规模随机 / 5-6 中等规模随机 / 7-8 大规模随机 / 9-10 顶格层
from cyaron import *

MAXA = 1000000

def w(io, a):
    io.input_writeln(len(a))
    io.input_writeln(' '.join(map(str, a)))

# 点 1（边界层）：n=1，最小规模，答案必为 0
io = IO(file_prefix="problem", data_id=1)
w(io, [randint(0, MAXA)])
io.output_gen("../std")

# 点 2（边界层）：n=3，全取最大值 1e6（全相等），答案必为 0
io = IO(file_prefix="problem", data_id=2)
w(io, [MAXA, MAXA, MAXA])
io.output_gen("../std")

# 点 3（小规模随机）：n=10，值域 [0,1]，大量重复值，可手算验证
io = IO(file_prefix="problem", data_id=3)
w(io, [randint(0, 1) for _ in range(10)])
io.output_gen("../std")

# 点 4（小规模随机）：n=20（20% 分上限），值域 [0,10]，可手算/枚举验证
io = IO(file_prefix="problem", data_id=4)
w(io, [randint(0, 10) for _ in range(20)])
io.output_gen("../std")

# 点 5（中等规模随机）：n=200，均匀随机
io = IO(file_prefix="problem", data_id=5)
w(io, [randint(0, MAXA) for _ in range(200)])
io.output_gen("../std")

# 点 6（中等规模随机）：n=2000（60% 分上限），均匀随机
io = IO(file_prefix="problem", data_id=6)
w(io, [randint(0, MAXA) for _ in range(2000)])
io.output_gen("../std")

# 点 7（大规模随机）：n=50000，双峰分布（一半 0 一半 1e6），
# 最优结构为 k 个 0 + (k+1) 个 1e6，价值随 k 增大，考察 k 较大时的三分
io = IO(file_prefix="problem", data_id=7)
w(io, [0] * 25000 + [MAXA] * 25000)
io.output_gen("../std")

# 点 8（大规模随机）：n=100000，小值域 [0,100]，大量重复值
io = IO(file_prefix="problem", data_id=8)
w(io, [randint(0, 100) for _ in range(100000)])
io.output_gen("../std")

# 点 9（顶格层）：n=200000，均匀随机顶格
io = IO(file_prefix="problem", data_id=9)
w(io, [randint(0, MAXA) for _ in range(200000)])
io.output_gen("../std")

# 点 10（顶格层）：n=200000，最坏结构构造：n-1 个 0 + 1 个 1e6
# 最优 k 在 n/2 附近，三分搜索区间最大，且答案峰值平缓，卡三分精度/收敛
io = IO(file_prefix="problem", data_id=10)
w(io, [0] * 199999 + [MAXA])
io.output_gen("../std")
