#include <cstdio>
#include <algorithm>

#define N 5010
#define INF 1000000010
using namespace std;
int n, k;
int a[N];
int v[N], dp[N];
// v[i] : dp[j] >= i 的最小 j
int main(){
	scanf("%d%d", &k, &n);
	for(int i = 1 ; i <= n ; i++) v[i] = INF;
	for(int i = 1 ; i <= n ; i++){
		for(int j = 1 ; j <= k ; j++) scanf("%d", &a[j]);
		int p = 0;
		for(int j = 1 ; j <= k ; j++){
			while(p + 1 <= n && v[p + 1] < a[j]) p++;
			dp[j] = p + 1;
		}
		for(int j = 1 ; j <= k ; j++) v[dp[j]] = min(v[dp[j]], a[j]);
	}
	for(int j = n ; j >= 1 ; j--){
		if(v[j] != INF){
			printf("%d\n", j);
			return 0;
		}
	}
	return 0;
}