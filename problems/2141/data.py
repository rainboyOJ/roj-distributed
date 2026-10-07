#!/usr/bin/env python

# 一本通 2141 公司下属 数据生成器
#
# 输入：第一行 n（员工数）；第二行 n-1 个整数，依次是员工 2..n 的直接上司编号。
# 输出：n 个整数，第 i 个为员工 i 的下属总人数（子树大小 - 1）。
# 限制：1 <= n <= 2*10^5（config: time 1000ms / memory 512MB）。
#
# 合法输入约定（与题面一致）：boss[i] ∈ [1,n]、boss[i] != i，
# 且全体员工在同一棵以 1（总经理）为根的树中。题面并未要求 boss[i] < i，
# 因此第 10 组特意用「标签置换后的链」构造 boss[子] > 子编号 的数据。
#
# 分层设计见每组上方的注释。

import random

from cyaron import *  # 引入CYaRon的库

random.seed(2141)

NMAX = 200000  # 题面上限


def rand_tree(n, window=None):
    """生成 boss[2..n]：
    - window 为 None：父节点在 [1, i-1] 均匀随机（随机树）；
    - window 为整数 w：父节点在 [max(1, i-w), i-1] 随机（有深度下界的随机树）。
    """
    bosses = []
    for i in range(2, n + 1):
        lo = 1 if window is None else max(1, i - window)
        bosses.append(random.randint(lo, i - 1))
    return bosses


def emit(data_id, n, bosses, note):
    """写出第 data_id 组：n 与 n-1 个上司编号。"""
    assert 1 <= n <= NMAX, note
    assert len(bosses) == n - 1, note
    # 严格校验：boss 在 [1,n]，且不等于自己（下标 +2 对应员工编号）
    for idx, b in enumerate(bosses):
        assert 1 <= b <= n, note
        assert b != idx + 2, note
    io = IO(file_prefix="problem", data_id=data_id)
    if bosses:
        io.input_write("%d\n%s\n" % (n, " ".join(map(str, bosses))))
    else:
        io.input_write("%d\n" % n)  # n=1：无上司数据
    io.output_gen("../std")


# ---- 点 1-2：边界层 ----------------------------------------------------------
# 1: n=1（题面下限，无上司数据），答案为 0 的极端情形
emit(1, 1, [], "n=1 边界")
# 2: n=2（最小非平凡树），答案是 [1, 0]，覆盖答案 = 1 的极端
emit(2, 2, [1], "n=2 边界")

# ---- 点 3-4：小规模层（可手算/解析验证）--------------------------------------
# 3: n=12 随机树（报告里给出完整树结构并手工核算）
emit(3, 12, rand_tree(12), "n=12 小随机")
# 4: n=64 纯链 boss[i]=i-1：答案恒为 n-i（可解析核对），同时覆盖小规模深链
emit(4, 64, [i - 1 for i in range(2, 65)], "n=64 链")

# ---- 点 5-6：中等规模层 ------------------------------------------------------
# 5: n=2000 随机树（随机形状、随机深度）
emit(5, 2000, rand_tree(2000), "n=2000 随机")
# 6: n=2000 完全二叉树 boss[i]=i//2：规则结构 + 子树大小可解析验证
emit(6, 2000, [i // 2 for i in range(2, 2001)], "n=2000 完全二叉树")

# ---- 点 7-8：大规模层（接近上限）---------------------------------------------
# 7: n=100000，前半均匀随机 + 后半窗口随机（父 ∈ [i-50,i-1]），
#    既有多兄弟的"宽"结构，又保证深度达到千级，检验不使用系统栈的实现
bosses7 = []
for i in range(2, 100001):
    if i <= 50000:
        bosses7.append(random.randint(1, i - 1))
    else:
        bosses7.append(random.randint(max(1, i - 50), i - 1))
emit(7, 100000, bosses7, "n=1e5 随机+深链")
# 8: n=100000 星形（所有 boss=1）：重复值极端结构，答案 n-1 与 n-1 个 0
emit(8, 100000, [1] * 99999, "n=1e5 星形")

# ---- 点 9-10：顶格层（取题面上限 n=2*10^5）-----------------------------------
# 9: n=200000 均匀随机树（最大规模随机）
emit(9, NMAX, rand_tree(NMAX), "n=2e5 随机")
# 10: n=200000 标签置换后的链：形状是同一条长链（深度最坏、输出最长），
#     但节点标签 2..n 随机置换，因此 boss 值经常大于下属编号，
#     可卡掉「假定 boss[i] < i、按编号倒序累加」的取巧写法
chain = [1] + random.sample(range(2, NMAX + 1), NMAX - 1)
boss_of = [0] * (NMAX + 1)
for k in range(1, NMAX):
    boss_of[chain[k]] = chain[k - 1]
bosses10 = [boss_of[i] for i in range(2, NMAX + 1)]
emit(10, NMAX, bosses10, "n=2e5 置换标签链")
