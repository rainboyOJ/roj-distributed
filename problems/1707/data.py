#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 1707《敲键盘》分层数据生成器（cyaron）
# ---------------------------------------------------------------------------
# 题意：T 组数据，每组给 n 个仅含小写字母的模式串 S_1..S_n；A 君每次等概率随机输入一个
#       小写字母，当某个 S_i 成为已输入串 T 的子串时停止。求停止时 |T| 的期望，模 1e9+7 输出。
#
# 数据范围（题面【提示】）：1 ≤ T ≤ 50，1 ≤ n ≤ 15，|S_i| ≤ 10。
# 时间 2000ms / 内存 256MB。
#
# 分层思路（10 组）：
#   点 1-4  边界/结构层（小，可手算或闭式核对）
#   点 5-6  小/中规模，多组、短模式
#   点 7    大规模随机（T=50 顶格，n=15 顶格，|S|=10 顶格，26 字母随机）
#   点 8    字母表收缩（2 字母 → 模式高度重叠、fail 链深、trie 近满）
#   点 9    结构层：所有模式共享长前缀 "aaa.." → 极深 fail 链 + 包含关系
#   点 10   顶格卡常层：T/n/|S| 三项全顶格 + 字母表 2 + 重复模式 + 前缀包含关系
#
# 可手算/闭式的点：
#   点 1：n=1, S="a" → 首次出现 a 的期望 = 26。
#   点 3：n=15, S = a..o 共 15 个单字母 → 每步命中概率 15/26，期望 = 26/15（有理数）。
# 随机均用 random.Random(1707*10+i) 独立种子，可复现。
# ---------------------------------------------------------------------------

from cyaron import *  # 引入CYaRon的库

import os
import random  # 显式引入（cyaron 的 star-import 不保证导出 random）

CASE_SEED = 1707
ALPHA26 = 'abcdefghijklmnopqrstuvwxyz'

# 以本脚本所在目录为基准：std 在同目录，.in/.out 输出到同目录的 data/ 子目录。
HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, 'std')
DATA_DIR = os.path.join(HERE, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)


def write_case(i, cases, note):
    """cases: list of (n, [pats...])；写出 problem<i>.in 并用标程生成 problem<i>.out。"""
    assert 1 <= len(cases) <= 50, len(cases)
    total_pat = 0
    for n, pats in cases:
        assert 1 <= n <= 15, n
        assert len(pats) == n, (n, pats)
        for p in pats:
            assert 1 <= len(p) <= 10, p
            assert all(c in ALPHA26 for c in p), p
        total_pat += n
    io = IO(file_prefix="problem", data_id=i)
    io.input_writeln(len(cases))
    for n, pats in cases:
        io.input_writeln(n)
        for p in pats:
            io.input_writeln(p)
    io.output_gen(STD)
    print(f"[{i:2d}] T={len(cases):2d} sum_n={total_pat:3d}  "
          f"n_range=[{min(n for n, _ in cases)},{max(n for n, _ in cases)}]  {note}")


def rnd_str(L, rnd, alpha=ALPHA26):
    return ''.join(rnd.choice(alpha) for _ in range(L))


# ---------------------------------------------------------------- 点 1：边界最小（可手算）
# T=1, n=1, |S|=1：等概率等 a 出现，期望 = 26。
write_case(1, [(1, ['a'])], "边界最小 n=1,|S|=1：期望 26（手算）")

# ---------------------------------------------------------------- 点 2：边界（单模式最长）
# T=1, n=1, |S|=10，同一字母重复；深链、fail 自指，检验最简结构下的大组答案。
write_case(2, [(1, ['a' * 10])], "边界 n=1,|S|=10 全同字母（深链 fail 自指）")

# ---------------------------------------------------------------- 点 3：闭式结构（可手算）
# n=15, S = 15 个互不相同的单字母：每步命中概率 15/26，
# 期望 = 26/15 = 26 * inv(15) mod 1e9+7 = 933333342。
write_case(3, [(15, list(ALPHA26[:15]))], "结构 n=15 全单字母：期望 26/15（闭式）")

# ---------------------------------------------------------------- 点 4：结构（重复 + 包含关系）
# 三组：① "ab","ab" 重复值 vs ② 单串 "ab"（答案应相同）；
#       ③ "a" 与 "ab"（后者是前者延长，前缀包含）；④ "abc" 与 "bc"（真后缀包含）。
# 检验「模式集合」语义而非多重计数。
write_case(4, [
    (2, ['ab', 'ab']),
    (1, ['ab']),
    (2, ['a', 'ab']),
    (2, ['abc', 'bc']),
], "结构：重复模式等价于单模式；前缀/后缀包含关系")

# ---------------------------------------------------------------- 点 5：小规模多组
# T=50（顶格组数），n∈[1,3]，|S|∈[1,3]，26 字母随机。多组小数据压力 + 覆盖短模式。
r5 = random.Random(CASE_SEED * 10 + 5)
cases5 = []
for _ in range(50):
    n = r5.randint(1, 3)
    cases5.append((n, [rnd_str(r5.randint(1, 3), r5) for _ in range(n)]))
write_case(5, cases5, "小规模：T=50 组，n∈[1,3]，|S|∈[1,3] 随机")

