/*
*/

//#pragma comment(linker, "/STACK:16777216")
#include <fstream>
#include <iostream>
#include <string>
#include <complex>
#include <math.h>
#include <set>
#include <vector>
#include <map>
#include <queue>
#include <stdio.h>
#include <stack>
#include <algorithm>
#include <list>
#include <ctime>
#include <memory.h>
#include <ctime>

#define y0 sdkfaslhagaklsldk
#define y1 aasdfasdfasdf
#define yn askfhwqriuperikldjk
#define j1 assdgsdgasghsf
#define tm sdfjahlfasfh
#define lr asgasgash

#define eps 1e-11
//#define M_PI 3.141592653589793
#define bs 1000000007
#define bsize 256
#define right adsgasgadsg
#define free adsgasdg

using namespace std;

long tests, n, m, l, r, ans[10000005], ttl;
long answ;
long prec[10000005];
long mem[10000005];

long long pw(long long a, long long b) {
	if (b == 0)
		return 1;
	if (b % 2)
		return a * pw(a, b - 1) % bs;
	return pw(a * a % bs, b / 2);
}

void ad(long &a, long &b) {
	a += b;
	if (a >= bs)
		a -= bs;
}

int main() {
	freopen("gcd.in", "r", stdin);
	freopen("gcd.out", "w", stdout);
	ios_base::sync_with_stdio(0);
	tests = 1;
	for (; tests; --tests) {
		cin >> n >> m >> l >> r;
		for (int i = m; i; --i) {
			ans[i] = 0;
			for (int j = i * 2; j <= m; j += i) {
				ans[i] += bs;
				ans[i] -= ans[j];
				if (ans[i] >= bs)
					ans[i] -= bs;
			}
			ttl = m / i;
			if (prec[ttl] == n)
				ans[i] += mem[ttl];
			else {
				long q = pw(ttl, n);
				ans[i] += q;
				prec[ttl] = n;
				mem[ttl] = q;
			}
			if (ans[i] >= bs)
				ans[i] -= bs;
		}
		answ = 0;
		for (int i = l; i <= r; i++)
			ad(answ, ans[i]);
		cout << answ << endl;
	}
	cin.get();
	cin.get();
	return 0;
}
