#!/usr/bin/env python3
# 一本通 1677 软件开发 数据生成器
# 数据范围：1<=n<=100, 1<=m<=100, 1<=d1,d2<=100
# 分层设计（10 组）：
#  点1  边界层：n=1, m=1, d=(1,1) 全最小值，答案 2
#  点2  边界层：n=1, m=100, d=(100,100) 单人顶格，答案 20000（理论最大答案）
#  点3  小规模随机：n=2, m=3，可手算验证
#  点4  小规模随机：n=3, m=5，可手算验证
#  点5  中等随机：n=10, m=30
#  点6  中等随机：n=30, m=50
#  点7  大规模随机：n=80, m=90
#  点8  大规模随机：n=100, m=95，偏极端权值（d 集中在 {1,100}）
#  点9  顶格层：n=100, m=100，d 全 100（全相等最坏构造，答案=2*m*100/n 上取整型）
#  点10 顶格层：n=100, m=100，d 均匀随机顶格
from cyaron import *

def gen(io, n, m, pairs):
    io.input_writeln(n, m)
    for d1, d2 in pairs:
        io.input_writeln(d1, d2)
    io.output_gen("../std")

def rand_pairs(n, lo=1, hi=100):
    return [(randint(lo, hi), randint(lo, hi)) for _ in range(n)]

# 点1 边界：全最小
io = IO(file_prefix="problem", data_id=1)
gen(io, 1, 1, [(1, 1)])

# 点2 边界：n=1 顶格，答案最大
io = IO(file_prefix="problem", data_id=2)
gen(io, 1, 100, [(100, 100)])

# 点3 小规模随机（可手算）
io = IO(file_prefix="problem", data_id=3)
gen(io, 2, 3, rand_pairs(2, 1, 5))

# 点4 小规模随机（可手算）
io = IO(file_prefix="problem", data_id=4)
gen(io, 3, 5, rand_pairs(3, 1, 10))

# 点5 中等随机
io = IO(file_prefix="problem", data_id=5)
gen(io, 10, 30, rand_pairs(10))

# 点6 中等随机
io = IO(file_prefix="problem", data_id=6)
gen(io, 30, 50, rand_pairs(30))

# 点7 大规模随机
io = IO(file_prefix="problem", data_id=7)
gen(io, 80, 90, rand_pairs(80))

# 点8 大规模，极端权值（大量 1 与 100 混合）
io = IO(file_prefix="problem", data_id=8)
pairs = [(choice([1, 100]), choice([1, 100])) for _ in range(100)]
gen(io, 100, 95, pairs)

# 点9 顶格：全相等最坏构造 d=(100,100)
io = IO(file_prefix="problem", data_id=9)
gen(io, 100, 100, [(100, 100)] * 100)

# 点10 顶格：随机
io = IO(file_prefix="problem", data_id=10)
gen(io, 100, 100, rand_pairs(100))
