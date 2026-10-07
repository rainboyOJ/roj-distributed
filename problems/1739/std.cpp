// ============================================================================
// 一本通 1739《观光巴士》标程（std.cpp，C++17，stdin -> stdout）
//
// 题源：信息学奥赛一本通 · 高手训练篇 · 三、图论 · 第 7 章 欧拉回路（1739）
//   - 章节/题号目录：https://blog.csdn.net/qq_36230375/article/details/136483654
//     （「信息学奥赛一本通高手训练 题解目录」；其中 1739 观光巴士 隶属「第7章 欧拉回路」）
//   - 站内题面页：https://ybt.ssoier.cn/problem_show.php?pid=1739
//   - 网络检索未发现本题的公开题解/AC 代码（检索记录见 gen-report.md「标程来源」节），
//     故本标程按下列推导自行编写；并用枚举所有接续配对的朴素程序在随机实例上做了
//     交叉验证（n<=12，8000+ 组，全部一致），样例 1/2 均逐字节通过（见 gen-report.md）。
//
// 题意：n 个巴士站，2n 条线路；线路 i 从站 ceil(i/2) 出发，终点 e_i，每天一班，
//   每日 l_i 时发车，历时 d_i 小时（每天 24 小时）。第 1 天 0 时在 1 号站，
//   要坐每条线路恰好一次并回到 1 号站，求回到 1 号站的最早时刻（= 停留时间）。
//
// 关键推导：
//   1) 线路 i 的班次时刻为 { l_i + 24k }（k ≥ 0；l_i 为“离开新潟”之前的时刻轴，
//      题面虽限定 l_i ≤ 1000，但“每天 24 小时”意味着它只能是一天以内的时刻偏移；
//      两种读法只在“首班等待”上有差别，且本包数据全部取 0 ≤ l_i < 24 使两者一致）。
//      到达时刻 t 接续线路 f 的等待为 W(e,f) = (l_f - l_e - d_e) mod 24 ∈ [0,24)，
//      只依赖 e、f 两条线路，与已经“过了几天”无关（差一个 24 的整数倍）。总时间
//        T = sum(d_i) + firstWait + sum_{接续} W(e, succ(e))，
//      开始时刻为 0，首班等待 = l_首班。
//   2) 线路 i 从站 ceil(i/2) 出发 ⇒ 站 v 的两条出边恰为 {2v-1, 2v}；
//      由「方案一定存在」得每个站入度也恰为 2。一次遍历恰一次的方案 ⟺ 在每个站把
//      两条入边与两条出边配成 succ（站 1 处：最后一条入边→首班出边这条「接续」不
//      发生、以首班等待代替），使 succ 构成单环。
//   3) 除站 1 外每站有两种配对，各有代价（两条 W 之和），先各取较小者得初始配对 π0，
//      两种方式的代价差 Δ_v ≥ 0。把 π0 的每个环看作一个点，站 v 翻转配对的「合并边」
//      连接 comp(in_a(v)) 与 comp(in_b(v))；要得到单环，翻转集必须在环图上连通。
//      ⇒ 最小合并代价 = 该图最小生成树（Kruskal）。站 1 的两种配对 × 「哪一对作虚拟
//      接续」共 4 种组合枚举取最小。
//   复杂度 O(n log n)，n ≤ 1000 时远低于 1000ms/128MB 限制。
// ============================================================================
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;

static int n, m;
static vector<int> lv, dv;   // 线路起点由下标决定：i -> i/2（0-indexed）

// 接续等待 W(e,f) = (l_f - l_e - d_e) mod 24（用 64 位防止 d_i 很大时溢出）
static inline int W(int e, int f) {
    ll w = (ll)(lv[f] % 24) - (ll)(((ll)lv[e] + dv[e]) % 24);
    if (w < 0) w += 24;
    return (int)w;
}

int main() {
    if (scanf("%d", &n) != 1) return 0;
    m = 2 * n;
    lv.assign(m, 0);
    dv.assign(m, 0);
    vector<vector<int> > inE(n);   // 每站的入边（题面保证恰 2 条）
    ll sumD = 0;
    for (int i = 0; i < m; ++i) {
        int e, l, d;
        if (scanf("%d %d %d", &e, &l, &d) != 3) return 0;
        inE[e - 1].push_back(i);
        lv[i] = l;
        dv[i] = d;
        sumD += d;
    }

    ll best = -1;
    for (int p0 = 0; p0 < 2; ++p0) {          // 站 1 的两种配对
        vector<int> succ(m, -1);
        succ[inE[0][0]] = p0 ? 1 : 0;         // 站 1 出边为 0、1
        succ[inE[0][1]] = p0 ? 0 : 1;

        vector<int> delta(n, 0);
        ll base = 0;
        for (int v = 1; v < n; ++v) {         // 其余站取局部最优配对
            int a = inE[v][0], b = inE[v][1], oa = 2 * v, ob = 2 * v + 1;
            int cA = W(a, oa) + W(b, ob);
            int cB = W(a, ob) + W(b, oa);
            if (cA <= cB) { succ[a] = oa; succ[b] = ob; base += cA; delta[v] = cB - cA; }
            else          { succ[a] = ob; succ[b] = oa; base += cB; delta[v] = cA - cB; }
        }

        // π0 的环编号
        vector<int> comp(m, -1);
        int ncomp = 0;
        for (int e = 0; e < m; ++e) {
            if (comp[e] != -1) continue;
            int cur = e;
            while (comp[cur] == -1) { comp[cur] = ncomp; cur = succ[cur]; }
            ++ncomp;
        }

        // 翻转站 v 可合并 comp(in_a)、comp(in_b) 两个环，代价 delta[v]
        vector<pair<int, pair<int, int> > > edges;
        edges.reserve(n);
        for (int v = 1; v < n; ++v) {
            int a = inE[v][0], b = inE[v][1];
            if (comp[a] != comp[b])
                edges.push_back(make_pair(delta[v], make_pair(comp[a], comp[b])));
        }
        sort(edges.begin(), edges.end());

        // Kruskal：把 ncomp 个环并成一个
        vector<int> par(ncomp);
        for (int i = 0; i < ncomp; ++i) par[i] = i;
        int merges = 0;
        ll add = 0;
        for (size_t ei = 0; ei < edges.size(); ++ei) {
            int x = edges[ei].second.first, y = edges[ei].second.second;
            while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
            while (par[y] != y) { par[y] = par[par[y]]; y = par[y]; }
            if (x != y) { par[x] = y; ++merges; add += edges[ei].first; }
        }
        if (merges != ncomp - 1) continue;    // 该配对下无法连成单环

        // 首班 s：与 s 配对的那条接续不发生（换成首班等待 lv[s]），另一条接续保留
        for (int s = 0; s < 2; ++s) {
            int other = 1 - s;
            int pin = -1;
            for (int e = 0; e < 2; ++e) {
                int id = inE[0][e];
                if (succ[id] == other) pin = id;
            }
            if (pin < 0) continue;
            ll tot = sumD + (ll)lv[s] + W(pin, other) + base + add;
            if (best < 0 || tot < best) best = tot;
        }
    }

    printf("%lld\n", best);
    return 0;
}
