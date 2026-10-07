// 一本通 1780《修墙》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 检索方式：题面特征句精确搜索（CSDN 站内搜「白格 黑格 矩阵 联通块 询问 矩形 一本通」
// 命中 2 篇）——本题原题为 GDSOI2018 模拟赛 4.19 的 T《修墙》，题面文字逐字一致：
//   [1] https://blog.csdn.net/eric1561759334/article/details/104567067
//       《【JZOJ GDSOI2018模拟4.19】修墙》—— 完整贴出题面（含 "其中用户为白格，墙为黑格"、
//       "地图上一开始只有一个白格"、样例 4 / 1 3 3 0、子任务表），并给出关键思路：
//         * 0 起编号后 (i,j) 为白格 <=> (i & j) == 0（每次迭代相当于新增一个二进制位，
//           并把该位全为 1 的部分全染黑）；
//         * 连通块数可拆成"行 x1 上的一维部分 + 列 y1 上的一维部分 - 左上角为白格"；
//         * 一维部分即统计满足 (j & M) == 0 的 j 的个数（M 由 x1 的 1 位与末尾 0 位构造），
//           "直接找 <= r 的最大的这样的数"，复杂度 O(q log x)。
//   [2] https://blog.csdn.net/alan_cty/article/details/80019412
//       《【GDSOI2018模拟4.19】修墙》—— 同题另一篇题解（站点反爬 403，仅确认标题与题源；
//       题源与 [1] 一致，无冲突）。
//   站内检索另见《【TEST190325】GDSOI2018模拟4.19 简要题解》
//   https://blog.csdn.net/corsica6/article/details/88803699 （同一场模拟赛的其它题，未含本题）。
// 依据：以上来源给出同一结论（白格判据 i&j==0 + 降维成两个一维计数），与题面样例一致，
// 故按其思路改写为下述"数位 DP 计数"实现（非盲抄；[1] 只给了思路与 O(q log x) 结论，
// 未给出可直接运行的完整代码，本文按其思路自研补齐计数函数）。
// =============================================================================
//
// 题面数据范围（content.md 子任务表）：
//   子任务1  q <= 300    , x2,y2 <= 300
//   子任务2  q <= 3000   , x2,y2 <= 3000
//   子任务3  q <= 100000 , x2,y2 <= 1e9
//   子任务4  q <= 1e6    , x2,y2 <= 1e9
// 限制：2000 ms / 1024 MB（config.json）。
//
// ------------------------------- 算法 -------------------------------
// 1) 0 起编号（下文 (i,j) 表示第 i 行第 j 列，均从 0 开始；输入减 1 即可）：
//    W(i,j) <=> (i & j) == 0。
//    证明：迭代一次即把下标二进制多一位，(a,b) 四象限中 (0,0)(0,1)(1,0) 是旧图、(1,1) 全黑，
//    于是 W(i,j) <=> 最高位不同时为 1 且低位递归成立 <=> i&j == 0。
//
// 2) 白格图是一棵树（无环），故矩形内连通块数 = 白格数 - 相邻白格边数；
//    更直接地：给每个白格定义唯一的"父亲"= 唯一的那个白邻居，其行下标或列下标减 1：
//      设 lsb(x) = x 的最低位 1 的位置（规定 lsb(0) = +inf）：
//        lsb(i) < lsb(j)  =>  (i-1,j) 是白格且 (i,j-1) 是黑格  =>  父亲 (i-1,j)
//        lsb(j) < lsb(i)  =>  (i,j-1) 是白格且 (i-1,j) 是黑格  =>  父亲 (i,j-1)
//      （(0,0) 无父亲，是全局唯一的树根；由 i&j==0 知 lsb(i)!=lsb(j) 除非 i=j=0。）
//    于是：矩形 R=[x1,x2]x[y1,y2] 内的连通块数 = R 内父亲落在 R 外的白格数：
//       父亲 (i-1,j) 出界 <=> i == x1 且 lsb(i) < lsb(j)
//       父亲 (i,j-1) 出界 <=> j == y1 且 lsb(j) < lsb(i)
//      => 答案 = A + B + [ (x1,y1) == (0,0) ]，其中
//        A = #{ j in [y1,y2] : (x1 & j) == 0 且 lsb(j) > lsb(x1) }     (x1 == 0 时 A = 0)
//        B = #{ i in [x1,x2] : (i & y1) == 0 且 lsb(i) > lsb(y1) }     (y1 == 0 时 B = 0)
//    说明：x1>0 时设 p = lsb(x1)，则 "x1&j==0 且 lsb(j)>p" <=> j & Mx == 0，
//          Mx = x1 | (2^p - 1)（x1 的 bit p 为 1，故与"低 p 位清零"合并成一个掩码）；
//          y1 同理得 My。这与来源 [1] 的"两个一维部分 - 左上角白格"完全等价
//          （一维部分就是该行/列的极大白段数，其起点集合正是 { j : j & M == 0 }）。
//
// 3) countFree(X, M) = #{ j in [0, X] : (j & M) == 0 }：数位 DP，从高位到低位枚举，
//    当 X 的当前位为 1 时，令 j 该位取 0，则低位可任取 ~M 的子集：
//      贡献 2^(低位中 M 为 0 的位数)；
//    若该位 M 也为 1 则无法继续与 X 前缀相同，直接返回；否则继续（j 该位取 1）。
//    循环结束再补上 j == X 本身（当 (X & M) == 0）。O(30) 每次。
//    区间计数 [l,r] = countFree(r,M) - countFree(l-1,M)。
//
// 复杂度：每组询问 O(log)（4 次 countFree，每次 <= 31 步），q <= 1e6 时约 1.2e8 次基本操作，
//        实测远小于 2000 ms（见 gen-report.md）。答案上界约 2e9，用 long long 存储。
//
// 正确性自检（题面样例）：
//   1 1 5 5 -> 1 ; 2 2 3 6 -> 3 ; 4 2 7 5 -> 3 ; 2 2 2 2 -> 0

