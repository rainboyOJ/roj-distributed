// 一本通 1759《采访计划》（目标 ROJ 题号 1759）标程
//
// ---------------------------------------------------------------------------
// 题意
// ---------------------------------------------------------------------------
// n 个星球，编号 1..n。第 i 个星球上有「球长 i」与「长者 i」。长者 i 管辖球长 i
// （长者管辖自己）。长者 i 手里有一份名单 B_i ⊆ {1..i-1}（元素互不重复）。
// 管辖的定义是充要条件式：
//      对 j != i：  i 管辖 j  <=>  (∀ k ∈ B_i, k 管辖 j)
//      对 j == i：  i 管辖 i（恒成立）
// （B_i = ∅ 时：上式右端对任意 j 空真，但题面明确只有「长者管辖自己」，
//   样例 1 号长者（B_1=∅）只管辖 1 号球长、而 2 号长者 S_2={1,2} 可验证：
//   若把空 B_i 视为管辖全体，则询问 {2,3} 的答案会变成 n=7，与样例输出 3 矛盾。
//   故约定：B_i = ∅ 时 S_i = {i}。）
// 记 S_i = { j : i 管辖 j }。m 个询问，每次给一个长者编号集合 T（同样无重复），
// 求 |∪_{i∈T} S_i|。
//
// 数据范围：n, m <= 200000，Σ|B_i| <= 2000000，询问中 Σ sz_i <= 2000000。
// 时间限制 2000 ms，内存限制 128 MB（config.json / 官方页 131072 KB）。
//
// ---------------------------------------------------------------------------
// 解法推导（本题无公开题解，本标程为自研；推导过程如下，已用样例与随机小数据校验）
// ---------------------------------------------------------------------------
// (1) 由定义可得：S_i = {i} ∪ ( ∩_{k∈B_i} S_k )（B_i = ∅ 时取 {i}）。
// (2) 「管辖」是偏序：自反、传递、反对称。
//     传递性证明：对 max(i,j) 归纳。i 管辖 j 且 j 管辖 l 时，
//       i=j 或 j=l 显然；否则 B_i ≠ ∅ 且 ∀k∈B_i (k<i) 有 k 管辖 j，再由 k<i 归纳得
//       k 管辖 l，于是 i 管辖 l。
//     反对称：先有 i 管辖 j ⟹ i >= j（对 i 归纳：j≠i 时每个 k∈B_i 满足 k>=j，故 i>k>=j）。
// (3) 关键引理：i 同时管辖 a 与 b ⟹ a 与 b 可比较（即每个 S_i 是一条链）。
//     反证：取「同时管辖两个不可比较元素」的最小元素 i。由 (2) 的传递性论证，a,b≠i，
//     故 B_i ≠ ∅ 且每个 k∈B_i 也同时管辖 a、b，而 k<i，与 i 的最小性矛盾。
//     ⇒ S_i 是链 ⇒ 在 Hasse 图里每个点至多被一个点覆盖（若覆盖 j,j'，则 j,j'∈S_i 可比较，
//       小的那个就被夹住，矛盾）⇒ 偏序的 Hasse 图是**森林**，且 S_i 恰是「该森林中
//       根到 i 的路径」上的点集。
// (4) 于是 parent(i) = S_i 中 i 之下的最大元素 = max( ∩_{k∈B_i} S_k ) = LCA(B_i)（在森林中；
//     若 B_i 中的点分属不同树，则交集为空，i 自成一棵新树，S_i={i}）。
//     由于 B_i ⊆ {1..i-1}，按 i 递增顺序建树即可：插入 i 时 B_i 的点都已在森林里，
//     新点只会作为叶子挂到已有点下面，已有点的祖先关系不会改变 ⇒ 增量建树 + 倍增 LCA 合法。
//     （注意：此时点的「插入次序」并不是合法的 DFS 序，不能拿插入序号当 dfn 用 min/max
//       性质求集合 LCA，必须逐个与当前 LCA 合并；后文求 dfn 时另做一次真正的 DFS。）
// (5) 询问 |∪_{i∈T} S_i| = 「森林中这些根路径并的顶点数」。把 T 按真正的 DFS 序（dfn）排序，
//     对同一棵树内的相邻两项有经典恒等式：
//         |∪ 根路径| = Σ_{v∈T} dep(v) - Σ_{相邻且同树} dep(LCA(v_j,v_{j+1})) + (涉及的树棵数)
//     （即 Σ depth - Σ depth(lca) + 树数；跨树的相邻项交集为空、贡献 0，只计一次树数。）
//     复杂度：建树 O(Σ|B_i| log n)，询问 O(Σ sz_i log sz_i + Σ sz_i log n)，均远低于限制。
//
// ---------------------------------------------------------------------------
// 来源 / 依据
// ---------------------------------------------------------------------------
//   * 官方题面（题目描述、输入输出格式、样例）：http://ybt.ssoier.cn:8088/problem_show.php?pid=1759
//     （已 curl 实抓核对：标题「1759：采访计划」、时间 2000 ms、内存 131072 KB、样例 7 / 3 3 4
//       与本目录 content.md 一致；该页正文为空模板，故以 content.md 为准。）
//   * 网络检索结论（均无该题公开解法，故自研）：
//     - CSDN 站内搜「一本通 1759 采访计划 / 一本通1759 / 采访计划 虚树 长者 管辖」→ 0 条相关；
//     - Bing / DuckDuckGo 精确句检索（"德高望重" "球长" 长者 管辖 等）→ 无任何 OJ 题解命中；
//     - 可判定本题并非某道知名公开题的改名（题面为 2044 宇宙纪元/长者/球长 的原创背景）。
//     故 std.cpp 为**自研实现**，算法即上文 (1)-(5) 的推导，未抄袭任何公开代码。
//   * 技术参照（仅取通用套路，非本题题解）：
//     - 树上「若干点到根的路径并顶点数 = Σdep - Σdep(LCA 相邻) + 连通块数」为虚树/树上
//       经典恒等式；本标程按此恒等式实现，并用题面样例 + 随机小数据校验（见 gen-report.md）。
// ---------------------------------------------------------------------------

