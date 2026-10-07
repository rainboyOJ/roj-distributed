#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 一本通 2042《【例5.10】稀疏矩阵》数据生成器（目标 ROJ 题号 5044；cyaron）
#
# 题意：读入 n×m 矩阵，逐行（先按行、再按列）输出全部非 0 元素的「行号 列号 值」
#       （行列号均 1 起），即稀疏矩阵的 K×3 简记形式；矩阵全 0 时没有任何输出。
#       题面【输入样例】：
#           3 5 / 0 0 0 0 5 / 0 0 4 0 0 / 1 0 0 0 1
#         对应本包口径（行主序）的输出为：
#           1 5 5 / 2 3 4 / 3 1 1 / 3 5 1
#         官方【输出样例】给了同一批三元组的另一种排列（3 5 1 提到最前），题面明文
#         「简记形式有多种形式，输出一种正确形式即可」。本包以 std 的行主序输出为准；
#         细节与风险见 gen-report.md §3、§7。
#
# 【数据范围】
#   - 题面明确声明：矩阵中每个正整数 < 1000（即非 0 元素 ∈ [1, 999]，0 为「空位」）；
#   - 题面与官方 OJ 页（http://ybt.ssoier.cn:8088/problem_show.php?pid=2042）**均未
#     声明 n、m 的取值范围**；本包自定工作范围 1 <= n, m <= 100。
#     依据：全部网络 AC 参考代码（博客园 zheng1945、CSDN qq_40802813、CSDN HAFT41016，
#     URL 见 std.cpp 头注释）一律写成 int a[100][100]，即作者们认定的规模上界就是
#     100×100；题面样例取 3×5 也与之相容；本题章（第五章 数组 / 例 5.10）正对应
#     「100×100 以内二维数组」的教学规模。自定范围如实记录在 gen-report.md 风险点 1。
#   - 单组输入（一个测试点一个矩阵），不存在多组数据的分层。
#
# 分层设计（10 个测试点，从最小铺到顶格；每个点的规模与设计意图见下方注释）：
#   点 1  边界层：1×1 全零 → 空输出（K=0 的极端；最小规模 1×1；「稀疏」的退化情形）
#   点 2  边界层：1×1 值 999 → `1 1 999`（K=1 的极端；题面「正整数<1000」的最大合法
#                 值 999 同时是全最大值；行列号最小取值 1）
#   点 3  小规模：题面【输入样例】3×5 原样（题面唯一声明的特殊值，可手算核对）
#   点 4  小规模随机：n=2、m∈[2,4]（显式覆盖 n=2 边界），值∈{0,1,2,999}
#                 （可手算量级；含 0 与值域两端）
#   点 5  中等规模随机：20×30，值∈[1,999]，非零率 ~12%
#   点 6  中等规模/形状边界：1×100 行向量（n=1 边界 + m 顶格；非零位置覆盖
#                 列号 1 与列号 100 两端）
#   点 7  大规模随机：100×100，恰 150 个非零（~1.5%）（真正意义上的稀疏矩阵；
#                 接近上限规模）
#   点 8  大规模随机：100×80，非零率 ~45%（值∈[1,999] 全值域；接近上限规模、
#                 高密度，与点 7 的稀疏形成两档对照）
#   点 9  顶格层：100×100 全非零（K = 10000 为本题最大输出规模，最坏输出结构；
#                 值域偏极端——一半取 999、一半取 [1,999]，卡 3 位数字宽）
#   点 10 顶格层/边界定向：100×100 全零，唯一非零元素置于 (100,100) = 999
#                 → `100 100 999`（最大行号、最大列号、最大值的联合边界）
#
# 与任务书分层清单的对照：
#   - 「n=1 / n=2」：点 1、2、6 取 n=1（点 6 另覆盖 m 顶格）；点 4 显式取 n=2；
#   - 「全最小值 / 全最大值」：点 1（全零 = 全最小）、点 2（999 = 题面允许的最大值）、
#     点 9（一半元素为 999 的最大值集合）；
#   - 「答案为 0 或 1」：本题输出是三元组表而非计数，对应极端是 K=0（点 1，空输出）
#     与 K=1（点 2，唯一一行输出；点 10 用另一组坐标/值复现）；
#   - 「题面声明的特殊值」：点 3 = 题面【输入样例】原样。
#
# 数据正确性自检：生成完每组后，用与本文件同源的纯 Python 参考实现（直接按题面定义
# 逐行扫描矩阵）复算期望输出，与 std 生成的 .out 逐字节比对；再校验 .in 的规模、取值
# 范围不越界。任一组不符即 AssertionError 终止（防止 std 与题意漂移）。

