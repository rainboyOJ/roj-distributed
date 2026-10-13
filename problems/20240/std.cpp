#include <bits/stdc++.h>
#define M 500005
#define L long long
using namespace std;




int l[M] = {0}, r[M] = {0}, a[M] = {0}, p[M] = {0};
int n, k;
L ans = 0;

bool cmp(int x, int y) {
	return a[x] < a[y];
}

int main() {
	freopen("kth.in", "r", stdin);
	freopen("kth.out", "w", stdout);
	ans = 0;
	scanf("%d%d", &n, &k);
	for (int i = 1; i <= n; i++)
		scanf("%d", a + i), p[i] = i;
	for (int i = 1; i <= n; i++)
		r[i] = i + 1, l[i] = i - 1;
	sort(p + 1, p + n + 1, cmp);
	for (int i = 1; i <= n; i++) {
		int id = p[i];
		int lid, lcnt = 1;
		for (lid = id; l[lid] != 0 && lcnt != k; lid = l[lid], lcnt++);
		int rid = id, rcnt = 0;
		while (lcnt + rcnt < k && r[rid] != n + 1) {
			rid = r[rid];
			rcnt++;
		}
		if (lcnt + rcnt == k) {
			while (rid != n + 1) {
				L ll = lid - l[lid], rr = r[rid] - rid;
				ans += ll * rr * a[id];
				if (lid == id)
					break;
				lid = r[lid];
				rid = r[rid];
			}
		}
		lid = l[id];
		rid = r[id];
		r[lid] = rid;
		l[rid] = lid;
	}
	printf("%lld\n", ans);
}