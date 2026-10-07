#!/usr/bin/env python
# 一本通 1691《文章评分》数据生成器
# 题面范围：1 <= m <= n <= 200000，字符串只含小写字母。
# 分层设计（10 个测试点，从最小铺到顶格）：
#   点1  边界层：n=1, m=1（最小规模，答案为 1）
#   点2  边界层：n=2 全同字符，m=n（答案为 1 的极端）
#   点3  小随机：n<=200（30% 档），26 字母随机，可手算
#   点4  小随机：n<=200，小字母表(2/3)制造大量重复子串
#   点5  中规模：n<=2000（50% 档），26 字母随机
#   点6  中规模：n<=2000，小字母表 + 周期块拼接（重复结构）
#   点7  大规模：n<=200000（另 20% 档 m<=50），m 小，26 字母随机
#   点8  大规模：n<=200000，m 小，小字母表（重复子串极多，检验去重）
#   点9  顶格层：n=200000, m=100000（n/2，重复窗口多，去重压力最大）
#   点10 顶格层：n=200000, m=200000=n（答案必为 1，最极端）
# 所有数据点均满足 1<=m<=n<=200000，规模不超过题面上限。

import random
from cyaron import *

ALPHA = 'abcdefghijklmnopqrstuvwxyz'

def rand_str(n, k=26):
    """长度 n、字母表前 k 个字符的随机串"""
    return ''.join(random.choice(ALPHA[:k]) for _ in range(n))

def periodic(n, blocks):
    """由给定小块循环拼接成长度 n 的串，制造大量重复子串"""
    pat = ''.join(blocks)
    return (pat * (n // len(pat) + 1))[:n]

def emit(i, n, m, s):
    """生成第 i 组数据：写 problem{i}.in，跑 ../std 生成 problem{i}.out"""
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(n, m)
    io.input_writeln(s)
    io.output_gen("../std")

random.seed(1691)

# ---- 点1：n=1, m=1 最小边界（答案为 1）----
emit(1, 1, 1, 'a')

# ---- 点2：n=2 全同字符，m=n=2（答案为 1 的极端）----
emit(2, 2, 2, 'zz')

# ---- 点3：30% 档小随机（n<=200，26 字母），可手算验证 ----
n3 = random.randint(100, 200)
emit(3, n3, random.randint(1, n3), rand_str(n3, 26))

# ---- 点4：小随机 + 小字母表（2 种字符，重复子串极多）----
n4 = random.randint(100, 200)
emit(4, n4, random.randint(1, min(n4, 50)), rand_str(n4, 2))

# ---- 点5：50% 档中规模（n<=2000，26 字母随机）----
n5 = random.randint(1500, 2000)
emit(5, n5, random.randint(1, n5), rand_str(n5, 26))

# ---- 点6：中规模 + 重复结构（周期块 + 小字母表混合）----
n6 = random.randint(1500, 2000)
s6 = periodic(n6, ['ab', 'aba', 'aab'])
s6 = list(s6)
# 混入少量随机扰动，避免完全周期
for j in range(0, n6, 37):
    s6[j] = random.choice(ALPHA[:3])
emit(6, n6, random.randint(1, min(n6, 100)), ''.join(s6))

# ---- 点7：大规模（n=200000, m<=50，26 字母随机，另 20% 档结构）----
n7 = 200000
emit(7, n7, random.randint(10, 50), rand_str(n7, 26))

# ---- 点8：大规模 + 小字母表（m 小，重复子串海量，去重正确性压力）----
n8 = 200000
emit(8, n8, random.randint(10, 50), rand_str(n8, 3))

# ---- 点9：顶格层（n=200000, m=n/2，窗口数 100001，哈希/排序压力最大）----
n9 = 200000
emit(9, n9, n9 // 2, rand_str(n9, 26))

# ---- 点10：顶格层（n=200000, m=n，答案必为 1，最极端 m）----
n10 = 200000
emit(10, n10, n10, rand_str(n10, 26))
