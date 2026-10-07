#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 一本通 1703《量子纠缠》分层测试数据生成器（只生成数据；按任务要求不做对拍）
# 运行：cd data && python3 ../data.py       （std 在上一级目录，io.output_gen("../std")）
#
# ---------------------------------------------------------------------------
# 题面数据范围（content.md【提示】）：
#   m <= 1e5                 操作总数
#   c <= 2050                操作 1 与操作 3 的次数之和
#   S <= 8e6                 所有询问串（操作 2）的总长度
#   L <= 50                  操作 1 / 操作 3 中数字串的长度上限（串非空）
#   P ≡ m (mod 10)           题面未解释 P；本生成器按「P = 测试点编号」解读，
#                            令每个点的 m ≡ 点号 (mod 10)（该解读见 gen-report.md 风险点）
#   题面点特征：不含操作3 / 串中只出现字符 0 / 信息集有限 / 1、3 操作全在 2 操作之前
#
# 数据语义（与 std 同一建模）：
#   纠缠 a b 令 a、b 成为「右语言等价」的同一状态（Myhill–Nerode 意义），等价类合并时
#   两状态的 10 条出边一并合并，故一次纠缠可能连带把（本用例下）同一后缀族的大量串
#   纳入信息集。生成器只用下面三条**可证**规则给询问打期望标记，其余询问交给 std：
#     规则 A：串 s 被操作 1 加入后，其后任意时刻询问 s 必为 1
#             （fin 只置真不置假、等价类只合并不拆分；且 s 的状态节点此后一直可达）。
#     规则 B：若数字 c 从未作为任何 1/3 操作串的首字符出现，则任何以 c 开头的询问串
#             必为 0（根节点永不参与合并，其 ch[c] 恒为空）。规则 B 与操作顺序无关。
#     规则 C：整份数据不含操作 3 时，信息集恰为「此前被操作 1 加入的串集合」，
#             故每个询问的答案可精确判定（加入过 ⇒ 1，否则 ⇒ 0）。
#   另有标记 '1d'（派生 1，可证）：若已加入的串 a 与 a+d 被纠缠（操作 3），
#   则状态[a] 的 d 出边指向自身，于是 a+d^k (k>=1) 全部进集 —— 这些串**从未被直接
#   加入**却必答 1，正是题面「一次纠缠可能导致若干（可能为无穷多个）串被加入」的直接
#   体现。生成器只在收尾（所有 1/3 之后，且 a 已被加入）放这类询问，并逐条校验
#   「确实未被直接加入」+「确实答 1」。
#   gen-report.md 记录：std 已由 3 份独立实现随机互验一致，另有样例验证。
#
# 分层设计（10 个测试点，由边界铺到顶格；每点独立 Random(170300+i) 种子，逐字节可复现）：
#   点 1  m=11      边界层：|s| 取 1 与 50 两端；1 次纠缠；含规则 A/B 收尾询问
#   点 2  m=12      边界层：所有串只含字符 0（题面点特征）；纠缠 ("00","000") 造成真实合并
#   点 3  m=493     小规模（对齐题面「m<=500」档）：字母表仅 {0,1}，
#                   含长度 50 的重复/拼接串（超长询问压力）
#   点 4  m=504     小规模随机：十进制随机、L=8（暴力/手算可验证量级）
#   点 5  m=1005    中等规模随机：L=20，250 次纠缠，范围中间档
#   点 6  m=99996   大规模（**不含操作 3**，题面点特征）：c=2050 顶格；规则 C 使
#                   全部 97946 个询问的答案可精确判定
#   点 7  m=99997   大规模随机：c=2050 顶格（1550 次加入 + 500 次纠缠），L=50
#   点 8  m=1998    中等规模（对应题面「m<=2000」档）：L=50，249 次纠缠
#   点 9  m=99999   顶格层：c=2050 顶格且 1、3 操作全在 2 操作之前（题面点特征）；
#                   纠缠按「同一后缀族的前缀与其+'3'」配对 ⇒ 形成自环等价类，
#                   加入某后缀族串会自动带出该族的 3、33、333…（信息集无限）
#   点 10 m=100000  顶格层：仅询问（c=0，信息集恒空 ⇒ 全部答案 0，规则 C 可证）；
#                   S=7.9e6 逼近 8e6 上限，压力集中在输入长度与输出量（I/O 最坏）
# ---------------------------------------------------------------------------
from cyaron import IO  # noqa: F401
import os
import random
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIGITS = "0123456789"
KEY_DIGITS = "012345678"      # 键串（1/3 操作的串）只用 0..8，留出 '9' 给规则 B
FREE = "9"                    # 规则 B 专用首字符
MAXM, MAXC, MAXS, MAXL = 100000, 2050, 8 * 10 ** 6, 50


