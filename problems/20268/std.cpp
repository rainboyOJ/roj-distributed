#include <bits/stdc++.h>
#define ll long long
#define mod 1000000007
#define N 110
#define ad(x,y) (x=(x+(y))%mod)
using namespace std;

int n, last, now, a[N], b[N], cnt, c[N], dp[2][N][N][N][2], num[N];
void ins(int t1, int t2, int t3, int t4, int x, int y) {
	if (num[t1] - num[x] <= num[t2] - num[t1])
		ad(dp[now][t1][t3][t4][0], y);
	if (num[x] - num[t4] >= num[t4] - num[t3])
		ad(dp[now][t1][t2][t4][1], y);
}

int main() {
	freopen("convex.in", "r", stdin);
	freopen("convex.out", "w", stdout);
	scanf("%d", &n);
	int i;
	for (i = 1; i <= n; i++)
		scanf("%d", &a[i]);
	sort(a + 1, a + n + 1);
	for (i = 1; i <= n; i++) {
		if (a[i] != a[i - 1] || i == 1)
			num[++cnt] = a[i];
		b[i] = cnt;
		c[cnt]++;
	}
	int x = 1, j, t1, t2, t3;
	for (i = 1; i <= c[1]; i++)
		x = (ll)x * i % mod;
	dp[0][1][1][1][0] = x;
	now = 0;
	//cout<<cnt<<endl;
	//for (i=1; i<=cnt; i++) cout<<i<<' '<<num[i]<<endl;
	for (i = c[1] + 1; i <= n; i++) {
		last = now;
		now ^= 1;
		memset(dp[now], 0, sizeof(dp[now]));
		for (t1 = 1; t1 <= cnt; t1++)
			for (t2 = 1; t2 <= cnt; t2++)
				for (t3 = 1; t3 <= cnt; t3++)
					for (j = 0; j < 2; j++)
						if (dp[last][t1][t2][t3][j]) {
							if (!j)
								ins(b[i - 1], t1, t2, t3, b[i], dp[last][t1][t2][t3][j]);
							else
								ins(t1, t2, t3, b[i - 1], b[i], dp[last][t1][t2][t3][j]);
						}
	}
	int ans = 0;
	for (t1 = 1; t1 <= cnt; t1++)
		for (t2 = 1; t2 <= cnt; t2++)
			for (t3 = 1; t3 <= cnt; t3++)
				for (i = 0; i < 2; i++)
					ad(ans, dp[now][t1][t2][t3][i]);
	printf("%d\n", ans);
	return 0;
}