#include <iostream>
#include <cmath>
#include <cstring>
#include <cstdio>
#include <algorithm>
using namespace std;
int A[400][400], B[400][400], n, inf = 1e9, x[400], y[400], a[400], C[400][400], where[400], D[400][400], whereB[400],
                                 pd[400];

void dfs(int k) {
	while (pd[k] == 0) {
		pd[k] = 1;
		k = x[k];
	}
}

void dfs2(int k) {
	while (pd[k] == 0) {
		pd[k] = 1;
		k = y[k];
	}
}

int calc() {
	memset(pd, 0x00, sizeof pd);
	int ans = 2 * n;
	for (int i = 1; i <= n; i++)
		if (pd[i] == 0)
			ans--, dfs(i);
	memset(pd, 0x00, sizeof pd);
	for (int i = 1; i <= n; i++)
		if (pd[i] == 0)
			ans--, dfs2(i);
	return ans;
}

int main() {
	freopen("square.in", "r", stdin);
	freopen("square.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			scanf("%d", &A[i][j]);
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			scanf("%d", &B[i][j]);
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			if (B[i][j] == 1)
				whereB[i] = j;
	int ans = inf;
	for (int i = 1; i <= n; i++)
		a[A[1][i]] = i;
	for (int now = 1; now <= n; now++) {
		for (int i = 1; i <= n; i++)
			x[i] = a[B[now][i]];
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				C[i][j] = A[i][x[j]];
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				if (C[i][j] == 1) {
					where[j] = i;
					break;
				}
		for (int i = 1; i <= n; i++)
			y[i] = where[whereB[i]];
		int flag = 0;
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				if (A[y[i]][x[j]] != B[i][j])
					flag = 1;
		if (flag == 0)
			ans = min(ans, calc());
	}
	if (ans >= 3 * n)
		printf("-1\n");
	else
		printf("%d\n", ans);
	return 0;
}