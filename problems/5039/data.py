#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2037《【例5.4】约瑟夫问题》数据生成器（目标 ROJ 题号 5039）
#
# 题意：N 个人围成一圈，从第 1 个人开始报数，报到 M 的人出圈；再由下一个人从 1
#       重新报数，报到 M 的人出圈；……按出圈次序输出这 N 个人的编号。
# 输入：一行两个整数 N M。输出：一行 N 个整数，依次出圈者的编号（空格分隔）。
# 数据范围（题面【提示】）：2 <= N, M <= 1000（单组输入，无多组数据）。
# 限制：time 1000 ms / memory 64 MB（config.json 与官方 OJ 页 65536 KB 一致）。
#
# 输入域极小（999*999 种组合），故分层策略是：**边界/极端结构显式指定**，
# 中间档随机填充，顶格层取上限并叠加最坏扫描结构；并在末尾用独立的 Python
# 参照实现（列表 pop 路线）逐点校验 .in/.out 自洽。
#
# 分层设计（10 个测试点，从最小铺到顶格）：
#   点 1-2   边界层：N、M 双最小 (2,2) / N 最小 × M 顶格 (2,1000)
#   点 3-4   小规模：题面【输入样例】(8,5) 可手算核对 / N,M ∈ [3,50] 随机
#   点 5-6   中等规模随机：N,M ∈ [100,500] / N,M ∈ [400,700]，范围中间档
#   点 7-8   大规模：N,M ∈ [700,1000] 随机 / (1000,2) 最大圈 × 最小步长结构
#   点 9-10  顶格层：(1000,1000) 双顶格 / (1000,999) 顶格邻域 —— N·M=999000
#            为标程逐格扫描的最坏量级（O(N*M) 顶格）
# 说明：本题输出长度固定为 N 个编号，不存在"答案为 0/1"之类的值域极端项；
#       "题面声明的特殊值"即样例 (8,5)，已放在点 3 覆盖。

from cyaron import *  # 引入CYaRon的库

import random

LO = 2      # 题面 N, M 下界
HI = 1000   # 题面 N, M 上界


def rnd2(i, nlo, nhi, mlo, mhi):
    """按点号取独立随机数对，与调用顺序无关、可精确复现。

    注意：同一个 Random 实例连续取两个数，避免两次
    `Random(seed).randint(...)` 返回相同值（序列被重置）。
    """
    rng = random.Random(2037 * 1000 + i)
    return rng.randint(nlo, nhi), rng.randint(mlo, mhi)


def gen(i, n, m, note):
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_write(n, m)
    io.output_gen("../std")
    print("problem%-2d: N=%-5d M=%-5d N*M=%-7d -- %s" % (i, n, m, n * m, note))


# ---- 点 1-2：边界层 ----
gen(1, LO, LO, "边界层：N、M 双取最小 (2,2) —— 全域最小规模；两人圈，步长恰为圈长")
gen(2, LO, HI, "边界层：N 最小 × M 顶格 (2,1000) —— 圈内仅 2 人但每轮绕 500 圈才出一人")

# ---- 点 3-4：小规模（可手算） ----
gen(3, 8, 5, "小规模：题面【输入样例】8 5（答案 5 2 8 7 1 4 6 3，可手算核对）")
gen(4, *rnd2(4, 3, 50, 3, 50), "小规模随机：N,M ∈ [3,50]，量级小到可手工/暴力复核")

# ---- 点 5-6：中等规模随机 ----
gen(5, *rnd2(5, 100, 500, 100, 500), "中等规模随机：N,M ∈ [100,500]，范围中间档")
gen(6, *rnd2(6, 400, 700, 400, 700), "中等规模随机：N,M ∈ [400,700]，中间档偏大")

# ---- 点 7-8：大规模 ----
gen(7, *rnd2(7, 700, HI, 700, HI), "大规模随机：N,M ∈ [700,1000]，接近上限")
gen(8, HI, LO, "大规模结构：N=1000 最大圈 × M=2 最小步长（出圈序列呈隔一取一形态）")

# ---- 点 9-10：顶格层 ----
gen(9, HI, HI, "顶格层：N=M=1000 双顶格，每轮几乎绕整圈，扫描量与输出长度同时顶格")
gen(10, HI, HI - 1, "顶格层：N=1000 顶格 × M=999 顶格邻域（N*M=999000 为标程 O(N*M) 最坏量级）")


# ---- 自检：独立 Python 参照（列表 pop 路线）逐点复核 in/out 自洽 ----
def josephus_ref(n, m):
    """纯 Python 独立参照：不等价于 std 的写法（用 list.pop 直接定位）。"""
    ring = list(range(1, n + 1))
    idx = 0
    order = []
    while ring:
        idx = (idx + m - 1) % len(ring)
        order.append(ring.pop(idx))
    return order


import os  # noqa: E402

_pts = [
    (1, LO, LO), (2, LO, HI), (3, 8, 5), (4, None, None), (5, None, None),
    (6, None, None), (7, None, None), (8, HI, LO), (9, HI, HI), (10, HI, HI - 1),
]
for i, n, m in _pts:
    inp = open("problem%d.in" % i).read().split()
    out = open("problem%d.out" % i).read().split()
    gn, gm = int(inp[0]), int(inp[1])
    assert len(inp) == 2, "problem%d: 输入必须恰为两个整数" % i
    assert LO <= gn <= HI and LO <= gm <= HI, \
        "problem%d: N=%d M=%d 超出题面范围 [%d,%d]" % (i, gn, gm, LO, HI)
    if n is not None:
        assert (gn, gm) == (n, m), "problem%d: 生成值与设计不符" % i
    expect = josephus_ref(gn, gm)
    assert out == [str(x) for x in expect], \
        "problem%d: 输出与独立 Python 参照不一致" % i
    assert len(out) == gn, "problem%d: 输出个数应为 N=%d" % (i, gn)
    assert sorted(int(x) for x in out) == list(range(1, gn + 1)), \
        "problem%d: 输出不是 1..N 的排列" % i
    assert max(len(s) for s in out) >= 1
    print("problem%-2d 自检通过：N=%-5d M=%-5d 输出为 1..N 的排列且与 Python 参照一致"
          % (i, gn, gm))

# 行末空白检查（输出只允许单个 '\n' 结尾，无行末空格）
for i in range(1, 11):
    raw = open("problem%d.out" % i, "rb").read()
    assert raw.endswith(b"\n") and not raw.endswith(b" \n"), \
        "problem%d: 行末存在多余空白" % i
print("自检通过：10 个测试点均满足 2 <= N,M <= 1000，输出为 1..N 的排列，"
      "与独立 Python 参照完全一致，且行末仅一个换行。")
