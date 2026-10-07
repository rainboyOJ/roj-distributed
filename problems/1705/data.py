#!/usr/bin/env python
# 一本通 1705《DNA序列》数据生成器（cyaron 惯例）
# 题面范围：m <= 10，n <= 2e9，每个禁止子串长度 <= 10，字符集 ACTG，答案模 100000。
# 10 个测试点分层：边界 -> 小随机 -> 中随机 -> 大随机 -> 顶格最坏结构。

from cyaron import *
import random

CS = "ACTG"

def rand_pattern(rng, L):
    return ''.join(rng.choice(CS) for _ in range(L))

def make(rng, m, n, pats):
    """返回 (input 文本, 描述)"""
    inp = "%d %d\n" % (m, n)
    for p in pats:
        inp += p + "\n"
    return inp

for i in range(1, 11):
    io = IO(file_prefix="problem", data_id=i)
    rng = random.Random(17050000 + i)

    # ---------- 分层构造 ----------
    if i == 1:
        # 边界层：n=1 最小长度；m=1；单个最短禁止串（长度 1）；答案 = 3（可手算）
        # 输入: 1 1 / A  =>  合法串为 C,T,G 共 3 个
        m, n, pats = 1, 1, ["A"]
        note = "边界: n=1(最小), m=1, 长度1禁止串, 答案3"
    elif i == 2:
        # 边界层：全部 4 个单字符禁止 => 答案 0（极端：无解）
        m, n, pats = 4, 1, ["A", "C", "T", "G"]
        note = "边界: 全部单字符禁止, 答案0"
    elif i == 3:
        # 边界层：m=0（无任何禁止串，允许 0 个模式）；n 较小 => 答案 4^n mod 1e5
        m, n, pats = 0, 7, []
        note = "边界: m=0 无禁止串, 答案=4^7=16384"
    elif i == 4:
        # 边界/结构层：禁止串互为前缀（一个串是另一个的前缀），
        # 考察 fail 指针后缀 danger 继承是否正确；n 小可暴力验证
        m, n, pats = 3, 8, ["ACT", "AC", "A"]
        note = "结构: 前缀嵌套模式 {ACT,AC,A} 考察fail继承, n=8"
    elif i == 5:
        # 小规模随机：可手算/暴力验证的量级
        m = 4
        n = rng.randint(5, 12)
        pats = [rand_pattern(rng, rng.randint(1, 4)) for _ in range(m)]
        note = "小随机: m=4, n=%d, |s|<=4" % n
    elif i == 6:
        # 小-中规模随机：含重复模式（题面未禁止重复）
        m = 6
        n = rng.randint(10, 20)
        pats = [rand_pattern(rng, rng.randint(1, 6)) for _ in range(m)]
        pats.append(pats[0])  # 重复一个
        m = len(pats)
        note = "中小随机: m=%d 含重复模式, n=%d" % (m, n)
    elif i == 7:
        # 中等规模随机：m 取中间档，模式长度中等，n 进入 1e6 级
        m = 6
        n = 10 ** 6
        pats = [rand_pattern(rng, rng.randint(5, 8)) for _ in range(m)]
        note = "中随机: m=6, n=1e6, |s|5..8"
    elif i == 8:
        # 大规模随机：m=10 顶格，n 接近上限，模式随机长
        m = 10
        n = 1999999999
        pats = [rand_pattern(rng, rng.randint(1, 10)) for _ in range(m)]
        note = "大随机: m=10, n=1999999999, |s|1..10"
    elif i == 9:
        # 顶格层：全部模式取上限长度 10，n=2e9 顶格；随机最坏结构
        m = 10
        n = 2000000000
        pats = [rand_pattern(rng, 10) for _ in range(m)]
        note = "顶格: m=10 全长10模式, n=2e9 随机"
    else:
        # 顶格层（最坏结构）：n=2e9 顶格 + 前缀嵌套 + 重复 + 长度 10：
        #   一个长度 10 的模式及其多个前缀（制造深度 Trie 与 fail 链），
        #   加重复项（题面未禁止重复输入），卡"是否正确去重/建图"的实现。
        base = rand_pattern(rng, 10)
        pats = [base, base[:5], base[:8], base[:1]]
        pats += [rand_pattern(rng, 10) for _ in range(4)]
        pats += [pats[0]]  # 重复
        m = len(pats)
        n = 2000000000
        note = "顶格最坏: 前缀嵌套+重复+全长10, m=%d, n=2e9" % m

    inp = make(rng, m, n, pats)
    io.input_write(inp)  # 原样写入（含换行的多行文本）
    io.output_gen("../std")
    print("test %2d: %s" % (i, note))
