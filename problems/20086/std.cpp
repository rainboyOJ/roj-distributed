#include <bits/stdc++.h>
using namespace std;

void solve() {
	int n, s, t;
	cin >> n >> s >> t;
	vector<int> vis(2 * n + 1);
	for (int i = 1; i <= n; i++) {
		int x;
		cin >> x;
		vis[i] = vis[x] = i;
	}
	if (s == t) {
		cout << "Yes\n";
		return;
	}
	if ((s <= n && t <= n) || (s > n && t > n)) {
		if (n <= 2) cout << "No\n";
		else cout << "Yes\n";
	} else {
		if (vis[s] != vis[t]) cout << "Yes\n";
		else cout << "No\n";
	}
}

int main() {
	ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
	int T;
	cin >> T;
	while (T--) solve();
	return 0;
}