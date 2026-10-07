// std.cpp —— 一本通 1764《社会送温暖》(目标 ROJ 1764)
//
// 来源说明 / 依据：
//   * 未找到公开题解。已用题面特征句在 Bing / 百度 / CSDN / DuckDuckGo 精确检索
//     （如 "社会送温暖" + 树/等差数列/等比数列、"对链接它们的道路上的点"、
//       "一本通 1764 社会送温暖"），均无本题（社会送温暖）的公开 C++ 解法，
//     故本题为自研实现。算法依据为标准数据结构结论：
//       - 树上路径操作 + 路径求和 → 树链剖分 (HLD) 把路径拆成 O(log n) 段连续 dfn 区间；
//       - 段内维护 "位置 p 的加/改值是关于 p 的线性函数 / 2^{±p} 型等比函数" → 线段树懒标记。
//   * 题面特征：路径按 u→v 顺序编号，4 种区间加/赋值（等差 / 等比公比 2），路径和询问，答案模 P。
//   * 关键点：模数 P 任意（1<=P<=1e7，不必为质数），故 2 不能求逆元。
//     本实现把等比懒标记锚定在区间端点（左端 A*2^{p-l} 或右端 B*2^{r-p}），
//     下传时只需乘以 2 的非负次幂，全程只用 pow2[k]=2^k mod P，不涉及除法/逆元。
//     因此形如 value(p)=A*2^{p-l}+B*2^{r-p}+c0+c1*p 的函数族在 pushdown 时封闭。
//   * 路径编号（用题面样例验证过）：
//       设 L=lca(u,v)，u 侧节点 x 的编号 = dep[u]-dep[x]+1；v 侧节点 x 的编号 = dep[u]+dep[x]-2dep[L]+1。
//     于是 u 侧段内编号随 dfn 递减（右端点锚定），v 侧段内编号随 dfn 递增（左端点锚定）。
//
// 复杂度 O((n+q) log^2 n)。
//
// 编译：g++ -O2 -o std std.cpp

#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
typedef long long ll;

static const int MAXN = 100005;
int n, q;
ll P;

// ---------- 邻接表 ----------
int eh[MAXN], enxt[2 * MAXN], eto[2 * MAXN], ecnt;
inline void addEdge(int u, int v) { eto[ecnt] = v; enxt[ecnt] = eh[u]; eh[u] = ecnt++; }

// ---------- HLD ----------
int dep[MAXN], par[MAXN], sz[MAXN], heavy[MAXN], head_[MAXN], dfn[MAXN], ord[MAXN];
ll val[MAXN], arr[MAXN];   // val[node] 初值；arr[dfn] 展平后初值

// ---------- 预处理 2 的幂 & 位置前缀和 ----------
ll pow2[MAXN + 2];
ll pre[MAXN + 2];          // pre[i] = (1+2+...+i) mod P

// ---------- 线段树 ----------
// 懒标记含义：待下传给子区间的 “函数”，对区间 [l,r] 内位置 p：
//     f(p) = lzA * 2^{p-l} + lzB * 2^{r-p} + lzC0 + lzC1 * p     (mod P)
// hasSet=false 表示 “对子区间加上 f”；hasSet=true 表示 “把子区间赋值为 f”。
ll sumv[4 * MAXN];
ll lzA[4 * MAXN], lzB[4 * MAXN], lzC0[4 * MAXN], lzC1[4 * MAXN];
bool hasSet[4 * MAXN];

inline ll sumRangeP(int l, int r) {
    ll res = pre[r] - pre[l - 1];
    if (res < 0) res += P;
    return res;
}

// 计算函数 f 在区间 [l,r] 上的和
inline ll funcSum(ll A, ll B, ll c0, ll c1, int l, int r) {
    int len = r - l + 1;
    ll g = pow2[len] - 1;
    if (g < 0) g += P;
    ll res = (A % P) * g % P;
    res = (res + (B % P) * g) % P;
    res = (res + (c0 % P) * (len % P)) % P;
    res = (res + (c1 % P) * sumRangeP(l, r)) % P;
    return res;
}

