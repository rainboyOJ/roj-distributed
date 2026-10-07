#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1754《栈的维护》 分层测试数据生成器
# 用法：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
#
# 题意：m 个操作（k=0 压入 v；k=1 从栈顶弹出 v 个，不足则清空），随后 q 次单点修改
#       某个操作的两个参数，每次修改后输出依次执行全部操作后栈中剩余元素之和。
# 数据范围（题面明文）：m, q <= 2*10^5，v <= 10^4。
#
# ---- 分层策略（10 组）----
#   点 1  边界层：m=q=1，最小规模（单操作 + 单次修改），答案为单元素和。
#   点 2  边界层：m=2, q=2，压入/弹出切换的最小组合（含“弹空栈”分支）。
#   点 3  小规模随机：m=q=10，v∈[1,10]（可手算核对）。
#   点 4  小规模随机：m=q=1000（30% 子任务上限），v∈[1,1000]。
#   点 5  特殊性质层：m=q=1000，所有 k=1 的 v 取题面上限 1e4，
#         且栈规模始终 <= m=1000 < 1e4 ⇒ 每个弹出都清空栈（20% 子任务性质）。
#   点 6  中等规模随机：m=q=50000。
#   点 7  大规模随机：m=q=100000。
#   点 8  顶格层：m=q=200000 全随机（k,v 均随机，v∈[1,1e4]）。
#   点 9  顶格层（大和）：m=q=200000，前 m-200 个操作全部压入 v=1e4，
#         后 200 个弹出 v=1 ⇒ 剩余和接近 2e9（sum 上限、long long 边界）。
#   点 10 顶格层（清空极端）：m=q=200000，所有操作均为弹出 v=1e4 ⇒ 栈恒空，答案恒 0。
#
#   关于 .out：本脚本**不用** cyaron 的 output_gen（其写缓冲不 flush 会产出 0 字节文件），
#   而是用 subprocess 显式运行 std 产出 .out，并断言 .out 行数 == q（q>=1，输出非空）、
#   每行均为整数。
import os
import random
import subprocess

from cyaron import IO

HERE = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(HERE, "std")
VMAX = 10000  # 题面上限 v <= 1e4


def rand_ops_mods(m, q, seed, p_push, vpush, vpop):
    """生成 m 个操作 + q 次修改。
    p_push：操作为压入的概率；压入值 v∈vpush；弹出值 v∈vpop。c∈[1,m]。"""
    rnd = random.Random(seed)

    def one():
        if rnd.random() < p_push:
            return (0, rnd.randint(*vpush))
        return (1, rnd.randint(*vpop))

    ops = [one() for _ in range(m)]
    mods = []
    for _ in range(q):
        c = rnd.randint(1, m)
        k, v = one()
        mods.append((c, k, v))
    return ops, mods


def emit(idx, m, ops, mods, note):
    assert len(ops) == m, "point %d: ops 数不符" % idx
    assert len(mods) >= 1, "point %d: 至少一次修改" % idx
    for k, v in ops:
        assert k in (0, 1) and 1 <= v <= VMAX, "point %d: 操作越界 (%d,%d)" % (idx, k, v)
    for c, k, v in mods:
        assert 1 <= c <= m and k in (0, 1) and 1 <= v <= VMAX, \
            "point %d: 修改越界 (%d,%d,%d)" % (idx, c, k, v)

    lines = ["%d %d" % (m, len(mods))]
    lines += ["%d %d" % (k, v) for (k, v) in ops]
    lines += ["%d %d %d" % (c, k, v) for (c, k, v) in mods]
    content = "\n".join(lines) + "\n"

    io = IO(file_prefix="problem", data_id=idx)
    io.input_write(content)
    io.close()

    inpath = "problem%d.in" % idx
    outpath = "problem%d.out" % idx
    with open(inpath) as fin, open(outpath, "w") as fout:
        subprocess.run([STD], stdin=fin, stdout=fout, check=True)

    with open(outpath) as f:
        out = f.read()
    outlines = out.split("\n")
    if outlines and outlines[-1] == "":
        outlines.pop()
    assert len(outlines) == len(mods), \
        "point %d: .out 行数 %d != q=%d" % (idx, len(outlines), len(mods))
    assert len(outlines) > 0, "point %d: .out 为空" % idx
    for x in outlines:
        int(x)  # 每行必须为整数

    print("problem%-2d: m=%-6d q=%-6d  %s" % (idx, m, len(mods), note))


