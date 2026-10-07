// 一本通 1760《树上数颜色》 标程（自研实现，无公开题解可参照）
//
// 题意：n 个点的树（根为 1），每点颜色 c_i∈[1,n]。操作：
//   1 u l r : 询问子树 u 中，颜色在 [l,r] 内的颜色种数（至少出现一次）
//   2 u c   : 把 u 的颜色改为 c
//   t=1 时除操作类型外的数需异或上一次询问答案 lastans。
//
// 算法：DFS 序把子树化为连续区间 [tin[u], tout[u]]，于是询问 = 数区间内
// 出现过的、颜色落在 [l,r] 的颜色种数。
//   * 颜色分块（块大小 K=64，每块一个 64 位 bitset）；
//   * 位置（DFS 序）分块（块大小 S）；
//   * 对每个颜色块维护「该颜色块的哪些颜色出现在位置块 b」的 bitset，
//     并对位置块建稀疏表，O(1) 求「位置块区间内出现过的颜色集合」；
//   * 询问：整颜色块用稀疏表直接 popcount；两端不完整颜色块逐色判断
//     （用每个颜色的位置块 bitset + 边界位置扫描）；位置两端不完整块扫描处理。
//   * 修改：更新计数、颜色块 bitset 与颜色的位置块 bitset，重建受影响颜色块稀疏表。
// 复杂度：询问 O((r-l)/64 + S + K)；修改 O(nb·log(nb))，nb=n/S。
// 自研，未经网络题解验证；已用题面样例验证（见 gen-report.md）。
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>
#include <algorithm>
using namespace std;

typedef unsigned long long u64;
typedef unsigned short u16;

static const int INBUF = 1 << 20;
struct FastIn {
    char buf[INBUF];
    int len = 0, pos = 0;
    inline char gc() {
        if (pos == len) { len = (int)fread(buf, 1, INBUF, stdin); pos = 0; if (len <= 0) return 0; }
        return buf[pos++];
    }
    inline int readInt() {
        char c = gc();
        while (c && (c < '0' || c > '9')) c = gc();
        int x = 0;
        while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
        return x;
    }
} fin;

static char outbuf[1 << 22];
static int outlen = 0;
inline void outInt(long long x) {
    if (x == 0) { outbuf[outlen++] = '0'; outbuf[outlen++] = '\n'; return; }
    char tmp[24]; int k = 0;
    while (x > 0) { tmp[k++] = char('0' + x % 10); x /= 10; }
    while (k) outbuf[outlen++] = tmp[--k];
    outbuf[outlen++] = '\n';
}

int n, q, t;
vector<int> col, tin, tout, euler;
vector<int> adjHead, adjNext, adjTo;

// 参数（编译期可用 -DS_PARAM / -DK_PARAM 覆盖，便于小规模调试；默认按上限取值）
#ifndef S_PARAM
#define S_PARAM 1000
#endif
#ifndef K_PARAM
#define K_PARAM 64
#endif
int S = S_PARAM;          // 位置块大小
int K = K_PARAM;          // 颜色块大小（=64，一个 bitset 字）
int nb, cb, levels, nbW;
size_t cbW;            // = cb * (K/64) = cb

vector<u16> cnt;       // (n+1)*nb
vector<u64> Bbits;     // cb*nb
vector<u64> SP;        // levels*nb*cb
vector<u64> cbits;     // (n+1)*nbW
vector<u64> cacheBits; // cb
vector<int> bndSeen;
int stamp = 0;

inline int log2floor(int x) { return 31 - __builtin_clz((unsigned)x); }

void rebuild(int bi) {
    size_t base0 = (size_t)bi;
    for (int b = 0; b < nb; b++)
        SP[(size_t)b * cbW + base0] = Bbits[(size_t)bi * nb + b];
    for (int j = 1; j < levels; j++) {
        int half = 1 << (j - 1);
        size_t prev = (size_t)(j - 1) * nb * cbW;
        size_t cur = (size_t)j * nb * cbW;
        for (int b = 0; b < nb; b++) {
            u64 a = SP[prev + (size_t)b * cbW + base0];
            u64 x = (b + half < nb) ? SP[prev + (size_t)(b + half) * cbW + base0] : 0ULL;
            SP[cur + (size_t)b * cbW + base0] = a | x;
        }
    }
}

