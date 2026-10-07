#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2026《【例4.12】阶乘和》分层数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2070/data.py
#
# 题意：输入正整数 n，输出 S = 1! + 2! + 3! + ... + n!。样例：n=3 -> 9。
# 数据范围（题面【提示】明文，官方 OJ 页同）：1 <= n <= 10。
# 限制：time 1000 ms / memory 65536 KB（config.json 与官方 OJ 页一致）。
#
# ---- 分层策略（本包与常规题的差异，必须说明）----
#   题面声明的输入域只有 {1,2,...,10} 共 **10 个可能取值**，而测试点恰好也有 10 组。
#   因此本题唯一正确的"分层"不是抽样，而是**把整个输入域穷举覆盖**：
#   10 个测试点 = n=1..10 各一次，一个不漏、不重复。这比"小/中/大随机"更强 ——
#   随机抽样在 10 点上必然漏掉部分取值，而穷举保证任何 off-by-one、初值错误、
#   提前终止、上界写成 n<10 或 n<=9 的错误实现都至少挂在 1 个点上。
#   层次仍按答案量级（位数 / 阶乘表跨越点）标注，对应任务书要求的"从最小铺到顶格"：
#
#   分层表（10 组；单组输入题，一个测试点 = 一个 n）：
#     点 1  边界层｜n = 1（全最小值，答案 1 = 1!，本题答案最小值；检验 term/sum 初值）
#     点 2  边界层｜n = 2（最小非平凡值，答案 3 = 1!+2!；与点 1 相邻对比，
#                    检验累加是否漏项：只算 n! 的实现会得 2，只算 1! 会得 1）
#     点 3  小规模｜n = 3（题面【输入样例】声明的特殊值，答案 9，与题面样例逐字节一致）
#     点 4  小规模｜n = 4（答案 33，首位进入两位数；可手算 1+2+6+24）
#     点 5  小规模｜n = 5（答案 153，三位数，可手算 33+120）
#     点 6  中等规模｜n = 6（答案 873，3 位数；本题区间中点，检验累加不截断）
#     点 7  中等规模｜n = 7（答案 5913，首位进入四位数；跨过 4 位数量级门槛）
#     点 8  大规模｜n = 8（答案 46233，5 位数；10! 量级的中段）
#     点 9  大规模｜n = 9（答案 409113，6 位数；接近上限）
#     点 10 顶格层｜n = 10（题面上限，答案 4037913，7 位数，本题最大规模最坏点）
#
#   说明：本题输入只有一个整数 n，不存在"多组数据按组数分层"；也没有可选择的
#   "结构"（输入域就是一维有序整数），故结构陷阱由点 1/2/7/10 的"量级门槛"承担。
#   点 1-10 覆盖 1..10 每个取值恰好一次，无随机点，数据完全确定、可复现、手算可核。
#
# ---- 精度口径 ----
#   本题**全程整数运算，无浮点**：不存在 2058（staging/2058/gen-report.md 教训）那类
#   %g / printf 尾零与指数形态的跨平台文本差异。输出为精确十进制整数 + 单个换行，
#   macOS / glibc / Windows 结果逐字节一致，故本包无需"平台安全过滤"。
#   上界 S(10) = 4037913 远小于 int 上限，int 实现亦不溢出（long long 更安全，见 std.cpp）。

from cyaron import *  # 引入CYaRon的库

import math
import os

NMIN, NMAX = 1, 10  # 题面【提示】明文范围

# 每个测试点：(data_id, n, 分层标注)
# 断言 n 覆盖 [NMIN, NMAX] 全部取值且不重复（穷举，见文件头"分层策略"）。
CASES = [
    (1, 1, "边界层｜全最小值 n=1，答案 1（=1!，答案最小值）；检验 term/sum 初值"),
    (2, 2, "边界层｜最小非平凡 n=2，答案 3=1!+2!；检验累加不漏项（只算 n! 会得 2）"),
    (3, 3, "小规模｜题面【输入样例】值 n=3，答案 9（与样例逐字节一致，可手算）"),
    (4, 4, "小规模｜n=4，答案 33（首位进入两位数量级，可手算 1+2+6+24）"),
    (5, 5, "小规模｜n=5，答案 153（三位数，可手算 33+120）"),
    (6, 6, "中等规模｜n=6，答案 873（本题区间中点，检验累加不截断）"),
    (7, 7, "中等规模｜n=7，答案 5913（首位进入四位数量级，跨越量级门槛）"),
    (8, 8, "大规模｜n=8，答案 46233（5 位数，接近上限的中段）"),
    (9, 9, "大规模｜n=9，答案 409113（6 位数，逼近上限）"),
    (10, 10, "顶格层｜题面上限 n=10，答案 4037913（7 位数，最大规模最坏点；10!=3628800）"),
]

assert len(CASES) == 10, "必须恰好 10 个测试点"
assert sorted(n for _, n, _ in CASES) == list(range(NMIN, NMAX + 1)), \
    "10 个测试点必须穷举覆盖 n=1..10（不重不漏）"


def truth(n):
    """独立真值（CPython 任意精度整数）：S(n) = sum_{k=1..n} k!。

    与 std.cpp 的编译期 C 整数运算完全无关，是第三条独立路径（stdlib 大整数），
    用于逐点核对 std 的输出文本，防止标程自身算错。
    """
    return sum(math.factorial(k) for k in range(1, n + 1))


def gen_case(data_id, n, note):
    """写出第 data_id 组：输入 n，输出由 std 生成；并打印独立真值供人工核对。"""
    assert NMIN <= n <= NMAX, "n=%d 超出题面范围 [%d,%d]" % (n, NMIN, NMAX)
    io = IO(file_prefix="problem", data_id=data_id)  # problem{data_id}.in / .out
    io.input_writeln(n)          # 单行输入，行末带换行（与 2070/2052 等较新包一致）
    io.output_gen("../std")      # .out 由 std 生成
    print("problem%-2d: n=%-2d 期望值=%-8d -- %s" % (data_id, n, truth(n), note))


def self_check():
    """生成后立即审计：成对齐全、格式合规、输出与任意精度独立真值逐字节一致。"""
    bad = 0
    for data_id, n, _note in CASES:
        in_path, out_path = "problem%d.in" % data_id, "problem%d.out" % data_id
        try:
            raw_in = open(in_path, "r", encoding="utf-8").read()
            raw_out = open(out_path, "r", encoding="utf-8").read()
        except OSError as exc:
            print("MISSING pair for point %d: %s" % (data_id, exc))
            bad += 1
            continue
        if raw_in != "%d\n" % n:
            print("BAD INPUT problem%d.in: %r (expect %r)" % (data_id, raw_in, "%d\n" % n))
            bad += 1
        if raw_out != "%d\n" % truth(n):
            print("OUTPUT != TRUTH problem%d: got %r expect %r"
                  % (data_id, raw_out, "%d\n" % truth(n)))
            bad += 1
    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)
    print("SELF-CHECK OK: 10/10 pairs, well-formed, outputs == exact big-int truth"
          " (n=1..10 穷举覆盖)")


if __name__ == "__main__":
    for _data_id, _n, _note in CASES:
        gen_case(_data_id, _n, _note)
    self_check()
