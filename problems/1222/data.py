#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1222《放苹果》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/2030/data.py
#
# 题意：t 组询问，每组给 M N，输出 K = 把 M 个相同苹果放进 N 个相同盘子（允许空盘）的放法数。
#       5,1,1 与 1,5,1 计同一种（盘子相同 => 只按非降多重集计数）。
# 数据范围（题面明文，与官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1222 一致）：
#   0 <= t <= 20；1 <= M, N <= 10。限制 time 1000 ms / memory 64 MB（config.json）。
#
# ---- 分层策略（多组数据题：t 的组数 + (M,N) 规模 一起分层，每点组数均 <= 20）----
#   点 1  边界层：t=0 —— 题面下界（0<=t<=20 的最小值），合法输入但**输出为空**；
#         对应「答案为 0 或 1 的极端」中的退化分支（0 行输出）。
#   点 2  边界层：t=1，(M,N)=(1,1) —— 全最小值 + 最小非空组数 + 答案 K=1 的下界极端。
#   点 3  边界层：t=20（组数上限）—— 题面样例 (7,3) + N=1 整列(10 组，答案恒 1，
#         含 (10,1) 单维顶格) + N=2 列(m=1..8) + 全最大值 (10,10)。
#   点 4  小规模随机：t=10，M,N∈[1,3]（答案∈{1,2,3}，逐组可手算核对）。
#   点 5  小规模随机：t=20；补覆盖小规模组合 + [1,5]² 随机。
#   点 6  中等规模随机：t=20；补覆盖中规模组合 + [3,8]² 随机。
#   点 7  大规模随机：t=20；补覆盖大规模组合 + [6,10]² 随机。
#   点 8  大规模随机：t=20；补覆盖近上限组合 + [8,10]² 随机（贴近上限）。
#   点 9  顶格层（单维顶格结构）：t=20 —— N=10 整列(10 组) + M=10 整行(9 组) + (9,9)，
#         单维读满上限 10 的全部结构，答案从 1 跨到 42。
#   点 10 顶格层（全最大 + 全相等）：t=20，(M,N)=(10,10)×20 —— 最大答案 42 重复最坏。
#
#   点 5-8 的「补覆盖」设计：为使 10 个测试点合起来**穷尽题面范围内全部 100 个 (M,N) 组合**
#   （任一组都至少被某点考到），每个随机点优先容纳尚未覆盖的组合（按 m+n 递增顺序，
#   故四档随点号单调变大：点5 m+n∈[4,11] → 点8 m+n∈[13,20]），剩余名额用同档随机补足。
#   生成用固定随机种子，结果完全可复现。
#
#   关于题面范围外的 M=0 / N=0：题面明文 1<=M,N<=10，正式数据严格不越界（m=0 属越界探针，
#   只在 work/stress.py 的 C 段与 std 做交叉验证），见 gen-report.md「风险点」。

from cyaron import IO  # 引入CYaRon的库

import random

MAXM = MAXN = 10  # 题面上限

ALL_PAIRS = [(m, n) for m in range(1, MAXM + 1) for n in range(1, MAXN + 1)]

# ---------------- 固定层 ----------------
# 点 1：边界层 —— t=0（题面下界，空输出）
P1 = []

# 点 2：边界层 —— 全最小值 (1,1)，答案 K=1
P2 = [(1, 1)]

# 点 3：边界层 —— 样例 + N=1 整列 + N=2 列(m=1..8) + 全最大值
P3 = [(7, 3)] + [(m, 1) for m in range(1, MAXM + 1)] + \
     [(m, 2) for m in range(1, 9)] + [(10, 10)]
assert len(P3) == 20 and len(set(P3)) == 20

# 点 4：小规模随机 —— [1,3]²，可手算
_r4 = random.Random(122204)
P4 = [(_r4.randint(1, 3), _r4.randint(1, 3)) for _ in range(10)]

# 点 9：顶格层 —— N=10 整列 + M=10 整行 + (9,9)
P9 = [(10, n) for n in range(1, MAXN + 1)] + \
     [(m, 10) for m in range(1, MAXM)] + [(9, 9)]
assert len(P9) == 20 and len(set(P9)) == 20

