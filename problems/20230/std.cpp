#include <bits/stdc++.h>
using namespace std;
const int maxn = 605;
const int mod = 1e9 + 7;
int t;
int n, m, k;
int a[maxn];

struct qnode {
	int x, y;
	qnode () {

	}
	qnode (int xx, int yy) {
		x = xx;
		y = yy;
	}
	bool operator < (const qnode &r) const {
		return x > r.x;
	}
};

struct inFo {
	int cnt;
	qnode v[maxn];
	void clr () {
		cnt = 0;
	}
	void add (int A, int B) {
		v[++cnt] = qnode(A, B);
	}
	void fix () {
		sort(v + 1, v + cnt + 1);
		int i, j, k = 0;
		for (i = 1; i <= cnt; i = j) {
			int tt = 0;
			for (j = i; j <= cnt && v[i].x == v[j].x; j++)
				tt = (tt + v[j].y) % mod;
			v[++k] = qnode(v[i].x, tt);
			if (k >= m)
				break;
		}
		cnt = k;
	}
} f[2][maxn][3];

int main () {
	freopen("permutation.in", "r", stdin);
	freopen("permutation.out", "w", stdout);
	scanf("%d%d", &n, &m);
	for (int i = 1; i <= n; i++)
		scanf("%d", a + i);
	sort(a + 1, a + n + 1);
	for (int i = 0; i < 2; i++)
		for (int j = 0; j <= n; j++)
			for (int k = 0; k < 3; k++)
				f[i][j][k].clr();
	f[1][1][0].add(0, 1);
	f[1][1][1].add(0, 2);
	int tt = 1;
	for (int i = 1; i < n; i++) {
		for (int j = 0; j <= n; j++)
			for (int k = 0; k < 3; k++)
				f[tt ^ 1][j][k].clr();
		for (int j = 0; j <= n; j++)
			for (int k = 0; k < 3; k++) {
				f[tt][j][k].fix();
				int cnt = f[tt][j][k].cnt;
				if (!cnt)
					continue;
				int base = (a[i + 1] - a[i]) * (j * 2 - k);
				for (int l = 1; l <= cnt; l++) {
					int A = base + f[tt][j][k].v[l].x;
					int B = f[tt][j][k].v[l].y;
					if (j + 1 > k)
						f[tt ^ 1][j + 1][k].add(A, 1ll * B * (j + 1 - k) % mod);
					if (j > 1)
						f[tt ^ 1][j - 1][k].add(A, 1ll * B * (j - 1) % mod);
					if (j * 2 > k)
						f[tt ^ 1][j][k].add(A, 1ll * B * (j * 2 - k) % mod);
					if (k < 2) {
						f[tt ^ 1][j + 1][k + 1].add(A, 1ll * B * (2 - k) % mod);
						f[tt ^ 1][j][k + 1].add(A, 1ll * B * (2 - k) % mod);
					}
				}
			}
		tt ^= 1;
	}
	f[tt][1][2].fix();
	int i;
	for (i = 1; i <= f[tt][1][2].cnt && i <= m; i++) {
		printf("%d %d\n", f[tt][1][2].v[i].x, (f[tt][1][2].v[i].y % mod + mod) % mod);
	}
	for (; i <= m; i++)
		printf("-1 -1\n");
}