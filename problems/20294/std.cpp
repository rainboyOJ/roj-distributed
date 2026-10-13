#include <cstdio>
#include <cstring>

const int MOD = 1e9 + 7;
inline int addmod(int a, int b) {
	return (a + b) % MOD;
}

const int MAXN = (1 << 22);

char str[MAXN];
int n;
int f[MAXN];
int ans;

void dfs(int l, int r) {
	if (l > n) {
		return;
	}
	if (l == r - 1) {
		ans = f[l];
		return;
	}
	int m = (l + r) / 2;
	int len = (r - l) / 2;
	dfs(l, m);
	for (int i = m; i < r; i++) {
		if (str[i] != '+') {
			f[i] = addmod(f[i], f[i - len]);
		}
	}
	dfs(m, r);
	for (int i = m; i < r; i++) {
		f[i] = addmod(f[i], f[i - len]);
	}
}

int main() {
	freopen("expr.in", "r", stdin);
	freopen("expr.out", "w", stdout);
	scanf("%s", str + 1);
	n = strlen(str + 1) + 1;
	int r = 1;
	while (r <= n) {
		r <<= 1;
	}
	for (int i = 1; i < r; i++) {
		f[i] = 0;
	}
	f[0] = 1;
	dfs(0, r);
	printf("%d %d\n", n, ans);
	return 0;
}