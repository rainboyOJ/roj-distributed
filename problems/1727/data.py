#!/usr/bin/env python3
# 一本通 1727《魔棒》数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py   （std 二进制须为 ../std）
#
# 题面数据范围（content.md）：30% 的 n<=12；100% 的 n<=500，|a[i]|<=1000。
# 单组数据：第 1 行 n hp，第 2 行 n 个整数 a[1..n]。
# 输出：最大的正整数 cd / "No upper bound." / -1。
#
# 分层设计（10 组，三型输出 -1 / 正整数 / No upper bound. 全覆盖）：
#   点 1  边界层 n=1 最小规模，开局即死 -> -1
#   点 2  边界层 n=2，a 取 |a| 上限的负值（题面特例：负伤害回血），必活且无上界
#   点 3  小规模 题面样例 n=7 hp=30（回归点，答案 2 可人工推演）
#   点 4  小规模 n=12（30% 子任务上限），a=[1]*11+[15] hp=2：首次释放与 cd 约束交互
#   点 5  中规模 n=50 随机 a∈[1,20]，hp=200 -> 中等规模数值解
#   点 6  中规模 n=250 交替构造 a=1,15,1,15,... hp=120 -> 中等规模数值解
#   点 7  大规模 n=500 随机 a∈[-1000,1000]，hp=7387 -> 数值解（恰在无上界临界之下，hp+1 即无上界）
#   点 8  大规模 n=500 构造 [1]*499+[1000]，hp=94 -> 471（单尖峰；hp+1 即无上界，卡二分边界）
#   点 9  顶格层 n=500 全 a=1000（|a| 上限），hp=492620 -> 467（大血量临界数值解）
#   点 10 顶格层 n=500 [1]*499+[1000]，hp=95 -> No upper bound.（点 8 临界的另一侧）
import os
import random
import sys

from cyaron import IO

STD = "../std"  # 相对 data/ 目录（在 data/ 下运行本脚本）

# 先硬校验 std 已编译存在：cyaron 的 output_gen 在二进制缺失时会静默产出 0 字节 .out
if not os.path.isfile(STD) or not os.access(STD, os.X_OK):
    sys.exit("[FATAL] std 二进制缺失或不可执行：%s\n"
             "        请先执行：g++ -O2 -std=c++17 std.cpp -o std" % STD)

# 记录的人工资核过的期望答案（题目输出三型：-1 / 正整数 / "No upper bound."）
EXPECTED = ["-1", "No upper bound.", "2", "10", "22",
            "28", "171", "471", "467", "No upper bound."]
# 每组 (n, hp) 供自检
EXPECTED_NH = [(1, 1), (2, 2), (7, 30), (12, 2), (50, 200),
               (250, 120), (500, 7387), (500, 94), (500, 492620), (500, 95)]


def write_case(i, n, hp, arr):
    io = IO(file_prefix="problem", data_id=i)
    io.input_write(n, hp, "\n", " ".join(map(str, arr)), "\n")
    io.output_gen(STD)


def gen1():
    # 边界层：n=1 最小规模；hp=1 受到 1 点伤害后 hp=0 -> 无论 cd 均为 -1
    write_case(1, 1, 1, [1])


def gen2():
    # 边界层：n=2；a 取 |a| 上限的负值（题面明示负伤害回血、魔杖仍积攒能量），
    # 生命只增不减且能量每次都能积攒，任意 cd 均可活 -> No upper bound.
    write_case(2, 2, 2, [-1000, -1000])


def gen3():
    # 小规模：题面样例回归（答案 2，可人工推演）
    write_case(3, 7, 30, [20, 5, 30, 4, 10, 5, 20])


def gen4():
    # 小规模：n=12 恰好 30% 子任务上限；[1]*11+[15] 与 hp=2：
    # 必须 t=1 首放（早期 1 点伤害下 hp 仅剩 1），第二次释放受 cd 约束 -> 10
    write_case(4, 12, 2, [1] * 11 + [15])


def gen5():
    # 中规模：n=50 随机 a∈[1,20]，hp=200 -> 数值解
    random.seed(11)
    write_case(5, 50, 200, [random.randint(1, 20) for _ in range(50)])


def gen6():
    # 中规模：n=250 交替构造（1 与 15 交替，能量节奏规律）-> 数值解
    write_case(6, 250, 120, [(15 if i % 2 else 1) for i in range(250)])


def gen7():
    # 大规模：n=500 随机 a∈[-1000,1000]（满值域含负伤害），hp=7387：
    # 恰在无上界临界之下（hp=7388 时输出 No upper bound.）-> 数值解
    random.seed(1727010)
    write_case(7, 500, 7387, [random.randint(-1000, 1000) for _ in range(500)])


def gen8():
    # 大规模：n=500 构造 [1]*499+[1000]（单尖峰），hp=94：
    # 恰为数值解临界（hp=95 时无上界）-> 471，专卡二分边界与整数不变量
    write_case(8, 500, 94, [1] * 499 + [1000])


def gen9():
    # 顶格层：n=500 全部 a=1000（|a| 上限），hp=492620：
    # 大血量下恰为数值解临界（hp=492621 时无上界）-> 467
    write_case(9, 500, 492620, [1000] * 500)


def gen10():
    # 顶格层：与点 8 同结构但越过临界（hp=95）-> No upper bound.，
    # 与点 1/2 合计覆盖全部三种输出形态
    write_case(10, 500, 95, [1] * 499 + [1000])


def verify():
    """生成后自检：.in/.out 成对齐全、.out 非空且恰 1 行、首行与记录值一致。"""
    for i in range(1, 11):
        nip, nop = "problem%d.in" % i, "problem%d.out" % i
        assert os.path.isfile(nip), "缺输入文件：%s" % nip
        assert os.path.isfile(nop), "缺输出文件：%s" % nop
        inp = open(nip, encoding="utf-8").read().split()
        out = open(nop, encoding="utf-8").read().strip()
        assert out, "空 .out（std 缺失或崩溃）：%s" % nop
        lines = [ln for ln in out.splitlines() if ln.strip()]
        assert len(lines) == 1, "%s 行数异常：%r" % (nop, out)
        n, hp = int(inp[0]), int(inp[1])
        assert (n, hp) == EXPECTED_NH[i - 1], "%s 头行异常：n=%d hp=%d" % (nip, n, hp)
        assert len(inp) == 2 + n, "%s 元素个数异常：%d" % (nip, len(inp) - 2)
        assert lines[0] == EXPECTED[i - 1], \
            "%s 输出 %r != 记录值 %r" % (nop, lines[0], EXPECTED[i - 1])
        print("problem%d: n=%d hp=%d ans=%s OK" % (i, n, hp, lines[0]))


if __name__ == "__main__":
    for g in (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10):
        g()
    verify()
    print("ALL 10 CASES OK")
