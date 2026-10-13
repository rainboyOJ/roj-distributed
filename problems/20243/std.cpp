#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <vector>
#include <iomanip>
#define ALL(x) (x).begin(), (x).end()
#define rt return
#define dll(x) scanf("%I64d",&x)
#define xll(x) printf("%I64d\n",x)
#define sz(a) int(a.size())
#define all(a) a.begin(), a.end()
#define rep(i,x,n) for(int i=x;i<n;i++)
#define repd(i,x,n) for(int i=x;i<=n;i++)
#define pii pair<int,int>
#define pll pair<long long ,long long>
#define gbtb ios::sync_with_stdio(false),cin.tie(0),cout.tie(0)
#define MS0(X) memset((X), 0, sizeof((X)))
#define MSC0(X) memset((X), '\0', sizeof((X)))
#define pb push_back
#define mp make_pair
#define fi first
#define se second
#define eps 1e-6
#define gg(x) getInt(&x)
#define db(x) cout<<"== [ "<<x<<" ] =="<<endl;
using namespace std;
typedef long long ll;

ll gcd(ll a, ll b) {
	return b ? gcd(b, a % b) : a;
}

ll lcm(ll a, ll b) {
	return a / gcd(a, b) * b;
}

ll powmod(ll a, ll b, ll MOD) {
	ll ans = 1;
	while (b) {
		if (b % 2)
			ans = ans * a % MOD;
		a = a * a % MOD;
		b /= 2;
	}
	return ans;
}
inline void getInt(int *p);
const int maxn = 100010;
const int inf = 0x3f3f3f3f;
/*** TEMPLATE CODE * * STARTS HERE ***/
int t;
int n, m;
ll b[maxn];
int dp[maxn];
int num[maxn];

int c(int n, int m) {
	int sum = 1;
	for (int i = n - m + 1; i <= n; i++)
		sum *= i;
	for (int i = 1; i <= m; i++)
		sum /= i;
	return sum;
}

int main() {
	freopen("subset.in", "r", stdin);
	freopen("subset.out", "w", stdout);
	MS0(num);
	MS0(dp);
	scanf("%d%d", &n, &m);
	repd(i, 0, m) {
		scanf("%lld", &b[i]);
		// cin >> b[i];
	}
	num[0] = log2(b[0]);
	num[1] = b[1] / b[0];
	dp[0] = b[0];
	repd(i, 0, m) {
		for (int j = m; j >= 0; j--) {
			if (dp[j] == 0)
				continue;
			if (num[i] == 0)
				break;
			for (int k = 1; k <= num[i]; k++) {
				if (j + k * i <= m) {
					dp[j + k * i] += dp[j] * c(num[i], k);
				}
			}
		}
		if (i + 1 <= m) {
			num[i + 1] = (b[i + 1] - dp[i + 1]) / b[0];
		}
	}
	bool flag = 0;
	for (int i = 0; i <= m; i++) {
		for (int j = 1; j <= num[i]; j++) {
			if (!flag)
				printf("%d", i), flag = 1;
			else
				printf(" %d", i);
		}
	}
	puts("");

	return 0;
}

inline void getInt(int *p) {
	char ch;
	do {
		ch = getchar();
	} while (ch == ' ' || ch == '\n');
	if (ch == '-') {
		*p = -(getchar() - '0');
		while ((ch = getchar()) >= '0' && ch <= '9') {
			*p = *p * 10 - ch + '0';
		}
	} else {
		*p = ch - '0';
		while ((ch = getchar()) >= '0' && ch <= '9') {
			*p = *p * 10 + ch - '0';
		}
	}
}