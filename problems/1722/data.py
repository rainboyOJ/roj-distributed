#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 一本通 1722《骑士游戏》数据生成器（cyaron，分层 10 组）
#
# 输入格式（单组测试，无 T）：
#   第 1 行：N
#   随后 N 行：第 i 行 = S_i K_i R_i v_1 ... v_{R_i}
#     S_i = 普通攻击体力，K_i = 法术攻击体力，R_i = 死后产生的新怪兽数，
#     v_j = 新怪兽编号（1..N，可重复，同一编号可出现多个）
#
# 数据范围（题面【提示】）：2 <= N <= 2e5，1 <= R_i 且 ΣR_i <= 1e6，1 <= S_i, K_i <= 5e14
#
# 分层策略（10 组，单调递增 + 边界/顶格）：
#   1  边界最小：N=2 二元环，S=K=1                       -> 手算 1
#   2  边界自环 + 权值顶格：1 号自环，S=K=5e14           -> 手算 5e14
#   3  小：N=100 随机图，K 全取最小 1                    -> 手算 1
#   4  小：N=2000 随机图，S,K ∈ [1,1e9]
#   5  中：N=5e4 随机图，R∈[1,20]，S,K 全取顶格 5e14     -> 手算 5e14
#   6  大：N=2e5 随机映射（R≡1），S,K ∈ [1,5e14]
#   7  大：N=2e5，R∈[1,3] 随机（ΣR≈4e5），S,K ∈ [1,5e14]
#   8  顶格：N=2e5，R≡5  ->  ΣR=1e6 精确顶格，S,K ∈ [1,5e14]
#   9  顶格：单点巨扇出（R_1=800001，其余 1）-> ΣR=1e6 精确，手算 800002
#  10  顶格：长链累加（N=2e5 链 + 末端自环，S=2.4e9）-> 手算 4.79997600001e14
#
# 运行：cd <本目录> && g++ -O2 -std=c++17 std.cpp -o std && python3 data.py
#      （data.py 自动定位自身的 data/ 目录与 std，输出落到 <本目录>/data/）
#      全量重跑约 1.7 s（生成 + 读回自检 + 闭式公式自检）；固定种子，可精确复现。
#
# 说明：生成器只用 numpy 向量化随机 + 一次 str.join 拼串，无 O(n^2) 循环；
#       生成后对每个点做**格式/范围自检**，并对 1/2/3/5/9/10 六个结构确定的点
#       用闭式公式校验 std 的输出（不涉及任何暴力/对拍）。

import os
import sys

import numpy as np
from cyaron import IO

MAXN = 200000
MAXSR = 1000000
MAXV = 500000000000000  # 5e14，题面 S_i / K_i 上限

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)
os.chdir(DATA_DIR)  # cyaron 的 .in/.out 落在 cwd，此处固定为 <本目录>/data

_pts = []          # (id, N, sumR, note)
_formula = {}      # id -> (期望答案, 公式说明)


def _j(arr):
    return " ".join(map(str, arr))


def build_input(N, R, S, K, children):
    """拼出完整输入文本。children[i] 为长度为 R[i] 的编号数组。"""
    parts = [str(N)]
    ap = parts.append
    for i in range(N):
        ap("%d %d %d %s" % (S[i], K[i], R[i], _j(children[i])))
    ap("")
    return "\n".join(parts)


