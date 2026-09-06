#include <cstdio>
#include <algorithm>
using namespace std; 
#define ll long long
#define eps 1e-3
int n;
ll k;
int a[100005], c[100005];
double p[100005], q[100005];

bool cmp(double a, double b){
	return a < b;
} 

int check(double v){
    ll tot = 0;
	for(int i = 1;i <= n;i++){
		double x = a[i] * 1.0 * c[i], y = v * a[i]; 
		p[i] = x - y;
		q[i] = y - x; 
		if(q[i] - p[i] < eps) tot--;
	}
	sort(p + 1, p + n + 1, cmp);
	sort(q + 1, q + n + 1, cmp);
	int j = 0;
	for(int i = 1;i <= n;i++){
		while((q[j + 1] - p[i]) < eps && j + 1 <= n) j++;
		tot += j;
	}
	return (tot / 2 < k);
}

int main(){
	scanf("%d%lld", &n, &k);
	for(int i = 1 ; i <= n ; i++){
		scanf("%d%d", &a[i], &c[i]);
	}
	double l = 1,r = 1000000000,mid;
	while((r - l) > eps){
		mid = (l + r) / 2;
		if(check(mid)){
			r = mid;
		}
        else{
			l = mid;
		}
	}
	printf("%.3f\n", l);
	return 0;
}