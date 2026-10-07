// std.cpp —— 一本通 1736《最大连通块》
//
// 来源说明（依据）：
//   本题为自研题解（未找到公开题解）。已检索：搜狗搜索（可用的引擎）以题面特征句
//   「最小化最大的连通块 / 删去一个点」「1736 最大连通块」「最大连通块 合数」等检索，
//   仅命中 CSDN 上一篇同名的《最大连通块》（blog.csdn.net/CylMK/article/details/137693095），
//   经阅读为「01 矩阵四连通块 DFS」的**另一道题**，与本题无关；
//   CSDN 站内搜索（so.csdn.net/api/v3/search）「一本通 1736 题解」「一本通高手训练 最大连通块」
//   均无对应题解；Bing/Baidu/DDG/cnblogs 站内搜索在本次环境中响应异常（返回空页）；
//   官方页面 http://ybt.ssoier.cn:8088/problem_show.php?pid=1736 可访问，题面/时限/样例与
//   .ybt-import/staging/1736/content.md 一致，但未提供题解。
//
// 算法（自研，标准图论技巧）：
//   建边条件：gcd(a_u, a_v) 为合数  <=>  Ω(gcd) >= 2
//            <=> 存在见证数 w ∈ { p^2 | p 素数 } ∪ { p*q | p<q 素数 }，使 w | a_u 且 w | a_v。
//   于是构造辅助二部图：原图 n 个点 0..n-1，外加「见证数」点；点 v 与见证 d 连边 <=> d | a_v。
//   引理：a) 原图两点的连通性与辅助图中两原点的连通性一致（见证路径交替 v-w-v，相邻两原点共享见证 -> 原图有边）；
//         b) 见证点永不被删除，故删去原点 x 后，原点之间的连通分量 = 辅助图 G - x 中只含原点的连通分量。
//   因此答案 = min_x M(x)，M(x) = 删 x 后最大分量的大小（只数原点）。
//   在辅助图（无向）上做一次迭代 DFS 求 disc/low/parent/sz(sz 只数原点)，则对原点 x：
//     设 compTot = x 所在连通分量（含 x）的原点数；sep 子 = 满足 low[c] >= disc[x] 的树儿子 c。
//     M(x) = max( max_{sep c} sz[c] , compTot - 1 - Σ_{sep c} sz[c] , 其他分量最大原点数 )
//   其他分量最大值用分量总量 top1/top2 得到。删点后剩余部分至少 1（n>=2），直接取 min。
//   复杂度 O(maxA loglog maxA + Σ (n + W + E) )，W <= Σ distinct 见证数 <= 36n，E <= 2*36n。
//
// 编译/验证（见 gen-report.md）：g++ -O2 -std=c++17 -o std std.cpp
// 三组题面样例：2 / 3 / 6（实测一致）。
#include <bits/stdc++.h>
using namespace std;

static const size_t IBS = 1u << 24;
static char ibuf[IBS];
static int ip = 0, ilen = 0;
static inline int gc() {
    if (ip == ilen) {
        ilen = (int)fread(ibuf, 1, IBS, stdin);
        ip = 0;
        if (ilen <= 0) return -1;
    }
    return ibuf[ip++];
}
static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

