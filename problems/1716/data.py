#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1716《次短路计数》数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py     （std 二进制位于 ../std）
#
# 题面数据范围：T 组数据；每组 2<=n<=1000，1<=m<=10000，1<=x,y,s,t<=n，x!=y，
#   1<=w<=1000，s!=t，保证至少一条 s->t 路线；输出保证所有数据 <= 1e9。
# 本题与 POJ 3463 Sightseeing 同题（样例逐字一致）。
#
# 分层设计（10 组，从边界到顶格；本题有输入，全部造满 10 组）：
#   点 1   边界层：题面样例（T=2，含平行边 5->2 7 触发答案 2）
#   点 2   边界层：n=2 / m=1 最小值，w=1000 最大值，平行边同权与差权
#   点 3   边界层：手算构造，覆盖「次短路 = 最短路 + 1」与「不存在次短路」两种分支
#   点 4   规模层：n=10（小），随机 DAG + 小分层多解构造（答案 99）
#   点 5   规模层：n=50（小），随机 DAG + 分层 + 平行链构造（答案 256 / 6）
#   点 6   规模层：n=300，m=3000（中），随机 + 分层跨层边（答案 18）
#   点 7   规模层：n=600，m=6000（中大），随机 + 含环图 + 分层
#   点 8   规模层：n=1000、m=10000（顶格 n/m），随机 W∈[1,1000]、含环、分层
#   点 9   规模层：n=1000、m=10000 顶格 + 小权 W∈{1,2} 多解 + 大答案构造
#          （答案 430467210 = 3^18 + 3^16，覆盖“次短路 = 最短路+1”有解分支）
#   点 10  顶格层：n=1000、m=10000、T=10，首组分层构造 2^14*3^10 = 967458816（贴近 1e9）

import random

from cyaron import IO

MAXN = 1000
MAXM = 10000
MAXW = 1000
MAXANS = 10 ** 9


def rand_case(seed, n, m, wmax, permute=True, back=0):
    """随机 DAG（链式边 1-2-...-n 保证 s->t 可达）；back>0 时额外加 back 条
    “反向/跨层”边（可能形成环），用于覆盖有环图的 Dijkstra 行为。

    注：由于 1<=w 且无自环，任何长度 <= 最短路+1 的 s->t 行走必为简单路径，
    故有环与无环情形下“路线计数”语义一致（有环不影响答案定义）。

    返回 (n, m, edges, s, t)：edges 为 [(x, y, w), ...]，顺序已打乱。
    """
    rnd = random.Random(seed)
    if permute:
        lab = list(range(1, n + 1))
        rnd.shuffle(lab)
    else:
        lab = list(range(1, n + 1))
    edges = []
    for i in range(1, n):
        edges.append((lab[i - 1], lab[i], rnd.randint(1, wmax)))
    target = m - back
    while len(edges) < target:
        u = rnd.randint(1, n - 1)
        v = rnd.randint(u + 1, n)
        edges.append((lab[u - 1], lab[v - 1], rnd.randint(1, wmax)))
    for _ in range(back):
        u = rnd.randint(1, n)
        v = rnd.randint(1, n)
        while v == u:
            v = rnd.randint(1, n)
        edges.append((lab[u - 1], lab[v - 1], rnd.randint(1, wmax)))
    rnd.shuffle(edges)
    s_pos = rnd.randint(1, n - 1)
    t_pos = rnd.randint(s_pos + 1, n)
    return n, len(edges), edges, lab[s_pos - 1], lab[t_pos - 1]


def cases_to_text(cases):
    """cases: [(n, m, edges, s, t), ...] -> 完整输入文本。"""
    out = ["%d" % len(cases)]
    for n, m, edges, s, t in cases:
        out.append("%d %d" % (n, m))
        for x, y, w in edges:
            out.append("%d %d %d" % (x, y, w))
        out.append("%d %d" % (s, t))
    return "\n".join(out) + "\n"


def write(idx, text):
    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(text)
    io.output_gen("../std")


# ---------------- 点 1：题面样例（边界层） ----------------
def gen1():
    text = """2
5 8
1 2 3
1 3 2
1 4 5
2 3 1
2 5 3
3 4 2
3 5 4
4 5 3
1 5
5 6
2 3 1
3 2 1
3 1 10
4 5 2
5 2 7
5 2 7
4 1
"""
    write(1, text)


# ---------------- 点 2：n/m/w 上下界 + 平行边（边界层） ----------------
def gen2():
    cases = [
        # n=2、m=1 双重下界，唯一路线 -> 1
        (2, 1, [(1, 2, 1)], 1, 2),
        # w=1000 上界 + 两条同权平行边：两条都是最短路，无次短路 -> 2
        (2, 2, [(1, 2, MAXW), (1, 2, MAXW)], 1, 2),
        # 平行边差异化：999 一条（最短路）+ 1000 两条（唯一“恰好 +1”）-> 1+2=3
        (2, 3, [(1, 2, 999), (1, 2, MAXW), (1, 2, MAXW)], 1, 2),
    ]
    write(2, cases_to_text(cases))


