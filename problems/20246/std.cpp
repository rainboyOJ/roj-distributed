#include <bits/stdc++.h>
using namespace std;
#define LL long long
const int inf = 0x3f3f3f3f;
const int maxn = 2e5 + 5;
const int Mod = 998244353;

vector<pair<int, int> > e[maxn];
vector<int> Q;
int st, nxt, dir, siz, edg;
int d[maxn], dp[maxn];
bool vis[maxn];

void check(int u) {//判断边与点数的关�?
	vis[u] = 1;
	siz ++;
	for (int i = 0; i < e[u].size(); i ++) {
		edg++;
		if (!vis[e[u][i].first])
			check(e[u][i].first);
	}
}

void dfs(int u, int fa) {//以i点为根时图的反转数量
	vis[u] = 1;
	d[u] = 0;
	for (int i = 0; i < e[u].size(); i ++) {
		pair<int, int> v = e[u][i];
		if (!vis[v.first]) {
			dfs(v.first, u);
			d[u] += d[v.first] + ((v.second % 2) ^ 1);
		} else if (v.first != fa) {
			st = u;
			nxt = v.first;
			dir = v.second;
		}
	}
}

void calc(int u, pair<int, int> pre) {//树形dp改变根的数字，可以有已得的推�?
	Q.push_back(dp[u]);
	for (int i = 0; i < e[u].size(); i ++) {
		pair<int, int> v = e[u][i];
		if (v == pre)
			continue;
		if (v.second == dir || v.second == (dir ^ 1))
			continue;
		dp[v.first] = dp[u] + ((v.second % 2 == 0) ? -1 : 1);
		calc(v.first, {u, v.second ^ 1});
	}
}

int main(int argc, char *argv[]) {
	freopen("card.in", "r", stdin);
	freopen("card.out", "w", stdout);
	int T, n;
	scanf("%d", &n);
	for (int i = 1; i <= n * 2; i ++)
		e[i].clear();
	for (int i = 1; i <= n; i ++) {
		int x, y;
		scanf("%d %d", &x, &y);
		e[y].push_back(make_pair(x, 2 * i - 1));//给边编号
		e[x].push_back(make_pair(y, 2 * i - 2));
	}
	memset(vis, 0, sizeof(vis));
	int fl = 1;
	for (int i = 1; i <= 2 * n; i ++) {
		if (vis[i])
			continue;
		siz = edg = 0;
		check(i);
		if (edg / 2 > siz) {
			fl = 0;
			break;
		}
	}
	if (fl == 0)
		puts("-1 -1");
	else {
		memset(vis, 0, sizeof(vis));
		int ans = 0, tot = 1;
		for (int i = 1; i <= n * 2; i ++) {
			if (vis[i])
				continue;
			st = dir = nxt = -1;
			dfs(i, 0);
			dp[i] = d[i];
			Q.clear();
			calc(i, {0, 0});
			int cnt = 0;
			if (st == -1) {
				sort(Q.begin(), Q.end());
				for (int i = 0; i < Q.size(); i ++)//Q[0]是最少改变的边，也就是反转卡片的数量
					if (Q[i] == Q[0])
						cnt ++;
				ans += Q[0];
			} else {
				dir %= 2;
				if (dp[st] + dir == dp[nxt] + (dir ^ 1))
					cnt = 2;//判断环的顺时针和逆时针是否相�?
				else
					cnt = 1;
				ans += min(dp[st] + dir, dp[nxt] + (dir ^ 1));
			}
			tot = 1LL * tot * cnt % Mod;//方法�?
		}
		cout << ans << " " << tot << endl;
	}
	return 0;
}

