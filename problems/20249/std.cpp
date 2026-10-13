#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <vector>
#define SIZE 100005
#define INF 1000000000

using namespace std;

int in[SIZE], diff[SIZE];
int sum[SIZE], now[SIZE];
int n;

int main() {
	freopen("seq.in", "r", stdin);
	freopen("seq.out", "w", stdout);
	int T = 1;
	while (T--) {
		scanf("%d", &n);
		for (int i = 0; i < n; i++)
			scanf("%d", &in[i]);
		int ret = 0;
		for (int i = 0; i < n; i++) {
			int a;
			scanf("%d", &a);
			in[i] = (4 + a - in[i]) % 4;
			int d = in[i];
			if (i > 0) {
				d += 4 - in[i - 1];
				d %= 4;
			}
			diff[i] = d;
			ret += d;
			sum[i] = ret;
		}
		for (int j = 3; j >= 0; j--) {
			for (int i = n - 1; i >= 0; i--) {
				now[i] = sum[i];
				if (i + 1 < n)
					now[i] = min(now[i], now[i + 1]);
			}
			int mn = 0;
			for (int i = 0; i < n; i++) {
				sum[i] -= mn;
				if (diff[i] == j && now[i] >= mn + 4) {
					sum[i] -= 4;
					ret -= j;
					mn += 4;
				}
			}
		}
		printf("%d\n", ret);
	}
	return 0;
}