def rand_str(rng, n, digits=DIGITS):
    return "".join(rng.choice(digits) for _ in range(n))


def uniq_keys(rng, cnt, lo, hi, digits=KEY_DIGITS, exclude=()):
    """cnt 个互不相同的键串（长度 lo..hi）。"""
    out, seen = [], set(exclude)
    for _ in range(400 * cnt + 10000):
        if len(out) == cnt:
            return out
        s = rand_str(rng, rng.randint(lo, hi), digits)
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    raise RuntimeError("uniq_keys: 键池不足 (cnt=%d lo=%d hi=%d)" % (cnt, lo, hi))


def zero_queries(rng, cnt, lo=2, hi=20):
    """cnt 个规则 B 询问（必 0）：首字符为 '9'，键串从不以 '9' 开头。"""
    out, seen = [], set()
    while len(out) < cnt:
        s = FREE + rand_str(rng, rng.randint(lo - 1, hi - 1))
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def build(adds, merges, body_queries, tail_queries, m, rng, mode="interleave"):
    """拼装操作序列。

    adds / merges : 操作 1 与操作 3 的操作数
    body_queries  : [(s, exp)] 夹杂在操作之间的询问（exp 多为 None，规则 B 可带 '0'）
    tail_queries  : [(s, exp)] 文件末尾的询问（在所有 1/3 之后，可安全用规则 A）
    m             : 期望操作总数（必须精确相等）
    返回 (lines, expects)：lines 为 m 行操作，expects 等长，'0'/'1'/None
    """
    assert len(adds) + len(merges) + len(body_queries) + len(tail_queries) == m, (
        "m 不匹配: adds=%d merges=%d body=%d tail=%d 期望 %d"
        % (len(adds), len(merges), len(body_queries), len(tail_queries), m))

    ops = [("1", s) for s in adds] + [("3", a, b) for (a, b) in merges]
    body = ops + [("2", s, e) for (s, e) in body_queries]
    if mode == "ops_first":            # 所有 1、3 排在所有 2 之前（允许预标 '1'/'1d'）
        heads = [x for x in body if x[0] != "2"]
        qs = [x for x in body if x[0] == "2"]
        rng.shuffle(heads)
        rng.shuffle(qs)
        body = heads + qs
    elif mode == "queries_only":
        assert not ops, "queries_only 模式只能含询问"
        rng.shuffle(body)
    else:
        rng.shuffle(body)
        for q in body:                 # 规则 B 的期望 '0' 与顺序无关；'1'/'1d' 依赖顺序
            assert q[0] != "2" or q[2] in (None, "0"), \
                "打散模式只允许预标 '0'（'1'/'1d' 依赖操作顺序，请放进 tail）"
    body += [("2", s, e) for (s, e) in tail_queries]

    lines, expects = [], []
    for op in body:
        if op[0] == "2":
            lines.append("2 " + op[1])
            expects.append(op[2])
        else:
            lines.append(" ".join(op))
            expects.append(None)
    return lines, expects


def chain_merges(stems, d, cnt=None):
    """「自环」型纠缠：merge (s, s+d) 且 s 已被 op1 加入。

    效果：等价类 [s] 的 d 出边指向自身，于是 s+d^k（k>=1）全部被带入信息集
    —— 正对应题面「一次纠缠可能导致若干（可能为无穷多个）串被加入」。
    这些串从未被 op1 直接加入，故其答案为 1 即为「派生 1」，可用于验证合并语义。
    """
    picked = [s for s in stems if len(s) + len(d) <= MAXL]
    if cnt is not None:
        assert cnt <= len(picked), (cnt, len(picked))
        picked = picked[:cnt]
    return [(s, s + d) for s in picked]


