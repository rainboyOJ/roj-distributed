#include <bits/stdc++.h>
#define y e[x][i]
using namespace std;
const int N=35,mod=1e9+7;
int n,m,cnt,sum,ans=1,f[N*N],d[N*N],p[N*N],b[N][N];
vector<int> e[N*N];
char s[N];
int id(int u,int v){
	if(!u||v==m) return 0;if(u==n||!v) return cnt;
	return v+(u-1)*(m-1);
}
int getf(int x) {return f[x]==x?x:f[x]=getf(f[x]);}
signed main(){
    freopen("plant.in","r",stdin);
    freopen("plant.out","w",stdout);
	scanf("%d%d",&n,&m);fill_n(b[0],N,1);fill_n(b[n+1],N,1);
	for(int i=1;i<=n;i++){
		scanf("%s",s+1);fill_n(b[i],N,1);
		for(int j=1;j<=m;j++) b[i][j]=(s[j]=='#');
	}
	b[0][1]=b[1][0]=b[n+1][m]=b[n][m+1]=0;
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++)
			if(!b[i][j]) if(b[i-1][j]&&b[i][j-1]) b[i][j]=1,(ans+=ans)%=mod;
	for(int i=n;i;i--)
		for(int j=m;j;j--)
			if(!b[i][j]) if(b[i+1][j]&&b[i][j+1]) b[i][j]=1,(ans+=ans)%=mod;
	cnt=(n-1)*(m-1)+1;
	for(int i=1;i<=cnt;i++) f[i]=i;
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++)
			if(b[i][j]) f[getf(id(i,j))]=f[getf(id(i-1,j-1))]=f[getf(id(i,j-1))]=getf(id(i-1,j));
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++) if(!b[i][j]){
			int u=getf(id(i-1,j)),v=getf(id(i,j-1));
			e[u].push_back(v);p[v]++;
		}
	queue<int> q;d[getf(0)]=1;q.push(getf(0));
	while(!q.empty()){
		int x=q.front();q.pop();
		for(int i=0;i<e[x].size();i++){
			if(!--p[y]) q.push(y);(d[y]+=d[x])%=mod;
		}
	}
	printf("%lld\n",1ll*d[getf(cnt)]*ans%mod);
	return 0;
}