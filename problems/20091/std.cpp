#include <bits/stdc++.h>
using namespace std;

#define int long long
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

int n, s;

signed main() {
    // freopen("T1.in", "r", stdin);
    // freopen("T1.out", "w", stdout);
    n = rd;
    s = rd;
    if (n < s) {
        printf("%lld\n", 0LL);
        return 0;
    }
    int ans = 0;
    if (n - s - 9 * 18 > 0) 
    {
        ans += n - s - 9 * 18;
        n = s + 9 * 18;
    }
    for (int i = s; i <= n; i++) 
    {
        int x = i, sum = 0;
        while(x) 
        {
            sum += (x % 10);
            x /= 10;
        }
        if (i - sum >= s) 
        {
            ans ++;
        }
    }
    printf("%lld\n", ans);
    return 0;
}