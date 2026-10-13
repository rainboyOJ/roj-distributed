#include <bits/stdc++.h>
#define inf 0x3f3f3f3f
#define LL long long
using namespace std;
int n,k;
struct seg { int l,r; } a[5005];
LL res;
void solve1() {
	sort(a+1,a+1+n,[](seg _,seg $){return _.r-_.l>$.r-$.l;});
	LL ans=0;
	for(int i=1;i<k;i++) ans+=a[i].r-a[i].l;
	int mx=-inf,mn=inf;
	for(int i=k;i<=n;i++) mx=max(mx,a[i].l),mn=min(mn,a[i].r);
	ans+=max(0,mn-mx);
	res=max(res,ans);
}
LL f[5005],g[5005]; int q[5005],h,t;
void solve2() {
	int m=0;
	sort(a+1,a+1+n,[](seg _,seg $){return (_.l==$.l)?(_.r>$.r):(_.l<$.l);});
	vector<LL>le{0};
	for(int i=1;i<=n;a[++m]=a[i],i++) while(m&&a[m].r>=a[i].r) le.push_back(a[m].r-a[m].l),m--;
	sort(le.begin(),le.end()); reverse(le.begin()+1,le.end()); while(le.size()<=k) le.push_back(0);
	for(int i=1;i<le.size();i++) le[i]+=le[i-1];
	for(int i=1;i<=m;i++) f[i]=-inf; f[0]=0;
	for(int T=1;T<=min(m,k);T++) {
		for(int i=0;i<=m;i++) g[i]=-inf;
		for(int i=1;i<=m;i++) f[i-1]+=a[i].r;
		h=1,t=0;
		for(int i=1;i<=m;i++) {
			while(h<=t&&a[q[h]+1].r<=a[i].l) h++;
			while(h<=t&&f[q[t]]<f[i-1]) t--; q[++t]=i-1;
			g[i]=f[q[h]]-a[i].l;
		} res=max(res,g[m]+le[k-T]);
		for(int i=0;i<=m;i++) f[i]=g[i];
	}
}
int main() {
	scanf("%d%d",&n,&k); k=min(n,k);
	for(int i=1;i<=n;i++) scanf("%d%d",&a[i].l,&a[i].r);
	solve1();
	solve2();
	printf("%lld\n",res);
}