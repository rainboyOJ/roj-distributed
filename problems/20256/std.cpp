#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cmath>
#include <iostream>
#include <algorithm>
using namespace std;
typedef long long ll;
const int MAXN = 505;
const ll Mod = 1000000007LL;
ll a[MAXN], f[MAXN], inv[MAXN];
char s[MAXN];
ll dp[MAXN][MAXN];

void build() {
	f[0] = 1LL;
	for (int i = 1; i <= 500; i++)
		f[i] = i * f[i - 1] % Mod;
}

ll fp(ll a, ll k) {
	ll res = 1LL;
	while (k > 0) {
		if (k & 1)
			res = res * a % Mod;
		a = a * a % Mod;
		k >>= 1;
	}
	return res;
}

int main() {
	freopen("expression.in", "r", stdin);
	freopen("expression.out", "w", stdout);
	build();
	int n;
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		scanf("%lld", &a[i]), inv[i] = fp(i, Mod - 2);
	scanf("%s", s + 1);
	memset(dp, 0, sizeof(dp));
	for (int i = 1; i <= n; i++)
		dp[i][i] = a[i];
	for (int len = 1; len < n; len++) {
		for (int i = 1; i + len <= n; i++) {
			int j = i + len;
			for (int k = i; k < j; k++) {
				if (s[k] == '+')
					dp[i][j] = (dp[i][j] + dp[i][k] + dp[k + 1][j]) % Mod;
				else if (s[k] == '-')
					dp[i][j] = (dp[i][j] + dp[i][k] - dp[k + 1][j]) % Mod;
				else
					dp[i][j] = (dp[i][j] + dp[i][k] * dp[k + 1][j] % Mod) % Mod;
			}
			dp[i][j] = dp[i][j] * inv[len] % Mod;
		}
	}
	ll ans = ((dp[1][n] * f[n - 1] % Mod) + Mod) % Mod;
	printf("%lld\n", ans);
	return 0;
}