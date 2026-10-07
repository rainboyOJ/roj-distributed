#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 一本通 2046《【例5.15】替换字母》分层测试数据生成器（cyaron）
# 用法（在本目录下）：
#     g++ -O2 -std=c++17 std.cpp -o std
#     mkdir -p data && cd data && python3 ../data.py
# 参考仓库惯例：problems/1000/data.py（IO(file_prefix="problem", data_id=i) + output_gen("../std")）、
#               problems/5006/data.py（无输入题只生成 1 组）、
#               .ybt-import/staging/2044/data.py、staging/2020/data.py（分层 + 生成期自检）。
#
# ---------------------------------------------------------------------------
# 题意（content.md；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2046
#       本轮实抓核对，题面五节与 content.md 逐字一致）：
#   【题目描述】模拟文档编辑中的替换操作（把“电脑”都替换成“计算机”）。
#   【输入】两行。第 1 行是原文（长度不超过 200 个字符）；第 2 行包含以空格分隔的
#           两个字符 A 和 B，要求把原文中所有的字符 A 都替换成字符 B，区分大小写。
#   【输出】一行，输出替换后的结果。
#   【输入样例】I love China. I love Beijing. / I U
#   【输出样例】U love China. U love Beijing.
#   config.json：time 1000 ms / memory 64 MB（官方页「时间限制 1000 ms
#               内存限制 65536 KB」，一致）。
#
# ---------------------------------------------------------------------------
# 数据范围与判读（与 std.cpp 头部注释一致，逐条给依据）：
#   * 规模：**第 1 行原文 ≤ 200 个字符**（题面唯一给出的定量约束）。本包按最保守读法
#     取「原始字节数 ≤ 200」——全部 8 个网络来源的字符数组都是 205 字节左右
#     （如来源 [1] `char s[205]`、[3] `char s[1000]`、[2] C 版 `#define N 210`），
#     说明其缓冲区按「≤200 字节」设计。10 个测试点全部满足（顶格点 9/10 恰 200 字节）。
#   * 字符集：原文只用**可打印 ASCII**（含空格、字母、数字、标点），不含 '\t'、'\r'、
#     不含多字节字符。依据：A、B 是 `char`（8 个来源全部用 `cin>>a>>b` 或
#     `scanf("%c %c")` 读入单个字符），若原文含多字节字符，含 `char s[205]` 的实现
#     会按字节截断/乱码 —— 这类实现全部 AC 反证官方原文是单字节可打印字符。
#   * A、B 为**非空白可见 ASCII 单字符**。依据：全部来源用 `cin>>a>>b` / `scanf` 读 A、B，
#     两种读法都会跳过空白，故官方数据里 A、B 不可能是空白字符（否则那些代码必错）。
#     本包因此不构造 A 或 B 为空格/制表符的数据（构造了也不公平：题面没要求支持）。
#   * 原文**可以含空格**：题面样例本身就含空格，且全部来源都强调「必须整行读取
#     （getline/cin.getline）才能处理原文中的空格」，点 3/6/7/10 定向覆盖
#     （行首空格、连续多空格、词间空格、与标点/数字混杂）。
#   * **不含行尾空格**（本包的设计选择，理由见 gen-report.md 风险点 1）：行尾空白是所有
#     判题器归一化策略里唯一存在分歧的构造（有的判题器按行尾忽略空白比对），
#     而它相对「行内空格」并不增加区分度（`cin>>s` 这类分词读法早已被行内空格杀掉）。
#     故本包原文（以及输出）都不以空白字符结尾；最大输出量点 9/10 亦不以空格结尾。
#   * 单组输入：一组数据就是「一行原文 + 一行 A B」，不存在组数 T，故 10 个点 = 10 组数据。
#
# ---------------------------------------------------------------------------
# 分层设计（10 个测试点；每点的规模与设计意图见下面各 genN() 的注释）：
#   点 1  ｜边界层｜最小规模：原文长度 1（题面隐含下限），唯一字符即 A ⇒ 100% 替换，
#         答案恰 1 次替换（「答案为 1」的极端）
#   点 2  ｜边界层｜长度 2 + **答案为 0 的极端**（A 不在原文中，一次替换都没有）
#         + A、B 取标点字符（非字母）
#   点 3  ｜边界层（题面声明的特殊值）｜【输入样例】原样，断言 = 【输出样例】逐字节
#   点 4  ｜小规模随机｜长度 4–12、小字符集（含数字/标点/空格），可手算核对；
#         A 从原文中取（保证确有替换）
#   点 5  ｜中等规模·临界｜长度 60 且 **A == B**（恒等替换，A 取大小写成对字母）
#         ⇒ 输出须与原文逐字节相同，同时杀大小写不敏感写法
#   点 6  ｜中等规模·临界（空白结构）｜长度恰 100：行首 2 个空格 + 词间 1–3 个连续空格，
#         非空白结尾 ⇒ 杀「按空白分词读入 / 输出时压缩空白」的写法
#   点 7  ｜大规模随机｜长度 170（行首 2 空格），混大小写 + 数字 + 标点 + 空格，接近上限
#   点 8  ｜大规模定向｜长度 190 = "Aa"×95：只替换大写 A（小写 a 保留）且**相邻密集替换**；
#         B='a' 已在原文中出现 ⇒ 杀「两趟替换 / 链式替换」写法
#   点 9  ｜顶格层｜长度上限 200 且**全相等**（200 个 'a'）⇒ 200 次替换，最坏替换密度
#   点 10 ｜顶格层｜长度上限 200 且**字符集最广**（可打印非空白 ASCII 94 个字符各两遍
#         = 188，中部插 12 个空格）⇒ 满长度 + 最大字符多样性，且大小写敏感（A='a'、B='A'）
#
# 分层项适用性说明（题面性质决定，详见 gen-report.md「分层对照」）：
#   * 「有序 / 逆序 / 链 / 卡常结构 / 极端权值」不适用：本题输入是一个字符串 + 两个字符，
#     无数组/序列/图结构，也没有数值权值；n ≤ 200 时任何 O(n) 写法都远低于 1000 ms
#     （std 实测最大点 < 1 ms），不存在可卡的常数。
#   * 「多组数据按组数分层」不适用：单组输入（无 T）。
#   * 题面声明的特殊值只有【输入样例】一个，已作为点 3 做逐字节回归。
#
# 生成期自检（本文件末尾 verify 段）：把每个 .in 回读解析 → 用**独立于 std 的 Python
#   per-char 循环**重算答案 → 与 std 生成的 .out 逐字节比对；同时校验长度上限、
#   A/B 合法性、行尾无空白、点 3 与题面【输出样例】逐字节一致。
# 随机性：每个随机点使用独立 Random(2046 + 点号)，与调用顺序无关、逐字节可复现。
# ---------------------------------------------------------------------------

