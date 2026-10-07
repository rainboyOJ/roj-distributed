#!/usr/bin/env python3
# 一本通 1723《交通》数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（content.md）：
#   1 <= n <= 200，1 <= m <= 400（m 为双向边条数，可有重边，无自环），
#   1 <= x, y <= 10^7（且题面声明"所有 x,y 均在其范围内随机生成"），
#   保证 S 到 T 存在路径；多组数据：单组（每组一个 n,m,S,T）。
#   时间 3000 ms / 内存 256 MB（config.json）。
#
# 输出说明：题面只写"一行一个实数"，样例为 "2.5" / "13.0"（非定点位数）。
#   std 按 %.10f 输出后去掉多余尾零（至少保留一位小数），与样例逐字符一致。
#
# 分层设计（10 组，从小到大铺到顶格）：
#   点 1-2  边界层：n=2 最小规模 / 全最小值 / 极端权值 / 重边 / 手算可验证；
#   点 3-4  小规模随机：n=5,10（30% 档 n<=10 内）；
#   点 5-6  中等规模随机：n=50,100，权重多档；
#   点 7-8  大规模随机/构造：n=200, m=400 链式长路径 + 重边结构；
#   点 9-10 顶格层：n=200, m=400 双顶格，重边最多结构（折点最坏）与极端权值混合。
from cyaron import IO, randint, random


def write_case(data_id, n, edges, S, T):
    """edges: list[(u,v,x,y)]；按题面格式写出并调用 std 生成 .out。"""
    io = IO(file_prefix="problem", data_id=data_id)
    lines = [f"{n} {len(edges)} {S} {T}"]
    for u, v, x, y in edges:
        lines.append(f"{u} {v} {x} {y}")
    io.input_write("\n".join(lines), "\n")
    io.output_gen("../std")


def chain_plus_random(n, m, wlo, whi, rng=random):
    """链 1-2-...-n（保证 S=1 连通到 T=n）再加随机边补到 m 条，O(m)。"""
    edges = []
    for i in range(1, n):
        edges.append((i, i + 1, rng.randint(wlo, whi), rng.randint(wlo, whi)))
    while len(edges) < m:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u == v:
            continue
        edges.append((u, v, rng.randint(wlo, whi), rng.randint(wlo, whi)))
    return edges


# ---------------- 点 1：边界层 ----------------
# n=2, m=1 最小规模；x=y=1 全最小值（题面下界）；
# 单边时 d(a) = 1 恒为常数，答案为 1（"答案为整/退化"极端）。
def gen1():
    write_case(1, 2, [(1, 2, 1, 1)], 1, 2)


# ---------------- 点 2：边界层 ----------------
# n=2, m=2 重边 + 极端权值（1 与 10^7 对调）：
#   d(a) = min(10^7 - 9999999a, 1 + 9999999a)，在 a=1/2 相交，
#   手算答案 = 2*∫_0^{1/2}(1+9999999a) da = 2500000.75（见 gen-report）。
def gen2():
    write_case(2, 2, [(1, 2, 1, 10 ** 7), (1, 2, 10 ** 7, 1)], 1, 2)


# ---------------- 点 3：小规模随机 ----------------
# n=5, m=6（与题面样例同量级），权值 1..20：可手算/小规模核对。
def gen3():
    random.seed(172303)
    write_case(3, 5, chain_plus_random(5, 6, 1, 20), 1, 5)


# ---------------- 点 4：小规模随机 ----------------
# n=10（30% 档上限），m=20（30% 档上限），权值 1..1000。
def gen4():
    random.seed(172304)
    write_case(4, 10, chain_plus_random(10, 20, 1, 1000), 1, 10)


# ---------------- 点 5：中等规模随机 ----------------
# n=50, m=100，权值 1..10^5；含少量 x=y 的常数边（题面允许 x 与 y 任意）。
def gen5():
    random.seed(172305)
    edges = chain_plus_random(50, 100, 1, 10 ** 5)
    for k in range(0, len(edges), 7):
        u, v, x, _ = edges[k]
        edges[k] = (u, v, x, x)
    write_case(5, 50, edges, 1, 50)


# ---------------- 点 6：中等规模随机 ----------------
# n=100, m=200，权值 1..10^6；S=1,T=100。
def gen6():
    random.seed(172306)
    write_case(6, 100, chain_plus_random(100, 200, 1, 10 ** 6), 1, 100)


# ---------------- 点 7：大规模随机 ----------------
# n=200, m=400 接近上限，权值全域 1..10^7 随机（题面声明随机生成的口径）。
def gen7():
    random.seed(172307)
    write_case(7, 200, chain_plus_random(200, 400, 1, 10 ** 7), 1, 200)


# ---------------- 点 8：大规模构造（全最大值 / 全相等边界） ----------------
# n=200, m=400（顶格）：199 条链边权值全为 (x=y=10^7)（题面权值上限、全相等），
# 另 201 条为链段上的平行重边（同样全为 10^7）。
# 每条边任意 a 下耗时恒 = 10^7，故答案恰为 199*10^7 = 1990000000（全相等退化 + 答案量级上限）。
def gen8():
    edges = []
    for i in range(1, 200):
        edges.append((i, i + 1, 10 ** 7, 10 ** 7))
    while len(edges) < 400:
        i = randint(1, 199)
        edges.append((i, i + 1, 10 ** 7, 10 ** 7))
    write_case(8, 200, edges, 1, 200)


# ---------------- 点 9：顶格层（折点最坏结构） ----------------
# n=200, m=400 双顶格：300 条 1-2 平行边，每条路径只含 1 条边，
# 期望最短路 = 300 条直线的下包络 —— 折点数上限结构，卡分治递归；
# 其余 100 条随机边。权值全域随机。
def gen9():
    random.seed(172309)
    edges = []
    for _ in range(300):
        edges.append((1, 2, randint(1, 10 ** 7), randint(1, 10 ** 7)))
    while len(edges) < 400:
        u = randint(2, 200)
        v = randint(2, 200)
        if u == v:
            continue
        edges.append((u, v, randint(1, 10 ** 7), randint(1, 10 ** 7)))
    write_case(9, 200, edges, 1, 2)


# ---------------- 点 10：顶格层（极端权值混合） ----------------
# n=200, m=400 双顶格：权值只取 {1, 10^7} 两档极端值（一半一半），
# 覆盖最大数量级差与全边界权值；结构为链 + 随机边。
def gen10():
    random.seed(172310)
    def ext():
        return 1 if randint(0, 1) == 0 else 10 ** 7
    edges = []
    for i in range(1, 200):
        edges.append((i, i + 1, ext(), ext()))
    while len(edges) < 400:
        u = randint(1, 200)
        v = randint(1, 200)
        if u == v:
            continue
        edges.append((u, v, ext(), ext()))
    write_case(10, 200, edges, 1, 200)


if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
        print(f"{g.__name__} done")
