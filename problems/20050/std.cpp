#include <iostream>
#include <cstdio>
#include <vector>
#include <map>
using namespace std;
const int N = 100005;
int n, a[N], b[N], x, cnt, anss, ans;
map<int, int> mp;
int vis[N];
vector<int> g[N];
void dfs(int u) {
    vis[u] = 1;
    for (int v : g[u])
        if (!vis[v])
            dfs(v);
}
signed main() {
    freopen("xor.in", "r", stdin);
    freopen("xor.out", "w", stdout);
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
        mp[a[i]]++;
        x ^= a[i];
    }
    for (int i = 1; i <= n; i++) {
        scanf("%d", &b[i]);
        mp[b[i]]--;
    }
    mp[x]++;
    for (auto p : mp)
        if (p.second < 0)
            return puts("-1"), 0;
    for (auto &p : mp) p.second = ++cnt;
    for (int i = 1; i <= n; i++)
        if (a[i] != b[i]) {
            int u = mp[b[i]], v = mp[a[i]];
            g[u].push_back(v);
            g[v].push_back(u);
            anss++;
        }
    for (int i = 1; i <= cnt; i++)
        if (!g[i].empty())
            if (!vis[i])
                ans++, dfs(i);
    if (!g[mp[x]].empty())
        ans--;
    printf("%d\n", anss + ans);
}
