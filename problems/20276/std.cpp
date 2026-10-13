#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <string>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int dp[20][20000];

void addIt(int &x, int c) {
	x += c;
	if (x >= MOD)
		x -= MOD;
}

int main() {
	freopen("and.in", "r", stdin);
	freopen("and.out", "w", stdout);
	int T;
	int n, k;
	cin >> k >> n;
	memset(dp, 0, sizeof dp);
	dp[0][0] = 1;
	for (int bit = 0; bit < 15; ++bit) {
		int sum = 0;
		for (int num = 0; num <= k; ++num) {
			for (int j = 0; j + sum <= n; ++j) {
				addIt(dp[bit + 1][j + sum], dp[bit][j]);
			}
			sum += 1 << bit;
			if (sum > n)
				break;
		}
	}
	cout << dp[15][n] << endl;
}
