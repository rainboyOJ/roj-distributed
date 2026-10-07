#!/usr/bin/env python

from cyaron import *  # 引入CYaRon的库

# 题面保证 0<=A,B,C<=100 且均为 10 的整数倍
VALS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def rnd():
    return choice(VALS)


for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)  # problem1.in / problem1.out

    if i == 1:
        # 最小规模边界：三项全 0
        a, b, c = 0, 0, 0
    elif i == 2:
        # 最大规模边界：三项全 100
        a, b, c = 100, 100, 100
    elif i == 3:
        # 题面样例 1
        a, b, c = 100, 100, 80
    elif i == 4:
        # 题面样例 2
        a, b, c = 60, 90, 80
    elif i == 5:
        # 30% 数据特征：A = B = 0
        a, b, c = 0, 0, rnd()
    elif i == 6:
        # 另外 30% 数据特征：A = B = 100
        a, b, c = 100, 100, rnd()
    elif i == 7:
        # 单项取极值
        a, b, c = 0, 100, 0
    elif i == 8:
        a, b, c = 100, 0, 100
    else:
        # 一般随机数据（i == 9, 10）
        a, b, c = rnd(), rnd(), rnd()

    io.input_write(a, b, c)
    io.output_gen("../std")
