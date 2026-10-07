#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1712《汉堡店》分层数据生成器

题面数据范围：2 < N <= 1000，0 <= X,Y <= 1000，0 < P < 10000，输出保留两位小数。
输入只有一组（第一行 N，接下来 N 行 x y P），故每个测试点文件 = 一组数据。

分层（10 组）：
  1  边界层：理论最小 N=3、最小坐标、最小 P（答案 2.00，可手算）
  2  边界层：极端坐标 (0 与 1000) + 极端 P=9999（共线三点，答案 20.00，可手算）
  3  小规模：题面样例（N=4，答案 65.00，与题面【输出样例】对照）
  4  小规模随机：N=8，坐标 0..10，P 小值（可手算/抽查量级）
  5  中等随机：N=120，坐标 0..120
  6  中等随机：N=350，坐标 0..300
  7  大规模随机：N=800，坐标铺满 0..1000
  8  大规模随机：N=950，坐标铺满 0..1000
  9  顶格·最坏结构：N=1000（题面上限），两块稠密点云（中心 (20,20)/(980,980)，
     各 500 点，半径 20）+ 一条 ~1400 长边连接，构造 B 极小、A/B 极大的极端比值结构
  10 顶格·最坏结构：N=1000 点阵（32x32 格点 ×31 铺满 0..961），
     存在大量等距边（权重全为 31 的倍数），MST 多重最优 / 大量等权边，
     用于压测「MST 替换性质」在等权边情形下的正确性。

注：所有点对坐标互不相同。题面未定义两点重合（欧氏距离 0）的情形：此时 B 可为 0，
      A/B 无定义，故原题数据必然不含重合点，生成器同样保证坐标唯一。
"""
import random

from cyaron import IO

random.seed(20251712)

MAXC = 1000      # 坐标上限
MAXP = 9999      # 美味度上限（P < 10000）
MINN = 3         # 题面 2 < N <= 1000，N 最小可取 3


def gen1(io):
    """边界：最小 N、最小坐标、最小 P。MST 两条直角边权均为 1，W=2，
    任意点对 B=1，A=1+1，答案 2/1 = 2.00。"""
    io.input_writeln(MINN)
    for x, y, p in [(0, 0, 1), (0, 1, 1), (1, 0, 1)]:
        io.input_writeln(x, y, p)


def gen2(io):
    """边界：极端坐标 0/1000 + 极端 P=9999。共线三点 (0,0),(1000,0),(0,1000)，
    MST 两腿各 1000，W=2000；任取一条腿，B = 2000-1000 = 1000，A = 19998，
    答案 19.998 -> 20.00。"""
    io.input_writeln(MINN)
    for x, y, p in [(0, 0, MAXP), (MAXC, 0, MAXP), (0, MAXC, MAXP)]:
        io.input_writeln(x, y, p)


def gen3(io):
    """小规模：题面【输入样例】原题数据（答案 65.00）。"""
    io.input_writeln(4)
    for x, y, p in [(1, 1, 20), (1, 2, 30), (200, 2, 80), (200, 1, 100)]:
        io.input_writeln(x, y, p)


def gen4(io):
    """小规模随机：N=8，坐标 0..10（小整数距离，便于手工核对量级），P 1..50。"""
    pts = random.sample([(x, y) for x in range(11) for y in range(11)], 8)
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, 50))


def gen5(io):
    """中等随机：N=120，坐标 0..120，P 1..9999。"""
    pts = random.sample([(x, y) for x in range(121) for y in range(121)], 120)
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


def gen6(io):
    """中等随机：N=350，坐标 0..300，P 1..9999。"""
    pts = random.sample([(x, y) for x in range(301) for y in range(301)], 350)
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


def _random_full(n):
    pts = []
    seen = set()
    while len(pts) < n:
        xy = (random.randint(0, MAXC), random.randint(0, MAXC))
        if xy in seen:
            continue
        seen.add(xy)
        pts.append(xy)
    return pts


def gen7(io):
    """大规模随机：N=800，坐标铺满 0..1000。"""
    pts = _random_full(800)
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


def gen8(io):
    """大规模随机：N=950，坐标铺满 0..1000。"""
    pts = _random_full(950)
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


def gen9(io):
    """顶格·最坏结构：N=1000（题面上限）。两块稠密点云（中心 (20,20) 与 (980,980)，
    各 500 点，半径 20），中间由一条 ~1400 的长边连接。
    此时 W = 内部两组 MST + 长边；取跨簇的两点 a,b，路径最大边即长边，
    B = W - 长边 ≈ 组内 MST 之和（很小），故 A/B 极大 —— 极端比值结构。"""
    pts = []
    seen = set()
    for cx, cy in ((20, 20), (980, 980)):
        cnt = 0
        while cnt < 500:
            x = cx + random.randint(-20, 20)
            y = cy + random.randint(-20, 20)
            if 0 <= x <= MAXC and 0 <= y <= MAXC and (x, y) not in seen:
                seen.add((x, y))
                pts.append((x, y))
                cnt += 1
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


def gen10(io):
    """顶格·最坏结构：N=1000 点阵 32x32（坐标 = 31*i, 31*j，铺满 0..961）。
    所有边权均为 31 的倍数，含大量等权边与多个最优 MST 形态，
    压测等权边下「含边 (u,v) 的最小生成树」公式的实现正确性。"""
    pts = [(31 * i, 31 * j) for i in range(32) for j in range(32)][:1000]
    io.input_writeln(len(pts))
    for x, y in pts:
        io.input_writeln(x, y, random.randint(1, MAXP))


GENS = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]

for i, gen in enumerate(GENS, start=1):
    io = IO(file_prefix="problem", data_id=i)
    gen(io)
    io.output_gen("../std")
