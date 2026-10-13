#include <set>
#include <map>
#include <cmath>
#include <queue>
#include <bitset>
#include <string>
#include <cstdio>
#include <cctype>
#include <cassert>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <iostream>
#include <algorithm>

#define For(i,x,y) for (int i=x;i<y;i++)
#define pb push_back
#define mp make_pair
#define fi first
#define se second
#define lf else if

#define dprintf(...) fprintf(stderr,__VA_ARGS__)
using namespace std;

typedef long long ll;
typedef double db;
typedef pair<int, int> pii;
typedef vector<int> Vi;

int IN() {
	int c, f, x;
	while (!isdigit(c = getchar()) && c != '-')
		;
	c == '-' ? (f = 1, x = 0) : (f = 0, x = c - '0');
	while (isdigit(c = getchar()))
		x = (x << 1) + (x << 3) + c - '0';
	return !f ? x : -x;
}

const int N = 1e6 + 19;

char s[N];
int dp[N][2];
int n;

int main() {
	freopen("mul.in", "r", stdin);
	freopen("mul.out", "w", stdout);
	scanf("%s", s + 1);
	n = strlen(s + 1);
	dp[n + 1][1] = 2;
	for (int i = n; i; i--) {
		if (s[i] == '0') {
			dp[i][0] = min(dp[i + 1][0], dp[i + 1][1] + 4);
			dp[i][1] = min(dp[i + 1][1] + 2, dp[i + 1][0] + 2);
		} else {
			dp[i][0] = min(dp[i + 1][0] + 2, dp[i + 1][1] + 2);
			dp[i][1] = min(dp[i + 1][1], dp[i + 1][0] + 4);
		}
	}
	printf("%d\n", dp[1][0] - 1);
}