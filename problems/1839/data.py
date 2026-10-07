#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1839《【05NOIP提高组】谁拿了最多奖学金》分层测试数据生成器（cyaron，仓库惯例）
# 用法：g++ -O2 -std=c++17 std.cpp -o std && mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py、problems/5006/data.py、.ybt-import/staging/1222/data.py
#
# 题意：N 名学生，每人给 姓名/期末平均成绩/班级评议成绩/是否干部/是否西部/论文数；
#       五项奖学金条件独立判定、可叠加，计算每生奖金总数、最高者及其金额、全体总和。
#       并列最高时输出输入中**最早出现**者（题面【输出】明文规定）。
# 数据范围（题面明文，与官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1839 一致）：
#   1 <= N <= 100；姓名：1..20 个大小写英文字母（不含空格）；平均成绩/评议成绩 ∈ [0,100]；
#   干部/西部标志 ∈ {Y,N}；论文数 ∈ [0,10]。
# 限制：time 1000 ms / memory 64 MB（config.json，与官方页 1000 ms / 65536 KB 一致）。
#
# ---- 分层策略（单组输入题：一个测试点 = 一个 N + N 行学生；10 点从最小铺到顶格）----
#   点 1  边界层：n=1 单人（唯一学生只满足班级贡献奖 → 奖金恰为最小正数 850）——
#         覆盖「单人边界 + 答案为最小值」；严格保证「总有同学获奖」。
#         （纯全零输入在题面保证之外，不进正式点，见点 4 注与报告风险点 1。）
#   点 2  边界层：n=2 且**两人全字段最大值**（100/100/Y/Y/10）→ 每人 15850 并列最高，
#         输出**最早出现**者 —— 一次覆盖 n=2、全最大值、单项奖金理论上限 15850、并列裁定。
#   点 3  边界层：题面【输入样例】原样（n=4）—— 题面声明的特殊值，逐字节回归样例输出。
#   点 4  边界层：n=17 手工阈值矩阵（可逐行手算，见下方注释表）—— 五项条件的严格大于边界
#         （avg=80/81/85/86/90/91、cls=80/81、papers=0/1）、20 字符姓名、同名双行、
#         首行与倒数第二行同为 15850 并列（答案必须取首行，卡"取最后一个"的错解）、
#         含全零学生行（奖金 0，题面保证内的合法记录）。
#   点 5  小规模随机：n=5，全字段全域均匀随机（量级可手算核对）。
#   点 6  小规模随机：n=20，全字段全域均匀随机。
#   点 7  中等规模随机：n=50，全字段全域均匀随机（范围中间档）。
#   点 8  大规模随机：n=95，接近题面上限 100。
#   点 9  顶格层（规模顶格 + 双极端在列）：n=100 全域随机，且强制首行全最大值（15850）、
#         另有一行全最小值（0）—— 规模、单项奖金上限与下界同点出现。
#   点 10 顶格层（最坏结构）：n=100 **全部满分**（100/100/Y/Y/10）→ max=15850 由 100 人
#         并列（全体并列的最坏情形），sum 取到理论上限 1585000；首行 20 字符姓名、
#         末行用另一名字，答案必须取首行 —— 卡「并列取最后」「并列取字典序」类错解。
#
#   边界清单对照：n=1→点1；n=2→点2；全最小值→点1（除触发项外全字段取极小）、点4 全零行、
#   点9（全零行）；全最大值→点2、点4、点9、点10；答案为最小值→点1（850，本题最小正奖金）；
#   「答案为 0」→点4/点9 的全零学生行（学生级 0 奖金）；纯全零输入属题面保证外，不进正式点
#   （见风险点 1）；答案为 1 在本题金额口径下**不存在**（见报告）；
#   题面特殊值→点3；并列总分→点2、点4、点10。
#   固定随机种子，生成结果完全可复现。

import random
import string

from cyaron import IO  # 引入CYaRon的库

# ---------------- 题面口径的独立打分函数（仅用于生成期自检与概览打印） ----------------

def score(avg, cls, leader, west, papers):
    """按题面五项逐条独立判定、可叠加（与 std.cpp 同口径，生成期复核用）。"""
    total = 0
    if avg > 80 and papers >= 1:
        total += 8000   # 1) 院士奖学金
    if avg > 85 and cls > 80:
        total += 4000   # 2) 五四奖学金
    if avg > 90:
        total += 2000   # 3) 成绩优秀奖
    if avg > 85 and west == 'Y':
        total += 1000   # 4) 西部奖学金
    if cls > 80 and leader == 'Y':
        total += 850    # 5) 班级贡献奖
    return total


def expected(rows):
    """返回 (最早出现的最高奖金者姓名, 最高奖金, 全体总和)。"""
    totals = [score(*r[1:]) for r in rows]
    best_i = 0
    for i in range(1, len(totals)):
        if totals[i] > totals[best_i]:  # 严格 > ⇒ 并列取最早出现者
            best_i = i
    return rows[best_i][0], totals[best_i], sum(totals)


