#include <bits/stdc++.h>
#define int long long
#define maxn 200005
using namespace std;

#define il inline
#define rd read()

il int read() {
    int res = 0, f = 1;
    char c = getchar();
    while (c < '0' || c > '9') {
        if (c == '-') f = -1;
        c = getchar();
    }
    while (c >= '0' && c <= '9') {
        res = res * 10 + c - '0';
        c = getchar();
    }
    return res * f;
}

int n, k;
int a[maxn], dp[maxn][50];

signed main() 
{
    // freopen("T4.in", "r", stdin);
    // freopen("T4.out", "w", stdout);
    n = rd;
    k = rd;
    for (int i = 1; i <= n; i++) 
    {
        a[i] = rd;
    }
    memset(dp, 0x3f, sizeof(dp));
    sort(a + 1, a + n + 1);
    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) 
    {
        for (int j = 0; j <= 40; j++) 
        {
            dp[i][j] = dp[i - 1][j] + 1;
            int last = upper_bound(a + 1, a + i + 1, a[i] / 2) - a - 1;
            if (j > 0) 
            {
                dp[i][j] = min(dp[i][j], dp[last][j - 1]);
            }
        }
    }
    for (int i = 0; i <= 40; i++) 
    {
        if (dp[n][i] <= k) 
        {
            printf("%lld %lld", i, dp[n][i]);
            break;
        }
    }
    return 0;
}