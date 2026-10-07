#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2022《【例4.7】最小n值》分层数据生成器（目标 ROJ 题号 5024）
#
# 题意：输入正整数 m，输出最小的正整数 n，使得
#         H_n = 1 + 1/2 + 1/3 + ... + 1/n >= m。
#   题面数据范围：m <= 11（content.md【提示】），且 m >= 1（题面写明 m 为正整数）。
#   样例：m = 3 -> n = 11。
#   限制：time 1000 ms / memory 64 MB（config.json；官方 OJ 页一致）。
#
# ---------------------------------------------------------------------------
# 【输入域只有 11 个取值：分层策略】
# ---------------------------------------------------------------------------
#   m 的合法取值恰为 {1, 2, ..., 11}，是一个**可完全枚举**的有限域
#   （与 staging/2019《求阶乘》n∈[1,20]、staging/2024《末两位数》n∈[1,1999] 同类）。
#   因此本生成器不引入随机量：10 个测试点取 10 个**互不相同**的固定 m 值，
#   按答案规模（n = 1 -> 4 -> 11 -> 31 -> 83 -> 227 -> 1674 -> 4550 -> 12367 -> 33617）
#   从最小单调铺到顶格，保证不浪费测试点、逐字节可复现。
#
#   精确答案（整数有理数枚举核验，见文末自检；与 OEIS A002387 的 b-file 前 12 项一致）：
#     m  =  1   2   3    4    5    6    7     8     9     10     11
#     n  =  1   4  11   31   83  227  616  1674  4550  12367  33617
#
#   11 个取值只有 10 个测试点名额，缺 m = 7（答案 616）：
#   其正确性由文末**全定义域精确枚举**（m = 1..11 全部 11 个值，含 7）与
#   work/stress.py 的穷举对拍另行覆盖，不占用正式测试点名额。
#
# ---------------------------------------------------------------------------
# 分层表（10 个测试点；本题为单组输入：一个测试点 = 一个整数 m）
# ---------------------------------------------------------------------------
#   点  1  边界层（取等极端）  ：m=1  —— H_1 = 1 **恰好取等**（>= 的等号侧）
#                              -> n=1，本题最小可能答案；`while (s <= m)` 类
#                              off-by-one 会错答 2（已由 work/mutation_check.py 实测）
#   点  2  边界层（最小非平凡）：m=2  —— H_3 = 1.8333 < 2 <= 2.0833 = H_4 -> n=4，可手算
#   点  3  小规模（题面样例）  ：m=3  —— 题面【输入样例】原样 -> n=11，与【输出样例】对齐
#   点  4  小规模              ：m=4  —— n=31（循环 31 次），可手算核对量级
#   点  5  中等规模            ：m=5  —— n=83
#   点  6  中等规模（精度最紧）：m=6  —— n=227；m - H_226 = 3.86e-5，是 11 个 m 中
#                              「前一步缺口 /(1/n)」最小者（0.0088），浮点容错最吃紧的一档
#   点  7  大规模              ：m=8  —— n=1674，进入千级循环
#   点  8  大规模              ：m=9  —— n=4550
#   点  9  顶格前一档          ：m=10 —— n=12367
#   点 10  顶格层（题面上限）  ：m=11 —— n=33617，最坏规模（循环 33617 次；std 实测 < 1 ms）
#
# ---------------------------------------------------------------------------
# 与任务书通用分层清单的对照（不适用/越界项如实说明，不强行凑数）
# ---------------------------------------------------------------------------
#   - 「n=1 / n=2 的组数分层」：本题为**单组输入**（一个测试点一个整数 m），
#     不存在"数据组数"；等价落点是输入域两端 m=1 / m=2（点 1、点 2）。
#   - 「全最小值 / 全最大值」：点 1（m=1）/ 点 10（m=11 题面上限）。
#   - 「答案为 0 或 1 的极端」：答案不可能为 0（m >= 1 时 H_1 = 1 即已满足 m=1）；
#     答案 1 仅当 m = 1（H_1 >= 1 恰好取等），由点 1 覆盖。
#   - 「题面声明的特殊值」：点 3（题面样例 m=3 -> 11）。
#   - 「小/中/大/顶格随机」：输入域可完全枚举（仅 11 个值），按**答案规模分档**
#     （1 / 31 / 83 / 227 / 1674 / 4550 / 12367 / 33617 单调铺开），不使用随机，
#     以保证逐字节可复现且不与边界点重复覆盖。四个档位都有真实落点：
#     小规模（点 3-4）、中等（点 5-6）、大规模（点 7-8）、顶格（点 9-10）。
#   - 「有序/逆序/链/重复值等结构构造」：输入是单个整数，无序列/图结构可构造，不适用。
#
# 生成方式：cyaron 的 IO(file_prefix="problem", data_id=i) + io.output_gen("../std")，
#   与 problems/1000/data.py、staging/2019、staging/2020 一致（单整数输入用
#   io.input_write(m)，.in 为一行十进制数字、无行尾换行）。
#
# 【cyaron 静默失败防护（本轮复核补强）】
#   CYaRon 的 io.output_gen() 只是把 std 的 stdout 重定向进 .out：std 不存在、
#   不可执行或启动失败时**不会报错**，会静默留下 0 字节 .out（假数据）。因此本脚本：
#   (a) 生成前校验 ../std 存在且可执行；std.cpp 比 std 新时告警提示重新编译；
#   (b) 生成前删除上一轮的 problem*.in/.out，防止旧产物掩盖本轮静默失败；
#   (c) 每点生成后立刻断言 .in/.out 均存在且非空，再进入下一轮；
#   (d) 全部生成后按行数/逐字节核对 .in/.out，并用 big-int 精确枚举复算答案。

