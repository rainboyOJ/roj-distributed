#include <iostream>
#include <cstdio>
#include <string.h>
#include <algorithm>
#define ll long long
using namespace std;
ll a[1000010];

int main() {
	freopen("tournament.in", "r", stdin);
	freopen("tournament.out", "w", stdout);
	ll n, k;
	int ans = 1;
	scanf("%lld%lld", &n, &k);
	for (int i = 0; i < n; i++) {
		scanf("%lld", &a[i]);
	}
	sort(a, a + n);
	for (int i = n - 1; i > 0; i--) {
		if ((a[i] - a[i - 1]) > k)
			break;
		ans++;
	}
	printf("%d\n", ans);
}
