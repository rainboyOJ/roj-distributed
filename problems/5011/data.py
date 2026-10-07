#!/usr/bin/env python3
# 一本通 1675《塔》分层测试数据生成器
# 数据范围：1 <= N, Ai <= 3000；时限 1s / 内存 256MB
# 分层设计（10 组，从边界到顶格）：
from cyaron import *

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)

    if i == 1:
        # 边界层①：N=1（题面最小值），答案恒为 0
        n = 1
        a = [1]
    elif i == 2:
        # 边界层②：N=3000 但全部 Ai=1（全等/全最小值），已不降，答案=0
        n = 3000
        a = [1] * n
    elif i == 3:
        # 小规模随机①：N=10（30% 分上限），小值域，可手算验证
        n = 10
        a = [randint(1, 10) for _ in range(n)]
    elif i == 4:
        # 小规模随机②：N=15，值域到 200，含重复值
        n = 15
        a = [randint(1, 200) for _ in range(n)]
    elif i == 5:
        # 中等随机①：N=200, Ai<=200（60% 分上限）
        n = 200
        a = [randint(1, 200) for _ in range(n)]
    elif i == 6:
        # 中等随机②：N=1000，值域到 1000，范围中间档
        n = 1000
        a = [randint(1, 1000) for _ in range(n)]
    elif i == 7:
        # 大规模随机①：N=2500, Ai<=3000，接近上限
        n = 2500
        a = [randint(1, 3000) for _ in range(n)]
    elif i == 8:
        # 大规模随机②：N=3000（顶格 N），值域大随机
        n = 3000
        a = [randint(1, 3000) for _ in range(n)]
    elif i == 9:
        # 顶格层①（最坏结构）：N=3000 严格递减序列，
        # 答案极大（实测 2936≈0.98N，接近上界 N-1），压满 DP 转移与长段合并
        n = 3000
        a = list(range(n, 0, -1))
    else:  # i == 10
        # 顶格层②（卡常+特殊形态）：N=3000，Ai 全部取上限 3000（全最大值/全等），
        # 答案=0 但对 DP 是全量转移，叠加递增序列打乱，保证运算量拉满
        n = 3000
        a = [3000] * (n // 2) + [randint(1, 3000) for _ in range(n - n // 2)]

    io.input_writeln(n)
    io.input_writeln(a)
    io.output_gen("../std")
