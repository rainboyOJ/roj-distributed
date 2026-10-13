#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=1005;
const ll inf=1e15;
ll dep[N],dp[N][N],f[N];
int n,c[N],d[N];bool ok[N][N];
struct edge{int to,w;};
vector<edge>e[N];
void dfs(int u,int fa)
{
	for(auto v:e[u])
		if(v.to^fa)
		{
			dep[v.to]=dep[u]+v.w;
			dfs(v.to,u);
		}
}
void work(int u,int fa)
{
	for(int i=1;i<=n;++i)
		if(ok[u][i])dp[u][i]=c[i];
		else dp[u][i]=inf;
	for(auto v:e[u])
		if(v.to^fa)
		{
			work(v.to,u);
			for(int i=1;i<=n;++i)
				if(ok[u][i])dp[u][i]+=min(f[v.to],dp[v.to][i]-c[i]);
		}
	f[u]=*min_element(dp[u]+1,dp[u]+n+1);
}
inline void clear()
{
	for(int i=1;i<=n;++i)
	{
		e[i].clear();
		for(int j=1;j<=n;++j)ok[i][j]=0;
	}
}
int main()
{
    freopen("dagger.in", "r", stdin);
    freopen("dagger.out", "w", stdout);
	int T;scanf("%d",&T);
	while(T-->0)
	{
		scanf("%d",&n);
		for(int i=1;i<=n;++i)scanf("%d",c+i);
		for(int i=1;i<=n;++i)scanf("%d",d+i);
		for(int i=1,u,v,w;i<n;++i)
		{
			scanf("%d%d%d",&u,&v,&w);
			e[u].push_back({v,w});
			e[v].push_back({u,w});
		}
		for(int i=1;i<=n;++i)
		{
			dep[i]=0;dfs(i,0);
			for(int j=1;j<=n;++j)
				if(dep[j]<=d[i])ok[i][j]=1;
		}
		work(1,0);printf("%lld\n",f[1]);clear();
	}
	return 0;
}