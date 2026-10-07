#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2036《【例5.3】开关门》分层数据生成器（cyaron）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2030/data.py
#
# 题意：n(2<=n<=1000) 个房间编号 1..n。第 1 个服务员把所有的门都打开；第 j(2..n) 个
#   服务员把所有编号为 j 的倍数的房间"相反处理"。问第 n 个服务员来过后哪几扇门是
#   打开的：一行，由小到大的房间序号，各序号之间用一个空格隔开。
#   样例：输入 "100" -> 输出 "1 4 9 16 25 36 49 64 81 100"。
# 数据范围（题面明文，官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2036 一致）：
#   2 <= n <= 1000 —— 本题**只有一个输入量 n**，且下界为 2（不是 1）。
# 限制：time 1000 ms / memory 65536 KB（config.json 的 64 MB 与官方页一致）。
#
# ---- 数学结论（std.cpp 依据，全部来源一致）----
#   门 i 恰被"编号为 i 的因数"的服务员各操作一次，操作次数 = d(i)（约数个数）。
#   门初态为关 => 最终开着 <=> d(i) 为奇数 <=> i 是完全平方数。
#   输出即 1,4,9,...,<=n，共 floor(sqrt(n)) 项。n<=1000 时最大 31^2=961（32^2=1024>1000），
#   最多 31 项输出。**可考量的"规模"只有 n 与答案项数两维**，两者单调同向。
#
# ---- 分层策略（10 组）----
#   题面下界 n=2、上界 n=1000，输入域 [2,1000] 仅 999 个取值，域很小。
#   本包策略：边界层穷举题面声明的边界/临界值，其余各层在对应区间内随机，
#   **10 个测试点输入互不相同**，规模从 (2) 最小一路铺到顶格 (1000)：
#
#     点 1 ｜边界层｜n=2（全最小值，题面下界）
#       唯一输出 "1"（仅 1 项，最小非空答案）；覆盖"n 取最小合法值"。
#     点 2 ｜边界层｜n=3（下界紧邻值）
#       输出仍为 "1"，但状态演化与点 1 不同（n=2 只翻门 2、n=3 还翻门 3）：
#       抓「服务员循环起点写错（如从 3 起，门 2 会留在开 → 输出 1 2）」之类的 off-by-one。
#     点 3 ｜小规模随机｜n ∈ [5,99]（种子 2036 得 12）
#       可手算量级（答案 3 项：1 4 9）；覆盖小 n 的非平方数一般情形。
#     点 4 ｜小规模（题面声明的特殊值）｜n=100
#       题面【输入样例】原样，输出必须逐字节等于【输出样例】
#       "1 4 9 16 25 36 49 64 81 100\n"（10 项）；同时 100=10^2 是**小规模处的
#       平方数临界点**，专抓循环条件 i*i<n 写成严格小于（会漏掉末项 100）。
#     点 5 ｜中等规模随机｜n ∈ [100,499]（种子 2036 得 406）
#       范围中间档（答案 20 项：1^2..20^2，末项 400）。
#     点 6 ｜中等规模（临界结构）｜n=484=22^2
#       中段**恰好是完全平方数**：末项必须恰为 484 且被取到（< 与 <= 的分界）；
#       与点 5 的非平方 n 成对，检验 floor(sqrt(n)) 取整方向在中段也正确。
#     点 7 ｜大规模随机｜n ∈ [500,800]（种子 2036 得 792）
#       接近上限的大规模随机（答案 28 项，末项 784）。
#     点 8 ｜大规模随机（逼近上限）｜n ∈ [801,999]（种子 2036 得 951）
#       逼近上限的随机点（答案 28~31 项）；与点 9/10 的顶格值不重复。
#     点 9 ｜顶格层（按题型构造最坏/临界结构）｜n=961=31^2
#       [2,1000] 内**最大的完全平方数**：n 本身即末项，最后一对 (i,i^2) 恰卡在
#       i*i<=n 的等号上；把 <= 写成 < 就会少输出 961，是最有价值的临界点。
#     点 10｜顶格层（题面上限 + 最大输出量）｜n=1000
#       题面上限顶格：输入字节最多（"1000"）、正确答案项数最多（31 项）、
#       总工作量最大；覆盖 961<n<1024 区间，保证第 31 项必须出现。
#
#   结论：10 点 = 边界 2（2/3）+ 小规模 2（12/100）+ 中等 2（406/484）
#   + 大规模 2（792/951）+ 顶格 2（961/1000）；题面声明的边界值（下界、上界、
#   样例值）与平方数临界结构（10^2、22^2、31^2、31^2-1 邻域）全部覆盖，
#   点 5-10 的输出项数单调放大（20→31），**不存在"10 个点全是小随机"**。
#
# ---- 输入输出格式口径 ----
#   输入：单行整数 + 行末换行（"n\n"），与仓库语料惯例一致；
#   输出：元素间恰一个空格、行末无多余空格、以单个 '\n' 结束（"1 4 9 ... \n"）。
#   本题**全程整数运算、无浮点**，不存在 %g/尾零等跨平台文本差异。

