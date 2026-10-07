#!/usr/bin/env python

from cyaron import * # 引入CYaRon的库

# 手动指定若干边界与代表性测试点，其余随机
fixed = {
    1: 1,
    2: 2,
    3: 100,
    4: 99,
    5: 50,
}

for i in range(1,11):
    io = IO(file_prefix="problem", data_id=i) # problem1.in ...

    if i in fixed:
        n = fixed[i]
    else:
        n = randint(1,100)

    io.input_write(n)
    io.output_gen("../std")
