#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>
#include <queue>
#include <vector>
using namespace std;
typedef long long LL;
typedef pair<int, int> PII;
typedef vector<int> VI;
const int maxn = 411111;
const int mod = (int) (1e9 + 7);
const int POW = 19;
int head[maxn], e, N, M;
int score[maxn];
int p[POW][maxn], dep[maxn];
int cur[maxn], top, father[maxn];
PII st[maxn];
bool vis[maxn];
vector<PII> V[maxn];
vector<int> val[maxn];
vector<int> odd[maxn];
vector<int> even[maxn];

struct node {
	int v, next, w;
	node(int v = 0, int next = 0, int w = 0) :
		v(v), next(next), w(w) {
	}
} edge[maxn << 2];

void add_edge(int u, int v, int w) {
	edge[e] = node(v, head[u], w);
	head[u] = e++;
	edge[e] = node(u, head[v], w);
	head[v] = e++;
}

void dfs(int s) {
	score[1] = 0;
	int i, v, top = 0, u;
	st[top++] = PII(1, 0);
	for (i = 1; i <= N; ++i)
		cur[i] = head[i];
	vis[1] = true;
	p[0][1] = 1;
	father[1] = 0;
	while (top) {
		u = st[top - 1].first;
		p[0][u] = father[u];
		for (i = 1; i < POW; ++i) {
			v = p[i - 1][u];
			p[i][u] = p[i - 1][v];
		}
		int &i = cur[u];
		for (i = cur[u]; ~i; i = edge[i].next) {
			v = edge[i].v;
			if (vis[v])
				continue;
			vis[v] = true;
			st[top++] = PII(v, edge[i].w);
			father[v] = u;
			dep[v] = dep[u] + 1;
			break;
		}
		if (i < 0) {
			u = st[top - 1].first;
			score[father[u]] += score[u] + st[top - 1].second;
			--top;
		}
	}
}

void bfs(int s) {
	static int q[maxn], front, rear;
	int v, i, u;
	front = rear = 0;
	vis[s] = true;
	q[rear++] = s;
	int tot = score[1];
	while (front < rear) {
		u = q[front++];
		for (i = head[u]; ~i; i = edge[i].next) {
			v = edge[i].v;
			if (!vis[v]) {
				vis[v] = true;
				q[rear++] = v;
				V[u].push_back(PII(v, edge[i].w + score[v]));
				V[v].push_back(PII(u, tot - score[v]));
				val[u].push_back(edge[i].w + score[v]);
				val[v].push_back(tot - score[v]);
			}
		}
	}
	int j, sz, k, t = 0;
	vector<int>::iterator it;
	for (i = 1; i <= N; ++i) {
		sort(V[i].begin(), V[i].end());
		sort(val[i].begin(), val[i].end(), greater<int>());
		sz = val[i].size();
		t = 0;
		for (it = val[i].begin(); it != val[i].end(); t ^= 1, ++it) {
			k = *it;
			if (t & 1) {
				even[i].push_back(0);
				odd[i].push_back(k);
			} else {
				even[i].push_back(k);
				odd[i].push_back(0);
			}
		}
		for (j = 1; j < sz; ++j) {
			even[i][j] += even[i][j - 1];
			odd[i][j] += odd[i][j - 1];
		}
	}

}

int find(int u, int k) {
	if (!k)
		return u;
	for (int i = 0; i < POW; ++i)
		if ((k >> i) & 1)
			u = p[i][u];

	return u;
}

int query(int a, int b) {
	int i;

	if (dep[a] > dep[b])
		swap(a, b);
	if (dep[b] > dep[a])
		b = find(b, dep[b] - dep[a]);
	if (a ^ b) {
		for (i = POW - 1; i >= 0; --i) {
			if (p[i][a] ^ p[i][b]) {
				a = p[i][a];
				b = p[i][b];
			}
		}
		a = p[0][a];
	}
	return a;
}

int getsum(int l, int r, const vector<int> &v) {
	if (l > r)
		return 0;
	if (l)
		return v[r] - v[l - 1];
	else
		return v[r];
}

int binary(int l, int r, int k, const VI &v) {
	int m, ans;
	while (l <= r) {
		m = (l + r) >> 1;
		if (v[m] >= k)
			ans = m, l = m + 1;
		else
			r = m - 1;
	}
	return ans;
}

int main() {
	freopen("tree.in", "r", stdin);
	freopen("tree.out", "w", stdout);
	int i, u, v, w, d, k;
	int T;
	int q = 0;
	vector<PII>::iterator iter;
	scanf("%d%d", &N, &M);

	e = 0;

	fill(score, score + N + 3, 0);
	fill(head, head + N + 3, -1);
	fill(dep, dep + N + 3, 0);
	for (i = 1; i < N; ++i) {
		scanf("%d%d%d", &u, &v, &w);
		add_edge(u, v, w);
	}
	for (i = 0; i <= N; ++i) {
		V[i].clear();
		val[i].clear();
		odd[i].clear();
		even[i].clear();
	}
	fill(vis, vis + N + 2, false);
	dfs(1);
	fill(vis, vis + N + 2, false);
	bfs(1);
	int dis, x, y, ans, sz, LCA;
	for (i = 0; i < M; ++i) {
		scanf("%d%d", &u, &v);
		if (u == v) {
			k = u;
			sz = V[k].size();
			printf("%d\n", getsum(0, sz - 1, even[k]));
			continue;
		}

		ans = 0;
		LCA = query(u, v);
		d = dep[u] + dep[v] - (dep[LCA] << 1);
		if (d == 1) {
			sz = val[v].size();
			iter = lower_bound(V[v].begin(), V[v].end(), PII(u, -1));
			y = binary(0, sz - 1, iter->second, val[v]);
			ans += getsum(0, y - 1, odd[v]);
			ans += getsum(y + 1, sz - 1, even[v]);
			ans += iter->second;
			printf("%d\n", ans);
			continue;
		}

		dis = (d + 1) >> 1;

		if (dep[u] == dep[v] || dep[u] == dep[v] + 1) {
			u = find(u, dis - 1);
			v = find(v, (d - dis - 1));
			k = p[0][u];
		} else if (dep[u] > dep[v]) {
			k = find(u, dis);
			u = find(u, dis - 1);
			v = p[0][k];
		} else {
			dis = d - dis;
			k = find(v, dis);
			v = find(v, dis - 1);
			u = p[0][k];
		}

		sz = V[k].size();
		iter = lower_bound(V[k].begin(), V[k].end(), PII(u, 0));
		x = binary(0, sz - 1, iter->second, val[k]);

		iter = lower_bound(V[k].begin(), V[k].end(), PII(v, 0));
		y = binary(0, sz - 1, iter->second, val[k]);

		if (sz < 3) {
			printf("%d\n", val[k][x]);
			continue;
		}

		if (d & 1)
			ans += val[k][y];
		else
			ans += val[k][x];

		if (x == y)
			x = y - 1;
		if (x > y)
			swap(x, y);
		ans += getsum(0, x - 1, even[k]);
		ans += getsum(x + 1, y - 1, odd[k]);
		ans += getsum(y + 1, sz - 1, even[k]);
		if (d & 1)
			ans = score[1] - ans;

		printf("%d\n", ans);

	}
	q += M;
	return 0;
}