inline void applyAdd(int node, int l, int r, ll A, ll B, ll c0, ll c1) {
    A %= P; B %= P; c0 %= P; c1 %= P;
    sumv[node] = (sumv[node] + funcSum(A, B, c0, c1, l, r)) % P;
    lzA[node] = (lzA[node] + A) % P;
    lzB[node] = (lzB[node] + B) % P;
    lzC0[node] = (lzC0[node] + c0) % P;
    lzC1[node] = (lzC1[node] + c1) % P;
    // hasSet 保持不变：已有 “赋值 f” 再 “加 g” ⇒ 仍为赋值 f+g
}

inline void applySet(int node, int l, int r, ll A, ll B, ll c0, ll c1) {
    A %= P; B %= P; c0 %= P; c1 %= P;
    sumv[node] = funcSum(A, B, c0, c1, l, r);
    hasSet[node] = true;
    lzA[node] = A; lzB[node] = B; lzC0[node] = c0; lzC1[node] = c1;
}

inline void pushdown(int node, int l, int r) {
    if (!hasSet[node] && lzA[node] == 0 && lzB[node] == 0 && lzC0[node] == 0 && lzC1[node] == 0)
        return;
    int mid = (l + r) >> 1;
    int lenl = mid - l + 1, lenr = r - mid;
    ll A = lzA[node], B = lzB[node], c0 = lzC0[node], c1 = lzC1[node];
    // 左子 [l,mid]：左锚不变 A；右锚由 r 变 mid ⇒ B*2^{r-mid}=B*2^{lenr}
    ll Al = A, Bl = B * pow2[lenr] % P;
    // 右子 [mid+1,r]：右锚不变 B；左锚由 l 变 mid+1 ⇒ A*2^{mid+1-l}=A*2^{lenl}
    ll Ar = A * pow2[lenl] % P, Br = B;
    if (hasSet[node]) {
        applySet(node << 1, l, mid, Al, Bl, c0, c1);
        applySet(node << 1 | 1, mid + 1, r, Ar, Br, c0, c1);
        hasSet[node] = false;
    } else {
        applyAdd(node << 1, l, mid, Al, Bl, c0, c1);
        applyAdd(node << 1 | 1, mid + 1, r, Ar, Br, c0, c1);
    }
    lzA[node] = lzB[node] = lzC0[node] = lzC1[node] = 0;
}

void build(int node, int l, int r) {
    if (l == r) { sumv[node] = arr[l] % P; return; }
    int mid = (l + r) >> 1;
    build(node << 1, l, mid);
    build(node << 1 | 1, mid + 1, r);
    sumv[node] = (sumv[node << 1] + sumv[node << 1 | 1]) % P;
}

// 说明：传入的 (A,B) 以“查询区间” (ql,qr) 为锚：A 锚在 p=ql，B 锚在 p=qr。
// 命中的整段节点 [l,r] 需要把锚平移到该节点自身两端（指数 l-ql、qr-r 均非负），
// 否则线段树内部节点的坐标与函数坐标不一致。
void updAdd(int node, int l, int r, int ql, int qr, ll A, ll B, ll c0, ll c1) {
    if (ql <= l && r <= qr) {
        applyAdd(node, l, r, A * pow2[l - ql] % P, B * pow2[qr - r] % P, c0, c1);
        return;
    }
    pushdown(node, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) updAdd(node << 1, l, mid, ql, qr, A, B, c0, c1);
    if (qr > mid) updAdd(node << 1 | 1, mid + 1, r, ql, qr, A, B, c0, c1);
    sumv[node] = (sumv[node << 1] + sumv[node << 1 | 1]) % P;
}

void updSet(int node, int l, int r, int ql, int qr, ll A, ll B, ll c0, ll c1) {
    if (ql <= l && r <= qr) {
        applySet(node, l, r, A * pow2[l - ql] % P, B * pow2[qr - r] % P, c0, c1);
        return;
    }
    pushdown(node, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) updSet(node << 1, l, mid, ql, qr, A, B, c0, c1);
    if (qr > mid) updSet(node << 1 | 1, mid + 1, r, ql, qr, A, B, c0, c1);
    sumv[node] = (sumv[node << 1] + sumv[node << 1 | 1]) % P;
}

ll query(int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return sumv[node];
    pushdown(node, l, r);
    int mid = (l + r) >> 1;
    ll res = 0;
    if (ql <= mid) res += query(node << 1, l, mid, ql, qr);
    if (qr > mid) res += query(node << 1 | 1, mid + 1, r, ql, qr);
    return res % P;
}

