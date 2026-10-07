// 一本通 1671《扑克牌》标程
// 思路：二分答案 + 可行性判定（贪心）。
//   设要整理 k 副牌，则第 i 种普通牌至少缺 max(0, k-a_i) 张，
//   共需特殊牌 need = sum max(0, k-a_i) 张。
//   可行当且仅当 need <= b（特殊牌够用）且 need <= k
//   （每副牌最多用 1 张特殊牌，即最多 k 副牌是"缺一种普通牌"的）。
//   need(k) 关于 k 单调不降，且可行集为 [0, K] 区间，故二分最大 k。
// 参考来源（网络题解，已按题面自行改写并编译验证）：
//   1) https://blog.csdn.net/qq_36230375/article/details/136381440
//      （"信息学奥赛一本通高手训练 1671：扑克牌 贪心算法"：
//       二分法 check 为 sum(max(0,x-a[i]))<=b 且 <=x；并指出
//       "特殊牌一副牌中只能有一张，所以使用的特殊牌数量不能超过答案"）
//   2) https://blog.csdn.net/weixin_30836759/article/details/99279574
//      （转载自 http://www.cnblogs.com/KGW-/p/11247807.html ，贪心+堆做法）
//   3) https://blog.csdn.net/andyc_03/article/details/109165938
//      （【贪心】ybtoj1671扑克牌，贪心+堆做法）
#include <cstdio>

typedef long long ll;

const int MAXN = 1000005;

int n;
ll b;
int a[MAXN];

// 判断能否整理出 x 副牌
bool check(ll x)
{
    ll need = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] < x) {
            need += x - a[i];
            if (need > x)   // 特殊牌用得比副数还多：必有一副要用 2 张，不可行
                return false;
        }
    }
    return need <= b;   // need <= x 已在循环中保证
}

int main()
{
    scanf("%d %lld", &n, &b);
    ll sum = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        sum += a[i];
    }
    // k 副牌共需 k*n 张牌，故 k <= (sum+b)/n，取其上界 +1 作二分上界（必不可行）
    ll lo = 0, hi = (sum + b) / n + 1;
    while (hi - lo > 1) {
        ll mid = (lo + hi) / 2;
        if (check(mid))
            lo = mid;
        else
            hi = mid;
    }
    printf("%lld\n", lo);
    return 0;
}
