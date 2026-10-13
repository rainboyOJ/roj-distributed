#include <bits/stdc++.h>

using namespace std;

const int maxn = 1000005, mo = 998244353;

int fac[maxn], rfac[maxn], n;

int pow(int a, int b) {
	int tmp = 1;
	for (; b; b >>= 1, a = a * 1ll * a % mo)
		if (b & 1)
			tmp = tmp * 1ll * a % mo;
	return tmp;
}

int get_c(int n, int m) {
	return fac[n] * 1ll * rfac[n - m] % mo * rfac[m] % mo;
}

int main() {
	freopen("variance.in", "r", stdin);
	freopen("variance.out", "w", stdout);
	cin >> n;
	int ans = 2 * (n - 1) * 1ll * pow(n, mo - 2) % mo;
	ans = ans * 1ll * ans % mo;
	ans = ans * 1ll * pow(n, n - 2) % mo;
	ans = (mo - ans) % mo;
	fac[0] = 1;
	for (int i = 1; i <= n; i ++)
		fac[i] = fac[i - 1] * 1ll * i % mo;
	rfac[n] = pow(fac[n], mo - 2);
	for (int i = n; i; i --)
		rfac[i - 1] = rfac[i] * 1ll * i % mo;
	static int pw[maxn];
	pw[0] = 1;
	for (int i = 1; i <= n; i ++)
		pw[i] = pw[i - 1] * 1ll * (n - 1) % mo;
	for (int d = 0; d < n - 1; d ++) {
		int sqr = (d + 1) * 1ll * (d + 1) % mo;
		ans = (ans + get_c(n - 2, d) * 1ll * sqr % mo * pw[n - 2 - d] % mo) % mo;
	}
	printf("%d\n", ans);
	return 0;
}
