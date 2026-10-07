// 一本通 1722《骑士游戏》标程（目标 ROJ 题号 1722）
//
// 题意：1 号怪兽入侵。对每只怪兽 i：
//         普通攻击：花 S_i 体力，"打死"i 但 i 死亡后会产生 R_i 只新怪兽（编号给定，可重复）；
//         法术攻击：花 K_i 体力，彻底杀死 i（不产生新怪兽）。
//       求消灭村庄内所有怪兽（从 1 号开始）的最小体力。
//
// 设 f[i] = 彻底消灭"一只 i 号怪兽及其衍生怪"的最小体力，则
//     f[i] = min( K_i ,  S_i + sum_{j=1..R_i} f[son_j(i)] )
// （各衍生怪彼此独立，代价可加；普通攻击后原怪已"死"，只需再清掉 R_i 只衍生怪。）
//
// ---- 来源（网络检索；本题即经典题 Luogu P4042 / BZOJ 3875 [AHOI2014/JSOI2014] 骑士游戏）----
// 题面特征句「JYY一共有两种攻击方式，一种是普通攻击，一种是法术攻击」检索得到多篇同题题解，
// 且数据范围逐字一致（2<=N<=2e5，1<=R_i, ΣR_i<=1e6，1<=K_i,S_i<=5e14），故确定为同题。
//   [1] https://blog.csdn.net/a1799342217/article/details/83583058
//       《BZOJ3875: [Ahoi2014&Jsoi2014]骑士游戏（洛谷P4042）》：
//       给出 f[u]=min(k_u, s_u + Σ f[v]) 的 SPFA 迭代解法；建图用两条邻接表 h1（u->产出怪）、
//       h2（产出怪->u，即反向边），每次 u 的值被更新后把它的所有"父"节点入队松弛。
//   [2] https://blog.csdn.net/sslz_fsy/article/details/86594054
//       《P4042 骑士游戏 [spfa 实现 DP]》：同一方程 + 同一"正向边 + 反向边"建图（d[i] 初值 K_i）。
//   [3] https://so.csdn.net/api/v3/search?q=P4042%20骑士游戏&t=blog
//       站内检索命中 10 篇同题题解（另含 weixin_30323961《luogu 4042 有后效性的dp》、
//       weixin_44577381《题解 洛谷 P4042》等），全部为同一方程 + SPFA / 堆实现的迭代解，无结论冲突。
// 依据说明：本题无 Special Judge，单一确定答案；上述来源与题面样例（1 号怪兽 -> 26）互相印证。
//
// ---- 本实现的改写（方程不变，只换迭代载体；工程上更稳）----
// 把 "SPFA 反复松弛" 换成**优先队列版广义 Dijkstra**（单调小根堆 + 子节点计数），
// 复杂度 O((N + ΣR) log N) 有保证，避开 SPFA 的最坏情况：
//   · d[i] 初值 K_i（法术秒杀）全部入堆；每次取出当前最小的未定稿节点 u，定稿 f[u]=d[u]；
//   · u 定稿后，对每个"能产出 u 的怪兽 p"（反向边）做 acc[p] += f[u]，cnt[p]++；
//     一旦 cnt[p] == R_p（p 的全部产出怪都已定稿），就用 S_p + acc[p] 入堆松弛 p。
//   正确性依据（Dijkstra 对"单调超图/单调方程组"的推广）：
//     方程右端对每个 f[v] 单调不减，且普通攻击代价 S_u >= 1 > 0，故最优普通攻击分支里
//     所有子怪都满足 f[v] < f[u]；于是按 f 递增序定稿时，任一节点 p 的 R_p 个子节点
//     必在 p 之前定稿，acc[p] 恰为 Σf[v] 的真实值，得到正确候选 min(K_p, S_p+acc[p])。
//   防溢出：acc[p] 只与 K_p 比较即可，累计一旦超过 K_p 就置 big[p] 并停止参与
//     （此时 S_p+acc[p] > K_p >= f[p]，永远不可能更优）；所有累加值 <= 1e15 << 9.2e18。
//   注：f[i] <= K_i <= 5e14，答案必在 long long 内。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std

