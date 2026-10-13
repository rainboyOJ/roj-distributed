#include <bits/stdc++.h>
using namespace std;
#define int long long
const int MAXN = 2e3 + 50;
const int Mod = 998244353;
int n;
int f[MAXN][MAXN << 1], ans = 0, inv[MAXN * 2];

int Pow(int x, int y) {
	int z = 1;
	while (y) {
		if (y & 1)
			z = z * x % Mod;
		x = x * x % Mod;
		y >>= 1;
	}
	return z;
}

signed main() {
	freopen("eat.in", "r", stdin);
	freopen("eat.out", "w", stdout);
	cin >> n;
	f[n][0] = 1;
	for (int i = 1 ; i <= 4001 ; i ++)
		inv[i] = Pow(i, Mod - 2);
	for (int i = n - 1 ; i >= 0 ; i --) {
		for (int j = (n - i) * 2 ; j >= (i != 0 ? 0 : 2) ; j --) {
			if (i == 0) {
				f[i][j] = (i + 1) * inv[i + j - 1] % Mod * f[i + 1][j - 2] % Mod;
				continue;
			}
			if (j >= 2 && j < (n - i) * 2)
				f[i][j] = ((i + 1) * inv[i + j - 1] % Mod * f[i + 1][j - 2] % Mod + (j + 1) * inv[i + j + 1] % Mod * f[i][j + 1] % Mod)
				          % Mod;
			if (j < 2)
				f[i][j] = (j + 1) * inv[i + j + 1] % Mod * f[i][j + 1] % Mod;
			if (j == (n - i) * 2)
				f[i][j] = (i + 1) * inv[i + j - 1] % Mod * f[i + 1][j - 2] % Mod;
		}
	}
	for (int i = 1 ; i <= 2 * n ; i ++)
		ans += (3 * n - i) * f[0][i] % Mod, ans %= Mod;
	printf("%lld\n", ans);
	//cout << ans;
	return 0;
}