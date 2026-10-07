#!/usr/bin/env python
# 一本通 1681《统计方案》数据生成器（cyaron 惯例）
# 题面数据范围：n<=32, p<=1e9（质数）, c<=1e9, a[i]<p（正整数）
# 分层策略（10 个测试点）：
#   点 1-2  边界层：n=1/2 最小规模、答案为 0（c>=p）、答案为 1、全 1 陷阱（c=1 空-空集）
#   点 3-4  小规模随机：n=3~8，小质数 p，可手算验证量级
#   点 5-6  中等规模随机：n=12~20，p 覆盖小/中/大质数
#   点 7-8  大规模随机：n=24~30，p 接近 1e9
#   点 9-10 顶格层：n=32 顶格 + 最坏结构（全 1 → 方案数 2^32-1 顶满 / 全 p-1 / 大质数 + 混合重复值）

from cyaron import * # 引入CYaRon的库

def is_prime(x):
    if x < 2: return False
    if x < 4: return True
    if x % 2 == 0: return False
    i = 3
    while i * i <= x:
        if x % i == 0: return False
        i += 2
    return True

def rand_prime(lo, hi):
    while True:
        x = randint(lo, hi)
        if is_prime(x):
            return x

cases = []

# ---- 点 1：边界层（最小 n、答案极端）----
# n=1, p=2（最小质数）, c=1, a=[1]：唯一非空子集 {1}，乘积 1 ≡ 1，答案恰为 1
cases.append((1, 2, 1, [1]))

# ---- 点 2：边界层（c>=p → 答案必为 0 + 空-空集陷阱）----
# n=2, p=7, c=2（题面样例原样），a=[1,2]：{2} 与 {1,2} 两种 → 2
cases.append((2, 7, 2, [1, 2]))

# ---- 点 3：小规模随机（n=3~5，小质数）----
n = 5; p = rand_prime(2, 50); a = [randint(1, p - 1) for _ in range(n)]
c = randint(0, p - 1)
cases.append((n, p, c, a))

# ---- 点 4：小规模随机（n=8，含大量 1 与 p-1，方案数偏多）----
n = 8; p = rand_prime(2, 200)
a = [1 if i % 3 == 0 else (p - 1 if i % 3 == 1 else randint(1, p - 1)) for i in range(n)]
c = randint(0, p - 1)
cases.append((n, p, c, a))

# ---- 点 5：中等规模随机（n=12，中等质数）----
n = 12; p = rand_prime(2, 100000)
a = [randint(1, p - 1) for _ in range(n)]
c = randint(0, p - 1)
cases.append((n, p, c, a))

# ---- 点 6：中等规模随机（n=20=2^20=1e6 子集，仍小到可对照 30% 档 n<=16 之上的过渡档）----
n = 20; p = rand_prime(2, 10000000)
a = [randint(1, p - 1) for _ in range(n)]
c = 1 if randint(0, 2) == 0 else randint(0, p - 1)  # 1/3 概率触发 c=1 陷阱
cases.append((n, p, c, a))

# ---- 点 7：大规模随机（n=24，p 接近 1e9）----
n = 24; p = rand_prime(999000000, 999999999)
a = [randint(1, p - 1) for _ in range(n)]
c = randint(0, p - 1)
cases.append((n, p, c, a))

# ---- 点 8：大规模随机（n=30，大质数 + 混合重复值/1）----
n = 30; p = rand_prime(500000000, 999999999)
a = []
for i in range(n):
    r = randint(0, 9)
    if r == 0: a.append(1)
    elif r == 1: a.append(p - 1)
    else: a.append(randint(1, p - 1))
c = 1 if randint(0, 3) == 0 else randint(0, p - 1)
cases.append((n, p, c, a))

# ---- 点 9：顶格层（n=32 顶格 + 最坏结构：全 1，c=1）----
# 全 1 时任意非空子集乘积均为 1，方案数 = 2^32 - 1 = 4294967295，
# 是本题答案的理论最大值，同时触发 c=1 的空-空集扣除逻辑（必须减 1 才正确）
cases.append((32, rand_prime(999000000, 999999999), 1, [1] * 32))

# ---- 点 10：顶格层（n=32 顶格 + c>=p 边界 + 大质数随机）----
# p 顶到最大量级（<=1e9），c 取 p-1（合法余数最大），a 随机
p = rand_prime(999999000, 999999999)
cases.append((32, p, p - 1, [randint(1, p - 1) for _ in range(32)]))

for i, (n, p, c, a) in enumerate(cases, start=1):
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(n, p, c)
    io.input_writeln(a)
    io.output_gen("../std")
