#include <bits/stdc++.h>
#define rep(i,a,b) for(int i=(a);i<=(b);++i)
#define dep(i,a,b) for(int i=(a);i>=(b);--i)
#define lowbit(x) (x&(-x))
#define debug(x) cout<<#x<<" :"<<x<<endl
#define debug1(x) cout<<#x<<" :"<<x<<" "
using namespace std;
typedef unsigned long long ull;
typedef long long ll;
const int N = 2e5 + 20;
const int MAX = 10000007;

inline int read() {
	char c = getchar();
	int x = 0, f = 1;
	while (c < '0' || c > '9') {
		if (c == '-')
			f = -1;
		c = getchar();
	}
	while (c >= '0' && c <= '9') {
		x = x * 10 + c - '0', c = getchar();
	}
	return x * f;
}

inline void out(int x) {
	if (x > 9)
		out(x / 10);
	putchar(x % 10 + '0');
}
int q[N];
int n;

int main() {
	freopen("palindrome.in", "r", stdin);
	freopen("palindrome.out", "w", stdout);
	int T = read();
	while (T--) {
		n = read();
		int sum = 0;
		int od = 0;
		rep(i, 1, n) {
			q[i] = read();
			if (q[i] & 1) {
				od++;
				sum += q[i] / 2;
			} else
				sum += q[i] / 2;
		}
		if (!od)
			printf("%d\n", sum * 2);
		else
			printf("%d\n", sum / od * 2 + 1);
	}
	return 0;
}