# ---------------- 点 3：次短路分支手算构造（边界层） ----------------
def gen3():
    cases = [
        # 最短 = 10 有两条（直达 / 经 2），无更长路线 -> 次短路不存在，答案 2
        (3, 3, [(1, 2, 5), (2, 3, 5), (1, 3, 10)], 1, 3),
        # 最短 = 10 两条（直达 / 经 2），恰有 11 = 10+1 一条 -> 2+1=3
        (4, 5, [(1, 2, 4), (2, 4, 6), (1, 3, 4), (3, 4, 7), (1, 4, 10)], 1, 4),
        # 最短 = 10 两条（直达 / 经 2）；11 = 10+1 两条（经 3 / 经 4）-> 2+2=4
        (5, 7, [(1, 5, 10), (1, 2, 3), (2, 5, 7), (1, 3, 4), (3, 5, 7), (1, 4, 2), (4, 5, 9)], 1, 5),
    ]
    write(3, cases_to_text(cases))


# ---------------- 点 4：小规模随机（可手算） ----------------
def gen4():
    cases = [rand_case(1716040 + k, 10, 20, 5) for k in range(2)]
    cases.append(rand_layered(1716042, 4, 4, 3, wmax=1, skips=4))  # 小分层：等长/多 1 并列
    cases.append(rand_layered(1716043, 5, 3, 2, wmax=2, skips=3))
    write(4, cases_to_text(cases))


def parallel_chains(nodes_per_chain, k, w, seed):
    """k 条等权等长平行链 + 一条“恰好多 1 单位”的直达边。

    s=1, t=2，第 j 条链占 nodes_per_chain 个点，内部节点间及与 s/t 相连，
    共 nodes_per_chain+1 条边、链长 dist = (nodes_per_chain+1)*w，
    最短路线共 k 条（每条链一条）；
    再加边 s->t 权 dist+1（恰多 1 单位，1 条）-> 期望答案 k + 1。
    """
    s, t = 1, 2
    n = 2 + k * nodes_per_chain
    dist = (nodes_per_chain + 1) * w
    edges = []
    for j in range(k):
        base = 3 + j * nodes_per_chain
        chain = list(range(base, base + nodes_per_chain))
        prev = s
        for node in chain:
            edges.append((prev, node, w))
            prev = node
        edges.append((prev, t, w))
    edges.append((s, t, dist + 1))
    random.Random(seed).shuffle(edges)
    return (n, len(edges), edges, s, t), k + 1


def rand_layered(seed, layers, width, outdeg, wmax=1, extra=0, skips=0):
    """随机分层图：s -> L1 -> ... -> LL -> t，每点向下层连 outdeg 条边。

    分层保证每条 s->t 路线的边数 = layers+1；当 wmax=1 时所有边权相同，
    最短路计数由 outdeg/width 控制（可能出现大量并列）。
    extra: 额外随机前向边（低层->高层，保持无环）。
    skips: 额外加 skips 条“跨层边”（Li -> Li+2），权重取 2*wmax（与两条层内
           边等长，制造等长并列路线）或 2*wmax+1（制造恰好多 1 单位的路线），
           专门覆盖“次短路 = 最短路+1”分支。
    返回 (case, None)；期望答案由 work/validate.py 独立参照实现校验。
    """
    rnd = random.Random(seed)
    layers_nodes, nxt = [], 2
    for _ in range(layers):
        layers_nodes.append(list(range(nxt, nxt + width)))
        nxt += width
    t = nxt
    n = t
    s = 1
    edges = []
    seq = [s] + [v for layer in layers_nodes for v in layer] + [t]
    for i, layer in enumerate(layers_nodes + [[t]]):
        prev = [s] if i == 0 else layers_nodes[i - 1]
        nxt_layer = layer
        for u in prev:
            picks = rnd.sample(nxt_layer, min(outdeg, len(nxt_layer)))
            for v in picks:
                edges.append((u, v, rnd.randint(1, wmax)))
    for _ in range(extra):
        i = rnd.randint(0, len(seq) - 2)
        j = rnd.randint(i + 1, len(seq) - 1)
        edges.append((seq[i], seq[j], rnd.randint(1, wmax)))
    for k in range(skips):
        i = rnd.randint(0, len(layers_nodes) - 2)
        u = rnd.choice([s] + layers_nodes[i])
        v = rnd.choice(layers_nodes[i + 1])
        w = 2 * wmax if k % 2 == 0 else 2 * wmax + 1
        edges.append((u, v, w))
    rnd.shuffle(edges)
    assert n <= MAXN and len(edges) <= MAXM, (n, len(edges))
    return (n, len(edges), edges, s, t)


# ---------------- 点 5：小规模随机 + 平行链多解 ----------------
def gen5():
    cases = [rand_case(1716050 + k, 50, 250, 10) for k in range(3)]
    cases.append(rand_layered(1716053, 8, 5, 2))
    c, want = parallel_chains(4, 5, 3, 1716055)
    cases.append(c)
    print("  gen5 平行链组期望答案：%d" % want)
    write(5, cases_to_text(cases))


