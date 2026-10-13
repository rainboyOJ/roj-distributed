#include <cstdio>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <stack>
#include <queue>
#include <algorithm>
#include <cmath>
#include <string>
#include <cstdlib>
#include <climits>
#include <cstring>
#include <cassert>
using namespace std;

#define CLR(a,x) memset(a,x,sizeof(a))
#define PB push_back
#define INF 1000000000
#define MOD 1000000007
#define MP make_pair
#define tr(container , it) for(typeof(container.begin()) it=container.begin() ; it!=container.end() ; it++)
#define FOR(i,a,b) for(i=a;i<b;i++)
#define REP(i,a) FOR(i,0,a)
#define LL long long
#define VI vector < LL >
#define PII pair < LL , LL >


void precompute(void) {
}
queue < LL > Q[2], rem;
set < LL > S;
set < LL >::iterator it1, it2;
LL top, val[1 << 20], len, cur, nx1, pre1, nx;
LL ans;
string str;
LL BIT[1 << 20];

LL query(LL x) {
	x += 5;
	LL ret = 0;
	while (x) {
		ret += BIT[x];
		x -= (x & (-x));
	}
	return ret;
}

void update(LL x, LL val) {
	x += 5;
	while (x < (1 << 18)) {
		BIT[x] += val;
		x += (x & (-x));
	}
}


int main() {
	freopen("lucky.in", "r", stdin);
	freopen("lucky.out", "w", stdout);
	precompute();
	cin >> len >> str;
	S.clear();
	for (LL i = 0; i < len; i++) {
		S.insert(i);
		if (i < len - 1 && str[i] == '4' && str[i + 1] == '7') {
			Q[0].push(i);
		}
	}
	ans = 0LL;
	cur = 0;
	while (!(Q[cur].empty() && Q[1 - cur].empty())) {
		if (Q[cur].empty()) {
			while (!rem.empty()) {
				top = rem.front();
				rem.pop();
				val[top] = 1;
				update(top, 1);
			}
			cur = 1 - cur;
		}
		top = Q[cur].front();
		Q[cur].pop();
		nx = *(S.lower_bound(top + 1));
		assert(S.find(top) != S.end() && S.lower_bound(top + 1) != S.end());

		it1 = S.lower_bound(top);
		if (it1 != S.begin()) {
			it1--;
			it2 = S.lower_bound(nx + 1);
			if (it2 != S.end()) {
				pre1 = *it1;
				nx1 = *it2;
				if (str[pre1] == '4' && str[nx1] == '7') {
					Q[1 - cur].push(pre1);
				}
			}
		}
		S.erase(top);
		S.erase(nx);

		ans += (LL)(top  + 1 - query(top - 1));
		rem.push(top);
		rem.push(nx);
	}
	while (!rem.empty())
		rem.pop();
	for (LL i = 0; i < len; i++) {
		update(i, -val[i]);
		val[i] = 0;
	}
	cout << ans << endl;
	return 0;
}

