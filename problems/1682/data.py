#!/usr/bin/env python

# 一本通 1682 最小字典序 数据生成器
#
# 输入：第一行 T，接下来 T 行每行一个只含数字、逗号、问号的字符串 S。
# 输出：每行字典序最小的合法还原，或 impossible。
# 限制：1<=T<=10，1<=len(S)<=50。

import random
from cyaron import *  # 引入CYaRon的库

random.seed(1682)

MAXLEN = 50
MAXT = 10
ALPHA = ",0123456789?"


def emit(data_id, cases):
    """cases: list[str]，写入 T 与各行。"""
    assert 1 <= len(cases) <= MAXT
    for s in cases:
        assert 1 <= len(s) <= MAXLEN
        assert all(c in ALPHA for c in s)
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(str(len(cases)) + "\n" + "\n".join(cases) + "\n")
    io.output_gen("../std")


def rand_pattern(L, p_q=0.5, p_comma=0.15):
    """随机字符模式。"""
    out = []
    for _ in range(L):
        r = random.random()
        if r < p_q:
            out.append("?")
        elif r < p_q + p_comma:
            out.append(",")
        else:
            out.append(random.choice("0123456789"))
    return "".join(out)


def from_answer(L, p_mask):
    """先生成一个合法串，再随机遮掉一部分字符，保证有解。"""
    nums = []
    cur = random.randint(1, 9)
    while True:
        need = len(str(cur)) + (1 if nums else 0)
        if sum(len(str(x)) + 1 for x in nums) + need > L:
            break
        nums.append(cur)
        if sum(len(str(x)) + 1 for x in nums) >= L:
            break
        cur += random.randint(1, 12)
    s = ",".join(map(str, nums))
    s = s[:L]
    if s.endswith(","):
        s = s[:-1]
    return "".join("?" if random.random() < p_mask else c for c in s)


# 1. 最小规模边界：单个问号 / 单个数字 / 逗号
emit(1, ["?", "1", ",", "0"])

# 2. 最大长度单个串
emit(2, ["?" * MAXLEN, "1" * MAXLEN])

# 3. 满规模：T=10，全问号，各种长度
emit(3, ["?" * random.randint(45, MAXLEN) for _ in range(MAXT)])

# 4. 满长度全问号 + 少量固定数字
emit(4, ["?" * MAXLEN, "?" * (MAXLEN - 1) + "9", "9" + "?" * (MAXLEN - 1)])

# 5. 随机模式（问号/数字/逗号混合）
emit(5, [rand_pattern(random.randint(1, MAXLEN)) for _ in range(MAXT)])

# 6. 由合法答案遮罩而来（保证有解，考验最小性）
emit(6, [from_answer(random.randint(5, MAXLEN), random.uniform(0.2, 0.7))
         for _ in range(MAXT)])

# 7. 大量固定字符的随机模式（多为 impossible）
emit(7, [rand_pattern(random.randint(1, MAXLEN), p_q=0.15, p_comma=0.25)
         for _ in range(MAXT)])

# 8. 密集逗号 / 连续逗号 / 首尾逗号等非法结构
emit(8, [
    ",".join(["?"] * 25),          # 长度 49
    ",".join(["??"] * 16)[:MAXLEN],
    ",?," + "?" * 44,
    "?" * 45 + ",,",
    "?,," + "?," * 22,
    "?," * 24 + "?",
])

# 9. 长数字 + 短数字混合（长串递增数量少）
emit(9, [
    "?" * 49,
    "1,2," + "?" * 44,
    "?,10," + "?" * 20,
    "?" * 10 + ",9",
    "?2?5??7?,??",
])

# 10. 题面样例 + 随机补充
emit(10, [
    "??",
    "???",
    "?????????,9",
    "?,10,?????????????????,16,??",
    "?2?5??7?,??",
] + [rand_pattern(random.randint(1, MAXLEN)) for _ in range(5)])
