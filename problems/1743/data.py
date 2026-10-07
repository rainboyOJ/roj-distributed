#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1743《数羊》分层测试数据生成器（cyaron；仓库惯例参考 problems/1000/data.py）
#
# 用法：
#   g++ -O2 -std=c++17 std.cpp -o std
#   mkdir -p data && cd data && python3 ../data.py
#
# 题意：统计三元组 (i,j,k) 的组数，满足 i<j<k 且 a[i]<a[k]<a[j]；
#       输入保证第二行是 1..N 的排列（题面【提示】）。
# 数据范围（题面【提示】，与官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1743 一致）：
#   20%: N<=100；40%: N<=1000；60%: N<=100000；100%: N<=200000，且为 1..N 的排列。
#   限制 time 1000 ms / memory 256 MB（config.json）。
#   答案上限 C(200000,3) ≈ 1.33e15 —— 必须 64 位整数（std 用 long long）。
#
# ---- 分层策略（10 个测试点，本题单组数据，规模从最小铺到顶格） ----
#   点 1  边界层：N=1（全最小值/下界；答案恒 0 的极端）                断言 == 0
#   点 2  边界层：题面样例 N=3, "1 3 2"（题面声明的特殊值；答案 1 极端） 断言 == 1
#   点 3  边界层：N=2 逆序 [2,1]（n=2 最小非平凡规模；递减排列 -> 0）    断言 == 0
#   点 4  小规模随机（可手工核对）：N=8 随机排列                        断言 == 6
#   点 5  小规模随机：N=100（20% 档上限，含 1..100 排列）
#   点 6  中等规模随机：N=1000（40% 档上限）
#   点 7  中等偏大随机：N=10000
#   点 8  大规模随机：N=100000（60% 档上限）
#   点 9  顶格随机：N=200000（100% 上限）
#   点 10 顶格构造（近最坏答案 / 卡 32 位溢出）：
#         [1..100000] + [200000..100001]（两个等长段、前升后降结构），
#         答案有闭式 m*C(m,2)（m=N/2=100000）-> 499995000000000（≈5.0e14，
#         高出 int32 上限 5 个数量级，专测溢出）。闭式已对小 N 穷举验证。
#
# 自查（生成时断言，失败即 loud fail）：
#   A. `../std` 必须存在、是文件且可执行 —— cyaron 的 output_gen 在 std 缺失时
#      会静默产出 0 字节 .out，故先显式检查，且每点生成后再校验 .out 非空；
#   B. 每个排列都必须是 1..N 的合法排列（排序后恰为 1..N），N 不超题面上限 200000；
#   C. 定点断言：点1=0、点2=1（=题面样例）、点3=0、点4=6、点10=闭式 m*C(m,2)；
#   D. 每个 .out 存在、非空、恰好 1 行、可解析为非负整数；并回读 .in 校验
#      （首行==N，次行恰 N 个整数且与生成排列逐位一致）。
#   全部随机点用固定种子（174304..174309），数据可复现（同一 Python 版本下）。
#
# 注：按任务书铁律「不得使用暴力/对拍/stress」，本生成器不内置任何暴力对拍；
#     验证采用：定点闭式断言（A/C/D 项）+ 生成后 .out 完整性校验。

import os
import random
import sys

from cyaron import IO  # 引入CYaRon的库

MAXN = 200000  # 题面上限
STD = "../std"  # 标程可执行文件（相对 data/ 目录）


def make_perm(n, seed):
    """固定种子生成 1..n 的随机排列（Fisher-Yates 洗牌，O(n)）。"""
    rng = random.Random(seed)
    p = list(range(1, n + 1))
    rng.shuffle(p)
    return p


def two_half(n):
    """顶格构造：[1..n/2] + [n..n/2+1]，答案闭式 = m*C(m,2)。"""
    m = n // 2
    return list(range(1, m + 1)) + list(range(n, m, -1))


