#!/usr/bin/env python3
# 一本通 1692《字符串编码》分层数据生成器
# 数据范围：n,m ≤ 2×10^5（官方题面确认）。10 个测试点从最小铺到顶格。
from cyaron import *
import random

ALPH = 'abcdefghijklmnopqrstuvwxyz'

def rs(length, alpha):
    return ''.join(random.choice(alpha) for _ in range(length))

def rand_perm_mapping(src_letters, ident_p=0.5, alpha=ALPH):
    """对 src_letters 中每个字母，以 ident_p 概率恒等，否则与字母表中
    随机未占用字母配对（构成合法编码映射的对合限制由调用场景保证宽松）。"""
    pool = list(alpha)
    random.shuffle(pool)
    mp = {}
    used = set()
    for c in src_letters:
        if random.random() < ident_p:
            mp[c] = c
        else:
            while pool and pool[-1] in used:
                pool.pop()
            if pool:
                d = pool.pop()
                mp[c] = d
                used.add(c); used.add(d)
            else:
                mp[c] = c
    return mp

def encode(u, mp):
    return ''.join(mp[c] for c in u)

random.seed(20241692)

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)

    if i == 1:
        # 边界层：n=m=1，最小规模，单字母相等（答案恒为 1）
        n = m = 1
        S, T = 'a', 'a'

    elif i == 2:
        # 边界层：最小无匹配点。S=ab, T=cd——若 f(a)=c,f(b)=d 则需 c,d 都入选配对，
        # 但 c,d 不在 U 中出现时仍可配对的解释有歧义（见 gen-report 风险点），
        # 这里取 ab->cd：无论宽严解释，双射要求两对字母 (a,c),(b,d) 均合法，
        # 宽松解释下也合法……为保险改用 答案=0 的严格无匹配：
        # S=ab, T=ca：f(a)=c,f(b)=a，则 a 既映到 c 又是 b 的像，需 a->c 且 a->? 矛盾，
        # 任何解释下都不合法（k=0）。
        n, m = 2, 2
        S, T = 'ab', 'ca'

    elif i == 3:
        # 小规模随机：n,m≤10（题面 10% 档），小字母表，手算可验证
        n = random.randint(8, 10); m = random.randint(3, 5)
        S = rs(n, 'abc'); T = rs(m, 'abc')

    elif i == 4:
        # 小规模：T 由 S 的子串经随机字母对编码生成（构造正例密集）
        n = 10; m = 5
        S = rs(n, 'abcd')
        p = random.randint(0, n - m)
        mp = rand_perm_mapping(set(S[p:p+m]))
        T = encode(S[p:p+m], mp)

    elif i == 5:
        # 中等随机：n=2000, m=50（题面 30% 档 m≤50 的上沿），小字母表易出匹配
        n, m = 2000, 50
        S = rs(n, 'abcde'); T = rs(m, 'abcde')

    elif i == 6:
        # 中等随机：n=20000, m=5000，全字母表，答案大概率稀疏/为 0
        n, m = 20000, 5000
        S = rs(n, ALPH); T = rs(m, ALPH)

    elif i == 7:
        # 大规模随机：n=150000, m=100000，中等字母表随机
        n, m = 150000, 100000
        S = rs(n, 'abcdefghij'); T = rs(m, 'abcdefghij')

    elif i == 8:
        # 大规模：S 中周期性嵌入多个经编码的 T（正例密集 + 长滑窗压力）
        n, m = 200000, 40000
        base = rs(m, 'abcdefgh')
        T = base
        parts = []
        pos = 0
        while pos + m <= n:
            mp = rand_perm_mapping(set(base), ident_p=0.5)
            parts.append(encode(base, mp))
            pos += m + random.randint(1, 3) * m // 4
        S = ''.join(parts)
        S = (S + rs(n, 'abcdefgh'))[:n]

    elif i == 9:
        # 顶格最坏结构 1：全相同字母。S='a'*n, T='a'*m —— 每个起点都匹配，
        # k=n-m+1=100001 个答案，考验输出规模与滑窗 O(1) 更新
        n, m = 200000, 100000
        S = 'a' * n; T = 'a' * m

    else:  # i == 10
        # 顶格最坏结构 2：高重复周期串 + 近顶格 m（m=199999），
        # prev 编码大量变化下标，考验滑窗修正逻辑与 O(26n) 判定
        n, m = 200000, 199999
        unit = rs(97, ALPH)
        S = (unit * (n // 97 + 1))[:n]
        T = S[0:m]

    io.input_writeln(n, m)
    io.input_writeln(S)
    io.input_writeln(T)
    io.output_gen("../std")
    print(f"problem{i}: n={n} m={m}")
