#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

const int N = 5010000;
const int mod = 1e9 + 7;
int n, T;
bool f[N], g[N], preg[N], preg2[N];
char s[N];
int ret[N], ret2[N], cnt[N], cnt2[N];
void work(bool *g, int *ret, int n) {
	for (int i = 1; i <= n; i++)
		ret[i] = 1 << 30;
	int fo = n + 1, lo = -1;
	for (int i = 1; i <= n; i++) {
		if (g[i]) {
			if (fo == n + 1)
				fo = i;
			lo = i;
		}
	}
	if (fo > lo) {
		for (int i = 1; i <= n; i++)
			ret[i] = 0;
		return;
	}
	for (int i = 1; i <= n; i++) {
		preg[i] = preg[i - 1] ^ g[i] ^ 1;
		preg2[i] = preg2[i - 1] ^ g[i];
		cnt[i] = cnt[i - 1] + preg[i];
		cnt2[i] = cnt2[i - 1] + preg2[i];
		//  cout<<i<<" "<<cnt[i]<<endl;
	}
	for (int i = 1; i <= lo; i++) {
		if (i <= fo) {
			int fw = i, lw = lo;
			if (i == lo) {
				ret[i] = min(ret[i], 3);
				continue;
			}
			int ans = lw - fw;
			if (preg[fw - 1])
				ans += 2 * (cnt[lw - 1] - cnt[fw - 1]);
			else
				ans += 2 * (lw - fw - cnt[lw - 1] + cnt[fw - 1]);
			if (preg[lw - 1]^preg[fw - 1] ^ 1)
				ans--;
			ret[i] = min(ret[i], ans);
		} else {
			int fw = fo, lw = lo;
			int ans = i - fo + lw - fw;
			if (preg2[fw - 1])
				ans += 2 * (cnt2[i - 1] - cnt2[fw - 1]);
			else
				ans += 2 * (i - fw - cnt2[i - 1] + cnt2[fw - 1]);

			int x = preg2[i - 1] ^ preg2[fw - 1] ^ 1;
			if (x == preg[i - 1])
				ans += 2 * (cnt[lw - 1] - cnt[i - 1]);
			else
				ans += 2 * (lw - i - cnt[lw - 1] + cnt[i - 1]);
			if (x ^ preg[i - 1]^preg[lw - 1])
				ans--;
			ret[i] = min(ret[i], ans);
		}
	}
}

int main() {
	freopen("light.in", "r", stdin);
	freopen("light.out", "w", stdout);
	scanf("%d", &n);
	scanf("%s", s + 1);
	for (int i = 1; i <= n; i++)
		g[i] = (s[i] == '1');
	work(g, ret, n);
	reverse(g + 1, g + n + 1);
	work(g, ret2, n);
	LL ans = 0;
	for (int i = 1; i <= n; i++) {
		ret[i] = min(ret[i], ret2[n + 1 - i]);
		//fprintf(stderr, "%d\n", ret[i]);
		ans = (ans + (LL)i * ret[i]) % mod;
	}
	printf("%lld\n", ans);
}