def planned_body(rng, n, spec):
    """按 spec=[(比例, 生成函数)] 生成 n 个夹入询问，比例按四舍五入取整、总数精确等于 n。
    生成函数签名 f(rng) -> (s, exp)。"""
    assert abs(sum(p for p, _ in spec) - 1.0) < 1e-9, "比例之和需为 1"
    cnts, acc = [], 0.0
    for p, _ in spec[:-1]:
        k = int(round(p * n))
        cnts.append(k)
        acc += p
    cnts.append(n - sum(cnts))
    assert all(k >= 0 for k in cnts), (cnts, n)
    out = []
    for (_, f), k in zip(spec, cnts):
        for _ in range(k):
            out.append(f(rng))
    rng.shuffle(out)
    return out


def make_body(rng, n, key_pool, long_gen, random_gen, zero_gen, p=(0.35, 0.2, 0.25, 0.2)):
    """通用的夹入询问构造：按 p 四种类型分配数量（精确合计 n）。
    key_pool(s) 为键串池；long_gen / random_gen / zero_gen 分别为长串/随机短串/规则B生成器。
    """
    spec = [
        (p[0], lambda r: (key_pool(r), None)),
        (p[1], lambda r: long_gen(r)),
        (p[2], lambda r: random_gen(r)),
        (p[3], lambda r: zero_gen(r)),
    ]
    return planned_body(rng, n, spec)


def write_case(io, lines):
    io.input_write(str(len(lines)) + "\n" + "\n".join(lines) + "\n")
    io.output_gen("../std")
    # cyaron 不自动 flush，立即落盘供下面回读复核
    io.input_file.flush()
    try:
        io.output_file.flush()
    except (AttributeError, OSError):
        pass


# ============================================================ 点 1 边界层 m=11
def point1(rng):
    adds = ["0", "1" * 50, "9" * 50]                 # |s| = 1 与 50 两端（首字符 0/1/9）
    merges = [("0", "00")]                            # 1 次纠缠（"00" 未加入）
    body = [("00", None), ("000", None),              # 派生 1：合并后自动入集
            ("0" * 50, None), ("1" * 50, None)]      # 4 个
    tail = [("9" * 50, "1"),                          # 规则 A
            ("00", "1d"), ("0" * 4, "1d"),            # 派生 1（未直接加入，由纠缠带出）
            ("2" * 20, "0"),                          # 规则 B（首字符 2 未用于 1/3）
            ("3" + "9" * 49, "0")]                    # 规则 B
    # 3 次加入 + 1 次纠缠 + 2 个夹入询问 + 5 个收尾询问 = 11
    body = body[:2]
    return build(adds, merges, body, tail, 11, rng, "interleave")


# ============================================ 点 2 边界层（全部串只含字符 0）m=12
def point2(rng):
    adds = ["0", "00", "0" * 50]
    merges = [("00", "000")]                          # 同一后缀族，真实产生合并
    body = [("0" * k, None) for k in (1, 2, 3, 4, 5, 49)]        # 6 个
    tail = [("0" * 50, "1"), ("0", "1"),                          # 规则 A
            ("0" * 6, "1d"), ("0" * 12, "1d")]                    # 派生 1（纠缠带出）
    # 3 次加入 + 1 次纠缠 + 6 个夹入询问 + 4 个收尾询问 = 12
    body = body[:4]
    return build(adds, merges, body, tail, 12, rng, "interleave")


# ======================================= 点 3 小规模：字母表仅 {0,1}，含长串 m=503
def point3(rng):
    keys = uniq_keys(rng, 120, 1, 50, digits="01")
    m = 493            # 同时满足题面「m<=500」档与 m ≡ 3 (mod 10)
    adds = keys[:118]
    short = [s for s in adds if len(s) <= 6][:6]
    merges = chain_merges(short[:4], "0")                 # 4 次自环纠缠（派生 1）
    merges += [(keys[118], keys[119])]                    # 1 次无关配对
    n_body = m - len(adds) - len(merges) - 2              # 2 个收尾询问
    extended = [(s + "0" * k, None) for s in short[:3] for k in (1, 2, 3, 6, 12)]
    body = list(extended)
    while len(body) < n_body:
        r = rng.random()
        if r < 0.35:
            body.append((rng.choice(keys), None))
        elif r < 0.6:
            base = rng.choice(["01", "010", "0100", "10", "1", "0"])
            body.append(((base * 40)[:rng.randint(20, 50)], None))       # 重复串
        elif r < 0.8:
            body.append((rand_str(rng, rng.randint(1, 50), "01"), None))
        else:
            body.append((("010010" * 9)[:rng.randint(45, 50)], None))    # 长度贴 50
    tail = [(adds[0], "1"), (adds[7], "1"),                          # 规则 A
            (short[0] + "0" * 7, "1d"), (short[1] + "0" * 9, "1d")]  # 派生 1
    body = body[:n_body - 2]
    return build(adds, merges, body, tail, m, rng, "interleave")


