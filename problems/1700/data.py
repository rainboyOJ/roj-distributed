#!/usr/bin/env python3
# 一本通 1700《PFS集合》分层数据生成器
# 数据范围: 1 <= n <= 50000, 每个字符串长度 <= 50, 小写字母, 互不相同。
# 分层设计:
#   点 1-2  边界层: n=1 / n=2 前缀冲突 / 全最小长度
#   点 3-4  小规模随机(手算量级): n=5 / n=12
#   点 5-6  中等规模随机: n=200 / n=2000
#   点 7-8  大规模随机: n=15000 / n=35000
#   点 9-10 顶格层: n=50000, 长度恰好 50(全最大值长度) / 满 26 叉 trie(卡常结构)
import random
from cyaron import IO

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def rand_str(min_len=1, max_len=50):
    L = random.randint(min_len, max_len)
    return "".join(random.choice(ALPHABET) for _ in range(L))


def unique_strings(n, min_len=1, max_len=50):
    """生成 n 个互不相同的小写字符串。"""
    seen = set()
    while len(seen) < n:
        seen.add(rand_str(min_len, max_len))
    return list(seen)


def full_trie_strings(n):
    """生成近似满 26 叉 trie 的串集合, 使 trie 节点数尽量多(卡常结构)。
    从短到长逐层填充, 每个串长度 <= 50。"""
    import collections
    strs = []
    q = collections.deque([""])
    while len(strs) < n and q:
        p = q.popleft()
        if p:
            strs.append(p)
        if len(p) < 50:
            for c in ALPHABET:
                q.append(p + c)
                if len(strs) >= n:
                    break
    while len(strs) < n:
        strs.append(rand_str())
    return strs[:n]


def emit(data_id, strings):
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_writeln(len(strings))
    for s in strings:
        io.input_writeln(s)
    io.output_gen("../std")


# 点 1: 边界层 n=1, 长度为 1。答案 = 空集 + {a} = 2
emit(1, ["a"])

# 点 2: 边界层 n=2, 直接前缀冲突 {"a", "ab"} -> 空集 + 两个单元素 = 3
emit(2, ["a", "ab"])

# 点 3: 小规模随机 n=5, 手算量级
emit(3, unique_strings(5, 1, 4))

# 点 4: 小规模随机 n=12, 长度 1..6
emit(4, unique_strings(12, 1, 6))

# 点 5: 中等规模 n=200
emit(5, unique_strings(200, 1, 20))

# 点 6: 中等规模 n=2000, 长度 1..30
emit(6, unique_strings(2000, 1, 30))

# 点 7: 大规模 n=15000, 长度 1..50
emit(7, unique_strings(15000, 1, 50))

# 点 8: 大规模 n=35000, 长度 1..50
emit(8, unique_strings(35000, 1, 50))

# 点 9: 顶格 n=50000, 长度恰好 50(全最大值长度), 随机
emit(9, unique_strings(50000, 50, 50))

# 点 10: 顶格 n=50000, 满 26 叉 trie 最坏卡常结构, 长度 <= 50
emit(10, full_trie_strings(50000))
