#include<bits/stdc++.h>
using namespace std;
const int N=1<<12|5,MOD=998244353;
inline void mo(int& x){ x>=MOD?x-=MOD:0; }
inline int mo1(int x){ return x>=MOD?x-MOD:x; }
int a[N],n,f[N][N],g[N],h[N][N],s;
int main(){
	int n,m,s; scanf("%d%d%d",&n,&m,&s);
	for(int i=1;i<=n;++i) scanf("%d",&a[i]);
	int ans=n;
	for(int i=1;i<=n;++i){
		g[i]=0;
		for(int j=1;j<i;++j){
			f[i][a[j]]=(1ll+g[j]+MOD-h[j-1][a[i]^a[j]^s])%MOD;
			mo(g[i]+=f[i][a[j]]);
		}
		mo(ans+=g[i]);
		for(int t=0;t<1<<m;++t)
			h[i][t]=(h[i-1][t]+f[i][a[i]^t])%MOD;
	}
	printf("%d\n",ans);
	return 0;
}