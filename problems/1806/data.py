#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1806「计算器」造数据脚本 (10 组, 分层: 边界/小/中/大/顶格)

输入格式: 第一行 N, 接下来 N 行 `type y z P` (type∈{1,2,3})
  1: y^z mod P
  2: y^x ≡ z (mod P) 的最小非负整数 x, 无解输出 Math Error
  3: C(z,y) mod P

数据规模分层 (依据题面表格, 见 content.md):
  problem1  : 题面样例 (6 组)
  problem2  : 边界, type1 极小值 (y=0,z=0,P=2 等)
  problem3  : type1 小 (N=50, y,z,P ≤ 1e3)                  [对应 5~10 行]
  problem4  : type1 顶格 (N=500, y,z,P ≤ 1e9)                [对应 1~4 行]
  problem5  : type2 小 (N=10, y,z ≤ 1e3, P ≤ 1e9, 含合数)     [对应 5~10 行]
  problem6  : type2 中 (N=30, y,z ≤ 1e7, P 质数 ≤ 1e9)        [对应 11~16 行]
  problem7  : type2 大 (N=50, y,z ≤ 1e6, P ≤ 1e9, 含合数)     [对应 17~20 行]
  problem8  : type3 小 (N=20, y,z ≤ 1e3, P ≤ 1e3)
  problem9  : type3 大 (N=30, y,z ≤ 1e9, P 满足 p_i^{a_i} ≤ 1e5)
  problem10 : 混合顶格 (50×type1 + 50×type2 + 50×type3)