int main() {
    int T = readInt();
    if (T < 1) return 0;
    vector<vector<int> > tests(T);
    int maxA = 0;
    for (int t = 0; t < T; t++) {
        int n = readInt();
        tests[t].resize(n);
        for (int i = 0; i < n; i++) {
            int x = readInt();
            tests[t][i] = x;
            if (x > maxA) maxA = x;
        }
    }
    if (maxA < 2) maxA = 2;

    // 最小质因子筛（线性）
    vector<int> spf(maxA + 1, 0);
    {
        vector<int> primes;
        primes.reserve(maxA / 10 + 16);
        for (int i = 2; i <= maxA; i++) {
            if (spf[i] == 0) { spf[i] = i; primes.push_back(i); }
            for (size_t j = 0; j < primes.size(); j++) {
                long long p = primes[j];
                if (p > spf[i] || p * i > maxA) break;
                spf[(int)(p * i)] = (int)p;
            }
        }
    }

    // 见证数 -> 本轮内局部编号的映射；fresh 全局单调递增，baseId 为每轮起点，判定 wid[d] > baseId 表示本轮已分配
    vector<int> wid(maxA + 1, 0);
    int fresh = 0;

    // 复用的缓冲区
    vector<int> wl;          // 原点 -> 见证点 的扁平边表
    vector<int> off, wcnt, wdeg, ofs, adj, disc, low, par, itp, sz, comp, compTot;
    vector<int> a;
    int P[16], E[16];

    string out;
    out.reserve(1 << 16);

    for (int t = 0; t < T; t++) {
        a = tests[t];
        int n = (int)a.size();
        int baseId = fresh;

        wl.clear();
        off.assign(n + 1, 0);
        for (int i = 0; i < n; i++) {
            int x = a[i];
            int k = 0;
            while (x > 1) {
                int p = spf[x], e = 0;
                while (x % p == 0) { x /= p; e++; }
                P[k] = p; E[k] = e; k++;
            }
            off[i] = (int)wl.size();
            for (int j = 0; j < k; j++) {
                for (int j2 = j + 1; j2 < k; j2++) {         // p*q 见证
                    int d = P[j] * P[j2];
                    int w;
                    if (wid[d] > baseId) w = wid[d];
                    else { w = (++fresh); wid[d] = w; }
                    wl.push_back(n + w - baseId - 1);
                }
                if (E[j] >= 2) {                              // p^2 见证
                    int d = P[j] * P[j];
                    int w;
                    if (wid[d] > baseId) w = wid[d];
                    else { w = (++fresh); wid[d] = w; }
                    wl.push_back(n + w - baseId - 1);
                }
            }
            off[i + 1] = (int)wl.size();
        }
        int W = fresh - baseId;
        int N = n + W;

        wdeg.assign(W, 0);
        for (size_t e = 0; e < wl.size(); e++) wdeg[wl[e] - n]++;

        ofs.assign(N + 1, 0);
        for (int v = 0; v < n; v++) ofs[v + 1] = ofs[v] + (off[v + 1] - off[v]);
        for (int w = 0; w < W; w++) ofs[n + w + 1] = ofs[n + w] + wdeg[w];
        adj.assign(ofs[N], 0);
        {
            vector<int> pos(ofs.begin(), ofs.begin() + N);
            for (int i = 0; i < n; i++) {
                for (int e = off[i]; e < off[i + 1]; e++) {
                    int w = wl[e];
                    adj[pos[i]++] = w;
                    adj[pos[w]++] = i;
                }
            }
        }

        disc.assign(N, 0); low.assign(N, 0); par.assign(N, -1);
        itp.assign(N, 0); sz.assign(N, 0); comp.assign(N, -1);
        vector<int> stk;
        stk.reserve(N);
        compTot.clear();

        int timer = 0;
        for (int s = 0; s < N; s++) {
            if (disc[s]) continue;
            int cid = (int)compTot.size();
            int cnt = 0;
            disc[s] = low[s] = ++timer;
            par[s] = -1; itp[s] = 0; sz[s] = (s < n) ? 1 : 0; comp[s] = cid;
            if (s < n) cnt++;
            stk.clear(); stk.push_back(s);
            while (!stk.empty()) {
                int v = stk.back();
                if (itp[v] < ofs[v + 1] - ofs[v]) {
                    int u = adj[ofs[v] + itp[v]++];
                    if (u == par[v]) continue;
                    if (disc[u] == 0) {
                        disc[u] = low[u] = ++timer;
                        par[u] = v; itp[u] = 0; sz[u] = (u < n) ? 1 : 0; comp[u] = cid;
                        if (u < n) cnt++;
                        stk.push_back(u);
                    } else if (disc[u] < low[v]) {
                        low[v] = disc[u];
                    }
                } else {
                    stk.pop_back();
                    int p = par[v];
                    if (p != -1) {
                        if (low[v] < low[p]) low[p] = low[v];
                        sz[p] += sz[v];
                    }
                }
            }
            compTot.push_back(cnt);
        }

        // 分量总量的 top1 / top2（注意并列最大：cnt1>=2 时「其他分量最大」仍是 t1）
        int t1 = 0, t2 = 0, cnt1 = 0;
        for (size_t c = 0; c < compTot.size(); c++) {
            int v = compTot[c];
            if (v > t1) { t2 = t1; t1 = v; cnt1 = 1; }
            else if (v == t1) cnt1++;
            else if (v > t2) t2 = v;
        }

        int best = INT_MAX;
        for (int x = 0; x < n; x++) {
            int cid = comp[x];
            int ctot = compTot[cid];
            int other = (ctot == t1 && cnt1 == 1) ? t2 : t1;
            int rest = ctot - 1;
            int sepMax = 0;
            for (int e = ofs[x]; e < ofs[x + 1]; e++) {
                int u = adj[e];
                if (par[u] == x && low[u] >= disc[x]) {
                    if (sz[u] > sepMax) sepMax = sz[u];
                    rest -= sz[u];
                }
            }
            int M = max(sepMax, max(rest, other));
            if (M < best) best = M;
        }
        if (best == INT_MAX) best = 0;
        out += to_string(best);
        out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