def gen(data_id, N, R, S, K, children, note):
    # ---- 逐点断言：严格贴题面范围 ----
    assert 2 <= N <= MAXN, "N 越界：%d" % N
    assert len(R) == len(S) == len(K) == len(children) == N, "长度不一致"
    tot = 0
    for i in range(N):
        ri = int(R[i])
        assert 1 <= ri, "R_%d < 1" % (i + 1)
        assert len(children[i]) == ri, "R_%d 与子节点个数不符" % (i + 1)
        assert 1 <= int(S[i]) <= MAXV and 1 <= int(K[i]) <= MAXV, "权值越界 @%d" % (i + 1)
        tot += ri
    assert tot <= MAXSR, "ΣR=%d 超过 1e6" % tot

    buf = build_input(N, R, S, K, children)
    io = IO(file_prefix="problem", data_id=data_id)
    io.input_write(buf)
    io.output_gen(os.path.join(HERE, "std"))
    io.close()  # 冲刷并关闭 .in/.out，确保下面读回校验看到落盘内容
    _pts.append((data_id, N, tot, note))

    # ---- 格式自检：读回 .in，逐字段核对 ----
    path = os.path.join(DATA_DIR, "problem%d.in" % data_id)
    with open(path, "r") as f:
        tok = f.read().split()
    p = 0
    n2 = int(tok[p]); p += 1
    assert n2 == N, "problem%d: 读回 N=%d != %d" % (data_id, n2, N)
    sr = 0
    for i in range(N):
        si = int(tok[p]); ki = int(tok[p + 1]); ri = int(tok[p + 2]); p += 3
        assert (si, ki, ri) == (int(S[i]), int(K[i]), int(R[i])), "problem%d: 行 %d 头三数不符" % (data_id, i + 1)
        got = list(map(int, tok[p:p + ri])); p += ri
        assert got == list(map(int, children[i])), "problem%d: 行 %d 子节点不符" % (data_id, i + 1)
        sr += ri
    assert p == len(tok), "problem%d: 末尾有残留 token" % data_id
    assert sr == tot, "problem%d: ΣR 不符" % data_id

    # ---- 闭式公式自检（仅结构确定的点）----
    if data_id in _formula:
        exp, why = _formula[data_id]
        with open(os.path.join(DATA_DIR, "problem%d.out" % data_id), "r") as f:
            got = f.read().strip()
        assert got == str(exp), "problem%d: std 输出 %s != 闭式期望 %s（%s）" % (data_id, got, exp, why)
        print("  [公式自检] problem%d: %s = %s  ✔（%s）" % (data_id, got, exp, why))


# ---------------------------------------------------------------- 1. 边界最小
R = [1, 1]
S = [1, 1]
K = [1, 1]
ch = [np.array([2]), np.array([1])]
_formula[1] = (1, "N=2 二元环 1->2->1，S=K=1：f2=min(1,1+f1)=1，f1=min(1,1+f2)=1")
gen(1, 2, R, S, K, ch, "边界最小：N=2、R≡1、S=K=1 的二元环（题面全部下界）")

# ------------------------------------------------- 2. 边界自环 + 权值读满上限
R = [1, 1]
S = [MAXV, 1]
K = [MAXV, 1]
ch = [np.array([1]), np.array([1])]
_formula[2] = (MAXV, "1 号自环 S=K=5e14：f1=min(5e14, 5e14+f1)=5e14（普通攻击永不收敛，只能法术）")
gen(2, 2, R, S, K, ch, "边界：1 号怪兽自环（R_1=1 指向自己）+ S,K 双顶格 5e14")

# ------------------------------------------------------------- 3. 小：K 全最小
rng = np.random.default_rng(172203)
N = 100
R = rng.integers(1, 4, size=N).tolist()
S = rng.integers(1, 101, size=N).tolist()
K = [1] * N
_flat3 = rng.integers(1, N + 1, size=int(sum(R)))
_off = 0
ch = []
for r in R:
    ch.append(_flat3[_off:_off + r].tolist())
    _off += r
_formula[3] = (1, "K 全为 1（最小值）：f_i<=K_i=1 且 f_i>=1 => 恒 1")
gen(3, N, R, S, K, ch, "小规模随机：N=100，R∈[1,3]，S∈[1,100]，K≡1（答案恒为 1 的极端）")

# --------------------------------------------------------------- 4. 小：随机
rng = np.random.default_rng(172204)
N = 2000
R = rng.integers(1, 6, size=N).tolist()
S = rng.integers(1, 10 ** 9 + 1, size=N).tolist()
K = rng.integers(1, 10 ** 9 + 1, size=N).tolist()
_flat4 = rng.integers(1, N + 1, size=int(sum(R)))
_off = 0
ch = []
for r in R:
    ch.append(_flat4[_off:_off + r].tolist())
    _off += r
gen(4, N, R, S, K, ch, "小规模随机：N=2000，R∈[1,5]，S,K∈[1,1e9]")

# ------------------------------------------------- 5. 中：随机 + 权值双顶格
rng = np.random.default_rng(172205)
N = 50000
R = rng.integers(1, 21, size=N).tolist()
S = [MAXV] * N
K = [MAXV] * N
_flat5 = rng.integers(1, N + 1, size=int(sum(R)))
_off = 0
ch = []
for r in R:
    ch.append(_flat5[_off:_off + r].tolist())
    _off += r
