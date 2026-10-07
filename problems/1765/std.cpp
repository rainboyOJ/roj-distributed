// 一本通 1765《树上斐波那契》 标准程序 (std)
// ---------------------------------------------------------------------------
// 来源: 自研。公开网络检索(必应/CSDN/百度/DDG)未找到本题可用的公开代码或题解,
//       故按题面自研, 依据下述数学恒等式 + 树链剖分。
//
// 数学依据 (Fibonacci 加法公式, 对全体整数成立):
//   Fib(a+b) = Fib(a) * Fib(b+1) + Fib(a-1) * Fib(b),
//   其中负数下标约定 Fib(-n) = (-1)^(n+1) * Fib(n), 于是 Fib(0)=0, Fib(-1)=1 ...
//   (可直接由 Fib(m)=Fib(m+2)-Fib(m+1) 双向延拓验证。)
//
// 关键转化:
//   对更新 U X k, 设节点 v 在 X 的子树中, 距离 D = dep[v] - dep[X] (子树内路径唯一
//   经过 X, 故距离 = 深度差)。要加的值 Fib(k+D) 可写为
//       Fib(k + D) = Fib(k - dep[X] + dep[v])
//                  = Fib(K) * Fib(dep[v]+1) + Fib(K-1) * Fib(dep[v]),  K = k - dep[X].
//   其中系数 Fib(K), Fib(K-1) 与 v 无关; 而 Fib(dep[v]) 与 Fib(dep[v]+1) 只依赖于
//   节点静态深度, 是两条固定序列。
//   => "子树内按距离加 Fibonacci" 等价于在 dfs 序的一段连续区间上, 加
//      c1 * (Fib(dep[v]+1) 序列) + c0 * (Fib(dep[v]) 序列), c1=Fib(K), c0=Fib(K-1).
//
// 做法:
//   树链剖分(HLD) 把子树映射为 dfs 序区间 [pos[X], pos[X]+sz[X]-1], 把 X..Y 的
//   路径拆成 O(log n) 个连续区间。
//   线段树: 每个节点静态预存该区间内 s0 = sum Fib(dep[v]) mod M 与
//   s1 = sum Fib(dep[v]+1) mod M; 懒标记 (c0,c1) 表示对该区间每个点 v 加上
//   c0*Fib(dep[v]) + c1*Fib(dep[v]+1)。下传时只需 val += c0*s0 + c1*s1,
//   因为 s0/s1 是静态的, 标记可直接相加。
//   路径询问即对 O(log n) 个区间求和。
//
// 复杂度: 建树 O(n), 单次更新 O(log n), 单次询问 O(log^2 n);
//   n,m <= 1e5, k <= 1e15, 完全在时限(2s)/内存(512MB)内。
//   Fib(K) 用快速倍增(对数时间)计算, K 可负。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;
typedef long long ll;

static const ll MOD = 1000000007LL;

int n, m;
vector<vector<int>> ch;      // 孩子表
vector<int> dep, sz, heavy, fa, top_, pos, revpos;

// 返回 (F(t), F(t+1)) mod MOD, 要求 t >= 0
pair<ll, ll> fib_pair(ll t) {
    if (t == 0) return {0, 1};
    pair<ll, ll> p = fib_pair(t >> 1);
    ll a = p.first, b = p.second;
    ll c = a * ((2 * b % MOD - a + MOD) % MOD) % MOD;   // F(2k)
    ll d = (a * a % MOD + b * b % MOD) % MOD;           // F(2k+1)
    if (t & 1) return {d, (c + d) % MOD};
    return {c, d};
}

// Fib(t) mod MOD, 支持 t 为负: Fib(-t) = (-1)^(t+1) Fib(t)
ll fib(ll t) {
    if (t >= 0) return fib_pair(t).first;
    ll t2 = -t;
    ll f = fib_pair(t2).first;
    if ((t2 + 1) & 1) f = (MOD - f) % MOD;
    return f;
}

// ---------------- 线段树: 区间加 (c0,c1), 区间求和 ----------------
vector<ll> val, s0, s1, lz0, lz1;

void build(int node, int l, int r) {
    if (l == r) {
        int v = revpos[l];
        s0[node] = fib(dep[v]);
        s1[node] = fib((ll)dep[v] + 1);
        return;
    }
    int mid = (l + r) >> 1;
    build(node << 1, l, mid);
    build(node << 1 | 1, mid + 1, r);
    s0[node] = (s0[node << 1] + s0[node << 1 | 1]) % MOD;
    s1[node] = (s1[node << 1] + s1[node << 1 | 1]) % MOD;
}

