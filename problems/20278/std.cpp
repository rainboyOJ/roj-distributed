#include <iostream>
#include <cmath>
#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;
int dp[1 << 20], x[22], n, two[1 << 20], w[22];
const int mo = 1e9 + 7;

int main() {
	freopen("perm.in", "r", stdin);
	freopen("perm.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		scanf("%d", &x[i]), x[i] = n - x[i] + 1;
	for (int i = 1; i <= n; i++)
		w[i] = w[i - 1] + (1 << x[i] - 1);
	dp[0] = 1;
	for (int i = 0; i < (1 << n); i++)
		two[i] = two[i >> 1] + (i & 1);
	for (int i = 0; i < (1 << n); i++) {
		int flag = 0, N = two[i];
		for (int j = 1; j <= n; j++) {
			if (two[w[N] & ((1 << j) - 1)] < two[i & ((1 << j) - 1)])
				flag = 1;
		}
		if (flag)
			continue;
		for (int j = 1; j <= n; j++)
			if ((i & (1 << j - 1)) == 0)
				dp[i + (1 << j - 1)] = (dp[i + (1 << j - 1)] + dp[i]) % mo;
	}
	printf("%d\n", dp[(1 << n) - 1]);
	return 0;
}