#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1736《最大连通块》分层测试数据生成器（cyaron，仓库惯例）
# 用法：cd .ybt-import/staging/1736
#       g++ -O2 -std=c++17 std.cpp -o std      # macOS 需 Homebrew g++：/opt/homebrew/opt/gcc/bin/g++-16
#       mkdir -p data && cd data && python3 ../data.py
#
# 题意：T 组数据。n 个点、点权 a_i；gcd(a_i,a_j) 为合数则有边。删去恰好 1 个点，使剩余图中
#       最大连通块最小，输出该最小值。
# 数据范围（题面明文，与官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1736 一致）：
#   100%: T<=10, n>=2, a_i>=2, n<=1e5, a_i<=1e7；其中 52% 的数据 a_i<=1e5；
#   16%: n<=300（8% 另有 a_i<=2000）；40%: n<=5000（20% 另有 a_i<=30000）。
#   限制 2000 ms / 512 MB（config.json）。多组数据题：T 与 n、a_i 三档一起分层。
#
# ---- 分层策略（10 组，从边界铺到顶格）----
#   点 1  边界层：T=10, n=2 下界 + 权值上下界（2..1e7）；答案恒 1（删 1 剩 1）。
#   点 2  小规模（n<=300, a<=2000）：4 团 / 素数孤立 / 两不连通团 / 36 桥+孤立 / 全相等 /
#         素数+4 团混合 / 一般随机 / 素数与孤立合数点。
#   点 3  小规模结构（n<=300, a<=2000）：hub 900 + 4/9/25 三团（删 hub 得 m）、
#         星形（中心 30030）、全相等 432（2^4*3^3）、链、多见证多分量。
#   点 4  中规模（n<=5000, a<=30000）：随机、4 团/9 团均分+36 桥、6 团、全相等大值、
#         半素数随机、连续值域、四个平行团（断言 100）。
#   点 5  中规模顶格（n≈5000, a<=30000）：均分团+36 桥（断言 2499）、纯随机、大团、连续偶数。
#   点 6  大规模 52% 档（n=1e5, a<=1e5）：随机、4 团、6 团、全相等 30030、素数孤立、
#         4/9 均分团+36 桥（断言 49999）、半素数随机、混合、小值域随机。
#   点 7  大规模结构（n=1e5, a<=1e5）：4/9 均分团+36 桥（断言 49998）、4/25 均分团+100 桥
#         （断言 49998）、素数孤立+4 团（断言 49999）、四个平行团各 25000（断言 25000）。
#   点 8  大规模随机全权（n=1e5, a<=1e7）：随机、1e7 半半、全偶、6q 海量见证、大素数孤立、
#         4/9 均分团（断言 50000）。
#   点 9  顶格（T=10, n=1e5, a<=1e7）：5 组全相等 9699690（8 素因子=团）、5 组 6q（断言全 99999）。
#   点 10 顶格混合（n=1e5, a<=1e7）：小素数乘积、1e7 全相等、9699690 全相等、170170 全相等、
#         混合、随机、4 团、6q、4/9 均分团+36 桥（断言 49999）。
#
#   结构构造的「互不串门」保证（用于断言）：取素数 q>=11，则
#     4q 的见证集 = {4, 2q}，9q = {9, 3q}，25q = {25, 5q}，49q = {49, 7q}，
#   两两交集为空（p,q>=11 时 2p=3q、3p=5q 等均无解），故各团内部两两有边、跨团无边；
#   桥点 36（见证 {4,9,6}）或 100（见证 {4,25,10}）恰把两团连起来，删除它即切分。
#   全相等值 v（合数）构成团，删一个点答案 = n-1。
#
#   所有随机均固定种子，完全可复现；生成器只用 O(n) 循环（无 O(n²)）。

from cyaron import IO  # 引入CYaRon的库

from bisect import bisect_left, bisect_right
import os
import random
import sys

MAXN = 100000      # n 上限
MAXA = 10000000    # a_i 上限
MAXA52 = 100000    # 52% 档 a_i 上限
MAXA16 = 2000      # 16% 档 a_i 上限
MAXA40 = 30000     # 40% 档 a_i 上限
MAXT = 10          # T 上限

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def sieve(limit):
    """返回 <= limit 的素数列表（bytearray 切片筛）。"""
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"
    i = 2
    while i * i <= limit:
        if flags[i]:
            flags[i * i:: i] = bytearray(len(range(i * i, limit + 1, i)))
        i += 1
    return [v for v in range(limit + 1) if flags[v]]


