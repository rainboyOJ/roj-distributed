#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一本通 2127《【例1.2】高精度加法》数据生成器（cyaron）
#
# 题意：第一行一个非负整数 a，第二行一个非负整数 b，
#       每行「不超过 100 位」，输出 a+b（一行）。
# 限制：time 1000ms / memory 64MB（config.json）。
#
# 关键语义（题面为准，见 gen-report.md「风险点」）：
#   * 位数上限 100，但和最多 101 位（两个 100 位数相加可能产生最高位进位）；
#   * 输入是非负整数（可为 0），答案 0 必须输出单个 `0`；
#   * 输出无前导零；每个测试文件只有一组数据（两行）。
#
# 分层设计（10 组，从最小铺到顶格）：
#   点 1     边界层：0 + 0 —— 全最小值，答案是 0 的极端（考输出空行/前导零）
#   点 2     边界层：1 + 0 —— 答案是 1 的极端；单侧为 0；最小非零加数
#   点 3     边界层：题面样例（20 位 + 20 位，逐位无进位）—— 与题面输出样例对齐
#   点 4     小规模随机：1~2 位 —— 可手算验证
#   点 5     小规模随机：3~6 位 —— 可手算验证，含随机进位
#   点 6     中等规模随机：20~50 位且位数不等 —— 范围中间档
#   点 7     中等规模随机：0 + (60~80) 位 —— 单侧为 0 的大位数情形
#   点 8     大规模（近顶格）：100 位全 9 + 1 —— 进位链贯穿整串 + 位数极不等
#   点 9     顶格层：100 位随机 + 100 位随机（首位非 0）—— 最长等长随机输入
#   点 10    顶格最坏：100 位全 9 + 100 位全 9 —— 全进位链，结果 101 位（最高位进位）

from cyaron import IO  # 引入CYaRon的库
import random

random.seed(2127)  # 固定种子，便于复现

MAXLEN = 100  # 题面位数上限


def rnd_number(lo_len, hi_len, fixed_len=None):
    """生成 [lo_len, hi_len] 位、无前导零的十进制数串（字符串）。

    fixed_len 给定时忽略 lo_len/hi_len，固定生成该位数；首位取 1..9，
    保证有效位数严格等于 len(数串)。
    """
    n = fixed_len if fixed_len is not None else random.randint(lo_len, hi_len)
    if n <= 0:
        return "0"
    return str(random.randint(1, 9)) + "".join(
        str(random.randint(0, 9)) for _ in range(n - 1))


def digits(n):
    """字符串的有效位数（题面位数）。"""
    return len(n.lstrip("0")) or 1


def write_case(i, a, b, note):
    """写出第 i 组：第一行 a，第二行 b。"""
    assert digits(a) <= MAXLEN and digits(b) <= MAXLEN, "超出题面位数上限"
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(a)
    io.input_writeln(b)
    io.output_gen("../std")
    io.close()  # flush + close，确保随后能读到落盘的 .out
    with open("problem%d.out" % i) as f:
        ans = f.read().strip()
    # 独立真值（Python 大整数）自校验
    truth = str(int(a) + int(b))
    assert ans == truth, "case %d: std=%r truth=%r" % (i, ans, truth)
    print("problem%-2d: len(%s,%s) ans_len=%-3d -- %s"
          % (i, digits(a), digits(b), len(ans), note))


# ---------------- 点 1：边界层，全最小值 / 答案 0 ----------------
write_case(1, "0", "0", "边界层：0+0=0，全最小值，答案 0 的极端")

# ---------------- 点 2：边界层，答案 1 的极端 / 单侧为 0 ----------------
write_case(2, "1", "0", "边界层：1+0=1，单侧为 0，最小非零加数")

# ---------------- 点 3：边界层，题面样例 ----------------
write_case(3, "22222222222222222222", "33333333333333333333",
           "边界层：题面样例，20 位 + 20 位，逐位无进位")

# ---------------- 点 4：小规模随机，1~2 位 ----------------
a4, b4 = rnd_number(1, 2), rnd_number(1, 2)
write_case(4, a4, b4, "小规模随机：1~2 位，可手算验证")

# ---------------- 点 5：小规模随机，3~6 位 ----------------
a5, b5 = rnd_number(3, 6), rnd_number(3, 6)
write_case(5, a5, b5, "小规模随机：3~6 位，可手算验证，含随机进位")

# ---------------- 点 6：中等规模随机，20~50 位，位数不等 ----------------
a6 = rnd_number(20, 50)
b6 = rnd_number(20, 50)
while digits(b6) == digits(a6):
    b6 = rnd_number(20, 50)
write_case(6, a6, b6, "中等规模随机：20~50 位，强制位数不等")

# ---------------- 点 7：中等规模随机，单侧为 0（大位数） ----------------
a7 = "0"
b7 = rnd_number(60, 80)
write_case(7, a7, b7, "中等规模随机：0 + 60~80 位，单侧为 0 的大位数情形")

# ---------------- 点 8：大规模近顶格，全 9 + 1（进位链 + 位数极不等） ----------------
a8 = "9" * MAXLEN  # 100 位全 9
b8 = "1"
write_case(8, a8, b8, "大规模近顶格：100 位全 9 + 1，进位链贯穿整串")

# ---------------- 点 9：顶格层，100 位随机 + 100 位随机 ----------------
a9 = rnd_number(0, 0, fixed_len=MAXLEN)
b9 = rnd_number(0, 0, fixed_len=MAXLEN)
write_case(9, a9, b9, "顶格层：100 位随机 + 100 位随机（首位非 0），最长等长随机")

# ---------------- 点 10：顶格最坏，全 9 + 全 9（结果 101 位） ----------------
a10 = "9" * MAXLEN
b10 = "9" * MAXLEN
write_case(10, a10, b10, "顶格最坏：100 位全 9 + 100 位全 9，全进位链，结果 101 位")
