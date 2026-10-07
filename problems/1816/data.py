#!/usr/bin/env python3
# 一本通 1816《取石子》分层数据生成器
#
# 题面范围：t<=1000, n<=1000, 1<=a<=b<=1e9, 1<=x_i<=1e9。
# 分层设计（10 组，文件名 problem1..problem10）：
#   点1  边界：n=1（Subtask 1），含 a=b=1e9、x=1e9 等极值，可手算
#   点2  Subtask 2：a=b，x 覆盖 <a / =a / (a,2a) / 2a / >2a
#   点3  Subtask 3：a=1，b 从 1 到 1e9
#   点4  Subtask 4：x_i<=1000（a,b 可到 1e9，含全部死堆的情形）
#   点5  Subtask 5：a,b<=1000，x 可到 1e9
#   点6  小规模手算（无特殊限制，n<=5, a,b<=20, x<=60）
#   点7  中等：t=100, n<=300，半数"构造非平凡局面"（无立即胜堆，XOR 定胜负）
#   点8  大：t=300, n=1000，半数构造
#   点9  顶格边界构造：t=1000, n=1000，x 取 a-1/a/b/b+1/M-1/M/M+1/qM+r 等关键点
#   点10 顶格随机：t=1000, n=1000，a,b,x 全域随机 + 构造 Bob/Alice 局面
#
# 生成方式说明（规避 cyaron output_gen 缓冲坑）：
#   .in 用 Python 直接写文件（写后 close+fsync），.out 用 subprocess 显式执行 ./std
#   重定向生成；随后断言 .out 行数 == t、每行属于 {Alice,Bob}，
#   并把 .in 重新解析一遍用 Python 版同一公式复算比对，确保数据文件无截断/错位。
import os
import random
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD = os.path.join(HERE, "std")
LIM = 10 ** 9


# ---------- 题解公式（与 std.cpp 同一算法，用于构造与复算断言） ----------
def grundy(x, a, b):
    """返回 Grundy 值；x in [a,b] 时返回 None（立即胜，不属于化简后游戏）。"""
    M = a + b
    if a <= x <= b:
        return None
    if x < a:
        return 0
    if x < M:
        return 1
    r = x % M
    if a == 1:
        return r
    if r < a:
        return 0
    if r >= M - a:
        return 1
    return 2 + (r - a) // a


def solve(a, b, xs):
    M = a + b
    xr = 0
    for x in xs:
        if a <= x <= b:
            return True
        if x < a:
            continue
        if x < M:
            xr ^= 1
            continue
        r = x % M
        if a == 1:
            xr ^= r
        elif r < a:
            pass
        elif r >= M - a:
            xr ^= 1
        else:
            xr ^= 2 + (r - a) // a
    return xr != 0


def clamp(x):
    return max(1, min(LIM, x))


def key_points(a, b, rng, cap=12):
    """a,b 固定时取一圈关键 x（边界值）。"""
    M = a + b
    pts = {1, a - 1, a, a + 1, b - 1, b, b + 1, M - 1, M, M + 1, 2 * M, 2 * M + 1,
           LIM, LIM - 1, rng.randint(1, LIM)}
    for r in (0, a - 1, a, a + 1, M - a - 1, M - a, M - 1):
        if r < 0 or r >= M:
            continue
        qmax = LIM // M
        for q in {0, 1, 2, max(0, qmax - 1), qmax}:
            pts.add(M * q + r)
    pts = sorted(clamp(p) for p in pts)
    rng.shuffle(pts)
    return pts[:cap]