from cyaron import IO  # 引入CYaRon的库

import os
import random

# 题面声明的特殊值（content.md【输入样例】/【输出样例】逐字）
SAMPLE_TEXT = "I love China. I love Beijing."
SAMPLE_A, SAMPLE_B = "I", "U"
SAMPLE_OUT = "U love China. U love Beijing."

MAX_LEN = 200  # 题面：原文长度不超过 200 个字符

# 可打印 ASCII（0x21..0x7E）；空格单独处理
PRINTABLE = "".join(chr(c) for c in range(0x21, 0x7F))

# 供随机点使用的混合字符集（大小写字母 + 数字 + 常见标点 + 空格）
MIXED = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    ".,!?;:-"
    "  "
)

# 记录 (点号, 长度, 替换次数, 设计意图)，末尾打印分层表，便于人工核对
_points = []


def expected(text, a, b):
    """题面的独立直译（逐字符，不用 str.replace）：把每个等于 a 的字符改成 b。"""
    return "".join(b if ch == a else ch for ch in text)


def emit(i, text, a, b, note, assert_out=None):
    """写出第 i 组数据（原文 + 'A B'），用 std 生成 .out，并记录元信息。"""
    assert len(text) <= MAX_LEN, "第 %d 组原文超长：%d" % (i, len(text))
    assert a != "" and b != "" and len(a) == 1 and len(b) == 1, "A/B 必须是单字符"
    assert not a.isspace() and not b.isspace(), "A/B 不得是空白字符（见文件头判读）"
    assert a.isprintable() and b.isprintable(), "A/B 必须是可打印字符"
    assert text == text.rstrip(), "原文不得以空白结尾（本包设计选择，见文件头）"
    assert "\r" not in text and "\t" not in text, "原文不含 CR/TAB"

    io = IO(file_prefix="problem", data_id=i)  # problem{i}.in / problem{i}.out
    io.input_writeln(text)  # 第 1 行：原文（含空格原样写出）
    io.input_writeln(a, b)  # 第 2 行：以空格分隔的两个字符
    io.output_gen("../std")

    out = expected(text, a, b)
    if assert_out is not None and out != assert_out:
        raise AssertionError("第 %d 组期望输出与断言不符" % i)
    n_rep = sum(1 for ch in text if ch == a)
    _points.append((i, len(text), n_rep, note))
    print(
        "problem%-2d len=%-4d 替换=%-4d A=%r B=%r -- %s"
        % (i, len(text), n_rep, a, b, note)
    )


