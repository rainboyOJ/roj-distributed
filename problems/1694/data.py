#!/usr/bin/env python

# 一本通 1694 回文串 数据生成器
#
# 输入格式：
#   第 1 行：数据类型 str（A/B/C，标程忽略）
#   第 2 行：A
#   第 3 行：B
#   第 4 行：Q
#   接下来 Q 行：x y
#
# 记 A_x 为 A 的第 x 长后缀（长度 n-x+1），B_y 为 B 的第 y 长前缀（长度 m-y+1）。

import random
from cyaron import *

MAXN = 800000
MAXQ = 100000
random.seed(1694)


def write_case(data_id, dtype, A, B, queries):
    io = IO(file_prefix="problem", data_id=data_id)
    lines = [dtype, A, B, str(len(queries))]
    lines += ["%d %d" % (x, y) for (x, y) in queries]
    io.input_write("\n".join(lines) + "\n")
    io.output_gen("../std")


def rand_string(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))


def rand_queries(n, m, q):
    return [(random.randint(1, n), random.randint(1, m)) for _ in range(q)]


def edge_queries(n, m, q):
    """混合极端询问：左上角/右下角 + 随机。"""
    qs = [(1, 1), (n, m), (1, m), (n, 1)]
    qs += rand_queries(n, m, max(0, q - len(qs)))
    random.shuffle(qs)
    return qs[:q]


# 1. 最小规模边界 n=m=1
write_case(1, "C", "a", "a", [(1, 1)])

# 2. 子任务 1：max<=40, Q<=200, 类型 C（小字母表，回文多）
n, m = 40, 40
A = rand_string(n, "ab")
B = rand_string(m, "ab")
write_case(2, "C", A, B, edge_queries(n, m, 200))

# 3. 子任务 2：max<=2000, Q<=2000, 类型 A（随机）
n, m = 2000, 2000
A = rand_string(n, "abcdefghijklmnopqrstuvwxyz")
B = rand_string(m, "abcdefghijklmnopqrstuvwxyz")
write_case(3, "A", A, B, rand_queries(n, m, 2000))

# 4. 子任务 4：max<=2000, Q<=2000, 类型 C（全 'a'，回文极多）
n, m = 2000, 2000
A = "a" * n
B = "a" * m
write_case(4, "C", A, B, rand_queries(n, m, 2000))

# 5. 子任务 3：max<=1e5, Q=1, 类型 C（全 'a'）
n, m = 100000, 100000
write_case(5, "C", "a" * n, "a" * m, [(1, 1)])

# 6. 子任务 5：max<=8e5, Q<=1e5, 类型 B（串随机且 |B|<=1e4）
n, m = 800000, 10000
A = rand_string(n, "abcdefghijklmnopqrstuvwxyz")
B = rand_string(m, "abcdefghijklmnopqrstuvwxyz")
write_case(6, "B", A, B, edge_queries(n, m, MAXQ))

# 7. 子任务 6/7：max=8e5, Q=1e5, 类型 C（随机 26 字母）
n, m = 800000, 800000
A = rand_string(n, "abcdefghijklmnopqrstuvwxyz")
B = rand_string(m, "abcdefghijklmnopqrstuvwxyz")
write_case(7, "C", A, B, edge_queries(n, m, MAXQ))

# 8. 子任务 6/7：max=8e5, Q=1e5, 类型 C（全 'a'，答案最大）
n, m = 800000, 800000
write_case(8, "C", "a" * n, "a" * m, edge_queries(n, m, MAXQ))

# 9. 子任务 6/7：max=8e5, Q=1e5, 类型 C（周期串 "abab..."，回文结构规则）
n, m = 800000, 800000
A = ("ab" * ((n + 1) // 2))[:n]
B = ("ba" * ((m + 1) // 2))[:m]
write_case(9, "C", A, B, edge_queries(n, m, MAXQ))

# 10. 子任务 6/7：max=8e5, Q=1e5, 类型 C，B = reverse(A)
#     使 A[x..] 与 rev(B)[x..] 相同，LCP 极大，压哈希/二分与答案量级
n, m = 800000, 800000
A = rand_string(n, "abcdefghijklmnopqrstuvwxyz")
B = A[::-1]
qs = [(x, x) for x in [1, 2, n // 2, n - 1, n]]
qs += rand_queries(n, m, MAXQ - len(qs))
random.shuffle(qs)
write_case(10, "C", A, B, qs[:MAXQ])
