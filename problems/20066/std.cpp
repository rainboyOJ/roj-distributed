#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int N = 1e5 + 5;

int n, k, q;
char s[N];
ll a[N];

int main()
{
	scanf("%d%d%d%s", &n, &k, &q, s + 1);
	for (int i = 1; i <= q; i++) scanf("%lld", &a[i]);
	int L = 0, R = 0;
	for (int i = 1; i <= n; i++) L += (s[i] == '1');
	R = L + n;
	for (int i = 1; i <= q; i++) {
		ll x = a[i];
		if (x % k) puts("No");
		else {
			x /= k;
			if (L <= x && x <= R) puts("Yes");
			else puts("No");
		}
	}
	return 0;
}
