#include <cstdio>
#include <algorithm>

using namespace std;

const int mod = 1e9 + 7;

int dp[210][210][210];

inline void update(int &a, int x) {
	a += x;
	if (a >= mod)
		a -= mod;
}

int main() {
	freopen("lnds.in", "r", stdin);
	freopen("lnds.out", "w", stdout);
	int n;
	scanf("%d", &n);
	dp[0][0][0] = 1;
	for (int i = 1; i <= n; ++i) {
		int p;
		scanf("%d", &p);
		for (int j = 0; j <= n; ++j) {
			for (int k = 0; k <= n; ++k) {
				update(dp[i][j + 1][max(k, j + 1)], 1ll * dp[i - 1][j][k] * (1000 - p) % mod);
				update(dp[i][j][k + 1], 1ll * dp[i - 1][j][k] * p % mod);
			}
		}
	}
	int ans = 0;
	for (int i = 0; i <= n; ++i)
		for (int j = 1; j <= n; ++j)
			update(ans, 1ll * j * dp[n][i][j] % mod);
	printf("%d\n", ans);
	return 0;
}