#include <cstdio>
#include <cstring>
#include <cstdint>

namespace fastio {
const size_t IN_BUF = 1u << 20;
char ibuf[IN_BUF];
size_t ipos = 0, ilen = 0;

inline int gc() {
    if (ipos == ilen) {
        ilen = fread(ibuf, 1, IN_BUF, stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return (unsigned char)ibuf[ipos++];
}

inline bool readInt(long long &out) {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    if (c == -1) return false;
    long long x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    out = x;
    return true;
}

const size_t OUT_BUF = 1u << 20;
char obuf[OUT_BUF];
size_t opos = 0;

inline void flushOut() {
    if (opos) { fwrite(obuf, 1, opos, stdout); opos = 0; }
}
inline void pc(char c) {
    if (opos == OUT_BUF) flushOut();
    obuf[opos++] = c;
}
inline void writeInt(long long x) {
    if (x <= 0) { pc('0'); pc('\n'); return; }   // 答案恒 >= 0
    char tmp[24];
    int n = 0;
    while (x > 0) { tmp[n++] = (char)('0' + (int)(x % 10)); x /= 10; }
    while (n > 0) pc(tmp[--n]);
    pc('\n');
}
}  // namespace fastio

// 坐标上界 1e9 < 2^30，故只看 bit 0..30
static const int TOPBIT = 30;

// #{ j in [0, X] : (j & M) == 0 }，X < 0 返回 0
static inline long long countFree(long long X, unsigned int M) {
    if (X < 0) return 0;
    long long res = 0;
    for (int b = TOPBIT; b >= 0; --b) {
        if ((X >> b) & 1LL) {
            // 令 j 的第 b 位取 0，则低位可任取（只能取 ~M 的位）
            long long lowMask = (1LL << b) - 1;
            int freeBits = b - __builtin_popcountll((unsigned long long)(M & (unsigned int)lowMask));
            res += 1LL << freeBits;
            if ((M >> b) & 1u) return res;   // 该位 M=1，j 无法与 X 前缀相同，结束
        }
        // X 该位为 0：j 该位取 0（与 X 相同），继续
    }
    if ((X & (long long)M) == 0) ++res;      // j == X 本身
    return res;
}

int main() {
    long long q;
    if (!fastio::readInt(q)) return 0;       // 空输入安全退出
    for (long long t = 0; t < q; ++t) {
        long long x1, y1, x2, y2;
        if (!fastio::readInt(x1)) break;
        if (!fastio::readInt(y1)) break;
        if (!fastio::readInt(x2)) break;
        if (!fastio::readInt(y2)) break;

        long long X1 = x1 - 1, Y1 = y1 - 1, X2 = x2 - 1, Y2 = y2 - 1;
        long long ans = 0;

        if (X1 > 0) {                        // A：第 x1 行上的"根"白格
            int p = __builtin_ctzll((unsigned long long)X1);
            unsigned int Mx = (unsigned int)(X1 | ((1LL << p) - 1));
            ans += countFree(Y2, Mx) - countFree(Y1 - 1, Mx);
        }
        if (Y1 > 0) {                        // B：第 y1 列上的"根"白格
            int p = __builtin_ctzll((unsigned long long)Y1);
            unsigned int My = (unsigned int)(Y1 | ((1LL << p) - 1));
            ans += countFree(X2, My) - countFree(X1 - 1, My);
        }
        if (X1 == 0 && Y1 == 0) ans += 1;    // 全局树根 (0,0) 本身

        fastio::writeInt(ans);
    }
    fastio::flushOut();
    return 0;
}
