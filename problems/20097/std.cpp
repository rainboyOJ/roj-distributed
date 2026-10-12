#include <bits/stdc++.h>
using namespace std;

const int mod = 9901;
int n, k, dp[205][105];

int main() {
	ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
	cin >> n >> k;
	for (int j = 1; j <= k; j++) dp[1][j] = 1;
	for (int j = 1; j <= k; j++)
		for (int i = 3; i <= n; i += 2)
			for (int t = 1; t <= i - 1; t += 2)
				dp[i][j] = (dp[i][j] + dp[t][j - 1] * dp[i - t - 1][j - 1] % mod) % mod;
	cout << (dp[n][k] - dp[n][k - 1] + mod) % mod << endl;
	return 0;
}