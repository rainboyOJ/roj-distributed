#!/usr/bin/env python3
# 一本通 1701《最大值》分层数据生成器
# 数据范围：n<=30, m<=100000, 0<=a_i<2^n
from cyaron import *

def gen(io, n, m, lo, hi):
    io.input_writeln(n, m)
    io.input_writeln([randint(lo, hi) for _ in range(m)])

# ---- 点1 边界层：n=1, m=1, a_1=0 全最小值 ----
io = IO(file_prefix="problem", data_id=1)
io.input_writeln(1, 1)
io.input_writeln(0)
io.output_gen("../std")

# ---- 点2 边界层：n=2, m=2, a 全最大值(=2^n-1)，对手等价于直接 rol ----
io = IO(file_prefix="problem", data_id=2)
io.input_writeln(2, 2)
io.input_writeln(3, 3)
io.output_gen("../std")

# ---- 点3 小规模随机：n=3, m=4，可手算/暴力验证 ----
io = IO(file_prefix="problem", data_id=3)
gen(io, 3, 4, 0, 7)
io.output_gen("../std")

# ---- 点4 小规模随机：n=10, m=100（对应 20% 档上界）----
io = IO(file_prefix="problem", data_id=4)
gen(io, 10, 100, 0, 1023)
io.output_gen("../std")

# ---- 点5 中等规模：n=15, m=1000，值域只用低半段（构造稀疏值域）----
io = IO(file_prefix="problem", data_id=5)
gen(io, 15, 1000, 0, 255)
io.output_gen("../std")

# ---- 点6 中等规模：n=30, m=10（对应“另外20%”档：大 n 小 m）----
io = IO(file_prefix="problem", data_id=6)
gen(io, 30, 10, 0, (1 << 30) - 1)
io.output_gen("../std")

# ---- 点7 大规模随机：n=20, m=50000 ----
io = IO(file_prefix="problem", data_id=7)
gen(io, 20, 50000, 0, (1 << 20) - 1)
io.output_gen("../std")

# ---- 点8 大规模随机：n=30, m=80000 ----
io = IO(file_prefix="problem", data_id=8)
gen(io, 30, 80000, 0, (1 << 30) - 1)
io.output_gen("../std")

# ---- 点9 顶格层：n=30, m=100000 全满随机（卡字典树结点上界 ~(m+1)*n）----
io = IO(file_prefix="problem", data_id=9)
gen(io, 30, 100000, 0, (1 << 30) - 1)
io.output_gen("../std")

# ---- 点10 顶格层：n=30, m=100000，最坏结构——a_i 全相等(=2^30-1) ----
# c 集合仅含两个值，字典树退化为两条链；同时全最大权值
io = IO(file_prefix="problem", data_id=10)
io.input_writeln(30, 100000)
io.input_writeln([(1 << 30) - 1] * 100000)
io.output_gen("../std")
