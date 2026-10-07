// 一本通 1715《公交旅行》 标程
//
// 题意：n 个站台、m 条环形公交线路。第 i 条线路由 t_i 个站台组成（t_i>=2，同一站台可
//   在一线上出现多次但不相邻）。0 时刻第 i 辆公交车在 s_i[1]，之后每个时刻行驶到线路中
//   的下一个站台，到达终点站后下一时刻回到始发站（即按位置 t mod t_i 循环）。
//   0 时刻我在站台 1。若某时刻我与某辆公交车同处一个站台即可上车，可在任意时刻下车，
//   上下车不耗时；一次只能坐一辆车，但可换乘。求最早到达每个站台的时刻，不可达输出 -1。
//
// 建模（与网络题解一致）：
//   把"第 i 条线路的第 j 个位置"看作一个开门时刻固定的班次：线路 i 的公交车只在
//   时刻 T ≡ j (mod t_i) 出现在站台 s_i[j]。于是线路 i 的相邻两站 s_i[j] -> s_i[(j+1) mod t_i]
//   构成一条"开放时刻 T ≡ j (mod t_i)"的道路（费时 1）。
//   若我在时刻 d 位于站台 s_i[j]，则最早可于
//       T = d + ((j - d) mod t_i + t_i) mod t_i
//   上车，并在 T+1 时刻到达 s_i[(j+1) mod t_i]。
//   由于"早到不会更差"（多等一会儿不花代价），在站台图上跑 Dijkstra 即得每个站台的最早
//   到达时刻；边权在松弛时实时计算，不必显式建图。
//   复杂度 O(Σt_i · log Σt_i)，空间 O(n + Σt_i)。
//
// 来源：CSDN《两道水题 异或+公交旅行（扫描线+异或线性基）（最短路）》
//   https://blog.csdn.net/weixin_43960414/article/details/115399232
//   （原文给出同一建模："每条道路连接两个站点 u_i,v_i，该道路开放的时间点
//    T_i ≡ k_i (mod P_i) …… 我们肯定是能早到就早到，所以只要不把图建出来，每次实时
//    获得边权，然后跑最短路就可以获得满分"。本文件按其思路独立重写并自行验证。）
//   题面数据范围：n,m <= 1e5，Σt_i <= 2e5。

#include <cstdio>
#include <vector>
#include <queue>
using namespace std;

typedef long long ll;
static const ll INF = (ll)4e18;

// ---------- 快速读入 ----------
static char ibuf[1 << 22];
static int ilen = 0, ipos = 0;

static inline int gc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return ibuf[ipos++];
}

static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = gc();
    }
    return x;
}

int main() {
    int n = readInt(), m = readInt();

    vector<int> t(m), off(m);
    vector<int> pool;                       // 所有线路站台顺序拼接
    pool.reserve(2 << 18);

    // at[v] = 站台 v 上出现的所有 (线路号, 位置)
    vector<vector<pair<int, int> > > at(n + 1);

    for (int i = 0; i < m; i++) {
        int ti = readInt();
        t[i] = ti;
        off[i] = (int)pool.size();
        for (int j = 0; j < ti; j++) {
            int s = readInt();
            pool.push_back(s);
            at[s].push_back(make_pair(i, j));
        }
    }

    vector<ll> dist(n + 1, INF);
    vector<char> done(n + 1, 0);
    dist[1] = 0;

    // 小根堆：(时刻, 站台)
    priority_queue<pair<ll, int>, vector<pair<ll, int> >, greater<pair<ll, int> > > pq;
    pq.push(make_pair((ll)0, 1));

    while (!pq.empty()) {
        pair<ll, int> top = pq.top();
        pq.pop();
        ll d = top.first;
        int v = top.second;
        if (done[v]) continue;
        done[v] = 1;
        dist[v] = d;

        // 站台 v 上的每一班车：实时算边权
        for (size_t k = 0; k < at[v].size(); k++) {
            int r = at[v][k].first;
            int p = at[v][k].second;
            int per = t[r];
            // 最早 T >= d 且 T ≡ p (mod per)
            ll rmd = (ll)(p - d % per) % per;
            if (rmd < 0) rmd += per;
            ll T = d + rmd;
            // T == d 表示此刻公交正停在该站台，可立即上车
            int nxt = pool[off[r] + (p + 1) % per];
            if (done[nxt]) continue;
            if (T + 1 < dist[nxt]) {
                dist[nxt] = T + 1;
                pq.push(make_pair(dist[nxt], nxt));
            }
        }
    }

    // 输出站台 2..n 的最早到达时刻
    for (int i = 2; i <= n; i++) {
        if (i > 2) putchar(' ');
        if (dist[i] >= INF) fputs("-1", stdout);
        else printf("%lld", dist[i]);
    }
    putchar('\n');
    return 0;
}
