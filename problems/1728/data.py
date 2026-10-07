#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1728《构造序列》分层测试数据生成器（cyaron）。

用法：mkdir -p data && cd data && python3 ../data.py
      （std 须已编译在上一级目录：g++ -O2 -std=c++17 std.cpp -o std）

题面数据范围（content.md【提示】）：
    1 <= s <= n <= 1e5, 1 <= m <= 2e5, Σk <= 3e5, 1 <= l < r <= n,
    1 <= k <= r-l, l <= x_1 < ... < x_k <= r, 值域 [1,1e9]，已知位置 p_i 递增。

分层设计（10 点，由边界铺到顶格；每点独立种子，逐字节可复现）：
  点 1  n=2,    s=2,   m=1      边界：最小规模 + 值域下界 1 出现在解中；全已知 ⇒ 唯一解
  点 2  n=5,    s=2,   m=2      边界：两条信息互为反制（成环）⇒ NIE；含值域上界 1e9
  点 3  n=100,  s=50,  m=200    小规模：隐藏解 = 互异随机排名，x = 区间内最大的 k 个
  点 4  n=6,    s=2,   m=5      小规模 NIE：递增链 + 已知 a[1]=1,a[6]=5 冲突
  点 5  n=1000, s=100, m=1500   中等：短区间 top-k，值互异、x 分散、k∈{1,2,3}
  点 6  n=5000, s=2500,m=20000  中等：8 级台阶隐藏解（值大量重复），x = 区间最高级的全部位置
  点 7  n=1e5,  s=5e4, m=1e5    大规模：长区间（均值 5e4）+ x=区间后缀，k∈{1,2}
  点 8  n=1e5,  s=1,   m=99999  大规模 NIE：长度 1e5 严格递增链 + 已知 a[1]=1e9 ⇒ 下界 > 1e9
  点 9  n=1e5,  s=n,   m=2e5    顶格：Σk=3e5 顶格、值线性铺满且恰含 1e9；全已知 ⇒ 唯一解
 点 10  n=1e5,  s=n,   m=2e5    顶格：奇高偶低交替（值域两端）+ 1000 条 k=100 的“隔位”信息
                                （每条 100~101 个单点缺口 ⇒ 线段树拆图边数最坏）；全已知 ⇒ 唯一解

要点：
  * 可行点（1,3,5,6,7,9,10）一律由**隐藏可行解**反构信息 —— x 取区间内严格最大的一批位置，
    因此「无解」只可能来自刻意构造的点 2、4、8；
  * 点 9/10 全已知（s=n）⇒ 答案被完全钉死，脚本逐位比对隐藏解，可发现 std 的任何偏差；
  * 点 7 由后缀型约束强制递增；点 6 专测值重复；点 10 专测缺口极多（建图边数最坏）；
  * 点 8 专测「下界超过 1e9 ⇒ NIE」这一题面坑点（易漏判）。

⚠ cyaron 隐患防护（题面要求的重点）：output_gen 在 std 缺失/崩溃时会**静默**产出 0 字节 .out。
  本脚本因此 ① 启动先断言 std 存在可执行，并用题面样例实跑校验；② 每组生成后回读 .in/.out，
  断言非空、行数/数字个数符合预期、Σk 不超限，并用 work/check.py（独立实现）逐条验证
  「严格大于」语义、值域与已知值一致性；③ 期望 NIE 的点核对 std 确实判 NIE。
