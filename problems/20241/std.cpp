#include <bits/stdc++.h>
#define LL long long
using namespace std;
const int maxn = 500010;
vector<int> G[maxn];
int mp[maxn], mx_dis[maxn], f[maxn], Mx[maxn];
bool v[maxn], v1[maxn];
int root, mx, now;
vector<int> a;

void add(int x, int y) {
	G[x].push_back(y);
	G[y].push_back(x);
}

void dfs(int x, int fa, int dis, bool flag) {
	f[x] = fa;
	v1[x] = flag;
	if (dis > mx) {
		mx = dis;
		now = x;
	}
	for (auto y : G[x]) {
		if (y == fa || v[y])
			continue;
		dfs(y, x, dis + 1, flag);
	}
}

int dfs1(int x, int fa) {
	int mx = 0;
	for (auto y : G[x]) {
		if (v[y] || y == fa)
			continue;
		mx = max(mx, dfs1(y, x));
	}
	return mx + 1;
}

int main() {
	freopen("tree.in", "r", stdin);
	freopen("tree.out", "w", stdout);
	int T, x, y, n;
	scanf("%d", &n);
	a.clear();
	for (int i = 1; i <= n; i++)
		G[i].clear();
	for (int i = 1; i < n; i++) {
		scanf("%d%d", &x, &y);
		add(x, y);
	}
	for (int i = 1; i <= n; i++)
		v[i] = v1[i] = mp[i] = f[i] = mx_dis[i] = 0;
	root = 1, mx = 0;
	dfs(root, 0, 1, 0);
	root = now, mx = 0;
	dfs(root, 0, 1, 0);
	for (int i = now; i; i = f[i]) {
		v[i] = 1;
		a.push_back(i);
	}
	for (auto x : a) {
		mx_dis[x] = dfs1(x, 0);
	}
	for (int i = 1; i <= n; i++)
		v1[i] = 0;
	int tmp = 0;
	for (int i = 1; i <= n; i++) {
		if (v[i] == 0 && v1[i] == 0) {
			now = mx = 0;
			dfs(i, 0, 1, 0);
			dfs(now, 0, 1, 1);
			tmp = max(tmp, mx);
		}
	}
	mp[a.size()] = tmp;
	mp[tmp] = a.size();
	Mx[a.size()] = 0;
	for (int i = a.size() - 2; i >= 0; i--) {
		Mx[i + 1] = max(Mx[i + 2], (int)a.size() - i - 2 + mx_dis[a[i + 1]]);
	}
	for (int i = 0; i < a.size() - 1; i++) {
		int x = i + mx_dis[a[i]];
		int y = Mx[i + 1];
		mp[x] = max(mp[x], y);
		mp[y] = max(mp[y], x);
	}
	LL ans = 0;
	mx = 0;
	for (int i = a.size(); i >= 1; i--) {
		mx = max(mx, mp[i]);
		ans += mx;
	}
	printf("%lld\n", ans);
}