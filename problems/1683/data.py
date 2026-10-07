#!/usr/bin/env python3
# 一本通 1683 《稗田阿求》 分层测试数据生成器 (cyaron)
# 分层设计:
#   p1: 边界层  N=1,M=1,L=1 全最小值, 唯一字母唯一数字 -> ans=1
#   p2: 边界层  N=2,M=2, 两组直接冲突 (字母少, 最大独立), 答案 1 的极端
#   p3: 小规模随机 N=3,M=4, 沿用题面样例 (可手算验证, ans=2)
#   p4: 小规模随机 N=6,M=8, L<=6, 已由暴力对拍验证的量级
#   p5: 中等规模  N=10,M=20 (60%分档上限), 一半组来自同一真实映射(必相容) + 一半随机
#   p6: 中等规模  N=16,M=30, L<=40, 纯随机
#   p7: 大规模    N=26,M=40 (顶格), 20组同源相容 + 20组随机, 混合
#   p8: 大规模    N=26,M=40, 循环移位构造: 26 种全局映射各出现若干次, 答案=重复次数上限, 深冲突结构
#   p9: 顶格最坏结构 N=26,M=40,L=100: 40组全部两两相容 (同一映射), 卡 dfs 全选分支, ans=40
#   p10: 顶格最坏结构 N=26,M=40,L=100: 组 i 与组 j 仅在最后字母上冲突 (接近全相容的深树), 卡剪枝
from cyaron import *
import random

def rand_group(n, L, mapping=None):
    """生成一组合法 (文字段, 数列): 组内字母->数字是单射。
       mapping: 若给出则按该全局映射(字母->数字)生成, 保证与其他同 mapping 组相容。"""
    if mapping is None:
        letters = random.sample(range(n), min(n, L))
        values = random.sample(range(1, n + 1), len(letters))
        mp = dict(zip(letters, values))
    else:
        letters = list(range(n))
        mp = mapping
    word, seq = [], []
    for _ in range(L):
        c = random.choice(letters)
        word.append(chr(65 + c))
        seq.append(mp[c])
    return ''.join(word), seq

def write_case(io, n, groups):
    io.input_writeln(n, len(groups))
    for w, s in groups:
        io.input_writeln(w)
        io.input_writeln(' '.join(map(str, s)))
    io.output_gen("../std")

random.seed(123456789)

for t in range(1, 11):
    io = IO(file_prefix="problem", data_id=t)
    if t == 1:
        # p1: 最小边界 N=M=L=1
        write_case(io, 1, [('A', [1])])
    elif t == 2:
        # p2: N=2,M=2 两组冲突, 答案=1
        write_case(io, 2, [('AB', [1, 2]), ('AB', [2, 1])])
    elif t == 3:
        # p3: 题面样例原样, 可手算 ans=2
        write_case(io, 3, [('ACCA', [1, 3, 3, 1]),
                           ('AAC', [2, 2, 1]),
                           ('BCBC', [3, 1, 3, 1])])
    elif t == 4:
        # p4: 小规模随机, 暴力可验证
        n = 6
        groups = [rand_group(n, random.randint(1, 6)) for _ in range(8)]
        write_case(io, n, groups)
    elif t == 5:
        # p5: 中档, 一半同源(相容)一半随机
        n = 10
        perm = list(range(1, n + 1)); random.shuffle(perm)
        base = {c: perm[c] for c in range(n)}
        groups = [rand_group(n, random.randint(1, 20), base) for _ in range(10)]
        groups += [rand_group(n, random.randint(1, 20)) for _ in range(10)]
        write_case(io, n, groups)
    elif t == 6:
        # p6: 中档纯随机
        n = 16
        groups = [rand_group(n, random.randint(1, 40)) for _ in range(30)]
        write_case(io, n, groups)
    elif t == 7:
        # p7: 顶格 N,M, L<=100, 20 同源 + 20 随机混合
        n = 26
        perm = list(range(1, n + 1)); random.shuffle(perm)
        base = {c: perm[c] for c in range(n)}
        groups = [rand_group(n, random.randint(50, 100), base) for _ in range(20)]
        groups += [rand_group(n, random.randint(50, 100)) for _ in range(20)]
        random.shuffle(groups)
        write_case(io, n, groups)
    elif t == 8:
        # p8: 循环移位映射, 同余类内相容、类间全冲突, ans=最大类大小
        n = 26
        groups = []
        for g in range(40):
            mp = {c: ((c + g) % 26) + 1 for c in range(26)}
            groups.append(rand_group(n, random.randint(50, 100), mp))
        write_case(io, n, groups)
    elif t == 9:
        # p9: 顶格最坏结构: 40 组全部同一映射, 两两全相容, ans=40
        n = 26
        perm = list(range(1, n + 1)); random.shuffle(perm)
        base = {c: perm[c] for c in range(n)}
        groups = [rand_group(n, 100, base) for _ in range(40)]
        write_case(io, n, groups)
    else:
        # p10: 顶格最坏结构(近团): 39 组同一全局双射 + 1 组交换其中两个数字,
        #      仅这 1 组与其余全冲突, ans=39, 卡分支限界剪枝
        n = 26
        perm = list(range(1, n + 1)); random.shuffle(perm)
        base = {c: perm[c] for c in range(26)}
        bad = dict(base); bad[0], bad[1] = base[1], base[0]
        groups = [rand_group(n, 100, base) for _ in range(39)]
        groups.append(rand_group(n, 100, bad))
        write_case(io, n, groups)
