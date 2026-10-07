#!/usr/bin/env python
# 一本通 1676《手机游戏》分层测试数据生成器
# 产出 problem1.in/.out ... problem10.in/.out（在 data/ 目录下运行）
#
# 数据范围（题面）：
#   1 <= n <= 50000, 1 <= k <= 100000, 1 <= m_i <= 1e9
# 分层设计（10 组）：
#   1-2  边界层：n=1 的最小/最大极端
#   3-4  边界层：n=2 全最小 / 全最大（最小结构，手算可核）
#   5    小规模随机：n<=10, k<=10, m<=50（可用暴力对拍核验）
#   6    小规模随机：n<=50, k<=50, m<=1000
#   7    中等随机：n=1000, k<=1000, m<=1e6
#   8    中等偏大随机：n=10000, k=50000, m<=1e8
#   9    大规模随机：n=50000, k=100000, m<=1e9（接近上限）
#  10    顶格层：n=50000, k=1, m 全 1e9（最坏结构：单火球须覆盖全部怪物，
#         答案顶到 p = 1e9+1+(n-1)^2 ≈ 3.5e9，压满题面上限）

from cyaron import *
import random

random.seed(20240607)

def gen(i, n, k, ms):
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(n, k)
    io.input_writeln(list(ms))
    io.output_gen("../std")

# 1：n=1 最小，k=1，血量 1（答案 2）
gen(1, 1, 1, [1])

# 2：n=1 最大，k=100000，血量 1e9（答案 ceil((1e9+1)/1e5)=10001）
gen(2, 1, 100000, [10**9])

# 3：n=2 全最小，k=1（答案 3：一个火球射右，右 p>=2 且溅射左 p-1>=2）
gen(3, 2, 1, [1, 1])

# 4：n=2 全最大，k=1（一个火球射右，溅射 p-1>=1e9+1 => p>=1e9+2）
gen(4, 2, 1, [10**9, 10**9])

# 5：小规模随机，n<=10, k<=10, m<=50（可手算 / 暴力核验）
n = random.randint(1, 10)
k = random.randint(1, 10)
ms = [random.randint(1, 50) for _ in range(n)]
gen(5, n, k, ms)

# 6：小规模随机，n<=50, k<=50, m<=1000
n = random.randint(1, 50)
k = random.randint(1, 50)
ms = [random.randint(1, 1000) for _ in range(n)]
gen(6, n, k, ms)

# 7：中等随机，n=1000, k<=1000, m<=1e6
n = 1000
k = random.randint(1, 1000)
ms = [random.randint(1, 10**6) for _ in range(n)]
gen(7, n, k, ms)

# 8：中等偏大随机，n=10000, k=50000, m<=1e8
n = 10000
k = 50000
ms = [random.randint(1, 10**8) for _ in range(n)]
gen(8, n, k, ms)

# 9：大规模随机，n=50000, k=100000, m<=1e9
n = 50000
k = 100000
ms = [random.randint(1, 10**9) for _ in range(n)]
gen(9, n, k, ms)

# 10：顶格最坏结构，n=50000, k=1, 全 1e9
n = 50000
k = 1
ms = [10**9 for _ in range(n)]
gen(10, n, k, ms)
