#include <bits/stdc++.h>
using namespace std;
const int mod = 1000000007;
int a[2000010], n;
int sta[2000010], top, dp[2000010], sum[2000010], sumsta[2000010];

inline int Mod(int x) {
	if (x >= mod)
		return x - mod;
	return x;
}

int main() {
	freopen("perm.in", "r", stdin);
	freopen("perm.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		scanf("%d", a + i);
	dp[0] = 1;
	for (int i = 1; i <= n; i++) {
		while (top && a[sta[top]] > a[i])
			top--;
		dp[i] = ((top == 0 ? 1ll : 0ll) + sumsta[top] + sum[i - 1] + mod - sum[sta[top]]) % mod;
		sta[++top] = i;
		sumsta[top] = Mod(sumsta[top - 1] + dp[i]);
		sum[i] = Mod(sum[i - 1] + dp[i]);
	}
	cout << sumsta[top] << endl;
}