#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
#include <utility>
#include <algorithm>

typedef long long LL;

static const int MAXN = 200000 + 5;
static const int MAXE = 1000000 + 5;

static int N;
static LL S[MAXN], K[MAXN];
static int R[MAXN];

/* ---------- 快速输入（fread 手写整数读入；ΣR<=1e6，输入可达数十 MB） ---------- */
namespace fastio {
static const int BUFSZ = 1 << 20;
static char buf[BUFSZ];
static int len = 0, pos = 0;
inline int gc() {
    if (pos == len) {
        len = (int)fread(buf, 1, BUFSZ, stdin);
        pos = 0;
        if (len <= 0) return -1;
    }
    return (unsigned char)buf[pos++];
}
inline LL readInt() {
    int c = gc();
    while (c != '-' && (c < '0' || c > '9')) {
        if (c < 0) return 0;
        c = gc();
    }
    LL sgn = 1;
    if (c == '-') { sgn = -1; c = gc(); }
    LL x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x * sgn;
}
}  // namespace fastio

/* ---------- 图：CSR 存 "出边"（i -> 产出怪）与 "入边"（产出怪 -> i，即父表） ---------- */
static int outStart[MAXN], outTo[MAXE];
static int inStart[MAXN], inFrom[MAXE];
static int bucket[MAXN];

int main() {
    N = (int)fastio::readInt();

    int m = 0;
    for (int i = 1; i <= N; i++) {
        S[i] = fastio::readInt();
        K[i] = fastio::readInt();
        R[i] = (int)fastio::readInt();
        outStart[i] = m;
        for (int j = 0; j < R[i]; j++) {
            int v = (int)fastio::readInt();
            outTo[m++] = v;                    // 越界防御交给题面保证（1<=v<=N）
        }
    }
    outStart[N + 1] = m;

    /* 反向表：按"产出怪编号"桶排序，O(N + ΣR) */
    memset(bucket, 0, sizeof(int) * (size_t)(N + 2));
    for (int e = 0; e < m; e++) bucket[outTo[e]]++;
    int accPos = 0;
    for (int v = 1; v <= N; v++) {
        int c = bucket[v];
        inStart[v] = accPos;
        bucket[v] = 0;
        accPos += c;
    }
    inStart[N + 1] = accPos;
    for (int i = 1; i <= N; i++)
        for (int e = outStart[i]; e < outStart[i + 1]; e++) {
            int v = outTo[e];
            inFrom[inStart[v] + bucket[v]++] = i;
        }

    /* ---------- 广义 Dijkstra ---------- */
    static bool done[MAXN];
    static bool big[MAXN];     // acc[p] 已超过 K_p，S 分支必不优，停止累计
    static LL accum[MAXN];     // 已定稿子怪的 f 之和
    static int settled[MAXN];  // 已定稿子怪个数

    typedef std::pair<LL, int> P;  // (当前候选代价, 怪兽编号)
    std::priority_queue<P, std::vector<P>, std::greater<P> > pq;
    for (int i = 1; i <= N; i++) pq.push(P(K[i], i));

    LL ans = -1;
    while (!pq.empty()) {
        P cur = pq.top();
        pq.pop();
        LL d = cur.first;
        int u = cur.second;
        if (done[u]) continue;
        done[u] = true;            // 依 f 递增序定稿
        if (u == 1) { ans = d; break; }

        for (int e = inStart[u]; e < inStart[u + 1]; e++) {
            int p = inFrom[e];
            if (done[p] || big[p]) continue;
            accum[p] += d;
            if (accum[p] > K[p]) { big[p] = true; continue; }
            if (++settled[p] == R[p]) pq.push(P(S[p] + accum[p], p));
        }
    }

    printf("%lld\n", ans);
    return 0;
}
