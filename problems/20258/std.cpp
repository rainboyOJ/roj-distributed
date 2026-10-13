#include <cstdio>
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <vector>
#include <queue>
#include <map>
#include <set>
#include <ctime>
using namespace std;
typedef long long ll;
#define maxn 1005
#define mod 1000000007
int T, n, m, row[maxn], col[maxn], nr, nc, flag;
char s[maxn];

void inc(int &a, int b) {
	a = a + b >= mod ? a + b - mod : a + b;
}

void dec(int &a, int b) {
	a = a - b < 0 ? a - b + mod : a - b;
}

int mod_pow(int a, int b) {
	int ans = 1;
	while (b) {
		if (b & 1)
			ans = (ll)ans * a % mod;
		a = (ll)a * a % mod;
		b >>= 1;
	}
	return ans;
}

int main() {
	freopen("color.in", "r", stdin);
	freopen("color.out", "w", stdout);
	scanf("%d%d", &n, &m);
	nr = n, nc = m, flag = 0;
	for (int i = 1; i <= n; i++)
		row[i] = 0;
	for (int i = 1; i <= m; i++)
		col[i] = 0;
	for (int i = 1; i <= n; i++) {
		scanf("%s", s + 1);
		for (int j = 1; j <= m; j++)
			if (s[j] != '?' && !(nr == -1 && nc == -1)) {
				int type;
				if (s[j] == 'R')
					type = 1;
				else
					type = 2;
				if ((i + j) & 1)
					type = 3 - type;
				if (row[i] == 3 - type)
					nr = -1;
				else if (!row[i])
					nr--, row[i] = type;
				if (col[j] == 3 - type)
					nc = -1;
				else if (!col[j])
					nc--, col[j] = type;
				if (flag != -1)
					if (flag == 3 - type)
						flag = -1;
					else
						flag = type;
			}
	}
	int ans = 0;
	if (nr >= 0)
		inc(ans, mod_pow(2, nr));
	if (nc >= 0)
		inc(ans, mod_pow(2, nc));
	if (flag != -1) {
		if (flag == 0)
			dec(ans, 2);
		else
			dec(ans, 1);
	}
	printf("%lld\n", ans);
	return 0;
}
