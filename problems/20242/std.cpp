#include <cstdio>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <cstring>
#include <cmath>
#include <string>
#include <vector>
#include <queue>
#include <deque>
#include <stack>
#include <list>
#include <map>
#include <set>
#include <bitset>
#include <cstdlib>
#include <ctime>
using namespace std;

#define lson l, mid, rt << 1
#define rson mid + 1, r, rt << 1 | 1
typedef long long ll;
const int MAXN = 2e6 + 10;
const int INF = 0x3f3f3f3f;
const int MOD = 1e9 + 7;

int n, c;
int buy[MAXN * 2], sell[MAXN * 2];
int a[MAXN];
struct P {
	int val, num;
} q[MAXN];
ll ans;
int l, r;
int cnt;

void MAX(int x) {
	//把所有买的价格小于x的油都用x卖出
	int sum = 0;
	while (l <= r && x > q[l].val) {
		sum += q[l].num;
		l++;
	}
	if (sum) {
		q[--l].num = sum;
		q[l].val = x;
	}
}

void MIN(int x) {
	//把所有卖的价格大于x的油都用x买入
	while (l <= r && x < q[r].val) {
		ans -= 1ll * q[r].val * q[r].num;
		cnt += q[r].num;
		r--;
	}
}

int DEL(int x) {
	//路上所要消耗的�?
	while (x) {
		int v = min(x, q[l].num);
		q[l].num -= v;
		x -= v;
		if (q[l].num == 0)
			l++;
	}
}

int main() {
	freopen("candy.in", "r", stdin);
	freopen("candy.out", "w", stdout);
	scanf("%d%d", &n, &c);
	for (int i = 1; i <= n; i++)
		scanf("%d", &a[i]);
	for (int i = 0; i <= n; i++)
		scanf("%d%d", &buy[i], &sell[i]);
	ans = 0;
	l = r = n;
	r--;
	for (int i = 0; i < n; i++) {
		MAX(sell[i]);
		cnt = (i == 0 ? c : a[i] - a[i - 1]); //所需要的�?
		MIN(buy[i]);
		r++;
		q[r].val = buy[i];
		q[r].num = cnt;
		ans += 1ll * cnt * buy[i];//把油装满所需要的�?
		DEL(a[i + 1] - a[i]);
	}
	MAX(sell[n]);
	for (int i = l; i <= r; i++)
		ans -= 1ll * q[i].val * q[i].num;
	printf("%lld\n", ans);
}