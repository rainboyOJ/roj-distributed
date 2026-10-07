#!/usr/bin/env python
# 一本通 1697《深意》数据生成器
#
# 题面范围：len(t) <= len(s) <= 100000，n <= 10，s/t 仅小写字母。
# 分层（10 个测试点，n 与 |s| 都从最小铺到顶格）：
#   点1  边界层：n=1，|s|=|t|=1（最小规模），单字符出现
#   点2  边界层：n=2，|s| 极小；含 t 不出现（答案恒 1）与 s==t（答案 2）
#   点3  小规模随机：n=3，|s|<=30，可手算验证；含全同字符、周期重叠结构
#   点4  小规模随机：n=3，|s|<=100，小字母表制造高重叠匹配
#   点5  中等随机：n=5，|s|≈2000（50% 档 len<=1000 上下），26 字母
#   点6  中等随机：n=5，|s|≈1000 顶到 50% 档上限，2 字母表重叠密集
#   点7  大规模随机：n=10（组数顶格），|s|≈10000
#   点8  大规模随机：n=10，|s|≈50000，小字母表（出现次数多）
#   点9  顶格层：n=10，|s|=100000（长度顶格），26 字母随机
#   点10 顶格层：n=10，|s|=100000，最坏结构：单字符全同串 / 短周期 t
#        重叠出现次数最多（≈|s|），答案 2^(出现数) mod p 增长最快
# 每组内 t 长度多样化（1 / 短 / 与 s 同长），确保 KMP 边界都被覆盖。

import random
from cyaron import *

MOD_LIMIT = 100000


def rand_str(n, alpha="abcdefghijklmnopqrstuvwxyz"):
    return "".join(random.choice(alpha) for _ in range(n))