# ============================ 点 1：边界层·最小规模 ============================
# 原文长度 1 = 题面隐含的最小规模；唯一字符就是 A ⇒ 100% 替换率、答案恰 1 次替换
# （「答案为 1」的极端）。输出长度也是 1：全题理论最小输入/输出。
emit(1, "z", "z", "Z", "边界层·最小规模（len=1）+ 答案为 1 的极端（100% 替换）")

# ==================== 点 2：边界层·答案为 0 + len=2 + 标点 A/B ====================
# A='!' 不在原文 "a." 中 ⇒ 一次替换都没有（「答案为 0」的极端）；
# 同时覆盖「长度 2」这个最小非退化规模，以及 A、B 为标点字符（非字母）的情形。
emit(2, "a.", "!", "?", "边界层·答案为 0 的极端（A 不在原文）+ len=2 + 标点 A/B")

# ================= 点 3：边界层·题面声明的特殊值（样例逐字节回归） =================
# content.md【输入样例】原样（含 3 个词间空格与 1 个句号），断言 == 【输出样例】。
# 该样例天然覆盖「区分大小写」：原文同时含大写 'I'（被替换）与小写 'i'（Beijing，保留）。
emit(
    3,
    SAMPLE_TEXT,
    SAMPLE_A,
    SAMPLE_B,
    "边界层·题面声明的特殊值（【输入样例】原样，逐字节对齐【输出样例】）",
    assert_out=SAMPLE_OUT,
)

# ========================= 点 4：小规模随机（可手算核对） =========================
# 长度 4–12、小字符集（a/b/c + 数字 + 句点 + 空格）；A 从原文中取（保证确有替换）。
# 量级小到可以手算验证，作为随机层的起点。
_rng4 = random.Random(2046 + 4)
_alpha4 = "abc012. "
_len4 = _rng4.randint(4, 12)
_text4 = "".join(_rng4.choice(_alpha4) for _ in range(_len4))
_text4 = _text4.strip() or "abc"  # 去掉可能的首尾空格（本包原文不以空白结尾）
_A4 = _rng4.choice(_text4)  # 保证 A 出现在原文中
_B4 = _rng4.choice([c for c in "XYZ.#" if c != _A4])
emit(4, _text4, _A4, _B4, "小规模随机（len 4–12，小字符集，可手算核对）")

# ======================= 点 5：中等规模·A == B 临界 =======================
# 长度 60，A == B == 原文中出现的某个字符：替换是「恒等操作」，输出必须与原文逐字节相同。
# 专杀「先把 A 删掉再插入 B」「用 erase/insert 拼错位置」这类实现的 off-by-one。
_rng5 = random.Random(2046 + 5)


def pick_case_paired_letter(rng, text):
    """挑一个「在 text 中大小写两种形态都出现」的字母；没有则退化为任一非空白字符。

    这样 A == B 的恒等替换点同时具备大小写区分度：大小写不敏感的写法会把另一形态
    的字符也改成 A，输出立刻与原文不同。"""
    for lo in "abcdefghijklmnopqrstuvwxyz":
        if lo in text and lo.upper() in text:
            return lo
    return rng.choice(nonblank_list(text))


