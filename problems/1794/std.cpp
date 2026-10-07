// 题目：一本通 1794《分数》
// 来源核对：http://ybt.ssoier.cn:8088/problem_show.php?pid=1794 （题面原文逐字一致）
// 检索记录：Bing（含 RSS 接口）/Google/Sogou/CSDN 精确特征句检索均被拦截或只返回
//          无关词典页，4 轮无果 —— 本题 std 为自研实现，算法推导见下（见 gen-report.md）。
//
// ---------------------------------------------------------------------------
// 题意
//   选任意子集标记。得分 = (完全被标记的连续区间 [L,R] 的个数) - (被标记数字之和)。
//   M 组独立询问：把 T_P 改成 X 后，得分最大值。
//
// 建模
//   标记集合按极大连续段分解，长度 c 的一段贡献 C(c) - sum(T) ，C(c)=c(c+1)/2。
//   故原问题 = 在 1..N 上选若干互不相邻的不相交区间，最大化 sum f(l,r)，
//   其中 f(l,r) = C(r-l+1) - (S[r]-S[l-1])，S 为 T 的前缀和。
//
//   记 dpL[i] = 前缀 [1..i] 的最优值（dpL[0]=0），
//       dpR[i] = 后缀 [i..N] 的最优值（dpR[N+1]=0）。
//
//   询问 (P,X)：设 d = X - T_P。最优方案分两类：
//     (a) 没有任何区间覆盖 P（P 不标记）：A(P) = dpL[P-1] + dpR[P+1]；
//     (b) 恰有一个区间 [a,b] ∋ P 被标记：取值 = dpL[a-2] + f_X(a,b) + dpR[b+2]
//          = [ dpL[a-2] + f(a,b) + dpR[b+2] ] - d  =  B(P) - d。
//     因为覆盖 P 的区间至多一个（区间互不相交），所以
//         ans(P,X) = max( A(P), B(P) - d )。
//     关键点：A(P)、B(P) 只依赖原数组，与 X 无关 —— 一次预处理即可 O(1) 回答。
//
// 求 dpL / dpR（CHT 在线 O(N log N)）
//   dpL[i] = max( dpL[i-1], (i^2+i)/2 - S[i] + max_{m<i} ( c_m - i*m ) ),
//       c_m = dpL[m-1] + S[m] + m(m-1)/2      （dpL[-1]=0）
//   即对直线 y = m*x + c_m 查询 x = -i。
//   dpR[i] = max( dpR[i+1], S[i-1] + (i^2-i)/2 + max_{j>i} ( e_j - i*j ) ),
//       e_j = dpR[j+1] - S[j-1] + (j^2+j)/2   （dpR[N+2]=0）
//   即对直线 y = -j*x + e_j 查询 x = i。
//
// 求所有 B(P)（分治 + CHT，O(N log N)）
//   令 α(a) = dpL[a-2] + S[a-1] + (a^2-3a)/2,
//      β(b) = dpR[b+2] - S[b]   + (b^2+3b+2)/2,
//   则 dpL[a-2] + f(a,b) + dpR[b+2] = α(a) + β(b) - a*b。
//   B(P) = max_{a<=P<=b} ( α(a) + β(b) - a*b )。
//   权矩阵 α(a)+β(b)-a*b 是反 Monge 的（a1<a2,b1<b2 时
//   W(a1,b1)+W(a2,b2) <= W(a1,b2)+W(a2,b1)），故分治：
//     solve(lo,hi) 处理 a,b ∈ [lo,hi] 的区间；
//     跨中点 mid 的区间 a∈[lo,mid], b∈[mid+1,hi]：
//       对 P∈[lo,mid] 需要 a<=P 且 b>=mid+1 → max_{a<=P}( α(a) + max_b(β(b)-a*b) )
//         → 用 b 的凸包对 x=a 查询，再做前缀 max；
//       对 P∈[mid+1,hi] 需要 b>=P 且 a<=mid → max_{b>=P}( β(b) + max_a(α(a)-a*b) )
//         → 用 a 的凸包对 x=b 查询，再做后缀 max。
//     两侧斜率与查询 x 都单调，凸包用指针扫描 O(size)。
//
// 复杂度 O(N log N + M)，N,M<=3e5；实测最大点 < 0.6s（见 gen-report.md）。
// 数值范围：C(3e5)≈4.5e10，sum T<=1e12，全部 long long 内，凸包叉积用 __int128。
// ---------------------------------------------------------------------------

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <climits>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
typedef long long ll;

static const ll NEG = LLONG_MIN / 4;

// 上凸包（求最大值），要求斜率按严格递增顺序加入。
struct Hull {
    vector<ll> M, C;  // M: 斜率, C: 截距
    void clear() { M.clear(); C.clear(); }
    void add(ll m, ll c) {
        if (!M.empty() && M.back() == m) {
            if (C.back() >= c) return;  // 同斜率保留截距更大者
            M.pop_back(); C.pop_back();
        }
        while (M.size() >= 2) {
            int n = (int)M.size();
            // 中间线 b 冗余 <=> (a.c-b.c)*(c.m-b.m) >= (b.c-c.c)*(b.m-a.m)
            __int128 lhs = (__int128)(C[n - 2] - C[n - 1]) * (m - M[n - 1]);
            __int128 rhs = (__int128)(C[n - 1] - c) * (M[n - 1] - M[n - 2]);
            if (lhs >= rhs) { M.pop_back(); C.pop_back(); }
            else break;
        }
        M.push_back(m); C.push_back(c);
    }
    ll eval(int i, ll x) const { return M[i] * x + C[i]; }
    // 任意 x 的二分查询
    ll queryBS(ll x) const {
        int lo = 0, hi = (int)M.size() - 1;
        while (lo < hi) {
            int mid = (lo + hi) >> 1;
            if (eval(mid, x) <= eval(mid + 1, x)) lo = mid + 1; else hi = mid;
        }
        return eval(lo, x);
    }
};

