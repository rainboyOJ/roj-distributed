#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 5;

int n, k, p;
char s[N], t[N];
void solve() {
	scanf("%s %s %d", s + 1, t + 1, &k), n = strlen(s + 1), p = 0;
	for(int i = 1, pr = 0; i <= n; i++) {
		if(t[i] - '0') {
			if(s[i] < t[i] && pr <= k && n - i >= k - pr) p = i;
			if((t[i] > '1' || s[i] > '0') && pr + 1 <= k && n - i >= k - pr - 1) p = i;
		} pr += s[i] != t[i];
	} if(!p) return puts("-1"), void();
	for(int i = 1, out; i <= n; i++) {
		if(i < p) out = t[i];
		else if(!k) out = s[i];
		else if(i == p) out = t[i] - 1 - (s[i] + 1 == t[i] && n - i + 1 == k);
		else out = '9' - (n - i + 1 == k && s[i] == '9');
		putchar(out), k -= out != s[i];
	} cout << endl;
}
int main() {
	int T; cin >> T; while(T--) solve();
	return 0;
}
