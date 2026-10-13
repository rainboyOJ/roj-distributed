#include <bits/stdc++.h>
using namespace std;
inline int read(){
	int s=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9')s=(s<<3)+(s<<1)+ch-'0',ch=getchar();
	return s*f;
}
const int N=3e3+5,mod=998244353;
inline int add(int a,int b){return (a+b>=mod)?a+b-mod:a+b;}
int f[N][N],sum[N][N];
vector<int> e[N];
#define pb push_back
int n,dep[N],ans=1;
void dfs(int u,int fa){
	dep[u]=dep[fa]+1;
	for(int i=1;i<dep[u];++i)f[u][i]=1;
	for(int v:e[u]){
		if(v==fa)continue;
		dfs(v,u);
		for(int i=1;i<dep[u];++i)
			f[u][i]=1ll*f[u][i]*sum[v][i+1]%mod;
		if(!fa)ans=1ll*ans*f[v][1]%mod;
	}
	for(int i=1;i<dep[u];++i)
		sum[u][i]=add(sum[u][i-1],f[u][i]);
}
int main(){
	freopen("reflection.in","r",stdin);
	freopen("reflection.out","w",stdout);
	n=read();
	for(int i=1,u,v;i<n;++i){
		u=read();v=read();
		e[u].pb(v);e[v].pb(u);
	}
	dfs(n,0);
	printf("%d\n",ans);
	return 0;
}