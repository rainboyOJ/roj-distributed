#!/usr/bin/env python3
# 一本通 2041《【例5.9】新矩阵》分层测试数据生成器（cyaron）
# 用法：mkdir -p data && cd data && python3 ../data.py
#
# 题面数据范围（content.md / 官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2041）：
#   2 <= n <= 20                     （方阵阶数，官方页「时间限制 1000 ms 内存限制 65536 KB」）
#   1 <= a[i][j] <= 99               （题面「矩阵中各正整数小于 100」：正整数且严格小于 100）
#   单组输入：只给一个 n 与一个 n×n 矩阵，无多组数据、无测试组数 T。
#
# 答案口径（std.cpp + work/brute.cpp 双路线一致，work/stress.py 2671 组对拍通过）：
#   主对角线 (i==j) 与副对角线 (i+j==n-1, 0-indexed) 上的元素 +10，其余不变；
#   n 为奇数时中心格 (n//2, n//2) 同时属于两条对角线，**只加一次 10**（样例证实：
#   n=5 中心 38 → 48 而非 58）。输出 n 行、每行 n 个数、数与数之间恰一个空格。
#
# 分层设计（10 组，n 从下限 2 铺到上限 20，值域从下界 1 铺到上界 99）：
#   点 1  边界层：n 下限 + 值下界（全 1）+ 最小输出 11
#   点 2  边界层：最小奇数 n=3（中心格重合）+ 值上界（全 99）+ 最大输出 109
#   点 3  边界层：题面官方样原本样（题面声明的特殊值 / 样例回归）
#   点 4  小规模随机：n=4、值域 [1,9]，可手算验证
#   点 5  中等规模随机：n=10、值域 [1,99]（偶数，无中心格）
#   点 6  中等规模随机：n=11、中心格取极值 1（奇数 n 的中心格定向验证）
#   点 7  大规模随机：n=18、值域 [1,99]（接近上限的偶数）
#   点 8  大规模构造：n=19、定向"最大区分度"——对角线格=1、非对角线格=99
#   点 9  顶格层：n=20（上限）、值域 [1,99] 全覆盖随机
#   点 10 顶格层：n=20（上限）、逆序阶梯结构（有序 + 行内全相等/重复值 + 20 个档位）
#
# 分层项适用性说明（题面性质决定，详见 gen-report.md「分层对照」）：
#   * 「答案为 0 或 1 的极端」不适用 —— 本题输出恒为"原矩阵 + 部分 +10"，
#     最小可能输出是 1+10=11（点 1 用到），永不存在 0/1 的答案；
#     同理「链」等图论结构、随机种子型多组数据都不适用（单组定长矩阵）。
#   * 「卡常结构」不适用 —— n ≤ 20 时最多 20×20=400 格，任何 O(n²) 写法都远低于
#     1000 ms 限制（std 实测最大点 < 1 ms），不存在可卡的常数/结构。
#     顶格层因此按"规模顶格 + 最不利输出量"设计（点 9/10 均为 n=20、400 格全输出）。
#   * 「极端权值」在本题型中即 a[i][j] 的值域两端 1 与 99：点 1（全 1）与
#     点 2 / 点 8（全 99 或大量 99）已覆盖。
from cyaron import IO, randint, random

N_MIN, N_MAX = 2, 20     # 题面 n 范围
V_MIN, V_MAX = 1, 99     # 题面「正整数小于 100」

# 题面官方样例原样（content.md【输入样例】逐字；点 3 直接使用，做样例回归）
SAMPLE_N = 5
SAMPLE_MATRIX = [
    [13, 66, 53, 89, 55],
    [11, 72, 61, 62, 46],
    [90, 10, 38, 10, 55],
    [95, 20, 43, 27, 19],
    [60, 12, 66, 16, 96],
]


def write_matrix(io, n, mat):
    """写入一组：首行 n，随后 n 行、每行 n 个数、数与数之间恰一个空格、行末换行。"""
    io.input_writeln(n)
    io.input_write("\n".join(" ".join(map(str, row)) for row in mat) + "\n")
    io.output_gen("../std")


def gen1():
    """点 1 边界层：n=2（下限），全填 1（值下界）。
    2×2 的四个格子**全部**落在两条对角线上，故输出全为 1+10=11 ——
    这是本题理论最小输出值，同时覆盖"元组最小规模"与"值域下界"两个边界。"""
    n = N_MIN
    mat = [[V_MIN] * n for _ in range(n)]
    io = IO(file_prefix="problem", data_id=1)
    write_matrix(io, n, mat)
    return n, mat


def gen2():
    """点 2 边界层：n=3（最小奇数），全填 99（值上界）。
    3×3 的中心格 (1,1) 同时在两条对角线上，是全题最容易重复加 10 的位置；
    输出中心为 99+10=109（**不是 119**），即本题最大输出值。"""
    n = 3
    mat = [[V_MAX] * n for _ in range(n)]
    io = IO(file_prefix="problem", data_id=2)
    write_matrix(io, n, mat)
    return n, mat