void modify(int u, int cnew) {
    int old = col[u];
    if (old == cnew) return;
    int p = tin[u];
    int b = (p - 1) / S;
    int bo = (old - 1) / K, bn = (cnew - 1) / K;
    u16 &co = cnt[(size_t)old * nb + b];
    if (--co == 0) {
        Bbits[(size_t)bo * nb + b] &= ~(1ULL << (old - 1 - bo * K));
        cbits[(size_t)old * nbW + (b >> 6)] &= ~(1ULL << (b & 63));
        rebuild(bo);
    }
    u16 &cn = cnt[(size_t)cnew * nb + b];
    if (cn++ == 0) {
        Bbits[(size_t)bn * nb + b] |= (1ULL << (cnew - 1 - bn * K));
        cbits[(size_t)cnew * nbW + (b >> 6)] |= (1ULL << (b & 63));
        rebuild(bn);
    }
    col[u] = cnew;
}

long long query(int L, int R, int l, int r) {
    if (L > R) return 0;
    if (l < 1) l = 1;
    if (r > n) r = n;
    if (l > r) return 0;
    int pL = (L - 1) / S, pR = (R - 1) / S;
    ++stamp;
    if (pL == pR) {
        int res = 0;
        for (int p = L; p <= R; p++) {
            int c = col[euler[p]];
            if (c >= l && c <= r && bndSeen[c] != stamp) { bndSeen[c] = stamp; res++; }
        }
        return res;
    }
    int fL = pL + 1, fR = pR - 1;
    int cLo = (l - 1) / K, cHi = (r - 1) / K;
    long long ans = 0;
    bool hasFullPos = (fL <= fR);
    if (cLo < cHi) {
        int biFirst = cLo + 1, biLast = cHi - 1;
        if (hasFullPos) {
            int len = fR - fL + 1;
            int j = log2floor(len);
            int half = 1 << j;
            int b1 = fL, b2 = fR - half + 1;
            size_t base1 = (size_t)(j * nb + b1) * cbW;
            size_t base2 = (size_t)(j * nb + b2) * cbW;
            for (int bi = biFirst; bi <= biLast; bi++) {
                u64 res = SP[base1 + bi] | SP[base2 + bi];
                ans += (long long)__builtin_popcountll(res);
                cacheBits[bi] = res;
            }
        } else {
            for (int bi = biFirst; bi <= biLast; bi++) cacheBits[bi] = 0ULL;
        }
    }
    // 边界位置（L,R 所在的块的不完整部分）
    int endA = min(R, (pL + 1) * S);
    for (int p = L; p <= endA; p++) {
        int c = col[euler[p]];
        if (c < l || c > r) continue;
        bndSeen[c] = stamp;
        int bi = (c - 1) / K;
        if (bi > cLo && bi < cHi) {
            u64 bit = 1ULL << (c - 1 - bi * K);
            if (!(cacheBits[bi] & bit)) { cacheBits[bi] |= bit; ans++; }
        }
    }
    int startB = max(L, pR * S + 1);
    for (int p = startB; p <= R; p++) {
        int c = col[euler[p]];
        if (c < l || c > r) continue;
        bndSeen[c] = stamp;
        int bi = (c - 1) / K;
        if (bi > cLo && bi < cHi) {
            u64 bit = 1ULL << (c - 1 - bi * K);
            if (!(cacheBits[bi] & bit)) { cacheBits[bi] |= bit; ans++; }
        }
    }
    // 不完整颜色块：逐色判断是否在 [L,R] 出现
    auto present = [&](int c) -> bool {
        if (bndSeen[c] == stamp) return true;
        if (!hasFullPos) return false;
        const u64 *cb2 = &cbits[(size_t)c * nbW];
        int wl = fL >> 6, wr = fR >> 6;
        if (wl == wr) {
            u64 m = (~0ULL << (fL & 63)) & (~0ULL >> (63 - (fR & 63)));
            return (cb2[wl] & m) != 0;
        }
        if (cb2[wl] & (~0ULL << (fL & 63))) return true;
        if (cb2[wr] & (~0ULL >> (63 - (fR & 63)))) return true;
        for (int w = wl + 1; w < wr; w++) if (cb2[w]) return true;
        return false;
    };
    if (cLo == cHi) {
        for (int c = l; c <= r; c++) if (present(c)) ans++;
    } else {
        int endLo = min(cLo * K + K, n);
        for (int c = l; c <= endLo; c++) if (present(c)) ans++;
        for (int c = cHi * K + 1; c <= r; c++) if (present(c)) ans++;
    }
    return ans;
}

