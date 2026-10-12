#include <bits/stdc++.h>
using namespace std;

#define int long long

int n, m, k, pre[505][505];

void solve() {
	cin >> n >> m >> k;
	string s[505];
	for (int i = 1; i <= n; i++) cin >> s[i], s[i] = " " + s[i];
	for (int i = 0; i <= n; i++)
		for (int j = 0; j <= m; j++) pre[i][j] = 0;
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= m; j++)
			pre[i][j] = pre[i - 1][j] + pre[i][j - 1] - pre[i - 1][j - 1] + (s[i][j] == 'g');
	int res = INT_MAX;
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= m; j++)
			if (s[i][j] == '.') {
				int maxx = min(n, i + k - 1), maxy = min(m, j + k - 1);
				int minx = max(1LL, i - k + 1), miny = max(1LL, j - k + 1);
				int tmp = pre[maxx][maxy] - pre[minx - 1][maxy] - pre[maxx][miny - 1] + pre[minx - 1][miny - 1];
				res = min(res, tmp);
			}
	cout << pre[n][m] - res << "\n";
}

signed main() {
    ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
    int T;
    cin >> T;
    while (T--) solve();
    return 0;
}