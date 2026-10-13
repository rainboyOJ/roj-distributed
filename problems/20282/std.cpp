#include <bits/stdc++.h>

using namespace std;

const int maxn = 55, maxm = 2505, mo = int(1e9) + 7;

int x[maxm], y[maxm], a[maxn][maxn], w[maxn][maxn], fac[maxm], rfac[maxm], n, K;

int pow(int a, int b) {
	int tmp = 1;
	for (; b; b >>= 1, a = a * 1ll * a % mo)
		if (b & 1)
			tmp = tmp * 1ll * a % mo;
	return tmp;
}

int gauss() {
	int ans = 1;
	for (int i = 1, j = 1; i < n && j < n; j ++) {
		for (int k = i; k < n; k ++)
			if (a[k][j]) {
				swap(a[i], a[k]);
				if (i != k)
					ans = (mo - ans) % mo;
				break;
			}
		if (!a[i][j]) {
			ans = 0;
			return 0;
		}
		int r = pow(a[i][j], mo - 2);
		ans = ans * 1ll * a[i][j] % mo;
		for (int k = i + 1; k < n; k ++)
			if (a[k][j]) {
				int p = a[k][j] * 1ll * r % mo;
				for (int c = j; c < n; c ++)
					a[k][c] = (a[k][c] - 1ll * a[i][c] * p) % mo;
			}
		++ i;
	}
	return (ans + mo) % mo;
}

int main() {
	freopen("spanning.in", "r", stdin);
	freopen("spanning.out", "w", stdout);
	scanf("%d%d", &n, &K);
	for (int i = 1; i <= n; i ++)
		for (int j = 1; j <= n; j ++)
			scanf("%d", &w[i][j]);
	fac[0] = 1;
	for (int i = 1; i <= n * K; i ++)
		fac[i] = fac[i - 1] * 1ll * i % mo;
	rfac[n * K] = pow(fac[n * K], mo - 2);
	for (int i = n * K; i; i --)
		rfac[i - 1] = rfac[i] * 1ll * i % mo;
	for (int i = 0; i <= n * K; i ++) {
		x[i] = i;
		for (int j = 1; j <= n; j ++) {
			for (int k = 1; k <= n; k ++) {
				int v = i * 1ll * w[j][k] % mo;
				a[j][k] = 0;
				for (int p = 0, c = 1; p <= K; p ++) {
					a[j][k] = (a[j][k] + c * 1ll * rfac[p] % mo) % mo;
					c = c * 1ll * v % mo;
				}
			}
			a[j][j] = 0;
			for (int k = 1; k <= n; k ++)
				if (j != k) {
					a[j][j] = (a[j][j] + a[j][k]) % mo;
					a[j][k] = mo - a[j][k];
				}
		}
		y[i] = gauss();
	}
	static int rev[2505];
	static int f[2505], b[2505];
	for (int i = 0; i <= n * K; i ++)
		rev[i] = pow(i, mo - 2);
	b[0] = 1;
	for (int i = 0; i <= n * K; i ++)
		for (int p = i + 1; p >= 0; p --)
			if (p)
				b[p] = (b[p - 1] - 1ll * i * b[p]) % mo;
			else
				b[p] = (-1ll * i * b[p]) % mo;
	for (int i = 0; i <= n * K; i ++) {
		int c = y[i];
		static int cr[2505];
		memset(cr, 0, sizeof cr);
		for (int j = 0; j <= n * K; j ++)
			if (i != j) {
				int p = i - j;
				if (p < 0)
					c = c * 1ll * (mo - rev[-p]) % mo;
				else
					c = c * 1ll * rev[p] % mo;
			}
		memcpy(cr, b, sizeof cr);
		static int ans[2505];
		memset(ans, 0, sizeof ans);
		for (int j = n * K + 1; j; j --)
			if (cr[j])
				ans[j - 1] = cr[j], cr[j - 1] = (cr[j - 1] + i * 1ll * cr[j]) % mo;
		for (int i = 0; i <= n * K; i ++)
			f[i] = (f[i] + 1ll * c * ans[i]) % mo;
	}
	printf("%lld\n", (f[K] * 1ll * fac[K] % mo + mo) % mo);
	return 0;
}
