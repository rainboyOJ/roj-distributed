#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data.py  --  一本通 1798 《递推数列》 数据生成器

题面: f(i) = (a*f(i-1)+b)/(c*f(i-1)+d) mod p, 求 f(n), 多组数据.
范围: 1<=t<=1e4, 0<=n<=1e18, 2<=p<=1e9, 0<=|f0|,|a|,|b|,|c|,|d|<p, 逆元存在.

生成 10 组 .in/.out 到 data/ 子目录 (problem1.in/.out .. problem10.in/.out).
.out 由编译好的 std 通过 subprocess 显式生成, 生成后断言非空且行数 == t.

合法性: 生成时用矩阵快速幂 (O(log n)) 校验最终 v_n 与 p 互素 (逆元存在),
        并要求 det = ad-bc != 0 (mod p). 失败则重抽该组.
        取 p 为素数可进一步降低风险; 小 n 组会额外校验中间项非零.
"""
import os
import sys
import math
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")

rng = random.Random(202401798)


# ------------------------------------------------------------------ primes ---
def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True


def sieve(n):
    bs = bytearray([1]) * (n + 1)
    bs[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
    return [i for i in range(n + 1) if bs[i]]


P100 = sieve(100)                 # p <= 100
P1000 = sieve(1000)               # p <= 1000
P1E6 = sieve(1000000)             # p <= 1e6
PLARGE = [p for p in (999999937, 999999893, 999999883, 999999797,
                      999999761, 999999757, 999999751, 999999739)
          if is_prime(p)]


# ------------------------------------------------------------- matrix utils ---
def matmul(A, B, p):
    return [[(A[i][0] * B[0][j] + A[i][1] * B[1][j]) % p for j in range(2)]
            for i in range(2)]


def matpow(M, e, p):
    R = [[1, 0], [0, 1]]
    while e:
        if e & 1:
            R = matmul(R, M, p)
        M = matmul(M, M, p)
        e >>= 1
    return R


def is_valid(f0, a, b, c, d, n, p):
    """校验该组数据满足题面'逆元存在'的保证 (只看最终除法)."""
    f0 %= p; a %= p; b %= p; c %= p; d %= p
    if (a * d - b * c) % p == 0:          # 退化矩阵, 避开
        return False
    if n == 0:
        return True                        # v_0 = 1, 恒可逆
    if n <= 4096:                          # 小 n: 逐项校验所有中间分母
        u, v = f0, 1
        for _ in range(n):
            u, v = (a * u + b * v) % p, (c * u + d * v) % p
            if v == 0 or math.gcd(v, p) != 1:
                return False
        return True
    R = matpow([[a, b], [c, d]], n, p)
    v = (R[1][0] * f0 + R[1][1]) % p
    return v != 0 and math.gcd(v, p) == 1


def rand_coef(p, rng):
    """|x| < p 的随机整数 (含负)."""
    v = rng.randrange(p)
    if rng.random() < 0.45:
        v = -v
    return v


def gen_case(p, n, rng, pool=None):
    """随机生成一个满足约束的单组数据 (f0,a,b,c,d,n,p)."""
    for _ in range(2000):
        if pool is None:
            f0 = rand_coef(p, rng); a = rand_coef(p, rng)
            b = rand_coef(p, rng); c = rand_coef(p, rng); d = rand_coef(p, rng)
        else:
            f0, a, b, c, d = (rng.choice(pool) for _ in range(5))
        if is_valid(f0, a, b, c, d, n, p):
            return (f0, a, b, c, d, n, p)
    raise RuntimeError("gen_case failed for p=%d n=%d" % (p, n))


def rand_n(lo, hi, rng):
    return rng.randrange(lo, hi + 1)


# ------------------------------------------------------------------- layers ---
def build_layers():
    L = []  # (name, cases)

    # 1) 最小边界: t=1, n=0, p=2
    L.append(("problem1", [gen_case(2, 0, rng)]))

    # 2) 10% 层: t<=10, n<=100, p<=100
    L.append(("problem2",
              [gen_case(rng.choice(P100), rand_n(0, 100, rng), rng)
               for _ in range(10)]))

    # 3) 40% 层: t<=10, p<=1000, n 可很大
    L.append(("problem3",
              [gen_case(rng.choice(P1000), rand_n(0, 10 ** 18, rng), rng)
               for _ in range(10)]))

    # 4) n 边界: n in {0,1,2}
    c4 = []
    for n in (0, 1, 2, 0, 1, 2):
        c4.append(gen_case(rng.choice(P1000), n, rng))
    L.append(("problem4", c4))

    # 5) 小 p + 大 n (周期性压力)
    L.append(("problem5",
              [gen_case(rng.choice(P100), rand_n(0, 10 ** 18, rng), rng)
               for _ in range(20)]))

    # 6) 中等: t=100, p<=1e6
    L.append(("problem6",
              [gen_case(rng.choice(P1E6), rand_n(0, 10 ** 18, rng), rng)
               for _ in range(100)]))

    # 7) t=1000, p<=1e9
    L.append(("problem7",
              [gen_case(rng.choice(PLARGE), rand_n(0, 10 ** 18, rng), rng)
               for _ in range(1000)]))

    # 8) 最大 t=1e4, p<=1e9, n<=1e18
    L.append(("problem8",
              [gen_case(rng.choice(PLARGE), rand_n(0, 10 ** 18, rng), rng)
               for _ in range(10000)]))

    # 9) 顶格单组: t=1, n=1e18, p=999999937, 系数取边界
    P = 999999937
    pool = [P - 1, -(P - 1), 1, -1, 0, P - 2, -(P - 2)]
    L.append(("problem9", [gen_case(P, 10 ** 18, rng, pool=pool)]))

    # 10) 顶格满: t=1e4, n=1e18, p=999999937
    L.append(("problem10",
              [gen_case(P, 10 ** 18, rng) for _ in range(10000)]))

    return L


# --------------------------------------------------------------------- main ---
def main():
    if not os.path.exists(STD):
        print("ERROR: std binary not found; compile first", file=sys.stderr)
        sys.exit(1)
    os.makedirs(DATA_DIR, exist_ok=True)

    layers = build_layers()
    for name, cases in layers:
        in_path = os.path.join(DATA_DIR, name + ".in")
        out_path = os.path.join(DATA_DIR, name + ".out")
        with open(in_path, "w") as f:
            f.write("%d\n" % len(cases))
            for (f0, a, b, c, d, n, p) in cases:
                f.write("%d %d %d %d %d %d %d\n" % (f0, a, b, c, d, n, p))
            f.flush()
            os.fsync(f.fileno())

        with open(in_path, "rb") as fin:
            res = subprocess.run([STD], stdin=fin, capture_output=True,
                                 timeout=300)
        if res.returncode != 0:
            print("ERROR: std failed on %s: %s" % (name, res.stderr.decode()),
                  file=sys.stderr)
            sys.exit(1)
        out_bytes = res.stdout
        # 显式落盘 + flush, 避免 0 字节 .out
        with open(out_path, "wb") as f:
            f.write(out_bytes)
            f.flush()
            os.fsync(f.fileno())

        # 断言: .out 非空, 行数 == t, 每行是一个非负整数
        assert len(out_bytes) > 0, "%s: empty .out" % name
        lines = out_bytes.decode().split()
        assert len(lines) == len(cases), \
            "%s: expected %d lines, got %d" % (name, len(cases), len(lines))
        for ln in lines:
            assert ln.isdigit(), "%s: bad output token %r" % (name, ln)
        print("  %-10s t=%-6d p_max=%-10d  in=%d B out=%d B  OK"
              % (name, len(cases), max(c[6] for c in cases),
                 os.path.getsize(in_path), os.path.getsize(out_path)))

    print("all 10 datasets generated into %s" % DATA_DIR)


if __name__ == "__main__":
    main()
