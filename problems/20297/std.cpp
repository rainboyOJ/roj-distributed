#include <bits/stdc++.h>
#define ls(p) (p << 1)
#define rs(p) (p << 1 | 1)
using namespace std;
typedef long long ll;
template <typename T>

inline void read(T &x) {
	char c = getchar();
	int w = 1;
	x = 0;
	while (!isdigit(c))
		(c == '-') && (w = -w), c = getchar();
	while (isdigit(c))
		x = (x << 1) + (x << 3) + (c ^ '0'), c = getchar();
	x *= w;
}

const int N = 100010;
int n, Q, a[N], u, v, opt, x;
int inid = 0, in[N], out[N], val[N];
vector<int> G[N];
struct node {
	int L, R, v, tag;
} st[N << 2];

inline void push_up(int p) {
	st[p].v = st[ls(p)].v + st[rs(p)].v;
}

inline void push_down(int p) {
	if (!st[p].tag)
		return;
	st[ls(p)].v = st[ls(p)].R - st[ls(p)].L + 1 - st[ls(p)].v;
	st[rs(p)].v = st[rs(p)].R - st[rs(p)].L + 1 - st[rs(p)].v;
	st[ls(p)].tag ^= 1;
	st[rs(p)].tag ^= 1;
	st[p].tag = 0;
}

inline void build(int l, int r, int p) {
	st[p].L = l;
	st[p].R = r;
	st[p].tag = 0;
	if (l == r) {
		st[p].v = val[l];
		return;
	}
	int mid = l + r >> 1;
	build(l, mid, ls(p));
	build(mid + 1, r, rs(p));
	push_up(p);
}

inline void update(int x, int y, int p) {
	int l = st[p].L, r = st[p].R, mid = l + r >> 1;
	if (x <= l && r <= y) {
		st[p].v = st[p].R - st[p].L + 1 - st[p].v;
		st[p].tag ^= 1;
		return;
	}
	push_down(p);
	if (x <= mid)
		update(x, y, ls(p));
	if (y >  mid)
		update(x, y, rs(p));
	push_up(p);
}

inline int query(int x, int y, int p) {
	int l = st[p].L, r = st[p].R, mid = l + r >> 1;
	if (x <= l && r <= y) {
		return st[p].v;
	}
	push_down(p);
	if (y <= mid)
		return query(x, y, ls(p));
	if (x >  mid)
		return query(x, y, rs(p));
	return query(x, y, ls(p)) + query(x, y, rs(p));
}

inline void dfs(int u, int fa) {
	in[u] = ++ inid;
	val[in[u]] = a[u];
	for (auto v : G[u]) {
		if (v == fa)
			continue;
		dfs(v, u);
	}
	out[u] = inid;
}

signed main() {
	freopen("trerone.in", "r", stdin);
	freopen("trerone.out", "w", stdout);
	read(n);
	read(Q);
	for (int i = 1; i <= n; ++i) {
		char c = getchar();
		while (!isdigit(c))
			c = getchar();
		a[i] = c - '0';
	}
	for (int i = 1; i < n; ++i) {
		read(u);
		read(v);
		G[u].push_back(v);
		G[v].push_back(u);
	}
	dfs(1, 0);
	build(1, n, 1);
	while (Q -- > 0) {
		read(opt);
		read(x);
		if (opt == 0) {
			update(in[x], out[x], 1);
		} else {
			printf("%d\n", query(in[x], out[x], 1));
		}
	}
	return 0;
}