def nonblank_list(text):
    lst = [c for c in text if not c.isspace()]
    return lst if lst else list("abz")


_text5 = "".join(_rng5.choice(MIXED) for _ in range(60)).rstrip()
_text5 = _text5 or "aAb"
_A5 = pick_case_paired_letter(_rng5, _text5)  # 该字符在原文中大小写都出现
emit(5, _text5, _A5, _A5,
     "中等规模·临界 A == B（恒等替换：输出须原样等于原文；A 取大小写成对字母）")

# ==================== 点 6：中等规模·空白结构临界（len 恰 100） ====================
# 行首一段连续空格（起点 2 个，补齐余量也塞进词间空白，实测 9 个）；
# 词与词之间 1–N 个连续空格；结尾是非空白字符（末字符必为字母）。
# A='e' → 'E'（大小写翻转，替换点显眼），空格必须逐一原样保留：
# 杀「按空白分词读入（cin>>s / split）」「输出时压缩或丢弃空格」的写法。
def build_spaced_exact(rng, words, target):
    """构造恰 target 字符的「词 + 连续空格」文本，末字符必为非空白。

    行首固定写 2 个空格；长度不足 target 时把余量全部并进「第一个词之后的分隔符」，
    于是词间/首段空白宽度可达数十个连续空格 —— 正是本点要压的空白结构。"""
    s = "  "  # 行首两个空格
    inject_at = None  # 第二个词前的分隔符位置（用于把补齐余量塞进词间空白）
    i = 0
    while True:
        w = words[i % len(words)]
        i += 1
        sep = " " * rng.randint(1, 3)
        if len(s) + len(sep) + len(w) > target:
            break
        s += sep + w
        if inject_at is None:
            inject_at = len(s) - len(w)  # 第一个词结束处 = 其后的分隔符起点
    gap = target - len(s)
    if gap > 0:  # 余量加宽词间空白（不动末字符，仍以字母结尾）
        s = s[:inject_at] + " " * gap + s[inject_at:]
    assert len(s) == target and not s[-1].isspace(), (len(s), repr(s[-5:]))
    return s


_words6 = [
    "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
    "and", "then", "runs", "away", "into", "deep", "green", "wood",
]
_rng6 = random.Random(2046 + 6)
_text6 = build_spaced_exact(_rng6, _words6, 100)
emit(6, _text6, "e", "E", "中等规模·空白结构（行首连续空格 + 词间 1–N 连续空格，len 恰 100）")

# ========================= 点 7：大规模随机（len 170） =========================
# 接近上限（170/200）的混合字符集随机：大小写 + 数字 + 标点 + 空格；
# A 从原文中取（保证有替换），B 取一个不同的可见字符。
_rng7 = random.Random(2046 + 7)
_body7 = "".join(_rng7.choice(MIXED) for _ in range(168)).rstrip() or "abc"
_text7 = ("  " + _body7)[:200]  # 行首 2 个空格 + 随机正文（行首空白也不得被吞）
_text7 = _text7.rstrip()
_A7 = _rng7.choice(nonblank_list(_text7))
_B7 = _rng7.choice([c for c in "Zq7.%!" if c != _A7])
emit(7, _text7, _A7, _B7,
     "大规模随机（len 170 + 行首 2 空格，混合字符集，接近上限）")

# ============== 点 8：大规模定向·大小写敏感 + 相邻密集替换（len 190） ==============
# "Aa"×95：只有大写 A 被替换成 'a'，小写 a 必须原样保留 ⇒ 输出 "a"×190。
# 同时 A 出现 95 次且两两相邻（最坏相邻结构）；B='a' 本来就在原文中出现，
# 专杀「先全部标记再统一替换 / 两趟替换导致链式改写」的实现。
emit(8, "Aa" * 95, "A", "a", "大规模定向·大小写敏感 + 相邻密集替换（len 190，A 出现 95 次）")

# ================= 点 9：顶格层·长度上限 200 + 全相等（最坏密度） =================
# 200 个 'a'，A='a' ⇒ 200 次替换（全题理论最大替换次数），输出 200 个 'b'。
# 覆盖「全相等」结构与「替换密度 100%」的顶格构造，同时是长度上限。
emit(9, "a" * 200, "a", "b", "顶格层·len=200（上限）+ 全相等结构（200 次替换，最大密度）")

