// 一本通 1727《魔棒》标程（C++17，stdin -> stdout）
// 参考来源（网络题解，按本地 content.md 改写为单组数据并自行编译验证）：
//   CSDN《[二分+DP]魔棒》 https://blog.csdn.net/chouquet/article/details/108240284
//   原文为 T 组数据版本，本地题面为单组（第一行 n hp，第二行 n 个 a[i]）。
//
// 算法：二分答案 cd + O(n^2) DP 可行性检查。
//   f[i][j][k] = 第 i 秒末的最大剩余生命值；j = 魔杖当前能量点数；
//     k = 0 从未释放（此时 j 恒为 i）；1 恰释放过一次；2 释放过至少两次。
//   （k>=1 时 j 恰等于"距上次释放的秒数"，能量按秒累积。）
//   第 i 秒转移，前提 f[i-1][...] > a[i]，即受伤后 hp>0：
//     题面「任何时刻 hp<=0 即死亡」，受伤瞬间 hp<=0 死亡，来不及释放回血。
//     · 不释放：f[i][j][k] <- f[i-1][j-1][k] - a[i]；
//     · 释放：回血 15*j、能量清零。首次释放不受 cd 约束（k=0 -> 1）；
//       之后释放要求 j >= cd（"间隔至少 cd 秒" <=> 释放时能量点数 j>=cd），
//       k=1/2 -> 2。
//   第 n 秒末存在 f[n][j][k] > 0 即可存活。
//   可行性关于 cd 单调不增；cd >= n 时至多释放一次且与 cd 无关，故
//   check(n+1) 成立 <=> "No upper bound."；check(1) 不成立 <=> -1。
//   复杂度 O(n^2 log n)，n<=500 瞬时完成；64 位防溢出。
#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;
static const ll NEG = -(1LL << 60);
static const int MAXN = 505;

static int n;
static ll hp;
static ll a[MAXN];
static ll f[MAXN][MAXN][3];

// 检查施法间隔 cd 能否存活
static bool check(int cd) {
    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= n; j++)
            f[i][j][0] = f[i][j][1] = f[i][j][2] = NEG;
    f[0][0][0] = hp;
    for (int i = 1; i <= n; i++) {
        // k=0：从未释放，能量恒为 i
        if (f[i - 1][i - 1][0] > a[i]) {
            f[i][i][0] = f[i - 1][i - 1][0] - a[i];                 // 不释放
            f[i][0][1] = max(f[i][0][1],
                             f[i - 1][i - 1][0] - a[i] + 15LL * i); // 首次释放
        }
        for (int j = 1; j <= i; j++) {
            if (f[i - 1][j - 1][1] > a[i]) {                        // k=1
                ll v = f[i - 1][j - 1][1] - a[i];
                f[i][j][1] = max(f[i][j][1], v);                    // 不释放
                if (j >= cd) f[i][0][2] = max(f[i][0][2], v + 15LL * j);
            }
            if (f[i - 1][j - 1][2] > a[i]) {                        // k=2
                ll v = f[i - 1][j - 1][2] - a[i];
                f[i][j][2] = max(f[i][j][2], v);
                if (j >= cd) f[i][0][2] = max(f[i][0][2], v + 15LL * j);
            }
        }
    }
    for (int j = 0; j <= n; j++)
        if (f[n][j][0] > 0 || f[n][j][1] > 0 || f[n][j][2] > 0) return true;
    return false;
}

int main() {
    if (scanf("%d %lld", &n, &hp) != 2) return 0;
    for (int i = 1; i <= n; i++) scanf("%lld", &a[i]);
    if (!check(1)) { printf("-1\n"); return 0; }
    if (check(n + 1)) { printf("No upper bound.\n"); return 0; }
    int lo = 1, hi = n, best = 1;   // check(1)=true, check(n+1)=false 时答案在 [1,n]
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (check(mid)) { best = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    printf("%d\n", best);
    return 0;
}
