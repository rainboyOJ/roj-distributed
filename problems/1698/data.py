#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1698 字符串匹配 数据生成器
# 输入格式：T=3 C；随后 T 组，每组 n m / s / t，字符取 1..C
# 数据范围：1<=n,m,C<=1e6，T=3（题面约定），1s / 256MB
from cyaron import *
import random

# ---------- 造例工具 ----------
def rand_seq(rng, n, C):
    return [rng.randint(1, C) for _ in range(n)]

def permute_t(rng, s, st, m, C):
    """取 s[st:st+m]，对每个字符做一次随机重命名（保证与窗口双射匹配）"""
    mp = {}
    perm = list(range(1, C + 1))
    rng.shuffle(perm)
    out = []
    for x in s[st:st + m]:
        if x not in mp:
            mp[x] = perm[x - 1]
        out.append(mp[x])
    return out

def embed_case(rng, n, m, C, emb):
    """s 随机，t = s 的某个窗口做双射重命名，保证至少 1 个匹配"""
    s = rand_seq(rng, n, C)
    st = rng.randint(0, n - m)
    t = permute_t(rng, s, st, m, C)
    return n, m, s, t

def nohit_case(rng, n, m, C):
    """大概率 0 匹配：t 中某个字符的出现模式在 s 中不存在（重复结构不同）"""
    s = rand_seq(rng, n, C)
    # t 形如 x,y,x,y,... 但第 3 位换成与第 1 位不同映射，使 1,3 位相同但 2,4 位关系被破坏
    t = [1 if i % 2 == 0 else 2 for i in range(m)]
    if C >= 3 and m >= 4:
        t[3] = 1  # 位置 1,3,4 相同而位置 2 不同 -> 双射关系仅在 s 中出现 1,2,1,1 结构才可能
    return n, m, s, t

def all_same_case(rng, n, m, C):
    """s 全 1，t 全 1：所有窗口均匹配，答案 n-m+1（最坏输出规模）"""
    return n, m, [1] * n, [1] * m

def big_cycle_case(rng, n, m, C, period):
    """最坏结构：s 为长周期循环串（如 1..period 重复），t 取窗口重命名，
    广义 KMP 在此类串上失配跳转最频繁，且答案数量大"""
    s = [i % period + 1 for i in range(n)]
    t = permute_t(rng, s, rng.randint(0, period - 1), m, C)
    return n, m, s, t

def write_case(io, rng, case):
    n, m, s, t = case
    io.input_writeln(n, m)
    io.input_writeln(s)
    io.input_writeln(t)

def gen(io, seed, C, cases):
    rng = random.Random(seed)
    io.input_writeln(3, C)
    for c in cases:
        write_case(io, rng, c)

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)
    R = random.Random(169800 + i)

    if i == 1:
        # 点1【边界层·最小值】：C=1；n=m=1 单字符必匹配；n=m=2 全同；m>n 答案 0
        gen(io, 1, 1,
            [(1, 1, [1], [1]),
             (2, 2, [1, 1], [1, 1]),
             (2, 3, [1, 1], [1, 1, 1])])

    elif i == 2:
        # 点2【边界层·小范围特殊】：C=3 同题面样例档；m=1 每处都匹配(答案 n)；
        # m=n 整体判断；全 1 串窗口全匹配
        gen(io, 2, 3,
            [(6, 1, [1, 2, 1, 2, 3, 2], [3]),
             (5, 5, [1, 2, 1, 2, 1], [3, 1, 3, 1, 3]),
             (6, 3, [1, 1, 1, 1, 1, 1], [2, 2, 2])])

    elif i == 3:
        # 点3【小随机·10%档】：n,m,C<=50，可手算/暴力核对，嵌入 1 个必中
        gen(io, 3, 20,
            [embed_case(R, 50, 20, 20, 1),
             (40, 15, rand_seq(R, 40, 20), rand_seq(R, 15, 20)),
             nohit_case(R, 45, 10, 20)])

    elif i == 4:
        # 点4【小随机·10%档】：n,m,C<=1000，周期结构 + 随机 + 全同
        gen(io, 4, 1000,
            [big_cycle_case(R, 1000, 300, 1000, 7),
             embed_case(R, 900, 400, 1000, 1),
             all_same_case(R, 1000, 500, 1000)])

    elif i == 5:
        # 点5【中随机·30%档】：n,m,C<=1e5，纯随机为主
        gen(io, 5, 100000,
            [(100000, 50000, rand_seq(R, 100000, 100000), rand_seq(R, 50000, 100000)),
             embed_case(R, 80000, 30000, 100000, 1),
             big_cycle_case(R, 100000, 20000, 100000, 11)])

    elif i == 6:
        # 点6【中随机·20%档特征】：n,m<=1e5 但 C=40 小字符集，重复多、匹配多
        gen(io, 6, 40,
            [embed_case(R, 100000, 40000, 40, 1),
             big_cycle_case(R, 100000, 30000, 40, 5),
             nohit_case(R, 100000, 50000, 40)])

    elif i == 7:
        # 点7【大随机】：n=5e5, m=3e5, C=5e5，接近上限的随机 + 嵌入
        gen(io, 7, 500000,
            [(500000, 300000, rand_seq(R, 500000, 500000), rand_seq(R, 300000, 500000)),
             embed_case(R, 500000, 250000, 500000, 1),
             big_cycle_case(R, 400000, 200000, 500000, 13)])

    elif i == 8:
        # 点8【大随机·小字符集最坏结构】：n=8e5, C=2/3，短周期循环 -> KMP 最坏
        gen(io, 8, 3,
            [big_cycle_case(R, 800000, 400000, 2, 2),
             big_cycle_case(R, 800000, 399999, 3, 3),
             all_same_case(R, 800000, 400000, 3)])

    elif i == 9:
        # 点9【顶格】：n=m=C=1e6；m=n 整体匹配/不匹配；全同串最大输出
        gen(io, 9, 1000000,
            [(1000000, 1000000, rand_seq(R, 1000000, 1000000), rand_seq(R, 1000000, 1000000)),
             all_same_case(R, 1000000, 1000000, 1000000),
             embed_case(R, 1000000, 1000000, 1000000, 1)])

    elif i == 10:
        # 点10【顶格·最坏结构】：n=C=1e6，m≈5e5；周期 2 循环 + 全同 + 随机，
        # 卡 KMP 失配跳转与输出规模
        gen(io, 10, 1000000,
            [big_cycle_case(R, 1000000, 500000, 2, 2),
             all_same_case(R, 1000000, 500000, 1000000),
             (1000000, 500000, rand_seq(R, 1000000, 1000000), rand_seq(R, 500000, 1000000))])

    io.output_gen("../std")
    print(f"problem{i} done")