# ============== 点 10：顶格层·长度上限 200 + 字符集最广（满字符集） ==============
# 可打印非空白 ASCII（0x21..0x7E，共 94 个）各两轮 = 188 字符，再在中部插 12 个空格
# 补到恰好 200（不在行尾插，保证输出不以空格结尾）。A='a'、B='A'：
# 原文中 'a' 与 'A' 各出现 2 次 —— 只有 'a' 被替换，'A' 保持不变，空格全部原样保留。
# 这是「满长度 + 最大字符多样性 + 大小写敏感」的综合顶格点。
_cycle = PRINTABLE * 2  # 188 字符（94 种可打印非空白 ASCII × 2）
assert len(_cycle) == 188, len(_cycle)
_text10 = _cycle[:94] + " " * 12 + _cycle[94:]  # 中部插 12 空格 => 恰 200 字符
assert len(_text10) == 200, len(_text10)
emit(10, _text10, "a", "A", "顶格层·len=200（上限）+ 满字符集（94 种可打印非空白 ASCII 全轮两遍 + 12 空格）")


# ============================== 生成期自检 ==============================
# 1) 每组 .in 回读解析，校验格式与范围；
# 2) 用独立于 std 的 Python per-char 直译重算答案，与 std 生成的 .out 逐字节比对；
# 3) 校验输出恰为一行（末尾恰一个 '\n'、无 '\r'、无行尾多余空白）。
def verify():
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    problems = []
    for i in range(1, 11):
        fin = os.path.join(data_dir, "problem%d.in" % i)
        fout = os.path.join(data_dir, "problem%d.out" % i)
        assert os.path.exists(fin), "缺少 " + fin
        assert os.path.exists(fout), "缺少 " + fout
        raw_in = open(fin, "rb").read().decode("ascii")  # 必须是纯 ASCII
        assert raw_in.endswith("\n"), "第 %d 组 .in 末尾缺换行" % i
        lines = raw_in[:-1].split("\n")
        assert len(lines) == 2, "第 %d 组 .in 行数应为 2，实际 %d" % (i, len(lines))
        text, second = lines
        toks = second.split(" ")
        assert len(toks) == 2, "第 %d 组第 2 行应恰有 2 个以空格分隔的字符" % i
        a, b = toks
        assert len(a) == 1 and len(b) == 1, "第 %d 组 A/B 必须是单字符" % i
        assert len(text) <= MAX_LEN, "第 %d 组原文超长 %d" % (i, len(text))
        assert text == text.rstrip(), "第 %d 组原文以空白结尾" % i

        raw_out = open(fout, "rb").read().decode("ascii")
        assert raw_out.endswith("\n") and not raw_out.endswith("\n\n"), \
            "第 %d 组 .out 末尾应恰一个换行" % i
        assert "\r" not in raw_out, "第 %d 组 .out 含 CR" % i
        got = raw_out[:-1]
        assert "\n" not in got, "第 %d 组 .out 应只有一行" % i
        assert got == expected(text, a, b), "第 %d 组 .out 与 Python 直译不符" % i
        assert got == got.rstrip(), "第 %d 组输出以空白结尾" % i
        problems.append((i, len(text), len(got), sum(1 for c in text if c == a)))

    # 点 3 必须与题面【输出样例】逐字节一致
    sample_out = open(os.path.join(data_dir, "problem3.out"), "rb").read().decode("ascii")
    assert sample_out == SAMPLE_OUT + "\n", "点 3（样例）输出与题面【输出样例】不符：" + repr(sample_out)

    print("\n==== 自检通过 ====")
    print("点号  原文长度  输出长度  替换次数")
    for i, l1, l2, rep in problems:
        print("%-5d %-8d %-8d %d" % (i, l1, l2, rep))
    print("样例（点 3）：%r -> %r  （与题面【输出样例】逐字节一致）"
          % (SAMPLE_TEXT, SAMPLE_OUT))
    print("全部 10 组：.in/.out 成对、纯 ASCII、原文 <= 200、A/B 单字符非空白、"
          "输出恰一行、与 Python 直译逐字节一致。")


verify()