PRIMES = sieve(2500000)  # 覆盖 4q<=1e7（q<=2.5e6）、6q<=1e7（q<=1.67e6）


def primes_between(lo, hi):
    return PRIMES[bisect_left(PRIMES, lo):bisect_right(PRIMES, hi)]


# 各档「见证团」构造用的素因子池（均 >=11，保证 4p/9q/25r/49s 系列互不串门）
S_P4 = primes_between(11, 500)        # 4p <= 2000
S_P9 = primes_between(11, 222)        # 9p <= 2000
S_P25 = primes_between(11, 80)        # 25p <= 2000
M_P4 = primes_between(11, 7500)       # 4p <= 30000
M_P9 = primes_between(11, 3333)       # 9p <= 30000
H_P4 = primes_between(11, 25000)      # 4p <= 1e5
H_P9 = primes_between(11, 11111)      # 9p <= 1e5
H_P25 = primes_between(11, 4000)      # 25p <= 1e5
H_P49 = primes_between(11, 2040)      # 49p <= 1e5
F_P4 = primes_between(11, 2500000)    # 4p <= 1e7
F_P9 = primes_between(11, 1111111)    # 9p <= 1e7
F_P6 = primes_between(11, 1666666)    # 6p <= 1e7
F_P47 = primes_between(11, 210000)    # 47*p <= 1e7（点 10 混合：小素数 x 大素数）


def cycled(pool, n):
    """把 pool 循环取 n 个（O(n)），允许重复以凑满规模。"""
    assert pool, "空素数池"
    return [pool[i % len(pool)] for i in range(n)]


def write_case(io, tests):
    io.input_writeln(len(tests))
    for arr in tests:
        io.input_writeln(len(arr))
        io.input_writeln(" ".join(map(str, arr)))


def check(point, expected=None):
    """自检：输入结构/范围逐 token 校验 + .out 非空、行数一致、答案范围合法；
    expected 给定时逐组比对（组号从 1 起）。"""
    with open("problem%d.in" % point, encoding="utf-8") as fh:
        tok = fh.read().split()
    assert tok, "点 %d .in 为空" % point
    T = int(tok[0])
    assert 1 <= T <= MAXT, "点 %d T=%d 越界" % (point, T)
    pos = 1
    for g in range(T):                      # 按题面格式解析：每组 n + n 个 a_i
        n = int(tok[pos]); pos += 1
        assert 2 <= n <= MAXN, "点 %d 第 %d 组 n=%d 越界" % (point, g + 1, n)
        group = tok[pos:pos + n]; pos += n
        assert len(group) == n, "点 %d 第 %d 组点数不足" % (point, g + 1)
        for v in group:
            x = int(v)
            assert 2 <= x <= MAXA, "点 %d 第 %d 组 a=%d 越界（题面 2..1e7）" % (point, g + 1, x)
    assert pos == len(tok), "点 %d .in 尾部多余 token" % point
    with open("problem%d.out" % point, encoding="utf-8") as fh:
        outs = fh.read().split()
    assert outs, "点 %d .out 为空（std 缺失或崩溃？）" % point
    assert len(outs) == T, "点 %d .out 行数 %d != T=%d" % (point, len(outs), T)
    nums = [int(v) for v in outs]
    assert all(0 < v <= MAXN for v in nums), "点 %d .out 含非法答案" % point
    if expected:
        for idx, want in expected.items():
            got = nums[idx - 1]
            assert got == want, "点 %d 第 %d 组：期望 %d，得到 %d" % (point, idx, want, got)
    return nums


def make_io(point):
    return IO(file_prefix="problem", data_id=point)  # problem{point}.in / problem{point}.out


SP = SMALL_PRIMES                     # [2,3,5,7,11,...,47]
F_P6_1E5 = primes_between(11, 16666)  # 6p <= 1e5