inline void apply(int node, ll c0, ll c1) {
    val[node] = (val[node] + c0 * s0[node] + c1 * s1[node]) % MOD;
    lz0[node] = (lz0[node] + c0) % MOD;
    lz1[node] = (lz1[node] + c1) % MOD;
}

inline void push(int node) {
    if (lz0[node] || lz1[node]) {
        apply(node << 1, lz0[node], lz1[node]);
        apply(node << 1 | 1, lz0[node], lz1[node]);
        lz0[node] = lz1[node] = 0;
    }
}

void update(int node, int l, int r, int ql, int qr, ll c0, ll c1) {
    if (ql <= l && r <= qr) { apply(node, c0, c1); return; }
    push(node);
    int mid = (l + r) >> 1;
    if (ql <= mid) update(node << 1, l, mid, ql, qr, c0, c1);
    if (qr > mid) update(node << 1 | 1, mid + 1, r, ql, qr, c0, c1);
    val[node] = (val[node << 1] + val[node << 1 | 1]) % MOD;
}

ll query(int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return val[node];
    push(node);
    int mid = (l + r) >> 1;
    ll res = 0;
    if (ql <= mid) res += query(node << 1, l, mid, ql, qr);
    if (qr > mid) res += query(node << 1 | 1, mid + 1, r, ql, qr);
    return res % MOD;
}

// ---------------- 树链剖分 ----------------
void build_hld() {
    dep.assign(n + 1, 0);
    sz.assign(n + 1, 1);
    heavy.assign(n + 1, -1);
    top_.assign(n + 1, 0);
    pos.assign(n + 1, 0);
    revpos.assign(n + 1, 0);

    // 迭代 dfs 求先序 order 与深度
    vector<int> order;
    order.reserve(n);
    vector<int> stk;
    stk.push_back(1);
    while (!stk.empty()) {
        int v = stk.back(); stk.pop_back();
        order.push_back(v);
        for (int c : ch[v]) {
            dep[c] = dep[v] + 1;
            stk.push_back(c);
        }
    }
    // 逆先序累加 size / 求重儿子
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int v = order[i];
        sz[v] = 1;
        int best = 0;
        for (int c : ch[v]) {
            sz[v] += sz[c];
            if (sz[c] > best) { best = sz[c]; heavy[v] = c; }
        }
    }
    // 重儿子优先的先序 => 子树连续, 且每条重链连续
    vector<pair<int, int>> st;   // (node, chain_top)
    st.push_back({1, 1});
    int cur = 0;
    while (!st.empty()) {
        pair<int, int> pr = st.back(); st.pop_back();
        int v = pr.first, t = pr.second;
        top_[v] = t;
        pos[v] = ++cur;
        revpos[cur] = v;
        for (int c : ch[v]) if (c != heavy[v]) st.push_back({c, c});
        if (heavy[v] != -1) st.push_back({heavy[v], t});
    }
}

ll path_query(int x, int y) {
    ll res = 0;
    while (top_[x] != top_[y]) {
        if (dep[top_[x]] < dep[top_[y]]) swap(x, y);
        res = (res + query(1, 1, n, pos[top_[x]], pos[x])) % MOD;
        x = fa[top_[x]];
    }
    if (dep[x] > dep[y]) swap(x, y);
    res = (res + query(1, 1, n, pos[x], pos[y])) % MOD;
    return res;
}

int main() {
    scanf("%d %d", &n, &m);
    ch.assign(n + 1, {});
    fa.assign(n + 1, 0);
    for (int i = 2; i <= n; ++i) {
        int x;
        scanf("%d", &x);
        fa[i] = x;
        ch[x].push_back(i);
    }
    build_hld();

    val.assign(4 * n + 4, 0);
    s0.assign(4 * n + 4, 0);
    s1.assign(4 * n + 4, 0);
    lz0.assign(4 * n + 4, 0);
    lz1.assign(4 * n + 4, 0);
    build(1, 1, n);

    char op[8];
    for (int i = 0; i < m; ++i) {
        scanf("%s", op);
        if (op[0] == 'U') {
            int X; ll k;
            scanf("%d %lld", &X, &k);
            ll K = k - dep[X];
            ll c1 = fib(K);       // Fib(K)
            ll c0 = fib(K - 1);   // Fib(K-1)
            update(1, 1, n, pos[X], pos[X] + sz[X] - 1, c0, c1);
        } else {
            int X, Y;
            scanf("%d %d", &X, &Y);
            printf("%lld\n", path_query(X, Y));
        }
    }
    return 0;
}