import os
import sys
from fractions import Fraction

from cyaron import *  # 引入 CYaRon 的库

HERE = os.path.dirname(os.path.abspath(__file__))
M_MIN, M_MAX = 1, 11  # 题面：m 为正整数且 m <= 11
STD_TIME_LIMIT = 20    # output_gen 调 std 的单点超时（秒）；std 实测最大点 < 1 ms

# 精确答案表（m -> 最小 n）。由文末 big-int 全定义域枚举核验，且与 OEIS A002387
# 的 b-file（Least k such that H(k) > n）第 0..11 项 1,2,4,11,31,83,227,616,1674,
# 4550,12367,33617 逐项一致（本题 >= 与 OEIS > 的等号差异只影响 m=1 的 H 取等情形，
# 已由自检中的取等断言单独覆盖）。
EXPECTED = {
    1: 1, 2: 4, 3: 11, 4: 31, 5: 83, 6: 227,
    7: 616, 8: 1674, 9: 4550, 10: 12367, 11: 33617,
}

# (测试点号, m, 层次, 设计意图)
PLAN = [
    (1, 1, "边界层（取等极端）",
     "m=1：全最小值，H_1=1 恰好取等（>= 的等号侧）-> n=1（本题最小可能答案）；"
     "`while(s<=m)` 类 off-by-one 会错答 2"),
    (2, 2, "边界层（最小非平凡）",
     "m=2：H_3=1.8333<2<=2.0833=H_4 -> n=4，可手算"),
    (3, 3, "小规模（题面样例）",
     "m=3：题面【输入样例】原样 -> n=11，与【输出样例】对齐"),
    (4, 4, "小规模",
     "m=4 -> n=31（循环 31 次），可手算核对量级"),
    (5, 5, "中等规模",
     "m=5 -> n=83"),
    (6, 6, "中等规模（精度最紧）",
     "m=6 -> n=227；m-H_226=3.86e-5 是 11 个 m 中「前一步缺口/(1/n)」最小者（0.0088），"
     "浮点容错最吃紧的一档"),
    (7, 8, "大规模",
     "m=8 -> n=1674，进入千级循环"),
    (8, 9, "大规模",
     "m=9 -> n=4550"),
    (9, 10, "顶格前一档",
     "m=10 -> n=12367"),
    (10, 11, "顶格层（题面上限）",
     "m=11 为题面数据范围最大值 -> n=33617，最坏规模（循环 33617 次）"),
]

N_BOUND = max(EXPECTED.values())  # 33617：精确枚举的 n 上界


# --------------------------------------------------------------------------
# 精确参考实现（与 std 的浮点路径完全无关的 big-int 有理数枚举）
# --------------------------------------------------------------------------

def _primes_upto(n):
    """<= n 的素数表（埃氏筛）。"""
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def lcm_1_to(n):
    """L = lcm(1..n) = 每个 <= n 的素数的最高次幂之积（精确整数）。"""
    L = 1
    for p in _primes_upto(n):
        pk = p
        while pk * p <= n:
            pk *= p
        L *= pk
    return L


