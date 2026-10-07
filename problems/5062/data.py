#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 2061 【例1.2】梯形面积 —— 测试数据生成器（cyaron）
#
# 本题【输入】为“(无)”，输出恒为梯形面积 400.00（保留两位小数）：
#   题图上底 a=15、下底 b=25，阴影三角形面积 150 => h = 2*150/15 = 20
#   S = (15+25)*20/2 = 400。
# 无输入题按语料惯例只生成 1 组数据，避免重复（参考 problems/5006/data.py）。
# 分层说明：本题无可铺开的输入量，边界/随机/顶格各层均不适用，详见 gen-report.md。

from cyaron import *  # 引入CYaRon的库

# 本题无输入，输出恒为固定值，只生成 1 组数据。
io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
# 无输入：problem1.in 保持为空文件
io.input_write()
io.output_gen("../std")
