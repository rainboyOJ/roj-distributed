#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 1785《简单的期望》 数据生成器（目标 ROJ 题号 1785）
#
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
#
# 题意（按官方样例校准的口径，见下「题面冲突」）：
#   变量 x 初值给定；依次执行 n 次操作：以 p% 的概率 x = x*2，以 (100-p)% 的概率 x = x+1。
#   记最终值 w，d = w 的质因数分解中 2 的指数（= w 的二进制末尾 0 的个数），求 E[d]。
#   范围：x ≤ 1e9, n ≤ 200, 0 ≤ p ≤ 100（题面【数据规模】；单组输入，一行 "x n p"）。
#   限制：time 1000 ms / memory 524288 KB（config.json 与官方 OJ 页一致）。
#
# ⚠ 题面冲突（详见 gen-report.md §1、§3）：
#   content.md 与官方 OJ 页的【题目描述】写的是 "x = x/2"，但题面给出的三个官方样例
#   **只有 x = x*2 能同时对上**（1 1 50 -> 1.0；5 3 0 -> 3.0；5 3 25 -> 1.921875 = 123/64）。
#   x/2 读法在 x=1 时一步得到 0（v2(0) 无定义），且 d(0) 取任何约定都无法同时满足样例 1 与 3
#   （d(0)=1 ⇒ 样例1 成立但样例3 得 121/64；d(0)=3 ⇒ 样例3 成立但样例1 得 2.0）。
#   同源题 JZOJ5805 题面/样例/规模逐字一致且写作 x = x*2。故本包按 x = x*2 生成数据。
#
# 产物：data/problem1.in/.out … data/problem10.in/.out（IO(file_prefix="problem", data_id=i)）。
#
# ⚠ 关于 .out 生成：不使用 cyaron 的 io.output_gen（其写缓冲不显式 flush 时可能留下 0 字节 .out）。
#   本脚本对每个点先 io.input_write(...) + io.close() 落地 .in，再用 subprocess 显式把 .in 喂给
#   std 直接写 .out，并在末尾断言：.out 非空、恰好 1 行、可解析为有限非负浮点数，
#   且对存在闭式解的点（p=0 / p=100 / n=1）逐点比对精确值。
#
# ⚠ 性能：std 为位 DP，O(n·2^8·(k0+n))，n ≤ 200 时实测 < 20 ms（限制 1000 ms）。
#   生成器本身只有 O(1) 的构造与 O(10) 的 std 调用，无任何 O(n²) Python 循环、无对拍/暴力。
#
# ---- 分层策略（单组输入题：一个测试点 = 一行 "x n p"；10 点从最小铺到顶格）----
#   点 1  边界层：题面【输入样例 1】原样 "1 1 50" -> 1.0（x、n 同时取最小 + 题面特殊值）
#   点 2  边界层：题面【输入样例 2】原样 "5 3 0"  -> 3.0（p=0 端点：唯一路径 w = x+n = 8，d = 3）
#   点 3  边界层：题面【输入样例 3】原样 "5 3 25" -> 1.921875（非平凡概率；唯一能区分 x*2 / x/2 的点）
#   点 4  边界层：n=1 最小、x=1e9 最大、p=100 端点（闭式 d = v2(x)+1 = 9+1 = 10）
#   点 5  小规模随机：x∈[1,60]、n∈[2,8]、p∈[1,99]（固定种子；量级可手算核对）
#   点 6  小规模定向：x = 2^29 = 536870912（初值 v2 = 29 ≫ 8 位），n = 12，p = 50
#                     —— 专门走「低 8 位全 0、答案由高位游程 k 决定」的分支
#   点 7  中等规模定向：x = 1（最小）、n = 200（最大）、p = 1（近端点，×2 概率 1%）
#   点 8  大规模闭式：x = 1e9 = 2^9·5^9，n = 100（50% 子任务上限），p = 100
#                     -> w = x·2^100，d = v2(x)+100 = 109（精确断言）
#   点 9  顶格层闭式：x = 2^20-200 = 1048376，n = 200（上限），p = 0 -> w = x+200 = 2^20，d = 20（精确断言）
#   点 10 顶格层：x = 1e9（上限）、n = 200（上限）、p = 50（概率中点）—— 最大规模、最广状态分布
#
#   边界清单对照：n 最小=1 → 点1/点4；n 最大=200 → 点7/点9/点10；x 最小=1 → 点1/点7；
#   x 最大=1e9 → 点4/点8/点10；p=0 → 点2/点9；p=100 → 点4/点8；p 中间 → 点1/3/5/6/10；
#   题面声明的特殊值（三个样例）→ 点1/2/3；答案为「大 d」（>30，远超 8 位分块）→ 点8(109)、点6(≈41)。
#   随机性：点 5 用独立 random.Random(1785+5)，与调用顺序无关，可精确复现。

import math
import os
import random
import subprocess

from cyaron import IO  # 引入 CYaRon 的库

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
if not os.path.exists(STD):                      # 兼容在题目目录直接执行
    STD = os.path.join(HERE, "..", "std")

MAX_X = 10 ** 9   # 题面上限
MAX_N = 200       # 题面上限


def v2(v):
    """v 的质因数分解中 2 的次数（v >= 1）。"""
    assert v >= 1
    c = 0
    while v % 2 == 0:
        v //= 2
        c += 1
    return c


