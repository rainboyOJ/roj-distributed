// 一本通 高手训练 1719 过河 —— 数据标程 (std.cpp)
//
// 题目来源: 信息学奥赛一本通 · 高手训练篇 三、图论(高手训练) 1719 过河
// 题面核对镜像: https://www.kidscoding8.com/116858.html (仅题面, 无题解/代码)
//
// 公开题解 (网络检索命中的同题解, 模型与本题面逐字一致):
//   《过河》 by werkeytom_ftd  https://blog.csdn.net/werkeytom_ftd/article/details/53164954
//   该文给出的建图: 每个 "(木桩, 圆盘种类)" 建点, 由圆盘 p 到圆盘 q 连边, 权为圆盘 q 的价格,
//   条件为两盘圆心距 <= r_p + r_q (相交/相切即可通行); 源点 S 连向所有触底盘 (Y <= r, 费用0)
//   (原文: 与圆盘重合的地面点可走 => S->i 权 0), 所有触顶盘 (W-Y <= r) 连向汇点 T (权 0),
//   S -> T 的最短路即最小花费; 其代码常量 mx=250+10 亦印证 N,M<=250.
//   公开解的进一步优化: 「R 更大且 C 不更大」的圆盘无用 (Pareto), 以及同木桩上 
//   (R_j, R_{j+1}) 之间用差价权 c_j - c_{j-1} 的链式边替代稠密边, "新图是 n^3 的边数".
//   本标程采用与公开解**等价**的模型, 实现上直接做带点权的堆优化 Dijkstra
//   (见下方做法 1) 2)), 用 Pareto 前沿 + 后缀收缩避免显式建 n^3 条边;
//   正确性另经独立暴力程序 stress 对拍验证, 题面样例 206 / 5 / impossible 全部吻合.
//
// 模型:
//   可行走集合 = 直线 y=0, 直线 y=W, 以及购买的若干圆盘 (边界+内部).
//   圆心必须放在木桩上; 同种圆盘可买任意多块, 可放在任意木桩上.
//   两圆盘之间可通行 <=> 圆心距 d <= r1 + r2 (相切或相交, 交叠处可通行);
//   圆盘触底 <=> Y <= R; 触顶 <=> W - Y <= R (圆盘可以伸到地面以外 y<0 / y>W).
//   因此问题 = 带点权(圆盘价格)的最短路: 起点 = "底边" (费用0), 终点 = "顶边",
//   节点 = (木桩, 圆盘种类), 节点权 = C.
//
// 做法:
//   1) 每根木桩上不需要考虑所有种类: (R,C) 被 (R',C') (R'>=R 且 C'<=C) 支配的种类无用.
//      保留 Pareto 前沿: 按 R 升序则 C 严格升序. 之后"找 R >= need 的最便宜种类"可二分,
//      且从某个节点出发能到达的是一段后缀.
//   2) 堆优化 Dijkstra: 节点 (k,t) 被首次松弛即为其最终最短路 (= 出堆顺序单调不减, 第一个
//      能到达它的源点给出最小候选). 维护 frontier[k] = 木桩 k 上尚未被松弛的最小后缀下标,
//      每次弹出源点 (i,a) 代价 v 时, 对每个木桩 k 求 need = dist(i,k) - R_a, 二分得到后缀
//      起点 idx, 若 idx < frontier[k] 则用 v + C_k[t] (t ∈ [idx, frontier[k]-1]) 松弛并
//      把 frontier[k] 收缩到 idx. 每个 (k,t) 至多入堆一次. 弹出圆盘触顶即得答案, 提前退出.
//   复杂度: 堆中节点 <= N * M, 每次弹 O(N log M), 总 O(N^2 M log M) 级别 (实际远小于).
//   距离判定全部用整数 (圆心距平方 / ceil_sqrt), 避免浮点误差.

#include <cstdio>
#include <cmath>
#include <vector>
#include <map>
#include <queue>
#include <tuple>
#include <algorithm>
#include <climits>
using namespace std;
typedef long long ll;

static ll isqrt_ceil(ll s) { // smallest r >= 0 with r*r >= s
    if (s <= 0) return 0;
    ll r = (ll)sqrtl((long double)s);
    while (r > 0 && (r - 1) * (r - 1) >= s) r--;
    while (r * r < s) r++;
    return r;
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int N, M;
        ll W;
        scanf("%d %d %lld", &N, &M, &W);
        vector<ll> X(N), Y(N);
        for (int i = 0; i < N; i++) scanf("%lld %lld", &X[i], &Y[i]);

        // 读入圆盘种类, 去重后求 Pareto 前沿 (R 升序, C 升序)
        map<ll, ll> best;
        for (int i = 0; i < M; i++) {
            ll R, C;
            scanf("%lld %lld", &R, &C);
            auto it = best.find(R);
            if (it == best.end() || C < it->second) best[R] = C;
        }
        vector<ll> Rs, Cs;
        {   // 按 R 降序扫描, C 严格变小者保留 (即 R 升序 C 升序的前沿)
            ll curmin = LLONG_MAX;
            for (auto it = best.rbegin(); it != best.rend(); ++it) {
                if (it->second < curmin) {
                    Rs.push_back(it->first);
                    Cs.push_back(it->second);
                    curmin = it->second;
                }
            }
            reverse(Rs.begin(), Rs.end());
            reverse(Cs.begin(), Cs.end());
        }
        int P = (int)Rs.size();

        // 圆心距 (向上取整的整数), D[i][k]
        vector<vector<ll>> D(N, vector<ll>(N));
        for (int i = 0; i < N; i++)
            for (int k = 0; k < N; k++) {
                ll dx = X[i] - X[k], dy = Y[i] - Y[k];
                D[i][k] = isqrt_ceil(dx * dx + dy * dy);
            }

        const ll INF = LLONG_MAX / 4;
        vector<vector<ll>> dist(N, vector<ll>(P, INF));
        vector<int> frontier(N, 0); // 0 表示还没有初始化
        vector<char> inited(N, 0);
        priority_queue<tuple<ll, int, int>, vector<tuple<ll, int, int>>, greater<>> pq;

        auto relaxFrom = [&](int k, int idx, ll v) {
            for (int t = idx; t < frontier[k]; t++) {
                dist[k][t] = v + Cs[t];
                pq.emplace(dist[k][t], k, t);
            }
            frontier[k] = idx;
        };

        // 起点: 触底圆盘 (R >= Y[k])
        for (int k = 0; k < N; k++) {
            int idx = (int)(lower_bound(Rs.begin(), Rs.end(), Y[k]) - Rs.begin());
            frontier[k] = P;
            inited[k] = 1;
            if (idx < P) relaxFrom(k, idx, 0);
        }

        ll ans = -1;
        while (!pq.empty()) {
            auto [v, i, a] = pq.top();
            pq.pop();
            if (v != dist[i][a]) continue; // 理论不会发生 (每节点只入堆一次)
            if (Rs[a] >= W - Y[i]) { ans = v; break; } // 该盘触顶
            ll Ra = Rs[a];
            for (int k = 0; k < N; k++) {
                if (frontier[k] == 0) continue;
                ll need = D[i][k] - Ra;
                if (need <= Rs[0]) {
                    if (frontier[k] > 0) relaxFrom(k, 0, v);
                } else if (need <= Rs.back()) {
                    int idx = (int)(lower_bound(Rs.begin(), Rs.end(), need) - Rs.begin());
                    if (idx < frontier[k]) relaxFrom(k, idx, v);
                }
            }
        }
        if (ans < 0) printf("impossible\n");
        else printf("%lld\n", ans);
    }
    return 0;
}