def build_points():
    m = MAXN // 2  # = 100000
    pts = []

    # 点 1：边界层 —— N=1（全最小值/下界），答案恒 0
    pts.append(dict(idx=1, n=1, perm=[1], expected=0,
                    note="边界层：N=1 全最小值（下界），答案 0 极端"))

    # 点 2：边界层 —— 题面样例（特殊值），答案 1 极端
    pts.append(dict(idx=2, n=3, perm=[1, 3, 2], expected=1,
                    note="边界层：题面样例 N=3 1 3 2（题面声明特殊值），答案 1 极端"))

    # 点 3：边界层 —— N=2 逆序，2 元组无 3-triple，答案恒 0
    pts.append(dict(idx=3, n=2, perm=[2, 1], expected=0,
                    note="边界层：N=2 逆序 [2,1]（最小非平凡规模+递减序），答案 0"))

    # 点 4：小规模随机 —— N=8，可手工核对（该排列的答案 = 6）
    pts.append(dict(idx=4, n=8, perm=make_perm(8, 174304), expected=6,
                    note="小规模随机：N=8 随机排列，答案 6（可手工核对）"))

    # 点 5：小规模随机 —— N=100（20% 档上限）
    pts.append(dict(idx=5, n=100, perm=make_perm(100, 174305), expected=None,
                    note="小规模随机：N=100（20% 档上限）"))

    # 点 6：中等规模随机 —— N=1000（40% 档上限）
    pts.append(dict(idx=6, n=1000, perm=make_perm(1000, 174306), expected=None,
                    note="中等规模随机：N=1000（40% 档上限）"))

    # 点 7：中等偏大随机 —— N=10000
    pts.append(dict(idx=7, n=10000, perm=make_perm(10000, 174307), expected=None,
                    note="中等偏大随机：N=10000"))

    # 点 8：大规模随机 —— N=100000（60% 档上限）
    pts.append(dict(idx=8, n=100000, perm=make_perm(100000, 174308), expected=None,
                    note="大规模随机：N=100000（60% 档上限）"))

    # 点 9：顶格随机 —— N=200000（100% 上限）
    pts.append(dict(idx=9, n=MAXN, perm=make_perm(MAXN, 174309), expected=None,
                    note="顶格随机：N=200000（100% 上限）"))

    # 点 10：顶格构造 —— 等长两段 前升后降，答案 = m*C(m,2)（近最坏，卡 32 位）
    pts.append(dict(idx=10, n=MAXN, perm=two_half(MAXN), expected=m * m * (m - 1) // 2,
                    note="顶格构造：[1..100000]+[200000..100001]，答案闭式 m*C(m,2)=499995000000000"))

    return pts


def check_std_present():
    """铁律：output_gen 对缺失的程序会静默产出 0 字节 .out —— 生成前先查 std。"""
    assert os.path.isfile(STD), "%s 不存在：请先编译 std.cpp（g++ -O2 -std=c++17 std.cpp -o std）" % STD
    assert os.access(STD, os.X_OK), "%s 不可执行" % STD


def check_perm(n, perm):
    assert 1 <= n <= MAXN, "N=%d 超出题面上限 %d" % (n, MAXN)
    assert len(perm) == n, "排列长度 %d != N=%d" % (len(perm), n)
    assert sorted(perm) == list(range(1, n + 1)), "不是 1..N 的排列"


def read_out(idx):
    fn = "problem%d.out" % idx
    assert os.path.isfile(fn), "%s 不存在（cyaron 可能因 std 缺失而静默失败）" % fn
    raw = open(fn, "rb").read()
    assert len(raw) > 0, "%s 为 0 字节（std 未产出，检查 ../std）" % fn
    text = raw.decode("utf-8")
    lines = text.splitlines()
    assert len(lines) == 1, "%s 应恰好 1 行，实际 %d 行" % (fn, len(lines))
    assert lines[0] == lines[0].strip(), "%s 行尾有多余空白" % fn
    val = int(lines[0])  # 非整数会抛异常 -> loud fail
    assert val >= 0, "%s 答案为负：%d" % (fn, val)
    return val


def main():
    check_std_present()
    points = build_points()
    assert len(points) == 10, "必须恰好 10 个测试点"
    assert [p["idx"] for p in points] == list(range(1, 11))

    answers = {}
    for p in points:
        idx, n, perm = p["idx"], p["n"], p["perm"]
        check_perm(n, perm)

        io = IO(file_prefix="problem", data_id=idx)  # problem{idx}.in / problem{idx}.out
        io.input_write(n, "\n", " ".join(map(str, perm)), "\n")
        io.output_gen(STD, time_limit=60)  # .out 由标程生成（60s 兜底上限，远高于 1000ms 题限）
        io.close()  # 确保输入/输出文件都已 flush + close

        # 回读 .in：格式与内容必须与设计一致
        in_lines = open("problem%d.in" % idx, "r").read().splitlines()
        assert in_lines[0] == str(n), "点 %d .in 首行(%s) != N(%d)" % (idx, in_lines[0], n)
        got = list(map(int, in_lines[1].split()))
        assert got == perm, "点 %d .in 次行与生成排列不一致" % idx

        # 校验 .out：非空、恰好 1 行、可解析
        val = read_out(idx)
        answers[idx] = val

        # 定点闭式断言（生成器内置的独立校验）
        if p["expected"] is not None:
            assert val == p["expected"], \
                "点 %d 答案 %d != 期望闭合值 %d" % (idx, val, p["expected"])

        sz_in = os.path.getsize("problem%d.in" % idx)
        sz_out = os.path.getsize("problem%d.out" % idx)
        print("problem%-2d OK  N=%-6d answer=%-18d  .in=%-9d .out=%-3d bytes  %s"
              % (idx, n, val, sz_in, sz_out, p["note"]))

    # 单调性&量级粗查：大 N 的答案量级应随规模上升（随机排列下 132 数 ~ C(n,3)/6）
    assert answers[1] == 0 and answers[2] == 1 and answers[3] == 0 and answers[4] == 6, "边界/小规模断言失败"
    assert answers[5] < answers[6] < answers[7] < answers[8] < answers[9], "大规模随机答案量级未单调上升"
    assert answers[10] == 499995000000000, "点 10 闭式断言失败（应为 m*C(m,2)）"
    print("全部 10 个测试点生成完毕，自查断言全部通过。")


if __name__ == "__main__":
    main()
