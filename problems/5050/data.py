#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一本通 2048《【例5.18】串排序》数据生成器（cyaron）
#
# 题意：读入 n (1<=n<=20) 个国家名，每个名字长度不超过 20，按字母顺序升序输出 n 行。
#       比较规则为逐字符字典序（ASCII），样例：Korea/China/Japan -> China/Japan/Korea。
#
# 数据范围（题面）：1 <= n <= 20；名字长度 <= 20。无限定字符集，按常识用英文字母
#   （大写/小写/混合均出现，用于检验 ASCII 字典序）。
#
# 分层设计（10 组，从最小铺到顶格）：
#   点 1-2  边界层：n=1 下限 + 名字长度最小值 1；n=2 全相等/前缀关系（答案=输入原样）
#   点 3-4  小规模层：点 3 题面原样例（答案已知）；点 4 小规模随机 n=5（可手算）
#   点 5-6  中等规模随机：n=10 / n=12（含重复值）
#   点 7-8  大规模随机：n=18 随机长名 / n=19 逆序（最坏比较量）+ 长度接近顶格
#   点 9-10 顶格层：n=20 且名字长度 20 双顶格；点 9 随机混合、点 10 前缀链最坏结构
#
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py

from cyaron import IO  # 引入CYaRon的库
import random

random.seed(2048)  # 固定种子，便于复现

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MIXED = LOWER + UPPER


def rand_name(charset, lo=1, hi=20):
    """随机名字，长度在 [lo, hi] 内（题面要求长度不超过 20）。"""
    L = random.randint(lo, hi)
    return "".join(random.choice(charset) for _ in range(L))


def write_case(i, n, names, note):
    """写出第 i 组：第一行 n，随后 n 行名字；输出交给 std 生成。"""
    assert 1 <= n <= 20, note
    assert len(names) == n
    for s in names:
        assert 1 <= len(s) <= 20, note
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(n)
    for s in names:
        io.input_writeln(s)
    io.output_gen("../std")
    io.output_file.flush()  # 让本组 .out 落盘后再读取，便于在日志里核对
    with open("problem%d.out" % i) as f:
        lines = f.read().rstrip("\n").split("\n")
    assert len(lines) == n, "expect %d lines, got %d" % (n, len(lines))
    print("problem%-2d: n=%-2d maxlen=%-2d -- %s | out[0]=%s out[-1]=%s"
          % (i, n, max(len(s) for s in names), note, lines[0], lines[-1]))


# ---- 点 1：边界层 ----
# n=1 下限 + 名字长度最小值 1（全最小值）；排序后输出即输入本身。
write_case(1, 1, ["a"], "边界：n=1 下限、名字长度 1 最小值，答案=输入原样")

# ---- 点 2：边界层 ----
# n=2 下限 + 全相等（两个相同名字，答案=输入原样，测重复值不产生多余输出）。
write_case(2, 2, ["Zz", "Zz"], "边界：n=2 下限、全相等重复值，答案=输入原样")

# ---- 点 3：小规模（文面原样例，答案已知）----
# 逐字节照抄题面【输入样例】，期望输出即题面【输出样例】 China/Japan/Korea。
write_case(3, 3, ["Korea", "China", "Japan"], "小规模：题面原样例，答案已知（China/Japan/Korea）")

# ---- 点 4：小规模随机 ----
# n=5；大小写混合（ASCII 序中 'A'<'Z'<'a'），人工可算，验证大小写比较。
names = [rand_name(MIXED, 1, 5) for _ in range(5)]
write_case(4, 5, names, "小规模随机：n=5 大小写混合，可手算验证 ASCII 序")

# ---- 点 5：中等规模随机 ----
# n=10；小写随机，长度铺开 [1,10]。
names = [rand_name(LOWER, 1, 10) for _ in range(10)]
write_case(5, 10, names, "中等规模随机：n=10，长度 1~10")

# ---- 点 6：中等规模随机 ----
# n=12；含重复值 + 前缀关系（同一基名加长），考察长度不等的字典序比较。
base = rand_name(LOWER, 3, 5)
names = [base + rand_name(LOWER, 0, 8) if random.random() < 0.5 else base
         for _ in range(12)]
names = [s if s else base for s in names]
write_case(6, 12, names, "中等规模随机：n=12，同基名前缀/重复值混合")

# ---- 点 7：大规模随机 ----
# n=18（接近上限）；采样长度 10~20（本组实际最大 19），混合大小写。
names = [rand_name(MIXED, 10, 20) for _ in range(18)]
write_case(7, 18, names, "大规模随机：n=18 接近上限，长度 10~20 混合大小写")

# ---- 点 8：大规模构造（逆序，最坏比较量）----
# n=19；先随机长名排序，再整体逆序喂入——排序算法的最坏输入形态。
names = sorted(rand_name(LOWER, 15, 20) for _ in range(19))
names.reverse()
write_case(8, 19, names, "大规模构造：n=19 逆序输入（最坏比较量）")

# ---- 点 9：顶格层 ----
# n=20 与名字长度 20 双顶格；大小写混合随机。
names = [rand_name(MIXED, 20, 20) for _ in range(20)]
write_case(9, 20, names, "顶格：n=20、长度 20 双顶格，随机混合大小写")

# ---- 点 10：顶格层（前缀链最坏结构 + 全相等尾部）----
# n=20、长度顶格 20；构造 a, aa, ..., a^20 前缀链，再全相等段，覆盖
# "一个是另一个前缀"的最长公共前缀比较路径与重复值稳定性。
names = ["a" * k for k in range(1, 16)] + ["a" * 20] * 5
write_case(10, 20, names, "顶格：n=20、长度 20；前缀链 + 全相等（最长公共前缀）")

print("ALL 10 CASES GENERATED")
