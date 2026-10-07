// 一本通 1676《手机游戏》标准程序（C++17，stdin -> stdout）
//
// 题意：一排 n 个怪物，第 i 个怪物血量 m_i。有 k 个伤害均为 p 的火球，
//   每个火球可射向任意一个怪物。射向位置 i 的火球使该怪物掉 p 血，
//   并使其左侧第 j 个怪物（j <= i）受到 max(0, p - (i-j)^2) 的溅射伤害。
//   求能消灭所有怪物的最小 p。题面明确："血量为负的时候，它就死了"，
//   即死亡条件是血量 < 0，等价于对第 i 个怪物造成的总伤害必须 >= m_i + 1。
//
// 参考来源（思路改写，与题面冲突处一律以题面为准）：
//   [一本通1676]手机游戏 题解 - Icys - 博客园（360 搜索命中，正文反爬，思路自研重构）
//   https://www.so.com/link?m=wkRsDFU4uI%2FLFEStxu0T1%2Fapl7zEJYcW04CIoKj4laSm0ZDYfGVbcrbRVn1LgE1lkZt%2Fc70NkOStkp5GueBV7nceCw8F2FaE1P%2F7uHBQEXl5PgG1W7kLXP9HynRmMTURyIYI9yGLfnH7flrwjZZKMgyVtGc8JZysztyLZ%
//   信息学奥赛一本通高手训练 题解目录 - CSDN（确认本题属于「二分与三分」章节）
//   https://blog.csdn.net/qq_36230375/article/details/136483654
//
// 算法：
//   二分答案 p。check(p) 用贪心求"消灭所有怪物所需的最少火球数"：
//     从右向左处理（先炸最右边的）。对位置 i，记 S 为右侧已放火球对 i 的溅射总伤害，
//     若 S < m_i + 1，则还需 (m_i+1-S) 的伤害。放在 i 自身的火球对 i 造成满伤害 p、
//     对更左侧位置的溅射也严格大于放在右侧任意位置的火球，故在 i 处补
//     ceil((m_i+1-S)/p) 个火球是贪心最优。
//   右侧火球对 i 的溅射 S 用"滑动窗口 + 三项和" O(1) 维护：
//     S = sum_{j in (i, i+R]} cnt[j] * (p - (j-i)^2)
//       = (p - i^2) * sumCnt + 2*i*sumJ - sumJ2
//     其中 R = floor(sqrt(p-1))（溅射严格大于 0 的最远距离），
//     sumCnt/sumJ/sumJ2 为窗口内 cnt[j]、cnt[j]*j、cnt[j]*j*j 的和。
//   总复杂度 O(n log(1e9))，n<=50000 时远小于 1s。
//
// 正确性说明见 gen-report.md。

#include <cstdio>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;

int n;
ll k;
vector<ll> m;

// 整数开方：返回 floor(sqrt(x))，x >= 0
ll isqrt(ll x) {
    if (x <= 0) return 0;
    ll r = (ll)sqrtl((long double)x);
    while ((r + 1) * (r + 1) <= x) r++;
    while (r * r > x) r--;
    return r;
}

// check(p)：p 是否足以用 <= k 个火球消灭所有怪物（等价于最少火球数 <= k）。
bool check(ll p) {
    ll R = isqrt(p - 1);              // 溅射伤害 >0 的最远距离
    vector<ll> cnt(n, 0);             // 每个位置实际放置的火球数
    ll sumCnt = 0, sumJ = 0, sumJ2 = 0; // 当前窗口内三项和
    ll total = 0;                     // 已用火球总数

    for (ll i = n - 1; i >= 0; i--) {
        // 当前窗口：右侧且距离 <= R 的火球来源 j \in [i+1, i+R]
        ll S = (p - i * i) * sumCnt + 2 * i * sumJ - sumJ2;

        ll need = m[i] + 1 - S;       // 还需造成的伤害（血量必须 <0）
        ll c = 0;
        if (need > 0) {
            c = (need + p - 1) / p;   // ceil(need/p)
            total += c;
            if (total > k) return false;
        }
        cnt[i] = c;

        // 维护窗口：从 [i+1, i+R] 移动到下一位置的 [i, i+R-1]
        // 1) 去掉距离恰为 R+1 的来源 i+R（R>=1 时它才可能位于旧窗口内）
        ll rem = i + R;
        if (R >= 1 && rem < n) {
            ll cr = cnt[rem];
            if (cr) {
                sumCnt -= cr;
                sumJ -= cr * rem;
                sumJ2 -= cr * rem * rem;
            }
        }
        // 2) 加入位置 i 的火球来源
        if (c) {
            sumCnt += c;
            sumJ += c * i;
            sumJ2 += c * i * i;
        }
    }
    return total <= k;
}

int main() {
    if (scanf("%d %lld", &n, &k) != 2) return 0;
    m.resize(n);
    ll maxm = 0;
    for (int i = 0; i < n; i++) {
        scanf("%lld", &m[i]);
        if (m[i] > maxm) maxm = m[i];
    }

    // 上界：在最后一个怪物放 1 个火球，p = maxm+1+(n-1)^2 时，
    // 溅射到任意左侧怪物的伤害都 >= maxm+1 >= m_i+1，故 check(hi) 必为真。
    ll lo = 1;
    ll hi = maxm + 1 + (ll)(n - 1) * (n - 1);
    while (lo < hi) {
        ll mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    printf("%lld\n", lo);
    return 0;
}
