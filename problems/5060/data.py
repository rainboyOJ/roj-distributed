#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 一本通 2058《【例3.10】简单计算器》分层数据生成器（cyaron）
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2070/data.py
#
# 题意：一行输入「第一个数 第二个数 运算符」，运算符 ∈ {+, -, *, /}，输出表达式结果；
#       除数为 0 → "Divided by zero!"；运算符非法（不为 + - * / 之一）→ "Invalid operator!"。
#
# ---- 数据范围说明（重要，也是本包最大的风险点）----
#   题面（content.md 与官方 OJ 页）**完全没有给出操作数的数值范围**，也没有输出精度约定，
#   只有两个样例：`34 56 +` → `90`、`2 1.2 -` → `0.8`。
#   由样例 2 可知：(a) 操作数可为小数；(b) 结果按「默认浮点输出」打印
#   （C 的 %g / C++ 默认 ostream：6 位有效数字，去掉无意义尾随零，整数不带小数点）。
#   本包据此定义工作范围：|操作数| ≤ 10^6、小数位 ≤ 2；判定约定 = 默认浮点输出（%g 语义）。
#
# ---- 分层维度说明 ----
#   本题每个测试点只有一行输入（没有 n 之类的规模参数），因此规模分层体现为
#   **操作数量级 + 结构/特殊值**，而不是输入长度或组数：
#     特殊值/极端 → 样例量级 → 中等量级（10^3~10^4）→ 大量级（接近 10^6）→ 顶格。
#
# 分层表（10 组）：
#   点 1    边界层｜题面声明的特殊值（1）：除数为 0 → "Divided by zero!"
#   点 2    边界层｜题面声明的特殊值（2）：无效运算符 → "Invalid operator!"
#   点 3    小规模｜答案为 0 的极端：相反数相加（最小量级），检验实现不打印 "-0"
#   点 4    小规模｜答案为 1 的极端：两位小数相加恰为整数 1，检验实现不打印 "1.0"
#   点 5    小规模｜题面样例 1（十位量级整数加法，可手算核对）
#   点 6    小规模｜题面【提示】样例 2（小数减法；结果 0.8，检验尾随零被去除）
#   点 7    中等规模随机｜三位整数与两位小数混合运算（结果约 10^4 量级，可复算）
#   点 8    大规模随机｜接近上限（10^6 邻域）的整数加减，结果越过 10^6
#                    进入默认浮点输出的指数形态（如 1.23456e+06）
#   点 9    顶格层｜接近上限的最坏结构：999999×999999 = 999998000001（12 位精确值）
#                    舍入到 6 位有效数字 → 科学计数法 "9.99998e+11"
#   点 10   顶格层｜上限操作数：1000000×1000000 = 10^12（精确十进制数），
#                    默认浮点输出为科学计数法 "1e+12"（检验实现是否真的采用默认浮点输出）
#
# ---- 平台安全（重要）----
#   生成时对每个样本调用**独立真值**（CPython float + "%g"，glibc 语义）复核 std 输出：
#   本机是 macOS，libc 的 %g 在「舍入后尾数含尾零」的边界情形不会剥尾零
#   （1000005 → "1.00000e+06"，glibc 为 "1e+06"）。这类文本在评测机上会不一致，
#   故随机点采用**重摇直到平台安全**的方式构造；静态点已逐个预先核验。
#
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py

from cyaron import *  # 引入CYaRon的库

import os
import random
import subprocess
import sys

RNG = random.Random(2058)  # 固定种子，保证可复现
STD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "std")


def py_truth(x, y, op):
    """独立真值（glibc 语义）。

    CPython float（IEEE double）运算 + "%g"（6 位有效数字、去尾零）。std 走的是 C 的
    scanf + printf("%g")（本机 macOS libc）；两者数值语义相同，但 macOS libc 存在
    "舍入边界不剥尾零"的已知偏差（见文件头），因此这里用作**平台安全过滤器**：
    只有两者逐字符一致的样本才允许进入数据。
    """
    if op not in "+-*/":
        return "Invalid operator!"
    xf, yf = float(x), float(y)
    if op == "/":
        if yf == 0.0:
            return "Divided by zero!"
        v = xf / yf
    elif op == "+":
        v = xf + yf
    elif op == "-":
        v = xf - yf
    else:
        v = xf * yf
    return "%g" % v