def gen1():
    """点 1 边界层：T=10, n=2 下界 + 权值上下界；答案恒 1。"""
    io = make_io(1)
    tests = [
        [2, 2],              # 最小权值，gcd=2 非合数 => 无边
        [2, 3],              # 两个最小素数
        [4, 4],              # gcd=4 合数 => 有边（见证 p^2）
        [4, 6],              # gcd=2 无边（见证 4、6 互不共享）
        [4, 9],              # gcd=1 无边
        [6, 9],              # gcd=3 无边
        [4, 8],              # gcd=4 有边
        [9, 27],             # gcd=9 有边
        [MAXA, MAXA],        # 权值顶格：gcd=1e7=2^7*5^7 合数 => 有边
        [MAXA, MAXA - 1],    # 顶格值 + 9999999
    ]
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(1, {i: 1 for i in range(1, 11)})  # n=2：删 1 剩 1，恒 1


def gen2():
    """点 2 小规模（n<=300, a<=2000）：团/孤立/双团/桥/全相等/链/星形。"""
    io = make_io(2)
    random.seed(173602)
    tests = []
    tests.append([4 * (i + 1) for i in range(50)])                 # 4 团 50 -> 49
    tests.append([SP[i % len(SP)] for i in range(40)])             # 素数孤立 -> 1
    tests.append([4 * p for p in S_P4[:12]] + [9 * p for p in S_P9[:8]])  # 双团 12/8 -> 11
    tests.append([20, 28, 44, 52, 68] + [45, 63, 99, 117, 153] + [36, 101])  # 双 5 团 + 36 桥 -> 5
    tests.append([1000] * 30)                                      # 全相等团 30 -> 29
    tests.append([random.choice([2, 3, 5, 7, 11, 13]) for _ in range(60)]
                 + [4 * random.randint(1, 12) for _ in range(60)])  # 混合
    tests.append([random.randint(2, MAXA16) for _ in range(300)])   # 一般随机
    chain_p = [11, 13, 17, 19, 23, 29, 31]
    tests.append([2 * chain_p[i] * chain_p[i + 1] for i in range(6)])  # 链 6 -> 3
    leaves = [p * q for i, p in enumerate([2, 3, 5, 7]) for q in [2, 3, 5, 7][i + 1:]]
    tests.append([210] + leaves)                                   # 星形中心 210=2*3*5*7 -> 1
    tests.append([2, 3, 5, 7, 11, 13, 17, 19, 12, 18])             # {12,18} + 孤立 -> 1
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(2, {1: 49, 2: 1, 3: 11, 4: 5, 5: 29, 8: 3, 9: 1, 10: 1})


def gen3():
    """点 3 小规模结构（n<=300, a<=2000）：hub 三团/星形/全相等/链/多分量/复杂桥。"""
    io = make_io(3)
    tests = []
    tests.append([900] + [4 * p for p in S_P4[:12]] + [9 * p for p in S_P9[:8]]
                 + [25 * p for p in S_P25[:4]])                    # hub 900 连三团 -> 12
    leaves = [p * q for i, p in enumerate([2, 3, 5, 7]) for q in [2, 3, 5, 7][i + 1:]]
    tests.append([210] + leaves)                                   # 星形（中心 210）-> 1
    tests.append([432] * 80)                                       # 全相等 432（2^4*3^3）团 -> 79
    chain_p = [11, 13, 17, 19, 23, 29, 31]
    tests.append([2 * chain_p[i] * chain_p[i + 1] for i in range(6)])  # 链 -> 3
    tests.append([4 * p for p in [11, 13, 17, 19, 23, 29]]
                 + [9 * p for p in [11, 13, 17, 19]] + [25 * p for p in [11, 13, 17]])  # 三团 6/4/3 -> 5
    tests.append([4 * p for p in S_P4[:20]] + [2, 3, 5, 7, 11, 13])    # 大团+孤立 -> 19
    tests.append([36] + [4 * p for p in S_P4[:8]] + [9 * p for p in S_P9[:8]] + [30, 42])  # 桥+两团+30-42 -> 8
    tests.append([6 * (i + 1) for i in range(60)])                 # 6 团 60 -> 59
    tests.append([4, 8, 12] + [9, 18, 27] + [25, 50, 75] + [2, 3, 5, 7])  # 多分量混合
    tests.append([49 * p for p in S_P25[:8]] + [121 * p for p in S_P25[:2]] + [6, 66])  # 平行团
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(3, {1: 12, 2: 1, 3: 79, 4: 3, 5: 5, 6: 19, 7: 8, 8: 59})


