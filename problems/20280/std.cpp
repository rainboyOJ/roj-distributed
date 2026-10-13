#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const int N = 100000 + 5;
const int INF = 1e8;

vector<int> G[N];

int dp[N][3];
int n;

void dfs(int u, int fa) {
	int tmp = 0;
	for (int i = 0; i < G[u].size(); i++) {
		int v = G[u][i];
		if (v == fa)
			continue;
		dfs(v, u);
		if (tmp >= INF)
			continue;
		tmp += dp[v][1];
	}
	dp[u][0] = min(INF, tmp + 1);
	dp[u][1] = dp[u][2] = 0;
	for (int i = 0; i < G[u].size(); i++) {
		int v = G[u][i];
		if (v == fa)
			continue;
		int tmp[3];
		tmp[1] = tmp[2] = INF;
		tmp[1] = min(tmp[1], dp[u][1] + dp[v][0]);
		tmp[2] = min(tmp[2], dp[u][1] + dp[v][1]);
		tmp[2] = min(tmp[2], dp[u][1] + dp[v][2]);
		tmp[2] = min(tmp[2], dp[u][2] + dp[v][0]);
		tmp[1] = min(tmp[1], dp[u][2] + dp[v][1] + 1);
		tmp[1] = min(tmp[1], dp[u][2] + dp[v][2] + 1);
		dp[u][1] = tmp[1];
		dp[u][2] = tmp[2];
	}
	dp[u][2] = min(dp[u][2], dp[u][1]);
}

int main() {
	freopen("cover.in", "r", stdin);
	freopen("cover.out", "w", stdout);
	scanf("%d", &n);
	int u, v;
	for (int i = 0; i < n - 1; i++) {
		scanf("%d%d", &u, &v);
		u--;
		v--;
		G[u].push_back(v);
		G[v].push_back(u);
	}
	dfs(0, -1);
	printf("%d\n", min(dp[0][0], dp[0][1]));
	return 0;
}
