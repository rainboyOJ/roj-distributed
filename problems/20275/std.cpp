#include <stdio.h>
#include <stdlib.h>
using namespace std;

int n, i, j, k;
int a[10005], f[10005];

int main() {
	freopen("tree.in", "r", stdin);
	freopen("tree.out", "w", stdout);
	scanf("%d", &n);
	for (i = 1; i < n; ++i)
		scanf("%d", &k), ++a[k];
	for (i = 2; i <= n; ++i)
		f[i] = 100000;
	for (i = 1; i <= n; ++i)
		if (a[i])
			for (j = n; j >= 1; --j)
				if (f[j] + 1 < f[j + a[i]])
					f[j + a[i]] = f[j] + 1;
	for (i = 1; i <= n; ++i) {
		if (f[i] <= n)
			printf("%d", f[i]);
		else
			printf("-1");
		if (i == n)
			printf("\n");
		else
			printf(" ");
	}
}