#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cassert>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <queue>
#include <deque>
#include <set>
#include <map>
#include <utility>
#include <numeric>
#include <algorithm>
#include <bitset>
#include <complex>
#include <unordered_set>
#include <unordered_map>

using namespace std;

typedef unsigned uint;
typedef long long Int;
typedef vector<int> vint;
typedef pair<int, int> pint;
#define mp make_pair

template<typename T> void pv(T a, T b) {
	for (T i = a; i != b; ++i)
		cout << *i << " ";
	cout << endl;
}

template<typename T> void chmin(T &t, const T &f) {
	if (t > f)
		t = f;
}

template<typename T> void chmax(T &t, const T &f) {
	if (t < f)
		t = f;
}

int in() {
	int x;
	scanf("%d", &x);
	return x;
}

const int E = 17;
const int LIM_SMALL = 300;

int N;
int X[100010], Y[100010], D[100010];
int Q;
int S[100010], T[100010], P[100010];

int m;
int ptr[100010], nxt[200010], zu[200010], ca[200010];

int par[E + 10][100010];
int dep[100010];
int dists[100010];

void dfs(int u, int p, int depth, int dist) {
	par[0][u] = p;
	dep[u] = depth;
	dists[u] = dist;
	for (int i = ptr[u]; ~i; i = nxt[i]) {
		const int v = zu[i];
		if (v != p) {
			dfs(v, u, depth + 1, dist + ca[i]);
		}
	}
}

int LCA(int u, int v) {
	if (dep[u] > dep[v])
		swap(u, v);
	for (int e = E; e--; )
		if (dep[u] <= dep[v] - (1 << e))
			v = par[e][v];
	for (int e = E; e--; )
		if (par[e][u] != par[e][v]) {
			u = par[e][u];
			v = par[e][v];
		}
	if (u != v) {
		u = par[0][u];
		v = par[0][v];
	}
	return u;
}

int gpar[E + 10][100010];

int oneDay(int strength, int u) {
	int v = u;
	for (int e = E; e--; ) {
		if (dists[u] - dists[par[e][v]] <= strength) {
			v = par[e][v];
		}
	}
	return v;
}

void doIt(int strength) {
// cout<<"strength = "<<strength<<endl;
	for (int u = 0; u < N; ++u) {
		gpar[0][u] = oneDay(strength, u);
	}
// cout<<"  gpar[0] : ";pv(gpar[0],gpar[0]+N);
	for (int e = 1; e < E; ++e) {
		for (int u = 0; u < N; ++u) {
			gpar[e][u] = gpar[e - 1][ gpar[e - 1][u] ];
		}
	}
}

pint days(int strength, int t, int u) {
	if (u == t) {
		return mp(0, 0);
	}
	int ret = 0;
	for (int e = E; e--; ) {
		if (dep[t] < dep[gpar[e][u]]) {
			u = gpar[e][u];
			ret |= 1 << e;
		}
	}
	return mp(ret, dists[u] - dists[t]);
}

pint daysNaive(int strength, int t, int u) {
	int ret = 0;
	for (; ; ) {
		const int v = oneDay(strength, u);
		if (dep[t] >= dep[v]) {
			return mp(ret, dists[u] - dists[t]);
		}
		u = v;
		++ret;
	}
}

pint queries[100010];
int ans[100010];

int main() {

	freopen("tree.in", "r", stdin);
	freopen("tree.out", "w", stdout);

	for (; ~scanf("%d", &N); ) {
		for (int i = 0; i < N - 1; ++i) {
			X[i] = in() - 1;
			Y[i] = in() - 1;
			D[i] = in();
		}
		Q = in();
		for (int q = 0; q < Q; ++q) {
			S[q] = in() - 1;
			T[q] = in() - 1;
			P[q] = in();
		}
		m = 0;
		fill(ptr, ptr + N, -1);
		for (int i = 0; i < N - 1; ++i) {
			const int u = X[i];
			const int v = Y[i];
			nxt[m] = ptr[u];
			ptr[u] = m;
			zu[m] = v;
			ca[m] = D[i];
			++m;
			nxt[m] = ptr[v];
			ptr[v] = m;
			zu[m] = u;
			ca[m] = D[i];
			++m;
		}
		dfs(0, -1, 0, 0);
// cout<<"par[0] : ";pv(par[0],par[0]+N);
// cout<<"dep : ";pv(dep,dep+N);
// cout<<"dists : ";pv(dists,dists+N);
		par[0][0] = 0;
		for (int e = 1; e < E; ++e) {
			for (int u = 0; u < N; ++u) {
				par[e][u] = par[e - 1][ par[e - 1][u] ];
			}
		}

		for (int q = 0; q < Q; ++q) {
			queries[q] = mp(P[q], q);
		}
		sort(queries, queries + Q);
		int countSmall = 0;
		for (int qi = 0, qj; qi < Q; qi = qj) {
			for (qj = qi; qj < Q && queries[qi].first == queries[qj].first; ++qj);
			doIt(queries[qi].first);
			for (int qk = qi; qk < qj; ++qk) {
				const int q = queries[qk].second;
// cout<<"query "<<S[q]<<" "<<T[q]<<" "<<P[q]<<endl;
				const int l = LCA(S[q], T[q]);
				const pint resS = days(P[q], l, S[q]);
				const pint resT = days(P[q], l, T[q]);
// cout<<"  "<<resS.first<<" "<<resS.second<<"  "<<resT.first<<" "<<resT.second<<endl;
				const int left = resS.second + resT.second;
				ans[q] = resS.first + resT.first + ((left == 0) ? 0 : (left <= P[q]) ? 1 : 2);
			}
			if (++countSmall >= LIM_SMALL) {
				for (int qk = qi; qk < Q; ++qk) {
					const int q = queries[qk].second;
// cout<<"query "<<S[q]<<" "<<T[q]<<" "<<P[q]<<endl;
					const int l = LCA(S[q], T[q]);
					const pint resS = daysNaive(P[q], l, S[q]);
					const pint resT = daysNaive(P[q], l, T[q]);
// cout<<"  "<<resS.first<<" "<<resS.second<<"  "<<resT.first<<" "<<resT.second<<endl;
					const int left = resS.second + resT.second;
					ans[q] = resS.first + resT.first + ((left == 0) ? 0 : (left <= P[q]) ? 1 : 2);
				}
				break;
			}
		}

		for (int q = 0; q < Q; ++q) {
			printf("%d\n", ans[q]);
		}
	}

	return 0;
}

