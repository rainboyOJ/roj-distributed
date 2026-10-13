#include <ctime>
#include <cstdio>
#include <random>
#include <algorithm>

#define nyaa(neko...) fprintf(stderr, neko)

typedef long long ll;
const int maxn = 1E+6 + 5;

namespace Ibuf {
	const int LEN = 1 << 20;
	
	char ibuf[LEN + 5], *p1 = ibuf, *p2 = ibuf;
	
	inline char get() {
#ifndef WHX1003
		return p1 == p2 && (p2 = (p1 = ibuf) + fread(ibuf, 1, LEN, stdin), p1 == p2) ? EOF : *p1++;
#endif
		return getchar();
	}
	
	inline ll getll(char c = get(), ll x = 0, ll op = 1) {
		while(c < '0' || c > '9') c == '-' && (op = -op), c = get();
		while(c >= '0' && c <= '9') x = x * 10 + c - 48, c = get();
		return x * op;
	}
}
using Ibuf::getll;

std::mt19937_64 rnd(time(0));

int T, n, m; 
unsigned long long a[maxn], rdm[maxn];
int main() {
	freopen("st.in","r",stdin);
	freopen("st.out","w",stdout);
	T = getll();
    while(T --> 0) {
		n = getll(), m = getll();

		unsigned long long S = 0;
		for(int i = 1; i < m; ++i)
			rdm[i] = rnd(), S += rdm[i];
		rdm[m] = -S;

		for(int i = 1; i <= n; ++i)
			a[i] = rdm[getll()] + a[i - 1];
		std::sort(a, a + n + 1);

		ll ans = 0;
		for(int i = 1, cnt = 1; i <= n; ++i) {
			if(a[i] == a[i - 1]) ++cnt;
			else cnt = 1;
			ans += cnt - 1;
		}
		printf("%lld\n", ans);
    }
	nyaa("%d\n", clock());
}