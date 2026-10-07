#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1810《登山》分层测试数据生成器（cyaron，仓库惯例）
# 用法：nice -n 19 timeout 120 g++ -O2 -std=c++17 std.cpp -o std
#       mkdir -p data && cd data && nice -n 19 timeout 120 python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、.ybt-import/staging/1222/data.py
#
# 题意：从 (0,0) 走格路到 (N,N)，每步 (x+1,y) 或 (x,y+1)；站在 (x,x)（山脊）上时不能走 (x,y+1)。
#       => 路径全程 x>=y（不越过 y=x），再挖掉 C 个不可走点，问路径数 mod 1e9+7。
# 数据范围（题面明文）：1 <= N <= 100000，0 <= C <= 1000；障碍点满足 X >= Y 且互不相同，
#   (0,0) 与 (N,N) 不是障碍。限制 time 1000 ms / memory 128 MB（config.json）。
#
# ---- 分层策略（10 个点，规模从最小铺到顶格）----
#   点 1  边界层：N=1, C=0（全最小值）—— 唯一路径 (0,0)->(1,0)->(1,1)，答案 1。
#   点 2  边界层：N=1, C=1，障碍 (1,0) —— 答案为 0 的极端（最小网格 + 唯一必经点被堵）。
#   点 3  边界层（题面样例回归）：题面【样例输入1】N=5 C=2 (5,0)(1,1) -> 27。
#   点 4  边界层（题面样例回归）：题面【样例输入2】N=7 C=4 -> 34。
#   点 5  边界层（无解结构）：N=50, C=5，含必经点 (N,N-1)=(50,49) —— 通向 (N,N) 的
#         唯一合法前驱只有 (N,N-1)（(N-1,N) 越出 x>=y 区域），故答案必为 0。
#   点 6  小规模：N=200, C=1（覆盖题面「另外 20% 数据 C=1」），障碍取非割点 (100,50)。
#   点 7  中等规模：N=5000, C=100 随机障碍（x>y，避开割点 (N,N-1)）。
#   点 8  大规模：N=100000, C=0（覆盖题面「另外 20% 数据 C=0」，答案=卡特兰数 Cat(1e5)）。
#   点 9  大规模：N=100000, C=1000 随机障碍（贴上限的随机结构）。
#   点 10 顶格层（最坏结构）：N=100000, C=1000 = 900 个链式障碍 (i+1,i), i=1..900
#         （两两可比 => 容斥内层跑满 ~4.05e5 对，卡 O(C^2)）+ 100 个随机障碍。
#
# 说明：随机点均取 x>y（山脊上方的点），避免随机堵住必经结构使答案恒 0；
#       0 答案的极端由点 2/点 5 定点构造。固定随机种子，结果可复现。

import os
import random
import subprocess

from cyaron import IO  # 引入CYaRon的库

MOD = 10 ** 9 + 7
MAXN = 100000
MAXC = 1000
STD = os.path.abspath("../std")


def catalan(n):
    """独立公式（与 std 的反射/容斥路线不同）：Cat(n) = C(2n,n)/(n+1) mod p。"""
    f = 1
    for i in range(1, 2 * n + 1):
        f = f * i % MOD
    g = 1
    for i in range(1, n + 1):
        g = g * i % MOD
    h = 1
    for i in range(1, n + 1):
        h = h * i % MOD
    return f * pow(g * h % MOD * (n + 1) % MOD, MOD - 2, MOD) % MOD


def rand_obstacles(n, c, seed, skip=()):
    """在 x>y 区域随机取 c 个互不相同的障碍点（X>=Y 满足题面保证）。"""
    rng = random.Random(seed)
    got = set(skip)
    res = []
    while len(res) < c:
        x = rng.randint(1, n)
        y = rng.randint(0, x - 1)          # y < x，避开山脊线
        if (x, y) in got:
            continue
        got.add((x, y))
        res.append((x, y))
    return res


def chain_obstacles(cnt):
    """链式障碍 (i+1, i)：两两可比，容斥内层跑满，最坏 O(C^2) 结构。"""
    return [(i + 1, i) for i in range(1, cnt + 1)]


