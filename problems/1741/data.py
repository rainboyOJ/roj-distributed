#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一本通 1741《电子速度》分层数据生成器（cyaron）

题意：n 个电子，第 i 个速度 v_i=(x_i,y_i)；操作 1 p x y（单点改速度）、操作 2 l r
（询问 Σ_{l≤i<j≤r} |v_i×v_j|²，模 20170927）。

题面数据表（单组测试，无多组数据、无 Σ 限制）：
    点1 n≤100,  m≤100          点6 n≤50000,  m≤50000
    点2 n≤500,  m≤500          点7 n≤100000, m≤100000
    点3 n≤1000, m≤1000         点8 n≤500000, m≤500000
    点4 n≤5000, m≤5000         点9 n≤10^6,   m≤10^6
    点5 n≤10000,m≤10000        点10 n≤10^6,  m≤10^6
    100%：1≤n,m≤10^6，0≤x_i,y_i<20170927，1≤l≤r≤n。

分层设计（10 组 .in/.out，每组单测试）：
    1  最小边界 n=1,m=1：l=r=1，答案必为 0
    2  n=m=500 极端值层：x,y∈{0,1,MOD-1,MOD-2,10085863}，含 [1,1]/[n,n]/全区间/相邻区间
    3  n=m=1000 小随机
    4  n=m=5000 退化层：全部 x=y（答案恒 0）+ 更新仍保持 x=y
    5  n=m=10000 中等随机
    6  n=m=50000 随机，查询一半为全区间（长区间压力）
    7  n=m=100000 随机，查询一半为全区间
    8  n=m=500000 极端值交替 + l=r 查询 + 2^k-1 右端点前缀查询 + 全区间
    9  n=m=10^6 顶格均匀随机
   10  n=m=10^6 顶格最坏结构：全值 MOD-1，20 万次 [1,1] 查询 + 20 万次 p=1/p=n 更新
       + 40 万次全区间查询 + 20 万次极端值单点更新

安全措施（针对 cyaron 在 std 缺失时静默产出 0 字节 .out 的隐患）：
  * 生成前校验 ../std 存在；
  * 生成后断言 .out 存在、非空、行数 == 该点 op2 的个数、每行取值 ∈ [0,MOD)；
  * 断言单点 n、m 不超题面该点上限。

用法（本目录 = .ybt-import/staging/1741/）：
    nice -n 19 timeout 900 python3 data.py            # 生成全部 10 组
    nice -n 19 timeout 900 python3 data.py 1 2        # 只生成指定点
