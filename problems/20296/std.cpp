#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
template <typename T>

inline void read(T &x) {
	char c = getchar();
	int w = 1;
	x = 0;
	while (!isdigit(c))
		(c == '-') && (w = -w), c = getchar();
	while (isdigit(c))
		x = (x << 1) + (x << 3) + (c ^ '0'), c = getchar();
	x *= w;
}

const int N = 10010;
char s[N], t[N];
int ans = 0;

signed main() {
	freopen("type.in", "r", stdin);
	freopen("type.out", "w", stdout);
	scanf("%s", s + 1);
	scanf("%s", t + 1);
	int lena = strlen(s + 1), lenb = strlen(t + 1);
	int p1 = 1;
	while (p1 + lenb - 1 <= lena) {
		bool flag = true;
		for (int i = p1; i <= p1 + lenb - 1 && flag; ++i) {
			if (s[i] != t[i - p1 + 1])
				flag = false;
		}
		if (!flag) {
			++ ans;
			++ p1;
			continue;
		}
		p1 = p1 + lenb;
		++ ans;
	}
	cout << ans + (lena - p1 + 1) << endl;
	return 0;
}