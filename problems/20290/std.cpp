#include <bits/stdc++.h>
#define rep(i, a, b) for (int i = (a); i <= int(b); i++)
#define per(i, a, b) for (int i = (a); i >= int(b); i--)
using namespace std;

typedef long long ll;
const int maxn = 4e6, mod = 998244353, i00 = 828542813;
int T, n, m, p, q, fact[maxn + 5], finv[maxn + 5], a, b, c;
int pa[maxn + 5], pb[maxn + 5], pc[maxn + 5], f[maxn + 5];

int qpow(int a, int b) {
	int c = 1;
	for (; b; b >>= 1, a = 1ll * a * a % mod)
		if (b & 1)
			c = 1ll * a * c % mod;
	return c;
}

void prework(int n) {
	fact[0] = 1;
	rep(i, 1, n) fact[i] = 1ll * fact[i - 1] * i % mod;
	finv[n] = qpow(fact[n], mod - 2);
	per(i, n, 1) finv[i - 1] = 1ll * finv[i] * i % mod;
}

int bin(int n, int m) {
	return 1ll * fact[n] * finv[m] % mod * finv[n - m] % mod;
}

inline void mad(int &x, int y) {
	x += y, x < mod ? 0 : x -= mod;
}

int main() {
	freopen("game.in", "r", stdin);
	freopen("game.out", "w", stdout);
	scanf("%d %d %d %d", &n, &m, &p, &q);
	prework(n + m);
	p = 1ll * p * i00 % mod;
	q = 1ll * q * i00 % mod;
	a = 1ll * q * (1 - p + mod) % mod;
	b = 1ll * p * (1 - q + mod) % mod;
	c = 1ll * p * q % mod;
	int t = qpow(((ll)a + b + c) % mod, mod - 2);
	a = 1ll * a * t % mod;
	b = 1ll * b * t % mod;
	c = 1ll * c * t % mod;
	n--, m--;
	pa[0] = pb[0] = pc[0] = 1;
	rep(i, 1, max(n, m)) {
		pa[i] = 1ll * pa[i - 1] * a % mod;
		pb[i] = 1ll * pb[i - 1] * b % mod;
		pc[i] = 1ll * pc[i - 1] * c % mod;
	}
	rep(i, 0, n) {
		f[i] = 1ll * bin(m + i, i) * pa[i] % mod;
		if (i > 0)
			mad(f[i], f[i - 1]);
	}
	int res = 0;
	rep(i, 0, min(n, m)) {
		res = (res + 1ll * bin(m, i) * pc[i] % mod * pb[m - i] % mod * f[n - i]) % mod;
	}
	res = 1ll * res * (b + c) % mod;
	printf("%d\n", res);
	return 0;
}