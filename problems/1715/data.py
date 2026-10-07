#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一本通 1715《公交旅行》数据生成器（cyaron）
#
# 题面（.ybt-import/staging/1715/content.md）：
#   n 个站台、m 条环形公交线路。第 i 条线路长度 t_i，由站台 s_i,1..s_i,t_i 组成；
#   0 时刻第 i 辆车在 s_i,1，之后每时刻到线路中下一个站台，到终点后下一时刻回到起点
#   （位置按 (j+1) mod t_i 循环）。0 时刻我在站台 1，同时在同站即可上车、任意时刻可下车，
#   可换乘。求最早到达站台 2..n 的时刻，不可达输出 -1。
#
# 数据范围（题面【提示】表格）：
#   子任务1: n,m<=50,      Σt_i<=300
#   子任务2: n,m<=10^3,    Σt_i<=2*10^4
#   子任务3: n,m<=5*10^3,  Σt_i<=10^5
#   子任务4: n,m<=10^5,    Σt_i<=2*10^5
#   另有 100% 约束 t_i>=2；同一站台可在一条线路中出现多次，但不会相邻。
#
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 分层设计（10 组，覆盖 边界/小/中/大/顶格）：
#   点 1  边界：题面样例（答案已知 2 3 4 6 3 -1 -1）
#   点 2  边界：n=3,m=1 最小结构，含不可达站台（手算 "1 -1"）
#   点 3  小规模：n=m=50, Σt≈300 随机（子任务1 上限）
#   点 4  小规模结构：同站台在线路中重复出现（不相邻）、同站多线路竞争、含不可达
#   点 5  中规模：n=m=1000, Σt=2*10^4 随机（子任务2 上限）
#   点 6  中规模链式：4999 跳换乘链 + 长捷径线路，答案呈层状（考验等待时刻递推）
#   点 7  大规模：n=m=5000, Σt=1e5（子任务3 上限），随机长线路
#   点 8  顶格：n=m=1e5, Σt=2e5（子任务4 上限）：半链接链 + 半随机边
#   点 9  顶格长环：一条 t=1e5 的置换长线路 + 5 万条 t=2 边（顶格 Σt、大周期取模）
#   点 10 顶格星形卡常：站台 1 挂 5 万条 t=2 线路 + 一条 t=1e5 长线路（Dijkstra 松弛量最大）

import os
import random
from cyaron import IO  # 引入CYaRon的库

random.seed(1715)

MAXN = 100000
MAXM = 100000
MAXSUM = 200000


def emit(data_id, n, routes, note):
    """写出第 data_id 组：n, m 与各线路；用 std 生成 .out。"""
    assert len(routes) <= MAXM, "m 超上限"
    for r in routes:
        assert len(r) >= 2, "t_i 必须 >= 2"
        assert all(1 <= s <= n for s in r), "站台编号越界"
        for a, b in zip(r, r[1:]):
            assert a != b, "相邻站台不能相同"
    total = sum(len(r) for r in routes)
    assert total <= MAXSUM, "Σt_i 超上限"

    io = IO(file_prefix="problem", data_id=data_id)
    body = [str(n) + " " + str(len(routes))]
    for r in routes:
        body.append(str(len(r)) + " " + " ".join(map(str, r)))
    io.input_write("\n".join(body) + "\n")
    io.output_gen("../std")
    print("problem%-2d: n=%-6d m=%-6d Σt=%-6d  %s" % (data_id, n, len(routes), total, note))


# ---------------- 点 1：题面样例（边界，答案手算/官方样例已知） ----------------
def gen1():
    routes = [[5, 4], [6, 1, 2], [4, 2, 1, 3], [7, 8]]
    emit(1, 8, routes, "边界：题面样例，答案 2 3 4 6 3 -1 -1")


# ---------------- 点 2：最小边界（含不可达） ----------------
def gen2():
    routes = [[1, 2]]          # 一辆车只在 1<->2 往返
    emit(2, 3, routes, "边界：n=3 最小结构，站台 3 不可达 → 1 -1")


def fix_adjacent(routes, n):
    """题面保证同一站台不会在一条线路中相邻出现。"""
    for r in routes:
        for i in range(1, len(r)):
            if r[i] == r[i - 1]:
                r[i] = r[i] % n + 1


# ---------------- 点 3：小规模随机（子任务 1 顶格） ----------------
def gen3():
    n = 50
    m = 50
    sum_t = 300
    routes = []
    budget = sum_t - n                 # 预留一条覆盖 1..n 的随机环
    for i in range(m - 1):
        left = m - 2 - i
        t = random.randint(2, max(2, min(8, budget - 2 * left)))
        assert t >= 2
        routes.append([random.randint(1, n) for _ in range(t)])
        budget -= t
    assert budget >= 0
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    routes.append(perm)                # 保证站台 1..n 全部连通
    fix_adjacent(routes, n)
    emit(3, n, routes, "小规模随机：n=m=50, Σt=300（子任务1 上限）")


