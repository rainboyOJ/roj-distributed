#include <cassert>
#include <cstring>
#include <bits/stdc++.h>

using namespace std;
//typedef double db;
typedef long long ll;

struct edge {
	int v, next;
} e[4005];
int etot = 0;
int g[2005];
const ll mod = 1000000007;

void ae(int u, int v) {
	e[etot].v = v;
	e[etot].next = g[u];
	g[u] = etot++;
}

ll powmod(ll a, ll b) {
	ll res = 1;
	a %= mod;
	assert(b >= 0);
	for (; b; b >>= 1) {
		if (b & 1)
			res = res * a % mod;
		a = a * a % mod;
	}
	return res;
}

ll p[2005];//rozne

int qu[2005];
int pre[2005], h[2005], upe[2005];
int n, m;
void bfs(int rt) {
	int p = 0, q = 0;
	for (int i = 1; i <= n; i++)
		pre[i] = h[i] = 0;
	qu[q++] = rt;
	while (p != q) {
		int u = qu[p++];
		for (int i = g[u]; ~i; i = e[i].next)
			if (e[i].v != pre[u]) {
				h[e[i].v] = h[u] + 1;
				pre[e[i].v] = u;
				upe[e[i].v] = i >> 1;
				qu[q++] = e[i].v;
			}
	}
}

int main() {
	freopen("color.in", "r", stdin);
	freopen("color.out", "w", stdout);
	memset(g, -1, sizeof(g));
	scanf("%d%d", &n, &m);
	for (int i = 1; i < n; i++) {
		int x, y;
		scanf("%d%d", &x, &y);
		ae(x, y);
		ae(y, x);
	}
	while (m--) {
		int x, d;
		scanf("%d%d", &x, &d);
		bfs(x);
		ll pinv = powmod(d + 1, mod - 2);
		for (int i = 1; i <= n; i++)
			if (h[i] >= 1 && h[i] <= d + 1) {
				p[upe[i]] = (pinv + (h[i] - 1) * pinv % mod * p[upe[i]]) % mod;
			}
	}
	ll su = 1;
	for (int i = 0; i < n - 1; i++)
		su = (su + p[i]) % mod;
	printf("%lld\n", su);
	return 0;
}