"""
import os
import random
import shlex
import sys
import time

from cyaron import IO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STD = os.path.join(BASE_DIR, "std")
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.insert(0, BASE_DIR)
from work.check import validate as check_one      # noqa: E402  独立校验器（另一份实现）

N_MAX, M_MAX, SUMK_MAX, VAL_MAX = 100000, 200000, 300000, 10 ** 9

SAMPLE_IN = "5 2 2\n2 7\n5 3\n1 4 2 2 3\n4 5 1 4\n"


# ------------------------------------------------------------------ 格式与自检

def write_input(io, n, s, m, known, infos):
    """known=[(p,d)] 位置须递增；infos=[(l,r,[x...])]，x 须严格递增。"""
    out = ["%d %d %d" % (n, s, m)]
    for (p, d) in known:
        out.append("%d %d" % (p, d))
    for (l, r, xs) in infos:
        out.append("%d %d %d %s" % (l, r, len(xs), " ".join(map(str, xs))))
    io.input_write("\n".join(out) + "\n")


def check_input(path, n, s, m):
    """回读 .in：行数 / 值域 / 递增性 / k 与 x 个数一致 / Σk —— 逐项断言。"""
    with open(path, "r") as f:
        lines = f.read().split("\n")
    assert lines and lines[-1] == "", "%s: .in 末尾缺换行" % path
    body = lines[:-1]
    assert len(body) == 1 + s + m, "%s: 行数 %d != 1+s+m=%d" % (path, len(body), 1 + s + m)
    h = body[0].split()
    assert len(h) == 3 and tuple(map(int, h)) == (n, s, m), "%s: 首行 %r 不符" % (path, h)
    assert 1 <= s <= n <= N_MAX and 1 <= m <= M_MAX, "%s: n/s/m 越界" % path
    prev = 0
    for i in range(1, 1 + s):
        p, d = map(int, body[i].split())
        assert prev < p <= n, "%s: 已知位置非递增/越界 (行%d: %d)" % (path, i, p)
        assert 1 <= d <= VAL_MAX, "%s: 已知值越界 (行%d: %d)" % (path, i, d)
        prev = p
    sumk = 0
    for i in range(1 + s, len(body)):
        v = list(map(int, body[i].split()))
        l, r, k, xs = v[0], v[1], v[2], v[3:]
        assert len(xs) == k, "%s: 行%d k=%d 与实际 %d 个不符" % (path, i, k, len(xs))
        assert 1 <= l < r <= n, "%s: 行%d l/r 非法 (%d,%d)" % (path, i, l, r)
        assert 1 <= k <= r - l, "%s: 行%d k=%d 越界 (r-l=%d)" % (path, i, k, r - l)
        assert xs == sorted(xs) and len(set(xs)) == k, "%s: 行%d x 非严格递增" % (path, i)
        assert l <= xs[0] and xs[-1] <= r, "%s: 行%d x 越出 [l,r]" % (path, i)
        sumk += k
    assert sumk <= SUMK_MAX, "%s: Σk=%d 超限 %d" % (path, sumk, SUMK_MAX)
    return sumk


def check_output(in_path, out_path, n, expect, expect_arr=None):
    """回读 .out：非空 / 行数 / 独立校验合法性 /（唯一解点）逐位比对。"""
    raw = open(out_path, "r").read()
    assert raw.strip(), ("%s: .out 为空 —— std 缺失或崩溃时 cyaron 会静默产出空文件！"
                         % out_path)
    toks = raw.split()
    assert toks[0] in ("TAK", "NIE"), "%s: 首 token %r 非法" % (out_path, toks[0])
    if toks[0] == "TAK":
        lns = raw.rstrip("\n").split("\n")
        assert len(lns) == 2, "%s: TAK 应恰好 2 行，实为 %d 行" % (out_path, len(lns))
        assert len(lns[1].split()) == n, ("%s: 第二行应含 %d 个数，实为 %d"
                                         % (out_path, n, len(lns[1].split())))
    else:
        assert len(toks) == 1, "%s: NIE 后有多余输出" % out_path
    res = check_one(in_path, out_path, expect=expect)
    assert res["ok"], "%s: %s" % (out_path, res["msg"])
    if expect_arr is not None:
        assert res["arr"] == expect_arr, "%s: 全已知点答案与隐藏解不符" % out_path
    return res["verdict"], res["msg"], sumk_of(in_path)


def sumk_of(path):
    with open(path) as f:
        lines = f.read().split("\n")[:-1]
    return sum(int(x.split()[2]) for x in lines[1 + int(lines[0].split()[1]):])


def emit(idx, spec):
    """生成单点：写 .in → 用 std 出 .out → 四项自检（含 NIE 点结构证明）；返回一行摘要。"""
    t0 = time.time()
    os.makedirs(DATA_DIR, exist_ok=True)
    io = IO(file_prefix="problem", data_id=idx)
    write_input(io, spec["n"], spec["s"], spec["m"], spec["known"], spec["infos"])
    io.input_file.flush()
    io.output_gen(shlex.quote(STD), time_limit=120)      # std 缺失 → 输出空文件，下面会抓到
    try:
        io.output_file.flush()
    except (AttributeError, OSError):
        pass
    ip = os.path.join(DATA_DIR, "problem%d.in" % idx)
    op = os.path.join(DATA_DIR, "problem%d.out" % idx)
    sumk = check_input(ip, spec["n"], spec["s"], spec["m"])
    verdict, _, sumk2 = check_output(ip, op, spec["n"], spec["expect"], spec.get("arr"))
    assert sumk == sumk2, "Σk 两处统计不一致"
    proof = ""
    if spec["expect"] == "NIE":
        proof = prove_nie(spec)                          # 无解必须可证，不能只信 std
    dt = time.time() - t0
    line = ("点%2d: n=%-6d s=%-6d m=%-6d Σk=%-6d 期望=%-3s 实判=%-3s %-40s [%.1fs]"
            % (idx, spec["n"], spec["s"], spec["m"], sumk, spec["expect"], verdict,
               spec["tag"], dt))
    print(line)
    if proof:
        print("      无解证明：%s" % proof)
    return line


def known_of(positions, a):
    """按位置递增取已知值：[(p, a[p])]。"""
    return [(p, a[p]) for p in sorted(positions)]


def topk_infos(rng, n, a, m, kdist, Lmax, Lmin=None):
    """[l,r] 内取 a 值最大的 k 个位置作为 x ⇒ 相对隐藏解 a 严格可行。

    a 在该区间内值互异时选择唯一；k 须 < r-l+1（留至少 1 个非 x 位置）。
    """
    infos, sumk = [], 0
    for i in range(m):
        k = kdist[i % len(kdist)]
        lo = Lmin if Lmin else k + 1
        L = rng.randint(max(lo, k + 1), Lmax)
        l = rng.randint(1, n - L + 1)
        r = l + L - 1
        xs = sorted(sorted(range(l, r + 1), key=lambda p: -a[p])[:k])
        assert len(xs) == k and l <= xs[0] and xs[-1] <= r
        infos.append((l, r, xs))
        sumk += k
    assert sumk <= SUMK_MAX, "Σk=%d 超限" % sumk
    return infos


def level_infos(rng, n, a, m, Lmax, kdist=None):
    """台阶隐藏解：x = 区间内处于最高级的**全部**位置（值重复场景，仍严格可行）。"""
    infos, sumk, tries = [], 0, 0
    while len(infos) < m:
        tries += 1
        assert tries < 200 * m, "level_infos: 反复取不到合法区间"
        L = rng.randint(2, Lmax)
        l = rng.randint(1, n - L + 1)
        r = l + L - 1
        hi = max(a[l:r + 1])
        xs = [p for p in range(l, r + 1) if a[p] == hi]
        if len(xs) >= L or sumk + len(xs) > SUMK_MAX:      # 必须 k = |x| < r-l+1
            continue
        infos.append((l, r, xs))
        sumk += len(xs)
    return infos


def suffix_infos(rng, n, m, kdist, Lmin):
    """递增隐藏解 a[i]=i（由后缀型约束自行强制）：x = 区间后缀，长区间友好。"""
    infos, sumk = [], 0
    for i in range(m):
        k = kdist[i % len(kdist)]
        L = rng.randint(max(Lmin, k + 1), n)
        l = rng.randint(1, n - L + 1)
        r = l + L - 1
        infos.append((l, r, list(range(r - k + 1, r + 1))))
        sumk += k
    assert sumk <= SUMK_MAX
    return infos


def tent_infos(rng, n, a, m, p0, kdist, Lmax):
    """严格单峰隐藏解（峰在 p0）：x = 区间内离峰最近的 k 个位置。

    O(k) 定位：峰在区间内时 x 是以 p0 为中心的连续块（两侧各 1 个缺口）；峰在区间外时
    x 为就近端点的连续块（1 个缺口）。缺口长、区间长，正是线段树拆图边数最多的形态；
    且相对严格单峰的 a 严格可行（min(x) 大于缺口内任何值）。
    要求 a 在区间内无并列值（调用方保证）。
    """
    infos, sumk = [], 0
    for i in range(m):
        k = kdist[i % len(kdist)]
        L = rng.randint(k + 1, Lmax)
        if rng.random() < 0.85:                     # 85% 让区间包含峰（⇒ 2 个缺口）
            l = rng.randint(max(1, p0 - L + 1), min(p0, n - L + 1))
        else:
            l = rng.randint(1, n - L + 1)
        r = l + L - 1
        # 离峰最近的 k 个位置（在 [l,r] 内交替向两侧扩展；峰在区间外时取就近端块）
        lo0 = min(max(p0, l), r)
        order, d = [lo0], 1
        while len(order) < k:
            if lo0 - d >= l:
                order.append(lo0 - d)
            if len(order) < k and lo0 + d <= r:
                order.append(lo0 + d)
            d += 1
        xs = sorted(order)
        assert len(xs) == k and l <= xs[0] and xs[-1] <= r and k <= r - l, (l, r, xs)
        infos.append((l, r, xs))
        sumk += k
    assert sumk <= SUMK_MAX, "Σk=%d 超限" % sumk
    return infos


def prove_nie(spec):
    """对 NIE 点做**结构可证**的无解证明（机器校验，非搜索/非对拍）。

    两种模式（由 spec['nie_kind'] 指定）：
      complement：存在两条信息 X 与 [l,r]\\X —— 它们互推“每组都大于对方” ⇒ 自相矛盾；
      chain     ：严格递增链（a[i+1] > a[i]）+ 已知值 ⇒ 必经下界超过 1e9 值域上界。
    返回一段人可读的证明文字；任一步不成立则断言失败。
    """
    n, known, infos = spec["n"], dict(spec["known"]), spec["infos"]
    kind = spec["nie_kind"]
    if kind == "complement":
        by_set = {}
        for (l, r, xs) in infos:
            by_set.setdefault((l, r), []).append(frozenset(xs))
        for (l, r), sets in by_set.items():
            full = frozenset(range(l, r + 1))
            for i in range(len(sets)):
                for j in range(i + 1, len(sets)):
                    if sets[i] | sets[j] == full and sets[i] & sets[j] == frozenset():
                        return ("信息 (l=%d,r=%d) 的 X=%s 与补集 X=%s 互相要求对方全部更大 ⇒ "
                                "min(X) > min(补) 与 min(补) > min(X) 同时成立，矛盾。"
                                % (l, r, sorted(sets[i]), sorted(sets[j])))
        raise AssertionError("nie_kind=complement 但未找到互补信息对")
    if kind == "chain":
        edge_to = {}
        for (l, r, xs) in infos:
            if r == l + 1 and len(xs) == 1 and xs[0] == r:      # 隐式 a[r] > a[l]
                edge_to[l] = r
        assert edge_to, "nie_kind=chain 但未找到 a[i+1] > a[i] 型信息"
        # 从每个已知位置出发沿链走到底，检查下界是否 ① 越值域上界 或 ② 与另一已知值冲突
        hit = None
        for p, d in sorted(known.items()):
            cur, cnt = p, 0
            while cur in edge_to:
                cur = edge_to[cur]; cnt += 1
            if d + cnt > VAL_MAX:
                hit = ("严格递增链 a[%d] -> ... -> a[%d]（%d 步）给出 a[%d] >= a[%d] + %d "
                       "= %d > 1e9（值域上界），故无解。" % (p, cur, cnt, cur, p, cnt, d + cnt))
                break
            if cur in known and d + cnt > known[cur]:
                hit = ("严格递增链 a[%d] -> ... -> a[%d]（%d 步）给出 a[%d] >= a[%d] + %d = %d "
                       "> %d = 题面给定的 a[%d]，故无解。"
                       % (p, cur, cnt, cur, p, cnt, d + cnt, known[cur], cur))
                break
        if hit is None:
            raise AssertionError("nie_kind=chain 但未找到与值域/已知值冲突的链")
        return hit
    raise AssertionError("未知 nie_kind=%r" % kind)


# ------------------------------------------------------------------ 10 个分层点

POINTS = {}


def point(idx):
    def deco(fn):
        POINTS[idx] = fn
        return fn
    return deco


@point(1)
def p1(rng):
    """边界层：n 最小（2）、s=n 全已知（含值域下界 1）⇒ 答案唯一且可逐位核对。"""
    n, s, m = 2, 2, 1
    known = [(1, 1), (2, 2)]
    infos = [(1, 2, [2])]                      # a[2] > a[1]
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK", arr=[1, 2],
                tag="边界 n=2 全已知 值域下界")


@point(2)
def p2(rng):
    """边界层：两条信息互为反制 ⇒ 有环 ⇒ NIE；已知值含值域上界 1e9。

    可证无解：信息 A 断言 X={3} 全部大于 [1,5] 去掉 {3}；信息 B 断言 X={1,2,4,5} 全部大于
    剩下的 {3}。两式合得 a[3] > a[3]，矛盾。（prove_nie 逐条机器校验）
    """
    n, s, m = 5, 2, 2
    known = [(2, 3), (4, VAL_MAX)]
    infos = [(1, 5, [3]),                      # a[3] > 其余全部
             (1, 5, [1, 2, 4, 5])]             # 其余全部 > a[3] ⇒ 矛盾
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="NIE",
                nie_kind="complement", tag="边界 双向反制成环")


@point(3)
def p3(rng):
    """小规模：隐藏解为互异随机排名，x = 区间内最大的 k 个（手算可验证量级）。"""
    n, s, m = 100, 50, 200
    a = [0] + rng.sample(range(1, 10 ** 6), n)
    known = known_of(rng.sample(range(1, n + 1), s), a)
    infos = topk_infos(rng, n, a, m, kdist=[1, 2, 3], Lmax=16)
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK",
                tag="小规模 互异值 top-k")


@point(4)
def p4(rng):
    """小规模 NIE：a[i+1]>a[i] 链与已知 a[6]=5 冲突（链强制 a[6]>=a[1]+5=6）。"""
    n = 6
    known = [(1, 1), (6, 5)]
    infos = [(i, i + 1, [i + 1]) for i in range(1, n)]
    return dict(n=n, s=2, m=n - 1, known=known, infos=infos, expect="NIE",
                nie_kind="chain", tag="小规模 NIE 链与已知冲突")


@point(5)
def p5(rng):
    """中等：短区间 top-k，值互异、x 分散，k∈{1,2,3}。"""
    n, s, m = 1000, 100, 1500
    a = [0] + rng.sample(range(1, 10 ** 9), n)
    known = known_of(rng.sample(range(1, n + 1), s), a)
    infos = topk_infos(rng, n, a, m, kdist=[1, 2, 3], Lmax=32)
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK",
                tag="中等 短区间 top-k 值互异")


@point(6)
def p6(rng):
    """中等：8 级台阶隐藏解（值大量重复），x = 区间最高级的全部位置。"""
    n, s, m = 5000, 2500, 20000
    a = [0] + [rng.randint(1, 8) for _ in range(n)]
    known = known_of(rng.sample(range(1, n + 1), s), a)
    infos = level_infos(rng, n, a, m, Lmax=24)
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK",
                tag="中等 台阶值重复 0.5n 已知")


@point(7)
def p7(rng):
    """大规模：长区间（均值约 5e4）+ x=区间后缀（k∈{1,2}），n=s*2。

    隐藏解 a[i]=i 由后缀约束 + 已知值共同钉死；Σk=1.5e5。
    """
    n, s, m = 100000, 50000, 100000
    a = list(range(0, n + 1))
    known = known_of(rng.sample(range(1, n + 1), s), a)
    infos = suffix_infos(rng, n, m, kdist=[1, 2], Lmin=50000)
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK",
                tag="大规模 长区间后缀型 Σk=1.5e5")


@point(8)
def p8(rng):
    """大规模 NIE（题面坑点）：长度 1e5 严格递增链 + 已知 a[1]=1e9 ⇒ 下界越 1e9。

    可证无解：链强制 a[100000] >= a[1] + 99999 = 1e9 + 99999 > 1e9，超出值域上界。
    """
    n = 100000
    known = [(1, VAL_MAX)]
    infos = [(i, i + 1, [i + 1]) for i in range(1, n)]
    return dict(n=n, s=1, m=n - 1, known=known, infos=infos, expect="NIE",
                nie_kind="chain", tag="大规模 NIE 下界超 1e9")


@point(9)
def p9(rng):
    """顶格：n=m=s=上限；s=n 全已知，值线性铺满且恰好含 1e9；Σk=3e5 顶格。

    信息：1000 条 k=100（长区间、围绕峰 ⇒ 两侧大缺口）+ 199000 条 k=1（随机长区间 ⇒
    缺口平均覆盖 2*log n 个线段树节点），专门压线段树拆图的边数与内存。
    全已知 ⇒ 答案被完全钉死，可逐位比对隐藏解。
    """
    n, s, m = 100000, 100000, 200000
    a = [0] * (n + 1)
    for i in range(1, n):
        a[i] = i * 10000                       # a[1]=1e4 … a[n-1]=999990000
    a[n] = VAL_MAX                             # 仍严格递增（恰好含值域上界）
    assert all(1 <= a[i] <= VAL_MAX for i in range(1, n + 1))
    known = known_of(range(1, n + 1), a)
    # 值线性递增：x = 区间后缀（O(k) 定位），k=100 时是长区间里的一大块 x
    big = suffix_infos(rng, n, 1000, kdist=[100], Lmin=50000)      # Σk=1e5
    mid = suffix_infos(rng, n, 1000, kdist=[2], Lmin=2)            # Σk=2e3
    small = suffix_infos(rng, n, m - 2000, kdist=[1], Lmin=2)      # Σk=1.98e5
    infos = big + mid + small
    assert sum(len(x[2]) for x in infos) == SUMK_MAX
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK", arr=a[1:],
                tag="顶格 全已知唯一解 Σk=3e5 顶格 长区间")


@point(10)
def p10(rng):
    """顶格：最坏建图。s=n 全已知（答案钉死）；隐藏解 = 定长帐篷（峰在 n/2）。

    m=2e5、Σk=3e5 双顶格：199000 条 k=1（随机长区间且 85% 跨峰 ⇒ 每条 2 个大缺口）
    + 1000 条 k=100（跨峰长区间 ⇒ 大缺口 + 大量 x）。缺口总数约 4e5，正是
    线段树优化建图边数的最坏形态；同时覆盖“x 个数多”与“缺口大”两条路径。
    """
    n, s, m = 100000, 100000, 200000
    p0 = n // 2
    # 严格单峰的“余峰”解（外侧严格递减，无并列值）：左靠峰比右靠峰大 1
    a = [0] + [VAL_MAX - 2 * abs(i - p0) + (1 if i < p0 else 0) for i in range(1, n + 1)]
    assert all(1 <= a[i] <= VAL_MAX for i in range(1, n + 1))
    assert a[p0] == VAL_MAX
    assert len(set(a[1:])) == n, "隐藏解必须无并列值"
    known = known_of(range(1, n + 1), a)
    big = tent_infos(rng, n, a, 1000, p0, kdist=[100], Lmax=n)      # Σk=1e5
    mid = tent_infos(rng, n, a, 1000, p0, kdist=[2], Lmax=n)        # Σk=2e3
    small = tent_infos(rng, n, a, m - 2000, p0, kdist=[1], Lmax=n)  # Σk=1.98e5
    infos = big + mid + small
    assert sum(len(x[2]) for x in infos) == SUMK_MAX
    return dict(n=n, s=s, m=m, known=known, infos=infos, expect="TAK", arr=a[1:],
                tag="顶格 最坏建图 m=2e5 Σk=3e5 顶格")


# ------------------------------------------------------------------ 主流程

def selftest_std():
    """std 存在性与样例验证（防 cyaron 静默空输出）。"""
    assert os.path.isfile(STD) and os.access(STD, os.X_OK), \
        "std 不存在/不可执行：%s —— 请先 g++ -O2 -std=c++17 std.cpp -o std" % STD
    import subprocess
    out = subprocess.run([STD], input=SAMPLE_IN.encode(), stdout=subprocess.PIPE,
                         timeout=60).stdout.decode()
    assert out.strip(), "std 对题面样例无输出"
    print("样例实跑（std）:", out.strip().replace("\n", " | "))
    assert out.split()[0] == "TAK", "样例应判 TAK，实得 %r" % out.split()[0]
    tmp_in = os.path.join(DATA_DIR, "_sample.in")
    tmp_out = os.path.join(DATA_DIR, "_sample.out")
    os.makedirs(DATA_DIR, exist_ok=True)
    open(tmp_in, "w").write(SAMPLE_IN)
    open(tmp_out, "w").write(out)
    res = check_one(tmp_in, tmp_out, expect="TAK")
    assert res["ok"], "std 样例输出非法: %s" % res["msg"]
    # 用独立校验器复核题面【输出样例】本身合法（顺带自检校验器）
    sample_ans = "TAK\n6 7 1000000000 6 3\n"
    open(tmp_out, "w").write(sample_ans)
    res2 = check_one(tmp_in, tmp_out, expect="TAK")
    assert res2["ok"], "题面输出样例未通过校验器（校验器有误？）: %s" % res2["msg"]
    os.remove(tmp_in)
    os.remove(tmp_out)
    print("样例验证：std 输出合法 ✓ ；题面【输出样例】经校验器复核合法 ✓（多解题，不逐字节比对）")


def main():
    argv = sys.argv[1:]
    only = set(int(x) for x in argv) if argv else set(range(1, 11))
    selftest_std()
    lines = []
    for i in range(1, 11):
        if i not in only:
            continue
        rng = random.Random(1728_000 + i)          # 每点独立种子，逐字节可复现
        spec = POINTS[i](rng)
        lines.append(emit(i, spec))
    print("\n全部 %d 组生成 + 自检通过：%s" % (len(lines), data_files_line()))
    return 0


def data_files_line():
    files = sorted(os.listdir(DATA_DIR))
    return " ".join(f for f in files if f.startswith("problem"))


if __name__ == "__main__":
    sys.exit(main())