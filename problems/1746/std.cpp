// 一本通 1746《矩阵最值》标程
//
// 来源 URL（按题面特征句「现在小Q有K个问题，每次询问一个以x1行y1列为左上角，
// x2行y2列为右下角的子矩阵的最大值」检索命中，另有题名检索命中同一题的
// YbtOJ 编号「数据结构 RMQ 课过 例4」）：
//   https://blog.csdn.net/ssl_guyixin/article/details/117474954
//     （该文即本题题解，给出二维 ST 表 AC 代码；本文件在其思路上重写：
//       改用 4 象限递推、动态分配、快速读入/输出，避免 #define int long long）
//   https://blog.csdn.net/weixin_43346722/article/details/115048079
//     （题名【ybt高效进阶4-3-4】矩阵最值，同题同解，二次确认题意）
//
// 题意：n 行 m 列矩阵，K 次询问子矩阵最大值。n,m<=250，K<=1e6，0<=a[i][j]<2^31。
//
// 算法：二维稀疏表（ST）。st[a][b][i][j] = 以 (i,j) 为左上角、2^a 行 x 2^b 列
//       的子矩阵最大值。
//   预处理 O(n*m*log n*log m)：按 4 象限递推
//     st[a][b][i][j] = max( st[a-1][b-1][i][j], st[a-1][b-1][i+dA][j],
//                           st[a-1][b-1][i][j+dB], st[a-1][b-1][i+dA][j+dB] )
//     （a=0 或 b=0 的两条边退化为两半合并，等价且更省）
//   询问 O(1)：a = lg(x2-x1+1), b = lg(y2-y1+1)，四角覆盖取 max。
// 复杂度：时间 O(n*m*log n*log m + K)；空间 O(log n*log m*n*m)。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra -o std std.cpp
#include <cstdio>
#include <cstdlib>
#include <vector>

namespace {

const int BUFSZ = 1 << 20;
char inbuf[BUFSZ];
int inlen = 0, inpos = 0;
char outbuf[BUFSZ];
int outpos = 0;

inline int gc() {
    if (inpos == inlen) {
        inlen = (int)std::fread(inbuf, 1, BUFSZ, stdin);
        inpos = 0;
        if (inlen <= 0) return -1;
    }
    return (unsigned char)inbuf[inpos++];
}

// 读入非负整数（题面 a[i][j] >= 0；带符号容错，便于复用）
inline long long readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9') && c != '-') c = gc();
    bool neg = false;
    if (c == '-') {
        neg = true;
        c = gc();
    }
    long long v = 0;
    while (c >= '0' && c <= '9') {
        v = v * 10 + (c - '0');
        c = gc();
    }
    return neg ? -v : v;
}

inline void flushOut() {
    if (outpos) {
        std::fwrite(outbuf, 1, (size_t)outpos, stdout);
        outpos = 0;
    }
}

inline void putChar(char c) {
    if (outpos == BUFSZ) flushOut();
    outbuf[outpos++] = c;
}

inline void writeInt(long long v) {
    if (v < 0) {
        putChar('-');
        v = -v;
    }
    char tmp[24];
    int t = 0;
    if (v == 0) tmp[t++] = '0';
    while (v > 0) {
        tmp[t++] = (char)('0' + (int)(v % 10));
        v /= 10;
    }
    while (t > 0) putChar(tmp[--t]);
}

}  // namespace

int main() {
    // ---- 读入 n, m, K ----
    long long nLL = readInt();
    long long mLL = readInt();
    long long kLL = readInt();
    if (nLL < 1 || mLL < 1) return 0;  // 退化输入保护
    const int n = (int)nLL;
    const int m = (int)mLL;
    const int K = (int)(kLL < 0 ? 0 : kLL);

    // 安全系数：题面上限 250 的 2 倍（512），超出直接拒绝而不是越界
    const int MAXN = 512;
    if (n > MAXN || m > MAXN) {
        std::fprintf(stderr, "FATAL: n=%d m=%d exceeds safety limit %d\n", n, m, MAXN);
        return 1;
    }

    // ---- 取对数表 ----
    std::vector<int> lg(MAXN + 2, 0);
    for (int i = 2; i <= MAXN + 1; ++i) lg[i] = lg[i >> 1] + 1;
    const int LA = lg[n], LB = lg[m];

    // st[a][b][i][j]，i in [1..n], j in [1..m]
    const int dims = (LA + 1) * (LB + 1);
    const size_t plane = (size_t)(n + 1) * (size_t)(m + 1);
    std::vector<long long> st((size_t)dims * plane, 0);
    const size_t strideA = (size_t)(LB + 1) * plane;
    const size_t strideB = plane;
#define ST(a, b, i, j) st[(size_t)(a) * strideA + (size_t)(b) * strideB + (size_t)(i) * (size_t)(m + 1) + (size_t)(j)]

    // ---- 读入矩阵 ----
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) ST(0, 0, i, j) = readInt();

    // ---- 预处理 ----
    for (int a = 0; a <= LA; ++a) {
        const int dA = (a == 0) ? 0 : (1 << (a - 1));
        for (int b = 0; b <= LB; ++b) {
            if (a == 0 && b == 0) continue;  // 已填
            const int dB = (b == 0) ? 0 : (1 << (b - 1));
            const int iLim = n - (1 << a) + 1;
            const int jLim = m - (1 << b) + 1;
            for (int i = 1; i <= iLim; ++i) {
                for (int j = 1; j <= jLim; ++j) {
                    long long v;
                    if (a == 0) {  // 只横向扩：两半
                        v = ST(0, b - 1, i, j);
                        long long w = ST(0, b - 1, i, j + dB);
                        if (w > v) v = w;
                    } else if (b == 0) {  // 只纵向扩：两半
                        v = ST(a - 1, 0, i, j);
                        long long w = ST(a - 1, 0, i + dA, j);
                        if (w > v) v = w;
                    } else {  // 4 象限
                        v = ST(a - 1, b - 1, i, j);
                        long long w = ST(a - 1, b - 1, i + dA, j);
                        if (w > v) v = w;
                        w = ST(a - 1, b - 1, i, j + dB);
                        if (w > v) v = w;
                        w = ST(a - 1, b - 1, i + dA, j + dB);
                        if (w > v) v = w;
                    }
                    ST(a, b, i, j) = v;
                }
            }
        }
    }

    // ---- 回答询问 ----
    for (int q = 0; q < K; ++q) {
        int x1 = (int)readInt(), y1 = (int)readInt();
        int x2 = (int)readInt(), y2 = (int)readInt();
        // 容错：非法/越界询问按题面保证不会出现，这里夹紧以避免 UB
        if (x1 < 1) x1 = 1;
        if (y1 < 1) y1 = 1;
        if (x2 > n) x2 = n;
        if (y2 > m) y2 = m;
        if (x1 > x2 || y1 > y2) {  // 退化区间（题面保证不出现）
            writeInt(0);
            putChar('\n');
            continue;
        }
        const int a = lg[x2 - x1 + 1];
        const int b = lg[y2 - y1 + 1];
        const int dA = 1 << a, dB = 1 << b;
        const int i2 = x2 - dA + 1, j2 = y2 - dB + 1;
        long long v = ST(a, b, x1, y1);
        long long w = ST(a, b, i2, y1);
        if (w > v) v = w;
        w = ST(a, b, x1, j2);
        if (w > v) v = w;
        w = ST(a, b, i2, j2);
        if (w > v) v = w;
        writeInt(v);
        putChar('\n');
    }
    flushOut();
#undef ST
    return 0;
}
