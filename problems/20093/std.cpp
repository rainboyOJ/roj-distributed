#include <bits/stdc++.h>
#define int long long
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

const int N = 200005;
int n, m, sum;
int a[N], s[N], vis[N], t[N];
vector<int> g[N];

bool check(int mid)
{
    queue<int> q;
    memset(vis, 0, sizeof(vis));
    for (int i = 1; i <= n; i++)
    {
        t[i] = s[i];
        if (s[i] <= mid)
        {
            q.push(i);
            vis[i] = 1;
        }
    }

    while (!q.empty())
    {
        int u = q.front();
        q.pop();
        for (int i = 0; i < (int)g[u].size(); i++)
        {
            int v = g[u][i];
            t[v] -= a[u];
            if (t[v] <= mid && vis[v] == 0)
            {
                vis[v] = 1;
                q.push(v);
            }
        }
    }

    for (int i = 1; i <= n; i++)
    {
        if (vis[i] == 0) return false;
    }
    return true;
}

signed main()
{
    // freopen("T3.in", "r", stdin);
    // freopen("T3.out", "w", stdout);
    n = rd;
    m = rd;
    for (int i = 1; i <= n; i++)
    {
        a[i] = rd;
    }

    for (int i = 1; i <= m; i++)
    {
        int u = rd;
        int v = rd;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    for (int i = 1; i <= n; i++)
    {
        for (int j = 0; j < (int)g[i].size(); j++)
        {
            s[i] += a[g[i][j]];
        }
    }

    int l = 0, r = 1e18;
    while (l < r)
    {
        int mid = (l + r) >> 1;
        if (check(mid)) r = mid;
        else l = mid + 1;
    }

    printf("%lld", r);
    return 0;
}