# ---------------- 姓名与随机学生 ----------------

def rand_name(rng, lo=1, hi=20):
    return ''.join(rng.choice(string.ascii_letters) for _ in range(rng.randint(lo, hi)))


def rand_row(rng):
    return (rand_name(rng), rng.randint(0, 100), rng.randint(0, 100),
            rng.choice('YN'), rng.choice('YN'), rng.randint(0, 10))


# ---------------- 各测试点固定构造 ----------------

# 点 1：n=1 单人边界。唯一学生取「最小正奖金」形态：avg=80（严格大于边界之外）、
#   papers=0（不给院士）、非西部；只有 cls=81>80 且是干部 → 只拿班级贡献奖 850。
#   **题面保证「总有同学能满足获得奖学金的条件」在该点成立**（该生获奖）；
#   「输入全零（无任何获奖者）」属题面保证之外，不进正式点，仅在 work/stress.py D 段作探针
#   （实测会击穿两家网络 AC 实现：见 gen-report.md 风险点 1）。
P1 = [("SoloMinAward", 80, 81, 'Y', 'N', 0)]

# 点 2：n=2 两人全字段最大值 → 并列最高，取最早
P2 = [("MaxFirst", 100, 100, 'Y', 'Y', 10),
      ("MaxSecond", 100, 100, 'Y', 'Y', 10)]

# 点 3：题面【输入样例】原样
P3 = [("YaoLin", 87, 82, 'Y', 'N', 0),
      ("ChenRuiyi", 88, 78, 'N', 'Y', 1),
      ("LiXin", 92, 88, 'N', 'N', 0),
      ("ZhangQin", 83, 87, 'Y', 'N', 1)]

# 点 4：阈值矩阵（n=16）。每行逐条手算（std 口径）：
#   #1  A   80 90 Y Y 10 -> 850                （avg=80 不给院士，80→85 各级严格大于都不触发，只给贡献 850）
#   #2  B   81 80 Y Y  1 -> 8000               （81>80 且 papers=1 给院士 8000；cls=80 不给贡献）
#   #3  C   85 81 N N  0 -> 0                  （avg=85 不给五四/西部；papers=0 不给院士；非干部不给贡献）
#   #4  D   86 81 N Y  0 -> 5000               （五四 4000 + 西部 1000）
#   #5  E   90 80 N N  0 -> 0                  （avg=90 不给优秀奖，严格大于边界）
#   #6  F   91  0 Y Y  0 -> 3000               （优秀 2000 + 西部 1000；cls=0 不给贡献）
#   #7  G  100 100 Y Y 10 -> 15850             ← 最高分持有者（最早）= 答案；五项全得
#   #8  H   85 100 Y N  1 -> 8850              （院士 8000 + 贡献 850；avg=85 不给五四/西部）
#   #9  I   81 81 N Y  1 -> 8000               （仅院士）
#   #10 J   86 85 Y N  0 -> 4850               （五四 4000 + 贡献 850）
#   #11 K   91 81 N Y  0 -> 7000               （五四 4000 + 优秀 2000 + 西部 1000）
#   #12 L   91 81 Y N  0 -> 6850               （五四 4000 + 优秀 2000 + 贡献 850）
#   #13 M   80 81 Y N  0 -> 850                （仅贡献）
#   #14 20 字符姓名 81 80 N N 1 -> 8000        （姓名长度上界）
#   #15 G  100 100 Y Y 10 -> 15850             （与 #7 同名同分并列）
#   #16 LastTie 100 100 Y Y 10 -> 15850        （倒数第二行同分并列：必须仍输出首行 G）
#   #17 ZeroRow 0 0 N N 0 -> 0                 （全零学生记录：五条件全不满足）
#   期望输出：G / 15850 / 108800（ZeroRow 加 0，总和不变）
P4 = [
    ("A", 80, 90, 'Y', 'Y', 10),
    ("B", 81, 80, 'Y', 'Y', 1),
    ("C", 85, 81, 'N', 'N', 0),
    ("D", 86, 81, 'N', 'Y', 0),
    ("E", 90, 80, 'N', 'N', 0),
    ("F", 91, 0, 'Y', 'Y', 0),
    ("G", 100, 100, 'Y', 'Y', 10),
    ("H", 85, 100, 'Y', 'N', 1),
    ("I", 81, 81, 'N', 'Y', 1),
    ("J", 86, 85, 'Y', 'N', 0),
    ("K", 91, 81, 'N', 'Y', 0),
    ("L", 91, 81, 'Y', 'N', 0),
    ("M", 80, 81, 'Y', 'N', 0),
    ("AbcdefghijKlmnopqrst", 81, 80, 'N', 'N', 1),
    ("G", 100, 100, 'Y', 'Y', 10),
    ("LastTie", 100, 100, 'Y', 'Y', 10),
    ("ZeroRow", 0, 0, 'N', 'N', 0),   # 学生级「全零」记录：五条件全不满足 → 奖金 0
]

