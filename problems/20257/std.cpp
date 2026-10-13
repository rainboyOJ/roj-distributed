#include <bits/stdc++.h>
#define LL long long
#define LD long double
#define ull unsigned long long
#define fi first
#define se second
#define mk make_pair
#define PLL pair<LL, LL>
#define PLI pair<LL, int>
#define PII pair<int, int>
#define SZ(x) ((int)x.size())
#define ALL(x) (x).begin(), (x).end()
#define fio ios::sync_with_stdio(false); cin.tie(0);

using namespace std;

const int N = 500 + 7;
const int inf = 0x3f3f3f3f;
const LL INF = 0x3f3f3f3f3f3f3f3f;
const int mod = 1e9 + 7;
const double eps = 1e-8;
const double PI = acos(-1);

template<class T, class S> inline void add(T &a, S b) {
	a += b;
	if (a >= mod)
		a -= mod;
}

template<class T, class S> inline void sub(T &a, S b) {
	a -= b;
	if (a < 0)
		a += mod;
}

template<class T, class S> inline bool chkmax(T &a, S b) {
	return a < b ? a = b, true : false;
}

template<class T, class S> inline bool chkmin(T &a, S b) {
	return a > b ? a = b, true : false;
}

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

int n, k, state[N];
int who[N];

vector<int> sml, big[N];

int prime[] = {2, 3, 5, 7, 11, 13, 17, 19};

void init() {
	for (int i = 2; i <= 500; i++) {
		bool flag = true;
		int x = i;
		for (int j = 2; j * j <= x; j++) {
			if (x % (j * j) == 0) {
				flag = false;
				break;
			}
		}
		if (!flag) {
			state[i] = -1;
			continue;
		}
		for (int j = 0; j < 8; j++) {
			if (x % prime[j] == 0) {
				state[i] |= 1 << j;
				x /= prime[j];
			}
		}
		if (x > 1)
			who[i] = x;
	}
}

int dp[2][501][1 << 8];
int (*f)[1 << 8] = dp[0];
int (*g)[1 << 8] = dp[1];

int main() {
	freopen("square.in", "r", stdin);
	freopen("square.out", "w", stdout);
	init();
	scanf("%d%d", &n, &k);
	sml.clear();
	for (int i = 1; i <= n; i++) {
		big[i].clear();
	}
	for (int i = 1; i <= n; i++) {
		if (state[i] == -1) {
			continue;
		} else if (who[i] == 0) {
			sml.push_back(i);
		} else {
			big[who[i]].push_back(i);
		}
	}

	for (int l = 0; l <= k; l++) {
		for (int mask = 0; mask < (1 << 8); mask++) {
			f[l][mask] = 0;
		}
	}

	f[0][0] = 1;

	for (auto v : sml) {
		swap(f, g);
		for (int l = 0; l <= k; l++) {
			for (int mask = 0; mask < (1 << 8); mask++) {
				f[l][mask] = 0;
			}
		}
		for (int l = 0; l <= k; l++) {
			for (int mask = 0; mask < (1 << 8); mask++) {
				add(f[l][mask], g[l][mask]);
				if (mask & state[v])
					continue;
				add(f[l + 1][mask | state[v]], g[l][mask]);
			}
		}
	}

	for (int i = 1; i <= n; i++) {
		if (!SZ(big[i]))
			continue;
		swap(f, g);
		for (int l = 0; l <= k; l++) {
			for (int mask = 0; mask < (1 << 8); mask++) {
				f[l][mask] = 0;
			}
		}
		for (int l = 0; l <= k; l++) {
			for (int mask = 0; mask < (1 << 8); mask++) {
				if (!g[l][mask])
					continue;
				add(f[l][mask], g[l][mask]);
				for (auto v : big[i]) {
					if (mask & state[v])
						continue;
					add(f[l + 1][mask | state[v]], g[l][mask]);
				}
			}
		}
	}

	int ans = 0;
	for (int l = 1; l <= k; l++) {
		for (int mask = 0; mask < (1 << 8); mask++) {
			add(ans, f[l][mask]);
		}
	}
	printf("%d\n", ans);
	return 0;
}