# ---------------- 点 6：中等规模随机 ----------------
def gen6():
    cases = [rand_case(1716060 + k, 300, 3000, 1000) for k in range(2)]
    cases.append(rand_layered(1716062, 12, 30, 3, wmax=2, extra=500, skips=200))
    write(6, cases_to_text(cases))


# ---------------- 点 7：中大规模随机 ----------------
def gen7():
    cases = [rand_case(1716070 + k, 600, 6000, 1000) for k in range(3)]
    cases.append(rand_case(1716073, 600, 6000, 1000, back=2000))  # 含环
    cases.append(rand_layered(1716074, 20, 40, 3, wmax=3, extra=1000, skips=300))
    write(7, cases_to_text(cases))


# ---------------- 点 8：n/m 顶格随机（w 1..1000） ----------------
def gen8():
    cases = [rand_case(1716080 + k, MAXN, MAXM, MAXW) for k in range(1)]
    cases.append(rand_case(1716081, MAXN, MAXM, MAXW, back=4000))  # 顶格规模含环
    cases.append(rand_layered(1716082, 40, 24, 2, wmax=5, extra=2000, skips=400))
    write(8, cases_to_text(cases))


# ---------------- 点 9：n/m 顶格 + 小权重（最短路密集）+ 分层大计数 ----------------
def layered(widths, detours=()):
    """构造分层完全二部图：s -> L1 -> ... -> Lk -> t，边权全 1。

    每条 s->t 路线恰好经过所有层，长度 = 层数 + 1（边数），
    故最短路线条数 = 各层宽度之积 P（且不存在长度 +1 的路线）。

    detours 给出若干层下标 i，表示在 layers[i] 与 layers[i+1] 之间把某一条边
    拆成 u->z->v（新增独立点 z）：经过 z 的路线恰比最短多 1 个单位，
    条数 = P / (w_i * w_{i+1})（独立于拆分位置的选择）。

    返回 (case, 期望答案)：case = (n, m, edges, s, t)，期望答案由公式独立算出。
    """
    layers, nxt = [], 2
    for w in widths:
        layers.append(list(range(nxt, nxt + w)))
        nxt += w
    t = nxt
    s = 1
    edges = []
    prev = [s]
    for layer in layers + [[t]]:
        for u in prev:
            for v in layer:
                edges.append((u, v, 1))
        prev = layer
    n = t
    prod = 1
    for w in widths:
        prod *= w
    second = 0  # 长度 = 最短+1 的路线总条数
    for i in detours:
        z = n + 1
        n += 1
        u, v = layers[i][0], layers[i + 1][0]
        edges.append((u, z, 1))
        edges.append((z, v, 1))
        second += prod // (widths[i] * widths[i + 1])
    assert n <= MAXN and len(edges) <= MAXM, (n, len(edges))
    return (n, len(edges), edges, s, t), prod + second


def gen9():
    # 顶格 n/m 随机 + 小权重（w∈{1,2}，最短路密集，重复边多）
    cases = [rand_case(1716090 + k, MAXN, MAXM, 2) for k in range(2)]
    cases.append(rand_case(1716092, MAXN, MAXM, 2, back=5000))  # 顶格小权含环
    # 顶格规模分层多解
    cases.append(rand_layered(1716093, 50, 19, 3, wmax=2, extra=1000, skips=500))
    # 分层构造：宽度 3^18 = 387420489，另加一条“恰好多 1 单位”的支路 3^16
    c, want = layered([3] * 18, detours=(0,))
    cases.append(c)
    # 分层构造：宽度 2^14 * 3^8 = 107495424，两处支路各 2^14*3^6*... = 11943936
    c, want2 = layered([2] * 14 + [3] * 8, detours=(14, 20))
    cases.append(c)
    assert want == 387420489 + 43046721, want
    assert want2 == 107495424 + 2 * 11943936, want2
    write(9, cases_to_text(cases))
    print("  gen9 分层组期望答案：%d, %d" % (want, want2))


# ---------------- 点 10：顶格层，含接近 1e9 的大答案构造 ----------------
def gen10():
    cases = []
    # 分层构造：宽度 2^14 * 3^10 = 967458816（接近 1e9，单一最短长度无 +1 路线）
    c, want = layered([2] * 14 + [3] * 10)
    cases.append(c)
    # 其余 8 组为 n=1000、m=10000 顶格随机（权重贴上限 1000）
    cases += [rand_case(1716100 + k, MAXN, MAXM, MAXW) for k in range(7)]
    cases.append(rand_case(1716107, MAXN, MAXM, MAXW, back=3000))  # 顶格含环
    # 末组：顶格规模 + 链式结构，w 全 =1000（路径权值累积达 999*1000，卡 int 弱实现）
    n = MAXN
    edges = [(i, i + 1, MAXW) for i in range(1, n)]
    rnd = random.Random(1716109)
    while len(edges) < MAXM:
        u = rnd.randint(1, n - 1)
        v = rnd.randint(u + 1, n)
        edges.append((u, v, MAXW))
    rnd.shuffle(edges)
    cases.append((n, len(edges), edges, 1, n))
    write(10, cases_to_text(cases))
    print("  gen10 分层组期望答案（首行）：%d" % want)


if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
        print("%s done" % g.__name__)