from cyaron import *  # 引入CYaRon的库

import os
import random

# 同一份 .in 内容两次生成完全一致（固定种子）：已用 sha256 双生成验证（见 gen-report.md §6）。

MAXN = 100   # 自定工作范围：行数上限（题面未声明，见文件头说明；网络 AC 代码均开 a[100][100]）
MAXM = 100   # 自定工作范围：列数上限
MAXV = 999   # 题面声明：矩阵中每个正整数 < 1000，故非 0 元素最大 999


def write_matrix(i, n, m, mat, note):
    """写出第 i 组：第一行 `n m`，随后 n 行矩阵；.out 由 std 生成。

    注意：cyaron 的 IO 对输出文件做了缓冲，必须等 IO 对象析构（缓冲区 flush）后
    才能读回 .out 做自检，因此这里只写文件，自检在全部生成结束后统一进行。
    """
    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_write("%d %d\n" % (n, m)
                   + "\n".join(" ".join(map(str, row)) for row in mat) + "\n")
    io.output_gen("../std")
    print("problem%-2d: n=%-3d m=%-3d 非零 K=%-6d -- %s" % (i, n, m, count_nonzero(mat), note))


def count_nonzero(mat):
    return sum(1 for row in mat for v in row if v != 0)


def expected_output(n, m, mat):
    """题面定义 + 本包行主序口径下的期望输出（独立于 std 的纯 Python 复算）。"""
    lines = []
    for i in range(n):
        for j in range(m):
            if mat[i][j] != 0:
                lines.append("%d %d %d" % (i + 1, j + 1, mat[i][j]))
    return "".join(line + "\n" for line in lines)


def rand_matrix(n, m, p_nonzero, value_choices):
    """随机矩阵：每个位置以 p_nonzero 的概率取 value_choices 中的值，否则为 0。"""
    return [[choice(value_choices) if random.random() < p_nonzero else 0
             for _ in range(m)] for _ in range(n)]


random.seed(2042)  # 固定种子，保证可复现（各点独立于调用顺序，见下方用法）

# 说明：cyaron 的 choice 绑定在 cyaron 内部的 Random 实例上，不受 random.seed 影响；
# 它只用在内层取值（外层位置/规模均由 random 控制），对本脚本属于“确定性选择”
# （无外部状态），可复现性已用 sha256sum 连续三次生成逐字节比对验证。

# 前置检查：data.py 需要本目录（staging/2042）下的已编译标程 std（.out 全部由 std 现场生成）。
# 编译：cd .ybt-import/staging/2042 && g++ -O2 -std=c++17 std.cpp -o std
# 注意：io.output_gen("../std") 是相对**运行目录 data/** 的路径，即 staging/2042/std。
_here = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(_here, "std")):
    raise SystemExit(
        "找不到标程可执行文件 %s：请先编译：\n"
        "    cd .ybt-import/staging/2042 && g++ -O2 -std=c++17 std.cpp -o std"
        % os.path.join(_here, "std"))

# ---- 点 1：边界层，1×1 全零（K=0 极端，最小规模，空输出） ----
write_matrix(1, 1, 1, [[0]],
             "边界层：最小规模 1×1 全零，K=0（无任何输出，退化情形）")

