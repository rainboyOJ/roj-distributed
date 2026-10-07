#!/usr/bin/env python3
# 数据生成器：一本通 1704《奇特的猫》
# 输入分三行，每行是一天的按键序列（ASCII 值，8 为退格）。
# 数据规模按 "集合结点数 |S|" 分层，10 个点从最小铺到顶格 10^6。
#
# 生成思路：
#   一个按键序列产生的集合 S 恰好是一棵 Trie 的结点集合（S 天然前缀封闭）。
#   先按目标结点数 target 构造一棵 Trie（用"每个结点的孩子数"的先序数组描述），
#   再用显式栈做先序 DFS 生成按键序列：进入一个孩子输出该孩子字符，离开该孩子
#   输出一次退格(8)。这样得到的按键序列长度恰为 2*(target-1)，且能精确复现这棵树。
#   空串、深链、宽树、菊花等结构都能直接构造。
import random
from cyaron import IO

# 1..127 可打印 ASCII（不含 8，避免与退格冲突）
CHARS = [c for c in range(1, 128) if c != 8]

def build_day(target, rnd, cap):
    """构造一棵 target 个结点的 Trie，返回按键 tokens 与实际结点数。
    先序数组 sizes[i] = 结点 i 的孩子数；ids 按先序分配。"""
    sizes = [0]          # 根（空串）
    remaining = target - 1
    stack = [0]          # 待"打开"（分配孩子）的结点，栈顶先处理 -> 先序
    while stack and remaining > 0:
        v = stack.pop()
        maxk = min(remaining, rnd.randint(1, cap))
        k = rnd.randint(1, maxk)
        sizes[v] = k
        children = list(range(len(sizes), len(sizes) + k))
        sizes.extend([0] * k)
        remaining -= k
        # 孩子按先序入栈：先让第一个孩子被处理
        for c in reversed(children):
            stack.append(c)
    # 显式栈 DFS 生成按键序列（先序）
    tokens = []
    nid = 0               # 新结点编号 = 先序 id
    st = [(0, 0)]
    while st:
        v, ci = st.pop()
        if ci < sizes[v]:
            st.append((v, ci + 1))
            tokens.append(rnd.choice(CHARS))
            nid += 1
            st.append((nid, 0))
        elif v != 0:
            tokens.append(8)
    return tokens, target

def line_to_str(tokens):
    return " ".join(map(str, tokens))

def main():
    rnd = random.Random(20240517)

    # 每层设计（三元组为三天的目标 Trie 结点数 = |S|，均不超过题面上限 10^6）
    cases = [
        # 1. 边界层：n=1（仅空串）
        (1, 1, 1),
        # 2. 边界层：n=2（空串 + 单字符）
        (2, 2, 2),
        # 3. 小规模随机：可手算验证
        (5, 6, 7),
        # 4. 小规模随机
        (10, 12, 14),
        # 5. 中等规模随机：范围中间档
        (300, 500, 700),
        # 6. 中等规模随机
        (2000, 3000, 4000),
        # 7. 大规模随机
        (50000, 80000, 100000),
        # 8. 大规模随机：接近上限
        (200000, 300000, 400000),
        # 9. 顶格层：接近上限的宽树（多分支）
        (600000, 800000, 900000),
        # 10. 顶格层：|S|=10^6 的深链（最坏结构，深度/距离和极端）
        (1000000, 1000000, 1000000),
    ]

    for i, (a, b, c) in enumerate(cases, start=1):
        io = IO(file_prefix="problem", data_id=i)
        cap = 1 if i == 10 else (8 if i == 9 else 3)
        ta, _ = build_day(a, rnd, cap)
        tb, _ = build_day(b, rnd, cap)
        tc, _ = build_day(c, rnd, cap)
        io.input_writeln(line_to_str(ta))
        io.input_writeln(line_to_str(tb))
        io.input_writeln(line_to_str(tc))
        io.output_gen("../std")

if __name__ == "__main__":
    main()
