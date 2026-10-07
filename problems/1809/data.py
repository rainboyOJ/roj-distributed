#!/usr/bin/env python3
# 一本通 1809《日食》测试数据生成器（纯 Python + subprocess，不使用 cyaron）
#
# 用法：cd .ybt-import/staging/1809 && python3 data.py
#   1) 把 std.cpp 编译到临时目录（结束即清理，工作目录不留编译产物）；
#   2) 生成 data/problem1.in .. problem10.in；
#   3) 用 subprocess 显式调用 std 二进制产出 data/problem1.out .. problem10.out
#      （不用 cyaron 的 output_gen，避免写缓冲不 flush 产出 0 字节 .out）；
#   4) 断言：.out 非空、行数 == ΣQ、答案 ∈ [0, R-L+1]、L==R 时答案 ∈ {0,1}，
#      并对若干**手算闭式可验证**的数据点逐条比对（见各 test 的 check 注释）。
#
# 题面数据范围（content.md）：T≤2；1≤Q≤2×10^4；1≤L≤R≤10^18；
#   0≤A,B,X,Y,Z,C<P≤10007 且 P 为质数。
#   本生成器全部按题面上限构造（P 最大取 10007，Q 最大取 2×10^4，R 最大取 10^18），
#   不越界。
#
# 分层（10 组）：
#   1  边界最小：P=2、T=1、Q 少、退化递推，答案含 0 与 10^18 量级，闭式可验
#   2  边界/退化：常数序列（Y=0, X=1, Z=0），闭式可验
#   3  小规模（子任务1 R≤10^7）：Y≠0 随机 + Y=0「答案为 0」极端，闭式可验
#   4  子任务2/3（P≤1000 / Q=1）：Q=1 且 L=1,R=10^18；Y=0 等差数列闭式可验
#   5  中等：P=5003、Y≠0 近满周期 lam=25030008、Q=2×10^4、R≤10^18
#   6  大：P=10007、Y≠0 满周期 lam=100140048(=P^2-1)、Q=2×10^4
#   7  顶格：T=2、P=10007、两个满周期点、Q=2×10^4、R=10^18
#   8  Y=0 分支大：P=10007、X=1,Z=1（mu=0,lam=P，闭式可验）与 X=2 混合
#   9  顶格最重：T=2、两个满周期点（合计约 2×10^8 步），时间上限压力点
#   10 混合边界：周期 2 的 Y≠0 点（闭式可验）+ 尾部常数点（闭式可验），L=R=10^18 等极值
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD_SRC = os.path.join(HERE, "std.cpp")
MAXR = 10 ** 18
MAXP = 10007
MAXQ = 20000
MAXT = 2

# ----------------------------------------------------------------------------
# 手算闭式公式（独立于 std，用于校验特定数据点）
# ----------------------------------------------------------------------------


def cf_tail_const(L, R, A, B, C, tail):
    """S1=A, S2=B, S_i=tail (i>=3)：统计 [L,R] 中 S_i==C 的个数。"""
    cnt = 0
    if L <= 1 <= R and A == C:
        cnt += 1
    if L <= 2 <= R and B == C:
        cnt += 1
    if R >= 3 and tail == C:
        cnt += R - max(L, 3) + 1
    return cnt


def cf_period2(L, R, A, B, C):
    """S_i = A (i 奇), B (i 偶)：统计 [L,R] 中 S_i==C 的个数。"""
    cnt = 0
    if C == A:
        cnt += (R + 1) // 2 - L // 2                 # [L,R] 中奇数个数
    if C == B:
        cnt += R // 2 - (L - 1) // 2                 # [L,R] 中偶数个数
    return cnt