# ---------------------------------------------------------------- 点 6：中等规模（n 顶格）
# T=25，n=15（顶格），|S|∈[1,5]，26 字母随机 + 少量重复。覆盖 n 上限下的短模式。
r6 = random.Random(CASE_SEED * 10 + 6)
cases6 = []
for gi in range(25):
    n = 15
    pats = [rnd_str(r6.randint(1, 5), r6) for _ in range(n)]
    if gi % 5 == 0:          # 每 5 组插入一组重复值
        pats[0] = pats[1]
    if gi % 5 == 1:          # 每 5 组插入一组前缀包含
        p = rnd_str(4, r6)
        pats[0], pats[1] = p, p[:2]
    cases6.append((n, pats))
write_case(6, cases6, "中等规模：T=25，n=15 顶格，|S|∈[1,5]（含重复/包含）")

# ---------------------------------------------------------------- 点 7：大规模随机（三项顶格）
# T=50，n=15，|S|=10，26 字母随机，各串前缀基本不共享 → trie 节点数接近上限 151。
r7 = random.Random(CASE_SEED * 10 + 7)
cases7 = []
for _ in range(50):
    cases7.append((15, [rnd_str(10, r7) for _ in range(15)]))
write_case(7, cases7, "大规模随机：T=50,n=15,|S|=10 全顶格，26 字母")

# ---------------------------------------------------------------- 点 8：字母表收缩（2 字母）
# T=50，n=15，|S|=10，仅用 {a,b}：模式间高度重叠，fail 链长、终止态沿 fail 链大量传播，
# 非终止状态数显著下降——检验「字母表极小 + 长模式重叠」的极端。
r8 = random.Random(CASE_SEED * 10 + 8)
cases8 = []
for _ in range(50):
    seen = set()
    while len(seen) < 15:                     # 组内去重，保证 15 个不同模式
        seen.add(rnd_str(10, r8, 'ab'))
    cases8.append((15, sorted(seen)))
write_case(8, cases8, "字母表收缩：T=50,n=15,|S|=10，仅 a/b（高度重叠）")

# ---------------------------------------------------------------- 点 9：结构层（共享长前缀）
# T=50，n=15，|S|=10：全部模式共享 4 位前缀 "aaaa"，尾巴 6 位取自 {a,b,c}（分支多而浅）。
# 共享前缀制造极长公共链 + 高频终端传播；每隔一组把前两条换成 'a'*10 / 'a'*9，
# 形成「短模式是长模式前缀」的极端（终端态沿 fail 链向下传播一整条链）。
r9 = random.Random(CASE_SEED * 10 + 9)
cases9 = []
for gi in range(50):
    pre = 'aaaa'
    seen = set()
    while len(seen) < 15:
        seen.add(pre + rnd_str(6, r9, 'abc'))
    pats = sorted(seen)
    if gi % 2 == 0:                            # 每隔一组加入真前缀（共享前缀的极端）
        pats[0] = 'a' * 10
        pats[1] = 'a' * 9
    cases9.append((15, pats))
write_case(9, cases9, "结构：全模式共享 4 位前缀 + 互为前缀（长 fail 链）")

# ---------------------------------------------------------------- 点 10：顶格卡常层
# T=50，n=15，|S|=10 三项顶格，3 种构型轮转，均保证矩阵维数（非终止态数）尽量大：
#   构型 A：15 条互不同、长度均为 10 的 26 字母串，且前 4 位两两不同 → trie 恰好 1+15*10=151
#           个节点、15 个叶子全为终止态、无子串包含关系 → 非终止态 = 136（理论最大值）；
#           其中强制包含周期串 "ab"*5（fail 链自匹配最长）。
#   构型 B：14 条互不相同 + 1 条与首条重复（重复值，检验集合语义），其余同 A。
#   构型 C：前缀链 'a'*1,'a'*2,…,'a'*10（互为前缀，终端态沿 fail 链连续传播）+ 4 条长度 10
#           的 26 字母随机串 + 重复值 1 条。
r10 = random.Random(CASE_SEED * 10 + 10)
cases10 = []
for gi in range(50):
    flavor = gi % 3

    def gen10_distinct(prefix4_conflict_free=True):
        pats = []
        seen = set()
        pref4 = set()
        while len(pats) < 15:
            s = rnd_str(10, r10)
            if s in seen or (prefix4_conflict_free and s[:4] in pref4):
                continue
            seen.add(s)
            pref4.add(s[:4])
            pats.append(s)
        return pats

    if flavor == 0:                            # 构型 A：维数最大 + 周期串
        pats = gen10_distinct()
        pats[0] = 'ab' * 5                      # 周期串，fail 链最长
        assert len(set(pats)) == 15
    elif flavor == 1:                          # 构型 B：维数最大 + 重复值
        pats = gen10_distinct()
        pats[14] = pats[0]                      # 重复值
        assert len(set(pats)) == 14
    else:                                      # 构型 C：前缀链 + 随机 + 重复
        pats = ['a' * k for k in range(1, 11)]  # 10 条互为前缀
        pats += gen10_distinct()[:4]            # 4 条长串（其中可能含与 'a'*10 相同者则无碍）
        pats.append(pats[0])                    # 重复值
    assert len(pats) == 15
    assert all(1 <= len(p) <= 10 for p in pats)
    if flavor != 2:
        assert all(len(p) == 10 for p in pats)
    cases10.append((15, pats))
write_case(10, cases10, "顶格卡常：T=50,n=15,|S|=10；维数最大/重复值/前缀链 三构型轮转")
