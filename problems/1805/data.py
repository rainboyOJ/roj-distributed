#!/usr/bin/env python3
# 一本通 1805《数数》数据生成器
# 用法：g++ -O2 -std=c++17 -o std std.cpp && mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围：1<=T<=20，1<=A<=10000，1<=B<=10^16，1<=N<=10^12。
# 每行一组 A B N；输出 T 行答案。
#
# 说明：
#   * 采用「显式 subprocess 跑 std」产出 .out（不依赖 cyaron 的 output_gen），
#     并断言 .out 行数 == T 且文件非空，规避写缓冲未 flush 导致 0 字节 .out 的隐患。
#   * 本题无「无解/空输出」点，所有点均须 T 行非空输出。
#   * 生成器仅做常数级/线性循环（T<=20），无 O(n^2) 循环。
#
# 分层设计（10 组，规模由边界 -> 小 -> 中 -> 大 -> 顶格，覆盖各种答案量级）：
#   1  边界：最小输入 T=1,A=1,B=1,N=1
#   2  边界：N 顶格 1e12
#   3  边界：B 顶格 1e16
#   4  边界：A 顶格 10000
#   5  小规模随机：可手算量级
#   6  中规模随机：B 中档、N 中档
#   7  大规模随机：全范围随机 T=20
#   8  边界组合：A/B/N 各自上下限的两两/三三组合
#   9  顶格：T=20 全为 A=10000,B=1e16,N=1e12
#   10 混合极端：顶格 + 2 的幂 A + 小 N 交替
import os
import subprocess

from cyaron import randint, random

STD = "../std"


def emit(data_id, cases):
    assert 1 <= len(cases) <= 20, "T 必须满足 1<=T<=20"
    for (A, B, N) in cases:
        assert 1 <= A <= 10000, f"A out of range: {A}"
        assert 1 <= B <= 10 ** 16, f"B out of range: {B}"
        assert 1 <= N <= 10 ** 12, f"N out of range: {N}"
    inp = f"problem{data_id}.in"
    out = f"problem{data_id}.out"
    with open(inp, "w") as fo:
        fo.write(str(len(cases)) + "\n")
        for (A, B, N) in cases:
            fo.write(f"{A} {B} {N}\n")
    # 显式跑 std 产 .out
    with open(inp, "rb") as fi:
        r = subprocess.run([STD], stdin=fi, capture_output=True, timeout=60)
    assert r.returncode == 0, f"{inp}: std exit {r.returncode}: {r.stderr.decode()}"
    text = r.stdout.decode()
    lines = [l for l in text.splitlines() if l.strip() != ""]
    assert len(lines) == len(cases), f"{inp}: expect {len(cases)} lines, got {len(lines)}"
    assert os.path.getsize(inp) > 0, f"{inp} empty"
    with open(out, "w") as fo:
        fo.write(text if text.endswith("\n") else text + "\n")
    assert os.path.getsize(out) > 0, f"{out} empty"
    print(f"problem{data_id}: T={len(cases):2d}  in={os.path.getsize(inp):>8d}B  out={os.path.getsize(out):>6d}B  ok")


# ---------------- 点 1：边界（最小输入） ----------------
def gen1():
    emit(1, [(1, 1, 1)])                       # 唯一项 = 2 -> 1


# ---------------- 点 2：边界（N 顶格） ----------------
def gen2():
    emit(2, [(1, 1, 10 ** 12)])                # N=1e12 最大项数


# ---------------- 点 3：边界（B 顶格） ----------------
def gen3():
    emit(3, [(1, 10 ** 16, 1)])                # B=1e16，项=1e16+1


# ---------------- 点 4：边界（A 顶格） ----------------
def gen4():
    emit(4, [(10000, 1, 1)])                   # A=10000，项=10001


# ---------------- 点 5：小规模随机（可手算） ----------------
def gen5():
    random.seed(180505)
    cases = [(randint(1, 100), randint(1, 10000), randint(1, 100)) for _ in range(5)]
    emit(5, cases)


# ---------------- 点 6：中规模随机 ----------------
def gen6():
    random.seed(180506)
    cases = [(randint(1, 10000), randint(1, 10 ** 9), randint(1, 10 ** 6)) for _ in range(10)]
    emit(6, cases)


# ---------------- 点 7：大规模随机（全范围 T=20） ----------------
def gen7():
    random.seed(180507)
    cases = [(randint(1, 10000), randint(1, 10 ** 16), randint(1, 10 ** 12)) for _ in range(20)]
    emit(7, cases)


# ---------------- 点 8：边界组合（A/B/N 上下限组合） ----------------
def gen8():
    M = 10 ** 16
    cases = [
        (1, M, 10 ** 12),          # B,N 顶格
        (10000, 1, 10 ** 12),      # A,N 顶格
        (10000, M, 10 ** 12),      # A,B,N 全顶格
        (1, 1, 1),                 # 全下限
        (9999, M, 10 ** 12),       # 接近 A 上限
        (8192, 1, 10 ** 12),       # A 为 2 的幂
        (1, M - 1, 10 ** 12),      # B 次顶格
        (10000, M, 10000),         # A,B 顶格、N 小
    ]
    emit(8, cases)


# ---------------- 点 9：顶格（T=20 全最大） ----------------
def gen9():
    cases = [(10000, 10 ** 16, 10 ** 12)] * 20
    emit(9, cases)


# ---------------- 点 10：混合极端（顶格 + 2 的幂 A + 小 N） ----------------
def gen10():
    random.seed(180510)
    cases = []
    for i in range(20):
        if i % 3 == 0:
            cases.append((10000, 10 ** 16, 10 ** 12))          # 顶格
        elif i % 3 == 1:
            cases.append((1 << randint(1, 13), randint(1, 10 ** 16), 10 ** 12))  # A=2^k, N 顶格
        else:
            cases.append((randint(1, 10000), randint(1, 10 ** 16), randint(1, 10)))  # 小 N
    emit(10, cases)


if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    print("ALL 10 POINTS DONE")
