// ============================================================================
// 一本通 1732《情报传递》 std.cpp  ——  C++17（本机 g++ -O2 编译零警告）
// 限制：time 2000 ms / memory 256 MB（见 config.json）
// ----------------------------------------------------------------------------
// 【网络检索情况】（题面特征句精确检索）
//   检索词：「有一个情报网共有n个人，通过有向的电话线联络」+「一本通 1732 情报传递 题解」
//   [1] https://blog.csdn.net/ygmjsjdboy/article/details/102557795
//       《【强联通】情报传递》—— 题面与本题**逐字一致**（n 人 / 两类要求 / P≤n+m+t 全同）。
//       结论：「直接用 m1 中的连边 + 缩点，再用 m2 的边检验」。
//   [2] https://blog.csdn.net/ronaldo7_zyb/article/details/106619024
//       《『毒瘤算法系列13』情报传递》—— 题面与本题逐字一致。
//       结论：「①中的边连接起来，再判断②是否合法」，缩点 → DAG 可达性（bitset + 分块）。
//   两来源做法一致、题面无歧义，**无冲突**（未触发「停下报告」条件）。
//   （两来源都直接「把 m1 的要求当边连」，但均未说明为何最优；本文件 §关键结论 补上了证明。）
//
// 【关键结论（自行推导，与 [1][2] 的「连①边 + 缩点”做法一致）】
//   注意题面的①是**要求**（a 必须能走到 b），并非给定边。设 R1 = 全部①要求对应的边集，
//   TC(R1) 为其传递闭包。对任意合法情报网 G：每条①要求 (a,b) 都要求 a⇝b ∈ G，而可达性是
//   传递的 ⇒ 对 R1 中路径长度归纳得 TC(R1) ⊆ Reach(G)。故：
//     • 若某② (a,b) 满足 a⇝b ∈ TC(R1)，则由上式 a⇝b ∈ Reach(G) ⇒ 任何 G 都违反② ⇒ **NO**；
//     • 否则取 G = R1（把 m1 条①要求原样铺成边）即合法：①的每条要求都成了 1 步边，
//       而 ② 全部满足（Reach(G) = TC(R1) 中无违反对）⇒ **YES**，且 P = m1 ≤ n+m1+m2 = n+m+t ✓。
//   ⇒ 判定只需：在「①要求图」上算可达性（缩点 + DAG bitset），检查有无②被违反。
//
// 【算法（自行改写，非直抄）】
//   1) 迭代式 Tarjan 缩点（n=1e5 的链也不爆栈）。②的 a,b 同属一个 SCC ⇒ 必然互相可达
//      ⇒ 立即 NO（快速路径，两来源同款判据）。
//   2) 缩点得 DAG（跨 SCC 边去重）。按 Tarjan 性质：跨 SCC 边 u→v 有 col[u] > col[v]，
//      故按 col 升序递推即为**逆拓扑序**。
//   3) 对缩点 DAG 做**分块 bitset 可达性 DP**：位空间 = SCC 编号，每块 W 个 u64
//      （W 按 96 MB 内存预算自适应）。每块内：row[c] = bit(c) | ∪ row[d]（c→d 为跨 SCC 边），
//      算完即回答 target 落在本块的②。复杂度 = O(跨SCC边数 · scc/64) 位运算
//      （与 [1][2] 同量级，本实现把每块行内存压到 96 MB 以内的整数块，无需分块时另开数组）。
//   4) 全程早退出：任何违例立即 NO 返回。
//   最坏情形（m1=t=1e5 且全为跨 SCC 边）实测见 gen-report.md §5 顶格点耗时。
//
// 【样例验证】(见 gen-report.md §4，与题面输出逐字节一致)
//   样例1 3/2/(1 2)(2 3)/1/(1 3)  -> NO
//   样例2 3/2/(1 2)(2 3)/1/(3 1)  -> YES / 2 / 1 2 / 2 3
// ============================================================================
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <algorithm>

using namespace std;

// ------------------------------ 快速输入 ------------------------------
static const size_t IBUF = 1 << 20;
static char ibuf[IBUF];
static size_t ipos = 0, ilen = 0;

