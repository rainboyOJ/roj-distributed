// 信息学奥赛一本通 1675《塔》 标程 (C++17)
//
// 参考来源（思路二：贪心 + 线性 DP，按题面改写实现）：
//   https://blog.csdn.net/qq_43857314/article/details/110644689
//   《【信息学奥赛一本通——高手训练】塔 | 贪心、线性dp、思维》
// 交叉验证参考（O(n^3) 区间 DP 写法）：
//   https://www.cnblogs.com/gryzy/p/18627435
//
// 题意：每次可合并相邻两座塔（高度叠加），求使最终塔列高度不降的最少操作次数。
//
// 关键观察：一系列合并操作等价于把原序列划分成若干连续段，
//   每段之和成为一座新塔；操作次数 = N - 段数。
//   要求段和从左到右不降，求最少操作次数即求最大段数。
//
// 贪心 DP：记 sum[] 为前缀和，
//   dp[i] = 前 i 座塔合法划分（段和不降）时，最后一段和的最小值。
//   dp[i] = min{ sum[i]-sum[j] | 0<=j<i 且 sum[i]-sum[j] >= dp[j] }，dp[0]=0。
//   贪心正确性：末段和取得最小不会使答案变劣——末段更小，只可能让整体
//   分出更多的段（这是 POI「Wieże / Towers」的经典贪心结论）。
// 回溯：从 n 出发沿取得 dp 值的转移点 j 跳回 0，统计段数 k，答案 = n - k。
//
// 复杂度 O(n^2)，n<=3000，最大约 9e6 次比较，远低于 1s 时限。
#include <cstdio>
#include <algorithm>
using namespace std;

const int MAXN = 3005;
const long long INF = (long long)4e18;

int n;
long long sum[MAXN];  // 前缀和，最大 3000*3000=9e6，int 亦可，long long 保险
long long dp[MAXN];   // dp[i]: 前 i 座塔合法划分时最后一段和的最小值
int pre[MAXN];        // 转移来源，用于回溯统计段数

int main() {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        long long a;
        scanf("%lld", &a);
        sum[i] = sum[i - 1] + a;
    }
    dp[0] = 0;
    pre[0] = -1;
    for (int i = 1; i <= n; i++) {
        dp[i] = INF;
        pre[i] = 0;  // j=0 恒合法（sum[i] >= dp[0] = 0），保证有解
        for (int j = 0; j < i; j++) {
            long long seg = sum[i] - sum[j];
            if (seg >= dp[j] && seg < dp[i]) {
                dp[i] = seg;
                pre[i] = j;
            }
        }
    }
    int k = 0;  // 段数
    for (int i = n; i > 0; i = pre[i]) k++;
    printf("%d\n", n - k);
    return 0;
}