# ================================================ 点 4 小规模随机（L=8）m=504

def point4(rng):
    keys = uniq_keys(rng, 64 + 60, 1, 8)          # 64 个加入 + 60 个无关配对用键
    m = 504
    adds = keys[:64]
    short = [s for s in adds if len(s) <= 6][:30]
    merges = chain_merges(short[:10], "0")        # 10 次自环纠缠（派生 1）
    merges += [(keys[64 + 2 * i], keys[65 + 2 * i]) for i in range(30)]
    n_body = m - len(adds) - len(merges) - 2
    extended = [(s + "0" * k, None) for s in short[:5] for k in (1, 2, 3, 5)]
    body = list(extended)
    zs = zero_queries(rng, n_body)
    while len(body) < n_body:
        r = rng.random()
        if r < 0.35:
            body.append((rng.choice(keys), None))
        elif r < 0.55:
            body.append((rng.choice(keys) * rng.randint(2, 6), None))    # 拼接长串
        elif r < 0.75:
            body.append((rand_str(rng, rng.randint(1, 30)), None))
        else:
            body.append((zs.pop(), "0"))                                 # 规则 B
    tail = [(adds[3], "1"), (adds[-1], "1"),                             # 规则 A
            (short[0] + "0" * 8, "1d"), (short[1] + "0" * 11, "1d")]     # 派生 1
    body = body[:n_body - 2]
    return build(adds, merges, body, tail, m, rng, "interleave")


# ================================ 点 5 中等规模随机（L=20，250 纠缠）m=1005

def point5(rng):
    keys = uniq_keys(rng, 1000, 2, 20)
    m = 1005
    adds = keys[:350]
    short = [s for s in adds if len(s) <= 17][:25]
    merges = chain_merges(short[:20], "17")       # 20 次自环纠缠（派生 1，|s|<=19）
    merges += [(keys[350 + 2 * i], keys[351 + 2 * i]) for i in range(230)]
    n_body = m - len(adds) - len(merges) - 2
    extended = [(s + "17" * k, None) for s in short[:4] for k in (1, 2, 3, 5)]
    body = list(extended)
    zs = zero_queries(rng, n_body)
    while len(body) < n_body:
        r = rng.random()
        if r < 0.35:
            body.append((rng.choice(keys), None))
        elif r < 0.6:
            body.append((rng.choice(keys) * rng.randint(2, 20), None))    # 长度可到 400
        elif r < 0.8:
            body.append((rand_str(rng, rng.randint(1, 400)), None))
        else:
            body.append((zs.pop(), "0"))                                  # 规则 B
    tail = [(adds[5], "1"), (adds[300], "1"),                             # 规则 A
            (short[0] + "17" * 8, "1d"), (short[2] + "17" * 6, "1d")]     # 派生 1
    body = body[:n_body - 2]
    return build(adds, merges, body, tail, m, rng, "interleave")