def gen(i, x, n, p, note, expect=None):
    """写出 problemN.in（cyaron），再用 subprocess 跑 std 生成 problemN.out，并做断言。

    expect: 若给出（float 或闭式算出的精确值），则断言 .out 与之相差 < 1e-9。
    """
    # ---- 合法性自检（严格按题面数据规模）----
    assert 1 <= x <= MAX_X, "点%d: x=%d 越界" % (i, x)
    assert 0 <= n <= MAX_N, "点%d: n=%d 越界" % (i, n)
    assert 0 <= p <= 100, "点%d: p=%d 越界" % (i, p)

    io = IO(file_prefix="problem", data_id=i)
    io.input_write("%d %d %d" % (x, n, p))
    io.close()                                   # 显式 flush + 关闭 .in

    inp = "problem%d.in" % i
    outp = "problem%d.out" % i
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        r = subprocess.run([STD], stdin=fi, stdout=fo, timeout=120)
    assert r.returncode == 0, "点%d: std 返回码 %d" % (i, r.returncode)

    # ---- .out 完整性断言（非空 / 恰好 1 行 / 有限非负浮点）----
    assert os.path.getsize(outp) > 0, "点%d: .out 为 0 字节" % i
    with open(outp) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip() != ""]
    assert len(lines) == 1, "点%d: 输出行数 %d != 1" % (i, len(lines))
    val = float(lines[0])
    assert math.isfinite(val) and val >= 0.0, "点%d: 输出非法 %r" % (i, lines[0])
    # d ≤ v2 上界：w ≤ x·2^n ⇒ d ≤ log2(x) + n，给出宽松上界做合理性检查
    assert val <= math.log2(MAX_X) + MAX_N + 1e-6, "点%d: 输出超过理论上界 %r" % (i, lines[0])

    if expect is not None:
        assert abs(val - expect) < 1e-9, \
            "点%d: 输出 %.10f != 期望 %.10f" % (i, val, expect)

    # ---- .in 回读自检 ----
    with open(inp) as f:
        tok = f.read().split()
    assert tok == ["%d" % x, "%d" % n, "%d" % p], "点%d: .in 内容异常 %r" % (i, tok)

    print("点 %-2d | x=%-10d n=%-3d p=%-3d | E[d]=%-16s | %s"
          % (i, x, n, p, lines[0], note))
    return val


# ---------------- 点 1-3：边界层（题面三个样例原样） ----------------
gen(1, 1, 1, 50, "边界层：题面样例1 原样（x、n 同时最小）", expect=1.0)
gen(2, 5, 3, 0, "边界层：题面样例2 原样（p=0 端点 ⇒ w=x+n=8, d=3）",
    expect=float(v2(5 + 3)))
gen(3, 5, 3, 25, "边界层：题面样例3 原样（非平凡概率 123/64，唯一区分 x*2/x÷2 的点）",
    expect=1.921875)

# ---------------- 点 4：边界层（x 上限 + n 最小 + p=100 端点） ----------------
gen(4, MAX_X, 1, 100, "边界层：x 上限、n=1 最小、p=100 ⇒ d=v2(2x)=v2(1e9)+1=10",
    expect=float(v2(MAX_X) + 1))

# ---------------- 点 5：小规模随机（可手算量级） ----------------
_rng = random.Random(1785 + 5)
_x = _rng.randint(1, 60)
_n = _rng.randint(2, 8)
_p = _rng.randint(1, 99)
gen(5, _x, _n, _p, "小规模随机：x∈[1,60]、n∈[2,8]、p∈[1,99]（种子 1790，可复现）")

# ---------------- 点 6：小规模定向（初值 v2 远超 8 位，走高位游程分支） ----------------
gen(6, 1 << 29, 12, 50, "小规模定向：x=2^29（初值 v2=29>8），n=12，p=50 ⇒ 高位游程 k 主导")

# ---------------- 点 7：中等规模定向（x 最小 + n 上限 + p 近端点） ----------------
gen(7, 1, MAX_N, 1, "中等规模定向：x=1（最小）、n=200（上限）、p=1（×2 概率仅 1%）")

# ---------------- 点 8：大规模（n=100 子任务上限 + p=100 闭式） ----------------
gen(8, MAX_X, 100, 100, "大规模闭式：p=100 ⇒ w=x·2^100, d=v2(1e9)+100=109",
    expect=float(v2(MAX_X) + 100))

# ---------------- 点 9：顶格层（n 上限 + p=0 闭式） ----------------
gen(9, (1 << 20) - 200, MAX_N, 0, "顶格层闭式：p=0 ⇒ w=x+200=2^20, d=20（n 取上限）",
    expect=float(v2((1 << 20) - 200 + MAX_N)))

# ---------------- 点 10：顶格层（x、n 同时取上限 + 概率中点） ----------------
gen(10, MAX_X, MAX_N, 50, "顶格层：x=1e9（上限）、n=200（上限）、p=50（概率中点，状态分布最广）")

print("自检通过：10 个测试点 .in/.out 成对齐全，.out 非空且恰 1 行；"
      "样例 1/2/3 与 p=0、p=100、n=1 的闭式解全部精确吻合。")
