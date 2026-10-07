#!/usr/bin/env python3
# 一本通 1702《异或运算》数据生成器（cyaron）
#
# 数据范围：
#   n ≤ 1000, m ≤ 300000, 0 ≤ X_i,Y_j < 2^31
#   p ≤ 500, 1 ≤ k ≤ (d-u+1)*(r-l+1)
#
# 分层方案（10 组）：
#   problem1   边界层：n=1, m=1，单个元素，k 只能为 1
#   problem2   边界层：n=2, m=2，全 0 与全最大值的极端混合
#   problem3   小规模随机：n,m ≤ 6，手算可验，普通随机值
#   problem4   小规模随机：n,m ≤ 15，含重复值/小值域
#   problem5   中等规模：n=40, m=2000，随机值
#   problem6   中等规模：n=200, m=10000，随机值
#   problem7   大规模：n=600, m=100000，随机值
#   problem8   大规模：n=1000, m=200000，随机值（接近上限）
#   problem9   顶格层：n=1000, m=300000，全随机值，p=500 全随机询问
#   problem10  顶格层：n=1000, m=300000，最坏结构：全相等/重复值 + 大跨度区间，
#              迫使每个询问都统计接近满区间，考验可持久化 trie 的最坏常数

from cyaron import *
import random

MAXV = (1 << 31) - 1


def gen_case(i, n, m, p, make_x, make_y, make_query):
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(n, m)
    io.input_writeln(make_x(n))
    io.input_writeln(make_y(m))
    io.input_writeln(p)
    for _ in range(p):
        u, d, l, r, k = make_query(n, m)
        io.input_writeln(u, d, l, r, k)
    io.output_gen("../std")


def rx(n):
    return [randint(0, MAXV) for _ in range(n)]


def small(n, lim):
    return [randint(0, lim) for _ in range(n)]


def query_full(n, m):
    return 1, n, 1, m, randint(1, n * m)


def query_rand(n, m):
    u = randint(1, n)
    d = randint(u, n)
    l = randint(1, m)
    r = randint(l, m)
    k = randint(1, (d - u + 1) * (r - l + 1))
    return u, d, l, r, k


def main():
    rng = random.Random(20260101)

    # problem1：边界层 n=1, m=1
    io = IO(file_prefix="problem", data_id=1)
    io.input_writeln(1, 1)
    io.input_writeln(0)
    io.input_writeln(MAXV)
    io.input_writeln(1)
    io.input_writeln(1, 1, 1, 1, 1)
    io.output_gen("../std")

    # problem2：边界层 n=2, m=2，全 0 与全最大值混合
    io = IO(file_prefix="problem", data_id=2)
    io.input_writeln(2, 2)
    io.input_writeln(0, MAXV)
    io.input_writeln(MAXV, 0)
    io.input_writeln(3)
    io.input_writeln(1, 2, 1, 2, 1)
    io.input_writeln(1, 2, 1, 2, 4)
    io.input_writeln(1, 1, 1, 2, 2)
    io.output_gen("../std")

    # problem3：小规模随机
    gen_case(3, 6, 6, 8, lambda n: small(n, 15), lambda m: small(m, 15), query_rand)

    # problem4：小规模随机，含重复值/小值域
    gen_case(4, 15, 15, 12, lambda n: small(n, 7), lambda m: small(m, 7), query_rand)

    # problem5：中等规模随机
    gen_case(5, 40, 2000, 100, rx, rx, query_rand)

    # problem6：中等规模随机
    gen_case(6, 200, 10000, 200, rx, rx, query_rand)

    # problem7：大规模随机
    gen_case(7, 600, 100000, 300, rx, rx, query_rand)

    # problem8：大规模随机（接近上限）
    gen_case(8, 1000, 200000, 400, rx, rx, query_rand)

    # problem9：顶格层，全随机
    gen_case(9, 1000, 300000, 500, rx, rx, query_rand)

    # problem10：顶格层最坏结构：全相等值 + 大跨度区间
    gen_case(10, 1000, 300000, 500,
             lambda n: [MAXV] * n,
             lambda m: [MAXV] * m,
             query_full)


if __name__ == "__main__":
    main()