#include <cstdio>
#include <cstdlib>
#include <algorithm>

// 数组上限按题面上限 × 安全系数 2 开（n <= 2e5 → MAXN = 4e5+5；LOGN: 2^19 > 4e5）
static const int MAXN = 400005;
static const int LOGN = 19;

// ------------------------------- 快速读入 -------------------------------
static char ibuf[1 << 20];
static int ipos = 0, ilen = 0;

static inline int gc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen <= 0) return -1;
    }
    return ibuf[ipos++];
}

static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

// ------------------------------- 快速输出 -------------------------------
static char obuf[1 << 20];
static int opos = 0;

static inline void wch(char c) {
    if (opos == (int)sizeof(obuf)) { fwrite(obuf, 1, opos, stdout); opos = 0; }
    obuf[opos++] = c;
}

static inline void writeInt(long long x) {
    char t[24];
    int k = 0;
    if (x == 0) t[k++] = '0';
    while (x > 0) { t[k++] = (char)('0' + (int)(x % 10)); x /= 10; }
    while (k > 0) wch(t[--k]);
    wch('\n');
}

static inline void oflush() {
    if (opos) { fwrite(obuf, 1, opos, stdout); opos = 0; }
}

// ------------------------------- 森林结构 -------------------------------
static int par[MAXN];   // 父亲（森林中的直接前驱），0 表示树根
static int dep[MAXN];   // 深度（根为 0）
static int rt[MAXN];    // 所在树的编号（用该树树根的编号表示）
static int dfn[MAXN];   // 真正的 DFS 先序编号（同一棵树内连续）
static int up[LOGN][MAXN];      // 倍增祖先：up[0]=par，up[j][0]=0
static int head[MAXN], nxt[MAXN];  // 孩子链表（CSR）
static int stk[MAXN];

static inline int lca(int a, int b) {
    if (dep[a] < dep[b]) { int t = a; a = b; b = t; }
    int d = dep[a] - dep[b];
    for (int j = 0; d; ++j, d >>= 1) if (d & 1) a = up[j][a];
    if (a == b) return a;
    for (int j = LOGN - 1; j >= 0; --j)
        if (up[j][a] != up[j][b]) { a = up[j][a]; b = up[j][b]; }
    return par[a];
}

int main() {
    int n = readInt();
    for (int i = 1; i <= n; ++i) {
        int sz = readInt();
        int cur = 0;
        bool cross = false;  // B_i 中的点是否分属不同树（⇒ 交集为空 ⇒ i 自成一树）
        for (int j = 0; j < sz; ++j) {
            int k = readInt();
            if (j == 0) { cur = k; continue; }
            if (cross) continue;
            if (rt[k] != rt[cur]) { cross = true; continue; }
            cur = lca(cur, k);   // 逐个合并求集合 LCA
        }
        if (sz == 0 || cross) {  // S_i = {i}，i 是一棵新树的根
            par[i] = 0; dep[i] = 0; rt[i] = i;
        } else {                 // S_i = {i} ∪ (根 -> LCA(B_i) 的路径)
            par[i] = cur; dep[i] = dep[cur] + 1; rt[i] = rt[cur];
        }
        up[0][i] = par[i];
        for (int j = 1; j < LOGN; ++j) up[j][i] = up[j - 1][up[j - 1][i]];
        if (par[i]) { nxt[i] = head[par[i]]; head[par[i]] = i; }
    }

    // 真正的 DFS 先序（迭代，避免链状树递归爆栈）
    int timer = 0;
    for (int i = 1; i <= n; ++i) {
        if (par[i]) continue;
        int top = 0;
        stk[top++] = i;
        while (top) {
            int v = stk[--top];
            dfn[v] = ++timer;
            for (int c = head[v]; c; c = nxt[c]) stk[top++] = c;
        }
    }

    int m = readInt();
    // 单个询问的元素数 ≤ Σsz ≤ 2e6（题面上限），按该上限开（再留冗余）
    int *qb = (int *)malloc(sizeof(int) * 2000005u + sizeof(int) * 16);
    for (int qi = 0; qi < m; ++qi) {
        int sz = readInt();
        for (int j = 0; j < sz; ++j) qb[j] = readInt();
        if (sz == 0) { writeInt(0); continue; }
        std::sort(qb, qb + sz, [](int a, int b) { return dfn[a] < dfn[b]; });
        long long ans = dep[qb[0]];
        int trees = 1;
        for (int j = 1; j < sz; ++j) {
            int u = qb[j - 1], v = qb[j];
            ans += dep[v];
            if (rt[u] != rt[v]) ++trees;              // 跨树：交集为空，只多计一棵树
            else ans -= dep[lca(u, v)];               // 同树：减去公共前缀的重复计数
        }
        ans += trees;
        writeInt(ans);
    }
    oflush();
    free(qb);
    return 0;
}