# ================= 点 6 大规模：不含操作 3（题面点特征），全部询问可精确判定 m=99996
def point6(rng):
    m = 99996
    adds = uniq_keys(rng, 2050, 1, 50)                # c = 2050 顶格，无 op3
    n_q = m - len(adds)                               # 97946 个询问
    ops = [("1", s) for s in adds]
    n_zero = n_q // 8
    zs = zero_queries(rng, n_zero, lo=2, hi=50)
    for i in range(n_q):
        r = rng.random()
        if i < n_zero:
            ops.append(("2", zs[i]))
        elif r < 0.55:
            ops.append(("2", rng.choice(adds)))                       # 与已加入串重合
        elif r < 0.75:
            ops.append(("2", rng.choice(adds) * rng.randint(2, 3)))   # 拼接（多为 0）
        elif r < 0.9:
            ops.append(("2", rand_str(rng, rng.randint(1, 50))))
        else:
            ops.append(("2", rand_str(rng, rng.randint(50, 90))))
    rng.shuffle(ops)
    # 规则 C：无 op3 ⇒ 1 当且仅当该串此前被操作 1 加入过；规则 B 一并覆盖
    got, lines, expects = set(), [], []
    for op in ops:
        if op[0] == "1":
            got.add(op[1])
            lines.append("1 " + op[1])
            expects.append(None)
        else:
            s = op[1]
            lines.append("2 " + s)
            expects.append("1" if s in got else "0")
    assert len(lines) == m
    return lines, expects


# ================= 点 7 大规模随机：m=99997，c=2050 顶格（1550 加入 + 500 纠缠）

def point7(rng):
    m = 99997
    keys = uniq_keys(rng, 1550 + 900 + 160, 1, 50)
    adds = keys[:1550]
    short = [s for s in adds if len(s) <= 48][:60]
    merges = chain_merges(short[:50], "3")        # 50 次自环纠缠（派生 1）
    merges += [(keys[1550 + 2 * i], keys[1551 + 2 * i]) for i in range(450)]
    n_body = m - len(adds) - len(merges) - 2
    extended = [(s + "3" * k, None) for s in short[42:50] for k in (1, 2, 3, 6, 10, 20)]
    body = list(extended)
    zs = zero_queries(rng, n_body)
    while len(body) < n_body:
        r = rng.random()
        if r < 0.35:
            body.append((rng.choice(keys), None))
        elif r < 0.5:
            body.append((rng.choice(keys) * rng.randint(2, 3), None))
        elif r < 0.9:
            body.append((rand_str(rng, rng.choice([1, 2, 3, 50, 60, 90])), None))
        else:
            body.append((zs.pop(), "0"))                                  # 规则 B
    tail = [(adds[0], "1"), (adds[1000], "1"),                       # 规则 A
            (short[0] + "3" * 30, "1d"), (short[25] + "3" * 12, "1d"),  # 派生 1
            (short[45] + "3" * 40, "1d")]                            # 长度 <=50
    body = body[:n_body - 3]
    return build(adds, merges, body, tail, m, rng, "interleave")


# =============================== 点 8 中等规模（m<=2000 档，L=50）m=1998

def point8(rng):
    m = 1998
    keys = uniq_keys(rng, 700 + 500 + 60, 1, 50)
    adds = keys[:700]
    short = [s for s in adds if len(s) <= 47][:30]
    merges = chain_merges(short[:24], "25")       # 24 次自环纠缠（派生 1）
    merges += [(keys[700 + 2 * i], keys[701 + 2 * i]) for i in range(225)]
    n_body = m - len(adds) - len(merges) - 2
    extended = [(s + "25" * k, None) for s in short[20:24] for k in (1, 2, 3, 5)]
    body = list(extended)
    zs = zero_queries(rng, n_body)
    while len(body) < n_body:
        r = rng.random()
        if r < 0.35:
            body.append((rng.choice(keys), None))
        elif r < 0.55:
            body.append((rng.choice(keys) * rng.randint(2, 10), None))   # 长拼接
        elif r < 0.85:
            body.append((rand_str(rng, rng.randint(1, 300)), None))
        else:
            body.append((zs.pop(), "0"))                                 # 规则 B
    tail = [(adds[1], "1"), (adds[600], "1"),                           # 规则 A
            (short[0] + "25" * 15, "1d"), (short[3] + "25" * 8, "1d")]  # 派生 1
    body = body[:n_body - 2]
    return build(adds, merges, body, tail, m, rng, "interleave")


