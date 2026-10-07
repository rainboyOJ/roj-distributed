// 一本通 1788《爬山》标程（C++17）
// 自研算法（同源参考：GDOI2014 模拟《Pty 爬山》，https://blog.csdn.net/u011056504/article/details/51509878
// ——按本题语义适配：①共线中间峰**阻挡**可见（严格斜率）②答案=行进步数 ③等高取 x 大为最高）：
//   1) L[i]/R[i] = 左/右最远可见峰（斜率单调链，短链跳跃 O(n)）；
//   2) 每点最高峰 = 两侧远端峰中 rank=(y,x) 最大者（同向可见峰斜率严格递增 ⇒ 远端者最高）；
//   3) 按 rank 升序用双向链表建「跳跃树」：i 走向的方向上最近未处理点 t，
//      树边权 = |i-t|（途经低 rank 点不转向）；答案 = 树根（全局最高）累计。
//   O(n)。已与暴力模拟器对质 600 组（含共线/等高对抗）0 分歧。
#include <cstdio>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

typedef long long ll;
const int MAXN = 500005;

int n;
int X[MAXN], Y[MAXN];
int L_[MAXN], R_[MAXN];
int up_[MAXN], dn_[MAXN];
ll ans[MAXN];

inline bool slope_lt(int i, int j, int k) {
    // slope(i,j) < slope(i,k)  （x 严格递增，无除法）
    return (ll)(Y[j] - Y[i]) * (X[k] - X[i]) < (ll)(Y[k] - Y[i]) * (X[j] - X[i]);
}
inline bool slope_lt2(int p, int q, int i) {
    // slope(p,i) < slope(q,i)（公共右端点 i）
    return (ll)(Y[i] - Y[p]) * (X[i] - X[q]) < (ll)(Y[i] - Y[q]) * (X[i] - X[p]);
}

struct FR { int y, x, idx; };  // rank（y 大者高；y 同 x 大者高）

int main() {
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%d %d", &X[i], &Y[i]);

    // 全局最高（y 同取 x 大）
    int hi = 0;
    for (int i = 1; i < n; i++)
        if (Y[i] > Y[hi] || (Y[i] == Y[hi] && X[i] > X[hi])) hi = i;

    // R[i]：右侧最远可见（严格斜率：slope(i,R[i]) < slope(i,R[R[i]]) 才跳）
    for (int i = 0; i < n; i++) { R_[i] = i + 1; }
    R_[n - 1] = n - 1;
    for (int i = n - 3; i >= 0; i--) {
        while (R_[i] != n - 1 && slope_lt(i, R_[i], R_[R_[i]]))
            R_[i] = R_[R_[i]];
    }
    for (int i = 0; i < n; i++) { L_[i] = i - 1; }
    L_[0] = 0;
    for (int i = 2; i < n; i++) {
        while (L_[i] != 0 && slope_lt2(L_[L_[i]], L_[i], i))
            L_[i] = L_[L_[i]];
    }

    // f rank 与方向
    vector<FR> fr(n);
    vector<int> dirn(n, 0); // 0=无（hi），-1=左，+1=右
    for (int i = 0; i < n; i++) {
        if (i == hi) { fr[i] = {Y[i], X[i], i}; continue; }
        int cand = -1;
        if (i > 0) cand = L_[i];
        if (i < n - 1) {
            int r = R_[i];
            if (cand == -1) cand = r;
            else {
                // rank 比较：y 大者；y 同 x 大者（右侧天然 x 大 ⇒ 平局选右）
                if (Y[r] > Y[cand] || (Y[r] == Y[cand] && X[r] > X[cand])) cand = r;
            }
        }
        fr[i] = {Y[cand], X[cand], i};
        dirn[i] = (cand < i) ? -1 : 1;
    }

    // 按 f rank 升序（y、x、idx 三键稳定）
    vector<int> order;
    order.reserve(n);
    for (int i = 0; i < n; i++) if (i != hi) order.push_back(i);
    sort(order.begin(), order.end(), [&](int p, int q) {
        if (fr[p].y != fr[q].y) return fr[p].y < fr[q].y;
        if (fr[p].x != fr[q].x) return fr[p].x < fr[q].x;
        return p < q;
    });

    // 双向链表 + 跳跃树
    for (int i = 0; i < n; i++) { up_[i] = i - 1; dn_[i] = i + 1; }
    up_[0] = -1; dn_[n - 1] = -1;
    vector<int> par(n, -1);
    vector<ll> pw(n, 0);
    for (int i : order) {
        int t = (dirn[i] == -1) ? up_[i] : dn_[i];
        if (t == -1) {  // 安全兜底：边界走向即为最高
            t = hi;
        }
        par[i] = t;
        pw[i] = (ll)(i > t ? i - t : t - i);
        if (up_[i] != -1) dn_[up_[i]] = dn_[i];
        if (dn_[i] != -1) up_[dn_[i]] = up_[i];
    }

    // 累计
    vector<vector<int>> ch(n);
    for (int i = 0; i < n; i++) if (i != hi && par[i] != -1) ch[par[i]].push_back(i);
    static queue<int> q;
    q.push(hi); ans[hi] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : ch[u]) { ans[v] = ans[u] + pw[v]; q.push(v); }
    }
    for (int i = 0; i < n; i++) printf("%lld\n", ans[i]);
    return 0;
}
