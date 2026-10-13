#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <cassert>
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
	for (; b; b >>= 1) {
		if (b & 1)
			res = res * a % mod;
		a = a * a % mod;
	}
	return res;
}
// head

const int N = 2010;
int n;
ll a[N], g[N];
vector<ll> dv;
unordered_map<ll, int> hs;
int check(ll c) {
	hs.clear();
	int ans = 0;
	rep(i, 1, n + 1) ans = max(ans, ++hs[a[i] % c]);
	return ans;
}

int main() {
	freopen("gcd.in", "r", stdin);
	freopen("gcd.out", "w", stdout);
	scanf("%d", &n);
	rep(i, 1, n + 1) {
		scanf("%lld", a + i);
		a[i] += a[i - 1];
	}
	for (ll i = 1; i * i <= a[n]; i++)
		if (a[n] % i == 0)
			dv.pb(i), dv.pb(a[n] / i);
	sort(all(dv));
	for (auto c : dv) {
		int k = check(c);
		g[k] = max(g[k], c);
	}
	per(k, 1, n + 1) g[k] = max(g[k], g[k + 1]);
	rep(k, 1, n + 1) printf("%lld\n", g[k]);
}
