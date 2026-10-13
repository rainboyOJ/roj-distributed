#include <cstdio>
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
#define mod 1000000007
#define maxn 5555
int n, a[maxn], h[maxn], pre[maxn][maxn], nxt[maxn][maxn];
typedef pair<int, int>P;
P dp[maxn][maxn];

int main() {
	freopen("palindrome.in", "r", stdin);
	freopen("palindrome.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		scanf("%d", &a[i]), h[i] = a[i];
	sort(h + 1, h + n + 1);
	int cnt = unique(h + 1, h + n + 1) - (h + 1);
	for (int i = 1; i <= n; i++)
		a[i] = lower_bound(h + 1, h + cnt + 1, a[i]) - h;
	memset(pre, -1, sizeof(pre));
	memset(nxt, -1, sizeof(nxt));
	for (int i = 0; i <= n + 1; i++) {
		for (int j = i + 1; j <= n; j++)
			if (nxt[i][a[j]] == -1)
				nxt[i][a[j]] = j;
		for (int j = i - 1; j >= 1; j--)
			if (pre[i][a[j]] == -1)
				pre[i][a[j]] = j;
	}
	for (int i = n; i >= 1; i--) {
		dp[i][i] = P(1, 1);
		P ans = P(0, 1);
		for (int j = i + 1; j <= n; j++) {
			dp[i][j] = P(0, 0);
			if (a[i] == a[j])
				dp[i][j] = P(ans.first + 2, ans.second);
			if (a[i] >= a[j]) {
				int ii = nxt[i][a[j]];
				if (ii == -1)
					continue;
				if (dp[ii][j].first > ans.first)
					ans = dp[ii][j];
				else if (dp[ii][j].first == ans.first) {
					int jj = pre[j][a[j]];
					if (jj != -1 && dp[ii][jj].first == dp[ii][j].first)
						ans.second -= dp[ii][jj].second;
					if (ans.second < 0)
						ans.second += mod;
					ans.second = (ans.second + dp[ii][j].second) % mod;
				}
			}
		}
	}
	P ans = P(0, 0);
	for (int i = 1; i <= n; i++) {
		int l = nxt[0][i], r = pre[n + 1][i];
		if (l == -1 || r == -1)
			continue;
		if (dp[l][r].first > ans.first)
			ans = dp[l][r];
		else if (dp[l][r].first == ans.first)
			ans.second = (ans.second + dp[l][r].second) % mod;
	}
	printf("%d %d\n", ans.first, ans.second);
}