int N;
vector<ll> T, S, dpL, dpR, al, be, res, Uarr;

void solve(int lo, int hi) {
    if (lo > hi) return;
    if (lo == hi) {
        ll v = al[lo] + be[lo] - (ll)lo * lo;  // 区间 [lo,lo]
        if (v > res[lo]) res[lo] = v;
        return;
    }
    int mid = (lo + hi) >> 1;
    solve(lo, mid);
    solve(mid + 1, hi);

    Hull H;
    // ---- 跨中点：P ∈ [lo, mid]，需要 a<=P，b 固定取 [mid+1,hi] ----
    // 直线斜率 -b（b 递减 → 斜率递增），查询 x=a（递增）→ 指针单调
    H.clear();
    for (int b = hi; b >= mid + 1; --b) H.add(-(ll)b, be[b]);
    {
        int ptr = 0, sz = (int)H.M.size();
        ll pref = NEG;
        for (int a = lo; a <= mid; ++a) {
            while (ptr + 1 < sz && H.eval(ptr + 1, a) >= H.eval(ptr, a)) ++ptr;
            ll v = al[a] + H.eval(ptr, a);
            if (v > pref) pref = v;
            if (pref > res[a]) res[a] = pref;
        }
    }
    // ---- 跨中点：P ∈ [mid+1, hi]，需要 b>=P，a 固定取 [lo,mid] ----
    // 直线斜率 -a（a 递减 → 斜率递增），查询 x=b（递增）→ 指针单调
    H.clear();
    for (int a = mid; a >= lo; --a) H.add(-(ll)a, al[a]);
    {
        int ptr = 0, sz = (int)H.M.size();
        for (int b = mid + 1; b <= hi; ++b) {
            while (ptr + 1 < sz && H.eval(ptr + 1, b) >= H.eval(ptr, b)) ++ptr;
            Uarr[b] = be[b] + H.eval(ptr, b);
        }
        ll suf = NEG;
        for (int b = hi; b >= mid + 1; --b) {   // 后缀 max：P 可取 [P, hi] 的任意 b
            if (Uarr[b] > suf) suf = Uarr[b];
            if (suf > res[b]) res[b] = suf;
        }
    }
}

int main() {
    // ---- 快读 ----
    int n;
    if (scanf("%d", &n) != 1) return 0;
    N = n;
    T.assign(N + 1, 0);
    S.assign(N + 1, 0);
    for (int i = 1; i <= N; ++i) { scanf("%lld", &T[i]); S[i] = S[i - 1] + T[i]; }

    // ---- dpL：前缀最优 ----
    dpL.assign(N + 1, 0);
    {
        Hull H;
        for (int i = 1; i <= N; ++i) {
            int m = i - 1;
            ll cm = (m == 0 ? 0 : dpL[m - 1]) + S[m] + (ll)m * (m - 1) / 2;
            H.add(m, cm);                       // 斜率 m 递增
            ll cand = (ll)i * (i + 1) / 2 - S[i] + H.queryBS(-(ll)i);
            dpL[i] = max(dpL[i - 1], cand);
        }
    }
    // ---- dpR：后缀最优 ----
    dpR.assign(N + 3, 0);                       // dpR[N+1]=dpR[N+2]=0
    {
        Hull H;
        for (int i = N; i >= 1; --i) {
            int j = i + 1;
            ll ej = dpR[j + 1] - S[j - 1] + (ll)j * (j + 1) / 2;
            H.add(-(ll)j, ej);                  // j 递减 → 斜率递增
            ll cand = S[i - 1] + (ll)i * (i - 1) / 2 + H.queryBS((ll)i);
            dpR[i] = max(dpR[i + 1], cand);
        }
    }

    // ---- α, β 与所有 B(P) ----
    al.assign(N + 1, 0);
    be.assign(N + 1, 0);
    for (int a = 1; a <= N; ++a) {
        ll dl = (a - 2 >= 0) ? dpL[a - 2] : 0;  // dpL[-1]=0
        al[a] = dl + S[a - 1] + ((ll)a * a - 3LL * a) / 2;
    }
    for (int b = 1; b <= N; ++b) {
        be[b] = dpR[b + 2] - S[b] + ((ll)b * b + 3LL * b + 2) / 2;
    }
    res.assign(N + 1, NEG);
    Uarr.assign(N + 2, 0);
    solve(1, N);

    // ---- 回答询问 ----
    int M;
    scanf("%d", &M);
    string out;
    out.reserve((size_t)M * 15);
    char buf[32];
    for (int q = 0; q < M; ++q) {
        int P; ll X;
        scanf("%d %lld", &P, &X);
        ll d = X - T[P];
        ll noCover = dpL[P - 1] + dpR[P + 1];   // (a) 不含覆盖 P 的区间
        ll withCover = res[P] - d;              // (b) 含覆盖 P 的区间
        ll ans = max(noCover, withCover);
        if (ans < 0) ans = 0;
        int len = snprintf(buf, sizeof(buf), "%lld\n", ans);
        out.append(buf, len);
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
