// 一本通 1744《跳台阶》标程（C++17）
// 自研 DP（无公开题解；模型：序列分两条索引递增的链，链代价 = |首-0| + Σ相邻|Δ|，最小化总代价）：
//   状态 G_i(x)：处理完前 i 步后，一条链以 H_i 结尾、另一条以 x 结尾的最小总代价。
//   转移：G_{i+1}(y) = G_i(y) + |H_{i+1}-H_i|；G_{i+1}(H_i) = min(·, φ_i(H_{i+1}))，
//   其中 φ_i(h) = min_x G_i(x) + |h-x|（锥下包络）。
//   维护：值域压缩 + 两棵区间最值线段树（min(v-x) / min(v+x)）+ 全局懒加，
//   查询 φ 在 h 处 = min( h + min_{x≤h}(v-x), -h + min_{x>h}(v+x) )，单点下调取 min。
//   O(n log n)。答案 = min_y G_n(y)。
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;
const ll INF = (ll)4e18;

int n;
ll H[500005];
ll xs[500005];
int R;

ll A[2100005], Bseg[2100005];   // v-x / v+x 的区间最小（存储值，不含全局懒加）
ll gadd = 0;

void upd(int node, int l, int r, int pos, ll va, ll vb) {
    if (l == r) {
        if (va < A[node]) A[node] = va;
        if (vb < Bseg[node]) Bseg[node] = vb;
        return;
    }
    int mid = (l + r) / 2;
    if (pos <= mid) upd(node * 2, l, mid, pos, va, vb);
    else upd(node * 2 + 1, mid + 1, r, pos, va, vb);
    A[node] = min(A[node * 2], A[node * 2 + 1]);
    Bseg[node] = min(Bseg[node * 2], Bseg[node * 2 + 1]);
}

ll qA(int node, int l, int r, int ql, int qr) {
    if (ql > r || qr < l) return INF;
    if (ql <= l && r <= qr) return A[node];
    int mid = (l + r) / 2;
    return min(qA(node * 2, l, mid, ql, qr), qA(node * 2 + 1, mid + 1, r, ql, qr));
}
ll qB(int node, int l, int r, int ql, int qr) {
    if (ql > r || qr < l) return INF;
    if (ql <= l && r <= qr) return Bseg[node];
    int mid = (l + r) / 2;
    return min(qB(node * 2, l, mid, ql, qr), qB(node * 2 + 1, mid + 1, r, ql, qr));
}

int rk(ll x) { return (int)(lower_bound(xs, xs + R, x) - xs); }

int main() {
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%lld", &H[i]);
    // 值域压缩（含 0）
    int tot = 0;
    xs[tot++] = 0;
    for (int i = 0; i < n; i++) xs[tot++] = H[i];
    sort(xs, xs + tot);
    R = (int)(unique(xs, xs + tot) - xs);

    for (int i = 0; i <= 4 * R + 4; i++) { A[i] = INF; Bseg[i] = INF; }

    // 初始：G_1 = {(x=0, v=H[0])}
    ll m = H[0];
    ll st0 = H[0];                 // stored（显示值 = stored + gadd，gadd=0）
    upd(1, 0, R - 1, rk(0), st0 - 0, st0 + 0);


    for (int i = 1; i < n; i++) {
        ll c = llabs(H[i] - H[i - 1]);
        ll h = H[i];
        int rkh = rk(h);
        ll t = INF;
        ll la = qA(1, 0, R - 1, 0, rkh);
        if (la < INF) t = min(t, h + la + gadd);
        ll lb = qB(1, 0, R - 1, rkh + 1, R - 1);
        if (lb < INF) t = min(t, -h + lb + gadd);
        m = min(m + c, t);
        gadd += c;
        // 单点下调：key = H[i-1]。因 t ≤ G_i(H_{i-1}) + c 恒成立，新显示值恒为 t。
        int k = rk(H[i - 1]);
        ll base = t - gadd;
        upd(1, 0, R - 1, k, base - xs[k], base + xs[k]);
    }
    printf("%lld\n", m);
    return 0;
}
