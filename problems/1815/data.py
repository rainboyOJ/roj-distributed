#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一本通 1815「放石子」造数据脚本 (10 组, 分层: 边界/小/中/大/顶格)

题面: n 点 m 边有向无环图, 每边颜色 c; q 颗石子各在一点上。
      每步选一个有出边且点上有石子的点 x, 取走 1 颗石子, 选颜色集合 S,
      对 x 的每条颜色 e∈S 的出边在终点各放 1 颗石子; 不能操作者负。
      输出 1 = 先手必胜, 0 = 后手必胜。
数据范围: 20%: n≤5, m≤10, q≤20; 30%: n≤20, m≤100, q≤100;
          100%: n≤200, m≤5000, q≤10000, c≤5000。(题面注明"捆绑测试")

分层表 (data/problem{1..10}.in/.out):
  problem1  n=2   m=1    q=1     c=1      题面样例(唯一公开样例)              期望 1 (样例)
  problem2  n=2   m=0    q=1     -        空图 m=0 边界, 无任何操作           期望 0 (手算)
  problem3  n=4   m=4    q=3     c≤4      手工小构造 k=2: 汇点0, w0=1, w1=2, v=4   期望 1 (手算 sg)
  problem4  n=5   m=10   q=20    c≤5      20% 层边界 (C(5,2)=10 条边全用)      仅范围断言
  problem5  n=20  m=100  q=100   c≤100    30% 层边界                          仅范围断言
  problem6  n=100 m=2000 q=5000  c≤5000   中                                  仅范围断言
  problem7  n=200 m=5000 q=10000 c≤5000   顶格随机 DAG (无重边, 含 c=5000)     仅范围断言
  problem8  n=200 m=5000 q=10000 c≤3      顶格 + 小颜色域(同色多边异或累积)    仅范围断言
  problem9  n=101 m=4951 q=10000 c≤4951   指数构造 k=99 (sg[v]=2^99); 9999 石在 v, 1 在汇点  期望 1 (推导)
  problem10 n=200 m=5000 q=10000 c≤5000   k=99 构造 + 49 条冗余边补齐 m=5000; 全点石子成对      期望 0 (推导)

校验策略 (不写/不跑任何 brute、对拍、stress):
  - 每个点: 用 std 经 subprocess 显式跑出 .out, 断言 .out 恰 1 行、非空、取值 ∈ {0,1};
  - 手算/推导点直接断言具体期望值 (推导见下);
  - 额外内部断言 (不落盘): 小构造 stones "4 4 1" → 0 (同点两颗石子异或抵消);
  - 生成器复杂度: 随机边 O(m) (random.sample 抽 pair 下标 + isqrt O(1) 解码),
    构造点写入边数 = k(k+1)/2+1 = O(m); 无任何 O(n²) Python 循环;
  - .in 行数断言 = m+3 (首行 + m 条边 + q 行 + 石子行), 石子数断言 = q。

手算/推导依据:
  problem3 图: 1=汇点; 2→1(c1); 3→2(c2); 4→2(c3); 4→3(c4)。
    sg[1]=0 (无操作); sg[2]=mex(span{0})=1; sg[3]=mex(span{1})=mex{0,1}=2;
    sg[4]=mex(span{1,2})=mex{0,1,2,3}=4。
    石子 {4,3,1} → 4^2^0=6≠0 → 1;  内部断言 {4,4,1} → 4^4^0=0 → 0。
  problem9 指数构造 (k=99): 汇点 1; w_j=2+j (j=0..98), w_0→汇点, w_j→w_i (i<j, 每边新颜色);
    v=101, v→w_j (每边新颜色)。归纳得 sg[w_j]=2^j, sg[v]=mex(span{1,2,...,2^98})=2^99;
    边数 = 1 + Σ_{j=1}^{98} j + 99 = 4951 (m=5000 下 e≤sqrt(2m)≈99 的顶格位宽)。
    v 非汇点 ⇒ sg[v]≠0; 9999 (奇) 颗在 v + 1 颗在汇点 → 异或 = 2^99 ≠ 0 → 1。
  problem10: 同上 + 49 条冗余边 v→w_i (i<49, 新颜色, h=2^i 已在 span 内, 不改变 sg) → m=5000, n=200;
    石子: 点 1..101 各 2 颗 (=202) + 点 200 共 9798 颗 → 每个点石子数全偶 → 异或 = 0 → 0。
    (该期望只依赖"异或按点数奇偶性归零", 与 sg 具体值无关。)