from cyaron import *  # 引入CYaRon的库

import os
import random

NMIN, NMAX = 2, 1000  # 题面明文范围：[2,1000]，下界为 2

# 固定种子 ⇒ 随机点完全可复现（随机量在 Python 侧一次算定后写入 .in，不依赖 cyaron 随机流）
RNG = random.Random(2036)

# 本包所有测试点：(data_id, n, 分层标注)
CASES = []


# ---- Python 独立真值 1：按题面流程逐步模拟（与 std 的"平方数枚举"是两条独立路径）----
def truth_simulate(n):
    """题面字面模拟：第 1 个服务员全开，第 j=2..n 个服务员对 j 的倍数做相反处理。"""
    open_state = [False] * (n + 1)               # False=关，True=开
    for k in range(1, n + 1):
        open_state[k] = True                     # 第 1 个服务员：全部打开
    for j in range(2, n + 1):                    # 第 j 个服务员
        for k in range(j, n + 1, j):             # 编号为 j 的倍数的房间
            open_state[k] = not open_state[k]    # 相反处理
    return [k for k in range(1, n + 1) if open_state[k]]


# ---- Python 独立真值 2：闭式（n 以内完全平方数，整数开方，不用浮点）----
def isqrt(n):
    r = 0
    while (r + 1) * (r + 1) <= n:
        r += 1
    return r


def truth_squares(n):
    return [i * i for i in range(1, isqrt(n) + 1)]


def expect_out(n):
    """期望输出文本：元素间恰一个空格、行末无多余空格、单个换行。"""
    return " ".join(str(x) for x in truth_squares(n)) + "\n"


def _add(data_id, n, note):
    assert NMIN <= n <= NMAX, "非法数据点 n=%d 超出 [%d,%d]" % (n, NMIN, NMAX)
    CASES.append((data_id, n, note))


# ---- 点 1-2：边界层（题面下界与紧邻值）----
_add(1, 2, "边界层｜全最小值 n=2（题面下界）：唯一答案 \"1\"（1 项）")
_add(2, 3, "边界层｜下界紧邻 n=3：答案仍 \"1\"，但状态演化不同（n=2 只翻门 2、n=3 还翻门 3），"
          "模拟派若把服务员循环起点写错（如从 3 起）门 2 会留在「开」")

# ---- 点 3-4：小规模 ----
_n3 = RNG.randint(5, 99)                       # 种子 2036 -> 12（非平方数）
_add(3, _n3, "小规模随机｜n∈[5,99]（种子 2036 复现）：答案 3 项，小 n 非平方数一般情形")
_add(4, 100, "小规模(题面特殊值)｜【输入样例】原样：输出须逐字节为 "
             "\"1 4 9 16 25 36 49 64 81 100\\n\"（10 项）；100=10^2 小规模平方临界")

