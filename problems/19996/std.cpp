#include <bits/stdc++.h>

#define ll long long
#define mod 998244353
using namespace std;

inline ll rd() {
	char c;
	bool flag = 0;
	while ((c = getchar()) < '0' || c > '9')
		if (c == '-')
			flag = 1;
	ll res = c - '0';
	while ((c = getchar()) >= '0' && c <= '9')
		res = (res << 3) + (res << 1) + c - '0';
	return flag ? -res : res;
}
int n;
ll ans = 1;
int a[110];

inline void add(int x) {
	int it = x - 1;
	if (a[x] >= 5)
		a[it]++;
	a[x] = 0;
	while (it > 1) {
		if (a[it] >= 10)
			a[it - 1] += (a[it] / 10), a[it] %= 10;
		it--;
	}
}

void Solve() {
	n = rd();
	for (int i = 1 ; i <= n ; i++)
		scanf("%1d", &a[i]);
	for (int i = 0 ; i < n ; i++) {
		if (i)
			add(n - i + 1);
		for (int j = 1 ; j <= n ; j++)
			printf("%d", a[j]);
		if (i < n - 1)
			printf(" -> ");
	}
	puts("");
}

int main() {
	int T = rd();
	while (T--)
		Solve();
	return 0;
}