运行: nice -n 19 timeout 120 python3 data.py
"""
import os
import random
import shutil
import subprocess
import time
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STD_CPP = os.path.join(HERE, "std.cpp")
BIN = os.path.join(HERE, ".std_bin")

NICE = shutil.which("nice")
TIMEOUT = shutil.which("timeout") or shutil.which("gtimeout")


def wrapped(cmd):
    """按任务要求以 nice -n 19 timeout 120 包裹耗时命令"""
    if NICE:
        cmd = [NICE, "-n", "19"] + cmd
    if TIMEOUT:
        cmd = [TIMEOUT, "120"] + cmd
    return cmd


def compile_std():
    for cxx in ("g++-16", "g++", "clang++"):
        path = shutil.which(cxx)
        if not path:
            continue
        r = subprocess.run(wrapped([path, "-O2", "-std=c++17", "-o", BIN, STD_CPP]),
                           capture_output=True, text=True)
        if r.returncode == 0:
            print("[compile] %s -O2 -std=c++17 -> %s" % (cxx, os.path.basename(BIN)))
            return
        print("[compile] %s failed: %s" % (cxx, r.stderr.strip().splitlines()[:1]))
    raise SystemExit("no working C++ compiler")


def run_std(inp):
    r = subprocess.run([BIN], input=inp, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit("std runtime error: %s" % r.stderr[:500])
    return r.stdout


def build_in(n, m, edges, q, stones):
    """组装 .in 文本, 并断言结构: m 条边 / q 个石子 / 每行格式"""
    assert len(edges) == m, "edge count mismatch"
    assert len(stones) == q, "stone count mismatch"
    assert 1 <= n <= 200 and 0 <= m <= 5000 and 1 <= q <= 10000, "range violated"
    for (s, t, c) in edges:
        assert 1 <= t < s <= n, "edge not in s>t DAG form: %r" % ((s, t, c),)
        assert 1 <= c <= 5000, "color out of range: %r" % ((s, t, c),)
    for a in stones:
        assert 1 <= a <= n, "stone position out of range: %r" % (a,)
    parts = ["%d %d" % (n, m)]
    parts += ["%d %d %d" % e for e in edges]
    parts.append("%d" % q)
    parts.append(" ".join(map(str, stones)))
    text = "\n".join(parts) + "\n"
    # 行数: 首行 + m 边行 + q 行 + 石子行 = m + 3
    assert text.count("\n") == m + 3, "line count != m+3"
    assert len(text.split("\n")[m + 2].split()) == q, "stone line count != q"
    return text


def emit(idx, inp, note, expect=None, expect_desc="", m=None, timed=False):
    """跑 std 产 .out, 断言非空/恰 1 行/取值合法 (及期望值), 落盘 data/"""
    t0 = time.perf_counter()
    out = run_std(inp)
    dt = time.perf_counter() - t0
    lines = out.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    assert len(lines) == 1, "problem%d: expect exactly 1 line, got %r" % (idx, out)
    assert lines[0].strip() != "", "problem%d: empty output" % idx
    val = lines[0].strip()
    assert val in ("0", "1"), "problem%d: output must be 0/1, got %r" % (idx, val)
    if expect is not None:
        assert val == expect, \
            "problem%d: expect %s got %s (%s)" % (idx, expect, val, expect_desc)
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "problem%d.in" % idx), "w") as f:
        f.write(inp)
    with open(os.path.join(DATA, "problem%d.out" % idx), "w") as f:
        f.write(val + "\n")
    tag = "  [hand %s]" % expect_desc if expect is not None else ""
    extra = "  std=%.3fs" % dt if timed else ""
    print("[data] problem%-2d: %-58s ans=%s%s%s" % (idx, note, val, tag, extra))
    return val


def rand_dag(n, m, cmax, rng, force_cmax=False):
    """随机 DAG: 无重边 (random.sample 抽 s>t 的 pair 下标, isqrt O(1) 解码)"""
    total = n * (n - 1) // 2
    assert 0 <= m <= total, "not enough pairs for distinct-edge DAG"
    edges = []
    for idx in rng.sample(range(total), m):
        s = (1 + isqrt(1 + 8 * idx)) // 2 + 1          # 行号: C(s-1,2) <= idx < C(s,2)
        t = idx - (s - 1) * (s - 2) // 2 + 1
        assert 1 <= t < s <= n
        edges.append((s, t, rng.randint(1, cmax)))
    if force_cmax and edges:
        s, t, _ = edges[0]
        edges[0] = (s, t, cmax)                        # 保证颜色顶格出现
    return edges


def exp_graph(k, extra, n):
    """指数构造: 汇点 1; w_j=2+j (j=0..k-1); v=k+2。sg[w_j]=2^j, sg[v]=2^k。
    extra: 追加 extra 条冗余边 v->w_i (新颜色), h=2^i 已在 span 内, 不改变任何 sg。
    返回 (edges, v, sink); 边数 = 1 + k(k-1)/2 + k + extra = O(m)。"""
    sink = 1
    w = [2 + j for j in range(k)]
    v = k + 2
    edges = []
    color = 0

    def nxt():
        nonlocal color
        color += 1
        return color

    edges.append((w[0], sink, nxt()))
    for j in range(1, k):
        for i in range(j):
            edges.append((w[j], w[i], nxt()))
    for j in range(k):
        edges.append((v, w[j], nxt()))
    for i in range(extra):
        edges.append((v, w[i], 1000 + i))
    assert len(edges) == 1 + k * (k - 1) // 2 + k + extra
    assert v <= n
    return edges, v, sink


def main():
    compile_std()
    rng = random.Random(20240615)      # 固定种子, 数据可复现

    # problem1: 题面样例
    emit(1, "2 1\n2 1 1\n1\n2\n", "题面样例 (n=2,m=1,q=1)", "1", "官方样例=1")

    # problem2: m=0 空图边界
    inp = build_in(2, 0, [], 1, [1])
    emit(2, inp, "空图 m=0, 无任何操作", "0", "无操作先手负")

    # problem3: 手工小构造 k=2 (sg: 汇点0, w0=1, w1=2, v=4)
    tiny = [(2, 1, 1), (3, 2, 2), (4, 2, 3), (4, 3, 4)]
    inp = build_in(4, 4, tiny, 3, [4, 3, 1])
    emit(3, inp, "手工构造 k=2, 石子{4,3,1}", "1", "4^2^0=6!=0")
    # 额外内部断言 (不落盘): 同点两颗石子异或抵消
    v = run_std(build_in(4, 4, tiny, 3, [4, 4, 1])).strip()
    assert v == "0", "internal tiny check: {4,4,1} should give 0, got %r" % v
    print("[check] 内部断言: 小构造 {4,4,1} -> 0 (同点异或抵消) OK")

    # problem4: 20% 层边界 (n<=5, m<=10, q<=20), C(5,2)=10 条边全用
    n, m, q = 5, 10, 20
    edges = rand_dag(n, m, 5, rng)
    inp = build_in(n, m, edges, q, [rng.randint(1, n) for _ in range(q)])
    emit(4, inp, "20% 层边界 n=5,m=10,q=20,c<=5")

    # problem5: 30% 层边界 (n<=20, m<=100, q<=100)
    n, m, q = 20, 100, 100
    edges = rand_dag(n, m, 100, rng)
    inp = build_in(n, m, edges, q, [rng.randint(1, n) for _ in range(q)])
    emit(5, inp, "30% 层边界 n=20,m=100,q=100,c<=100")

    # problem6: 中
    n, m, q = 100, 2000, 5000
    edges = rand_dag(n, m, 5000, rng)
    inp = build_in(n, m, edges, q, [rng.randint(1, n) for _ in range(q)])
    emit(6, inp, "中 n=100,m=2000,q=5000,c<=5000")

    # problem7: 顶格随机 (无重边, 含 c=5000)
    n, m, q = 200, 5000, 10000
    edges = rand_dag(n, m, 5000, rng, force_cmax=True)
    inp = build_in(n, m, edges, q, [rng.randint(1, n) for _ in range(q)])
    emit(7, inp, "顶格 n=200,m=5000,q=10000,c<=5000(含5000)", timed=True)

    # problem8: 顶格 + 小颜色域 (同色多边异或累积)
    n, m, q = 200, 5000, 10000
    edges = rand_dag(n, m, 3, rng)
    inp = build_in(n, m, edges, q, [rng.randint(1, n) for _ in range(q)])
    emit(8, inp, "顶格+小颜色域 n=200,m=5000,q=10000,c<=3", timed=True)

    # problem9: 指数构造 k=99 -> sg[v]=2^99; 9999 颗在 v + 1 颗在汇点
    k = 99
    edges, v, sink = exp_graph(k, 0, k + 2)
    assert len(edges) == 4951 and v == 101
    stones = [v] * 9999 + [sink]
    inp = build_in(v, len(edges), edges, 10000, stones)
    emit(9, inp, "指数构造 k=99 (sg[v]=2^99), 奇数颗在 v", "1", "v 非汇点, 奇偶->非0", timed=True)

    # problem10: 同构造 + 49 条冗余边补齐 m=5000 (n=200); 全点石子成对 -> 0
    edges, v, sink = exp_graph(k, 49, 200)
    assert len(edges) == 5000
    stones = [x for x in range(1, v + 1) for _ in range(2)] + [200] * 9798
    assert len(stones) == 10000
    inp = build_in(200, len(edges), edges, 10000, stones)
    emit(10, inp, "k=99 + 49 冗余边补齐 m=5000, 石子全成对", "0", "全偶数->异或0", timed=True)

    # 最终检查: data/ 命名与内容
    files = sorted(os.listdir(DATA))
    want = sorted("problem%d.%s" % (i, e) for i in range(1, 11) for e in ("in", "out"))
    assert files == want, "data/ 文件命名不符合 problem1..10.in/.out: %r" % files
    for i in range(1, 11):
        with open(os.path.join(DATA, "problem%d.in" % i)) as f:
            assert f.read().strip() != "", "problem%d.in empty" % i
        with open(os.path.join(DATA, "problem%d.out" % i)) as f:
            content = f.read()
            assert content.strip() != "" and content.count("\n") == 1, \
                "problem%d.out 应恰 1 行非空" % i
    print("[check] data/ 共 %d 个文件, 命名与内容断言通过" % len(files))
    if os.path.exists(BIN):
        os.remove(BIN)
        print("[clean] 删除编译产物 %s" % os.path.basename(BIN))


if __name__ == "__main__":
    main()
