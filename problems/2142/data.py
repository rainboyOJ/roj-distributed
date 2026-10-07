#!/usr/bin/env python
# 一本通 2142《树边匹配》数据生成器
#
# 输入：第一行 n（1<=n<=2e5），接下来 n-1 行每行一条边 a b（1<=a,b<=n）。
# 输出：一个整数，最大匹配边数（每点至多是选中一条边的端点）。
#
# 分层设计（10 组，单测点）：
#   1     边界层：n=1（最小值，无边的极端，答案 0）
#   2     边界层：n=2（最小非平凡，答案 1）
#   3     小规模：题面样例 n=5（手算 = 2）
#   4     小规模：n=500 均匀随机树（可手算量级）
#   5     中等规模：n=5000 均匀随机树（范围中间档）
#   6     中等规模：n=16383 = 2^14-1 完全二叉树（结构规则，答案有规律）
#   7     大规模：n=150000 均匀随机树（接近上限）
#   8     大规模：n=200000 链 1-2-3-...-n（深度顶格 2e5，最容易爆递归栈）
#   9     顶格层：n=200000 星形（度数顶格，答案 1 的最小非零极端）
#   10    顶格层：n=200000 扫帚 broom（10 万长链 + 10 万叶子挂在链尾，
#          同时压深度与度数的混合最坏结构，答案仍为 1e5）

import random
from cyaron import *  # 引入CYaRon的库

random.seed(2142)

MAXN = 200000


def emit(data_id, n, edges, note=""):
    """写出单个测点：n 与 n-1 条边。edges 为 1-indexed 的 (a,b) 列表。"""
    assert 1 <= n <= MAXN, f"n={n} 超出题面上限"
    assert len(edges) == n - 1, f"边数 {len(edges)} != n-1={n - 1}"
    for a, b in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b, f"非法边 ({a},{b})"
    io = IO(file_prefix="problem", data_id=data_id)
    lines = [str(n)] + ["%d %d" % (a, b) for a, b in edges]
    io.input_write("\n".join(lines) + "\n")
    io.output_gen("../std")


def rand_tree(n, lo=1):
    """均匀随机树：节点 v 的父节点在 [lo, v-1] 中均匀取。"""
    return [(random.randint(lo, v - 1), v) for v in range(2, n + 1)]


# ---- 1. 边界：n=1（最小值；不存在任何边，答案 0）----
emit(1, 1, [], "n=1 最小边界")

# ---- 2. 边界：n=2（最小非平凡情形，答案 1）----
emit(2, 2, [(1, 2)], "n=2 边界")

# ---- 3. 小规模：题面样例 ----
emit(3, 5, [(1, 2), (1, 3), (3, 4), (3, 5)], "题面样例，手算答案 2")

# ---- 4. 小规模：n=500 均匀随机树（手算量级/抽查）----
emit(4, 500, rand_tree(500), "n=500 随机")

# ---- 5. 中等规模：n=5000 均匀随机树 ----
emit(5, 5000, rand_tree(5000), "n=5000 随机")

# ---- 6. 中等规模：n=16383 = 2^14-1 完全二叉树 ----
n6 = (1 << 14) - 1
emit(6, n6, [((v // 2), v) for v in range(2, n6 + 1)], "n=16383 完全二叉树")

# ---- 7. 大规模：n=150000 均匀随机树 ----
emit(7, 150000, rand_tree(150000), "n=150000 随机")

# ---- 8. 大规模：n=200000 链（深度顶格，递归爆栈风险）----
emit(8, MAXN, [(i, i + 1) for i in range(1, MAXN)], "n=200000 链")

# ---- 9. 顶格层：n=200000 星形（度数顶格，答案 1）----
emit(9, MAXN, [(1, v) for v in range(2, MAXN + 1)], "n=200000 星形")

# ---- 10. 顶格层：n=200000 扫帚（长链+尾端大量叶子）----
half = MAXN // 2                      # 100000
edges10 = [(i, i + 1) for i in range(1, half)]              # 链 1..half
edges10 += [(half, v) for v in range(half + 1, MAXN + 1)]   # 其余挂链尾
emit(10, MAXN, edges10, "n=200000 扫帚(broom)")
