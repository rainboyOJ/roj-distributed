#include <bits/stdc++.h>

using namespace std;

const int mod = 1000000007;

char s[30][100];

int len[30];

long long pw[1005];

int vs[30];

int main() {
	freopen("trie.in", "r", stdin);
	freopen("trie.out", "w", stdout);
	pw[0] = 1;
	for (int i = 1; i <= 1000; ++i)
		pw[i] = pw[i - 1] * 2 % mod;
	int n;
	scanf("%d", &n);
	int sumk = 0;
	for (int i = 0; i < n; ++i) {
		scanf("%s", s[i]);
		len[i] = strlen(s[i]);
		for (int j = 0; j < len[i]; ++j)
			if (s[i][j] == '?')
				++sumk;
	}
	int sum = 1;
	for (int i = 0; i < n; ++i)
		sum += len[i];
	long long ans = 1ll * sum * pw[sumk] % mod;
	for (int i = 1; i < 1 << n; ++i) {
		int tot = 0;
		for (int j = 0; j < n; ++j)
			if (i >> j & 1)
				vs[tot++] = j;
		if (tot <= 1)
			continue;
		int minl = 1 << 30;
		for (int j = 0; j < tot; ++j)
			minl = min(minl, len[vs[j]]);
		int totq = sumk;
		for (int j = 0; j < minl; ++j) {
			int num = 0, chac = -1;
			for (int k = 0; k < tot; ++k) {
				if (s[vs[k]][j] == '?')
					++num;
				else if (chac == -1)
					chac = s[vs[k]][j];
				else if (chac != s[vs[k]][j]) {
					chac = -2;
					break;
				}
			}
			if (chac == -2)
				break;
			if (chac == -1) {
				totq -= num - 1;
			} else {
				totq -= num;
			}
			long long v = pw[totq];
			if (tot % 2 == 0)
				v = mod - v;
			ans += v;
			if (ans >= mod)
				ans -= mod;
		}
	}
	cout << ans << endl;
	return 0;
}