int main() {
    n = fin.readInt(); q = fin.readInt(); t = fin.readInt();
    col.assign(n + 1, 0);
    tin.assign(n + 1, 0); tout.assign(n + 1, 0);
    euler.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) col[i] = fin.readInt();

    adjHead.assign(n + 1, -1);
    adjNext.resize(2 * (n - 1) + 2);
    adjTo.resize(2 * (n - 1) + 2);
    int ec = 0;
    auto addEdge = [&](int u, int v) { adjTo[ec] = v; adjNext[ec] = adjHead[u]; adjHead[u] = ec++; };
    for (int i = 0; i < n - 1; i++) {
        int u = fin.readInt(), v = fin.readInt();
        addEdge(u, v); addEdge(v, u);
    }
    // 迭代 DFS 求 tin/tout
    {
        vector<int> it(n + 1, 0), stk;
        vector<char> vis(n + 1, 0);
        stk.reserve(n);
        int timer = 0;
        stk.push_back(1); vis[1] = 1;
        tin[1] = ++timer; euler[timer] = 1;
        while (!stk.empty()) {
            int u = stk.back();
            int e = adjHead[u];
            bool pushed = false;
            while (e != -1) {
                int v = adjTo[e];
                e = adjNext[e];
                if (!vis[v]) {
                    vis[v] = 1;
                    tin[v] = ++timer; euler[timer] = v;
                    stk.push_back(v);
                    pushed = true;
                    adjHead[u] = e; // 记录进度
                    break;
                }
            }
            if (!pushed) {
                tout[u] = timer;
                stk.pop_back();
            }
        }
    }

    nb = (n + S - 1) / S;
    cb = (n + K - 1) / K;
    cbW = cb;
    nbW = (nb + 63) / 64;
    levels = 1;
    while ((1 << levels) <= nb) levels++;

    cnt.assign((size_t)(n + 1) * nb, 0);
    Bbits.assign((size_t)cb * nb, 0ULL);
    SP.assign((size_t)levels * nb * cb, 0ULL);
    cbits.assign((size_t)(n + 1) * nbW, 0ULL);
    cacheBits.assign(cb, 0ULL);
    bndSeen.assign(n + 1, 0);

    for (int p = 1; p <= n; p++) {
        int c = col[euler[p]];
        int b = (p - 1) / S;
        cnt[(size_t)c * nb + b]++;
        int bi = (c - 1) / K;
        Bbits[(size_t)bi * nb + b] |= (1ULL << (c - 1 - bi * K));
        cbits[(size_t)c * nbW + (b >> 6)] |= (1ULL << (b & 63));
    }
    for (int b = 0; b < nb; b++) {
        for (int bi = 0; bi < cb; bi++) SP[(size_t)b * cbW + bi] = Bbits[(size_t)bi * nb + b];
    }
    for (int j = 1; j < levels; j++) {
        int half = 1 << (j - 1);
        size_t prev = (size_t)(j - 1) * nb * cbW, cur = (size_t)j * nb * cbW;
        for (int b = 0; b < nb; b++) {
            if (b + half < nb) {
                const u64 *A = &SP[prev + (size_t)b * cbW];
                const u64 *Bp = &SP[prev + (size_t)(b + half) * cbW];
                u64 *C = &SP[cur + (size_t)b * cbW];
                for (int bi = 0; bi < cb; bi++) C[bi] = A[bi] | Bp[bi];
            } else {
                const u64 *A = &SP[prev + (size_t)b * cbW];
                u64 *C = &SP[cur + (size_t)b * cbW];
                for (int bi = 0; bi < cb; bi++) C[bi] = A[bi];
            }
        }
    }

    long long lastans = 0;
    for (int i = 0; i < q; i++) {
        int op = fin.readInt();
        if (op == 1) {
            int u = fin.readInt(), l = fin.readInt(), r = fin.readInt();
            if (t == 1) { u ^= (int)lastans; l ^= (int)lastans; r ^= (int)lastans; }
            lastans = query(tin[u], tout[u], l, r);
            outInt(lastans);
        } else {
            int u = fin.readInt(), c = fin.readInt();
            if (t == 1) { u ^= (int)lastans; c ^= (int)lastans; }
            modify(u, c);
        }
    }
    fwrite(outbuf, 1, outlen, stdout);
    return 0;
}
