#include <bits/stdc++.h>
using namespace std;
#define int long long
int dp[2005][2005];

signed main() {
	freopen("giant.in", "r", stdin);
	freopen("giant.out", "w", stdout);
	int n, m;
	cin >> n >> m;
	for (int i = 1; i <= n; i++) {
		dp[1][i] = 1;
	}
	int ans = 0;
	for (int i = 1; i <= m; i++) {
		for (int j = 1; j <= n; j++) {
			for (int k = 1; k * j <= n; k++) {
				dp[i + 1][k * j] = (dp[i + 1][k * j] + dp[i][j]) % 1000000007;
			}
			ans += dp[i][j];
			ans %= 1000000007;
		}
	}
	cout << ans << endl;
	return 0;
}