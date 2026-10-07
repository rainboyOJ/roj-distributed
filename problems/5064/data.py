#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 2063《【例1.4】牛吃牧草》—— 测试数据生成器（cyaron，仓库惯例）
# 目标 ROJ 题号 5064；用法：mkdir -p data && cd data && python3 ../data.py
#
# 题意：牧场牧草每天匀速生长，可供 15 头牛吃 20 天，或可供 20 头牛吃 10 天，
#       问每天新生的草量可供几头牛吃 1 天？
#   设每头牛每天吃 1 单位草，A 为初始草量，g 为每天新生草量：
#       15*20 = A + 20g,  20*10 = A + 10g  =>  g = (300-200)/(20-10) = 10
#   答案唯一为 10（纯数字，无前缀——由题面【输出】「如题述，牛的数量。」确定，
#   冲突来源的判定见 gen-report.md）。
#
# 【输入】为（无），题目没有可铺开的输入量、取值范围或数据组数，
# 因此任务书要求的「边界/小/中/大/顶格」分层对本题不适用；
# 按任务书「无输入的题目（输出恒定）按语料惯例只生成 1 组 problem1.in/.out
# （参考 problems/5006/data.py），不要生成重复的空测试点」执行。
# 旁证：官方 OJ 该题的 Accepted 提交记录均为「Accepted|10:AC」单测试点，
#       即官方数据也只有 1 个测试点（详见 gen-report.md）。
#
# 参考实现：problems/5006/data.py、problems/2060（staging）同款写法。

from cyaron import *  # 引入CYaRon的库

# 本题无输入，输出恒为固定值 10，所有测试点内容完全相同，只生成 1 组数据。
io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
# 无输入：problem1.in 保持为空文件
io.input_write()
io.output_gen("../std")
print("problem1: 空输入 -> 期望输出 10（每天新生草量可供 10 头牛吃 1 天）")
