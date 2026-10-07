#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2023《【例4.8】数据统计》数据生成器（cyaron，目标 ROJ 题号 5025）
#
# 题意：输入一行若干个整数，输出一行：最小值、最大值、平均值（保留 3 位小数）。
#   题面【提示】数据范围：**数据个数不超过 100**；
#   题目描述保证：**这些数都是不超过 1000 的整数**（只给了上界）。
#   样例：输入 `1 2 3` -> 输出 `1 3 2.000`。
#   限制：1000 ms / 65536 KB（config.json 记 time 1000 / memory 64MB）。
#
# 【取值范围处置，见 gen-report.md 风险点 1】
#   题面只声明上界（"不超过 1000"），未声明下界。本包自定**工作范围 0 <= x <= 1000**：
#     * 已联网核对的 5 份题解（CSDN，见 std.cpp 头部 URL）全部把最小值初值写成
#       1001 / 10000、最大值初值写成 0 / -1 / -10000，这些初值只在「数据 >= 0」
#       的假设下才都正确（其中 mx=0 的写法一旦遇到**全负**数据就会输出错误的
#       最大值）——说明官方数据的自然读法是非负小整数；
#     * 0 作为工作范围下界仍在题面保证之内（"不超过 1000 的整数"），且能覆盖
#       最小值/平均值输出全零（"0.000"）的极端；
#     * **不把负数写进正式测试点**（虽然字面上未被题面禁止），以免把按官方惯例
#       初始化 min/max 的正常 AC 解法判错；std.cpp 本身写成对任意 int 输入都正确
#       （INT_MAX/INT_MIN 初值 + long long 求和），负数情形由 work/stress.py 的
#       对拍另行覆盖验证（见 gen-report.md）。
#
# 分层（10 个测试点，单组输入；n 从 1 铺到上限 100，取值从下界 0 铺到上界 1000）：
#   点 1  边界层：n=1，x=0        —— 最小个数 + 取值下界（输出 "0 0 0.000"）
#   点 2  边界层：n=1，x=1000     —— 最小个数 + 取值上界（输出 "1000 1000 1000.000"）
#   点 3  边界层：n=2，{0,1000}   —— 最小规模 n=2，且两端极值同时出现
#   点 4  边界层：n=3，{1,2,3}    —— **题面【输入样例】**声明的特殊值（可比对样例答案）
#   点 5  小规模：n=8，{2,8,3,5,1,7,3,6} —— **教材原题样例**（算法竞赛入门经典 习题2-5，
#                                       输出 1 8 4.375），三位小数非平凡，可手算
#   点 6  小规模·临界：n=16，{1,1,1,0×13} —— 平均值恰为 3/16 = 0.1875（4 位小数、第 4 位是 5
#                                      的**精确二进制可表示**临界值）；printf 舍入后为 0.188。
#                                      截断型实现会输出 0.187，直接暴露格式错误
#                                      （0.1875 -> 0.188 在 half-even 与 half-up 下一致，
#                                        故该点不依赖舍入约定）
#   点 7  中等规模随机：n=30，x∈[0,1000] —— 中间档；重复值自然出现
#   点 8  大规模随机：n=60，x∈[0,1000]   —— 接近个数上限
#   点 9  顶格随机：n=100（上限），x∈[0,1000]，且强制包含 0 与 1000 —— 个数顶格 + 值域两端
#   点 10 顶格构造：n=100，全 1000      —— 全最大值 / 全相等 / 重复值 / 平均值输出尾零
#                                       （"1000 1000 1000.000"）
#   注：本题输入是无序的一行数字，没有"有序/逆序/链"等结构可构造；
#       10 个点里 4 个精确构造 + 1 个临界 + 3 个随机 + 2 个边界，不存在"全是小随机"。
#
# 随机性：随机点使用独立 random.seed(2023000 + 点号)，逐字节可复现。
# 自检：每组生成后用 Python 独立预测期望输出（浮点格式与 printf 同为
#       IEEE binary64 + 就近舍入/半偶）并读回 problemN.out 逐字节比对，不一致立即报错。

from cyaron import *  # 引入CYaRon的库

import os
import random


def expected_line(vals):
    """独立预测输出：min max avg(3位小数)。与 std 的实现路线无关（Python 内建 float 格式化）。"""
    mn = min(vals)
    mx = max(vals)
    avg = sum(vals) / len(vals)  # 精确整数和 -> double 除法，与 C++ (double)sum/n 同为正确舍入
    return "%d %d %.3f" % (mn, mx, avg)


def build_points():
    """返回 [(data_id, 各值列表, 说明)]，逐点构造。"""
    pts = []

    # ---- 点 1-4：边界层 ----
    pts.append((1, [0], "边界：n=1 最小值 0（工作范围下界）"))
    pts.append((2, [1000], "边界：n=1 最大值 1000（题面上界）"))
    pts.append((3, [0, 1000], "边界：n=2，两极值同时出现"))
    pts.append((4, [1, 2, 3], "边界：题面【输入样例】1 2 3"))

    # ---- 点 5-6：小规模（精确构造）----
    pts.append((5, [2, 8, 3, 5, 1, 7, 3, 6], "小规模：教材原题样例，avg=4.375"))
    pts.append((6, [1, 1, 1] + [0] * 13, "小规模·临界：avg=3/16=0.1875 -> 0.188（舍入临界）"))

    # ---- 点 7-8：中等 / 大规模随机 ----
    random.seed(2023007)
    pts.append((7, [random.randint(0, 1000) for _ in range(30)], "中等随机：n=30, x∈[0,1000]"))
    random.seed(2023008)
    pts.append((8, [random.randint(0, 1000) for _ in range(60)], "大规模随机：n=60, x∈[0,1000]"))

    # ---- 点 9-10：顶格层 ----
    random.seed(2023009)
    vals = [random.randint(0, 1000) for _ in range(100)]
    vals[0], vals[1] = 0, 1000  # 强制覆盖值域两端
    pts.append((9, vals, "顶格随机：n=100（个数上限）, x∈[0,1000]，含 0 与 1000"))
    pts.append((10, [1000] * 100, "顶格构造：n=100 全 1000（全相等/重复/尾零）"))

    return pts


def main():
    for data_id, vals, note in build_points():
        io = IO(file_prefix="problem", data_id=data_id)  # problem{data_id}.in / .out
        io.input_writeln(*vals)                         # 一行，空格分隔，行末换行
        io.output_gen("../std")                         # 调 std 生成 .out
        io.close()                                      # 冲刷/关闭缓冲，保证下方回读到落盘内容

        # ---- 自检：独立预测并与 std 输出逐字节比对 ----
        out_path = "problem%d.out" % data_id
        with open(out_path, "r", encoding="utf-8") as f:
            got = f.read()
        exp = expected_line(vals) + "\n"
        if got != exp:
            raise SystemExit("SELF-CHECK FAILED at point %d: got %r, expect %r" % (data_id, got, exp))
        print("problem%-2d n=%-3d min=%-4d max=%-4d avg=%-8.3f -- %s"
              % (data_id, len(vals), min(vals), max(vals), sum(vals) / len(vals), note))


if __name__ == "__main__":
    main()