# ---------------- 点 4：小规模结构（重复站台、竞争线路、不可达） ----------------
def gen4():
    n = 40
    routes = [
        [1, 2, 1, 3, 2],          # 站台 1、2 在同一条线路中重复出现且不相邻（t=5）
        [7, 1, 9, 7, 11],         # 站台 7 重复出现且不相邻（t=5）
        [30, 31, 32, 33],         # 与 1 号站台不连通的小团（这些站台应输出 -1，t=4）
        [5, 40, 5],               # 站台 5 首尾重复（t=3）
        [1, 20],                  # 单边（t=2）
        [20, 21, 1, 22, 23, 24],  # 1 与 20 双向连通，同一站上多线路竞争
        [11, 12],
        [12, 13],
    ]
    for r in routes:
        assert len(r) >= 2
        assert all(r[i] != r[i + 1] for i in range(len(r) - 1))
    emit(4, n, routes, "小规模结构：重复站台/多线路竞争/不连通团")


# ---------------- 点 5：中规模随机（子任务 2 顶格） ----------------
def gen5():
    n = 1000
    m = 1000
    sum_t = 20000
    routes = []
    budget = sum_t - n                 # 预留一条覆盖 1..n 的随机环
    for i in range(m - 1):
        left = m - 2 - i
        t = random.randint(2, max(2, min(60, budget - 2 * left)))
        routes.append([random.randint(1, n) for _ in range(t)])
        budget -= t
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    routes.append(perm)                # 保证连通
    fix_adjacent(routes, n)
    emit(5, n, routes, "中规模随机：n=m=1000, Σt=2e4（子任务2 上限）")


# ---------------- 点 6：中规模链式换乘（层状答案） ----------------
def gen6():
    n = 5000
    # 站台 i 只能经线路 "2 i i+1" 到达 i+1：每跳都要等到下个时刻，形成 4999 跳长链，
    # 答案逐层递增；末条长线路（只走奇数站台）再制造跨层捷径与相位干扰。
    routes = [[i, i + 1] for i in range(1, n)]
    routes.append(list(range(1, n + 1, 2)))
    emit(6, n, routes, "中规模链式：4999 跳换乘链 + 长捷径线路")


# ---------------- 点 7：大规模随机长线路（子任务 3 顶格） ----------------
def gen7():
    n = 5000
    m = 5000
    sum_t = 100000
    routes = []
    budget = sum_t - n                 # 预留一条覆盖 1..n 的随机环
    for i in range(m - 1):
        left = m - 2 - i
        t = random.randint(2, max(2, min(40, budget - 2 * left)))
        routes.append([random.randint(1, n) for _ in range(t)])
        budget -= t
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    routes.append(perm)                # 保证连通
    fix_adjacent(routes, n)
    emit(7, n, routes, "大规模随机：n=m=5000, Σt=1e5（子任务3 上限）")


# ---------------- 点 8：顶格（子任务 4 上限） ----------------
def gen8():
    n = MAXN
    # 前 50000 条 t=2 线路串成长链 1-2-...-50001；余下 50000 条随机边
    routes = []
    for i in range(1, 50001):
        routes.append([i, i + 1])
    for _ in range(50000):
        a = random.randint(1, n)
        b = random.randint(1, n)
        if a == b:
            b = b % n + 1
        routes.append([a, b])
    emit(8, n, routes, "顶格：n=m=1e5, Σt=2e5（半链 + 半随机边）")


# ---------------- 点 9：顶格长环（大周期取模） ----------------
def gen9():
    n = MAXN
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    routes = [perm]                     # 单条 t=1e5 的环形线路（周期 1e5）
    for _ in range(50000):              # 再 5 万条 t=2 边，恰好顶格 Σt=2e5
        a = random.randint(1, n)
        b = random.randint(1, n)
        if a == b:
            b = b % n + 1
        routes.append([a, b])
    emit(9, n, routes, "顶格长环：1 条 t=1e5 置换环 + 5e4 条 t=2 边（Σt=2e5）")


# ---------------- 点 10：顶格星形卡常 ----------------
def gen10():
    n = MAXN
    routes = []
    # 站台 1 上挂 5 万条 t=2 线路：Dijkstra 从 1 出发时单点松弛量最大
    for _ in range(50000):
        x = random.randint(2, n)
        routes.append([1, x])
    # 一条 t=1e5 长线路：与所有星形边发生过模等待交互
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    routes.append(perm)
    emit(10, n, routes, "顶格星形：站台1 挂 5e4 条 t=2 + 1 条 t=1e5（Σt=2e5）")


if __name__ == "__main__":
    if not os.path.isdir("data"):
        os.makedirs("data")
    os.chdir("data")
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    print("done")
