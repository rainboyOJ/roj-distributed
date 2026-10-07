#!/usr/bin/env python3
# 一本通 1782《分层图》数据生成器（10 组，文件名 problem1.in/.out ... problem10.in/.out）
#
# 用法：
#   cd .ybt-import/staging/1782 && python3 data.py
#
# 题面数据范围：4 <= m <= 10^4，k <= 10（20%: m<=10,k<=2；40%: m<=10^3,k<=2；
#              60%: m<=10^3,k<=5；100%: m<=10^4,k<=10）。单组测试数据。
#   输入：第一行 m k；随后 m-1 行，首行/末行各 k 个 0/1（源点/汇点边），
#         其余每行 k^2 个 0/1（第 (j-1)*k+t 个整数表示 (i,j)->(i+1,t) 是否有边）。
#   输出：一行一个整数（方案数 mod 998244353）。
#
# 本生成器要点：
#   * 自己用 Python 直接写 .in（无 O(n^2) 循环，全部按行 join），再用 subprocess
#     显式跑 std 产 .out（避免 cyaron output_gen 写缓冲不 flush 产生 0 字节 .out），
#     并断言每个 .out 非空、恰 1 行、为 [0,998244353) 内整数。
#   * 退化结构断言（验证计数 DP 的正确性）：
#       - 源点无边（首行全 0）时 s->t 路径恒为 0 条（偶），答案应为 2^(m-3) mod p；
#       - 末行全 0（汇点无边）同理答案应为 2^(m-3) mod p；
#       - 中间矩阵全为对称矩阵时转置=自身，两个取反选择结果相同，
#         答案应为 2^(m-3) 或 0（取决于唯一奇偶向量的末态）；
#       - k=1 时 1×1 矩阵转置不变，答案应为 2^(m-3) 或 0。
#   * 分层：边界(点1-3) / 小(点4) / 中(点5-6) / 大-顶格(点7-10)。
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MOD = 998244353


# ---------------- 编译 std ----------------
def build_std():
    tmpdir = tempfile.mkdtemp(prefix="std1782_")
    exe = os.path.join(tmpdir, "std")
    subprocess.run(
        ["g++", "-O2", "-std=c++17", "-o", exe, os.path.join(HERE, "std.cpp")],
        check=True,
    )
    return tmpdir, exe


# ---------------- 行生成工具（k×k 矩阵，行优先 j*k+t） ----------------
def row_bits(bits):
    """bits: 长度 k*k 的 0/1 序列（行优先）-> 空格分隔字符串"""
    return " ".join("1" if b else "0" for b in bits)


def rand_mat_str(k, rng):
    kk = k * k
    s = bin(rng.getrandbits(kk))[2:].zfill(kk)
    return " ".join(s)


def zero_mat_str(k):
    return " ".join(["0"] * (k * k))


def sym_mat_str(k, rng):
    """随机对称矩阵（M == M^T）"""
    M = [[0] * k for _ in range(k)]
    for j in range(k):
        for t in range(j, k):
            b = rng.getrandbits(1)
            M[j][t] = b
            M[t][j] = b
    return row_bits([M[j][t] for j in range(k) for t in range(k)])


def perm_mat_str(k, shift):
    """循环移位置换矩阵：第 j 行 1 位于 (j+shift)%k（稀疏、一般非对称）"""
    M = [[0] * k for _ in range(k)]
    for j in range(k):
        M[j][(j + shift) % k] = 1
    return row_bits([M[j][t] for j in range(k) for t in range(k)])


def rand_vec(k, rng):
    return [rng.getrandbits(1) for _ in range(k)]


def rand_vec_nz(k, rng):
    """随机 0/1 向量，保证非全 0（避免意外退化成"无路径"平凡数据）"""
    v = [rng.getrandbits(1) for _ in range(k)]
    if not any(v):
        v[rng.randrange(k)] = 1
    return v


def sim_parity(k, first, mat_rows, last):
    """直接按 GF(2) 模拟唯一一条（转置不变的）路径链，返回 s->t 路径数 mod 2。
    仅用于"中段矩阵全部对称 / k=1"这类转置不变的退化数据，
    此时每种取反方案得到的奇偶向量相同，答案 = 2^(m-3)（偶）或 0（奇）。"""
    v = list(first)
    for row in mat_rows:
        bits = row.split()
        nv = [0] * k
        for j in range(k):
            if v[j]:
                base = j * k
                for t in range(k):
                    if bits[base + t] == "1":
                        nv[t] ^= 1
        v = nv
    p = 0
    for t in range(k):
        if v[t] and last[t]:
            p ^= 1
    return p


# ---------------- 写 .in ----------------
def write_in(path, m, k, first, mid_rows, last):
    # 行数必须严格为 m-1：首行 k 个 + 中段 (m-3) 行各 k^2 个 + 末行 k 个
    assert len(first) == k and len(last) == k, "首/末行长度必须为 k"
    cnt = 0
    with open(path, "w") as f:
        f.write("%d %d\n" % (m, k))
        f.write(" ".join(map(str, first)) + "\n")
        for r in mid_rows:
            assert len(r.split()) == k * k, "中段行长度必须为 k^2"
            f.write(r + "\n")
            cnt += 1
        f.write(" ".join(map(str, last)) + "\n")
    assert cnt == m - 3, "中段行数应为 m-3=%d，实为 %d" % (m - 3, cnt)


# ---------------- 跑 std 产 .out ----------------
def run_std(exe, in_path, out_path):
    with open(in_path, "rb") as fi, open(out_path, "wb") as fo:
        subprocess.run([exe], stdin=fi, stdout=fo, timeout=120, check=True)
    raw = open(out_path, "rb").read()
    assert raw, "empty .out for %s" % in_path            # 断言 .out 非空
    text = raw.decode().strip()
    lines = [l for l in text.split("\n") if l.strip()]
    assert len(lines) == 1, ".out 行数 != 1: %s -> %r" % (in_path, text)
    val = int(lines[0])
    assert 0 <= val < MOD, "答案越界: %s -> %d" % (in_path, val)
    return val