# 点 10：顶格层 —— 全最大且全相等（最坏重复）
P10 = [(10, 10)] * 20

fixed = set(P1) | set(P2) | set(P3) | set(P4) | set(P9) | set(P10)
leftover = sorted((p for p in ALL_PAIRS if p not in fixed), key=lambda p: (p[0] + p[1], p[0], p[1]))

# 点 5-8：把剩余组合按 m+n 递增均分 4 段（规模天然递增），段内不足 20 用同档随机补足
BANDS = [(1, 5), (3, 8), (6, 10), (8, 10)]  # 与各段规模对应的随机带
base, rem = divmod(len(leftover), 4)
rand_points = []
_idx = 0
for i in range(4):
    size = base + (1 if i < rem else 0)
    chunk = leftover[_idx:_idx + size]
    _idx += size
    lo, hi = BANDS[i]
    rng = random.Random(122205 + i)
    pool = [(m, n) for m in range(lo, hi + 1) for n in range(lo, hi + 1)
            if (m, n) not in set(chunk)]
    pad = rng.sample(pool, 20 - len(chunk))
    rand_points.append(sorted(chunk + pad, key=lambda p: (p[1], p[0])))

P5, P6, P7, P8 = rand_points

# ---------------- 生成 + 自检 ----------------
CASES = [
    (1, P1, "边界层：t=0（题面下界），合法但输出为空（0 行）"),
    (2, P2, "边界层：t=1，全最小值 (1,1)，答案 K=1 的下界极端"),
    (3, P3, "边界层：t=20；题面样例 (7,3) + N=1 整列（答案恒 1 极端，含 (10,1) 单维顶格）+ "
            "N=2 列 + 全最大值 (10,10)"),
    (4, P4, "小规模随机：t=10，M,N∈[1,3]，答案∈{1,2,3} 可手算"),
    (5, P5, "小规模随机：t=20；补覆盖小规模组合 + [1,5]² 随机"),
    (6, P6, "中等规模随机：t=20；补覆盖中规模组合 + [3,8]² 随机"),
    (7, P7, "大规模随机：t=20；补覆盖大规模组合 + [6,10]² 随机"),
    (8, P8, "大规模随机：t=20；补覆盖近上限组合 + [8,10]² 随机"),
    (9, P9, "顶格层：t=20；N=10 整列 + M=10 整行 + (9,9)，单维读满上限 10 的全部结构"),
    (10, P10, "顶格层：t=20 全最大值全相等，(M,N)=(10,10)×20，答案 42 重复最坏"),
]

# 自检 1：每点组数 <= 20，且每组都在题面范围内
for idx, rows, _note in CASES:
    assert 0 <= len(rows) <= 20, "点 %d 组数 %d 超出题面 t<=20" % (idx, len(rows))
    for m, n in rows:
        assert 1 <= m <= MAXM and 1 <= n <= MAXN, "点 %d 含越界组 (%d,%d)" % (idx, m, n)
assert len(CASES) == 10, "必须恰好 10 个测试点"

# 自检 2：10 个点合起来穷尽题面全部 100 个 (M,N) 组合
covered = set()
for _idx, rows, _note in CASES:
    covered |= set(rows)
assert covered == set(ALL_PAIRS), "未覆盖组合: %s" % sorted(set(ALL_PAIRS) - covered)

# 自检 3：打印各点规模概览（供人复核分层是否从最小铺到顶格）
print("各点 m+n 均值:", " ".join(
    ("%.1f" % (sum(m + n for m, n in rows) / len(rows))) if rows else "n/a"
    for _, rows, _ in CASES))

for idx, rows, note in CASES:
    io = IO(file_prefix="problem", data_id=idx)  # problem{idx}.in / problem{idx}.out
    io.input_writeln(len(rows))                  # 第一行：测试数据数目 t
    for m, n in rows:
        io.input_writeln(m, n)                   # 每组一行：M 与 N，空格分开
    io.output_gen("../std")                      # .out 由 std 生成
    print("problem%-2d: t=%-2d %s-- %s"
          % (idx, len(rows),
             ("m+n∈[%d,%d] " % (min(m + n for m, n in rows), max(m + n for m, n in rows))) if rows else "",
             note))