// ---------- 单段应用 ----------
// 段 [l,r]（dfn 区间）。anchorIdx = 锚点处的路径编号：
//   leftAnchored=true  → 锚点在最左端 p=l（编号随 p 递增，斜率 +1），用于 v 侧；
//   leftAnchored=false → 锚点在最右端 p=r（编号随 p 递减，斜率 -1），用于 u 侧。
inline void applySeg(int l, int r, int anchorIdx, bool leftAnchored, int op, ll a, ll d) {
    a %= P; d %= P;
    ll A = 0, B = 0, c0 = 0, c1 = 0;
    if (op == 1 || op == 3) {
        if (leftAnchored) {
            // i(p) = anchorIdx + (p-l)  ⇒  val = a + (i-1)d = [a + (anchorIdx-l-1)d] + d*p
            ll k = (ll)anchorIdx - l - 1;
            k %= P; if (k < 0) k += P;
            c0 = (a + k * d) % P;
            c1 = d;
        } else {
            // i(p) = anchorIdx + (r-p)  ⇒  val = a + (i-1)d = [a + (anchorIdx+r-1)d] - d*p
            ll k = (ll)anchorIdx + r - 1;
            k %= P; if (k < 0) k += P;
            c0 = (a + k * d) % P;
            c1 = (P - d) % P;
        }
    } else { // op == 2 || op == 4 等比，公比 2
        if (leftAnchored) {
            // i(p) = anchorIdx + (p-l)  ⇒  val = a*2^{i-1} = (a*2^{anchorIdx-1}) * 2^{p-l}
            A = a * pow2[anchorIdx - 1] % P;
        } else {
            // i(p) = anchorIdx + (r-p)  ⇒  val = a*2^{i-1} = (a*2^{anchorIdx-1}) * 2^{r-p}
            B = a * pow2[anchorIdx - 1] % P;
        }
    }
    if (op == 1 || op == 2) updAdd(1, 1, n, l, r, A, B, c0, c1);
    else                    updSet(1, 1, n, l, r, A, B, c0, c1);
}

inline int lca(int u, int v) {
    while (head_[u] != head_[v]) {
        if (dep[head_[u]] < dep[head_[v]]) swap(u, v);
        u = par[head_[u]];
    }
    return dep[u] < dep[v] ? u : v;
}

// ---------- 路径操作 ----------
void pathUpdate(int u, int v, int op, ll a, ll d) {
    int U0 = u, V0 = v;
    int L = lca(u, v);
    // u 侧：编号 i(x) = dep[U0]-dep[x]+1，右端锚定
    int x = U0;
    while (dep[head_[x]] > dep[L]) {
        int l = dfn[head_[x]], r = dfn[x];
        applySeg(l, r, dep[U0] - dep[x] + 1, false, op, a, d);
        x = par[head_[x]];
    }
    if (x != L) {
        int l = dfn[L] + 1, r = dfn[x];
        applySeg(l, r, dep[U0] - dep[x] + 1, false, op, a, d);
    }
    // v 侧：编号 i(x) = dep[U0]+dep[x]-2dep[L]+1，左端锚定
    int y = V0;
    while (dep[head_[y]] > dep[L]) {
        int l = dfn[head_[y]], r = dfn[y];
        applySeg(l, r, dep[U0] + dep[head_[y]] - 2 * dep[L] + 1, true, op, a, d);
        y = par[head_[y]];
    }
    if (y != L) {
        int l = dfn[L] + 1, r = dfn[y];
        applySeg(l, r, dep[U0] - dep[L] + 2, true, op, a, d);
    }
    // L 自身（点）
    {
        int p = dfn[L];
        applySeg(p, p, dep[U0] - dep[L] + 1, true, op, a, d);
    }
}

ll pathQuery(int u, int v) {
    int U0 = u, V0 = v;
    int L = lca(u, v);
    ll res = 0;
    int x = U0;
    while (dep[head_[x]] > dep[L]) {
        res += query(1, 1, n, dfn[head_[x]], dfn[x]);
        x = par[head_[x]];
    }
    if (x != L) res += query(1, 1, n, dfn[L] + 1, dfn[x]);
    int y = V0;
    while (dep[head_[y]] > dep[L]) {
        res += query(1, 1, n, dfn[head_[y]], dfn[y]);
        y = par[head_[y]];
    }
    if (y != L) res += query(1, 1, n, dfn[L] + 1, dfn[y]);
    res += query(1, 1, n, dfn[L], dfn[L]);
    return res % P;
}

