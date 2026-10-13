#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <cstring>
#include <set>
using namespace std;
typedef long long LL;
LL MAX = (1LL << 55);
const LL N = 100005;
set<LL >::iterator it, it1;
LL n, k;
LL a[N], ss[N], f[N];
LL tot[N];

LL find_fa (LL x)    {
	return f[x] == x ? f[x] : f[x] = find_fa(f[x]);
}
set<LL> s[N], s1[N];
LL ans;

void Merge (LL x, LL y) { //这两个联通块可以合在一起了
	bool tf = false; //前面的小
	if (tot[x] > tot[y]) {
		tf = true;
		swap(x, y); //把x并在y那里
	}
	f[x] = y;
	tot[y] = tot[y] + tot[x];
	if (tf == false) {
		for (it = s1[x].begin(); it != s1[x].end(); it++) {
			LL xx = (*it);
			LL t = xx + k;
			it1 = s[y].lower_bound(t);
			if (it1 != s[y].end())
				ans = min(ans, abs(*(it1) - t));
			if (it1 != s[y].begin()) {
				it1--;
				ans = min(ans, abs(*(it1) - t));
			}
		}
	} else {
		for (it = s[x].begin(); it != s[x].end(); it++) {
			LL xx = (*it);
			LL t = xx - k;
			it1 = s1[y].lower_bound(t);
			if (it1 != s1[y].begin()) {
				it1--;
				ans = min(ans, abs((*it1) - t));
			}
			t = k - xx;
			it1 = s1[y].lower_bound(-t);
			if (it1 != s1[y].end())
				ans = min(ans, abs((*it1) + t));
		}
	}
//    printf("TYB\n");
	for (it = s[x].begin(); it != s[x].end(); it++)
		s[y].insert((*it));
	for (it = s1[x].begin(); it != s1[x].end(); it++)
		s1[y].insert((*it));
	s[x].clear();
	s1[x].clear();
}
LL Ans[N];

int main() {
	freopen("neginf.in", "r", stdin);
	freopen("neginf.out", "w", stdout);
	a[0] = 0;
	scanf("%lld%lld", &n, &k);
	for (LL u = 1; u <= n; u++)
		scanf("%lld", &a[u]);
	for (LL u = 1; u <= n; u++)
		a[u] = a[u] + a[u - 1];
	for (LL u = 1; u <= n; u++)
		scanf("%lld", &ss[u]);
	bool ok = false;
	for (LL u = n; u >= 1; u--) {
		LL x = ss[u];
		//printf("del:%I64d %I64d\n",x,a[x]);
		f[x] = x;
		tot[x] = 1;
		s[x].clear();
		s1[x].clear();
		s[x].insert(a[x]);
		s1[x].insert(a[x - 1]);
		//printf("add:%I64d %I64d\n",a[x],a[x-1]);
		if (ok == false) {
			ans = abs((a[x] - a[x - 1]) - k);
			ok = true;
		}
		ans = min(ans, abs((a[x] - a[x - 1]) - k));
		if (f[x + 1] != 0)
			Merge(find_fa(x), find_fa(x + 1));
		if (f[x - 1] != 0)
			Merge(find_fa(x - 1), find_fa(x));
		Ans[u] = ans;
	}
	for (LL u = 1; u <= n; u++)
		printf("%lld\n", Ans[u]);
}