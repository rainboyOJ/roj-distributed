#!/usr/bin/env python

from cyaron import *  # 引入CYaRon的库

# 本题无输入，输出恒为固定字符串，所有测试点内容完全相同。
# 因此按题目实际情况只生成 1 组数据，避免重复。
io = IO(file_prefix="problem", data_id=1)  # problem1.in / problem1.out
# 无输入：problem1.in 保持为空文件
io.input_write()
io.output_gen("../std")
