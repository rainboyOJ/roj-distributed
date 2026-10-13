#include <bits/stdc++.h>
#define INF 0x3f3f3f3f
#define full(a, b) memset(a, b, sizeof a)
#define FAST_IO ios::sync_with_stdio(false), cin.tie(0), cout.tie(0)
using namespace std;
typedef long long ll;

inline int lowbit(int x) {
	return x & (-x);
}

inline int read() {
	int ret = 0, w = 0;
	char ch = 0;
	while (!isdigit(ch)) {
		w |= ch == '-';
		ch = getchar();
	}
	while (isdigit(ch))
		ret = (ret << 3) + (ret << 1) + (ch ^ 48), ch = getchar();
	return w ? -ret : ret;
}

inline int gcd(int a, int b) {
	return b ? gcd(b, a % b) : a;
}

inline int lcm(int a, int b) {
	return a / gcd(a, b) * b;
}
template <typename T>

inline T max(T x, T y, T z) {
	return max(max(x, y), z);
}
template <typename T>

inline T min(T x, T y, T z) {
	return min(min(x, y), z);
}
template <typename A, typename B, typename C>

inline A fpow(A x, B p, C lyd) {
	A ans = 1;
	for (; p; p >>= 1, x = 1LL * x * x % lyd)
		if (p & 1)
			ans = 1LL * x * ans % lyd;
	return ans;
}
const int N = 100005;
int _, n, w[N], p[N];
multiset<int> s[N];

int main() {
	freopen("sibling.in", "r", stdin);
	freopen("sibling.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 2; i <= n; i ++)
		scanf("%d", &p[i]);
	for (int i = 1; i <= n; i ++)
		scanf("%d", &w[i]);
	for (int i = 1; i <= n; i ++) {
		s[p[i]].insert(w[i]);
	}
	ll maximum = 0, minimum = 0, x = 0, y = 0;
	for (int i = 0; i <= n; i ++) {
		if (s[i].size() == 1) {
			set<int>::iterator it = s[i].begin();
			*it > 0 ? maximum += *it : minimum += *it;
		} else if (s[i].size() >= 2) {
			set<int>::iterator it = --s[i].end();
			if (*it > 0)
				maximum += *it;
			if (*(--it) > 0)
				x = max(x, (*it) * 1LL);
			it = s[i].begin();
			if (*it < 0)
				minimum += *it;
			if (*(++it) < 0)
				y = min(y, (*it) * 1LL);
		}
	}
	maximum += x, minimum += y;
	printf("%lld %lld\n", maximum, minimum);
	return 0;
}