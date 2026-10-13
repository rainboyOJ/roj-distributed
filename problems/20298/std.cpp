#pragma GCC optimize("Ofast,unroll-loops")
#pragma GCC target("avx,avx2,sse,sse2")
#include <bits/stdc++.h>
using namespace std;
#define N 3009
int n, m, ans, pos[N][N], num[N][N], c[N];
char a[N][N];

int main() {
	freopen("rectangle.in", "r", stdin);
	freopen("rectangle.out", "w", stdout);
	scanf("%d%d", &n, &m);
	for (int i = 1; i <= n; i++)
		scanf("%s", a[i] + 1);
	for (int j = 1; j <= m; j++) {
		pos[j][n + 1] = n;
		for (int i = n; i >= 1; i--) {
			if (a[i][j] == '0')
				pos[j][i] = pos[j][i + 1];
			else
				pos[j][i] = i - 1;
			++num[i][pos[j][i]];
		}
	}
	for (int i = 1; i <= n; i++) {
		int cnt = 0;
		for (int j = n; j >= i; j--) {
			cnt += num[i][j];
			int sum = cnt * (j - i + 1);
			ans = max(ans, sum);
		}
	}
	printf("%d\n", ans);
	return 0;
}