def gen3():
    """点 3 边界层：题面官方样原本样 —— 题面声明的特殊值，做样例回归。
    关键校验点：n=5 中心 (2,2)=38 → 48（只加一次）；副对角线 (0,4)=55 → 65、
    (4,0)=60 → 70；非对角线格全部不变（如 (0,1)=66）。"""
    io = IO(file_prefix="problem", data_id=3)
    write_matrix(io, SAMPLE_N, SAMPLE_MATRIX)
    return SAMPLE_N, SAMPLE_MATRIX


def gen4():
    """点 4 小规模随机：n=4、值域 [1,9] 小值域随机。
    4 为偶数（无中心格），规模小到可以手算/肉眼核对每一格，
    用于验证"两条对角线都加、其它格一律不动"。"""
    random.seed(204104)
    n = 4
    mat = [[randint(V_MIN, 9) for _ in range(n)] for _ in range(n)]
    io = IO(file_prefix="problem", data_id=4)
    write_matrix(io, n, mat)
    return n, mat


def gen5():
    """点 5 中等规模随机：n=10（范围中间档，偶数），值域 [1,99] 全覆盖。
    注意 n 为偶数时主副对角线**不相交**（共 2n=20 格互不重复），
    与奇数档形成对照。"""
    random.seed(204105)
    n = 10
    mat = [[randint(V_MIN, V_MAX) for _ in range(n)] for _ in range(n)]
    io = IO(file_prefix="problem", data_id=5)
    write_matrix(io, n, mat)
    return n, mat


def gen6():
    """点 6 中等规模随机：n=11（中等奇数，含中心格），值域 [1,99]，
    并把中心格强制设为值下界 1。
    这样若实现把中心格加两次，输出会是 1+20=21 而非正确的 1+10=11 ——
    在 1..99 的随机背景里，"21" 这个值极易被分辨出来（点 2 是 99 背景下的 109 vs 119，
    两点的组合让中心格双加的错误在值域两端都无处可藏）。"""
    random.seed(204106)
    n = 11
    mat = [[randint(V_MIN, V_MAX) for _ in range(n)] for _ in range(n)]
    mat[n // 2][n // 2] = V_MIN
    io = IO(file_prefix="problem", data_id=6)
    write_matrix(io, n, mat)
    return n, mat


def gen7():
    """点 7 大规模随机：n=18（接近上限的偶数），值域 [1,99] 全覆盖。
    规模档：n=18 时有 324 格、对角线 36 格；偶数 n 无中心重合，
    与点 9（n=20）共同构成大规模随机对照。"""
    random.seed(204107)
    n = 18
    mat = [[randint(V_MIN, V_MAX) for _ in range(n)] for _ in range(n)]
    io = IO(file_prefix="problem", data_id=7)
    write_matrix(io, n, mat)
    return n, mat


def gen8():
    """点 8 大规模构造：n=19（接近上限的奇数），定向"最大区分度"结构 ——
    两条对角线上的 2n-1=37 个格子全填 1（值下界），其余 324 格全填 99（值上界）。
    正确输出：对角线格 11、非对角线格 99。
    这是对"哪些格该加"的最强单点体检：漏加一格 ⇒ 该处出现 1（应 11）；
    多加一格 ⇒ 该处出现 109（应 99）；中心格双加 ⇒ 出现 21（应 11）。
    三种典型错误在该结构下都会留下刺眼的离群值。"""
    n = 19
    mat = [[V_MAX] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = V_MIN                    # 主对角线
        mat[i][n - 1 - i] = V_MIN            # 副对角线（中心格被写两次，值仍为 1）
    io = IO(file_prefix="problem", data_id=8)
    write_matrix(io, n, mat)
    return n, mat


def gen9():
    """点 9 顶格层：n=20（题面上限）、值域 [1,99] 全覆盖随机。
    400 格全部输出，是本题输入/输出体量的顶格形态（本题无"卡常"可言，
    最不利结构即最大规模）。"""
    random.seed(204109)
    n = N_MAX
    mat = [[randint(V_MIN, V_MAX) for _ in range(n)] for _ in range(n)]
    io = IO(file_prefix="problem", data_id=9)
    write_matrix(io, n, mat)
    return n, mat


def gen10():
    """点 10 顶格层：n=20（上限）+ 逆序阶梯结构 ——
    第 i 行（0-indexed）整行填 99-4i，即 99,95,91,...,23（20 个档位，全部落在 [1,99] 内）。
    这一结构同时提供：行内全相等（重复值）、行间严格递减（有序/逆序）、
    20 个互不相同的档位（覆盖值域两端及中间），且首行全 99 使对角线上出现本题最大
    输出值 99+10=109 —— 规模顶格 + 极端权值 + 有序/重复结构一次覆盖。"""
    n = N_MAX
    mat = [[V_MAX - 4 * i] * n for i in range(n)]
    io = IO(file_prefix="problem", data_id=10)
    write_matrix(io, n, mat)
    return n, mat


GENERATORS = (gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8, gen9, gen10)

if __name__ == "__main__":
    for g in GENERATORS:
        n, mat = g()
        print(f"{g.__name__} done: n={n}")