# ==== 点 9 顶格层：m=99999，c=2050 顶格，1/3 全在 2 之前；纠缠造出「自环」等价类
def point9(rng):
    m = 99999
    # 后缀族：stems[i] = "7" + 6 位编号（长度 7，两两不同，首字符都是 '7'）
    stems = ["7%06d" % i for i in range(700)]
    # 每次纠缠 (stem, stem+"3") ⇒ δ([stem],"3") = [stem]：加入 stem 会连带加入
    # stem+"3", stem+"33", ...（信息集在此处为无限集，正对题面「可能为无穷多个」）
    merges = [(st, st + "3") for st in stems]
    adds = stems[:200] + uniq_keys(rng, 1150, 1, 50, exclude=stems)   # c = 700+1350 = 2050
    n_body = m - len(adds) - len(merges) - 2
    zs = zero_queries(rng, n_body)
    def key_pool(r):
        return r.choice(stems) if r.random() < 0.45 else r.choice(adds)

    derived_set = set(stems[:200])          # 这些 stem 被 op1 加入过 ⇒ stem+"3"*k 必 1

    def long_gen(r):
        st = r.choice(stems)
        s_ = st + "3" * r.randint(1, 43)     # 长度 <= 50
        return (s_, "1d" if st in derived_set else None)

    body = make_body(
        rng, n_body, key_pool=key_pool,
        long_gen=long_gen,
        random_gen=lambda r: (r.choice(stems) + rand_str(r, r.randint(1, 42)), None),
        zero_gen=lambda r: (zs.pop(), "0"), p=(0.3, 0.2, 0.35, 0.15))
    tail = [(adds[10], "1"), (adds[-1], "1")]        # 规则 A
    return build(adds, merges, body, tail, m, rng, "ops_first")


# ======== 点 10 顶格层：仅询问、信息集恒空（答案全 0）、S≈7.9e6 逼近 8e6 上限
def point10(rng):
    m = 100000
    body = []
    total = 0
    for _ in range(m):
        n = rng.choice([78] * 4 + [79] * 4 + [80] * 2)
        total += n
        body.append((rand_str(rng, n), "0"))
    assert total <= MAXS, "S 超限: %d" % total
    return build([], [], body, [], m, rng, "queries_only")


POINTS = {1: point1, 2: point2, 3: point3, 4: point4, 5: point5,
          6: point6, 7: point7, 8: point8, 9: point9, 10: point10}


def stats(lines):
    c = sum(1 for x in lines if x[0] in "13")
    S = sum(len(x) - 2 for x in lines if x[0] == "2")
    L = max([len(x.split()[1]) for x in lines if x[0] in "13"] or [0])
    q = sum(1 for x in lines if x[0] == "2")
    return len(lines), c, S, L, q


