#include <bits/stdc++.h>
using namespace std;

const int mo = 998244353, inv2 = (mo + 1) / 2;
int l, r;
map <int, int> M;

int f(int x) {
	if (M.find(x) != M.end())
		return M[x];
	if (x == 1)
		return M[x] = 2;
	if (x & 1)
		return M[x] = (1LL * inv2 * (f(x / 2) + f(x / 2 + 1)) + 1) % mo;
	return M[x] = f(x / 2);
}

int ask(int l, int r) {
	int s = 0;
	if (l == r)
		return f(l);
	if (l & 1)
		s = f(l), l++;
	if (r & 1)
		s = (s + f(r)) % mo, r--;
	s = (s + (r - l) / 2 + 2LL * ask(l / 2, r / 2)) % mo;
	s = (s + mo - 1LL * inv2 * (f(l) + f(r)) % mo) % mo;
	return s;
}

void work() {
	scanf("%d %d", &l, &r);
	if (r == 0)
		puts("0"), exit(0);
	l = max(1, l);
	printf("%d", ask(l, r));
}

int main() {
	freopen("lowbit.in", "r", stdin);
	freopen("lowbit.out", "w", stdout);
	work();
	return 0;
}