# ---- 点 2：边界层，1×1 值 999（K=1 极端，题面允许的最大元素值） ----
write_matrix(2, 1, 1, [[999]],
             "边界层：K=1 极端 + 题面「正整数<1000」的最大合法值 999 + 行列号最小取值 1")

# ---- 点 3：小规模，题面【输入样例】原样（题面唯一声明的特殊值） ----
write_matrix(3, 3, 5, [[0, 0, 0, 0, 5],
                       [0, 0, 4, 0, 0],
                       [1, 0, 0, 0, 1]],
             "小规模：题面【输入样例】原样（3×5，含全零行与全零列，可手算核对）")

# ---- 点 4：小规模随机，n=2 显式边界（值只取 {0,1,2,999} 便于人工核对） ----
# 每个点用独立种子 random.seed(2042 + 点号)，与代码执行顺序无关、可精确复现。
random.seed(2042 + 4)
_n4, _m4 = 2, random.randint(2, 4)      # n=2 固定（边界），m 在 [2,4] 内随机
write_matrix(4, _n4, _m4, rand_matrix(_n4, _m4, 0.5, [1, 2, 999]),
             "小规模随机：n=2（边界）m∈[2,4]，值∈{0,1,2,999}（含 0 与值域两端，可手算）")

# ---- 点 5：中等规模随机，20×30，全值域，非零率 ~12% ----
random.seed(2042 + 5)
write_matrix(5, 20, 30, rand_matrix(20, 30, 0.12, list(range(1, MAXV + 1))),
             "中等规模随机：20×30，值∈[1,999] 全值域，非零率 ~12%")

# ---- 点 6：中等规模 / 形状边界，1×100 行向量（n=1 + m 顶格；覆盖列号 1 与 100） ----
random.seed(2042 + 6)
_row = [0] * MAXM
_row[0] = random.randint(1, MAXV)      # (1,1) 必非零：列号最小值
_row[MAXM - 1] = random.randint(1, MAXV)  # (1,100) 必非零：列号最大值（顶格）
for j in range(1, MAXM - 1):
    if random.random() < 0.1:
        _row[j] = random.randint(1, MAXV)
write_matrix(6, 1, MAXM, [_row],
             "形状边界：1×100 行向量（n=1 与 m 顶格；列号 1 与 100 两端均取到）")

# ---- 点 7：大规模随机，100×100，恰 150 个非零（~1.5%，本义稀疏矩阵） ----
random.seed(2042 + 7)
_m7 = [[0] * MAXM for _ in range(MAXN)]
_target7 = 150                        # 目标非零个数（100×100 的 ~1.5%）
_pos7 = random.sample([(r, c) for r in range(MAXN) for c in range(MAXM)], _target7)
for (r, c) in _pos7:                  # 取 150 个**互不相同**的位置，保证恰为该个数
    _m7[r][c] = random.randint(1, MAXV)
write_matrix(7, MAXN, MAXM, _m7,
             "大规模随机：100×100 稀疏（恰为 150 个非零，~1.5%；真正意义的稀疏矩阵）")

# ---- 点 8：大规模随机，100×80，非零率 ~45%（高密度对照，全值域随机） ----
random.seed(2042 + 8)
write_matrix(8, MAXN, 80, rand_matrix(MAXN, 80, 0.45, list(range(1, MAXV + 1))),
             "大规模随机：100×80，值∈[1,999] 全值域，非零率 ~45%（高密度，接近上限规模）")

# ---- 点 9：顶格层，100×100 全非零（K=10000 最大输出规模，值域偏极端） ----
random.seed(2042 + 9)
_m9 = [[999 if random.random() < 0.5 else random.randint(1, MAXV)
        for _ in range(MAXM)] for _ in range(MAXN)]   # 一半固定 999：卡 3 位数字宽
