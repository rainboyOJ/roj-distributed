// 一本通 1741《电子速度》标准程序（C++17）
//
// 来源：公开题解（CSDN，检索命中，改写为本题标准程序）
//   https://blog.csdn.net/andyc_03/article/details/109166304
//      《【树状数组】ybtoj1741 电子速度》
//   https://blog.csdn.net/qq_40900472/article/details/106714764
//      《【高手训练】【树状数组】电子速度》
//   两篇题解给出同一做法（三个树状数组），本程序按其思路重写（快读 + 快写，适配 n,m ≤ 10^6）。
//
// 题意：平面上 n 个电子，第 i 个初始速度 v_i = (x_i, y_i)。
//   操作 1 p x y ：把 v_p 改为 (x, y)；
//   操作 2 l r   ：询问 Σ_{l≤i<j≤r} |v_i × v_j|² ，答案对 20170927 取模。
//
// 推导（叉积展开为三个前缀和的组合）：
//   Σ_{i<j} (x_i y_j − x_j y_i)²
//     = Σ_{i<j} x_i²y_j² + Σ_{i<j} x_j²y_i² − 2 Σ_{i<j} x_i x_j y_i y_j
//     = Σ_{i≠j} x_i² y_j² − 2 Σ_{i<j} (x_i y_i)(x_j y_j)
//     = ( Σ x_i² )·( Σ y_i² ) − ( Σ x_i y_i )²        （对任意 i≠j 求和的分拆）
//   所以只需维护三个量：P = Σ x², Q = Σ y², R = Σ x·y；
//   区间答案 = (P_R·Q_R − R_R²) mod 20170927（区间前缀相减即得区间内的三个量）。
//
// 数据结构：三棵 Fenwick 树分别维护 P、Q、R（单点修改 O(log n)，前缀查询 O(log n)）。
// 复杂度：时间 O((n + m) log n)，空间 O(n)（约 32 MB，n = 10^6）。
// 取模注意：树内各结点恒保存在 [0, MOD)，加法后至多 2·MOD−2 < 2^31，一次减法即可；
// 查询累加量 < 21·MOD，仍在 long long 范围内，最后统一取模。
// 答案 = (P·Q − R²) mod MOD：P·Q < MOD² ≈ 4.07e14，long long 内精确。

#include <cstdio>
#include <cstdlib>

static const int MOD = 20170927;
static const int MAXN = 1000000 + 5;

static int n;
static int X[MAXN], Y[MAXN];            // 当前每个电子的速度
static long long TA[MAXN];              // Fenwick: Σ x²
static long long TB[MAXN];              // Fenwick: Σ y²
static long long TC[MAXN];              // Fenwick: Σ x·y

// ── 快速输入 ──
static char inbuf[1 << 20];
static int inpos = 0, inlen = 0;

static inline int gc() {
    if (inpos == inlen) {
        inlen = (int)fread(inbuf, 1, sizeof(inbuf), stdin);
        inpos = 0;
        if (inlen <= 0) return -1;
    }
    return (unsigned char)inbuf[inpos++];
}

static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

// ── 快速输出 ──
static char outbuf[1 << 20];
static int outpos = 0;

static inline void flushOut() {
    if (outpos > 0) { fwrite(outbuf, 1, (size_t)outpos, stdout); outpos = 0; }
}

static inline void outInt(long long v) {
    char tmp[24];
    int k = 0;
    if (v == 0) tmp[k++] = '0';
    while (v > 0) { tmp[k++] = (char)('0' + (int)(v % 10)); v /= 10; }
    if (outpos + k + 1 > (int)sizeof(outbuf)) flushOut();
    while (k > 0) outbuf[outpos++] = tmp[--k];
    outbuf[outpos++] = '\n';
}

// Fenwick：位置 pos 起加 v（v ∈ [0, MOD)），树内恒保存在 [0, MOD)
// 注：pos<1 时直接返回（题面保证 1≤p≤n，此处仅作防御，避免 pos=0 时 lowbit=0 死循环）
static inline void add(long long *t, int pos, long long v) {
    if (pos < 1) return;
    for (; pos <= n; pos += pos & (-pos)) {
        t[pos] += v;
        if (t[pos] >= MOD) t[pos] -= MOD;
    }
}

// 前缀和（对 MOD 取模，结果 ∈ [0, MOD)）
static inline long long pref(const long long *t, int pos) {
    if (pos > n) pos = n;
    long long s = 0;
    for (; pos > 0; pos -= pos & (-pos)) s += t[pos];
    return s % MOD;
}

int main() {
    n = readInt();
    int m = readInt();
    for (int i = 1; i <= n; i++) {
        int x = readInt() % MOD;
        int y = readInt() % MOD;
        X[i] = x; Y[i] = y;
        add(TA, i, (long long)x * x % MOD);
        add(TB, i, (long long)y * y % MOD);
        add(TC, i, (long long)x * y % MOD);
    }
    for (int q = 0; q < m; q++) {
        int op = readInt();
        if (op == 1) {
            int p = readInt();
            int x = readInt() % MOD;
            int y = readInt() % MOD;
            int ox = X[p], oy = Y[p];
            long long d;
            d = ((long long)x * x - (long long)ox * ox) % MOD;
            if (d < 0) d += MOD;
            add(TA, p, d);
            d = ((long long)y * y - (long long)oy * oy) % MOD;
            if (d < 0) d += MOD;
            add(TB, p, d);
            d = ((long long)x * y - (long long)ox * oy) % MOD;
            if (d < 0) d += MOD;
            add(TC, p, d);
            X[p] = x; Y[p] = y;
        } else {
            int l = readInt(), r = readInt();
            long long p = (pref(TA, r) - pref(TA, l - 1) + MOD) % MOD;
            long long q2 = (pref(TB, r) - pref(TB, l - 1) + MOD) % MOD;
            long long rr = (pref(TC, r) - pref(TC, l - 1) + MOD) % MOD;
            long long ans = (p * q2 - rr * rr) % MOD;
            if (ans < 0) ans += MOD;
            outInt(ans);
        }
    }
    flushOut();
    return 0;
}
