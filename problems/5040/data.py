#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2038《【例5.5】最大数位置》（目标 ROJ 题号 5040）数据生成器
#
# 题面（.ybt-import/staging/2038/content.md，与官方页
# http://ybt.ssoier.cn:8088/problem_show.php?pid=2038 逐字一致）：
#   输入 n 个整数，存放在数组 a[1] 至 a[n] 中，输出最大数所在位置（n <= 1000）。
#   第一行：数的个数 n；第二行：n 个正整数，每个数在 2^32-1 之内。
#   输出：最大数所在位置（1-based 下标）。
#
# 【数据范围与本题两个真实陷阱】
#   1. 值域上界 = 2^32-1 = 4294967295 > INT_MAX(2147483647)。用 int 读入 >= 2^31
#      的数会溢出（UB），公开题解里 `int a[1005]` 的写法在这个值域上不安全；
#      本组数据按题面把上限值（2^32-1）真正造出来。
#   2. 多个最大值时须输出**第一个**（最左）出现的位置；所有题解都用「严格大于才更新」
#      实现（见 gen-report.md 来源 1/2/4），故本组数据专门造了全相等、小值域大量重复
#      的结构来压这一语义。
#   数组本身是 1-based（a[1]..a[n]），答案范围为 [1, n]，故用点 1 覆盖答案=1、
#   点 10 覆盖答案=n 两个极端。（本题结构上不存在「答案为 0」的测试点。）
#
# 【分层设计（10 个测试点，从最小铺到顶格）】
#   点 1-2  边界层：n=1 全最小值（答案=1 极端）/ n=2 且值取到题面上限 2^32-1（末位）
#   点 3-4  小规模：题面【输入样例】（可手算）/ n=12 的随机小数据（可手算）
#   点 5-6  中等规模随机：n≈200 / n≈500，值域取满 [1, 2^32-1]
#   点 7-8  大规模随机：n≈900 / n=1000；点 7 用小值域造大量重复（压 tie 语义）
#   点 9-10 顶格层：n=1000 全相等（全部取上界值，答案=1 的最坏 tie 结构）/
#                    n=1000 严格递增且末位=2^32-1（答案=n=1000，压「最右」与越界）
#
# 【自检】每个点用与 std 结构不同的 Python 参照（max + index）复算期望答案，
#   回读刚生成的 .out 逐点比对；并 assert 校验 n <= 1000、取值均落在 [1, 2^32-1]。
#
# 【随机性】每点使用独立 random.Random(2038 + 点号)，与调用顺序无关，可精确复现。

from cyaron import *  # 引入CYaRon的库

import random

MAXN = 1000          # n 的上限（题面：n <= 1000）
MAXV = 2 ** 32 - 1   # 每个数的上限（题面：每个数在 2^32-1 之内）；正整数低下限为 1

# 已生成测试点的记录，末尾汇总打印
_pts = []


def expected_answer(vals):
    """与 std 结构不同的参照：先求最大值，再取第一次出现的位置（1-based）。"""
    return vals.index(max(vals)) + 1


def gen(i, vals, note):
    """生成第 i 组数据，并用 Python 参照复算校验 std 输出。"""
    assert 1 <= len(vals) <= MAXN, "problem%d: n 越界" % i
    assert all(1 <= v <= MAXV for v in vals), "problem%d: 值越出 [1, 2^32-1]" % i

    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(len(vals))                # 第一行：数的个数 n
    io.input_writeln(vals)                     # 第二行：n 个正整数（一行空格分隔）
    io.output_gen("../std")                    # 由编译好的 std 生成 .out
    io.output_file.flush()                     # cyaron 不自动 flush，先落盘再读回复算

    exp = expected_answer(vals)
    got = open("problem%d.out" % i).read().strip()
    assert got == str(exp), \
        "problem%d: std 输出 %r 与参照 %d 不一致" % (i, got, exp)
    _pts.append((i, len(vals), exp))
    print("problem%-2d: n=%-4d 答案=%-4d -- %s" % (i, len(vals), exp, note))


def rnd_vals(i, n, lo, hi):
    """生成 n 个 [lo,hi] 内的随机值。

    每个点用独立 Random(2038+i)，与调用顺序无关、可精确复现。
    """
    rng = random.Random(2038 + i)
    return [rng.randint(lo, hi) for _ in range(n)]


# ---- 点 1-2：边界层 ----
gen(1, [1],
    "边界层：n=1 且取全最小值 1（最小规模 + 答案=1 的下端极端）")
gen(2, [2147483648, MAXV],
    "边界层：n=2，两数分别取 2^31（=INT_MAX+1，int 读入即溢出）与题面上限 2^32-1（末位）")

# ---- 点 3-4：小规模（可手算） ----
gen(3, [67, 43, 90, 78, 32],
    "小规模：题面【输入样例】，答案 3（题面唯一声明值，可手算核对）")
gen(4, rnd_vals(4, 12, 1, 20),
    "小规模随机：n=12、值域 [1,20]，量级小到可心算验证")

# ---- 点 5-6：中等规模随机 ----
gen(5, rnd_vals(5, 200, 1, MAXV),
    "中等规模随机：n=200、值域取满 [1, 2^32-1]（全 32 位无符号值域）")
gen(6, rnd_vals(6, 500, 1, MAXV),
    "中等规模随机：n=500、值域取满 [1, 2^32-1]")

# ---- 点 7-8：大规模随机（接近上限） ----
gen(7, rnd_vals(7, 900, 1, 30),
    "大规模随机：n=900、值域压到 [1,30]（大量重复值，压「多个最大值取最左」语义）")
gen(8, rnd_vals(8, MAXN, 1, MAXV),
    "大规模随机：n=1000（顶格）、值域取满 [1, 2^32-1]")

# ---- 点 9-10：顶格层（上限 + 最坏结构） ----
gen(9, [MAXV] * MAXN,
    "顶格层：n=1000 全部取上界 2^32-1（全相等的最坏 tie 结构，答案必须为 1）")
gen(10, list(range(1, MAXN)) + [MAXV],
    "顶格层：n=1000 严格递增、末位=2^32-1（答案=n=1000，压「最右」与 1-based 越界）")

print("自检通过：%d 个测试点的 std 输出均与 Python 参照一致，且均在题面范围内。"
      % len(_pts))
