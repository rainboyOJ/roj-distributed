// 一本通 1679 子集（Codeforces 626E Simple Skewness 改版：只输出最大价值）
// 参考来源：
//   https://blog.csdn.net/qingfeixueyue/article/details/123188473 （一本通 1679 题解，降序实现）
//   https://blog.csdn.net/qq_34374664/article/details/77747269 （CF 626E 题解，思路转自 cnblogs.com/flipped/p/5211693.html）
// 思路：
//   1. 单元素子集价值为 0，故答案 >= 0。
//   2. 最优子集大小必为奇数 2k+1（偶数大小去掉排序后第 k+1 个元素不会更差）。
//   3. 升序排序后枚举中位数 a[i]，向左侧取紧邻的 k 个、向右侧取最大的 k 个，
//      平均值关于 k 先增后减（单峰），三分 k 求峰。
// 对网络代码的修复：
//   - 来源代码用浮点数计算并三分，存在精度风险；改为全程整数比较
//     （比较 S/(2k+1) 改为交叉相乘 S*(2k'+1) vs S'*(2k+1)，最大约 4e16，long long 安全）。
//   - 答案与 0 取 max 后按题面要求保留 5 位小数输出。
#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;
const int MAXN = 200000 + 5;

int n;
ll a[MAXN], sum[MAXN];

// 以位置 i 为中位数、左右各取 k 个时的子集元素和
static inline ll calc(int i, int k) {
    // 左侧：a[i-k..i]（升序，紧邻中位数更大）；右侧：a[n-k+1..n]（最大的 k 个）
    return (sum[i] - sum[i - k - 1]) + (sum[n] - sum[n - k]);
}

int main() {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) scanf("%lld", &a[i]);
    sort(a + 1, a + n + 1);
    for (int i = 1; i <= n; i++) sum[i] = sum[i - 1] + a[i];

    ll bestNum = 0, bestDen = 1; // 最大价值 bestNum/bestDen（>=0，单元素价值为 0）
    for (int i = 2; i <= n - 1; i++) {
        int lo = 0, hi = min(i - 1, n - i);
        while (lo <= hi) { // 整数三分：平均值 S(k)/(2k+1) 关于 k 单峰
            int m1 = lo + (hi - lo) / 3;
            int m2 = hi - (hi - lo) / 3;
            ll s1 = calc(i, m1), s2 = calc(i, m2);
            if (s1 * (2LL * m2 + 1) < s2 * (2LL * m1 + 1)) lo = m1 + 1;
            else hi = m2 - 1;
        }
        int k = lo;
        ll s = calc(i, k);                 // 子集和，大小 2k+1
        ll num = s - (2LL * k + 1) * a[i]; // 价值 = (s - (2k+1)*median) / (2k+1)
        if (num * bestDen > bestNum * (2LL * k + 1)) {
            bestNum = num;
            bestDen = 2LL * k + 1;
        }
    }
    printf("%.5f\n", (double)bestNum / (double)bestDen);
    return 0;
}
