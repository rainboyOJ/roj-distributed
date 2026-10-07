#!/usr/bin/env python3
# 一本通 1811《多项式相乘》数据生成器
#
# 用法：
#   g++ -O2 -std=c++17 std.cpp -o std
#   python3 data.py          # 在 staging/1811 目录下运行（脚本按自身路径定位 data/ 与 std）
#
# 说明：
#   * 本题输入只有一个整数 n，输出一个整数 t mod 10000。
#   * 按任务要求，.out 一律用 subprocess 显式调用 std 生成（不用 cyaron 的
#     output_gen，规避其写缓冲不 flush 导致 0 字节 .out 的隐患），
#     并对每个 .out 断言：文件非空、恰好 1 行、内容为 [0,10000) 的整数，
#     且与 .in 的整数一一对应（n=3 时须等于题面样例 40）。
#   * 数据规模按题面：1 <= n <= 10^9（数组/内存无关，O(log n) 解法）。
#     本题对任意合法 n 都有输出，不存在"无解空输出点"。
#
# 分层设计（10 组：边界 / 小 / 中 / 大 / 顶格，覆盖十进制位数边界与 mod 回绕）：
#   点 1   边界：n=1（下限；展开式 "x+a_1"，t=4）
#   点 2   边界：n=2（题面显式给出的 n=2 展开式，t=16）
#   点 3   样例：n=3（题面样例，t=40）
#   点 4   小/位数边界：n=9（下标全为 1 位数时的上限）
#   点 5   位数边界：n=10（出现 2 位数下标 a_10 的下限）
#   点 6   位数边界：n=100（出现 3 位数下标 a_100 的下限）
#   点 7   中/回绕：n=10000（n ≡ 0 mod 10000，检验 (n+D) 与 3n 取模；5 位数下标下限）
#   点 8   大：n=123456789（大规模、9 位数下标、非整十）
#   点 9   大/接近顶格：n=999999999（9 位数下标上限，顶格-1）
#   点 10  顶格：n=1000000000（题面上限 10^9）
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
STD_BIN = os.path.join(HERE, "std")
MOD = 10000

# (n, 层次, 设计意图)
CASES = [
    (1,          "边界",     "n 下限；展开式 'x+a_1'，t=4"),
    (2,          "边界",     "题面显式给出的 n=2 展开式，t=16"),
    (3,          "样例",     "题面样例，t=40"),
    (9,          "小/位数",  "下标全为 1 位数时的最大 n（小规模档）"),
    (10,         "位数边界", "出现 2 位数下标 a_10 的最小 n"),
    (100,        "位数边界", "出现 3 位数下标 a_100 的最小 n"),
    (10000,      "中/回绕",  "n ≡ 0 (mod 10000)，检验取模回绕；5 位数下标下限"),
    (123456789,  "大",       "大规模非整十随机值，9 位数下标"),
    (999999999,  "大/近顶格","9 位数下标上限（顶格-1）"),
    (1000000000, "顶格",     "题面上限 n=10^9"),
]


def run_std(inp: str) -> str:
    r = subprocess.run([STD_BIN], input=inp.encode(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=10)
    if r.returncode != 0:
        sys.exit(f"std failed rc={r.returncode} err={r.stderr.decode()!r} in={inp!r}")
    return r.stdout.decode()


def main():
    if not os.path.exists(STD_BIN):
        sys.exit(f"缺少 std 可执行文件：{STD_BIN}\n请先 g++ -O2 -std=c++17 std.cpp -o std")
    os.makedirs(DATA_DIR, exist_ok=True)

    total = len(CASES)
    assert total == 10, f"需要 10 组数据，实际 {total}"
    summary = []
    for idx, (n, layer, note) in enumerate(CASES, 1):
        inp = f"{n}\n"
        in_path = os.path.join(DATA_DIR, f"problem{idx}.in")
        out_path = os.path.join(DATA_DIR, f"problem{idx}.out")

        # 写 .in
        with open(in_path, "w") as f:
            f.write(inp)
            f.flush()
            os.fsync(f.fileno())

        # 用 subprocess 显式跑 std 产 .out
        out = run_std(inp)
        with open(out_path, "w") as f:
            f.write(out)
            f.flush()
            os.fsync(f.fileno())

        # ---- 断言 ----
        assert os.path.getsize(in_path) > 0, f"problem{idx}.in 为空"
        assert os.path.getsize(out_path) > 0, f"problem{idx}.out 为空"
        with open(in_path) as f:
            in_lines = [ln for ln in f.read().split("\n") if ln.strip() != ""]
        assert len(in_lines) == 1 and in_lines[0].strip() == str(n), \
            f"problem{idx}.in 行数/内容异常: {in_lines!r}"
        with open(out_path) as f:
            out_lines = [ln for ln in f.read().split("\n") if ln.strip() != ""]
        assert len(out_lines) == 1, f"problem{idx}.out 应恰好 1 行, 实为 {out_lines!r}"
        val = int(out_lines[0])
        assert 0 <= val < MOD, f"problem{idx}.out 越界: {val}"
        # 重跑一致性
        assert run_std(inp).strip() == out_lines[0].strip(), \
            f"problem{idx}.out 重跑不一致"

        summary.append((idx, n, layer, val, note))
        print(f"problem{idx}: n={n} layer={layer} ans={val}  ({note})")

    # 样例专项校验（题面【输入样例】3 -> 【输出样例】40）
    sample = run_std("3\n").strip()
    assert sample == "40", f"题面样例校验失败: n=3 期望 40, 实为 {sample}"
    print("SAMPLE CHECK: n=3 -> 40 (与题面样例一致) OK")

    # 手算小档校验（依据题面定义逐项手数展开式）
    for n, exp in [(1, 4), (2, 16), (4, 92)]:
        got = run_std(f"{n}\n").strip()
        assert got == str(exp), f"手算校验失败: n={n} 期望 {exp}, 实为 {got}"
    print("HAND CHECK: n=1->4, n=2->16, n=4->92 OK")

    print(f"ALL {total} CASES OK (10 pairs, .out 非空且恰 1 行)")


if __name__ == "__main__":
    main()
