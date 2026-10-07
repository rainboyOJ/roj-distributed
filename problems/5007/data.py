#!/usr/bin/env python3
# 一本通 1671《扑克牌》数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围：1<=n<=1000000，"牌的数量<=10^6"。
#   注："牌的数量"措辞有歧义（普通牌总数 / 含特殊牌的总数 / 单种牌上限），
#   本生成器按最严格的读法控制每组数据 sum(a_i)+b <= 1000000，
#   任何一种读法下都绝不越界；b 的范围题面未给出，同样计入总量控制。
#   a_i 可取 0（题面未禁）且点 1 用到 a_i=10^6 上限值，用于覆盖
#   "答案为 0 / 1 的极端""极端权值"等边界。
#
# 分层设计（10 组，规模从小到顶格，覆盖多种答案量级）：
#   点 1-2  边界层：n 下限、极端权值、答案 0 / 答案顶格；
#   点 3-4  小规模随机：可手算验证，覆盖 need<=b 受限档；
#   点 5-6  中等规模随机：范围中间档，覆盖 need<=k 与 need<=b 交互；
#   点 7-8  大规模随机/构造：接近上限，含有序/重复值结构；
#   点 9-10 顶格层：n=10^6、总牌数=10^6 双顶格，全相等与卡常结构。
from cyaron import IO, randint, random

# ---------------- 点 1：边界层 ----------------
# n=1 下限 + 极端权值 a_1=10^6（总牌数 10^6 顶格）+ 答案顶格：
# n=1 时一副牌即 1 张普通牌或 1 张特殊牌，答 a_1+b = 10^6
def gen1():
    io = IO(file_prefix="problem", data_id=1)
    n, b = 1, 0
    arr = [1000000]
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 2：边界层 ----------------
# n=2 下限 + 全最小值（两种牌各 0 张）+ 答案为 0 的极端：
# 副特殊牌仍需 n-1=1 张普通牌，1 张特殊牌补不出任何一副，答 0
def gen2():
    io = IO(file_prefix="problem", data_id=2)
    n, b = 2, 1
    arr = [0, 0]
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 3：小规模随机 ----------------
# n=5（与样例同量级）、a_i∈[1,5]、b∈[0,8]：可手算/暴力验证；
# 偶尔取 b=0 覆盖"无特殊牌"分支
def gen3():
    io = IO(file_prefix="problem", data_id=3)
    random.seed(167103)
    n = 5
    b = 0 if randint(1, 4) == 1 else randint(1, 8)   # 大概率非零，偶尔 b=0
    arr = [randint(1, 5) for _ in range(n)]
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 4：小规模随机 ----------------
# n=50，a_i∈[10,20] 紧凑分布，b∈[0,30]：答案约 10~20，
# need<=b 先于 need<=k 触顶，覆盖"特殊牌不够"的受限档
def gen4():
    io = IO(file_prefix="problem", data_id=4)
    random.seed(167104)
    n = 50
    b = randint(0, 30)
    arr = [randint(10, 20) for _ in range(n)]
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 5：中等规模随机 ----------------
# n=3000（40% 数据上限），a_i∈[281,300] 且恰 1 个 280（唯一最小堆），
# b∈[0,50000]：答案约 280，need<=k 与 need<=b 两个约束在此交互
def gen5():
    io = IO(file_prefix="problem", data_id=5)
    random.seed(167105)
    n = 3000
    b = randint(0, 50000)
    arr = [randint(281, 300) for _ in range(n)]
    arr[0] = 280
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 6：中等规模随机 ----------------
# n=10^5，a_i∈[4,8] 稀疏小堆（缺牌多、S(k)=sum max(0,k-a_i) 增长快，卡二分判定），
# b 取剩余总牌数内的随机值，保证 sum(a)+b <= 10^6
def gen6():
    io = IO(file_prefix="problem", data_id=6)
    random.seed(167106)
    n = 100000
    arr = [randint(4, 8) for _ in range(n)]
    b = randint(0, 1000000 - sum(arr))
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 7：大规模随机 ----------------
# n=5*10^5（接近上限），a_i∈[1,2] 无零牌种，b=10^6-sum(a)：
# 大 n + 大 b，答案被 need<=k 卡在 min(a)，专测判定式第二分支
def gen7():
    io = IO(file_prefix="problem", data_id=7)
    random.seed(167107)
    n = 500000
    arr = [randint(1, 2) for _ in range(n)]
    b = 1000000 - sum(arr)
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 8：大规模构造（有序/重复值） ----------------
# n=8*10^5，a_i 呈降序阶梯 2,2,…,1,1,…,0,0（有序+重复值+零牌种），
# b=10^6-sum(a)：总牌数恰好 10^6 顶格；海量零牌堆使 need>>k，答 0
def gen8():
    io = IO(file_prefix="problem", data_id=8)
    n = 800000
    arr = [2 - min(2, i * 3 // n) for i in range(n)]
    b = 1000000 - sum(arr)
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 9：顶格层 ----------------
# n=10^6 顶格 + 全相等结构（a_i 全为 1）+ 总牌数=10^6 顶格 + b=0：
# 答案恰为 1（答案为 1 的极端），考验全相等、无特殊牌时的下界
def gen9():
    io = IO(file_prefix="problem", data_id=9)
    n, b = 1000000, 0
    arr = [1] * n
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

# ---------------- 点 10：顶格层（卡常结构） ----------------
# n=10^6 顶格 + 重复值极端分布（a_i∈{0,1} 约各半）+ 总牌数恰好 10^6 顶格：
# 海量 0 张牌种 + 巨量特殊牌，S(k) 增速远超 k，专卡"忘记判 need<=k"的错误做法
def gen10():
    io = IO(file_prefix="problem", data_id=10)
    random.seed(167110)
    n = 1000000
    arr = [randint(0, 1) for _ in range(n)]
    b = 1000000 - sum(arr)
    io.input_write(n, b, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen("../std")

if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
        print(f"{g.__name__} done")
