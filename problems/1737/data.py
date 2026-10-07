#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1737《邮递员》分层数据生成器
# 范围（题面）：N≤5e4，M≤2e5，t≤1e4，Σ片段长≤1e6。
# 设计原则：TAK 点均显式构造「从 1 出发回到 1、线性包含全部片段」的欧拉回路
#   （环绕/线性两种语义同解）；NIE 点均因 片段弧缺失/粘合冲突/度数失衡/断连（两种语义同判 NIE）。
# 分层（10 组）：
#   p1  题面样例 → TAK
#   p2  片段引用不存在的弧 → NIE
#   p3  两片段粘合冲突 → NIE
#   p4  小规模 TAK 构造（n=10）
#   p5  中规模 TAK 构造（n=200，多片段）
#   p6  失衡 NIE（删一条弧）
#   p7  断连 NIE（两个平衡分量）
#   p8  大规模 TAK 构造（n=1e4，Σk≈3e5）
#   p9  大规模冲突 NIE（Σk≈6e5，藏一处冲突）
#   p10 顶格 TAK（n=5e4，M=2e5，t=1e4，Σk≈1e6）
import random
random.seed(1737)

def build(n, cycles):
    """由若干条经过 1 的圈拼出图与显式回路（弧序列）。"""
    edges = set()
    arcseq = []   # 显式回路的弧（(a,b)），按拼接顺序
    for cyc in cycles:
        for i in range(len(cyc) - 1):
            a, b = cyc[i], cyc[i + 1]
            if a == b or (a, b) in edges:
                raise ValueError('duplicate arc')
            edges.add((a, b))
            arcseq.append((a, b))
    return sorted(edges), arcseq

def frags_from(arcseq, count, kmax, avoid_junction=0):
    """从显式回路取窗口片段（避开拼接接缝，保证线性可实现）。"""
    m = len(arcseq)
    frags = []
    for _ in range(count):
        k = random.randint(2, kmax)
        s = random.randint(0, max(0, m - k - avoid_junction))
        vs = [arcseq[s][0]] + [arcseq[s + j][1] for j in range(k - 1)]
        frags.append(vs)
    return frags

def emit(name, n, edges, frags, expect):
    with open(f'data/{name}.in', 'w') as f:
        f.write(f'{n} {len(edges)}\n')
        for a, b in edges:
            f.write(f'{a} {b}\n')
        f.write(f'{len(frags)}\n')
        for fr in frags:
            f.write(f'{len(fr)} ' + ' '.join(map(str, fr)) + '\n')
    print(name, f'n={n} m={len(edges)} t={len(frags)} Σk={sum(len(x) for x in frags)} expect={expect}')

def rand_cycles(n, r, minlen=2, maxlen=6):
    """r 条经过 1 的圈，圈内点互异、弧全局不重复（冲突重采样）。"""
    cycles = []
    used_arcs = set()
    for _ in range(r):
        for _try in range(200):
            L = random.randint(minlen, maxlen)
            mids = random.sample(range(2, n + 1), min(L - 2, max(0, n - 1))) if n >= 3 else []
            cyc = [1] + mids + [1]
            arcs = [(cyc[i], cyc[i + 1]) for i in range(len(cyc) - 1)]
            if any(a in used_arcs or a[0] == a[1] for a in arcs):
                continue
            used_arcs.update(arcs)
            cycles.append(cyc)
            break
    return cycles

# p1 题面样例
sample_edges = [(1,5),(1,3),(4,1),(6,4),(3,6),(3,4),(4,3),(5,6),(6,2),(2,1)]
sample_frags = [[1,5,6],[3,4,3],[4,3,6,4],[5,6,2]]
emit('problem1', 6, sample_edges, sample_frags, 'TAK')

# p2 片段弧缺失
emit('problem2', 3, [(1,2),(2,3)], [[1,3,2]], 'NIE')

# p3 粘合冲突：(1,2) 后必须接 (2,3) 又必须接 (2,4)
emit('problem3', 4, [(1,2),(2,3),(2,4),(3,1),(4,1)], [[1,2,3],[1,2,4]], 'NIE')

# p4 小 TAK
cycs = rand_cycles(10, 6, 3, 6)
edges, arcseq = build(10, cycs)
emit('problem4', 10, edges, frags_from(arcseq, 10, 4), 'TAK')

# p5 中 TAK（n=200）
cycs = rand_cycles(200, 120, 3, 8)
edges, arcseq = build(200, cycs)
emit('problem5', 200, edges, frags_from(arcseq, 300, 6), 'TAK')

# p6 失衡 NIE：p5 结构删一条非 1 弧
edges2 = edges[:-1] if edges[-1][0] == 1 else [e for e in edges if e != edges[-1]]
emit('problem6', 200, edges2, frags_from(arcseq, 50, 5), 'NIE')

# p7 断连 NIE：两个平衡分量（1 的圈 + 独立圈）
cycs_a = rand_cycles(10, 4, 3, 5)
edges_a, seq_a = build(10, cycs_a)
edges_b = [(20,21),(21,22),(22,20)]
emit('problem7', 22, sorted(set(edges_a) | set(edges_b)), frags_from(seq_a, 8, 4), 'NIE')

# p8 大 TAK（n=1e4）
cycs = rand_cycles(10000, 800, 3, 20)
edges, arcseq = build(10000, cycs)
emit('problem8', 10000, edges, frags_from(arcseq, 3000, 30), 'TAK')

# p9 大冲突 NIE（在 TAK 构造上叠一对冲突片段）
edges9, seq9 = edges, arcseq
frags9 = frags_from(seq9, 3000, 30)
# 人为制造冲突：取某弧 (a,b)，编两个片段分别接不同后继
a, b = seq9[5]
outs = [(x, y) for (x, y) in edges9 if x == b][:2]
if len(outs) == 2:
    frags9.append([a, b, outs[0][1]])
    frags9.append([a, b, outs[1][1]])
emit('problem9', 10000, edges9, frags9, 'NIE')

# p10 顶格 TAK（n=5e4，M=2e5，t=1e4，Σk≈1e6）
cycs = rand_cycles(50000, 25000, 3, 12)
edges10, seq10 = build(50000, cycs)
frags10 = frags_from(seq10, 10000, 150)
emit('problem10', 50000, edges10, frags10, 'TAK')
print('done')
