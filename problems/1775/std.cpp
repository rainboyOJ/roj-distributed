// 一本通 1775《梦中漫步》标程
// 思路：树上随机游走的期望步数（树形 DP + LCA）。
//   以 1 为根。设 f[x] = 从 x 出发走到父亲父亲的期望边数，
//   g[x] = 从父亲出发走到 x 的期望边数。
//   对点 x（度 d[x]，儿子集合 son）：
//     f[x] = 1 + Σ_{c∈son}( f[c] + 1 )  （概率 1/d 上/下抵消后化简）
//          = d[x] + Σ_{c∈son} f[c]
//   由对称性可推出（x 为父亲，y 为儿子）：
//     g[y] = g[x] + f[x] - f[y]
//   于是任意询问 u→v，令 z=LCA(u,v)：
//     答案 = Σ_{x∈(z,u]} f[x] + Σ_{y∈(z,v]} g[y]
//   用树上前缀和 pf[x]=pf[fa]+f[x]、pg[x]=pg[fa]+g[x] 即可 O(1) 回答，
//   LCA 用倍增 O(log N)。所有量均为整数，最后对 1e9+7 取模（用 long long 防溢出）。
// 参考来源（网络题解，已按题面自行改写并编译验证）：
//   https://blog.csdn.net/qq_39897867/article/details/107923662
//   （#数学期望+lca# [ssloj 1457] 树(tree)：给出同一题的 f/g 递推与
//     dfs 前缀和 + 倍增 LCA + f[x]-f[z]+g[y]-g[z] 的解法；
//     其代码未取模、且递归深度按 N=1e5 有爆栈风险，本标程改为迭代 + long long + 取模。）
#include <cstdio>

typedef long long ll;

const int MOD = 1000000007;
const int MAXN = 100005;
const int LOG = 18;              // 2^17 > 1e5

int n, q;
int head[MAXN], nxt[MAXN << 1], to[MAXN << 1], ecnt;
int deg[MAXN];
int par[MAXN], dep[MAXN], order[MAXN];
ll f[MAXN], g[MAXN], pf[MAXN], pg[MAXN];
int up[MAXN][LOG];

inline void addEdge(int u, int v) {
    to[++ecnt] = v; nxt[ecnt] = head[u]; head[u] = ecnt; deg[u]++;
}

int main() {
    if (scanf("%d %d", &n, &q) != 2) return 0;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        addEdge(u, v);
        addEdge(v, u);
    }

    // 迭代 BFS 求父子关系、深度与 BFS 序（避免深树递归爆栈）
    int qh = 0, qt = 0;
    order[qt++] = 1;
    par[1] = 0; dep[1] = 0;
    while (qh < qt) {
        int x = order[qh++];
        for (int e = head[x]; e; e = nxt[e]) {
            int y = to[e];
            if (y == par[x]) continue;
            par[y] = x;
            dep[y] = dep[x] + 1;
            order[qt++] = y;
        }
    }

    // f[x] = deg[x] + Σ f[儿子]：按逆 BFS 序自底向上合并
    for (int i = 1; i <= n; i++) f[i] = deg[i];
    for (int i = n - 1; i >= 1; i--) {
        int x = order[i];
        f[par[x]] += f[x];
    }

    // g 与树上前缀和：按 BFS 序自顶向下
    g[1] = 0; pf[1] = 0; pg[1] = 0;
    for (int i = 1; i < n; i++) {
        int x = order[i];
        g[x] = g[par[x]] + f[par[x]] - f[x];
        pf[x] = pf[par[x]] + f[x];
        pg[x] = pg[par[x]] + g[x];
    }

    // 倍增表
    for (int x = 1; x <= n; x++) up[x][0] = par[x];
    for (int j = 1; j < LOG; j++)
        for (int x = 1; x <= n; x++)
            up[x][j] = up[up[x][j - 1]][j - 1];

    while (q--) {
        int u, v;
        scanf("%d %d", &u, &v);
        int a = u, b = v;
        if (dep[a] < dep[b]) { int t = a; a = b; b = t; }
        int d = dep[a] - dep[b];
        for (int j = 0; j < LOG; j++)
            if (d >> j & 1) a = up[a][j];
        if (a != b) {
            for (int j = LOG - 1; j >= 0; j--)
                if (up[a][j] != up[b][j]) { a = up[a][j]; b = up[b][j]; }
            a = up[a][0];
        }
        int z = a;
        ll ans = (pf[u] - pf[z]) + (pg[v] - pg[z]);
        ans %= MOD;
        if (ans < 0) ans += MOD;
        printf("%lld\n", ans);
    }
    return 0;
}
