#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <cassert>
#include <bitset>
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
// head

const int N = 1510;
int n, m, f[N][N], sr[N], sc[N];
int a[N], b[N], ret[N], A, B, vis[N];
char s[N];
vector<PII> row[N], col[N];
bitset<N> r[N], c[N];

int Dis(int u) {
	return abs(sr[A] - sr[a[u]]) + abs(sc[B] - sc[b[u]]);
}

int gao() {
	int ret = 0;
	rep(i, 0, n - A + 1) {
		ret += (c[i] & c[i + A - 1] & r[i] & (r[i] >> (B - 1))).count();
	}
	return ret;
}

int main() {
	freopen("rectangle.in", "r", stdin);
	freopen("rectangle.out", "w", stdout);
	scanf("%d%d", &n, &m);
	rep(i, 0, n) {
		scanf("%s", s);
		rep(j, 0, n) f[i][j] = s[j] - '0';
	}
	rep(i, 0, n) {
		int p = 0;
		per(j, 0, n) {
			if (f[i][j] == 1)
				p++;
			else
				p = 0;
			if (p)
				col[p].pb(mp(i, j));
		}
	}
	rep(j, 0, n) {
		int p = 0;
		per(i, 0, n) {
			if (f[i][j] == 1)
				p++;
			else
				p = 0;
			if (p)
				row[p].pb(mp(i, j));
		}
	}
	rep(i, 1, n + 1) sr[i] = sr[i - 1] + SZ(row[i]);
	rep(i, 1, n + 1) sc[i] = sc[i - 1] + SZ(col[i]);
	rep(i, 0, m) scanf("%d%d", a + i, b + i);
	int s = 0;
	rep(i, 0, n) rep(j, 0, n) if (f[i][j])
		r[i][j] = 1, c[i][j] = 1;
	rep(i, 0, m) {
		int dis = 1 << 30, cur = -1;
		rep(j, 0, m) if (!vis[j] && Dis(j) < dis)
			dis = Dis(j), cur = j;
		s += dis;
		if (A <= a[cur]) {
			rep(j, A, a[cur]) for (auto p : row[j])
				r[p.fi][p.se] = 0;
		} else {
			rep(j, a[cur], A) for (auto p : row[j])
				r[p.fi][p.se] = 1;
		}
		if (B <= b[cur]) {
			rep(j, B, b[cur]) for (auto p : col[j])
				c[p.fi][p.se] = 0;
		} else {
			rep(j, b[cur], B) for (auto p : col[j])
				c[p.fi][p.se] = 1;
		}
		A = a[cur];
		B = b[cur];
		vis[cur] = 1;
		ret[cur] = gao();
	}
	rep(i, 0, m) printf("%d\n", ret[i]);
	fprintf(stderr, "%d\n", s);
}
