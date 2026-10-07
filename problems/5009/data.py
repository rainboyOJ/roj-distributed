#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1673《楼间跳跃》分层测试数据生成器
#
# 题意模型：
#   到第 k 栋楼需 k-1 次跳跃；落点层免费取 1 件，楼内每多取 1 件需 1 单位时间。
#   总件数 = 总时间 + 1。等价于：在前缀 1..k 中每栋先取 1 件，其余件数贪心取价值最大的。
#
# 数据范围（题面）：n, h_i <= 10^6；题面未给出 m、v_i 上限。
#   按网上题解来源，本题 m <= 1e9、v_i <= 1e9（正整数）。据此造数，
#   最大答案 <= (m+1)*1e9 ≈ 1e18，仍在 long long 范围内。
#
# 分层设计（10 组）：
#   1  边界：n=1, m=1, h=1, v=1  -> 答案 1（最小规模 + v=1 特殊值 + 答案=1）
#   2  边界：n=2, m=1, h=1, v=1e9 -> 答案 2e9（n=2 + v 全最大值 + h 全最小值）
#   3  小规模可手算：n=3, m=3, 触发“部分替换”（堆顶价值分组只替换一部分）
#   4  小规模随机：n=4, m=5（可手算/暴力验证量级）
#   5  中等随机：n=1000, m=2000
#   6  中等随机：n=5000, m=1e5
#   7  大规模随机：n=1e5, m=1e6
#   8  大规模随机：n=2e5, m=5e8（m 接近来源上限）
#   9  顶格：n=1e6, h=1e6, v=1e9 全相等（最坏：大量重复值）
#  10  顶格：n=1e6, h=1e6, v 递增（最坏：每个新权值都要淘汰堆内旧值，堆反复弹出）

import random
from cyaron import IO

random.seed(20240517)


def write_case(data_id, n, m, pairs):
    """pairs: list of (h, v)"""
    lines = [f"{n} {m}"]
    for h, v in pairs:
        lines.append(f"{h} {v}")
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write("\n".join(lines) + "\n")
    io.output_gen("../std")


# 1. 边界：最小规模
write_case(1, 1, 1, [(1, 1)])

# 2. 边界：n=2，h 全最小，v 全最大
write_case(2, 2, 1, [(1, 10**9), (1, 10**9)])

# 3. 小规模可手算：触发“部分替换”的边界结构
#    n=3, m=3 -> 总件数预算 = 4
#    楼 1: h=2,v=5 (额外 1 件)；楼 2: h=3,v=4 (额外 2 件)；楼 3: h=3,v=6 (额外 2 件)
#    枚举前缀 k=3 时：免费 5+4+6=15，额外预算 1，需淘汰 5->4-> 最终只保留价值 6 的一部分。
write_case(3, 3, 3, [(2, 5), (3, 4), (3, 6)])

# 4. 小规模随机（可手算/暴力验证）
write_case(4, 4, 5, [(random.randint(1, 4), random.randint(1, 9)) for _ in range(4)])

# 5. 中等规模随机
write_case(5, 1000, 2000,
           [(random.randint(1, 100), random.randint(1, 100000)) for _ in range(1000)])

# 6. 中等规模随机
write_case(6, 5000, 100000,
           [(random.randint(1, 2000), random.randint(1, 1000000)) for _ in range(5000)])

# 7. 大规模随机
write_case(7, 100000, 1000000,
           [(random.randint(1, 100000), random.randint(1, 10**9)) for _ in range(100000)])

# 8. 大规模随机，m 接近来源上限
write_case(8, 200000, 500000000,
           [(random.randint(1, 100000), random.randint(1, 10**9)) for _ in range(200000)])

# 9. 顶格：全相等最坏结构（大量重复价值）
write_case(9, 10**6, 10**9, [(10**6, 10**9)] * 10**6)

# 10. 顶格：权值递增，堆反复弹空（最坏 O(n log n) 结构）
write_case(10, 10**6, 10**9, [(10**6, i) for i in range(1, 10**6 + 1)])