static inline int gc(void) {
    if (ipos == ilen) {
        ilen = fread(ibuf, 1, IBUF, stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return (int)(unsigned char)ibuf[ipos++];
}

static inline int readInt(void) {
    int c = gc();
    while (c < '0' || c > '9') {
        if (c == -1) return -1;
        c = gc();
    }
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = gc();
    }
    return x;
}

struct Solver {
    int n, m1, m2, scc;
    vector<int> eu, ev;                       // ①需求边（= 最终输出的边）
    vector<int> head, nxt, to;                // ①图 CSR
    vector<int> qa, qb;                       // ②查询
    vector<int> dfn, low, col, it;
    vector<int> ch, cn, ct;                   // 缩点 DAG CSR（去重）

    void buildGraph();
    void tarjanSCC();
    bool buildDAG();
    bool answerQueries();
    bool run();
};

// ---------------- 读入 + ①图 CSR ----------------
void Solver::buildGraph() {
    head.assign(n + 1, -1);
    nxt.assign(m1, -1);
    to.assign(m1, -1);
    eu.assign(m1, 0);
    ev.assign(m1, 0);
    for (int i = 0; i < m1; i++) {
        int a = readInt(), b = readInt();
        if (a < 1 || a > n) a = 1;            // 越界保护（数据合规时不触发）
        if (b < 1 || b > n) b = 1;
        eu[i] = a; ev[i] = b;
        to[i] = b; nxt[i] = head[a]; head[a] = i;
    }
}

// ---------------- 迭代式 Tarjan SCC ----------------
// 结果：col[u] ∈ [1, scc]；跨 SCC 边 u→v 满足 col[u] > col[v]（逆拓扑序）
void Solver::tarjanSCC() {
    dfn.assign(n + 1, 0);
    low.assign(n + 1, 0);
    col.assign(n + 1, 0);
    it.assign(n + 1, 0);
    vector<int> stk, call;
    stk.reserve(n + 2);
    call.reserve(n + 2);
    int timer = 0;
    scc = 0;
    for (int s = 1; s <= n; s++) {
        if (dfn[s]) continue;
        dfn[s] = low[s] = ++timer;
        stk.push_back(s);
        call.push_back(s);
        it[s] = head[s];
        while (!call.empty()) {
            int u = call.back();
            int e = it[u];
            if (e != -1) {
                it[u] = nxt[e];
                int v = to[e];
                if (!dfn[v]) {
                    dfn[v] = low[v] = ++timer;
                    it[v] = head[v];
                    stk.push_back(v);
                    call.push_back(v);
                } else if (!col[v]) {         // 仍在栈上 ⇒ 回边
                    if (dfn[v] < low[u]) low[u] = dfn[v];
                }
            } else {
                call.pop_back();
                if (low[u] == dfn[u]) {       // 弹出一个 SCC
                    scc++;
                    for (;;) {
                        int x = stk.back(); stk.pop_back();
                        col[x] = scc;
                        if (x == u) break;
                    }
                }
                if (!call.empty()) {
                    int p = call.back();
                    if (low[u] < low[p]) low[p] = low[u];
                }
            }
        }
    }
    dfn.clear(); dfn.shrink_to_fit();
    low.clear(); low.shrink_to_fit();
    it.clear();  it.shrink_to_fit();
    stk.clear(); stk.shrink_to_fit();
    call.clear(); call.shrink_to_fit();
}

// ---------------- 缩点 DAG（跨 SCC 边去重） ----------------
// 返回 false 表示发现「②的 a,b 同属一个 SCC」⇒ 必然 a 可达 b ⇒ NO
bool Solver::buildDAG() {
    m2 = readInt();
    if (m2 < 0) m2 = 0;
    qa.assign(m2, 0);
    qb.assign(m2, 0);
    for (int i = 0; i < m2; i++) {
        qa[i] = readInt(); qb[i] = readInt();
        if (qa[i] < 1 || qa[i] > n) qa[i] = 1;
        if (qb[i] < 1 || qb[i] > n) qb[i] = 1;
        if (col[qa[i]] == col[qb[i]]) {       // ②被①强制违反
            fputs("NO\n", stdout);
            return false;
        }
    }
    long long base = (long long)scc + 1;
    vector<long long> key;
    key.reserve(m1);
    for (int i = 0; i < m1; i++) {
        int a = col[eu[i]], b = col[ev[i]];
        if (a != b) key.push_back((long long)a * base + (long long)b);
    }
    sort(key.begin(), key.end());
    key.erase(unique(key.begin(), key.end()), key.end());
    int cN = (int)key.size();
    ch.assign(scc + 1, -1);
    cn.assign(cN, -1);
    ct.assign(cN, -1);
    for (int i = 0; i < cN; i++) {
        int a = (int)(key[i] / base), b = (int)(key[i] % base);
        ct[i] = b; cn[i] = ch[a]; ch[a] = i;
    }
    return true;
}

// ---------------- 分块 bitset 可达性 DP + ②判定 ----------------
bool Solver::answerQueries() {
    if (m2 == 0) return true;
    vector<int> qord(m2);
    for (int i = 0; i < m2; i++) qord[i] = i;
    sort(qord.begin(), qord.end(),
         [&](int x, int y) { return col[qb[x]] < col[qb[y]]; });

    const size_t BUDGET = 64u << 20;                    // 64 MB（题限 256 MB，留 4 倍余量）
    size_t wordsFull = ((size_t)scc + 63) / 64;         // 一次算完所需 u64 行宽
    size_t W = wordsFull;
    if (W > 1 && (size_t)(scc + 1) * W * 8 > BUDGET) {
        W = BUDGET / (8u * ((size_t)scc + 1));
        if (W < 1) W = 1;
    }
    size_t bitBlock = W * 64;
    vector<uint64_t> row((size_t)(scc + 1) * W, 0);

    size_t qptr = 0;
    for (size_t lo = 1; lo <= (size_t)scc; lo += bitBlock) {
        size_t hi = lo + bitBlock - 1;
        if (hi > (size_t)scc) hi = (size_t)scc;
        while (qptr < (size_t)m2 && (size_t)col[qb[qord[qptr]]] < lo) qptr++;
        if (qptr >= (size_t)m2 || (size_t)col[qb[qord[qptr]]] > hi) continue;  // 本块无②

        memset(row.data(), 0, row.size() * sizeof(uint64_t));
        for (int c = 1; c <= scc; c++) {                 // col 升序 = 逆拓扑序
            uint64_t *rc = row.data() + (size_t)c * W;
            if ((size_t)c >= lo && (size_t)c <= hi)
                rc[(size_t)(c - lo) >> 6] |= 1ULL << ((size_t)(c - lo) & 63);
            for (int e = ch[c]; e != -1; e = cn[e]) {
                const uint64_t *rd = row.data() + (size_t)ct[e] * W;
                for (size_t w = 0; w < W; w++) rc[w] |= rd[w];
            }
        }
        for (size_t k = qptr; k < (size_t)m2 && (size_t)col[qb[qord[k]]] <= hi; k++) {
            int q = qord[k];
            size_t off = (size_t)col[qb[q]] - lo;
            if (row[(size_t)col[qa[q]] * W + (off >> 6)] & (1ULL << (off & 63))) {
                fputs("NO\n", stdout);                   // a 可达 b ⇒ ②被违反
                return false;
            }
        }
    }
    return true;
}

bool Solver::run() {
    n = readInt();
    if (n <= 0) { fputs("YES\n0\n", stdout); return true; }
    m1 = readInt();
    if (m1 < 0) m1 = 0;
    buildGraph();
    tarjanSCC();
    if (!buildDAG()) return false;
    if (!answerQueries()) return false;

    // ---------------- YES：情报网 = 全部①边（P = m1 ≤ n+m+t） ----------------
    fputs("YES\n", stdout);
    printf("%d\n", m1);
    for (int i = 0; i < m1; i++) printf("%d %d\n", eu[i], ev[i]);
    return true;
}

int main(void) {
    Solver s;
    s.run();
    return 0;
}
