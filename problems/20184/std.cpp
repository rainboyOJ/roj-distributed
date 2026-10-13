#include <cassert>
#include <bits/stdc++.h>

const int N = 3e5 + 50;

int x[N], f[N], pre[N][2], suf[N][2];

inline int find(int x) {
	while (x != f[x])
		x = f[x] = f[f[x]];
	return x;
}

void push(int *A, int i, const auto &cmp) {
	if (!i) return;
	int fA0 = find(A[0]);
	int fA1 = find(A[1]);
	int fi = find(i);
	assert(A[0] == 0 || A[1] == 0 || fA0 != fA1);
	if (A[0] == 0 || cmp(x[A[0]], x[i])) {
		if (fi == fA0) {
			A[0] = i;
		}
		else {
			A[1] = A[0];
			A[0] = i;
		}
	}
	else if (A[1] == 0 || cmp(x[A[1]], x[i])) {
		if (fi != fA0) {
			A[1] = i;
		}
	}
}


void push_max(int *A, int i) {
	push(A, i, std::less<int>());
}
void push_min(int *A, int i) {
	push(A, i, std::greater<int>());
}
int take(int *A, int i) {
	if (find(i) != find(A[0]))
		return A[0];
	return A[1];
}
int val(int i, int j) {
	if (i > j) std::swap(i, j);
	return x[j] - x[i];
}

int to[N], to_v[N];
int64_t solve() {
	int n;
	std::cin >> n;
	for (int i = 1; i <= n; ++i) {
		std::cin >> x[i];
		f[i] = i;
	}
	int comp = n;
	int64_t ans = 0;
	while (comp > 1) {
		for (int i = 0; i <= n + 1; ++i) {
			pre[i][1] = pre[i][0] = suf[i][0] = suf[i][1] = 0;
		}
		for (int i = 1; i <= n; ++i) {
			if (i != 1) {
				push_max(pre[i], pre[i - 1][0]);
				push_max(pre[i], pre[i - 1][1]);
			}
			push_max(pre[i], i);
		}
		for (int i = n; i >= 1; --i) {
			if (i != n) {
				push_min(suf[i], suf[i + 1][0]);
				push_min(suf[i], suf[i + 1][1]);
			}
			push_min(suf[i], i);
		}
		for (int i = 1; i <= n; ++i) {
			to[i] = 0;
			to_v[i] = 2e9 + 50;
		}
		for (int i = 1; i <= n; ++i) {
			int pre_max = take(pre[i], i), pv = val(pre_max, i);
			int suf_min = take(suf[i], i), sv = val(suf_min, i);
			int o = find(i);
			assert(find(pre_max) != i);
			assert(find(suf_min) != i);
			if (pre_max && pv < to_v[o]) {
				to_v[o] = pv;
				to[o] = pre_max;
			}
			if (suf_min && sv < to_v[o]) {
				to_v[o] = sv;
				to[o] = suf_min;
			}
		}
		for (int i = 1; i <= n; ++i)
			if (i == find(i) && find(i) != find(to[i])) {
				--comp;
				ans += to_v[i];
				f[find(i)] = find(to[i]);
			}
	}
	return ans;
}

int main() {
	std::ios::sync_with_stdio(false);
	std::cin.tie(nullptr);
	std::cout.tie(nullptr);
	int t=1;
	while (t--) {
		std::cout << solve() << '\n';
	}
}