def gen4():
    """点 4 中规模（n<=5000, a<=30000）：随机/双团+桥/6 团/全相等/平行团。"""
    io = make_io(4)
    random.seed(173604)
    tests = []
    tests.append([random.randint(2, MAXA40) for _ in range(5000)])
    tests.append([4 * random.randint(1, 7000) for _ in range(2500)]
                 + [9 * random.randint(1, 3000) for _ in range(2500)])
    tests.append([6 * random.randint(1, 5000) for _ in range(4999)] + [2])   # 6 团 + 孤立 -> 4998
    tests.append([2310] * 3000 + [2, 3, 5, 7])                     # 全相等团 + 4 孤立 -> 2999
    tests.append([random.choice(SP) * random.choice(SP) for _ in range(5000)])
    tests.append([4 * p for p in cycled(M_P4, 2400)] + [9 * p for p in cycled(M_P9, 2400)]
                 + [36] + [101, 103, 107, 109, 113, 127, 131, 137, 139, 149])  # 2400/2400 + 桥 -> 2400
    tests.append(list(range(2, 5002)))                             # 连续值域
    tests.append([2 * (i + 1) for i in range(4999)] + [3])
    tests.append([4] * 100 + [9] * 100 + [25] * 100 + [49] * 100 + [121] * 100 + [2, 3, 5, 7])  # -> 100
    tests.append([random.randint(2, MAXA40) for _ in range(4999)] + [MAXA40])
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(4, {3: 4998, 4: 2999, 6: 2400, 9: 100})


def gen5():
    """点 5 中规模顶格（n≈5000, a<=30000）：均分团+桥/随机/大团/连续偶数。"""
    io = make_io(5)
    random.seed(173605)
    half = (5000 - 2) // 2
    tests = []
    tests.append([4 * p for p in cycled(M_P4, half)] + [9 * p for p in cycled(M_P9, half)]
                 + [36, 101])                                      # -> 2499
    tests.append([random.randint(2, MAXA40) for _ in range(5000)])
    tests.append([6 * random.randint(1, 5000) for _ in range(5000)])   # 6 团 -> 4999
    tests.append([2 * (i + 1) for i in range(4998)] + [9, 25])
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(5, {1: half, 3: 4999})