def main():
    os.makedirs(DATA, exist_ok=True)
    tmpdir, exe = build_std()
    results = []

    def emit(idx, m, k, first, mid_rows, last, note, expect=None):
        in_path = os.path.join(DATA, "problem%d.in" % idx)
        out_path = os.path.join(DATA, "problem%d.out" % idx)
        write_in(in_path, m, k, first, mid_rows, last)
        val = run_std(exe, in_path, out_path)
        if expect is not None:
            assert val == expect, "点%d 期望 %d 实得 %d" % (idx, expect, val)
        size = os.path.getsize(in_path)
        results.append((idx, m, k, note, val, size))
        print("problem%d: m=%d k=%d %s -> ans=%d (%d bytes)" % (idx, m, k, note, val, size))

    # ---- 点 1：边界层（m 下限 + k 下限）----
    # m=4,k=1：1×1 矩阵转置不变，唯一方案；源点->1->汇点各 1 条边，路径数 1（奇）
    # 故答案 0。k=1 时答案必为 0 或 2^(m-3)。
    emit(1, 4, 1, [1], ["1"], [1], "m=4,k=1 最小边界(奇路径)", expect=0)

    # ---- 点 2：题面样例 ----
    emit(2, 5, 3,
         [1, 0, 1],
         ["0 1 0 1 1 0 0 0 1", "0 1 1 1 0 0 0 1 1"],
         [0, 1, 1],
         "题面样例(应为 4)", expect=4)

    # ---- 点 3：边界层（m 下限 + k 上限）----
    rng = random.Random(178203)
    emit(3, 4, 10, rand_vec_nz(10, rng), [rand_mat_str(10, rng)], rand_vec_nz(10, rng),
         "m=4,k=10 单边界顶格 k")

    # ---- 点 4：小规模（20% 档：m<=10,k<=2）----
    rng = random.Random(178204)
    emit(4, 10, 2, rand_vec_nz(2, rng), [rand_mat_str(2, rng) for _ in range(7)],
         rand_vec_nz(2, rng), "20%档 m=10,k=2 随机")

    # ---- 点 5：中规模（40% 档：m<=10^3,k<=2）----
    rng = random.Random(178205)
    emit(5, 1000, 2, rand_vec_nz(2, rng), (rand_mat_str(2, rng) for _ in range(997)),
         rand_vec_nz(2, rng), "40%档 m=1000,k=2 随机")

    # ---- 点 6：中规模（60% 档：m<=10^3,k<=5）----
    rng = random.Random(178206)
    emit(6, 1000, 5, rand_vec_nz(5, rng), (rand_mat_str(5, rng) for _ in range(997)),
         rand_vec_nz(5, rng), "60%档 m=1000,k=5 随机")

    # ---- 点 7：顶格 + 源点无边（退化，答案必为 2^(m-3)）----
    rng = random.Random(178207)
    m7, k7 = 10000, 10
    emit(7, m7, k7, [0] * k7, (rand_mat_str(k7, rng) for _ in range(m7 - 3)),
         rand_vec(k7, rng), "顶格 m=10^4,k=10 源点无边",
         expect=pow(2, m7 - 3, MOD))

    # ---- 点 8：顶格随机稠密 ----
    rng = random.Random(178208)
    m8, k8 = 10000, 10
    emit(8, m8, k8, rand_vec_nz(k8, rng), (rand_mat_str(k8, rng) for _ in range(m8 - 3)),
         rand_vec_nz(k8, rng), "顶格 m=10^4,k=10 随机稠密")

    # ---- 点 9：顶格 + 对称中段（转置=自身，两选择同结果）----
    # 中段矩阵全对称 => 取反无实际效果，唯一末态奇偶由直接 GF(2) 模拟给出，
    # 答案必为 2^(m-3)（路径偶）或 0（路径奇）；此处用模拟值断言。
    rng = random.Random(178209)
    m9, k9 = 10000, 10
    first9 = rand_vec_nz(k9, rng)
    rows9 = [sym_mat_str(k9, rng) for _ in range(m9 - 3)]
    last9 = rand_vec_nz(k9, rng)
    p9 = sim_parity(k9, first9, rows9, last9)
    expect9 = 0 if p9 else pow(2, m9 - 3, MOD)
    emit(9, m9, k9, first9, rows9, last9,
         "顶格 m=10^4,k=10 对称中段(奇偶=%d)" % p9, expect=expect9)

    # ---- 点 10：顶格 + 稀疏置换矩阵（每行/列恰 1 个 1，转置为另一置换）----
    # 非退化：首/末行均非全 0，状态始终为初始向量的置换（popcount 不变）。
    rng = random.Random(178210)
    m10, k10 = 10000, 10
    emit(10, m10, k10, rand_vec_nz(k10, rng),
         (perm_mat_str(k10, rng.randrange(k10)) for _ in range(m10 - 3)),
         rand_vec_nz(k10, rng), "顶格 m=10^4,k=10 稀疏置换矩阵")

    print("\n=== 汇总 ===")
    for idx, m, k, note, val, size in results:
        print("problem%-2d  m=%-6d k=%-3d ans=%-11d in=%-8d %s" % (idx, m, k, val, size, note))
    print("全部 %d 组：.out 非空/单行/范围断言通过" % len(results))

    # 清理编译产物
    try:
        os.remove(exe)
        os.rmdir(tmpdir)
    except OSError:
        pass


if __name__ == "__main__":
    sys.exit(main())
