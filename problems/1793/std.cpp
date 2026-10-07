// 一本通 1793《鏖战字符串》（ROJ 1793）
// 题意：给定长度 n 的字符串与每个位置的删除难度 dif[i]（0<=dif[i]<=50）。
//   把前缀 [1,i] 分割成若干连续子串，每个子串二选一删除：
//     ① 代价 a*x^2 + b            （x = 子串 dif 之和）
//     ② 代价 c*x + d，当且仅当子串中出现次数最多的字符的出现次数 maxfreq ∈ [l, r]
//   求删去每个前缀 [1,i] 的最少用时（输出 n 行）。
//
// ---------------------------------------------------------------------------
// 来源 / 依据：
//   本题为《信息学奥赛一本通 · 高手训练篇 · 五、动态规划》中的题，题面/样例与
//   content.md 逐字一致（见下「样例验证」）。
//   网络检索情况（如实记录）：按题面特征句在 Bing（含 cn.bing.com、mkt=zh-CN）、
//   Baidu、DuckDuckGo、Sogou、Brave、以及 CSDN/博客园站内检索共 5 轮，均未命中
//   本题题解（搜索引擎对中文 OI 长尾题返回结果与本题无关/被反爬拦截，未见
//   「鏖战字符串」「量子态的字符串」相关 OI 博客）。故按「检索 3-4 轮无果即自研」
//   的约定，由题面独立推导实现，算法与正确性论证见下。
//
// ---------------------------------------------------------------------------
// 算法（O(n)）：
//   记 S[i] = sum_{k<=i} dif[k]（前缀和，因 dif>=0 故 S 单调不减）。
//   dp[0] = 0，对 i>=1：
//     dp[i] = min_{0<=j<i} ( dp[j] + cost(j+1, i) )
//     cost(l,r) = min( a*X^2 + b ,  [maxfreq(l,r) ∈ [l,r]] * (c*X + d) )，X = S[r]-S[l-1]
//
//   (A) 方法① 部分 —— 凸包（CHT）：
//       dp[j] + a*(S_i-S_j)^2 + b
//     = a*S_i^2 + b + (-2a*S_j)*S_i + (dp[j] + a*S_j^2)
//     = a*S_i^2 + b - max_j [ (2a*S_j)*S_i + (-dp[j] - a*S_j^2) ]
//     直线的斜率 2a*S_j 随 j 单调不减，询问点 S_i 也单调不减
//     => 单调凸包（max-hull）O(n)。交叉相乘用 __int128 防溢出。
//
//   (B) 方法② 部分 —— 频率窗口 + 单调队列：
//     固定 i，令 f(j) = maxfreq(j+1, i)。j 增大 => 窗口变短 => f 单调不增。
//     故满足「f(j) >= l」的 j 是一个前缀 [0, L_i]，满足「f(j) <= r」的 j 是一个
//     后缀 [R_i, i-1]，交集 J_i = [R_i, L_i] 是一个连续区间（可能为空，例如 l>r）。
//     由单调性可证 L_i、R_i 均随 i 单调不减：
//       设 s_l(i) = max_c ( 字符 c 第 (cnt_c - l + 1) 次出现的位置 )，则 L_i = s_l(i)-1；
//       设 R_i     = max_c ( 字符 c 第 (cnt_c - r)     次出现的位置 )，无则取 0。
//       每个字符的这两个位置随 i 只增不减，取 max 后仍单调不减。
//     实现：对每个字符维护「最近 l 次出现」的队列（队首即 s_l 的候选）与
//     「最近 r+1 次出现」的队列（队首即 R 的候选），用滚动最大值 O(n) 得到 L_i、R_i。
//     于是 dp2[i] = min_{j∈[R_i, L_i]} ( dp[j] - c*S_j ) + c*S_i + d，
//     区间两端点均单调不减 => 单调队列求滑动窗口最小值，O(n)。
//
//   dp[i] = min(dp1[i], dp2[i])。
//
// 边界：l > r 时 J_i 恒为空，方法② 自动失效，退化为纯 CHT（对应测试点 15）。
//       l=1 时 s_l(i)=i => L_i=i-1（任何非空子串 maxfreq>=1）；r>=n 时 R_i=0。
//
// 复杂度 O(n) 时间、O(n) 空间；n<=1e5、a,b,c,d<=233、dif<=50 时
// 中间量最大约 2*233*(50*1e5)*(50*1e5) ≈ 1.2e16，long long 安全。
// ---------------------------------------------------------------------------

