// 一本通 1790《序列划分》
// ---------------------------------------------------------------------------
// 题意：给定 n 个对 (a_i,b_i) 与正整数 m，把序列切成连续若干段，满足
//   ① 若 i<j 且 i 与 j 不在一段中，则 b_i > a_j；
//   ② 每一段的 a 的最大值之和 ≤ m；
//   在此基础上最小化「每一段 b 的和」的最大值。
//
// 关键转化（自研，见 gen-report.md）：
//   ① ⟺ 对每个切点 c（切在 c 与 c+1 之间）都有  min_{i≤c} b_i > max_{j>c} a_j。
//   证明：(⟸) 若 i<j 分属不同段，则存在切点 c 满足 i≤c<j，于是
//             b_i ≥ min_{i≤c} b_i > max_{j>c} a_j ≥ a_j；
//         (⟹) 若某切点 c 不满足，取 i*=argmin_{i≤c} b_i、j*=argmax_{j>c} a_j，
//             则 i*<j* 分属不同段且 b_{i*} ≤ a_{j*}，矛盾。
//   于是合法切点集合被唯一确定，把序列压缩成「原子段」（相邻合法切点之间）。
//   任何合法划分 = 若干连续原子段的并。
//
// 判定 + 二分：
//   二分答案 X = 每段 b 和的上限；判定「存在划分使每段 b 和 ≤ X 且 Σ max(a) ≤ m」。
//   对固定 X，DP  g[i] = 前 i 个原子段在「每段 b 和 ≤ X」下 Σ max(a) 的最小值，
//       g[i] = min_{j∈[L_i,i-1]} ( g[j] + maxA(j+1..i) )，L_i 由 b 前缀和双指针给出。
//   这是 POJ 3017 "Cut the Sequence" 的同型判定子问题：单调队列维护后缀最大值位置
//   + multiset 维护各块的 min g，做到 O(n log n) 判定；总 O(n log n · log Σb)。
//
// 参考依据：判定子问题的单调队列 DP 模板来自 POJ 3017《Cut the Sequence》
//   （https://poj.org/problem?id=3017，题解思路见 OI-Wiki「单调队列优化 DP」）。
//   本题题面条件 ① 的等价转化与整体「二分 + 判定」框架为自研：
//   在博客园 / CSDN / Bing / Brave 上以题面特征句（"不在一段中"、"每一段的a的最大值之和"、
//   "一本通 1790 序列划分"）多轮检索，均未找到该题的公开题解或原题出处，故按题面自研。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstring>
#include <climits>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;
typedef long long ll;

static const ll INF = (ll)1e16;  // 真值上界 Σmax(a) ≤ 1e5·2e9 = 2e14

static int n;
static ll m;
static vector<ll> a, b;   // 1-indexed

static int s;             // 原子段个数
static vector<ll> A, B, PB, g;

// ---- 线段树：区间 min（存 g） ----
static int segN;
static vector<ll> seg;
static void segInit(int cnt) {
    segN = 1;
    while (segN < cnt) segN <<= 1;
    seg.assign(2 * segN, INF);
}
static void segSet(int pos, ll v) {
    int p = pos + segN;
    seg[p] = v;
    for (p >>= 1; p; p >>= 1) seg[p] = min(seg[2 * p], seg[2 * p + 1]);
}
static ll segMin(int l, int r) {
    if (l > r) return INF;
    ll res = INF;
    l += segN; r += segN;
    while (l <= r) {
        if (l & 1) res = min(res, seg[l++]);
        if (!(r & 1)) res = min(res, seg[r--]);
        l >>= 1; r >>= 1;
    }
    return res;
}

// ---- 单调队列（记录 = 后缀最大值位置） ----
static vector<int> dqPos;
static vector<ll> dqLeft, dqMn, dqCand;

