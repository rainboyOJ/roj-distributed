/*
 * 一本通 1747《奶牛排队》标程
 * ---------------------------------------------------------------------------
 * 来源情况（诚实说明）：
 *   本题公开题解在网络检索中未能取回可用结果（Bing/cn.bing 对题面特征句
 *   「奶牛排成了一条直队」「最左边的奶牛A是最矮的」均返回无关结果，博客园
 *   搜索接口返回空，DuckDuckGo 超时）。故本题解为**自研**，依据为下方推导，
 *   并与题面样例 + 已知期望结论一致（见 gen-report.md）。
 *
 * 题意形式化：
 *   求最长的区间 [l, r]，使得
 *     (1) a[l] 是 [l, r] 内的**严格最小值**（唯一最小，即 l 处最小且中间无相等）；
 *     (2) a[r] 是 [l, r] 内的**严格最大值**（唯一最大）；
 *   （由 "A 最矮、B 最高、B>A、中间不能与 A/B 相同" 三条推出上面的严格性）
 *
 * 推导（O(n log n)，单调栈 + 二分）：
 *   记 q(l) = min{ k > l : a[k] <= a[l] }（不存在则 +inf），
 *        p(r) = max{ k < r : a[k] >= a[r] }（不存在则 0）。
 *   区间 [l, r] 合法  <=>  a[l] < a[k] (l<k<=r)  且  a[r] > a[k] (l<=k<r)
 *                   <=>  r < q(l)  且  l > p(r).
 *
 *   固定 r，记 M = min a[k] (p(r) < k < r)，取 M 在 (p(r), r) 内的**最后出现位置** l*：
 *     - 对 l*：其右侧直到 r 的所有元素都 > a[l*]（l* 是最后出现位置），故 q(l*) > r；
 *       又 l* > p(r) 保证 a[l*] < a[r]。=> 合法。
 *     - 对任何 l < l* 且 l > p(r)：若 a[l] = a[l*] 则 q(l) <= l* <= r；若 a[l] > a[l*]
 *       则 a[l*] <= a[l] 且 l* <= r 给出 q(l) <= l* <= r。均不合法。
 *   => 固定 r 的最优左端 l* 就是 (p(r), r) 上最小值的最后出现位置（= (p(r), r) 中
 *      满足 q(l) > r 的最小下标）。
 *
 *   维护两个单调栈：
 *     D：值**非增**，出栈条件 a[top] < a[r]；栈顶即 p(r)。
 *     S：值**严格增**，出栈条件 a[top] >= a[r]；栈内恰为 { l <= r : q(l) > r }，
 *        且下标递增。于是 l* = S 中第一个下标 > p(r) 的元素（二分 upper_bound）。
 *   答案 = max(r - l* + 1)（l* 存在且 < r 时）。
 *
 * 复杂度：时间 O(n log n)，空间 O(n)。n <= 1e5，值域 2^32-1 用 long long 承载。
 * 编译：g++ -O2 -std=c++17 -o std std.cpp
 */
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];

    vector<int> D;  // 值非增栈：求 p(r) = 最后一个下标 <r 且 a[p] >= a[r]
    vector<int> S;  // 值严格增栈：{ l <= r : q(l) > r }，下标递增
    D.reserve(n + 1);
    S.reserve(n + 1);

    int ans = 0;
    for (int r = 1; r <= n; ++r) {
        while (!D.empty() && a[D.back()] < a[r]) D.pop_back();
        int p = D.empty() ? 0 : D.back();
        D.push_back(r);

        while (!S.empty() && a[S.back()] >= a[r]) S.pop_back();
        S.push_back(r);

        // S 中第一个下标 > p 的元素即固定 r 的最优左端 l*
        int idx = (int)(upper_bound(S.begin(), S.end(), p) - S.begin());
        if (idx < (int)S.size() && S[idx] < r) {
            ans = max(ans, r - S[idx] + 1);
        }
    }

    cout << ans << '\n';
    return 0;
}