_formula[5] = (MAXV, "S=K≡5e14：f_i=min(5e14, 5e14+Σf)>5e14 不可能更优，归纳得 f_i≡5e14")
gen(5, N, R, S, K, ch, "中规模随机：N=5e4，R∈[1,20]，S=K≡5e14（普通攻击恒不优于法术的极端）")

# --------------------------------------------- 6. 大：随机映射（R≡1 稀疏）
rng = np.random.default_rng(172206)
N = MAXN
R = [1] * N
S = rng.integers(1, MAXV + 1, size=N).tolist()
K = rng.integers(1, MAXV + 1, size=N).tolist()
_pick6 = rng.integers(1, N + 1, size=N)
ch = [[int(x)] for x in _pick6]
gen(6, N, R, S, K, ch, "大规模：N=2e5 顶格，R≡1 随机映射（ΣR=2e5，大量随机环），S,K∈[1,5e14]")

# ------------------------------------------- 7. 大：ΣR 中等（随机小出度）
rng = np.random.default_rng(172207)
N = MAXN
R = rng.integers(1, 4, size=N).tolist()
S = rng.integers(1, MAXV + 1, size=N).tolist()
K = rng.integers(1, MAXV + 1, size=N).tolist()
_flat7 = rng.integers(1, N + 1, size=int(sum(R)))
_off = 0
ch = []
for r in R:
    ch.append(_flat7[_off:_off + r].tolist())
    _off += r
gen(7, N, R, S, K, ch, "大规模：N=2e5 顶格，R∈[1,3]（ΣR≈4e5），S,K 全范围随机")

# ------------------------------------------ 8. 顶格：ΣR=1e6 精确（R≡5）
rng = np.random.default_rng(172208)
N = MAXN
R = [5] * N
S = rng.integers(1, MAXV + 1, size=N).tolist()
K = rng.integers(1, MAXV + 1, size=N).tolist()
_pick8 = rng.integers(1, N + 1, size=(N, 5))
ch = [row.tolist() for row in _pick8]
assert sum(R) == MAXSR
gen(8, N, R, S, K, ch, "顶格：N=2e5 且 ΣR=1e6 精确读满（R≡5），S,K∈[1,5e14] 全范围随机")

# ---------------------------------- 9. 顶格：单点巨扇出（R_1=800001）ΣR=1e6
N = MAXN
R = [800001] + [1] * (N - 1)
S = [1] + [1] * (N - 1)
K = [MAXV] + [1] * (N - 1)
ch = [np.full(800001, 2, dtype=np.int64)]
ch += [[i] for i in range(2, N + 1)]  # 1-based 第 i 号怪兽自环（ch[i-1] = [i]）
assert sum(R) == MAXSR
_formula[9] = (800002, "i>=2 全为 K=1 自环 => f_i=1；f1=min(5e14, 1+800001*1)=800002")
gen(9, N, R, S, K, ch, "顶格：1 号巨扇出 R_1=800001（全指向 2 号），ΣR=1e6 精确；其余 i>=2 自环 K=1")

# ------------------------------------------ 10. 顶格：长链累加（答案量级最大）
N = MAXN
R = [1] * N
CHAIN_S = 2400000000  # 2.4e9
S = [CHAIN_S] * N
K = [MAXV] * (N - 1) + [1]  # 末端 N：K_N=1 自环 => f_N=1
ch = [[i + 2] for i in range(N - 1)] + [[N]]
_exp10 = CHAIN_S * (N - 1) + 1
_formula[10] = (_exp10, "i->i+1 长链 + 末端自环 K_N=1 => f_N=1，f1=1+ΣS=2.4e9*(N-1)+1≈4.8e14（贴 5e14 上限的大答案）")
gen(10, N, R, S, K, ch, "顶格：N=2e5 长链累加（S=2.4e9，末端自环 K=1），答案 ≈4.8e14 接近 K 上限")

# ------------------------------------------------------------------ 汇总输出
print()
print("分层数据生成完毕（共 %d 个测试点，全部单组测试）：" % len(_pts))
for i, n, sr, note in _pts:
    print("  problem%-2d N=%-6d ΣR=%-7d <- %s" % (i, n, sr, note))
print("自检通过：每点均满足 2<=N<=2e5、R_i>=1、ΣR<=1e6、1<=S_i,K_i<=5e14，")
print("          输入读回逐字段核对一致；结构确定的点已用闭式公式校验 std 输出。")
