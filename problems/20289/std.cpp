#include <algorithm>
#include <cstdio>
using namespace std;
typedef long long ll;
const int maxn = 2e5 + 100;
int val[maxn], q[maxn], mi[maxn], mx[maxn], n, k;
ll ans1, ans2;

inline void init() {
	int head = 0, tail = 0;
	for (int i = 1; i < k; i++) {
		while (head <= tail && val[q[tail]] >= val[i])
			tail--;
		q[++tail] = i;
	}
	for (int i = k; i <= n; i++) {
		while (head <= tail && val[q[tail]] >= val[i])
			tail--;
		q[++tail] = i;
		while (head <= tail && q[head] <= i - k)
			head++;
		mi[i - k + 1] = val[q[head]];
	}
	head = 0, tail = 0;
	for (int i = 1; i < k; i++) {
		while (head <= tail && mi[q[tail]] <= mi[i])
			tail--;
		q[++tail] = i;
		mx[i] = mi[q[head]];
		ans1 += mx[i];
	}
	for (int i = k; i <= n; i++) {
		while (head <= tail && mi[q[tail]] <= mi[i])
			tail--;
		q[++tail] = i;
		while (head <= tail && q[head] <= i - k)
			head++;
		mx[i] = mi[q[head]];
		ans1 += mx[i];
	}
}

int main() {
	freopen("fence.in", "r", stdin);
	freopen("fence.out", "w", stdout);
	scanf("%d %d", &n, &k);
	for (int i = 1; i <= n; i++)
		scanf("%d", val + i);
	init();
	printf("%lld\n", ans1);
	int v = -1, rt = -1;
	for (int i = 1; i <= n; i++)
		if (mx[i] != v || rt < i) {
			ans2++;
			v = mx[i];
			rt = i + k - 1;
		}
	printf("%lld\n", ans2);
	return 0;
}