#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1690《棋盘问题》分层数据生成器
# 题面数据范围：T<20；-5000<=fx,fy,tx,ty<=5000；1<=n<=10；1<=x,y<=10
# 生成 problem1.in/.out ... problem10.in/.out，用 std 直接生成答案。
# 说明：坐标可为负，向量分量题面约束为正（1..10），故「非负向量」时目标必须
#       位于起点的右上方向才可能到达；构造 IMPOSSIBLE 用奇偶性 / gcd 技巧。

from cyaron import IO
import random

random.seed(1690)

# 顶格坐标
MAXC = 5000


def vecs_all_even(k):
    """生成 k 个分量均为偶数的向量（1..10 内：2,4,6,8,10），用于构造奇偶不可达。"""
    choices = [2, 4, 6, 8, 10]
    return [(random.choice(choices), random.choice(choices)) for _ in range(k)]


def write_case(io, fx, fy, tx, ty, vecs):
    io.input_writeln(fx, fy, tx, ty)
    io.input_writeln(len(vecs))
    for x, y in vecs:
        io.input_writeln(x, y)


def make_reachable_vecs(n):
    """随机生成 n 个正向量，保证 (1,1) 在列，便于构造可达目标。"""
    vecs = [(1, 1)]
    while len(vecs) < n:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if (x, y) not in vecs:
            vecs.append((x, y))
    random.shuffle(vecs)
    return vecs


def reachable_target(start, vecs, maxsteps):
    """用若干步（<=maxsteps）向量组合构造一个可达目标，返回 (tx,ty) 或 None。"""
    sx, sy = start
    dx = dy = 0
    steps = random.randint(1, maxsteps)
    for _ in range(steps):
        x, y = random.choice(vecs)
        dx += x
        dy += y
        # 超出坐标范围则放弃（重新随机）
        if not (-MAXC - sx <= dx <= MAXC - sx and -MAXC - sy <= dy <= MAXC - sy):
            return None
    return sx + dx, sy + dy


def rand_start():
    return random.randint(-MAXC, MAXC), random.randint(-MAXC, MAXC)


def rand_vecs(n):
    vecs = set()
    while len(vecs) < n:
        vecs.add((random.randint(1, 10), random.randint(1, 10)))
    return list(vecs)


# ---------------------------------------------------------------------------
# 点 1：边界层（最小规模）
#   n=1 单向量、起点=终点（答案 0）、一步到达（答案 1）、最大坐标下起点=终点。
def gen1(io):
    io.input_writeln(3)
    write_case(io, 0, 0, 0, 0, [(1, 1)])               # 答案 0
    write_case(io, 0, 0, 1, 1, [(1, 1)])               # 答案 1
    write_case(io, MAXC, MAXC, MAXC, MAXC, [(1, 1)])   # 答案 0（顶格坐标）


# 点 2：边界层（答案为 1 / IMPOSSIBLE / 大跨度单向量）
#   单向量 (10,10) 一步到顶；单向量奇偶不可达；单向量 1000 步长链。
def gen2(io):
    io.input_writeln(3)
    write_case(io, 0, 0, 10, 10, [(10, 10)])                     # 答案 1
    write_case(io, 0, 0, 5, 5, [(10, 10)])                       # IMPOSSIBLE（奇偶）
    write_case(io, -MAXC, -MAXC, MAXC, MAXC, [(10, 10)])         # 答案 1000


# 点 3：小规模随机（可手算量级）
#   三组小坐标、向量含 (1,1) 保证可达，另含 (1,2)(2,1) 奇偶/3 整除不可达。
def gen3(io):
    io.input_writeln(3)
    write_case(io, 0, 0, 6, 6, [(1, 2), (2, 1), (2, 2), (1, 3), (3, 1)])  # 样例1：3
    write_case(io, 0, 0, 5, 5, [(1, 2), (2, 1)])                          # 样例2：IMPOSSIBLE
    write_case(io, 0, 0, 3, 4, [(1, 1), (2, 1), (1, 2)])                  # 小答案