#include <algorithm>
#include <climits>
#include <cstdio>
#include <deque>

using namespace std;

typedef long long ll;
typedef __int128 lll;

static const int MAXN = 100005;

static int n;
static ll A, B, C, D, Lp, Rp;
static char str_[MAXN];
static ll dif_[MAXN], S_[MAXN], dp_[MAXN];

// ---- max-hull：斜率单调不减加入，询问 x 单调不减 ----
struct Line {
    ll m, b;  // y = m*x + b
};

static inline ll evalLine(const Line &l, ll x) { return l.m * x + l.b; }

// p,q,r 斜率严格递增；判断 q 对最大凸包是否冗余
static inline bool hullBad(const Line &p, const Line &q, const Line &r) {
    // (p.b-q.b)/(q.m-p.m) >= (q.b-r.b)/(r.m-q.m)  <=>  q 冗余
    lll lhs = (lll)(p.b - q.b) * (lll)(r.m - q.m);
    lll rhs = (lll)(q.b - r.b) * (lll)(q.m - p.m);
    return lhs >= rhs;
}

static deque<Line> hull;

static void hullAdd(ll m, ll b) {
    if (!hull.empty() && hull.back().m == m) {  // 同斜率只保留截距更优者
        if (hull.back().b >= b) return;
        hull.pop_back();
    }
    while (hull.size() >= 2) {
        const Line &p = hull[hull.size() - 2];
        const Line &q = hull.back();
        Line r{m, b};
        if (hullBad(p, q, r)) hull.pop_back();
        else break;
    }
    hull.push_back(Line{m, b});
}

static ll hullQueryMax(ll x) {
    while (hull.size() >= 2 && evalLine(hull[0], x) <= evalLine(hull[1], x))
        hull.pop_front();
    return evalLine(hull[0], x);
}

// ---- 方法② 的滑动窗口最小值：窗口 [R_i, L_i] 两端点均单调不减 ----
static deque<int> win;  // 存下标 j，按 h[j]=dp[j]-C*S[j] 递增

static inline ll hval(int j) { return dp_[j] - C * S_[j]; }

int main() {
    if (scanf("%d %lld %lld %lld %lld %lld %lld", &n, &A, &B, &C, &D, &Lp, &Rp) != 7)
        return 0;
    scanf("%s", str_ + 1);
    for (int i = 1; i <= n; i++) {
        scanf("%lld", &dif_[i]);
        S_[i] = S_[i - 1] + dif_[i];
    }

    static deque<int> ql[26], qr[26];  // ql: 最近 Lp 次出现；qr: 最近 Rp+1 次出现
    ll sL = 0, sR = 0;                 // sL=s_l(i)，sR=R_i（滚动最大值）
    ll prevL = -1;                     // 上一次已推入窗口的右端点 L_i

    dp_[0] = 0;
    for (int i = 1; i <= n; i++) {
        int ch = str_[i] - 'a';

        ql[ch].push_back(i);
        if ((ll)ql[ch].size() > Lp) ql[ch].pop_front();
        if ((ll)ql[ch].size() == Lp) sL = max(sL, (ll)ql[ch].front());

        qr[ch].push_back(i);
        if ((ll)qr[ch].size() > Rp + 1) qr[ch].pop_front();
        if ((ll)qr[ch].size() == Rp + 1) sR = max(sR, (ll)qr[ch].front());

        ll Li = (sL == 0 ? -1 : sL - 1);  // J_i = [Ri, Li]
        ll Ri = sR;

        for (ll j = prevL + 1; j <= Li; j++) {  // L 单调不减，增量推入
            ll h = hval((int)j);
            while (!win.empty() && hval(win.back()) >= h) win.pop_back();
            win.push_back((int)j);
        }
        if (Li > prevL) prevL = Li;
        while (!win.empty() && (ll)win.front() < Ri) win.pop_front();

        // 方法①：加入 j = i-1 的直线后询问
        hullAdd(2 * A * S_[i - 1], -(dp_[i - 1] + A * S_[i - 1] * S_[i - 1]));
        ll M = hullQueryMax(S_[i]);
        ll dp1 = A * S_[i] * S_[i] + B - M;

        // 方法②：J_i 上的最小 h
        ll dp2 = LLONG_MAX;
        if (!win.empty()) {
            int j = win.front();
            dp2 = dp_[j] - C * S_[j] + C * S_[i] + D;
        }

        dp_[i] = min(dp1, dp2);
        printf("%lld\n", dp_[i]);
    }
    return 0;
}