def _derived1_witness(s_, a, b, added_set):
    """可证性见证：merge(a,b)、b == a+d（d 非空）、s_ == a + d^k (k>=1)、且 a 被 op1 加入。

    这类 s_ 必在信息集内：状态[a] 的 d 出边指向 [a] 自身 ⇒ s_ 与 a 同状态，而 a 已定终态。
    """
    if not s_.startswith(a) or a not in added_set:
        return False
    if not b.startswith(a):
        return False
    d = b[len(a):]
    if not d:
        return False
    rest = s_[len(a):]
    if not rest or len(rest) % len(d):
        return False
    return rest == d * (len(rest) // len(d))


def readback_check(i, lines, expects):
    """回读 .in/.out：格式校验 + 规则 A/B/C 复核 + 确定性点全量核对。"""
    p_in = os.path.join(BASE_DIR, "data", "problem%d.in" % i)
    p_out = os.path.join(BASE_DIR, "data", "problem%d.out" % i)
    inp = open(p_in, encoding="utf-8").read()
    outp = open(p_out, encoding="utf-8").read()
    assert inp == str(len(lines)) + "\n" + "\n".join(lines) + "\n", "点%d: .in 内容与生成不符" % i

    in_lines = inp.split("\n")[:-1]
    assert len(in_lines) == len(lines) + 1, "点%d: 行数不符" % i
    assert in_lines[0] == str(len(lines)), "点%d: 首行 m 不符" % i
    ops = in_lines[1:]
    for k, x in enumerate(ops):
        parts = x.split()
        assert parts[0] in "123", "点%d 第%d行: 操作码非法" % (i, k + 1)
        assert len(parts) == (3 if parts[0] == "3" else 2), "点%d 第%d行: 项数非法" % (i, k + 1)
        for s in parts[1:]:
            assert s and s.isdigit(), "点%d 第%d行: 串非法" % (i, k + 1)

    ans = [x for x in outp.split("\n") if x != ""]
    qpos = [k for k, x in enumerate(ops) if x[0] == "2"]
    assert len(ans) == len(qpos), "点%d: 输出行数 %d != 询问数 %d" % (i, len(ans), len(qpos))
    assert all(a in ("0", "1") for a in ans), "点%d: 输出并非只有 0/1" % i

    # 期望标记逐条核对
    for j, pos in enumerate(qpos):
        e = expects[pos]
        assert e in (None, "0", "1", "1d"), "点%d: 非法期望标记 %r" % (i, e)
        if e is not None:
            want = "1" if e == "1d" else e
            assert ans[j] == want, ("点%d: 第%d个询问 %r 期望 %s 实得 %s"
                                    % (i, j, ops[pos][:46], want, ans[j]))

    # 规则 B 全量复核：首字符从未在任何 1/3 串首位出现 ⇒ 必须为 0
    first_chars = {x.split()[1][0] for x in ops if x[0] in "13"}
    for j, pos in enumerate(qpos):
        s = ops[pos].split()[1]
        if s[0] not in first_chars:
            assert ans[j] == "0", ("点%d: 规则B 违反 %r 首字符 %r 未用于 1/3 却答 %s"
                                   % (i, s[:46], s[0], ans[j]))
    # 规则 C 全量复核：无 op3 ⇒ 答案 = 该串此前是否被 op1 加入
    if not any(x[0] == "3" for x in ops):
        got, j = set(), 0
        for x in ops:
            parts = x.split()
            if parts[0] == "1":
                got.add(parts[1])
            else:
                assert ans[j] == ("1" if parts[1] in got else "0"), \
                    "点%d: 规则C 违反 @%r (实得 %s)" % (i, parts[1][:46], ans[j])
                j += 1
    # 规则 A / C 复核（O(n)）：期望为 1 的询问，其串必须在此前已被 op1 加入
    merges = [tuple(x.split()[1:]) for x in ops if x[0] == "3"]
    added, j, pos_of_j = set(), 0, 0
    for x in ops:
        if x[0] == "1":
            added.add(x.split()[1])
            continue
        if x[0] == "3":
            continue
        e = expects[qpos[j]]
        pos_of_j = qpos[j]
        if e == "1":
            assert x.split()[1] in added, \
                "点%d: 第%d个询问标记必1(规则A)但此前无加入 %r" % (i, j, x.split()[1][:46])
        elif e == "1d":
            # 派生 1：答案为 1 但该串从未被 op1 直接加入 —— 只能由纠缠的等价类合并带出
            s_ = x.split()[1]
            assert s_ not in added, \
                "点%d: 第%d个询问标记为派生1却被直接加入过 %r" % (i, j, s_[:46])
            wit = [aa for (aa, bb) in merges if _derived1_witness(s_, aa, bb, added)]
            assert wit, ("点%d: 第%d个询问 %r 找不到派生1的构造见证"
                         % (i, j, s_[:46]))
            # 顺序前提：见证串 aa 必须在此询问之前已被 op1 加入过
            assert any(x[0] == "1" and x.split()[1] == aa for aa in wit for x in ops[:pos_of_j]), \
                "点%d: 第%d个询问 %r 的见证串此前未被加入" % (i, j, s_[:46])
        j += 1
    return len(ans)


def main():
    t0 = time.time()
    for i in range(1, 11):
        rng = random.Random(170300 + i)
        lines, expects = POINTS[i](rng)
        m, c, S, L, q = stats(lines)
        assert m == len(lines) and m <= MAXM, ("点%d m 超限" % i, m)
        assert c <= MAXC, ("点%d c 超限" % i, c)
        assert S <= MAXS, ("点%d S 超限" % i, S)
        assert L <= MAXL, ("点%d L 超限" % i, L)
        assert m % 10 == i % 10, ("点%d 未满足 m≡点号 (mod 10)" % i, m)
        t1 = time.time()
        io = IO(file_prefix="problem", data_id=i)
        write_case(io, lines)
        n_q = readback_check(i, lines, expects)
        print("problem%-2d: m=%-6d c=%-5d S=%-8d maxL=%-2d queries=%-6d "
              "gen%5.1fs std%5.1fs 复核=OK" % (i, m, c, S, L, n_q, t1 - t0, time.time() - t1))
        t0 = time.time()


if __name__ == "__main__":
    main()
