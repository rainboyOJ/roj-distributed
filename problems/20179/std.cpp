#include<bits/stdc++.h>
#define maxn 2000005
using namespace std;
int s[maxn],n,m,k,mxdep;
int dep[maxn];
vector<int>e[maxn],q;
priority_queue<pair<int,int> >Q;
void ins() {
	printf("%d",q.size());
	for(int x:q) printf(" %d",x); puts("");
	for(int x:q) for(int y:e[x]) Q.emplace(dep[y],y);
	q.clear();
}
void dfs(int u) { dep[u]=0; for(int v:e[u]) dfs(v),dep[u]=max(dep[u],dep[v]); dep[u]++; }
int main() {
	scanf("%d%d",&n,&k); s[0]=1;
	for(int i=2,x;i<=n;i++) scanf("%d",&x),s[dep[i]=dep[x]+1]++,e[x].emplace_back(i);
	for(int i=n;i>=1;i--) s[i-1]+=s[i];
	for(int i=1;i<=n;i++) mxdep=max(mxdep,dep[i]);
	int ans=0,p=0;
	for(int i=1,x;i<=mxdep;i++) if(ans<(x=i+(s[i]+k-1)/k)) ans=x,p=i;
	dfs(1);
	printf("%d\n",ans); q.push_back(1); ins();
	for(int i=1;i<ans;i++) {
		int T=k;
		while(T&&Q.size()) T--,q.push_back(Q.top().second),Q.pop();
		ins();
	}
}