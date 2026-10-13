#include <cassert>
#include <bits/stdc++.h>
using namespace std;
#define rep(i,a,n) for (int i=a;i<n;i++)
#define per(i,a,n) for (int i=n-1;i>=a;i--)
#define pb push_back
#define mp make_pair
#define all(x) (x).begin(),(x).end()
#define fi first
#define se second
#define SZ(x) ((int)(x).size())
typedef vector<int> VI;
typedef long long ll;
typedef pair<int, int> PII;
const ll mod = 1000000007;

ll powmod(ll a, ll b) {
	ll res = 1;
	a %= mod;
	assert(b >= 0);
	for (; b; b >>= 1) {
		if (b & 1)
			res = res * a % mod;
		a = a * a % mod;
	}
	return res;
}

ll gcd(ll a, ll b) {
	return b ? gcd(b, a % b) : a;
}
// head

int _, n, k, val[6], x;
int dp[1234567];
VI pos[3234][6];
vector<VI> key;
void dfs(int u, int f) {
	if (f == k) {
		key.pb(VI(val, val + k));
	} else {
		for (auto p : pos[u][f]) {
			val[f] = p;
			dfs(u, f + 1);
		}
	}
}

int main() {
	freopen("seq.in", "r", stdin);
	freopen("seq.out", "w", stdout);
	scanf("%d%d", &k, &n);
	rep(j, 0, k) {
		rep(i, 1, n + 1) pos[i][j].clear();
		rep(i, 1, n + 1) {
			scanf("%d", &x);
			pos[x][j].pb(i);
		}
	}
	rep(i, 1, n + 1) dfs(i, 0);
	sort(all(key));
	int ans = 0;
	fprintf(stderr, "%d\n", SZ(key));
	rep(i, 0, SZ(key)) {
		dp[i] = 1;
		for (int j = 0; j < i; j++) {
			bool les = 1;
			rep(c, 0, k) les &= (key[j][c] < key[i][c]);
			if (les) {
				dp[i] = (dp[i] + dp[j]) % mod;
			}
		}
		ans = (ans + dp[i]) % mod;
	}
	printf("%d\n", ans);
}
