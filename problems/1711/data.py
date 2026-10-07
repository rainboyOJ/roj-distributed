#!/usr/bin/env python

# 最小花费 数据生成器
# 建模：n+1 个点的完全图最小生成树，边 (i-1, j) 权 c[i][j]。
from cyaron import *  # 引入CYaRon的库
import random

random.seed(20241005)

MAXC = 10 ** 9


def build(io, n, cost_fn):
    """写入 n 以及下三角形状的 n 行费用。cost_fn(i,j) 给出 c[i,j]。"""
    io.input_writeln(n)
    for i in range(1, n + 1):
        row = [cost_fn(i, j) for j in range(i, n + 1)]
        io.input_writeln(row)


def rand_cost(maxc):
    return lambda i, j: random.randint(0, maxc)


for t in range(1, 11):
    io = IO(file_prefix="problem", data_id=t)

    if t == 1:
        n, fn = 3, rand_cost(10)
    elif t == 2:
        n, fn = 5, rand_cost(MAXC)
    elif t == 3:
        n, fn = 10, rand_cost(MAXC)
    elif t == 4:
        n, fn = 50, rand_cost(1000)
    elif t == 5:
        n, fn = 200, rand_cost(MAXC)
    elif t == 6:
        n, fn = 500, rand_cost(MAXC)
    elif t == 7:
        n, fn = 1000, (lambda i, j: 0)          # 全 0，答案为 0
    elif t == 8:
        n, fn = 1500, rand_cost(MAXC)
    elif t == 9:
        n, fn = 2000, rand_cost(MAXC)           # 最大规模随机
    else:
        n, fn = 2000, (lambda i, j: MAXC)       # 全 10^9，答案 = n*10^9

    build(io, n, fn)
    io.output_gen("../std")
