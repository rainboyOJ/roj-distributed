#include <bits/stdc++.h>

using namespace std;

const int N = 5e3 + 5, mod = 998244353;
typedef long long ll;

int n, m;
char str[N];

struct Z {
	ll v;
	bool o;
	inline Z() { v = 0, o = 0; }
	inline Z(ll v, bool o) : v(v), o(o) {}
	inline friend Z operator + (Z a, Z b) {
		Z c;
		if (a.o || b.o) c.o = 1;
		if (a.v + b.v >= mod) c.o = 1;
		c.v = (a.v + b.v) % mod;
		return c;
	}
	inline friend Z operator * (Z a, Z b) {
		Z c;
		if (a.o || b.o) c.o = 1;
		if (a.v * b.v >= mod) c.o = 1;
		c.v = a.v * b.v % mod;
		return c;
	}
	inline friend bool operator == (Z a, Z b) {
		return a.v == b.v && a.o == b.o;
	}
} a[N];

void work() {
	if (a[m] == Z(1, 0)) return;
	if (a[m].o) {
		for (int i = m - 1; i >= 1; i--) {
			if (a[i].v == -1) break;
			if (!(a[i] == Z(1, 0))) {
				a[i] = a[i] * a[m];
				m = i;
				return work();
			}
		}
		return;
	}
	ll p = a[m].v, s = a[m].v;
	const ll lim = 1e15;
	for (int i = m - 1; i >= 1; i--) {
		if (a[i].v == -1) break;
		if (a[i].o) {
			a[i] = a[i] * Z(p, 0), m = i;
			return work();
		}
		if (p >= lim / a[i].v) {
			a[i].o = 1, a[i].v = a[i].v * (p % mod) % mod;
			m = i;
			return work();
		}
		p = p * a[i].v, s = s + a[i].v;
		if (p >= s) {
			if (p >= mod) a[i].o = 1;
			a[i].v = p % mod;
			m = i;
			return work();
		}
	}
}

inline void solve() {
	scanf("%s", str + 1), n = strlen(str + 1);
	assert(n <= 5000);
	m = 0;
	for (int i = 1; i <= n; i++) {
		if (str[i] == '(') a[++m] = Z(-1, 0);
		if (str[i] == 'x') a[++m] = Z(1, 0), work();
		if (str[i] == ')') {
			Z cur;
			while (a[m].v != -1) {
				cur = cur + a[m];
				m--;
			}
			a[m] = cur, work();
		}
	}
	Z ans;
	while (m >= 1) ans = ans + a[m], m--;
	printf("%lld\n", ans.v);
}

int main()
{
	int T; scanf("%d", &T);
	while (T--) solve();
	return 0;
}
