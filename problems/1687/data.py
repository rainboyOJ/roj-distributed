#!/usr/bin/env python3
# 一本通 1687《积水问题》分层数据生成器
#
# 输入格式：第一行 n m；随后 n 行，每行 m 个整数（高度，|h|<=1e9）。
# 输出格式：n 行，每行 m 个非负整数（每个格子的积水高度）。
# 本题 n,m<=300，1e9 高度可用 long long 承载，水位值域也在 long long 内。
#
# 分层设计（10 个测试点）：
#   problem1  边界层  n=1, m=1  单格高度 -1：外围高 0，积水 1
#   problem2  边界层  n=2, m=2  全负高度，验证边界与内部负格子的积水
#   problem3  边界层  n=3, m=3  全 0，答案全 0（无积水）
#   problem4  小规模  n=3, m=4  随机非负高度（手算量级）
#   problem5  小规模  n=4, m=4  随机含负高度
#   problem6  中规模  n=50, m=50 随机混合高度
#   problem7  中规模  n=150, m=150 随机混合高度（中间档）
#   problem8  大规模  n=290, m=290 随机高度
#   problem9  顶格层  n=300, m=300 外围高墙 + 内部深坑（最坏蓄水结构）
#   problem10 顶格层  n=300, m=300 全相等负高度（全局蓄水 + 重复值压力）

from cyaron import *
import random

# 顶层上限
MAX_N = 300
MAX_M = 300
MAX_ABS_H = 10 ** 9

def write_case(data_id, n, m, grid, note):
    """把一整个矩阵写成一组的 in，并用 ../std 生成 out。"""
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_writeln(n, m)
    for row in grid:
        io.input_writeln(*row)
    io.output_gen("../std")
    print(f"  problem{data_id}: {n}x{m}  {note}")

def grid_of(n, m, gen):
    return [[gen(i, j) for j in range(m)] for i in range(n)]

# ---- 1. 边界层：单格 -1，外围 0，积水应为 1 ----
g = [[-1]]
write_case(1, 1, 1, g, "单格高度 -1，积水 1")

# ---- 2. 边界层：2x2 全负，验证边界/内部负格积水 ----
g = [[-5, -3], [-2, -7]]
write_case(2, 2, 2, g, "2x2 全负高度，验证负高度积水")

# ---- 3. 边界层：3x3 全 0，答案全 0 ----
g = grid_of(3, 3, lambda i, j: 0)
write_case(3, 3, 3, g, "全 0，无积水")

# ---- 4. 小规模：3x4 随机非负，可手算 ----
random.seed(1687)
g = grid_of(3, 4, lambda i, j: random.randint(0, 20))
write_case(4, 3, 4, g, "小规模随机非负高度")

# ---- 5. 小规模：4x4 随机含负 ----
g = grid_of(4, 4, lambda i, j: random.randint(-20, 20))
write_case(5, 4, 4, g, "小规模随机含负高度")

# ---- 6. 中规模：50x50 随机混合 ----
g = grid_of(50, 50, lambda i, j: random.randint(-10 ** 6, 10 ** 6))
write_case(6, 50, 50, g, "中规模随机混合高度")

# ---- 7. 中规模：150x150 随机混合 ----
g = grid_of(150, 150, lambda i, j: random.randint(-10 ** 8, 10 ** 8))
write_case(7, 150, 150, g, "中规模随机混合高度")

# ---- 8. 大规模：290x290 随机 ----
g = grid_of(290, 290, lambda i, j: random.randint(-10 ** 9, 10 ** 9))
write_case(8, 290, 290, g, "大规模随机高度")

# ---- 9. 顶格层：300x300 外围高墙 + 内部深坑（最坏蓄水） ----
# 边界全 1e9，内部全 -1e9：每个内部格子蓄水 = 1e9 - (-1e9) = 2e9，
# 蓄水量最大、松弛路径最长的最坏结构之一。
n = m = 300
g = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        if i == 0 or i == n - 1 or j == 0 or j == m - 1:
            g[i][j] = MAX_ABS_H
        else:
            g[i][j] = -MAX_ABS_H
write_case(9, n, m, g, "顶格 300x300 外围高墙+内部深坑(最坏蓄水)")

# ---- 10. 顶格层：300x300 全相等负高度 ----
# 全 -1e9：所有格子（含边界）积水 1e9，测试重复值/全局蓄水/顶格权值。
n = m = 300
g = grid_of(n, m, lambda i, j: -MAX_ABS_H)
write_case(10, n, m, g, "顶格 300x300 全 -1e9 重复值")