def main():
    assert os.path.exists(STD), "未找到 std，请先编译：g++ -O2 -std=c++17 std.cpp -o std"

    # 点 1：边界 —— m=q=1
    emit(1, 1, [(0, 5)], [(1, 0, VMAX)],
         "边界层：m=q=1，单操作 + 单次修改，答案 = 单元素和")

    # 点 2：边界 —— m=2, q=2，压入/弹出切换（含弹空栈）
    emit(2, 2, [(0, 3), (0, 4)], [(1, 1, 1), (2, 0, VMAX)],
         "边界层：m=2,q=2，压入/弹出切换的最小组合（含弹空栈分支）")

    # 点 3：小规模随机（压入为主 + 小弹出，答案有区分度）
    ops, mods = rand_ops_mods(10, 10, seed=175403, p_push=0.7,
                              vpush=(1, 5), vpop=(1, 3))
    emit(3, 10, ops, mods, "小规模随机：m=q=10，压入值∈[1,5]、弹出∈[1,3]（可手算核对）")

    # 点 4：30% 子任务上限
    ops, mods = rand_ops_mods(1000, 1000, seed=175404, p_push=0.65,
                              vpush=(1, 1000), vpop=(1, 2))
    emit(4, 1000, ops, mods, "小规模随机：m=q=1000（30% 子任务上限），压入∈[1,1000]、弹出∈[1,2]")

    # 点 5：20% 子任务性质 —— 每个弹出都清空栈
    rnd = random.Random(175405)
    m = q = 1000
    ops = []
    for i in range(m):
        if i % 2 == 0:
            ops.append((0, rnd.randint(1, 100)))   # 压入小值
        else:
            ops.append((1, VMAX))                  # 弹出，v=1e4 >= 栈规模(<=1000) ⇒ 清空
    mods = []
    for _ in range(q):
        c = rnd.randint(1, m)
        if rnd.random() < 0.5:
            mods.append((c, 0, rnd.randint(1, 100)))
        else:
            mods.append((c, 1, VMAX))              # 修改后仍保持“弹出必清空”
    emit(5, m, ops, mods,
         "特殊性质层：m=q=1000，所有弹出 v=1e4 且栈规模<=1000 ⇒ 每次弹出清空栈")

    # 点 6：中等规模随机
    ops, mods = rand_ops_mods(50000, 50000, seed=175406, p_push=0.7,
                              vpush=(1, VMAX), vpop=(1, 3))
    emit(6, 50000, ops, mods, "中等规模随机：m=q=50000，压入∈[1,1e4]、弹出∈[1,3]")

    # 点 7：大规模随机
    ops, mods = rand_ops_mods(100000, 100000, seed=175407, p_push=0.7,
                              vpush=(1, VMAX), vpop=(1, 3))
    emit(7, 100000, ops, mods, "大规模随机：m=q=100000，压入∈[1,1e4]、弹出∈[1,3]")

    # 点 8：顶格全随机（压入略占优，栈非空、答案有区分度）
    ops, mods = rand_ops_mods(200000, 200000, seed=175408, p_push=0.7,
                              vpush=(1, VMAX), vpop=(1, 3))
    emit(8, 200000, ops, mods, "顶格层：m=q=200000 全随机（压入∈[1,1e4]、弹出∈[1,3]）")

    # 点 9：顶格大和（接近 sum 上限 2e9）
    rnd = random.Random(175409)
    m = q = 200000
    ops = [(0, VMAX)] * (m - 200) + [(1, 1)] * 200
    mods = []
    for _ in range(q):
        c = rnd.randint(1, m)
        k = 0 if rnd.random() < 0.7 else 1
        v = VMAX if k == 0 else rnd.randint(1, 3)
        mods.append((c, k, v))
    emit(9, m, ops, mods,
         "顶格层（大和）：m=q=200000，前 m-200 全压入 1e4、后 200 弹出 1，剩余和接近 2e9")

    # 点 10：顶格清空极端
    rnd = random.Random(175410)
    m = q = 200000
    ops = [(1, VMAX)] * m
    mods = [(rnd.randint(1, m), 1, VMAX) for _ in range(q)]
    emit(10, m, ops, mods,
         "顶格层（清空极端）：m=q=200000，所有操作均弹出 v=1e4 ⇒ 栈恒空，答案恒 0")


if __name__ == "__main__":
    main()