def gen6():
    """点 6 大规模 52% 档（n=1e5, a<=1e5）。"""
    io = make_io(6)
    random.seed(173606)
    half = (MAXN - 2) // 2
    tests = []
    tests.append([random.randint(2, MAXA52) for _ in range(MAXN)])
    tests.append([4 * p for p in cycled(H_P4, MAXN)])              # 4 团 -> 99999
    tests.append([6 * p for p in cycled(F_P6_1E5, MAXN)])          # 6 团 -> 99999
    tests.append([30030] * MAXN)                                   # 全相等团 -> 99999
    tests.append([SP[i % len(SP)] for i in range(MAXN)])           # 素数孤立 -> 1
    tests.append([4 * p for p in cycled(H_P4, half)] + [9 * p for p in cycled(H_P9, half)]
                 + [36, 101])                                      # -> 49999
    tests.append([random.choice(SP) * random.choice(SP) for _ in range(MAXN)])
    tests.append([4 * random.randint(1, 25000) for _ in range(MAXN // 2)]
                 + [9 * random.randint(1, 11111) for _ in range(MAXN - MAXN // 2)])
    tests.append([random.randint(2, MAXA16) for _ in range(MAXN)])
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(6, {2: 99999, 3: 99999, 4: 99999, 5: 1, 6: half})


def gen7():
    """点 7 大规模结构（n=1e5, a<=1e5）：均分团+桥/孤立+团/四个平行团。"""
    io = make_io(7)
    random.seed(173607)
    half = (MAXN - 4) // 2
    tests = []
    tests.append([4 * p for p in cycled(H_P4, half)] + [9 * p for p in cycled(H_P9, half)]
                 + [36, 101, 103, 107])                           # 2*half+4 = 1e5 -> half
    tests.append([4 * p for p in cycled(H_P4, half)] + [25 * p for p in cycled(H_P25, half)]
                 + [100, 101, 103, 107])                          # 4 团/25 团 + 100 桥 -> half
    tests.append([SP[i % len(SP)] for i in range(MAXN // 2)]
                 + [4 * p for p in cycled(H_P4, MAXN - MAXN // 2)])  # 孤立 + 4 团 -> 49999
    q = MAXN // 4
    tests.append([4 * p for p in cycled(H_P4, q)] + [9 * p for p in cycled(H_P9, q)]
                 + [25 * p for p in cycled(H_P25, q)] + [49 * p for p in cycled(H_P49, q)])  # -> 25000
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(7, {1: half, 2: half, 3: MAXN // 2 - 1, 4: q})


def gen8():
    """点 8 大规模随机全权（n=1e5, a<=1e7）。"""
    io = make_io(8)
    random.seed(173608)
    tests = []
    for _ in range(5):
        tests.append([random.randint(2, MAXA) for _ in range(MAXN)])
    tests.append([random.randint(2, MAXA) for _ in range(MAXN // 2)] + [MAXA] * (MAXN // 2))
    tests.append([2 * random.randint(1, 5000000) for _ in range(MAXN)])       # 全偶
    tests.append([6 * p for p in cycled(F_P6, MAXN)])                        # 6 团 -> 99999
    tests.append([F_P6[i % len(F_P6)] for i in range(MAXN)])                  # 大素数孤立 -> 1
    tests.append([4 * p for p in cycled(F_P4, MAXN // 2)]
                 + [9 * p for p in cycled(F_P9, MAXN - MAXN // 2)])           # 均分团 -> 50000
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(8, {8: 99999, 9: 1, 10: MAXN // 2})


def gen9():
    """点 9 顶格（T=10, n=1e5, a<=1e7）：全相等 9699690 与 6q 见证洪泛。"""
    io = make_io(9)
    random.seed(173609)
    tests = []
    for _ in range(5):
        tests.append([9699690] * MAXN)          # 8 素因子、28 对见证 -> 99999
    for _ in range(5):
        tests.append([6 * p for p in cycled(F_P6, MAXN)])  # -> 99999
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(9, {i: 99999 for i in range(1, 11)})


def gen10():
    """点 10 顶格混合（n=1e5, a<=1e7）：小素数乘积/全相等/随机/均分团+桥。"""
    io = make_io(10)
    random.seed(173610)
    pool = [p * q for i, p in enumerate(SP) for q in SP[i:] if p * q <= MAXA]
    half = (MAXN - 2) // 2
    tests = []
    tests.append([random.choice(pool) for _ in range(MAXN)])
    tests.append([random.choice(pool) for _ in range(MAXN)])
    tests.append([9699690] * MAXN)                        # -> 99999
    tests.append([MAXA] * MAXN)                           # 1e7=2^7*5^7 -> 99999
    tests.append([2 * 5 * 7 * 11 * 13 * 17] * MAXN)       # 170170 -> 99999
    tests.append([random.choice(SP) * random.choice(F_P47) for _ in range(MAXN)])
    tests.append([random.randint(2, MAXA) for _ in range(MAXN)])
    tests.append([4 * random.randint(1, 2500000) for _ in range(MAXN)])  # 4 团 -> 99999
    tests.append([6 * p for p in cycled(F_P6, MAXN)])     # -> 99999
    tests.append([4 * p for p in cycled(F_P4, half)] + [9 * p for p in cycled(F_P9, half)]
                 + [36, 101])                             # -> half
    write_case(io, tests)
    io.output_gen("../std")
    io.close()  # 落盘（cyaron 输出有缓冲，须 flush/close 后再自检）
    check(10, {3: 99999, 4: 99999, 5: 99999, 8: 99999, 9: 99999, 10: half})


def main():
    # 守卫 1：std 必须存在且可执行，否则 output_gen 会静默产出 0 字节 .out
    std = os.path.abspath("../std")
    if not (os.path.isfile(std) and os.access(std, os.X_OK)):
        sys.exit("错误：未找到可执行 std（%s），请先编译："
                 "g++ -O2 -std=c++17 std.cpp -o std" % std)
    print("std: %s" % std)

    for point, gen in enumerate([gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10], 1):
        for suf in (".in", ".out"):
            path = "problem%d%s" % (point, suf)
            if os.path.exists(path):
                os.remove(path)
        gen()
        print("problem%-2d: 生成完成" % point)


if __name__ == "__main__":
    main()
