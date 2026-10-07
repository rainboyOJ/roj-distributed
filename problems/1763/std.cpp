// 一本通 1763《简单树》标程
//
// 题意：给定一棵 n 个点的带权树（边权 c），顺次回答 m 个询问，每个询问给出 L R x，
//       求编号在 [L,R] 内的所有点到点 x 的距离之和。type=1 表示强制在线
//       （输入的 L,R,x 均需异或 lastans = 上一次答案 mod n，初始 lastans = 0）。
// 数据范围：1<=n,m<=60000，0<=type<=1，1<=a,b<=n，0<=c<=10^9。
//
// 参考来源（联网检索到的两篇 AC 题解，结论一致，本文据此按题面改写、重写实现）：
//   [1] https://www.cnblogs.com/chdy/p/12810906.html
//       chdy《一本通 高手训练 1763 简单树 可持久化线段树 树链剖分 标记永久化》
//   [2] https://www.cnblogs.com/yiqiAtiya/p/13923549.html
//       (o-ωq)).oO《一本通1763：简单树》
//
// 做法（两篇题解同一套路）：
//   记 dis[u] 为 u 到根(1)的距离，则 dist(i,x) = dis[i] + dis[x] - 2*dis[lca(i,x)]，于是
//     Σ_{i=L..R} dist(i,x) = dis[x]*(R-L+1) + Σ_{i=L..R} dis[i] - 2*Σ_{i=L..R} dis[lca(i,x)]
//   前两项用 dis 的前缀和 O(1) 得到，难点是第三项 Σ dis[lca(i,x)]。
//   把「i 到根的路径上的每条边」都"打上"自己的边权，则
//     Σ_{i=L..R} dis[lca(i,x)] = Σ_{边 e ∈ path(root,x)} w(e) * #{ i∈[L,R] : e ∈ path(root,i) }
//   用树链剖分把 path(root,x) 拆成 O(log n) 个 dfn 连续的段，再用「可持久化线段树」
//   （版本 k 只含 i∈[1,k] 的路径插入）在 dfn 序上做区间插入、区间查询，
//   版本 R 与版本 L-1 相减即得 [L,R] 的贡献。
//   线段树每个节点存：
//     cnt  —— 恰好完全覆盖该节点区间的插入次数；
//     sum  —— 插入区间与该节点区间之交的边权和（沿递归路径逐层累加）。
//   查询时经过的每个节点加上 cnt * (查询区间与该节点区间之交的边权和)，
//   完全重合时再加上 sum —— 即题解中的「标记永久化」，无需 pushdown。
//   边权区间和用 dfn 序上的前缀和 prefE 相减得到（链内 dfn 连续且父先于子，
//   E[v] = 边 (fa[v],v) 的长度，E[root]=0，故 root 链段从 dfn[1]+1 起算即可）。
//
// 复杂度：时间 O((n+m) log^2 n)，空间 O(节点数)（实测节点数约为 7~12 n）。
// 实现细节：树剖的求 size/重儿子/dfn 全部用显式栈 + BFS 序迭代完成，
//           不使用递归 DFS，避免链形数据（深度 6e4）的爆栈风险。
//           答案用 __int128 中间量计算（最大可达 ~1.8e18，long long 足够但留余量）。

#include <cstdio>
#include <vector>

using namespace std;

static const int MAXN = 60005;

int n, m, typeFlag;
int head[MAXN], nxt[MAXN << 1], to[MAXN << 1], wt[MAXN << 1], ecnt;
int fa[MAXN], sz[MAXN], son[MAXN], top_[MAXN], dfn[MAXN], pos[MAXN], order[MAXN];
long long dis_[MAXN], E[MAXN];       // E[v] = 边 (fa[v], v) 的长度，E[1] = 0
long long prefDis[MAXN], prefE[MAXN]; // prefE 为 dfn 序上的边权前缀和

// 可持久化线段树（数组实现；下标 0 为空节点）
vector<int> lc, rc, cnt, rt;
vector<long long> sumv;

static inline void addEdge(int a, int b, int c) {
    to[++ecnt] = b; wt[ecnt] = c; nxt[ecnt] = head[a]; head[a] = ecnt;
}

// 复制节点 p 得到新节点
static inline int newNode(int p) {
    lc.push_back(lc[p]); rc.push_back(rc[p]);
    cnt.push_back(cnt[p]); sumv.push_back(sumv[p]);
    return (int)lc.size() - 1;
}

// 在版本 p 上插入 dfn 区间 [L,R]（保证 [L,R] ⊆ [l,r]）
int ins(int p, int l, int r, int L, int R) {
    int o = newNode(p);
    if (L == l && r == R) { ++cnt[o]; return o; }
    sumv[o] += prefE[R] - prefE[L - 1];
    int mid = (l + r) >> 1;
    if (R <= mid) lc[o] = ins(lc[o], l, mid, L, R);
    else if (L > mid) rc[o] = ins(rc[o], mid + 1, r, L, R);
    else {
        lc[o] = ins(lc[o], l, mid, L, mid);
        rc[o] = ins(rc[o], mid + 1, r, mid + 1, R);
    }
    return o;
}