生成器只用 pow() 等 O(log) 运算, 无 O(n^2) 循环; std 输出由 subprocess 显式跑出并断言非空/行数正确。
"""
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD_CPP = os.path.join(HERE, "std.cpp")
BIN = os.path.join(HERE, ".std_bin")

random.seed(1806)

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
                157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
                239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
                421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
                509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
                613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
                821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
                919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

BIG_PRIMES = [999999937, 999999893, 999999883, 999999797, 999999761, 999999757,
              999999751, 999999739, 999999733, 1000003, 9999991, 999983, 999979,
              99991, 99989, 65537, 15121]

# 合数模数 (质因数幂均 ≤ 1e5, 满足题面 100% 保证)
COMPOSITES = [
    4, 8, 9, 12, 16, 24, 25, 27, 32, 36, 48, 49, 64, 81, 100, 121, 128, 243, 256, 512,
    625, 729, 1000, 1024, 2187, 4096, 6561, 10000, 65536, 59049, 100000,
    999999999,          # 3^4 * 37 * 333667
    1000000000,         # 2^9 * 5^9
    991283456,          # 2^8 * 3872201 (仅用于 type1/type2 模数)
    290117737,          # 3^10 * 17^3
    999810009,          # 99991 * 3^2 * 11 * 101  (若 99991 为质数)
]


# type3 专用模数: 合数且每个质因数幂 ≤ 1e5 (满足题面 100% 保证)
TYPE3_COMPOSITES = [990969856, 892879929, 290117737, 999810009, 655294464,
                    999790011, 781171875, 65536, 59049, 99991 - 2]
# type3 专用质数模数 (≤ 1e5 走前缀表; > 1e5 走 Lucas 兜底)
TYPE3_PRIMES = [99991, 99989, 65537, 15121, 997, 991, 13, 7, 999999937, 999999893]


def factorize(n):
    f = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            pk = 1
            while n % d == 0:
                n //= d
                pk *= d
            f.append((d, pk))
        d += 1
    if n > 1:
        f.append((n, n))
    return f


def is_prime(n):
    return n >= 2 and len(factorize(n)) == 1 and factorize(n)[0][0] == n


def compile_std():
    for cxx in ("g++-16", "g++", "clang++"):
        path = shutil.which(cxx)
        if not path:
            continue
        r = subprocess.run([path, "-O2", "-std=c++17", "-o", BIN, STD_CPP],
                           capture_output=True, text=True)
        if r.returncode == 0:
            print("[compile] %s -O2 -std=c++17 -> %s" % (cxx, os.path.basename(BIN)))
            return
        print("[compile] %s failed: %s" % (cxx, r.stderr.strip().splitlines()[:1]))
    raise SystemExit("no working C++ compiler")


def run_std(inp):
    r = subprocess.run([BIN], input=inp, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit("std runtime error: %s" % r.stderr[:500])
    return r.stdout


def check_forward(queries, lines):
    """正向单点断言 (O(log), 非 brute/非对拍): type1 重算幂; type2 把答案代回验证 y^x≡z (mod P)"""
    for (t, y, z, P), s in zip(queries, lines):
        if t == 1:
            assert int(s) == pow(y, z, P), "type1 wrong: %d^%d mod %d = %s" % (y, z, P, s)
        elif t == 2 and s != "Math Error":
            x = int(s)
            assert x >= 0 and pow(y, x, P) == z % P, \
                "type2 not a solution: %d^%d mod %d != %d" % (y, x, P, z % P)


def emit(idx, queries, note):
    """写 problem{idx}.in 并用 std 跑出 problem{idx}.out, 断言输出非空/行数正确"""
    inp = "%d\n" % len(queries) + "".join("%d %d %d %d\n" % q for q in queries)
    out = run_std(inp)
    lines = out.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == len(queries), "problem%d: %d lines vs %d queries" % (idx, len(lines), len(queries))
    assert all(s.strip() != "" for s in lines), "problem%d: empty output line" % idx
    check_forward(queries, lines)
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "problem%d.in" % idx), "w") as f:
        f.write(inp)
    with open(os.path.join(DATA, "problem%d.out" % idx), "w") as f:
        f.write("\n".join(lines) + "\n")
    types = sorted(set(q[0] for q in queries))
    print("[data] problem%d: N=%-4d types=%s  in=%dB out=%dB   %s"
          % (idx, len(queries), types, len(inp), len(out), note))
    return lines


# ---------------------------------------------------------------- 各测试点
def q1(y, z, P):
    return (1, y, z, P)


def q2(y, z, P):
    return (2, y, z, P)


def q3(y, z, P):
    return (3, y, z, P)


def make_t1_small(n, hi):
    qs = []
    for _ in range(n):
        qs.append(q1(random.randint(0, hi), random.randint(0, hi), random.randint(2, hi)))
    return qs


def make_t1_max(n):
    qs = []
    for _ in range(n):
        y = random.randint(0, 10 ** 9)
        z = random.randint(0, 10 ** 9)
        P = random.choice([random.randint(2, 10 ** 9), random.choice(BIG_PRIMES),
                           random.choice(COMPOSITES), 10 ** 9])
        P = min(max(P, 2), 10 ** 9)
        qs.append(q1(y, z, P))
    return qs


def make_t2_solvable(y_hi, P, cnt):
    """构造有解询问: z = y^x mod P"""
    out = []
    for _ in range(cnt):
        y = random.randint(1, y_hi)
        x = random.randint(0, 10 ** 5)
        out.append(q2(y, pow(y, x, P), P))
    return out


def lucas_cost(n, m, p):
    """估计 Lucas 逐位直接乘积的乘法次数 (std 中质数 P>4e6 分支的代价)"""
    c = 0
    while n or m:
        a, b = n % p, m % p
        if b > a:
            return c
        c += min(b, a - b)
        n //= p
        m //= p
    return c


def check_type3_constraints(all_qs):
    for t, y, z, P in all_qs:
        if t != 3:
            continue
        f = factorize(P)
        if len(f) > 1 or f[0][0] != P:      # 合数
            for p, pk in f:
                assert pk <= 10 ** 5, "composite P=%d has prime power %d > 1e5" % (P, pk)
        else:                                # 质数: 保证 std 兜底分支代价可接受
            assert P <= 4 * 10 ** 6 or lucas_cost(z, y, P) <= 2 * 10 ** 6, \
                "prime P=%d y=%d z=%d too expensive" % (P, y, z)


def main():
    compile_std()
    all_qs = []

    # 1. 样例
    sample = [q2(2, 3, 4), q3(2, 7, 9), q2(1, 2, 9), q3(1, 6, 7), q1(5, 3, 7), q1(9, 2, 8)]
    got = emit(1, sample, "题面样例")
    want = ["Math Error", "3", "Math Error", "6", "6", "1"]
    assert got == want, "样例输出不一致: %s != %s" % (got, want)
    print("[check] problem1 输出与题面样例逐行一致 OK")
    all_qs += sample

    # 2. 边界 (type1 极小值)
    b = [q1(0, 0, 5), q1(0, 1000000000, 999999937), q1(1, 0, 2), q1(2, 0, 1000000000),
         q1(1000000000, 1000000000, 1000000000), q1(999999999, 999999999, 999999937),
         q1(2, 1, 2), q1(3, 5, 2), q1(7, 13, 1000000000), q1(999999937, 2, 999999937)]
    all_qs += b
    emit(2, b, "边界: 0^0 / 0^z / z=0 / P=2 / 顶格值")

    # 3. type1 小
    q = make_t1_small(50, 10 ** 3)
    all_qs += q
    emit(3, q, "type1 小: y,z,P ≤ 1e3")

    # 4. type1 顶格
    q = make_t1_max(500)
    all_qs += q
    emit(4, q, "type1 顶格: N=500, y,z,P ≤ 1e9")

    # 5. type2 小 (P 可为合数)
    q = [q2(2, 3, 4), q2(1, 2, 9), q2(3, 1, 7), q2(5, 6, 7), q2(2, 4, 8), q2(10, 100, 999),
         q2(7, 1, 1000000000), q2(0, 0, 1000000000), q2(0, 5, 1000000000), q2(2, 0, 999999937)]
    all_qs += q
    emit(5, q, "type2 小: y,z ≤ 1e3, P ≤ 1e9 (含合数/无解/0^0)")

    # 6. type2 中 (P 质数)
    q = []
    for P in [9999991, 1000003, 999983, 99991]:      # z = pow(y,x,P) < P ≤ 1e7
        q += make_t2_solvable(min(10 ** 7, P - 1), P, 6)
    for _ in range(6):                               # P 顶格质数, z ≤ 1e7 随机
        q.append(q2(random.randint(1, 10 ** 7), random.randint(0, 10 ** 7), 999999937))
    # 无解 / 边界
    q += [q2(0, 5, 999999937), q2(2, 0, 999999937), q2(1, 9999999, 999999937),
          q2(9999990, 123456, 9999991), q2(3, 1, 999999937)]
    q = q[:30]
    all_qs += q
    emit(6, q, "type2 中: y,z ≤ 1e7, P 质数 ≤ 1e9")

    # 7. type2 大 (P 含合数 -> exBSGS)
    q = []
    for P in [1000000000, 999999999, 991283456, 290117737, 4, 8, 9, 12, 65536, 999999937]:
        q += make_t2_solvable(min(10 ** 6, P - 1), P, 4)
    q += [q2(2, 3, 4), q2(2, 8, 8), q2(0, 0, 9), q2(0, 1, 9), q2(5, 999998, 7),
          q2(1, 2, 9), q2(2, 4, 8), q2(3, 999999, 1000), q2(2, 999998, 999999),
          q2(0, 7, 1000000000)]
    q = q[:50]
    all_qs += q
    emit(7, q, "type2 大: y,z ≤ 1e6, P ≤ 1e9 (合数 exBSGS, 含 z>P 取模)")

    # 8. type3 小 + 手算已知答案断言 (y,z ≤ 1e3, P ≤ 1e3)
    known = [
        (q3(2, 7, 9), 3),        # C(7,2)=21  mod 9  = 3
        (q3(3, 10, 8), 0),       # C(10,3)=120 mod 8 = 0
        (q3(5, 10, 100), 52),    # C(10,5)=252 mod 100 = 52
        (q3(2, 4, 4), 2),        # C(4,2)=6   mod 4  = 2
        (q3(3, 9, 8), 4),        # C(9,3)=84  mod 8  = 4
        (q3(1, 6, 7), 6),        # C(6,1)=6   mod 7  = 6
        (q3(2, 5, 7), 3),        # C(5,2)=10  mod 7  = 3
        (q3(10, 20, 999), 940),  # C(20,10)=184756 mod 999 = 940
        (q3(5, 13, 1000), 287),  # C(13,5)=1287 mod 1000 = 287
        (q3(7, 15, 100), 35),    # C(15,7)=6435 mod 100 = 35
        (q3(6, 12, 49), 42),     # C(12,6)=924 mod 49 = 42
        (q3(3, 11, 121), 44),    # C(11,3)=165 mod 121 = 44
        (q3(100, 100, 97), 1),   # C(100,100)=1 mod 97 = 1
        (q3(5, 2, 7), 0),        # y>z  -> 0
        (q3(0, 5, 9), 1),        # C(5,0)=1
        (q3(1, 1000, 1000), 0),  # C(1000,1)=1000 mod 1000 = 0
    ]
    q = []
    for _ in range(16):
        z = random.randint(0, 10 ** 3)
        y = random.randint(0, z)
        P = random.choice(SMALL_PRIMES + TYPE3_COMPOSITES[:8] + [4, 8, 9, 12, 16, 25, 27, 49, 121, 128, 243, 256, 512])
        q.append(q3(y, z, P))
    q += [k[0] for k in known]
    all_qs += q
    got = emit(8, q, "type3 小: y,z ≤ 1e3, P ≤ 1e3 (含手算已知答案)")
    for (qq, want), got_s in zip(known, got[-len(known):]):
        assert got_s == str(want), "type3 known wrong: C(%d,%d) mod %d = %s, want %d" \
            % (qq[2], qq[1], qq[3], got_s, want)
    print("[check] problem8 中 %d 组手算答案 (C_z^y mod P) 全部一致 OK" % len(known))

    # 9. type3 大
    q = []
    for _ in range(20):
        z = random.randint(0, 10 ** 9)
        y = random.randint(0, z)
        P = random.choice([990969856, 892879929, 290117737, 999810009, 655294464,
                           999790011, 781171875, 65536, 59049, 99991, 99989, 65537, 15121])
        q.append(q3(y, z, P))
    q += [q3(0, 10 ** 9, 990969856), q3(10 ** 9, 10 ** 9, 999810009),
          q3(500000, 10 ** 9, 781171875), q3(1, 10 ** 9, 655294464),
          q3(999999, 10 ** 9, 999999937), q3(3, 10 ** 8, 999999937),
          q3(1000000000, 10 ** 9 - 1, 99991), q3(12345, 987654321, 999999893),
          q3(50000, 999999999, 999999937), q3(99999, 10 ** 9, 999999893)]
    q = q[:30]
    all_qs += q
    emit(9, q, "type3 大: y,z ≤ 1e9, P 质因数幂 ≤ 1e5 (含质数 P 大值兜底)")

    # 10. 混合顶格
    q = make_t1_max(50)
    for P in [1000000000, 999999999, 991283456, 999999937, 9999991]:
        q += make_t2_solvable(min(10 ** 6, P - 1), P, 10)
    for _ in range(50):
        z = random.randint(0, 10 ** 9)
        y = random.randint(0, z)
        P = random.choice([990969856, 892879929, 290117737, 999810009, 655294464,
                           999790011, 781171875, 65536, 59049, 99991, 65537])
        q.append(q3(y, z, P))
    q = q[:150]
    all_qs += q
    emit(10, q, "混合顶格: 50×type1 + 50×type2 + 50×type3")

    check_type3_constraints(all_qs)
    print("[check] 所有 type3 询问满足 P_i^{a_i} ≤ 1e5 (合数) / 质数 P 兜底条件 OK")

    if os.path.exists(BIN):
        os.remove(BIN)
        print("[clean] 已删除编译产物 %s" % os.path.basename(BIN))


if __name__ == "__main__":
    main()