def exact_scan(n_bound=N_BOUND, m_values=range(M_MIN, M_MAX + 1)):
    """精确有理数枚举：令 L = lcm(1..n_bound)，A_n = sum_{i<=n} L//i（整数），
    则 H_n = A_n / L，判定 H_n >= m 等价于 A_n >= m*L —— 全程整数运算，
    与任何浮点实现完全无关。

    返回 (L, {m: (最小 n, A_{n-1}, A_n)})。
    由于 n=1 时 A_1 = L >= m*L 仅当 m=1，m=1 的取等情形自然落在 n=1。
    """
    L = lcm_1_to(n_bound)
    targets = {m: m * L for m in m_values}
    res = {}
    s = 0  # A_0
    for n in range(1, n_bound + 1):
        prev_s = s
        s += L // n
        for m in list(targets):
            if s >= targets[m]:
                res[m] = (n, prev_s, s)
                del targets[m]
        if not targets:
            break
    if targets:
        raise AssertionError("精确枚举的 n 上界 %d 不足：缺 %s" % (n_bound, sorted(targets)))
    return L, res


# --------------------------------------------------------------------------
# 主流程：生成 10 组 -> 生成后自检（读回 .in/.out 逐字节比对 + 精确枚举复算）
# --------------------------------------------------------------------------

