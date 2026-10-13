
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
const int MX = 2e5 + 5;
const LL mod = 1e9 + 7;

struct Edge {
	int v, nxt;
} E[MX * 2];
int head[MX], rear;

void add(int u, int v) {
	E[rear].v = v;
	E[rear].nxt = head[u];
	head[u] = rear++;
}

int col[MX];
int sz[MX];
int vis[MX];
LL sum[MX];
LL ans;

void init(int n) {
	for (int i = 1; i <= n; i++)
		head[i] = -1, vis[i] = sum[i] = 0;
	rear = 0;
}


void dfs(int u, int fa) {
	sz[u] = 1;
	LL pre = sum[col[u]], c = 0, szv;
	for (int i = head[u]; ~i; i = E[i].nxt) {
		int v = E[i].v;
		if (v == fa)
			continue;
		dfs(v, u);
		sz[u] += sz[v];
		LL tmp = sum[col[u]] - pre;//子树v中以颜色col[u]为根的子树大小
		szv = sz[v] - tmp; //子树v中其它颜色的连通的节点数量
		pre = sum[col[u]];
		ans -= szv * (szv - 1) / 2;
		c += tmp;  //c为了避免重复计算sz[u]的大小
	}
	sum[col[u]] += sz[u] - c; //sum[col[u]]加上以u为根的子树大小
}

int main() {
	freopen("tree.in", "r", stdin);
	freopen("tree.out", "w", stdout);
	int n, cas = 0;
	scanf("%d", &n);
	init(n);
	int cnt = 0;
	for (int i = 1; i <= n; i++) {
		scanf("%d", &col[i]);
		if (!vis[col[i]]) {
			vis[col[i]] = 1;
			cnt++;
		}
	}
	for (int i = 1, u, v; i < n; i++) {
		scanf("%d%d", &u, &v);
		add(u, v);
		add(v, u);
	}
	ans = (LL)cnt * n * (n - 1) / 2;
	dfs(1, -1);
	for (int i = 1; i <= n; i++) {
		if (sum[i] == 0)
			continue;
		LL tmp = n - sum[i];
		ans -= tmp * (tmp - 1) / 2;
	}
	printf("%lld\n", ans);
	return 0;
}