# ---- 点 5-6：中等规模 ----
_n5 = RNG.randint(100, 499)                    # 种子 2036 -> 406（非平方数）
_add(5, _n5, "中等规模随机｜n∈[100,499]（种子 2036 复现）：答案 20 项，末项 400")
_add(6, 484, "中等规模(临界结构)｜n=484=22^2：中段恰为完全平方数，末项须恰取到 484")

# ---- 点 7-8：大规模 ----
_n7 = RNG.randint(500, 800)                    # 种子 2036 -> 792（非平方数）
while _n7 in (961, 999, 1000):
    _n7 = RNG.randint(500, 800)                # 防御：避开顶格确定性值
_add(7, _n7, "大规模随机｜n∈[500,800]（种子 2036 复现）：答案 28 项，末项 784")
_n8 = RNG.randint(801, 999)
while _n8 in (961, 999):                       # 避开点 9/10 的确定性值，保证 10 点互不重复
    _n8 = RNG.randint(801, 999)
_add(8, _n8, "大规模随机(逼近上限)｜n∈[801,999]（种子 2036 复现）：答案 %.0f 项，末项 %d"
     % (len(truth_squares(_n8)), truth_squares(_n8)[-1]))

# ---- 点 9-10：顶格层 ----
_add(9, 961, "顶格层(临界结构)｜n=961=31^2：[2,1000] 内最大完全平方数，"
             "末项恰为 n，卡 i*i<=n 的等号（写成 < 会漏掉 961）")
_add(10, 1000, "顶格层(题面上限+最大输出量)｜n=1000：题面上限顶格，"
               "正确答案项数最多（31 项，末项 961），覆盖 961<n<1024 区间")

assert len(CASES) == 10, "必须恰好 10 个测试点"
assert len({n for _, n, _ in CASES}) == 10, "10 个测试点输入必须互不相同"


def gen_case(data_id, n, note):
    io = IO(file_prefix="problem", data_id=data_id)   # problem{data_id}.in / .out
    io.input_writeln(n)                               # "n\n"
    io.output_gen("../std")                           # .out 由 std 生成
    print("problem%-2d: n=%-4d 答案项数=%-2d 期望输出=%s -- %s"
          % (data_id, n, len(truth_squares(n)), repr(expect_out(n)), note))


def self_check():
    """生成后立即审计：成对齐全、输入格式合规、std 输出与两条独立真值逐字节一致。"""
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
        want_in = "%d\n" % n
        want_out = expect_out(n)
        if raw_in != want_in:
            print("BAD INPUT problem%d.in: %r (expect %r)" % (data_id, raw_in, want_in))
            bad += 1
        if raw_out != want_out:
            print("OUTPUT != TRUTH problem%d: %r (expect %r)" % (data_id, raw_out, want_out))
            bad += 1
        # 三路交叉：文件内容 == 闭式真值 == 题面逐步模拟真值
        sim = " ".join(str(x) for x in truth_simulate(n)) + "\n"
        if sim != want_out:
            print("SIMULATE != SQUARES at n=%d: %r vs %r" % (n, sim, want_out))
            bad += 1
    # 题面样例逐字节核对（点 4）
    sample_out = open("problem4.out", encoding="utf-8").read()
    if sample_out != "1 4 9 16 25 36 49 64 81 100\n":
        print("SAMPLE MISMATCH: problem4.out=%r" % sample_out)
        bad += 1
    if bad:
        print("SELF-CHECK FAILED: %d issue(s)" % bad)
        raise SystemExit(1)
    print("SELF-CHECK OK: 10/10 pairs, inputs well-formed, outputs == 闭式真值 == 逐步模拟真值"
          "（含题面样例 100 -> 1 4 ... 100 逐字节比对）")
    print("分层覆盖：边界 2 点 + 小规模 2 点 + 中等 2 点 + 大规模 2 点 + 顶格 2 点")


if __name__ == "__main__":
    assert os.path.exists("../std"), "../std 未编译，先执行 g++ -O2 -std=c++17 ../std.cpp -o ../std"
    for _data_id, _n, _note in CASES:
        gen_case(_data_id, _n, _note)
    self_check()