def make_case(a, b, style, alpha):
    """返回 (s, t)，|s|=a, |t|=b"""
    if style == "s==t":
        s = rand_str(a, alpha)
        return s, s
    if style == "t-absent":
        # 构造 t 几乎不出现：s 用 26 字母随机，t 取 12 字母随机串
        s = rand_str(a, alpha)
        t = rand_str(b, "abcdefghijklmnopqrstuvwxyz")
        return s, t
    if style == "periodic":
        # s 为 t 的重复：出现次数最多（顶格最坏结构）
        base = rand_str(b, alpha) if b > 0 else "a"
        s = (base * (a // b + 1))[:a]
        return s, base
    if style == "same-char":
        c = random.choice("abcdefghijklmnopqrstuvwxyz")
        s = c * a
        t = c * b
        return s, t
    if style == "planted":
        # 随机串中植入若干（含重叠）t
        s = list(rand_str(a, alpha))
        if a >= b:
            for _ in range(min(a, 8)):
                st = random.randint(0, a - b)
                s[st:st + b] = list(rand_str(b, alpha))
        t = rand_str(b, alpha)
        return "".join(s), t
    # plain 随机
    return rand_str(a, alpha), rand_str(b, alpha)


def write_point(idx, cases):
    io = IO(file_prefix="problem", data_id=idx)
    io.input_writeln(len(cases))
    for s, t in cases:
        io.input_writeln(s)
        io.input_writeln(t)
    io.output_gen("../std")


random.seed(1697 + 2024)

# ---- 点1 边界层：n=1，最小规模 |s|=|t|=1 ----
write_point(1, [("a", "a")])

# ---- 点2 边界层：n=2，极小规模 + t 不出现 + s==t ----
write_point(2, [
    ("ab", "ab"),            # s==t，答案 2
    ("qwertyuiop", "zxcvbn"), # t 不出现，答案 1
])

# ---- 点3 小规模随机：n=3，|s|<=30，可手算（见 gen-report）----
write_point(3, [
    make_case(30, 3, "periodic", "ab"),
    make_case(29, 2, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(30, 1, "planted", "abc"),
])

# ---- 点4 小规模随机：n=3，|s|<=100，小字母表高重叠 ----
write_point(4, [
    make_case(100, 5, "plain", "ab"),
    make_case(99, 4, "periodic", "ab"),
    make_case(100, 100, "s==t", "abcdefghijklmnopqrstuvwxyz"),
])

# ---- 点5 中等随机：n=5，|s|≈2000（跨 50% 档），26 字母 ----
write_point(5, [
    make_case(2000, 10, "plain", "abcdefghijklmnopqrstuvwxyz"),
    make_case(1999, 1, "periodic", "ab"),
    make_case(2000, 2000, "s==t", "abcdefghijklmnopqrstuvwxyz"),
    make_case(1500, 7, "planted", "abc"),
    make_case(1800, 500, "t-absent", "abcdefghijklmnopqrstuvwxyz"),
])

# ---- 点6 中等随机：n=5，50% 档顶格 |s|<=1000，重叠密集 ----
write_point(6, [
    make_case(1000, 10, "periodic", "ab"),
    make_case(1000, 1, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(999, 3, "plain", "ab"),
    make_case(1000, 4, "planted", "abc"),
    make_case(950, 800, "t-absent", "abcdefghijklmnopqrstuvwxyz"),
])

# ---- 点7 大规模随机：n=10（组数顶格），|s|≈10000 ----
write_point(7, [
    make_case(10000, 26, "plain", "abcdefghijklmnopqrstuvwxyz"),
    make_case(9999, 1, "periodic", "ab"),
    make_case(10000, 500, "planted", "abcdefgh"),
    make_case(10000, 10000, "s==t", "abcdefghijklmnopqrstuvwxyz"),
    make_case(9500, 3000, "t-absent", "abcdefghijklmnopqrstuvwxyz"),
    make_case(10000, 12, "periodic", "ab"),
    make_case(10000, 7, "plain", "ab"),
    make_case(10000, 5, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(10000, 3, "planted", "abc"),
    make_case(8000, 8000, "s==t", "abcdefghijklmnopqrstuvwxyz"),
])

# ---- 点8 大规模随机：n=10，|s|≈50000，小字母表 ----
write_point(8, [
    make_case(50000, 1, "periodic", "ab"),
    make_case(50000, 26, "plain", "abcdefgh"),
    make_case(49999, 2, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(50000, 11, "periodic", "ab"),
    make_case(50000, 1000, "planted", "abc"),
    make_case(48000, 40000, "t-absent", "abcdefghijklmnopqrstuvwxyz"),
    make_case(50000, 9, "plain", "ab"),
    make_case(50000, 500, "planted", "abcde"),
    make_case(46000, 23000, "s==t", "abcdefghijklmnopqrstuvwxyz"),
    make_case(50000, 3, "periodic", "abc"),
])

# ---- 点9 顶格层：n=10，|s|=100000（长度顶格），26 字母随机 ----
write_point(9, [
    make_case(100000, 26, "plain", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 1, "periodic", "ab"),
    make_case(100000, 100000, "s==t", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 17, "planted", "abc"),
    make_case(100000, 4096, "planted", "abcdefgh"),
    make_case(99999, 33333, "s==t", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 100, "plain", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 64, "planted", "abcdefg"),
    make_case(100000, 99999, "t-absent", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 128, "plain", "abcdefghij"),
])

# ---- 点10 顶格层：n=10，|s|=100000 最坏结构（重叠出现次数最大、答案最大）----
write_point(10, [
    make_case(100000, 1, "same-char", "abcdefghijklmnopqrstuvwxyz"),   # 出现 1e5 次
    make_case(100000, 2, "periodic", "ab"),   # 出现 ~1e5 次
    make_case(100000, 3, "periodic", "ab"),
    make_case(100000, 500, "periodic", "ab"),
    make_case(100000, 1, "periodic", "abc"),
    make_case(100000, 50, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 7, "periodic", "abc"),
    make_case(99999, 3, "same-char", "abcdefghijklmnopqrstuvwxyz"),
    make_case(100000, 1000, "periodic", "abc"),
    make_case(100000, 4, "periodic", "ab"),
])

print("done: 10 points")
