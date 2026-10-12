#include <bits/stdc++.h>

using namespace std;

#define pb push_back

typedef vector<int> vi;

const int N = 1e5 + 5;

int n, m;
int a[N];
vi g[N];
int up[N], dw[N];

int dfs(int x, int w) {
	w ^= dw[x];
	int res = up[x];
	for (auto y : g[x]) res ^= dfs(y, w);
	a[x] ^= w;
	a[x] ^= res;
	return res;
}

int main()
{
	scanf("%d%d", &n, &m);
	for (int i = 2, fa; i <= n; i++) scanf("%d", &fa), g[fa].pb(i);
	for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
	for (int i = 1, o, x, v; i <= m; i++) {
		scanf("%d%d%d", &o, &x, &v);
		if (o == 1) dw[x] ^= v;
		else up[x] ^= v;
	}
	dfs(1, 0);
	for (int i = 1; i <= n; i++) printf("%d ", a[i]);
	return 0;
} 
