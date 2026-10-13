#include <bits/stdc++.h>
#define LL long long
using namespace std;
int n,m,a[100005],fa[100005],p[100005];
LL sm[100005],ans=0,res[100005];
int find(int x) { return fa[x]==x ? x : fa[x]=find(fa[x]); }
void merge(int x,int y) { if((x=find(x))==(y=find(y))) return ; fa[x]=y,sm[y]+=sm[x],ans=max(ans,sm[y]); }
vector<int>e[100005]; bool vis[100005];
int main() {
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++) scanf("%d",a+i),fa[i]=i;
	for(int u,v;m--;) scanf("%d%d",&u,&v),e[u].emplace_back(v),e[v].emplace_back(u);
	for(int i=1;i<=n;i++) scanf("%d",p+i); reverse(p+1,p+1+n);
	for(int i=1,u;i<=n;i++) {
		res[i]=ans;
		vis[u=p[i]]=1; ans=max(ans,sm[u]=a[u]);
		for(int v:e[u]) if(vis[v]) merge(u,v);
	} for(int i=n;i;i--) printf("%lld\n",res[i]);
}