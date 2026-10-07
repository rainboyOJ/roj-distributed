#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2039《【例5.6】冒泡排序》数据生成器（目标 ROJ 题号 5041）
#
# 题意：读入 n(1<=n<=20) 个小于 1000 的非负整数，按从大到小输出，每个数占一行。
# 输入：第一行 n；第二行 n 个非负整数。
# 输出：降序的 n 个非负整数，每个数占一行。
# 数据范围（题面原文）：1 <= n <= 20；0 <= a[i] < 1000（非负整数、小于 1000）。
# 限制：time 1000 ms / memory 64 MB（config.json 与官方页 65536 KB 一致）。
#
# 输入域极小（n<=20、值<1000），故分层策略是：**边界/结构极端显式指定**，
# 中间档随机填充，顶格层取 n=20 上限并叠加结构性最坏（逆序 / 全最小值 / 全最大值）；
# 末尾用独立的 Python 参照（sorted 降序）逐点复核 .in/.out 自洽。
#
# 分层设计（10 个测试点，从最小铺到顶格）：
#   点 1     边界层：n=1，唯一元素取值域最小 0（全域最小规模；输出恰 1 行）
#   点 2     边界层：n=2 且逆序 [999,0]——最小非平凡规模 + 值域两极同时出现，
#            必须做一次真实交换才能得到降序
#   点 3     题面特殊值：题面【输入样例】5 / 2 5 8 6 12（唯一题面声明值，可手算核对）
#   点 4     小规模随机：n∈[1,5]、值∈[0,10]，量级小到可完全手算
#   点 5     中等规模随机：n∈[8,12]、值∈[0,6]，n 中间档且值域窄到鸽巢必重复
#            （值种类仅 7 种 × n>=8，保证至少一对重复值）
#   点 6     中等规模随机：n∈[13,17]、值∈[0,999]，范围中间档偏大、全值域
#   点 7     大规模随机：n=20（顶格）× 值∈[0,999] 全值域随机
#   点 8     顶格结构：n=20 严格递增 0,1,...,19 —— 对"降序冒泡"是完全逆序，
#            交换次数与比较次数同时顶格（sum_{i=1..19} i = 190 次交换），
#            题面名为《冒泡排序》，逆序输入即该算法的最坏结构
#   点 9     顶格层：n=20 全部为最小值 0 —— 全最小值 + 全相等（输出恒 0 的极端，
#            即本题"答案为 0"的题内类比）
#   点 10    顶格层：n=20 全部为最大值 999 —— 全最大值 + 全相等，值域上端顶格
# 说明：排序题输出即输入的重排，不存在"答案恒为 0/1"的答案值域极端项，
#       该通用分层项由点 9（输出全 0）与点 1（唯一值 0）近似覆盖；
#       模板"点 7-8 大规模随机"的随机部分由点 6（n∈[13,17]）与点 7（n=20）承担，
#       点 8 让位给逆序最坏结构——因 n 上限仅 20，"大规模"与"顶格"在本题为同一档。

from cyaron import *  # 引入CYaRon的库

import random

NLO, NHI = 1, 20       # 题面 n 的下界与上界
VLO, VHI = 0, 999      # 题面元素值域：0 <= a[i] < 1000


def rnd(i, nlo, nhi, vlo, vhi):
    """按点号取独立随机序列，与调用顺序无关、可精确复现。"""
    rng = random.Random(2039 * 1000 + i)
    n = rng.randint(nlo, nhi)
    return [rng.randint(vlo, vhi) for _ in range(n)]


def gen(i, arr, note):
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(len(arr))                 # 第一行：n
    io.input_writeln(arr)                      # 第二行：n 个整数（空格分隔）
    io.output_gen("../std")
    print("problem%-2d: n=%-2d 值域[%d,%d] -- %s"
          % (i, len(arr), min(arr), max(arr), note))