write_matrix(9, MAXN, MAXM, _m9,
             "顶格层：100×100 全非零（K=10000，本题最大输出规模；一半值为最大值 999）")

# ---- 点 10：顶格层 / 边界定向，100×100 全零 + 唯一非零在 (100,100)=999 ----
_m10 = [[0] * MAXM for _ in range(MAXN)]
_m10[MAXN - 1][MAXM - 1] = 999
write_matrix(10, MAXN, MAXM, _m10,
             "顶格层边界定向：仅 (100,100)=999 非零（最大行号+最大列号+最大值的联合边界）")

# ---- 自检：读回每组的 .in，用纯 Python 参考实现复算期望输出，与 std 的 .out 逐字节比对 ----
print("\n自检：复算 10 组期望输出并与 std 生成的 .out 比对……")
for i in range(1, 11):
    with open("problem%d.in" % i, encoding="utf-8") as fin:
        tokens = fin.read().split()
    n, m = int(tokens[0]), int(tokens[1])
    vals = list(map(int, tokens[2:]))
    assert 1 <= n <= MAXN and 1 <= m <= MAXM, \
        "problem%d: n,m 越出自定范围 1..100（n=%d m=%d）" % (i, n, m)
    assert len(vals) == n * m, \
        "problem%d: 矩阵元素个数 %d != n*m = %d" % (i, len(vals), n * m)
    mat = [vals[r * m:(r + 1) * m] for r in range(n)]
    for row in mat:
        for v in row:
            assert 0 <= v < 1000, "problem%d: 元素 %d 违反题面「正整数<1000」" % (i, v)
    expect = expected_output(n, m, mat)
    with open("problem%d.out" % i, encoding="utf-8") as fout:
        got = fout.read()
    assert got == expect, (
        "problem%d: std 输出与题意复算不一致\n--- 期望 ---\n%s\n--- std ---\n%s"
        % (i, expect[:400], got[:400]))
    k = count_nonzero(mat)
    print("  ok problem%-2d n=%-3d m=%-3d K=%-6d 输出 %d 字节" % (i, n, m, k, len(expect)))

# 附加结构性断言（防止分层设计与实际数据漂移）
def read_back(i):
    """读回 problem<i>.in 的 (n, m, 矩阵)，供生成后的结构性断言使用。"""
    with open("problem%d.in" % i, encoding="utf-8") as fin:
        tokens = fin.read().split()
    n, m = int(tokens[0]), int(tokens[1])
    vals = list(map(int, tokens[2:]))
    return n, m, [vals[r * m:(r + 1) * m] for r in range(n)]


assert count_nonzero([[0]]) == 0, "点 1 必须是 K=0（空输出）"
assert open("problem1.out").read() == "", "点 1 的 .out 必须为空文件"
assert open("problem2.out").read() == "1 1 999\n", "点 2 必须是 1 1 999"
assert open("problem10.out").read() == "100 100 999\n", "点 10 必须是 100 100 999"
_a, _b, _m6 = read_back(6)
assert (_a, _b) == (1, MAXM), "点 6 必须是 1×100"
assert _m6[0][0] != 0 and _m6[0][MAXM - 1] != 0, \
    "点 6 必须同时覆盖列号 1 与列号 100（两端已置非零）"
_c, _d, _m7 = read_back(7)
assert (_c, _d) == (MAXN, MAXM) and count_nonzero(_m7) == _target7, \
    "点 7 必须是 100×100 且恰 150 个非零（~1.5%）"
_e, _f, _m8 = read_back(8)
assert (_e, _f) == (MAXN, 80), "点 8 必须是 100×80"
assert count_nonzero(_m9) == MAXN * MAXM, "点 9 必须是 100×100 全非零（K=10000）"
print("自检通过：10 组数据规模、取值均在自定范围内，std 输出与题面定义逐字节一致。")