// 在版本 p 上查询 dfn 区间 [L,R]（保证 [L,R] ⊆ [l,r]）
long long qry(int p, int l, int r, int L, int R) {
    if (!p) return 0;
    long long w = prefE[R] - prefE[L - 1];
    if (L == l && r == R) return sumv[p] + (long long)cnt[p] * w;
    int mid = (l + r) >> 1;
    long long res = (long long)cnt[p] * w;
    if (R <= mid) return res + qry(lc[p], l, mid, L, R);
    if (L > mid) return res + qry(rc[p], mid + 1, r, L, R);
    return res + qry(lc[p], l, mid, L, mid) + qry(rc[p], mid + 1, r, mid + 1, R);
}

// 统计「在 [l,r] 上插入 [L,R]」将访问（=新建）的节点数，用于一次性预留内存
long long countIns(int l, int r, int L, int R) {
    if (L == l && r == R) return 1;
    int mid = (l + r) >> 1;
    if (R <= mid) return 1 + countIns(l, mid, L, R);
    if (L > mid) return 1 + countIns(mid + 1, r, L, R);
    return 1 + countIns(l, mid, L, mid) + countIns(mid + 1, r, mid + 1, R);
}

// Σ_{i<=k} dis[lca(i,x)]
long long Query(int k, int x) {
    long long res = 0;
    while (top_[x] != 1) {
        res += qry(rt[k], 1, n, dfn[top_[x]], dfn[x]);
        x = fa[top_[x]];
    }
    if (x != 1) res += qry(rt[k], 1, n, dfn[1] + 1, dfn[x]);
    return res;
}

int main() {
    if (scanf("%d %d %d", &n, &m, &typeFlag) != 3) return 0;

    for (int i = 1; i < n; ++i) {
        int a, b, c;
        scanf("%d %d %d", &a, &b, &c);
        addEdge(a, b, c);
        addEdge(b, a, c);
    }

    // ---- BFS 序：求 fa / dis / E，并得到「父先于子」的遍历序 ----
    int qh = 0, qt = 0;
    order[qt++] = 1; fa[1] = 0; dis_[1] = 0; E[1] = 0;
    while (qh < qt) {
        int u = order[qh++];
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e];
            if (v == fa[u]) continue;
            fa[v] = u; E[v] = wt[e]; dis_[v] = dis_[u] + wt[e];
            order[qt++] = v;
        }
    }

    // ---- 逆序求 size 与重儿子 ----
    for (int i = n - 1; i >= 0; --i) {
        int u = order[i];
        sz[u] = 1; son[u] = 0;
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e];
            if (v == fa[u]) continue;
            sz[u] += sz[v];
            if (sz[v] > sz[son[u]]) son[u] = v;
        }
    }

    // ---- 沿重链走，给每条链分配连续的 dfn ----
    int dfa = 0;
    for (int i = 0; i < n; ++i) {
        int u = order[i];
        if (dfn[u]) continue;              // 已是某条链上的节点
        for (int v = u; v; v = son[v]) {
            top_[v] = u;
            dfn[v] = ++dfa;
            pos[dfa] = v;
        }
    }

    for (int k = 1; k <= n; ++k) prefE[k] = prefE[k - 1] + E[pos[k]];
    for (int i = 1; i <= n; ++i) prefDis[i] = prefDis[i - 1] + dis_[i];

    // ---- 建可持久化版本：版本 k = 插入编号 1..k 的「到根路径」 ----
    // 先精确统计节点总数并一次性预留，避免 vector 反复扩容造成的峰值内存翻倍
    long long totalNodes = 0;
    for (int k = 1; k <= n; ++k) {
        int x = k;
        while (top_[x] != 1) { totalNodes += countIns(1, n, dfn[top_[x]], dfn[x]); x = fa[top_[x]]; }
        if (x != 1) totalNodes += countIns(1, n, dfn[1] + 1, dfn[x]);
    }
    lc.reserve(totalNodes + 1); rc.reserve(totalNodes + 1);
    cnt.reserve(totalNodes + 1); sumv.reserve(totalNodes + 1); rt.reserve(n + 1);

    lc.push_back(0); rc.push_back(0); cnt.push_back(0); sumv.push_back(0); rt.push_back(0);
    for (int k = 1; k <= n; ++k) {
        int cur = rt[k - 1], x = k;
        while (top_[x] != 1) {             // 不在根所在链上：整段 [dfn[top[x]], dfn[x]]
            cur = ins(cur, 1, n, dfn[top_[x]], dfn[x]);
            x = fa[top_[x]];
        }
        if (x != 1) cur = ins(cur, 1, n, dfn[1] + 1, dfn[x]); // 根链上：去掉根自己
        rt.push_back(cur);
    }

    long long last = 0;
    for (int i = 0; i < m; ++i) {
        long long L, R, X;
        scanf("%lld %lld %lld", &L, &R, &X);
        if (typeFlag) { L ^= last; R ^= last; X ^= last; }
        __int128 ans = (__int128)dis_[X] * (R - L + 1)
                     + (prefDis[R] - prefDis[L - 1])
                     - 2 * ((__int128)Query((int)R, (int)X) - Query((int)(L - 1), (int)X));
        long long a = (long long)ans;
        printf("%lld\n", a);
        last = a % n;
    }
    return 0;
}
