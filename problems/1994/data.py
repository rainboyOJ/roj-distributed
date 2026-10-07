#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1994《音乐会》数据生成器
# 数据范围（题面）：0<=hh<=9, 0<=mm<=59, 0<=ss<=59, 1<=n,m<=20000
# 时间折成秒：t = h*3600 + m*60 + s，范围 [0, 35999]。
# 每条记录是闭区间 [l, r]，表示这些“秒”都有该乐器演奏；单点询问输出该秒演奏的所有乐器（PVCDB 顺序，无则 None）。
import random
from cyaron import IO

random.seed(1994)

MAXT = 35999          # 9*3600 + 59*60 + 59
INSTR = "PVCDB"


def fmt(t):
    h = t // 3600
    m = (t % 3600) // 60
    s = t % 60
    return "%02d:%02d:%02d" % (h, m, s)


def rand_interval(max_t=MAXT):
    l = random.randint(0, max_t)
    r = random.randint(l, max_t)
    return l, r


def write_case(i, intervals, queries):
    """intervals: list of (l, r, ch); queries: list of seconds."""
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(len(intervals))
    for l, r, ch in intervals:
        io.input_writeln("%s %s %s" % (fmt(l), fmt(r), ch))
    io.input_writeln(len(queries))
    for t in queries:
        io.input_writeln(fmt(t))
    io.output_gen("../std")


def main():
    # ---- 点 1：n=1，单秒 P，询问命中/前后空档 ----
    write_case(1,
               [(0, 0, 'P')],
               [0, 1, 2])

    # ---- 点 2：单秒各乐器 + 同秒 P/V 重叠（考察 PVCDB 输出顺序），含空时刻 ----
    write_case(2,
               [(0, 0, 'P'), (0, 0, 'V'), (1, 1, 'C'), (2, 2, 'D'), (3, 3, 'B')],
               [0, 1, 2, 3, 4])

    # ---- 点 3：小规模随机（可手算量级）----
    iv = []
    for _ in range(10):
        l, r = rand_interval(100)
        iv.append((l, r, random.choice(INSTR)))
    write_case(3, iv, [random.randint(0, 120) for _ in range(10)])

    # ---- 点 4：小规模随机 ----
    iv = []
    for _ in range(20):
        l, r = rand_interval(1000)
        iv.append((l, r, random.choice(INSTR)))
    write_case(4, iv, [random.randint(0, 1200) for _ in range(20)])

    # ---- 点 5：中等规模随机 ----
    iv = []
    for _ in range(1000):
        l, r = rand_interval()
        iv.append((l, r, random.choice(INSTR)))
    write_case(5, iv, [random.randint(0, MAXT) for _ in range(1000)])

    # ---- 点 6：中等规模随机 ----
    iv = []
    for _ in range(2000):
        l, r = rand_interval()
        iv.append((l, r, random.choice(INSTR)))
    write_case(6, iv, [random.randint(0, MAXT) for _ in range(2000)])

    # ---- 点 7：大规模随机（接近上限）----
    iv = []
    for _ in range(10000):
        l, r = rand_interval()
        iv.append((l, r, random.choice(INSTR)))
    write_case(7, iv, [random.randint(0, MAXT) for _ in range(10000)])

    # ---- 点 8：大规模随机 ----
    iv = []
    for _ in range(15000):
        l, r = rand_interval()
        iv.append((l, r, random.choice(INSTR)))
    write_case(8, iv, [random.randint(0, MAXT) for _ in range(15000)])

    # ---- 点 9：顶格规模随机 ----
    iv = []
    for _ in range(20000):
        l, r = rand_interval()
        iv.append((l, r, random.choice(INSTR)))
    write_case(9, iv, [random.randint(0, MAXT) for _ in range(20000)])

    # ---- 点 10：顶格 + 最坏结构（5 种乐器全覆盖 [0,35999]，任意询问输出 PVCDB；含边界询问）----
    iv = []
    for i in range(20000):
        iv.append((0, MAXT, INSTR[i % 5]))
    queries = [0, MAXT] + [random.randint(0, MAXT) for _ in range(19998)]
    write_case(10, iv, queries)


if __name__ == "__main__":
    main()
