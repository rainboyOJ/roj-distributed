#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1684《翻转序列》数据生成器
# 题面范围：t = 5（固定 5 组数据），n <= 23；每个数据点含 5 组测试。
# 原提示中「测试点 1,2 n=5 / 3,4 n=6 / ...」为原始 25 个点的细分方案，
# 本仓库按惯例合并为 10 个点，故按 n 从小到大 + 结构分层铺满 1..23。
#
# 分层设计（每点 5 组）：
#   点1  n=1..5         边界：n=1 升序 0 步；n=2 升序 0 步；n=2 单次翻转；
#                         n=3 逆序(2 步)；n=5 已升序。
#   点2  n=5            小规模极端：升序(0)、逆序、单次翻转可达、相邻差构造、
#                         随机。
#   点3  n=6            小规模随机，可手算/暴力核对。
#   点4  n=7            小规模随机 + 逆序 + 半逆序结构。
#   点5  n=8..10        中规模，随机为主，含 1 个逆序结构。
#   点6  n=11..13       中规模随机，含重复出现的坏邻接结构。
#   点7  n=14..16       大规模随机。
#   点8  n=17..19       大规模随机 + 逆序。
#   点9  n=20..22       接近顶格：随机 + 逆序 + 特殊构造（先逆序再扰动）。
#   点10 n=23（题面上限）顶格：全逆序、逆序扰动、随机、坏邻接交错结构。
from cyaron import IO
import random


def permutation(n, rnd):
    """返回 1..n 的一个排列；rnd 为 random.Random 实例。"""
    p = list(range(1, n + 1))
    rnd.shuffle(p)
    return p


def reversed_perm(n):
    """完全逆序排列 n, n-1, ..., 1（pancake 最坏结构，需 2n-3 步）。"""
    return list(range(n, 0, -1))


def sorted_perm(n):
    return list(range(1, n + 1))


def single_flip(n, rnd):
    """升序基础上做 1 次前缀翻转：只需 1 步即可变回升序。"""
    i = rnd.randint(2, n)
    p = list(range(1, n + 1))
    p[:i] = reversed(p[:i])
    return p


def one_off(n, rnd):
    """升序基础上交换一对相邻元素，制造少量坏邻接。"""
    p = list(range(1, n + 1))
    if n >= 2:
        i = rnd.randint(1, n - 1)
        p[i - 1], p[i] = p[i], p[i - 1]
    return p


def rev_perturb(n, rnd):
    """逆序基础上随机交换少量对，保持接近最坏结构。"""
    p = reversed_perm(n)
    swaps = rnd.randint(1, min(5, n))
    for _ in range(swaps):
        i, j = rnd.randrange(n), rnd.randrange(n)
        p[i], p[j] = p[j], p[i]
    return p


def case_line(p):
    return " ".join(str(x) for x in p)


def emit(io, cases):
    """cases: list of permutation lists；写满每组 n 与排列。"""
    io.input_writeln(len(cases))
    for p in cases:
        io.input_writeln(len(p))
        io.input_writeln(case_line(p))


for pid in range(1, 11):
    rnd = random.Random(1684 * 100 + pid)
    io = IO(file_prefix="problem", data_id=pid)
    cases = []

    if pid == 1:
        # 边界层：最小 n、0 步、1 步
        cases = [
            [1],
            [1, 2],
            [2, 1],
            [3, 2, 1],
            [1, 2, 3, 4, 5],
        ]
    elif pid == 2:
        # n=5 极端结构
        cases = [
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            single_flip(5, rnd),
            one_off(5, rnd),
            permutation(5, rnd),
        ]
    elif pid == 3:
        # n=6 小规模随机
        cases = [permutation(6, rnd) for _ in range(5)]
    elif pid == 4:
        # n=7 小规模 + 逆序 + 半逆序
        half = list(range(7, 3, -1)) + list(range(1, 4))  # 7 6 5 4 1 2 3
        cases = [
            permutation(7, rnd),
            reversed_perm(7),
            half,
            permutation(7, rnd),
            one_off(7, rnd),
        ]
    elif pid == 5:
        # 中规模 n=8..10
        cases = [
            reversed_perm(8),
            permutation(9, rnd),
            permutation(9, rnd),
            permutation(10, rnd),
            rev_perturb(10, rnd),
        ]
    elif pid == 6:
        # 中规模 n=11..13
        cases = [
            permutation(11, rnd),
            reversed_perm(12),
            permutation(12, rnd),
            permutation(13, rnd),
            rev_perturb(13, rnd),
        ]
    elif pid == 7:
        # 大规模 n=14..16
        cases = [
            permutation(14, rnd),
            permutation(15, rnd),
            reversed_perm(15),
            permutation(16, rnd),
            rev_perturb(16, rnd),
        ]
    elif pid == 8:
        # 大规模 n=17..19
        cases = [
            permutation(17, rnd),
            permutation(18, rnd),
            reversed_perm(18),
            permutation(19, rnd),
            rev_perturb(19, rnd),
        ]
    elif pid == 9:
        # 接近顶格 n=20..22
        cases = [
            permutation(20, rnd),
            reversed_perm(21),
            permutation(21, rnd),
            permutation(22, rnd),
            rev_perturb(22, rnd),
        ]
    else:  # pid == 10
        # 顶格层 n=23（题面上限）
        cases = [
            reversed_perm(23),       # pancake 最坏结构
            rev_perturb(23, rnd),    # 逆序 + 少量扰动，仍接近最坏
            permutation(23, rnd),
            permutation(23, rnd),
            rev_perturb(23, rnd),
        ]

    emit(io, cases)
    io.output_gen("../std")