# 点 4：小规模随机
#   多组随机小坐标可达 + 一组奇偶不可达。
def gen4(io):
    io.input_writeln(4)
    vecs = make_reachable_vecs(3)
    for _ in range(3):
        s = rand_start()
        while True:
            t = reachable_target(s, vecs, 8)
            if t is not None:
                break
        write_case(io, s[0], s[1], t[0], t[1], vecs)
    write_case(io, 0, 0, 3, 7, vecs_all_even(3))   # 偶数向量 -> 奇坐标不可达


# 点 5：中等规模随机
#   坐标约 ±1500，n=5，构造可达；含一组不可达。
def gen5(io):
    io.input_writeln(3)
    vecs = make_reachable_vecs(5)
    for _ in range(2):
        s = (random.randint(-1500, -1000), random.randint(-1500, -1000))
        t = reachable_target(s, vecs, 300)
        while t is None:
            t = reachable_target(s, vecs, 300)
        write_case(io, s[0], s[1], t[0], t[1], vecs)
    write_case(io, 0, 0, 1001, 1003, vecs_all_even(5))


# 点 6：中等规模随机
#   坐标约 ±2500，n=8，构造可达。
def gen6(io):
    io.input_writeln(3)
    vecs = make_reachable_vecs(8)
    for _ in range(3):
        s = (random.randint(-2500, -2000), random.randint(-2500, -2000))
        t = reachable_target(s, vecs, 500)
        while t is None:
            t = reachable_target(s, vecs, 500)
        write_case(io, s[0], s[1], t[0], t[1], vecs)


# 点 7：大规模随机
#   坐标接近上限，n=10，构造可达（含大跨度）。
def gen7(io):
    io.input_writeln(2)
    vecs = make_reachable_vecs(10)
    for _ in range(2):
        s = (random.randint(-4500, -3500), random.randint(-4500, -3500))
        t = reachable_target(s, vecs, 900)
        while t is None:
            t = reachable_target(s, vecs, 900)
        write_case(io, s[0], s[1], t[0], t[1], vecs)


# 点 8：大规模随机
#   坐标接近上限，n=10，多样向量（含最大 D 的 (10,10)）。
def gen8(io):
    io.input_writeln(2)
    vecs = [(1, 1), (10, 10), (10, 9), (9, 10), (1, 10),
            (10, 1), (5, 5), (3, 7), (7, 3), (2, 2)]
    for _ in range(2):
        s = (random.randint(-4800, -4000), random.randint(-4800, -4000))
        t = reachable_target(s, vecs, 1000)
        while t is None:
            t = reachable_target(s, vecs, 1000)
        write_case(io, s[0], s[1], t[0], t[1], vecs)


# 点 9：顶格层（最坏结构·长走廊宽通道）
#   起点 (-5000,-5000) 终点 (5000,5000)，n=10，向量多样含大分量，
#   使可达且步数多、BFS 走廊宽，顶到题面上限。
def gen9(io):
    io.input_writeln(1)
    vecs = [(10, 10), (10, 9), (9, 10), (8, 10), (10, 8),
            (9, 9), (7, 10), (10, 7), (6, 10), (10, 6)]
    write_case(io, -MAXC, -MAXC, MAXC, MAXC, vecs)


# 点 10：顶格层（极端权值 + IMPOSSIBLE + 单轴极限）
#   (a) 全偶数向量 -> 大跨度奇偶不可达；(b) 顶格坐标大跨度可达。
def gen10(io):
    io.input_writeln(2)
    # 全偶数向量 -> 只能到达偶坐标增量；(5000,4999) 增量 dy=9999 为奇，不可达。
    write_case(io, -MAXC, -MAXC, MAXC, 4999, vecs_all_even(10))    # IMPOSSIBLE
    write_case(io, -MAXC, -MAXC, MAXC, MAXC, [(1, 1), (10, 10)])   # 1000


GENS = [gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10]

for i, gen in enumerate(GENS, start=1):
    io = IO(file_prefix="problem", data_id=i)
    gen(io)
    io.output_gen("../std")