"""
import os
import random
import sys
import time

from cyaron import IO

MOD = 20170927
MAXN = 10 ** 6
BATCH = 1 << 16

# ── 已在 data/ 目录则原地生成，否则自动建 data/ 并进入 ──
if os.path.basename(os.getcwd()) != "data":
    os.makedirs("data", exist_ok=True)
    os.chdir("data")

STD_PATH = "../std"
if not os.path.exists(STD_PATH):
    raise SystemExit("FATAL: %s 不存在，请先 g++ -O2 -std=c++17 std.cpp -o std" % STD_PATH)

# 每点规模上限（题面表），用于生成后断言
CAP = {
    1: (100, 100), 2: (500, 500), 3: (1000, 1000), 4: (5000, 5000), 5: (10000, 10000),
    6: (50000, 50000), 7: (100000, 100000), 8: (500000, 500000), 9: (MAXN, MAXN), 10: (MAXN, MAXN),
}
NOTES = {
    1: "最小边界 n=1,m=1，l=r=1（答案 0）",
    2: "极端值层 n=m=500，x,y∈{0,1,MOD-1,MOD-2,10085863}，含 l=r/全区间/相邻区间",
    3: "小规模随机 n=m=1000",
    4: "退化层 n=m=5000，全部 x=y（答案恒 0，含更新）",
    5: "中等规模随机 n=m=10000",
    6: "大规模随机 n=m=50000，1/2 查询为全区间",
    7: "大规模随机 n=m=100000，1/2 查询为全区间",
    8: "大极端值 n=m=500000，值交替 0/MOD-1，l=r + 2^k-1 前缀 + 全区间 + 单点更新",
    9: "顶格随机 n=m=10^6（值均匀 [0,MOD)）",
    10: "顶格最坏结构 n=m=10^6：全值 MOD-1，[1,1] 查询 + p=1/p=n 更新 + 全区间查询",
}


def rand_extreme(rng):
    return rng.choice((0, 1, MOD - 1, MOD - 2, 10085863))


def gen_ops(t, rng, n, m):
    """返回 (ops 列表, 查询数)；ops 为字符串行。"""
    ops = []

    def upd(p, x, y):
        ops.append("1 %d %d %d" % (p, x, y))

    def qry(l, r):
        ops.append("2 %d %d" % (l, r))

    if t == 1:
        qry(1, 1)
    elif t == 2:
        # 前 6 条固定边界操作，其余随机
        qry(1, n); qry(1, 1); qry(n, n); upd(1, 0, 0); upd(1, MOD - 1, MOD - 1); qry(1, n)
        while len(ops) < m:
            if rng.random() < 0.5:
                upd(rng.randint(1, n), rand_extreme(rng), rand_extreme(rng))
            else:
                l = rng.randint(1, n); r = rng.randint(l, n)
                if rng.random() < 0.2:
                    l = r = rng.randint(1, n)
                qry(l, r)
        ops = ops[:m]
    elif t == 3:
        while len(ops) < m:
            if rng.random() < 0.5:
                upd(rng.randint(1, n), rng.randrange(MOD), rng.randrange(MOD))
            else:
                l = rng.randint(1, n); r = rng.randint(l, n)
                qry(l, r)
    elif t == 4:
        # 全部 x=y（答案恒 0），更新也保持 x=y
        while len(ops) < m:
            if rng.random() < 0.5:
                v = rng.randrange(MOD); upd(rng.randint(1, n), v, v)
            else:
                l = rng.randint(1, n); r = rng.randint(l, n)
                if rng.random() < 0.15:
                    l = r = rng.randint(1, n)
                qry(l, r)
    elif t in (5, 6, 7):
        full_p = {5: 0.2, 6: 0.5, 7: 0.5}[t]
        while len(ops) < m:
            if rng.random() < 0.5:
                upd(rng.randint(1, n), rng.randrange(MOD), rng.randrange(MOD))
            else:
                u = rng.random()
                if u < full_p:
                    qry(1, n)
                elif u < full_p + 0.1:
                    l = r = rng.randint(1, n)
                    qry(l, r)
                else:
                    l = rng.randint(1, n); r = rng.randint(l, n)
                    qry(l, r)
    elif t == 8:
        pk = [(1 << k) - 1 for k in range(1, 20) if (1 << k) - 1 <= n]
        while len(ops) < m:
            u = rng.random()
            if u < 0.5:
                upd(rng.randint(1, n), rand_extreme(rng), rand_extreme(rng))
            elif u < 0.5 + 0.15:
                l = r = rng.randint(1, n)
                qry(l, r)
            elif u < 0.5 + 0.15 + 0.15:
                r = rng.choice([v for v in pk if v >= 1])
                qry(rng.randint(1, r), r)
            elif u < 0.5 + 0.15 + 0.15 + 0.1:
                qry(1, n)
            else:
                l = rng.randint(1, n); r = rng.randint(l, n)
                qry(l, r)
    elif t == 9:
        while len(ops) < m:
            u = rng.random()
            if u < 0.5:
                upd(rng.randint(1, n), rng.randrange(MOD), rng.randrange(MOD))
            elif u < 0.6:
                qry(1, n)
            elif u < 0.65:
                l = r = rng.randint(1, n)
                qry(l, r)
            else:
                l = rng.randint(1, n); r = rng.randint(l, n)
                qry(l, r)
    elif t == 10:
        # 20 万次 [1,1] 查询
        for _ in range(200000):
            qry(1, 1)
        # 20 万次 p=1 更新（Fenwick 长路径），值在 MOD-1 与 0 间交替
        for i in range(200000):
            v = MOD - 1 if i % 2 == 0 else 0
            upd(1, v, MOD - 1)
        # 40 万次全区间查询（最大数负载）
        ops.extend(["2 1 %d" % n] * 400000)
        # 20 万次 p=n 更新
        for i in range(200000):
            upd(n, rand_extreme(rng), rand_extreme(rng))
    else:
        raise ValueError("未知测试点 %d" % t)
    if len(ops) != m:
        raise SystemExit("点%d: 生成操作数 %d != m=%d" % (t, len(ops), m))
    nq = sum(1 for s in ops if s[0] == "2")
    return ops, nq


def gen_init(t, rng, n):
    """产初速度的生成器（逐行，避免大 list）。"""
    if t == 1:
        yield MOD - 1, MOD - 1
    elif t == 2:
        for _ in range(n):
            yield rand_extreme(rng), rand_extreme(rng)
    elif t == 4:
        for _ in range(n):
            v = rng.randrange(MOD)
            yield v, v
    elif t == 8:
        for i in range(1, n + 1):
            v = 0 if i % 2 else MOD - 1
            yield v, (MOD - 1 if i % 3 else 0)
    elif t == 10:
        for _ in range(n):
            yield MOD - 1, MOD - 1
    else:
        for _ in range(n):
            yield rng.randrange(MOD), rng.randrange(MOD)


def gen_point(t, n, m, rng):
    cap_n, cap_m = CAP[t]
    assert n <= cap_n and m <= cap_m, "点%d 超题面上限" % t
    t0 = time.time()
    io = IO(file_prefix="problem", data_id=t)
    # 直接向真实文件对象写，绕开 cyaron input_write 的 separator 逻辑（块间会插空格），
    # 并保证尾部 batch 一定 flush（早期版本漏 flush → .in 截断，截断输入会让 std 死等）
    fout = io.input_file
    fout.write("%d %d\n" % (n, m))
    batch = []
    cnt = 0
    for x, y in gen_init(t, rng, n):
        assert 0 <= x < MOD and 0 <= y < MOD
        batch.append("%d %d" % (x, y))
        if len(batch) >= BATCH:
            fout.write("\n".join(batch) + "\n")
            batch = []
        cnt += 1
    assert cnt == n, "初始速度行数 %d != n=%d" % (cnt, n)
    ops, nq = gen_ops(t, rng, n, m)
    for i in range(0, len(ops), BATCH):
        batch.extend(ops[i:i + BATCH])
        if len(batch) >= BATCH:
            fout.write("\n".join(batch) + "\n")
            batch = []
    if batch:
        fout.write("\n".join(batch) + "\n")
        batch = []
    fout.flush()
    assert nq >= 1, "点%d 无询问，.out 会为空" % t

    # ── .in 结构自检：流式逐行（行数 = 1 + n + m，每行令牌数符合格式）──
    inp = "problem%d.in" % t
    nq2 = 0
    with open(inp, "r") as f:
        first = f.readline()
        assert first == "%d %d\n" % (n, m), "%s: 首行错误 %r" % (inp, first)
        for i in range(2, 2 + n):
            p = f.readline().split()
            if len(p) != 2 or not all(0 <= int(v) < MOD for v in p):
                raise AssertionError("%s: 第 %d 行初速度非法" % (inp, i))
        for i in range(2 + n, 2 + n + m):
            ln = f.readline()
            if not ln.endswith("\n"):
                raise AssertionError("%s: 第 %d 行未以换行结尾" % (inp, i))
            p = ln.split()
            if p[0] == "1":
                ok = len(p) == 4 and 1 <= int(p[1]) <= n and all(0 <= int(v) < MOD for v in p[2:])
            elif p[0] == "2":
                ok = len(p) == 3 and 1 <= int(p[1]) <= int(p[2]) <= n
                nq2 += 1
            else:
                ok = False
            if not ok:
                raise AssertionError("%s: 第 %d 行操作非法 %r" % (inp, i, ln[:60]))
        extra = f.read()
        assert extra == "", "%s: 文件多出 %d 字节" % (inp, len(extra))
    assert nq2 == nq, "%s: 文件内询问数 %d != 计划 %d" % (inp, nq2, nq)
    io.output_gen(STD_PATH, time_limit=100)
    io.output_file.flush()
    io.input_file.flush()
    outp = "problem%d.out" % t
    assert os.path.exists(outp), "%s 未生成" % outp
    size = os.path.getsize(outp)
    assert size > 0, "%s 为 0 字节（std 未产出，cyaron 静默失败）" % outp
    with open(outp, "r") as f:
        vals = f.read().split()
    assert len(vals) == nq, "%s: 输出 %d 个数 != 询问数 %d" % (outp, len(vals), nq)
    for v in vals:
        assert v.isdigit() and 0 <= int(v) < MOD, "%s: 非法输出值 %r" % (outp, v)
    print("[point %2d] n=%-7d m=%-7d q=%-7d in=%-9d out=%-8d %5.1fs | %s"
          % (t, n, m, nq, os.path.getsize("problem%d.in" % t), size,
             time.time() - t0, NOTES[t]))


PLAN = {1: (1, 1), 2: (500, 500), 3: (1000, 1000), 4: (5000, 5000), 5: (10000, 10000),
        6: (50000, 50000), 7: (100000, 100000), 8: (500000, 500000), 9: (MAXN, MAXN),
        10: (MAXN, MAXN)}


def main():
    which = [int(x) for x in sys.argv[1:]] or list(range(1, 11))
    rng = random.Random(1741)
    for t in which:
        n, m = PLAN[t]
        gen_point(t, n, m, rng)


main()