# ---------- 非平凡局面构造（无立即胜堆，XOR 决定胜负） ----------
def cand_pool(a, b, rng, xmax=LIM, extra=60):
    M = a + b
    xs = {1, a - 1, a, b, b + 1, M - 1, M, M + 1, xmax - 1, xmax}
    qs = {0, 1, 2, 3}
    if M <= xmax:
        qs.add(xmax // M)
    for q in qs:
        for r in {0, 1, a - 1, a, a + 1, 2 * a, M // 2, M - a - 1, M - a, M - 1}:
            if 0 <= r < M:
                xs.add(q * M + r)
    for _ in range(extra):
        xs.add(rng.randint(1, xmax))
    pool = []
    for x in xs:
        if 1 <= x <= xmax and not (a <= x <= b):
            pool.append(x)
    groups = {}
    for x in pool:
        groups.setdefault(grundy(x, a, b), []).append(x)
    return groups


def build_nontrivial(a, b, n, rng, want_bob, xmax=LIM):
    """构造无立即胜堆的局面；want_bob 时保证 XOR==0，否则 XOR!=0。"""
    for _ in range(8):
        groups = cand_pool(a, b, rng, xmax)
        gs = list(groups.keys())
        if not gs:
            return None
        xs = []
        xr = 0
        for _ in range(max(0, n - 1)):
            g = rng.choice(gs)
            xs.append(rng.choice(groups[g]))
            xr ^= g
        if want_bob:
            if xr in groups:
                xs.append(rng.choice(groups[xr]))
                if solve(a, b, xs) is False:
                    return (a, b, xs)
        else:
            opts = [g for g in gs if g != xr]
            if opts:
                xs.append(rng.choice(groups[rng.choice(opts)]))
                if solve(a, b, xs) is True:
                    return (a, b, xs)
    return None


# ---------- 各点构造 ----------
def build_point(idx, rng):
    """返回 cases = [(a,b,[x...])]"""
    cases = []

    if idx == 1:  # 边界 / n=1（Subtask 1）
        cases = [
            (1, 1, [1]),                    # x in [a,b] -> Alice
            (1, 1, [2]),                    # r=0 -> Bob
            (1, 1, [3]),                    # r=1 -> Alice
            (2, 2, [4]),                    # x=2a, r=0 -> Bob
            (2, 2, [3]),                    # killable -> Alice
            (5, 5, [12]),                   # r=2<a -> Bob
            (5, 5, [15]),                   # r=5>=M-a -> Alice
            (10 ** 9, 10 ** 9, [10 ** 9]),  # x in [a,b] -> Alice
            (10 ** 9, 10 ** 9, [1]),        # 死堆 -> Bob
            (1, 10 ** 9, [10 ** 9]),        # x in [a,b] -> Alice
        ]
    elif idx == 2:  # Subtask 2: a=b
        for a in (1, 2, 3, 7, 999983, 5 * 10 ** 8, 999999999, 10 ** 9):
            for n in (1, 2, 3, 17, 500, 1000):
                xs = []
                for _ in range(n):
                    mode = rng.randrange(5)
                    if mode == 0:
                        xs.append(clamp(a - rng.randint(0, min(a - 1, 5))))
                    elif mode == 1:
                        xs.append(clamp(a))
                    elif mode == 2:
                        xs.append(clamp(a + rng.randint(1, max(1, min(a, 10)))))
                    elif mode == 3:
                        xs.append(clamp(2 * a + rng.randint(0, 3)))
                    else:
                        xs.append(rng.randint(1, LIM))
                cases.append((a, a, xs))
        # 追加若干构造局面（a=b 时 xor 定胜负）
        for a in (2, 7, 999983, 10 ** 6):
            for want_bob in (True, False):
                c = build_nontrivial(a, a, 500, rng, want_bob)
                if c:
                    cases.append(c)
    elif idx == 3:  # Subtask 3: a=1
        for b in (1, 2, 3, 1000, 10 ** 6, 5 * 10 ** 8, 10 ** 9):
            for n in (1, 2, 5, 100, 1000):
                xs = []
                for _ in range(n):
                    mode = rng.randrange(4)
                    if mode == 0:
                        xs.append(clamp(b + rng.randint(-2, 2)))
                    elif mode == 1:
                        xs.append(clamp(b + 1 + rng.randint(0, 3)))
                    elif mode == 2:
                        xs.append(LIM)
                    else:
                        xs.append(rng.randint(1, LIM))
                cases.append((1, b, xs))
        for b in (1, 2, 10 ** 6, 5 * 10 ** 8):
            for want_bob in (True, False):
                c = build_nontrivial(1, b, 500, rng, want_bob)
                if c:
                    cases.append(c)
    elif idx == 4:  # Subtask 4: x_i <= 1000
        ab_pool = [(1, 1), (1, 2), (2, 1000), (500, 1000), (1000, 1000),
                   (1001, 10 ** 9), (10 ** 6, 10 ** 6), (5 * 10 ** 8, 10 ** 9),
                   (999999999, 10 ** 9), (10 ** 9, 10 ** 9)]
        for (a, b) in ab_pool:
            for n in (1, 3, 50, 300, 1000):
                xs = [rng.randint(1, 1000) for _ in range(n)]
                for v in key_points(a, b, rng, 8):
                    if v <= 1000:
                        xs[rng.randrange(n)] = v
                cases.append((a, b, xs))
        for (a, b) in ((1, 1), (1, 2), (2, 1000), (1000, 1000), (1001, 10 ** 9)):
            for want_bob in (True, False):
                c = build_nontrivial(a, b, 300, rng, want_bob, xmax=1000)
                if c:
                    cases.append(c)
    elif idx == 5:  # Subtask 5: a,b <= 1000
        for _ in range(60):
            a = rng.randint(1, 1000)
            b = rng.randint(a, 1000)
            n = rng.choice([1, 2, 10, 200, 1000])
            xs = []
            for _ in range(n):
                mode = rng.randrange(4)
                if mode == 0:
                    xs.append(clamp(a + rng.randint(-2, 2)))
                elif mode == 1:
                    xs.append(clamp(a + b + rng.randint(-2, 2)))
                elif mode == 2:
                    xs.append(clamp(b + rng.randint(-2, 2)))
                else:
                    xs.append(rng.randint(1, LIM))
            cases.append((a, b, xs))
        for _ in range(20):
            a = rng.randint(1, 1000)
            b = rng.randint(a, 1000)
            for want_bob in (True, False):
                c = build_nontrivial(a, b, 500, rng, want_bob)
                if c:
                    cases.append(c)
    elif idx == 6:  # 小规模手算
        cases = [
            (1, 2, [3, 3]),                       # 两个 g=0 堆 -> Bob
            (1, 2, [4, 5]),                       # g=1,g=2 -> Alice
            (2, 3, [4, 4, 4]),                    # 三个 g=1 -> Alice
            (2, 3, [5, 5, 5]),                    # 三个 g=0 -> Bob
            (3, 5, [6, 7, 8]),                    # g=1,1,0 -> Bob
            (3, 5, [8, 8, 8, 8, 8]),              # 五个 g=0 -> Bob
            (4, 7, [5, 5]),                       # 两 killable -> Bob
            (7, 9, [10, 12]),                     # g=1,g=1 -> Bob
            (2, 2, [10 ** 9, 10 ** 9, 1]),        # 混死堆 -> Bob
            (1, 1, [1, 1, 1]),                    # 全 [a,b] -> Alice
            (2, 5, [6, 7, 12]),                   # 手工核对
            (3, 4, [5, 6, 7]),                    # 手工核对
        ]
    elif idx == 7:  # 中等
        for _ in range(100):
            a = rng.randint(1, LIM)
            b = rng.randint(a, LIM)
            n = rng.randint(50, 300)
            if rng.random() < 0.5:
                c = build_nontrivial(a, b, n, rng, rng.random() < 0.5)
                if c:
                    cases.append(c)
                    continue
            xs = [rng.randint(1, LIM) for _ in range(n)]
            for v in key_points(a, b, rng, 6):
                xs[rng.randrange(n)] = v
            cases.append((a, b, xs))
    elif idx == 8:  # 大
        for _ in range(300):
            a = rng.randint(1, LIM)
            b = rng.randint(a, LIM)
            n = 1000
            if rng.random() < 0.5:
                c = build_nontrivial(a, b, n, rng, rng.random() < 0.5)
                if c:
                    cases.append(c)
                    continue
            xs = [rng.randint(1, LIM) for _ in range(n)]
            for v in key_points(a, b, rng, 8):
                xs[rng.randrange(n)] = v
            cases.append((a, b, xs))
    elif idx == 9:  # 顶格边界构造
        big_ab = [(6 * 10 ** 8, 9 * 10 ** 8),      # a+b > 1e9
                  (10 ** 9, 10 ** 9),              # 全死堆或 x=1e9
                  (1, 10 ** 9),                    # x<=b 全是立即胜
                  (1, 1),
                  (10 ** 9 - 1, 10 ** 9),
                  (3, 7), (999999937, 999999999)]
        for _ in range(1000):
            if rng.random() < 0.35:
                a = rng.randint(1, LIM)
                b = rng.randint(a, LIM)
                c = build_nontrivial(a, b, 1000, rng, rng.random() < 0.5)
                if c:
                    cases.append(c)
                    continue
            if rng.random() < 0.5:
                a, b = rng.choice(big_ab)
            else:
                a = rng.randint(1, LIM)
                b = rng.randint(a, LIM)
            n = 1000
            xs = []
            for _ in range(n):
                mode = rng.randrange(4)
                if mode == 0:
                    xs.append(rng.choice(key_points(a, b, rng, 12)))
                elif mode == 1:
                    xs.append(clamp(a + rng.randint(-1, 1)))
                elif mode == 2:
                    xs.append(clamp(b + rng.randint(-1, 1)))
                else:
                    xs.append(rng.randint(1, LIM))
            cases.append((a, b, xs))
    elif idx == 10:  # 顶格随机 + 构造
        for _ in range(1000):
            a = rng.randint(1, LIM)
            b = rng.randint(a, LIM)
            n = 1000
            if rng.random() < 0.5:
                c = build_nontrivial(a, b, n, rng, rng.random() < 0.5)
                if c:
                    cases.append(c)
                    continue
            xs = [rng.randint(1, LIM) for _ in range(n)]
            cases.append((a, b, xs))
    else:
        raise ValueError(idx)
    return cases


# ---------- 写文件 + 跑 std + 断言 ----------
def write_in(path, cases):
    out = [str(len(cases))]
    for a, b, xs in cases:
        out.append(f"{len(xs)} {a} {b}")
        out.append(" ".join(map(str, xs)))
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
        f.flush()
        os.fsync(f.fileno())


def check_in(path, cases):
    """重新解析 .in，确认与构造一致（行数/个数）。"""
    with open(path) as f:
        tok = f.read().split()
    pos = 0
    t = int(tok[pos]); pos += 1
    assert t == len(cases), (path, t, len(cases))
    for a, b, xs in cases:
        n = int(tok[pos]); aa = int(tok[pos + 1]); bb = int(tok[pos + 2]); pos += 3
        assert (n, aa, bb) == (len(xs), a, b), (path, n, aa, bb, a, b)
        got = list(map(int, tok[pos:pos + n])); pos += n
        assert got == xs, (path, "xs mismatch")
    assert pos == len(tok), (path, "trailing tokens")


def main():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(STD):  # 编译 std（若缺）
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", STD,
                        os.path.join(HERE, "std.cpp")], check=True)
    t0 = time.time()
    for i in range(1, 11):
        rng = random.Random(20251007 + i)
        cases = build_point(i, rng)
        inp = os.path.join(DATA, f"problem{i}.in")
        outp = os.path.join(DATA, f"problem{i}.out")
        write_in(inp, cases)
        check_in(inp, cases)
        with open(inp, "rb") as fi, open(outp, "wb") as fo:
            r = subprocess.run([STD], stdin=fi, stdout=fo, timeout=60)
        assert r.returncode == 0, (i, r.returncode)
        with open(outp) as f:
            lines = f.read().split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        assert len(lines) == len(cases), (i, "out lines", len(lines), len(cases))
        assert all(s in ("Alice", "Bob") for s in lines), (i, "bad token")
        assert os.path.getsize(outp) > 0, (i, "empty out")
        # 复算比对（同一公式，防 std/文件层面的错位/截断）
        exp = ["Alice" if solve(a, b, xs) else "Bob" for a, b, xs in cases]
        assert lines == exp, (i, "answer mismatch")
        na = sum(1 for s in lines if s == "Alice")
        maxn = max(len(xs) for _, _, xs in cases)
        print(f"point {i:2d}: t={len(cases):4d} maxn={maxn:4d} "
              f"in={os.path.getsize(inp) / 1024:.0f}KB "
              f"Alice={na} Bob={len(lines) - na}")
    print(f"all 10 points generated & asserted, {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