def std_out(x, y, op):
    """调用标程算一次，用于生成 .out 与平台安全比对。"""
    proc = subprocess.run([STD], input=("%s %s %s\n" % (x, y, op)).encode(),
                          capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError("std crashed on %r: %s" % ((x, y, op), proc.stderr.decode()))
    return proc.stdout.decode().strip()


def platform_safe(x, y, op):
    """本机 std 输出是否与独立真值逐字符一致（即跨机语义安全）。"""
    return std_out(x, y, op) == py_truth(x, y, op)


def pick_safe(x_lo, x_hi, y_lo, y_hi, ops, dec_x=0, dec_y=0, want=None):
    """随机摇一组平台安全的 (x, y, op)；最多 2000 次尝试，失败即抛错（绝不静默降级）。

    want: 可选的谓词，接受生成的 input 字符串，用于约束结果的量级分层
          （例如要求结果落在 10^4~10^5，保证“中等规模”名副其实）。
    """
    for _ in range(2000):
        xv, yv = RNG.randint(x_lo, x_hi), RNG.randint(y_lo, y_hi)
        if dec_x:
            x = "%d.%0*d" % (xv, dec_x, RNG.randint(0, 10 ** dec_x - 1))
        else:
            x = str(xv)
        if dec_y:
            y = "%d.%0*d" % (yv, dec_y, RNG.randint(0, 10 ** dec_y - 1))
        else:
            y = str(yv)
        if RNG.random() < 0.5:
            x = "-" + x
        if RNG.random() < 0.5:
            y = "-" + y
        op = RNG.choice(ops)
        inp = "%s %s %s" % (x, y, op)
        if want is not None and not want(inp):
            continue
        if platform_safe(x, y, op):
            return x, y, op
    raise RuntimeError("no platform-safe random case found in 2000 tries")


def result_magnitude(inp):
    """解析一组输入的结果量级（绝对值），用于分层谓词。"""
    x, y, op = inp.split()
    xf, yf = float(x), float(y)
    if op == "/":
        return abs(xf / yf)
    if op == "+":
        return abs(xf + yf)
    if op == "-":
        return abs(xf - yf)
    return abs(xf * yf)


_CACHED_CASES = None


def build_cases():
    """构造 10 组数据（静态点 + 随机点，随机点构造时已通过平台安全过滤）。幂等：结果缓存。"""
    global _CACHED_CASES
    if _CACHED_CASES is not None:
        return _CACHED_CASES

    cases = [
        # ---- 点 1-2：边界层（题面声明的两种特殊情形）----
        (1, "5", "0", "/",
         "边界层｜题面情形（1）除数为 0（除数取最小值 0，运算符合法但除零）"),
        (2, "12", "4", "%",
         "边界层｜题面情形（2）无效运算符（第二位取非零，排除除零判定的干扰）"),
        # ---- 点 3-4：小规模（边界极端：答案取 0 / 取 1）----
        (3, "-6", "6", "+",
         "小规模｜答案为 0 的极端：相反数相加（最小量级），检验实现不打印 -0"),
        (4, "0.25", "0.75", "+",
         "小规模｜答案为 1 的极端：两位小数相加恰为整数 1，检验实现不打印 1.0"),
        # ---- 点 5-6：小规模（题面两个样例，可手算核对）----
        (5, "34", "56", "+",
         "小规模｜题面样例 1（十位量级整数加法，全范围最小量级，可手算）"),
        (6, "2", "1.2", "-",
         "小规模｜题面【提示】样例 2（小数减法；结果 0.8，检验尾随零被去除）"),
    ]

    # ---- 点 7：中等规模随机（三位整数与两位小数相乘，结果落在 10^4~10^5）----
    x7, y7, op7 = pick_safe(100, 999, 10, 99, "*", dec_x=2, dec_y=2,
                            want=lambda s: 1e4 <= result_magnitude(s) < 1e5)
    cases.append((7, x7, y7, op7,
                  "中等规模随机｜三位整数与两位小数相乘，结果落在 10^4~10^5（可复算核对）"))

    # ---- 点 8：大规模随机（接近上限的整数加法，结果落在 10^6~2×10^6）----
    #      默认浮点输出在此量级必须切换为指数形态（>6 位有效数字），是规模分层的"质量标记"
    x8, y8, op8 = pick_safe(500000, 999999, 500000, 999999, "+",
                            want=lambda s: 1.0e6 <= result_magnitude(s) <= 2e6)
    cases.append((8, x8, y8, op8,
                  "大规模随机｜接近上限（10^6 邻域）的整数加法，结果落在 10^6~2×10^6，"
                  "默认浮点输出必须进入指数形态（6 位有效数字不足，如 1.23456e+06）"))

    # ---- 点 9：顶格层（接近上限的最坏结构：12 位精确值 → 6 位有效数字舍入）----
    cases.append((9, "999999", "999999", "*",
                  "顶格层｜接近上限的最坏结构：999999×999999 = 999998000001（12 位精确值）"
                  "舍入到 6 位有效数字 → 科学计数法 9.99998e+11"))

    # ---- 点 10：顶格层（上限操作数相乘 = 10^12，精确十进制数）----
    cases.append((10, "1000000", "1000000", "*",
                  "顶格层｜上限操作数 10^6×10^6 = 10^12（精确十进制数），默认浮点输出为"
                  "科学计数法 1e+12（检验实现是否真的采用默认浮点输出）"))

    _CACHED_CASES = cases
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 10, "must produce exactly 10 test cases"
    for (idx, x, y, op, note) in cases:
        io = IO(file_prefix="problem", data_id=idx)  # problem{idx}.in / problem{idx}.out
        io.input_writeln(x, y, op)                  # 输入格式同题面：两个数 + 运算符，空格分隔
        io.output_gen("../std")                     # .out 由标程生成
        print("problem%-2d: %-12s %-12s %s  -- %s" % (idx, x, y, op, note))


def self_check():
    """生成后立即审计：成对齐全、单行格式、输出与独立真值/手算结论一致。"""
    # 静态可手算的期望值（点 1-6, 9, 10）；点 7-8 用独立真值现算
    fixed = {
        1: "Divided by zero!", 2: "Invalid operator!", 3: "0", 4: "1",
        5: "90", 6: "0.8", 9: "9.99998e+11", 10: "1e+12",
    }
    bad = 0
    for (idx, x, y, op, _note) in build_cases():
        in_path, out_path = "problem%d.in" % idx, "problem%d.out" % idx
        try:
            raw_in = open(in_path, "r", encoding="utf-8").read()
            raw_out = open(out_path, "r", encoding="utf-8").read()
        except OSError as exc:
            print("MISSING pair for point %d: %s" % (idx, exc))
            bad += 1
            continue
        toks = raw_in.split()
        if len(toks) != 3 or toks != [x, y, op] or not raw_in.endswith("\n"):
            print("BAD INPUT problem%d.in: %r" % (idx, raw_in))
            bad += 1
        if not raw_out.endswith("\n") or "\n" in raw_out[:-1]:
            print("BAD OUTPUT FORMAT problem%d.out: %r" % (idx, raw_out))
            bad += 1
        got = raw_out.strip()
        truth = py_truth(x, y, op)
        if got != truth:
            print("OUTPUT != INDEPENDENT TRUTH problem%d: got %r truth %r" % (idx, got, truth))
            bad += 1
        if idx in fixed and got != fixed[idx]:
            print("OUTPUT != HAND-CHECK problem%d: got %r expect %r" % (idx, got, fixed[idx]))
            bad += 1
    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)
    print("SELF-CHECK OK: 10/10 pairs, well-formed, outputs match independent truth"
          " (points 1-6,9,10 also match hand-computed values)")


if __name__ == "__main__":
    main()
    self_check()