CASES = [
    (1, 1, [], "边界层：N=1,C=0 全最小值，答案 1（唯一路径）"),
    (2, 1, [(1, 0)], "边界层：N=1,C=1 堵唯一必经点 (1,0)，答案 0 的极端"),
    (3, 5, [(5, 0), (1, 1)], "边界层：题面【样例输入1】，答案必须为 27"),
    (4, 7, [(6, 5), (5, 3), (2, 1), (7, 1)], "边界层：题面【样例输入2】，答案必须为 34"),
    (5, 50, [(50, 49), (1, 0), (2, 1), (3, 1), (50, 48)],
     "边界层：含必经点 (N,N-1)=(50,49)，无解结构，答案必为 0"),
    (6, 200, [(100, 50)], "小规模：C=1（题面 20% 子任务），非割点障碍"),
    (7, 5000, None, "中等规模：N=5000, C=100 随机障碍（x>y）"),
    (8, 100000, [], "大规模：N=1e5, C=0（题面 20% 子任务），答案=卡特兰数 Cat(1e5)"),
    (9, 100000, None, "大规模：N=1e5, C=1000 随机障碍（贴上限随机结构）"),
    (10, 100000, None, "顶格层：N=1e5, C=1000 = 900 链式 (i+1,i) + 100 随机，最坏 O(C^2)"),
]

# 为随机点准备固定种子的障碍集
CASES[6] = (7, 5000, rand_obstacles(5000, 100, 181007, skip={(5000, 4999)}),
            CASES[6][3])
CASES[8] = (9, 100000, rand_obstacles(100000, 1000, 181009, skip={(100000, 99999)}),
            CASES[8][3])
CASES[9] = (10, 100000,
            chain_obstacles(900) + rand_obstacles(100000, 100, 181010,
                                                  skip={(100000, 99999)}),
            CASES[9][3])

assert len(CASES) == 10, "必须恰好 10 个测试点"

# ---- 生成 .in + 显式 subprocess 产 .out（不依赖 cyaron 输出缓冲，规避 0 字节 .out 隐患）----
summary = []
for idx, n, obs, note in CASES:
    assert 1 <= n <= MAXN, "N 越界"
    assert len(obs) <= MAXC, "C 越界"
    assert len(set(obs)) == len(obs), "障碍点重复"
    for x, y in obs:
        assert 0 <= y <= x <= n and (x, y) not in ((0, 0), (n, n)), "障碍点不合法 (%d,%d)" % (x, y)

    io = IO(file_prefix="problem", data_id=idx, disable_output=True)
    io.input_writeln(n, len(obs))
    for x, y in obs:
        io.input_writeln(x, y)
    io.flush_buffer()                     # 显式 flush，保证 .in 完整落盘

    in_path = "problem%d.in" % idx
    out_path = "problem%d.out" % idx
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        r = subprocess.run([STD], stdin=fi, stdout=fo, timeout=60)
    assert r.returncode == 0, "点 %d std 退出码 %d" % (idx, r.returncode)

    # ---- 断言 .out 非空 / 行数符合预期（本题输出恒为 1 行非负整数）----
    raw = open(out_path, "rb").read()
    assert len(raw) > 0, "点 %d 的 .out 为空（0 字节）" % idx
    assert raw.count(b"\n") == 1 and raw.endswith(b"\n"), "点 %d 的 .out 行数不是 1" % idx
    ans = int(raw)
    assert 0 <= ans < MOD, "点 %d 答案越界 %d" % (idx, ans)

    summary.append((idx, n, len(obs), ans, note))

# ---- 独立期望值断言（样例 / 卡特兰公式 / 无解结构），不依赖 std ----
expect = {1: 1, 2: 0, 3: 27, 4: 34, 5: 0, 8: catalan(100000)}
for idx, n, c, ans, note in summary:
    if idx in expect:
        assert ans == expect[idx], "点 %d 答案 %d != 独立期望 %d" % (idx, ans, expect[idx])

for idx, n, c, ans, note in summary:
    print("problem%-2d: N=%-6d C=%-4d ans=%-10d %s" % (idx, n, c, ans, note))
print("OK: 10 组数据生成完毕，.out 均非空且为 1 行；样例/卡特兰/无解 独立期望值全部吻合")
