#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1693《正确答案》 数据生成器（cyaron）
范围：1 <= n <= 30000, 1 <= m <= 500, 0 <= p,q 且 p+q <= n
10 个测试点分层：
  1-2   边界层
  3-4   小规模随机（可手算验证）
  5-6   中等规模随机
  7-8   大规模随机（接近上限）
  9-10  顶格层（n=30000, m=500 的最坏/特殊结构）
"""
from cyaron import *
import random
import sys

random.seed(20261005)

MODE = sys.argv[1] if len(sys.argv) > 1 else "default"

# 一些工具
def inv(s):
    return ''.join('Y' if c == 'N' else 'N' for c in s)

def rnd_str(m):
    return ''.join(random.choice('NY') for _ in range(m))

def build(n, m, p, q, gen_rows):
    """按给定规模生成一份测试点：gen_rows(base) -> 长度 n 的行列表。
       base 为构造出的标准答案（None 表示不保证有解）。"""
    base = rnd_str(m)
    rows = gen_rows(base)
    assert len(rows) == n
    content = f"{n} {m} {p} {q}\n" + "\n".join(rows) + "\n"
    return content

def emit(data_id, content):
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(content)
    io.output_gen("../std")


# ----------------------------------------------------------------------
# 点 1：最小边界 n=1,m=1。构造 p=1,q=0，答案恰为唯一行。
def t1():
    n, m, p, q = 1, 1, 1, 0
    def g(base):
        return [base]
    return build(n, m, p, q, g)

# 点 2：n=2,m=1 边界 + 极端 p=0,q=0（答案与反串都不得出现）。
#        行 NY 不行，用两行 Y、N？不行(会覆盖)。构造 m=2 让存在解更直观：
#        行 "NN","YY"（互反），则字典序最小合法答案为 "NY"。
def t2():
    n, m, p, q = 2, 2, 0, 0
    def g(base):
        return ["NN", "YY"]
    return build(n, m, p, q, g)

# 点 3：小规模随机，保证有解（塞入 p 个满分、q 个零分），m=3。
def t3():
    n, m, p, q = 6, 3, 2, 1
    def g(base):
        rows = [base] * p + [inv(base)] * q
        while len(rows) < n:
            x = rnd_str(m)
            if x == base or x == inv(base):  # 避免污染满分/零分计数
                continue
            rows.append(x)
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 4：小规模，q=0 而 p>0（满分串唯一候选类），m=4，n=7。
def t4():
    n, m, p, q = 7, 4, 3, 0
    def g(base):
        rows = [base] * p
        while len(rows) < n:
            x = rnd_str(m)
            if x == base or x == inv(base):  # 避免污染满分/零分计数
                continue
            rows.append(x)
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 5：中等随机，m=50，n=200，p、q 均非 0。
def t5():
    n, m, p, q = 200, 50, 17, 9
    def g(base):
        rows = [base] * p + [inv(base)] * q
        while len(rows) < n:
            rows.append(rnd_str(m))
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 6：中等随机，p=0,q>0（用反串补），m=80，n=400。
def t6():
    n, m, p, q = 400, 80, 0, 23
    def g(base):
        rows = [inv(base)] * q
        while len(rows) < n:
            rows.append(rnd_str(m))
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 7：大规模随机，m=400，n=15000。
def t7():
    n, m, p, q = 15000, 400, 123, 77
    def g(base):
        rows = [base] * p + [inv(base)] * q
        while len(rows) < n:
            rows.append(rnd_str(m))
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 8：大规模随机，m=500（非顶格 n），p=0,q>0。
def t8():
    n, m, p, q = 20000, 500, 0, 200
    def g(base):
        rows = [inv(base)] * q
        while len(rows) < n:
            rows.append(rnd_str(m))
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 9：顶格 n=30000,m=500，p+q=n（全部为满分/零分，无"其他"），
#        且构造大量不同串，最坏地撑满哈希表/排序。
def t9():
    n, m, p, q = 30000, 500, 10000, 20000
    def g(base):
        rows = [base] * p + [inv(base)] * q
        # 顶部：把剩余行全部替换为互不相同随机串（可能覆盖掉上面的重复？不会，随机串与 base 不同）
        # 这里直接构造：p 个 base、q 个 inv(base)，恰好 p+q=n。
        random.shuffle(rows)
        return rows
    return build(n, m, p, q, g)

# 点 10：顶格 n=30000,m=500，p=0,q=0（标准答案及其反串都不出现）。
#         最坏结构：输入行全相同 -> 禁止集合仅 {X, comp(X)}，答案贪心构造。
def t10():
    n, m, p, q = 30000, 500, 0, 0
    def g(base):
        x = rnd_str(m)
        return [x] * n
    return build(n, m, p, q, g)


TESTS = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

if MODE == "default":
    for i, f in enumerate(TESTS, start=1):
        emit(i, f())
