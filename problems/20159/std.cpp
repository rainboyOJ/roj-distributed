#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=1e6+5;
const ll inf=1e18;
int n;
ll a[N],b[N],f[N];
signed main(){
    freopen("alice.in","r",stdin);
    freopen("alice.out","w",stdout);
	scanf("%d",&n);fill_n(f+1,n,inf);
	for(int i=1;i<=n;i++) scanf("%lld",&a[i]);
	for(int i=1;i<=n;i++) scanf("%lld",&b[i]);
	for(int i=1;i<=n;i++){
		int x=upper_bound(f+1,f+n+1,a[i])-f-1;
		if(f[x]*b[x]<a[i]) f[x+1]=a[i];
	}
	for(int i=n;i;i--)
		if(f[i]!=inf) return printf("%d\n",i),0;
}