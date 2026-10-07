#!/usr/bin/env python
# 一本通 2128《高精度乘法（II）》 分层数据生成器
#
# 题意：输入两个高精度正整数 a、b（均「小于 200000 位」→ 最多 199999 位），输出 a*b。
# 限制：time 1000ms / memory 128MB（config.json；官方题面页写 131072KB）。
#
# 分层设计（10 组，每组 1 个测试用例，两行输入）：
#   1  边界层：n=1 最小规模、答案为 1 的极端（1×1）
#   2  边界层：×0 语义（0 乘 19 位全 9）
#   3  小规模随机：各 1..5 位随机，可用 Python 大整数独立验证
#   4  小规模·前导零/×1/位数不等："00000001" × 9 位随机
#   5  中等·10^k 结构：10^4999 × 1000 位随机（尾随零 + 位数不等）
#   6  中等规模随机：各 50000 位
#   7  大规模随机：各 150000 位（接近上限）
#   8  大规模·位数不等随机：149999 位 × 34999 位
#   9  顶格层·全 9：各 199999 位全 9（最坏进位链，结果 399997 位）
#   10 顶格层·随机：各 199999 位随机（顶格规模的平均情形）
#
# 注：题面写「正整数」，第 2 组的 0 属于越界鲁棒性检查（语义：0×大数=0）；
#     第 4 组含前导零（语义：按数值解析）。两者均在 gen-report.md 风险点中说明。

import random

from cyaron import IO  # 引入 CYaRon 的库

random.seed(2128)  # 固定种子：数据可复现

DIGITS = "0123456789"
NONZERO = "123456789"
MAXLEN = 199999  # 题面「小于 200000 位」→ 顶格 199999 位


def rand_num(n, first_nonzero=True):
    """生成长度 n 的十进制数字串；first_nonzero=True 时首位非 0。"""
    s = "".join(random.choices(DIGITS, k=n))
    if first_nonzero:
        s = random.choice(NONZERO) + s[1:]
    return s


def gen(i, a, b):
    io = IO(file_prefix="problem", data_id=i)  # problem<i>.in / problem<i>.out
    io.input_write(a, "\n", b, "\n")  # 两行输入
    io.output_gen("../std")  # 用标程生成答案


# ---- 1. 边界层：n=1 / 全最小值 / 答案为 1 ----
gen(1, "1", "1")

# ---- 2. 边界层：×0（0×大数 = 0） ----
gen(2, "0", "9" * 19)

# ---- 3. 小规模随机：各 2..5 位（可手算/大整数独立验证） ----
gen(3, rand_num(random.randint(2, 5)), rand_num(random.randint(2, 5)))

# ---- 4. 小规模·前导零 + ×1 + 位数不等 ----
gen(4, "00000001", rand_num(9))

# ---- 5. 中等·10^k 结构（5000 位 × 1000 位） ----
gen(5, "1" + "0" * 4999, rand_num(1000))

# ---- 6. 中等规模随机：各 50000 位 ----
gen(6, rand_num(50000), rand_num(50000))

# ---- 7. 大规模随机：各 150000 位 ----
gen(7, rand_num(150000), rand_num(150000))

# ---- 8. 大规模·位数不等随机：149999 位 × 34999 位 ----
gen(8, rand_num(149999), rand_num(34999))

# ---- 9. 顶格层·全 9（最坏进位链）：各 199999 位 ----
gen(9, "9" * MAXLEN, "9" * MAXLEN)

# ---- 10. 顶格层·随机：各 199999 位 ----
gen(10, rand_num(MAXLEN), rand_num(MAXLEN))
