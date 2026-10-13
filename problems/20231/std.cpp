#include <bits/stdc++.h>
using namespace std;

string mul(string a, int b) {
	string c;
	for (int i = 0; i < b; i++)
		c += a;
	return c;
}
string mx, mn;

int main() {
	freopen("binary.in", "r", stdin);
	freopen("binary.out", "w", stdout);
	int T;
	scanf("%d", &T);
	while (T--) {
		int n, m;
		scanf("%d%d", &n, &m);
		if (n <= 1 || (n % 2 == 1 && m <= 1)) {
			mx = "-1";
			mn = "-1";
		} else {
			if (n % 2 == 0)
				mx = mul("1", n) + mul("0", m);
			else
				mx = mul("1", n - 2) + "0101" + mul("0", m - 2);
			if (n % 2 == 0)
				mn = "1" + mul("0", m / 2 * 2) + "1" + mul("0", m % 2) + mul("1", n - 2);
			else
				mn = "1" + mul("0", m / 2 * 2 - 1) + "101" + mul("0", m % 2) + mul("1", n - 3);
		}
		printf("%s\n%s\n", mx.c_str(), mn.c_str());
	}
}
