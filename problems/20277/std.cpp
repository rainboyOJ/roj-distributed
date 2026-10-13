#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <string>
#include <vector>
using namespace std;

const int INF = ~0U >> 1;

int n;
const int MAX_N = int(1e5) + 10;

int a[MAX_N];
int dp[MAX_N], pre[MAX_N];

struct Tree {
	Tree *pl, *pr;
	int l, r;

	pair<int, int> mxv, miv;

	void update() {
		mxv = max(pl->mxv, pr->mxv);
		miv = min(pl->miv, pr->miv);
	}

	Tree(int l, int r) :
		l(l), r(r) {
		if (l + 1 == r) {
			mxv = miv = make_pair(a[l], l);
			return;
		}
		pl = new Tree(l, l + r >> 1);
		pr = new Tree(l + r >> 1, r);
		update();
	}

	pair<int, int> queryMax(int L, int R) {
		if (L <= l && R >= r) {
			return mxv;
		}
		if (L >= r || l >= R)
			return make_pair(-INF, 0);
		return max(pl->queryMax(L, R), pr->queryMax(L, R));
	}

	pair<int, int> queryMin(int L, int R) {
		if (L <= l && R >= r) {
			return miv;
		}
		if (L >= r || l >= R)
			return make_pair(INF, 0);
		return min(pl->queryMin(L, R), pr->queryMin(L, R));
	}

	int findLastGreater(int L, int R, int x) {
		if (L <= l && R >= r) {
			if (mxv.first <= x)
				return -1;
			if (l + 1 == r)
				return l;
			int ret = pr->findLastGreater(L, R, x);
			if (ret == -1)
				return pl->findLastGreater(L, R, x);
			else
				return ret;
		}
		if (L >= r || l >= R)
			return -1;
		int ret = pr->findLastGreater(L, R, x);
		if (ret == -1)
			return pl->findLastGreater(L, R, x);
		else
			return ret;
	}

	int findLastSmaller(int L, int R, int x) {
		if (L <= l && R >= r) {
			if (miv.first >= x)
				return -1;
			if (l + 1 == r)
				return l;
			int ret = pr->findLastSmaller(L, R, x);
			if (ret == -1)
				return pl->findLastSmaller(L, R, x);
			else
				return ret;
		}
		if (L >= r || l >= R)
			return -1;
		int ret = pr->findLastSmaller(L, R, x);
		if (ret == -1)
			return pl->findLastSmaller(L, R, x);
		else
			return ret;
	}
} *rt;

int main() {
	freopen("seq.in", "r", stdin);
	freopen("seq.out", "w", stdout);
	scanf("%d", &n);
	for (int i = 0; i < n; ++i) {
		scanf("%d", a + i);
	}

	rt = new Tree(0, n);
	memset(dp, 0, sizeof dp);

	dp[0] = 1, pre[0] = -1;

	for (int i = 1; i < n; ++i) {

		dp[i] = INF;

		int me = a[i];

		int at = rt->findLastGreater(0, i, me) + 1;
		if (at < i) {
			int can = rt->queryMin(at, i).second;
			if (dp[can] + 1 < dp[i]) {
				dp[i] = dp[can] + 1;
				pre[i] = can;
			}
		}

		at = rt->findLastSmaller(0, i, me) + 1;
		if (at < i) {
			int can = rt->queryMax(at, i).second;
			if (dp[can] + 1 < dp[i]) {
				dp[i] = dp[can] + 1;
				pre[i] = can;
			}
		}
	}

	cout << dp[n - 1] << endl;

}