// 判定：是否存在划分，使每段 b 和 ≤ X 且 Σ max(a) ≤ m
static bool check(ll X) {
    segInit(s + 1);
    segSet(0, 0);
    g.assign(s + 1, INF);
    g[0] = 0;
    dqPos.assign(s + 2, 0);
    dqLeft.assign(s + 2, 0);
    dqMn.assign(s + 2, 0);
    dqCand.assign(s + 2, 0);
    int head = 0, tail = 0;
    multiset<ll> ms;
    int j0 = 0;
    for (int i = 1; i <= s; i++) {
        while (PB[i] - PB[j0] > X) j0++;      // L_i：最小的合法起点
        int L = j0;
        // 1) 弹出滑出窗口的队首记录
        while (head < tail && dqPos[head] <= L) {
            ms.erase(ms.find(dqCand[head]));
            head++;
        }
        // 2) 队首块的左端点随 L 右移
        if (head < tail && dqLeft[head] < L) {
            ms.erase(ms.find(dqCand[head]));
            dqLeft[head] = L;
            ll mm = segMin(L, dqPos[head] - 1);
            dqMn[head] = mm;
            dqCand[head] = (mm >= INF / 2) ? INF : A[dqPos[head]] + mm;
            ms.insert(dqCand[head]);
        }
        // 3) 压入 i：把 a 值 ≤ a[i] 的记录合并（它们的块并成一块）
        ll mergedMn = INF, mergedLeft = L;
        bool any = false;
        while (head < tail && A[dqPos[tail - 1]] <= A[i]) {
            tail--;
            ms.erase(ms.find(dqCand[tail]));
            mergedMn = min(mergedMn, dqMn[tail]);
            mergedLeft = dqLeft[tail];
            any = true;
        }
        ll newLeft, newMn;
        if (any) {                        // 被合并块并集 = [mergedLeft, i-1]
            newLeft = mergedLeft;
            newMn = mergedMn;
        } else if (head < tail) {         // 上一条记录必为 i-1，块 = [i-1, i-1]
            newLeft = dqPos[tail - 1];
            newMn = g[i - 1];
        } else {                          // 队列空：块 = [L, i-1]
            newLeft = L;
            newMn = segMin(L, i - 1);
        }
        ll cand;
        if (newLeft > i - 1 || newMn >= INF / 2) cand = INF;
        else cand = A[i] + newMn;
        dqPos[tail] = i; dqLeft[tail] = newLeft; dqMn[tail] = newMn; dqCand[tail] = cand;
        tail++;
        ms.insert(cand);
        g[i] = *ms.begin();
        segSet(i, g[i]);
    }
    return g[s] <= m;
}

int main() {
    if (scanf("%d %lld", &n, &m) != 2) return 0;
    a.assign(n + 2, 0);
    b.assign(n + 2, 0);
    for (int i = 1; i <= n; i++) {
        if (scanf("%lld %lld", &a[i], &b[i]) != 2) return 0;
    }
    // 条件 ① 的等价判定：合法切点 c ⟺ min_{i≤c} b_i > max_{j>c} a_j
    vector<ll> sufA(n + 3, 0);
    for (int i = n; i >= 1; i--) sufA[i] = max(sufA[i + 1], a[i]);
    vector<char> cut(n + 2, 0);
    ll preMin = LLONG_MAX;
    for (int c = 1; c < n; c++) {
        preMin = min(preMin, b[c]);
        if (preMin > sufA[c + 1]) cut[c] = 1;
    }
    // 压缩成原子段
    A.assign(1, 0);
    B.assign(1, 0);
    ll mx = 0, sum = 0;
    for (int i = 1; i <= n; i++) {
        mx = max(mx, a[i]);
        sum += b[i];
        if (i == n || cut[i]) {
            A.push_back(mx);
            B.push_back(sum);
            mx = 0; sum = 0;
        }
    }
    s = (int)A.size() - 1;
    PB.assign(s + 1, 0);
    for (int i = 1; i <= s; i++) PB[i] = PB[i - 1] + B[i];

    ll lo = 0, hi = PB[s];
    for (int i = 1; i <= s; i++) lo = max(lo, B[i]);

    if (!check(hi)) {                     // 无解（Σmax(a) ≥ max a > m）；题面数据保证有解
        printf("-1\n");
        return 0;
    }
    while (lo < hi) {
        ll mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    printf("%lld\n", lo);
    return 0;
}