# 点 5/6/7/8：小 / 小 / 中等 / 大规模随机（固定种子，全域均匀）
def rand_rows(seed, n):
    rng = random.Random(seed)
    return [rand_row(rng) for _ in range(n)]

P5 = rand_rows(183905, 5)
P6 = rand_rows(183906, 20)
P7 = rand_rows(183907, 50)
P8 = rand_rows(183908, 95)

# 点 9：n=100 全域随机 + 首行全最大值 + 第 2 行全最小值（双极端在列）
_r9 = random.Random(183909)
P9 = [("FullMaxTop", 100, 100, 'Y', 'Y', 10),
      ("ZeroFloor", 0, 0, 'N', 'N', 0)] + [rand_row(_r9) for _ in range(98)]

# 点 10：n=100 全部满分（全体并列最坏），首行 20 字符名、末行异名、另有同名对
_r10 = random.Random(183910)
P10 = [("AbcdefghijKlmnopqrst", 100, 100, 'Y', 'Y', 10),
       ("SameNameX", 100, 100, 'Y', 'Y', 10)]
P10 += [("SameNameX" if i == 0 else rand_name(_r10), 100, 100, 'Y', 'Y', 10) for i in range(97)]
P10 += [("ZzzLastStudent", 100, 100, 'Y', 'Y', 10)]

CASES = [
    (1, P1, "边界层：n=1 单人，唯一学生只满足班级贡献奖（奖金 850 = 最小正奖金）"),
    (2, P2, "边界层：n=2 两人全最大值 → 15850 并列，输出最早出现者（全最大 + 并列裁定）"),
    (3, P3, "边界层：题面【输入样例】原样（题面声明的特殊值，逐字节回归）"),
    (4, P4, "边界层：n=17 阈值矩阵（严格大于边界）+ 20 字符姓名 + 同名行 + 首行与倒二行 15850 并列 + 全零行"),
    (5, P5, "小规模随机：n=5，全字段全域均匀"),
    (6, P6, "小规模随机：n=20，全字段全域均匀"),
    (7, P7, "中等规模随机：n=50，全字段全域均匀"),
    (8, P8, "大规模随机：n=95，接近上限 100"),
    (9, P9, "顶格层：n=100 全域随机 + 首行全最大 + 第 2 行全最小（规模顶格、双极端在列）"),
    (10, P10, "顶格层：n=100 全部满分（100 人并列最坏结构，sum=1585000 理论上限）"),
]

# ---------------- 生成前自检 ----------------
assert len(CASES) == 10, "必须恰好 10 个测试点"

# 自检 1：规模与字段范围全部落在题面声明之内（点 1/2/3/4 为构造点，同样逐一检查）
for idx, rows, _note in CASES:
    assert 1 <= len(rows) <= 100, "点 %d 的 N=%d 超出题面 1<=N<=100" % (idx, len(rows))
    for name, avg, cls, leader, west, papers in rows:
        assert 1 <= len(name) <= 20 and name.isalpha() and name.isascii(), \
            "点 %d 姓名不合规: %r" % (idx, name)
        assert 0 <= avg <= 100 and 0 <= cls <= 100, "点 %d 成绩越界" % idx
        assert leader in ('Y', 'N') and west in ('Y', 'N'), "点 %d 标志非 Y/N" % idx
        assert 0 <= papers <= 10, "点 %d 论文数越界" % idx

# 自检 2：各构造点的关键结构断言（防生成器被改坏）
assert expected(P1) == ("SoloMinAward", 850, 850), "点 1 最小正奖金 850"
assert expected(P2) == ("MaxFirst", 15850, 31700)
assert expected(P3) == ("ChenRuiyi", 9000, 28700), "点 3 必须与题面样例一致"
assert len(P4[13][0]) == 20, "点 4 需含 20 字符姓名的行"
assert expected(P4) == ("G", 15850, 108800), "点 4 阈值矩阵期望 %r" % (expected(P4),)
assert expected(P9)[1] == 15850, "点 9 首行全最大应为单项上限"
assert expected(P10) == ("AbcdefghijKlmnopqrst", 15850, 1585000), "点 10 全体并列最坏"

print("各点 N:", " ".join(str(len(rows)) for _, rows, _ in CASES))
print("各点 max/sum:", " ".join("%d/%d" % (expected(rows)[1], expected(rows)[2])
                              for _, rows, _ in CASES))

# ---------------- 生成 + 逐点打印 ----------------
for idx, rows, note in CASES:
    io = IO(file_prefix="problem", data_id=idx)  # problem{idx}.in / problem{idx}.out
    io.input_writeln(len(rows))                  # 第一行：学生总数 N
    for name, avg, cls, leader, west, papers in rows:
        io.input_writeln(name, avg, cls, leader, west, papers)  # 每人一行，空格分隔
    io.output_gen("../std")                      # .out 由 std 生成
    best_name, best_total, total_sum = expected(rows)
    print("problem%-2d: N=%-3d 期望: %s / %d / %d  -- %s"
          % (idx, len(rows), best_name, best_total, total_sum, note))
