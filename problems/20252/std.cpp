#include <algorithm>
#include <iostream>
#include <string.h>
#include <stdio.h>
using namespace std;
const int INF = 0x3f3f3f3f;
const int maxn = 200010;
typedef long long ll;
const ll mod = 1e9 + 7;
ll fac[maxn], dp[maxn], inv[maxn], ans;
int cnt, sz[maxn], n;

struct node {
	int v;
	node *next;
} ed[maxn << 1], *head[maxn];

void adde(int u, int v) {
	ed[cnt].v = v;
	ed[cnt].next = head[u];
	head[u] = &ed[cnt++];
}

void dfs(int fa, int u) {
	dp[u] = sz[u] = 1;
	for (node *p = head[u]; p != NULL; p = p->next) {
		int v = p->v;
		if (v == fa)
			continue;
		dfs(u, v);
		dp[u] = (dp[u] * dp[v]) % mod;
		sz[u] += sz[v];
	}
	dp[u] = (dp[u] * inv[sz[u]] % mod) % mod;
}

void solve(int fa, int u, ll tp) {
	ll tt;
	ans = (ans + tp * tp % mod) % mod;
	for (node *p = head[u]; p != NULL; p = p->next) {
		int v = p->v;
		if (v == fa)
			continue;
		tt = (tp * inv[n - sz[v]] % mod * sz[v]) % mod;
		solve(u, v, tt);
	}
}

int main() {
	freopen("message.in", "r", stdin);
	freopen("message.out", "w", stdout);
	int t, i, u, v, rt;

	fac[0] = fac[1] = 1;
	inv[1] = 1;
	for (i = 2; i < maxn; i++) {
		fac[i] = (i * fac[i - 1]) % mod;
		inv[i] = (mod - mod / i) * inv[mod % i] % mod;
	}
	scanf("%d", &n);
	cnt = 0, ans = 0;
	for (i = 1; i <= n; i++)
		head[i] = NULL;
	for (i = 1; i < n; i++) {
		scanf("%d%d", &u, &v);
		adde(u, v);
		adde(v, u);
	}
	rt = (n + 1) / 2;
	dfs(-1, rt);
	solve(-1, rt, dp[rt]*fac[n] % mod);
	printf("%lld\n", ans);
}