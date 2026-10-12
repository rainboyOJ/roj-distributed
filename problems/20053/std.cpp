#include <iostream>
#include <cstdio>
#include <algorithm>
using namespace std;
const int N = 1e6 + 5;
int n, c;
int a[N];
int cnt[N];
int sum[N];
long long c2(int x) {
	if(x <= 1) {
		return 0;
	}
    return (long long)x * (x - 1) / 2;
}
long long c3(int x) {
    if(x <= 2) {
        return 0;
    }
    return (long long)x * (x - 1) * (x - 2) / 6;
}
int main() {
    scanf("%d%d", &n, &c);
    for(int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
        cnt[a[i]]++;
    }
    int li = c / 2;
    long long ans = 0;
    int now = 0;
    for(int i = 1; i <= li; i++) {
        now += cnt[i];
    }
    if(c % 2 == 0) {
    	for(int i = 0; i < c; i++) {
        	ans += (long long)cnt[i] * c2(now);
        	ans += (long long)c2(cnt[i]) * (now - cnt[(i + li) % c]);
        	now -= cnt[(i + 1) % c];
        	now += cnt[(i + li + 1) % c];
    	}
	} else {
		for(int i = 0 ; i < c; i++) {
			ans += (long long)cnt[i] * c2(now);
			ans += (long long)c2(cnt[i]) * now;
			now -= cnt[(i + 1) % c];
			now += cnt[(i + li + 1) % c];
		}
	}
    for(int i = 0; i < c; i++) {
        ans += c3(cnt[i]);
    }
    long long sum = c3(n);
    printf("%lld\n", sum - ans);
    return 0;
}