def cf_ap_plus1(L, R, A, B, P, C):
    """Y=0, X=1, Z=1：S1=A；i>=2 时 S_i = (B + i - 2) mod P。
    统计 [L,R] 中 S_i==C 的个数。"""
    cnt = 0
    if L <= 1 <= R and A == C:
        cnt += 1
    lo, hi = max(L, 2), R
    if hi >= lo:
        t0, t1 = lo - 2, hi - 2                      # i = t + 2
        r = (C - B) % P
        if t1 >= r:
            k = r if r >= t0 else r + ((t0 - r + P - 1) // P) * P
            if k <= t1:
                cnt += (t1 - k) // P + 1
    return cnt


# ----------------------------------------------------------------------------
# 数据描述
# ----------------------------------------------------------------------------


class Test:
    def __init__(self, A, B, X, Y, Z, P, C, queries, check=None, note=""):
        self.A, self.B, self.X, self.Y, self.Z, self.P, self.C = A, B, X, Y, Z, P, C
        self.queries = queries
        self.check = check
        self.note = note
        self.Q = len(queries)


def qrand(rng, q, rmax=MAXR):
    """随机区间 [L,R]，1<=L<=R<=rmax。"""
    out = []
    for _ in range(q):
        L = rng.randint(1, rmax)
        R = rng.randint(L, rmax)
        out.append((L, R))
    return out


# 满周期参数（由 Python 端 polylog 求阶得到 lam=P^2-1，见 gen-report.md）
FULL_10007 = [
    (1495, 8700, 9063, 3061, 5814, 42),        # lam=100140048
    (9978, 2123, 9925, 5324, 8332, 74),        # lam=100140048
    (9951, 2501, 3600, 7570, 90, 3771),        # lam=100140048
    (9950, 6874, 4596, 1896, 4804, 7614),      # lam=100140048
    (9915, 8, 7230, 947, 9661, 391),           # lam=100140048
]
FULL_5003 = (5001, 3275, 4192, 2812, 3857, 3804, 5003)   # lam=25030008


def build():
    """返回 {1..10: [Test, ...]}。"""
    probs = {}

    # ---- 点 1：边界最小 -------------------------------------------------
    # P=2（最小质数），T=1，Y=0 且 X=0,Z=0 => S1=1,S2=0,S_i=0 (i>=3)
    # 闭式：C=0 时答案 = (R-L+1) - [L<=1<=R]
    A, B, X, Y, Z, P, C = 1, 0, 0, 0, 0, 2, 0
    qs = [(1, 1), (1, 2), (2, 2), (3, MAXR), (1, MAXR)]
    probs[1] = [Test(A, B, X, Y, Z, P, C, qs,
                     check=lambda L, R, ans, A=A, B=B, C=C: cf_tail_const(L, R, A, B, C, 0),
                     note="最小 P/退化递推，答案 0 与 10^18 量级")]

    # ---- 点 2：边界/退化（常数序列，闭式可验） ---------------------------
    rng = random.Random(180902)
    t1 = Test(1, 1, 1, 0, 0, 2, 1, [(1, 1), (1, MAXR), (MAXR, MAXR), (5, 10)],
              check=lambda L, R, ans: R - L + 1,   # S_i 恒为 C
              note="S_i 恒为 1==C，答案 = R-L+1")
    t2 = Test(2, 0, 1, 0, 0, 3, 0,
              [(1, 1), (1, 2), (2, 2), (1, MAXR), (MAXR, MAXR), (7, MAXR)],
              check=lambda L, R, ans, A=2, B=0, C=0: cf_tail_const(L, R, A, B, C, 0),
              note="S1=2,S_i=0 (i>=2)，闭式可验")
    probs[2] = [t1, t2]

    # ---- 点 3：小规模（子任务1：R<=10^7） -------------------------------
    A, B, X, Y, Z, C = FULL_10007[1]
    t1 = Test(A, B, X, Y, Z, MAXP, C, qrand(rng, MAXQ, 10 ** 7),
              note="Y!=0 随机小 R（R<=10^7）")
    # Y=0,X=0,Z=0,B=5,C=7 => S1=3,S2=5,S_i=0 (i>=3)，C=7 永不出现 => 全 0
    t2 = Test(3, 5, 0, 0, 0, 997, 7, qrand(rng, MAXQ, 10 ** 7),
              check=lambda L, R, ans: 0,           # C 永不出现
              note="答案为 0 极端：C 永不出现")
    probs[3] = [t1, t2]

    # ---- 点 4：子任务2/3（P<=1000 / Q=1） ------------------------------
    # P=997（质数），Y!=0 满周期 lam=994008=P^2-1，Q=1，L=1,R=10^18
    t1 = Test(316, 530, 72, 309, 423, 997, 635, [(1, MAXR)],
              note="P<=1000 且 Q=1，L=1,R=10^18（满周期 lam=P^2-1）")
    # P=991，Y=0,X=1,Z=1 等差数列（v_t=B+t mod P），Q=1，闭式可验
    t2 = Test(123, 603, 1, 0, 1, 991, 500, [(1, MAXR)],
              check=lambda L, R, ans: cf_ap_plus1(L, R, 123, 603, 991, 500),
              note="Y=0,X=1,Z=1 等差数列，Q=1，闭式可验")
    probs[4] = [t1, t2]

    # ---- 点 5：中等规模（P=5003，近满周期） -----------------------------
    A, B, X, Y, Z, C, P = FULL_5003
    probs[5] = [Test(A, B, X, Y, Z, P, C, qrand(rng, MAXQ),
                     note="P=5003，lam=25030008≈P^2，Q=2×10^4")]

    # ---- 点 6：大规模（P=10007，满周期） --------------------------------
    A, B, X, Y, Z, C = FULL_10007[2]
    probs[6] = [Test(A, B, X, Y, Z, MAXP, C, qrand(rng, MAXQ),
                     note="P=10007，lam=100140048=P^2-1")]

    # ---- 点 7：顶格（T=2，两个满周期点，R=10^18） ----------------------
    qs7 = []
    for _ in range(MAXQ - 3):
        L = rng.randint(1, MAXR)
        qs7.append((L, MAXR))
    qs7 += [(1, MAXR), (MAXR, MAXR), (1, 1)]
    t7a = Test(FULL_10007[3][0], FULL_10007[3][1], FULL_10007[3][2],
               FULL_10007[3][3], FULL_10007[3][4], MAXP, FULL_10007[3][5], qs7,
               note="R 全部取 10^18 顶格")
    t7b = Test(FULL_10007[4][0], FULL_10007[4][1], FULL_10007[4][2],
               FULL_10007[4][3], FULL_10007[4][4], MAXP, FULL_10007[4][5],
               qs7[:], note="R 全部取 10^18 顶格")
    probs[7] = [t7a, t7b]

    # ---- 点 8：Y=0 分支大（P=10007） -----------------------------------
    # 8-1: X=1,Z=1 => v_t=B+t mod P（mu=0,lam=P），闭式可验
    t8a = Test(123, 4567, 1, 0, 1, MAXP, 5000, qrand(rng, MAXQ),
               check=lambda L, R, ans: cf_ap_plus1(L, R, 123, 4567, MAXP, 5000),
               note="Y=0,X=1,Z=1 长周期 P，闭式可验")
    # 8-2: X=2,Z=1234 => 仿射迭代有前导段+循环，无闭式
    t8b = Test(1, 2, 2, 0, 1234, MAXP, 8773, qrand(rng, MAXQ),
               note="Y=0,X=2,Z=1234 一般仿射迭代")
    probs[8] = [t8a, t8b]

    # ---- 点 9：顶格最重（T=2，两个满周期点，Q 顶格，R 顶格） ------------
    t9a = Test(FULL_10007[0][0], FULL_10007[0][1], FULL_10007[0][2],
               FULL_10007[0][3], FULL_10007[0][4], MAXP, FULL_10007[0][5],
               qrand(rng, MAXQ), note="满周期 lam=P^2-1，约 1e8 步")
    t9b = Test(FULL_10007[1][0], FULL_10007[1][1], FULL_10007[1][2],
               FULL_10007[1][3], FULL_10007[1][4], MAXP, FULL_10007[1][5],
               qrand(rng, MAXQ), note="满周期 lam=P^2-1，约 1e8 步")
    probs[9] = [t9a, t9b]

    # ---- 点 10：混合边界（周期 2 / 尾部常数，均闭式可验） ---------------
    # 10-1: Y=1,X=0,Z=0 => S_i = A (奇), B (偶)，闭式可验
    qs10 = qrand(rng, MAXQ - 5)
    qs10 += [(1, 1), (1, 2), (2, 2), (MAXR, MAXR), (MAXR - 1, MAXR)]
    t10a = Test(777, 1111, 0, 1, 0, MAXP, 777, qs10,
                check=lambda L, R, ans: cf_period2(L, R, 777, 1111, 777),
                note="Y!=0 周期 2（闭式），含 L=R=10^18 极值")
    # 10-2: Y=0,X=0,Z=11 => S1=3,S2=7,S_i=11 (i>=3)，闭式可验
    t10b = Test(3, 7, 0, 0, 11, MAXP, 11, qs10[:],
                check=lambda L, R, ans: cf_tail_const(L, R, 3, 7, 11, 11),
                note="尾部常数 11（闭式），含极值")
    probs[10] = [t10a, t10b]

    return probs


# ----------------------------------------------------------------------------
# 约束校验 / 输出 / 断言
# ----------------------------------------------------------------------------


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def validate_input(text, expect_tests):
    """按题面范围逐项校验 .in（同时确认 token 数与 T/Q 自洽）。"""
    tok = text.split()
    pos = 0
    T = int(tok[pos]); pos += 1
    assert 1 <= T <= MAXT, f"T={T} 越界"
    assert T == expect_tests, f"T={T} != 预期 {expect_tests}"
    total_q = 0
    for _ in range(T):
        vals = [int(tok[pos + i]) for i in range(8)]; pos += 8
        A, B, X, Y, Z, P, C, Q = vals
        assert 1 <= Q <= MAXQ, f"Q={Q} 越界"
        assert 2 <= P <= MAXP and is_prime(P), f"P={P} 非 [2,10007] 内质数"
        for name, v in (("A", A), ("B", B), ("X", X), ("Y", Y), ("Z", Z), ("C", C)):
            assert 0 <= v < P, f"{name}={v} 不满足 0<=v<P={P}"
        for _ in range(Q):
            L, R = int(tok[pos]), int(tok[pos + 1]); pos += 2
            assert 1 <= L <= R <= MAXR, f"询问 {L} {R} 越界"
        total_q += Q
    assert pos == len(tok), "存在多余 token"
    return T, total_q


def main():
    probs = build()
    assert sorted(probs) == list(range(1, 11))
    os.makedirs(DATA_DIR, exist_ok=True)

    tmp = tempfile.mkdtemp(prefix="std1809_")
    binpath = os.path.join(tmp, "std1809")
    try:
        print("[compile] g++ -O2 -std=c++17 std.cpp -o <tmp>/std1809")
        cp = subprocess.run(["g++", "-O2", "-std=c++17", "-o", binpath, STD_SRC],
                            capture_output=True, text=True)
        if cp.returncode != 0:
            print(cp.stderr)
            raise SystemExit("std.cpp 编译失败")
        assert os.path.exists(binpath) and os.path.getsize(binpath) > 0

        print(f"{'点':>3} {'T':>2} {'ΣQ':>6} {'in字节':>9} {'out字节':>9} "
              f"{'std耗时':>8} {'答案最大值':>14}  说明")
        for i in range(1, 11):
            tests = probs[i]
            lines = [str(len(tests))]
            for t in tests:
                lines.append(" ".join(map(str, [t.A, t.B, t.X, t.Y, t.Z, t.P, t.C, t.Q])))
                lines += [f"{L} {R}" for (L, R) in t.queries]
            in_text = "\n".join(lines) + "\n"
            T, total_q = validate_input(in_text, len(tests))

            in_path = os.path.join(DATA_DIR, f"problem{i}.in")
            out_path = os.path.join(DATA_DIR, f"problem{i}.out")
            with open(in_path, "w") as f:
                f.write(in_text)

            with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
                t0 = time.time()
                rp = subprocess.run(["nice", "-n", "19", "timeout", "120", binpath],
                                    stdin=fin, stdout=fout, stderr=subprocess.PIPE,
                                    timeout=150)
                elapsed = time.time() - t0
            assert rp.returncode == 0, f"点{i}: std 退出码 {rp.returncode} {rp.stderr[:200]}"

            raw = open(out_path, "rb").read()
            assert len(raw) > 0, f"点{i}: .out 为空（0 字节）"
            text = raw.decode()
            assert text.endswith("\n"), f"点{i}: .out 末行缺换行"
            out_lines = text.split("\n")[:-1]
            assert len(out_lines) == total_q, \
                f"点{i}: .out 行数 {len(out_lines)} != ΣQ {total_q}"
            assert all(ln.strip().lstrip('-').isdigit() for ln in out_lines), f"点{i}: 非整数行"

            # 逐查询断言：范围合法 + L==R 时 ∈{0,1} + 闭式数据点比对
            k = 0
            checked = 0
            amax = 0
            for t in tests:
                for (L, R) in t.queries:
                    ans = int(out_lines[k]); k += 1
                    assert 0 <= ans <= R - L + 1, \
                        f"点{i} 询问({L},{R}) 答案 {ans} 不在 [0,R-L+1]"
                    if L == R:
                        assert ans in (0, 1), f"点{i} 询问({L},{R}) 单点答案 {ans} 非 0/1"
                    if t.check is not None:
                        exp = t.check(L, R, ans)
                        assert ans == exp, \
                            f"点{i} 闭式校验失败 ({L},{R}): std={ans} 闭式={exp}"
                        checked += 1
                    amax = max(amax, ans)
            note = tests[0].note
            print(f"{i:>3} {T:>2} {total_q:>6} {len(in_text):>9} {len(raw):>9} "
                  f"{elapsed:>7.2f}s {amax:>14}  {note}"
                  + (f" [闭式校验 {checked} 条]" if checked else ""))
        print("\n全部 10 组：.out 非空、行数=ΣQ、答案范围合法、闭式数据点全部相符 ✅")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"[clean] 已删除临时编译产物 {tmp}")


if __name__ == "__main__":
    sys.exit(main())