# ---- 点 1-2：边界层 ----
gen(1, [0], "边界层：n=1 × 值域最小 0（全域最小规模，输出恰 1 行）")
gen(2, [999, 0], "边界层：n=2 且逆序 [999,0]——最小非平凡规模 + 值域两极，必须真实交换")

# ---- 点 3：题面样例（可手算） ----
gen(3, [2, 5, 8, 6, 12], "题面【输入样例】：5 / 2 5 8 6 12 -> 12 8 6 5 2，可手算核对")

# ---- 点 4：小规模随机（可手算） ----
gen(4, rnd(4, 1, 5, 0, 10), "小规模随机：n∈[1,5]、值∈[0,10]，量级小到可手算")

# ---- 点 5-6：中等规模随机 ----
gen(5, rnd(5, 8, 12, 0, 6), "中等规模随机：n∈[8,12]、值∈[0,6]——鸽巢保证重复值（7 种值/至少 8 个数）")
gen(6, rnd(6, 13, 17, 0, VHI), "中等规模随机：n∈[13,17]、值∈[0,999] 全值域，中间档偏大")

# ---- 点 7-8：大规模 / 逆序最坏 ----
gen(7, rnd(7, NHI, NHI, VLO, VHI), "大规模随机：n=20 顶格 × 值∈[0,999] 全值域随机")
gen(8, list(range(0, 20)), "顶格结构：n=20 严格递增 0..19——对降序冒泡完全逆序，交换 190 次为最坏")

# ---- 点 9-10：顶格层（结构性极端） ----
gen(9, [0] * 20, "顶格层：n=20 全部最小值 0——全最小值 + 全相等，输出恒 0 的极端")
gen(10, [999] * 20, "顶格层：n=20 全部最大值 999——全最大值 + 全相等，值域上端顶格")


# ---- 自检：独立 Python 参照（sorted 降序）逐点复核 in/out 自洽 ----
_expected_pts = {
    1: [0], 2: [999, 0], 3: [2, 5, 8, 6, 12],
    8: list(range(0, 20)), 9: [0] * 20, 10: [999] * 20,
}
for i in range(1, 11):
    inp = open("problem%d.in" % i).read().split()
    out = open("problem%d.out" % i).read().split()
    n = int(inp[0])
    arr = [int(x) for x in inp[1:]]
    assert len(inp) == n + 1, "problem%d: 输入应为 n 与 n 个数（实际 %d 个 token）" % (i, len(inp))
    assert NLO <= n <= NHI, "problem%d: n=%d 超出题面范围 [%d,%d]" % (i, n, NLO, NHI)
    assert all(VLO <= v <= VHI for v in arr), "problem%d: 元素值超出 [0,999]" % i
    if i == 5:
        assert len(set(arr)) < len(arr), "problem%d: 设计意图要求存在重复值" % i
    expect = sorted(arr, reverse=True)
    assert out == [str(x) for x in expect], \
        "problem%d: 输出与独立 Python 参照（sorted 降序）不一致" % i
    assert len(out) == n, "problem%d: 输出行数应为 n=%d" % (i, n)
    if i in _expected_pts:
        assert arr == _expected_pts[i], "problem%d: 生成值与设计不符" % i
    print("problem%-2d 自检通过：n=%-2d 输出为输入的多重集降序重排" % (i, n))

# 输出格式检查：每行一个数、末行仅一个换行、无行末空格
for i in range(1, 11):
    raw = open("problem%d.out" % i, "rb").read()
    assert raw.endswith(b"\n") and not raw.endswith(b" \n"), \
        "problem%d: 行末存在多余空白" % i
    for line in raw.decode().split("\n"):
        if line == "":
            continue
        assert line == line.strip() and line.isdigit(), \
            "problem%d: 存在非纯数字行（%r）" % (i, line)
print("自检通过：10 个测试点均满足 1<=n<=20、0<=a[i]<1000，输出为各输入的降序重排，"
      "每行一个数、末行仅一个换行。")
