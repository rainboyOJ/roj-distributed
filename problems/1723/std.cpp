// 一本通 1723《交通》标程
//
// 题意：无向图，第 i 条边 (u,v) 有 “最拥堵耗时 x_i” 与 “完全空闲耗时 y_i”。
// 拥堵系数 a ~ U[0,1]，拥堵为 a 时该边耗时 w_i(a) = a*x_i + (1-a)*y_i。
// C 先生每天从 S 到 T，求期望意义下的最短路：
//   answer = E_a[ d(a) ] = ∫_0^1 d(a) da，d(a) = a 下 S->T 的最短路。
//
// 算法（本题全网无公开题解，按题意自研；思路见下，样例已独立核对）：
//   记一条路径 P 的 X_P = Σx_e、Y_P = Σy_e，则其代价
//       cost_P(a) = a*X_P + (1-a)*Y_P = Y_P + a*(X_P - Y_P)
//   是关于 a 的直线。d(a) = min_P cost_P(a) 是若干直线的下包络，
//   故 d(a) 在 [0,1] 上**凹**且分段线性。
//   凹函数的一个判定：若 f(mid) == (f(l)+f(r))/2，则 f 在 [l,r] 上恒为直线
//   （凹函数在区间中点达到弦值 => 全区间贴合弦，否则中点会被凸组合抬高）。
//   于是递归：对区间 [l,r] 在中点跑一次 Dijkstra 得 f(mid)，与弦值比较：
//     - 相等（容差内）：整段按梯形积分，加 area = (f(l)+f(r))/2 * (r-l)；
//     - 否则：折点在区间内，二分递归 [l,mid]、[mid,r]。
//   由于直线斜率 X_P - Y_P 是整数，跨越折点时中点间隙 ≥ Δslope * width / 4，
//   递归深度有限（取 50 深 + 容差双保险，另设 Dijkstra 调用次数上限）；
//   随机数据折点很少，实际调用次数远小于上限。
//   复杂度 O(#折点 · log(1/eps) · m log n)，n≤200、m≤400 下毫秒级。
//
// 来源说明（重要）：本题为“全网无公开题解”的题目，未检索到可参考的 C++ 代码：
//   - cn.bing.com 多组关键词（一本通 1723 交通 / 拥堵系数 / 题干特征句）均无题解；
//   - 博客园搜索（zzk.cnblogs.com）0 篇；CSDN 搜索 API 无相关结果；GitHub 代码搜索无命中；
//   - ybt 官方本题通过数仅 25 / 提交 166，且官网注明站内数据为站长自产。
//   上述算法按题面自行推导，并用 Python 精确有理数（Fraction）独立核对过题面样例 2：
//   d(0)=15、d(1/4)=14、d(1/2)=13、d(3/4)=12、d(1)=11，梯形积分恰为 13.0，与题面一致。
//
// 输出格式：题面未规定精度，样例为 "2.5" / "13.0"。故按 %.10f 输出后去掉多余
//   尾零（至少保留一位小数），既与两个样例逐字符一致，又保留足够有效位。

#include <cstdio>
#include <cmath>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>
using namespace std;

struct Edge {
    int to;
    double x, y;
};

static int n, m, S, T;
static vector<vector<Edge>> g;
static const double INF = 1e300;

// a 固定时的单源最短路（堆优化 Dijkstra），返回 dist(T)。
static double shortest(double a) {
    static vector<double> dist;
    dist.assign(n + 1, INF);
    typedef pair<double, int> P;
    priority_queue<P, vector<P>, greater<P>> pq;
    dist[S] = 0.0;
    pq.push(P(0.0, S));
    while (!pq.empty()) {
        P top = pq.top();
        pq.pop();
        int u = top.second;
        double d = top.first;
        if (u == T) return d;
        if (d > dist[u]) continue;
        for (size_t i = 0; i < g[u].size(); ++i) {
            const Edge &e = g[u][i];
            double w = a * e.x + (1.0 - a) * e.y;
            double nd = d + w;
            if (nd < dist[e.to]) {
                dist[e.to] = nd;
                pq.push(P(nd, e.to));
            }
        }
    }
    return dist[T];
}

// 全局 Dijkstra 调用预算：防最坏情形（折点极多）下超时；超出时按弦近似。
static long long dijCalls = 0;
static const long long MAX_CALLS = 100000;

// 在 [lo,hi] 上积分 d(a)；flo = d(lo)，fhi = d(hi)。
static double integrate(double lo, double hi, double flo, double fhi, int depth) {
    double mid = (lo + hi) * 0.5;
    double fm = shortest(mid);
    ++dijCalls;
    double chord = (flo + fhi) * 0.5;
    // 容差：绝对项扛小量级浮点噪声，相对项按距离量级放大
    // （Dijkstra 沿 ≤n 条边累加，相对舍入误差 ≤ n·2^-52 ≈ 5e-14）。
    double eps = 1e-8 + 1e-11 * max(max(fabs(flo), fabs(fhi)), 1.0);
    if (depth >= 50 || dijCalls > MAX_CALLS || fm <= chord + eps) {
        return chord * (hi - lo);
    }
    return integrate(lo, mid, flo, fm, depth + 1) +
           integrate(mid, hi, fm, fhi, depth + 1);
}

int main() {
    if (scanf("%d %d %d %d", &n, &m, &S, &T) != 4) return 0;
    g.assign(n + 1, vector<Edge>());
    for (int i = 0; i < m; ++i) {
        int u, v;
        double x, y;
        scanf("%d %d %lf %lf", &u, &v, &x, &y);
        g[u].push_back(Edge{v, x, y});
        g[v].push_back(Edge{u, x, y});
    }
    double f0 = shortest(0.0);
    double f1 = shortest(1.0);
    double ans = integrate(0.0, 1.0, f0, f1, 0);
    if (ans < 0.0) ans = 0.0;  // 防御：理论上不会出现

    char buf[64];
    snprintf(buf, sizeof(buf), "%.10f", ans);
    string s(buf);
    size_t dot = s.find('.');
    if (dot != string::npos) {
        size_t last = s.find_last_not_of('0');
        if (last == dot) ++last;  // 至少保留一位小数
        s.erase(last + 1);
    }
    printf("%s\n", s.c_str());
    return 0;
}
