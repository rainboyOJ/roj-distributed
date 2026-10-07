#!/usr/bin/env python

# 1672 游戏通关 —— 分层测试数据生成器
# 题意：N 个任务，任务 i 的完成时限 T_i（时刻从 0 开始，单个任务耗时 1 个单位时间），
#       奖励 W_i；每任务要么完整做一个单位时间、要么不做，求最大总奖励。
# 数据范围（题面）：N <= 200000，T_i <= 200000，W_i <= 2000。
# 分层设计：点1-2 边界层 / 点3-4 小规模随机 / 点5-6 中等规模随机 /
#           点7-8 大规模随机 / 点9-10 顶格层（上限 + 最坏结构）。
from cyaron import *  # 引入CYaRon的库
import random

random.seed(1672)

MAXN = 200000   # 题面 N 上限
MAXT = 200000   # 题面 T_i 上限
MAXW = 2000     # 题面 W_i 上限


def write_tasks(io, tasks):
    """写入任务表：首行 N，随后 N 行 'T W'。"""
    io.input_writeln(len(tasks))
    io.input_write("\n".join("%d %d" % (t, w) for t, w in tasks) + "\n")


for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)  # problem1.in / problem1.out ...

    if i == 1:
        # 点1 边界层：n=1 + 全最小值（T=1, W=1）。
        # 时限为 1（题面特殊值：只能抢第 1 个时间槽），答案=1，即"答案为 1"的极端。
        tasks = [(1, 1)]

    elif i == 2:
        # 点2 边界层：n=2 + 全最大值（T=200000, W=2000）+ 重复值。
        # 两任务时限/奖励都顶格且相同，答案=4000（顺带覆盖 W_i=2000 上限特殊值）。
        tasks = [(MAXT, MAXW), (MAXT, MAXW)]

    elif i == 3:
        # 点3 小规模随机：n=6，T∈[1,8]，W∈[1,10]，量级可手算验证。
        tasks = [(random.randint(1, 8), random.randint(1, 10)) for _ in range(6)]

    elif i == 4:
        # 点4 小规模随机：n=15，T∈[1,20]，W∈[1,50]，小随机、可与暴力对拍量级对照。
        tasks = [(random.randint(1, 20), random.randint(1, 50)) for _ in range(15)]

    elif i == 5:
        # 点5 中等规模随机：n=2000，T∈[1,2000]，W∈[1,2000]。
        # 时限与任务数同量级，竞争激烈，大量任务被贪心淘汰。
        tasks = [(random.randint(1, 2000), random.randint(1, MAXW)) for _ in range(2000)]

    elif i == 6:
        # 点6 中等规模随机：n=10000，T∈[1,20000]，W∈[1,2000]，范围中间档。
        tasks = [(random.randint(1, 20000), random.randint(1, MAXW)) for _ in range(10000)]

    elif i == 7:
        # 点7 大规模随机：n=100000，T∈[1,100000]，W∈[1,2000]，接近上限。
        tasks = [(random.randint(1, 100000), random.randint(1, MAXW)) for _ in range(100000)]

    elif i == 8:
        # 点8 大规模随机：n=180000，T∈[1,180000]，W∈[1,2000]，接近上限。
        tasks = [(random.randint(1, 180000), random.randint(1, MAXW)) for _ in range(180000)]

    elif i == 9:
        # 点9 顶格层：n=200000，T∈[1,200000]，W∈[1,2000]，题面全部维度取到上限的随机数据。
        tasks = [(random.randint(1, MAXT), random.randint(1, MAXW)) for _ in range(MAXN)]

    else:
        # 点10 顶格最坏结构：n=200000，全部 T=200000、W=2000（全相等 + 重复值 + 极端权值 + 卡常）。
        # 所有任务都可完成，答案=200000*2000=400000000，考验答案范围与并查集长链退化。
        tasks = [(MAXT, MAXW)] * MAXN

    write_tasks(io, tasks)
    io.output_gen("../std")