def main():
    # 无论从 staging/2022/ 还是从 data/ 调用，都写到 staging/2022/data/，
    # 使 `python3 data.py` 与仓库惯例 `mkdir -p data && cd data && python3 ../data.py`
    # 两种方式行为一致。
    data_dir = os.path.join(HERE, "data")
    os.makedirs(data_dir, exist_ok=True)
    if os.path.abspath(os.getcwd()) != os.path.abspath(data_dir):
        os.chdir(data_dir)

    # ---------------- 生成前防护（a）：std 必须存在且可执行 ----------------
    std_path = os.path.join(HERE, "std")   # io.output_gen("../std") 相对 data/ 解析
    if not os.path.isfile(std_path):
        raise SystemExit("缺少标程 %s：请先执行 `g++ -O2 -std=c++17 std.cpp -o std`" % std_path)
    if not os.access(std_path, os.X_OK):
        raise SystemExit("标程 %s 无执行权限：请 `chmod +x std`" % std_path)
    std_cpp = os.path.join(HERE, "std.cpp")
    if os.path.isfile(std_cpp) and os.path.getmtime(std_cpp) > os.path.getmtime(std_path):
        print("⚠ 告警：std.cpp 比 std 新（改了标程未重编？）：%s" % std_path)

    # ---------------- 生成前防护（b）：清掉旧产物，防旧文件掩盖静默失败 ----------------
    for i, _, _, _ in PLAN:
        for suffix in ("in", "out"):
            stale = "problem%d.%s" % (i, suffix)
            if os.path.exists(stale):
                os.remove(stale)

    # ---------------- 生成 ----------------
    for i, m, layer, note in PLAN:
        io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
        io.input_write(m)          # 单组输入：一行一个正整数 m（语料惯例，无行尾换行）
        io.output_gen("../std", time_limit=STD_TIME_LIMIT)  # 调 ../std 生成 .out
        io.close()                 # 显式关闭，确保缓冲落盘后自检能读到完整内容

        # 生成后防护（c）：output_gen 静默失败时 .out 会是 0 字节，必须当场查觉
        for suffix in ("in", "out"):
            produced = "problem%d.%s" % (i, suffix)
            if not os.path.isfile(produced) or os.path.getsize(produced) == 0:
                raise SystemExit("点 %d：生成后 %s 缺失或为空 —— ../std 未产出？" % (i, produced))

    # ---------------- 生成后自检 ----------------
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    # (1) 全定义域精确枚举（m=1..11，含未占测试点的 m=7），与答案表逐项核对
    L, scan = exact_scan()
    for m in range(M_MIN, M_MAX + 1):
        check(m in scan, "精确枚举缺 m=%d" % m)
        if m in scan:
            check(EXPECTED[m] == scan[m][0],
                  "m=%d 的精确答案 %d 与答案表 %d 不符" % (m, scan[m][0], EXPECTED[m]))

    # (2) 临界结构断言（解释器内独立核对设计意图，而非套用 std）
    n1, prev1, cur1 = scan[1]
    check(n1 == 1 and prev1 == 0 and cur1 == L,
          "m=1 应恰在 n=1 处取等（H_1 = 1，即 A_1 = L）")
    _, prev6, cur6 = scan[6]
    gap6 = 6 * L - prev6
    check(0 < gap6 and gap6 * 227 * 20 < L,
          "m=6 的前一步缺口不在预期量级（应 < (1/227)/20）")
    _, prev11, cur11 = scan[11]
    gap11 = 11 * L - prev11
    check(0 < gap11 and gap11 * 33617 < L,
          "m=11 的前一步缺口不在预期量级（应 < 1 个单项 1/33617）")

    # (3) 每个测试点：读回 .in/.out 逐字节比对 + 最小性断言
    for i, m, layer, note in PLAN:
        in_path = "problem%d.in" % i
        out_path = "problem%d.out" % i
        raw_in = open(in_path, "r", encoding="utf-8").read()
        raw_out = open(out_path, "r", encoding="utf-8").read()

        # 行数/形状断言（防静默空文件或多余行）
        check(raw_in.count("\n") == 0, "点 %d：.in 应恰 1 行（无行尾换行），实有 %d 个换行" % (i, raw_in.count("\n")))
        check(raw_out.count("\n") == 1 and raw_out.endswith("\n"),
              "点 %d：.out 应恰 1 行且以换行结尾，实为 %r" % (i, raw_out))

        check(raw_in == str(m), "点 %d：.in 应为 %r，实为 %r" % (i, str(m), raw_in))
        check(raw_out == "%d\n" % EXPECTED[m],
              "点 %d：.out 应为 %r，实为 %r" % (i, "%d\n" % EXPECTED[m], raw_out))

        if m in scan:
            n, prev_s, cur_s = scan[m]
            check(n == EXPECTED[m], "点 %d：精确枚举答案 %d != 答案表 %d" % (i, n, EXPECTED[m]))
            # 最小性：前一步尚未达到，当前步首次达到
            check(prev_s < m * L <= cur_s,
                  "点 %d：n=%d 不是最小满足 H_n >= %d 的 n" % (i, n, m))

    # (4) 分层结构性断言
    ms = [m for _, m, _, _ in PLAN]
    check(ms == sorted(ms), "10 个测试点的 m 应单调不减（从最小铺到顶格）")
    check(len(set(ms)) == len(ms), "10 个测试点的 m 应互不相同（不浪费测试点）")
    check(ms[0] == M_MIN and ms[-1] == M_MAX, "首点应为下界 m=1，末点应为上限 m=11")
    check(len(ms) == 10 and ms[2] == 3, "点 3 应为题面样例 m=3")
    check(set(ms) == set(range(M_MIN, M_MAX + 1)) - {7},
          "10 个测试点应为全定义域去掉 m=7（m=7 由全定义域枚举与对拍另行覆盖）")

    # ---------------- 输出与总结 ----------------
    print("点 |  m | 答案 n | 层次               | 设计意图")
    print("---+----+--------+--------------------+------------------------------------------")
    for i, m, layer, note in PLAN:
        n = EXPECTED[m]
        print("%2d | %2d | %6d | %-18s | %s" % (i, m, n, layer, note))

    print()
    print("精确枚举（big-int，11 个取值全量）：", flush=False)
    print("  m  = " + " ".join("%6d" % m for m in range(1, 12)))
    print("  n  = " + " ".join("%6d" % EXPECTED[m] for m in range(1, 12)))
    print("临界量级：m=1 取等（H_1-1 = 0）；"
          "m=6 前一步缺口 %.3e = %.4f x (1/227)；"
          "m=11 前一步缺口 %.3e = %.4f x (1/33617)"
          % (float(Fraction(gap6, L)), float(Fraction(gap6 * 227, L)),
             float(Fraction(gap11, L)), float(Fraction(gap11 * 33617, L))))

    if problems:
        print("\n自检失败：", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        raise SystemExit(1)
    print("\n自检通过：10/10 组 .in/.out 成对且逐字节符合精确答案；"
          "全定义域 m=1..11（含未占点的 m=7 -> 616）的精确有理数枚举与答案表一致。")


if __name__ == "__main__":
    main()
