#include <bits/stdc++.h>

std::unordered_set<int64_t> set;
std::vector<int64_t> b;

void dfs(int64_t n) {
	if (set.count(n)) return;
	set.insert(n);
	for (auto x : b)
		dfs(n / x);
}

int main() {
	freopen("set.in", "r", stdin);
	freopen("set.out", "w", stdout);
	std::ios::sync_with_stdio(false);
	int64_t n;
	int m;
	std::cin >> n >> m;
	b.resize(m);
	for (int i = 0; i < m; ++i)
		std::cin >> b[i];
	dfs(n);
	std::cout << set.size() << '\n';
}