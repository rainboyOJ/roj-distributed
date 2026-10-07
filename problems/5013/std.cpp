// 一本通 1677 软件开发
// 参考来源：https://blog.csdn.net/qq_43857314/article/details/112759191
//           【信息学奥赛一本通——高手训练】软件开发 | 二分、dp
// 思路：二分答案天数 x。判定：dp[i][j] 表示前 i 个技术人员恰好完成软件1
//       的 j 个模块时，软件2 最多能完成的模块数；dp[n][m] >= m 则可交付。
// 对来源代码的修改：
//   1) 来源把 a/b 开成 1e7+700 的全局 int 数组（约 80MB，占内存上限 128MB
//      的大半，完全没必要），本实现按题面 n<=100 开 105。
//   2) 二分右界按题面上界收紧为 m*max(d1,d2) <= 10000。
// 数据范围：1<=n,m<=100，1<=d1,d2<=100；时间复杂度 O(n*m*log) 级别，远小于 1s。
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

int n, m;
int a[105], b[105];
int dp[105][105];

bool judge(int x) {
    memset(dp, -1, sizeof(dp));
    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= m; j++) dp[i][j] = dp[i - 1][j]; // 第 i 人不干活
        for (int k = 0; (long long)k * a[i] <= x && k <= m; k++) {
            // 第 i 人用 k*a[i] 天做软件1 的 k 个模块，余下时间做软件2
            int op = (x - k * a[i]) / b[i];
            for (int j = k; j <= m; j++) {
                if (dp[i - 1][j - k] >= 0)
                    dp[i][j] = max(dp[i][j], dp[i - 1][j - k] + op);
            }
        }
    }
    return dp[n][m] >= m;
}

int main() {
    scanf("%d %d", &n, &m);
    int hi = 0;
    for (int i = 1; i <= n; i++) {
        scanf("%d %d", &a[i], &b[i]);
        hi = max(hi, max(a[i], b[i]));
    }
    // 上界：让任意一人单独做完两个软件的所有模块
    int l = 1, r = 2 * m * hi, ans = r;
    while (l <= r) {
        int mid = (l + r) / 2;
        if (judge(mid)) { ans = mid; r = mid - 1; }
        else l = mid + 1;
    }
    printf("%d\n", ans);
    return 0;
}
