#include <bits/stdc++.h>
const int maxn = 1000010;
int a[maxn];

int main() {
	freopen("division.in", "r", stdin);
	freopen("division.out", "w", stdout);
	int n;
	scanf("%d", &n);
	for (int i = 1; i <= n; i++)
		scanf("%d", &a[i]);
	long long sum = 0;
	int cnt = 0;
	for (int i = n; i >= 1; i--) {
		sum += a[i];
		if (sum >= 0) {
			sum = 0;
			cnt++;
		}
	}
	if (sum < 0)
		cnt = -1;
	printf("%d\n", cnt);
	return 0;
}