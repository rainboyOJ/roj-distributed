#include <iostream>
#include <cmath>
#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

struct bian {
	int next, point, w, id;
} b[210000];

struct atom {
	int l, r;
} A[110000];
int n, m, p[110000], sign, dfs[110000], r[110000], d[110000], father[110000][17], len, x[110000], K, s[110000], head,
    pre[110000];
int ver[110000];
long long dis[110000];

void ade(int k1, int k2, int k3, int k4) {
	b[++len] = (bian) {
		p[k1], k2, k3, k4
	};
	p[k1] = len;
}

void add(int k1, int k2, int k3, int k4) {
	ade(k1, k2, k3, k4);
	ade(k2, k1, k3, k4);
}

void dfs1(int k1, int k2) {
	father[k1][0] = k2;
	d[k1] = d[k2] + 1;
	dfs[k1] = ++sign;
	x[sign] = k1;
	for (int i = p[k1]; i; i = b[i].next) {
		int j = b[i].point;
		if (j != k2) {
			ver[b[i].id] = j;
			dis[j] = dis[k1] + b[i].w;
			dfs1(j, k1);
		}
	}
	r[k1] = sign;
}

int getlca(int k1, int k2) {
	if (d[k1] < d[k2])
		swap(k1, k2);
	for (int i = 16; i >= 0; i--)
		if (d[k1] - d[k2] >= (1 << i))
			k1 = father[k1][i];
	if (k1 == k2)
		return k1;
	for (int i = 16; i >= 0; i--)
		if (father[k1][i] != father[k2][i]) {
			k1 = father[k1][i];
			k2 = father[k2][i];
		}
	return father[k1][0];
}

long long getdis(int k1, int k2) {
	if (k1 == 0 || k2 == 0)
		return -1;
	return dis[k1] + dis[k2] - (dis[getlca(k1, k2)] << 1);
}

struct tree {
	int u, v;
	long long w;
	void set(int k) {
		u = k;
		v = k;
		w = 0;
		if (k == 0)
			w = -1;
	}
	void update(tree k1) {
		if (k1.w > w) {
			u = k1.u;
			v = k1.v;
			w = k1.w;
		}
	}
} t[410000], ans[110000];

tree get(int k1, int k2) {
	return (tree) {
		k1, k2, getdis(k1, k2)
	};
}

tree operator + (tree k1, tree k2) {
//	cout<<"merge "<<k1.u<<" "<<k1.v<<" "<<k2.u<<" "<<k2.v<<endl;
	tree ans = k1;
	ans.update(k2);
	ans.update(get(k1.u, k2.u));
	ans.update(get(k1.u, k2.v));
	ans.update(get(k1.v, k2.u));
	ans.update(get(k1.v, k2.v));
	return ans;
}

void buildtree(int k1, int k2, int k3) {
	if (k2 == k3) {
		t[k1].set(x[k2]);
		return;
	}
	int mid = k2 + k3 >> 1;
	buildtree(k1 * 2, k2, mid);
	buildtree(k1 * 2 + 1, mid + 1, k3);
	t[k1] = t[k1 * 2] + t[k1 * 2 + 1];
}

int compare(atom k1, atom k2) {
	return k1.l < k2.l || (k1.l == k2.l && k1.r < k2.r);
}

int check(atom k1, atom k2) {
	return k1.l <= k2.l && k1.r >= k2.r;
}

tree find(int k1, int k2, int k3, int k4, int k5) {
//	cout<<"find "<<k2<<" "<<k3<<" "<<k4<<" "<<k5<<" "<<t[k1].u<<" "<<t[k1].v<<" "<<t[k1].w<<endl;
	if (k2 > k5 || k3 < k4) {
		tree num;
		num.set(0);
		return num;
	}
	if (k2 >= k4 && k3 <= k5)
		return t[k1];
	int mid = k2 + k3 >> 1;
	return find(k1 * 2, k2, mid, k4, k5) + find(k1 * 2 + 1, mid + 1, k3, k4, k5);
}

int main() {
	freopen("diameter.in", "r", stdin);
	freopen("diameter.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 1; i < n; i++) {
		int k1, k2, k3;
		scanf("%d%d%d", &k1, &k2, &k3);
		add(k1, k2, k3, i);
	}
	dfs1(1, 0);
	for (int i = 1; i <= 16; i++)
		for (int j = 1; j <= n; j++)
			father[j][i] = father[father[j][i - 1]][i - 1];
	buildtree(1, 1, n);
	scanf("%d", &m);
	for (; m; m--) {
		scanf("%d", &K);
		for (int i = 1; i <= K; i++) {
			int k1;
			scanf("%d", &k1);
			k1 = ver[k1];
			A[i] = (atom) {
				dfs[k1], r[k1]
			};
		}
		//	for (int i=1;i<=K;i++) cout<<A[i].l<<" "<<A[i].r<<endl;
		K++;
		A[K] = (atom) {
			1, n
		};
		sort(A + 1, A + K + 1, compare);
		//for (int i=1;i<=K;i++) cout<<A[i].l<<" "<<A[i].r<<endl;
		for (int i = 1; i <= K; i++)
			pre[i] = A[i].l;
		for (int i = 1; i <= K; i++)
			ans[i].set(0);
		head = 1;
		s[1] = 1;
		for (int i = 2; i <= K; i++) {
			while (head && check(A[s[head]], A[i]) == 0)
				head--;
			if (pre[s[head]] != A[i].l)
				ans[s[head]] = ans[s[head]] + find(1, 1, n, pre[s[head]], A[i].l - 1);
			pre[s[head]] = A[i].r + 1;
			s[++head] = i;
		}
		for (int i = 1; i <= K; i++)
			if (pre[i] <= A[i].r)
				ans[i] = ans[i] + find(1, 1, n, pre[i], A[i].r);
		long long tot = 0;
		//	for (int i=1;i<=K;i++) cout<<ans[i].u<<" "<<ans[i].v<<" "<<ans[i].w<<endl;
		for (int i = 1; i <= K; i++)
			tot += ans[i].w;
		printf("%lld\n", tot);
	}
	return 0;
}