// ---------- 快读 ----------
static char buf[1 << 25];
static size_t bufLen = 0, bufPos = 0;
inline int readInt() {
    if (bufPos >= bufLen) { bufLen = fread(buf, 1, sizeof(buf), stdin); bufPos = 0; }
    while (bufPos < bufLen && (buf[bufPos] < '0' || buf[bufPos] > '9') && buf[bufPos] != '-') bufPos++;
    bool neg = false;
    if (bufPos < bufLen && buf[bufPos] == '-') { neg = true; bufPos++; }
    ll x = 0;
    while (bufPos < bufLen && buf[bufPos] >= '0' && buf[bufPos] <= '9') { x = x * 10 + (buf[bufPos] - '0'); bufPos++; }
    return neg ? (int)(-x) : (int)x;
}
inline ll readLL() {
    if (bufPos >= bufLen) { bufLen = fread(buf, 1, sizeof(buf), stdin); bufPos = 0; }
    while (bufPos < bufLen && (buf[bufPos] < '0' || buf[bufPos] > '9') && buf[bufPos] != '-') bufPos++;
    bool neg = false;
    if (bufPos < bufLen && buf[bufPos] == '-') { neg = true; bufPos++; }
    ll x = 0;
    while (bufPos < bufLen && buf[bufPos] >= '0' && buf[bufPos] <= '9') { x = x * 10 + (buf[bufPos] - '0'); bufPos++; }
    return neg ? -x : x;
}

int main() {
    n = readInt(); q = readInt(); P = readLL();
    memset(eh, -1, sizeof(int) * (n + 1));
    ecnt = 0;
    for (int i = 0; i < n - 1; i++) {
        int u = readInt(), v = readInt();
        addEdge(u, v); addEdge(v, u);
    }
    for (int i = 1; i <= n; i++) val[i] = readLL();

    // ---- HLD: BFS 求 par/dep/order ----
    int qh = 0, qt = 0;
    static int que[MAXN];
    que[qt++] = 1; par[1] = 0; dep[1] = 0;
    while (qh < qt) {
        int u = que[qh++];
        for (int e = eh[u]; e != -1; e = enxt[e]) {
            int v = eto[e];
            if (v == par[u]) continue;
            par[v] = u; dep[v] = dep[u] + 1; que[qt++] = v;
        }
    }
    for (int i = 1; i <= n; i++) ord[i] = que[i - 1];
    for (int i = n; i >= 1; i--) {
        int u = ord[i];
        sz[u] = 1; heavy[u] = 0;
        for (int e = eh[u]; e != -1; e = enxt[e]) {
            int v = eto[e];
            if (v == par[u]) continue;
            sz[u] += sz[v];
            if (heavy[u] == 0 || sz[v] > sz[heavy[u]]) heavy[u] = v;
        }
    }
    // ---- 分配 dfn：重链连续 ----
    {
        static int stk[MAXN];
        int top = 0;
        stk[top++] = 1; head_[1] = 1;
        int cur = 0;
        while (top) {
            int u = stk[--top];
            dfn[u] = ++cur;
            // 先压轻儿子，最后压重儿子（后压先出，保证重链连续）
            for (int e = eh[u]; e != -1; e = enxt[e]) {
                int v = eto[e];
                if (v == par[u] || v == heavy[u]) continue;
                head_[v] = v; stk[top++] = v;
            }
            if (heavy[u]) { head_[heavy[u]] = head_[u]; stk[top++] = heavy[u]; }
        }
    }
    for (int i = 1; i <= n; i++) arr[dfn[i]] = val[i] % P;

    // ---- pow2 / pre ----
    pow2[0] = 1 % P;
    for (int i = 1; i <= n + 1; i++) pow2[i] = pow2[i - 1] * 2 % P;
    pre[0] = 0;
    for (int i = 1; i <= n + 1; i++) pre[i] = (pre[i - 1] + i) % P;

    build(1, 1, n);

    for (int i = 0; i < q; i++) {
        int op = readInt(), u = readInt(), v = readInt();
        if (op == 5) {
            printf("%lld\n", pathQuery(u, v));
        } else if (op == 1 || op == 3) {
            ll a = readLL(), d = readLL();
            pathUpdate(u, v, op, a, d);
        } else { // op == 2 || op == 4
            ll a = readLL();
            pathUpdate(u, v, op, a, 0);
        }
    }
    return 0;
}
