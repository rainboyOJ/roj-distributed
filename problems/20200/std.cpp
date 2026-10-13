#include <bits/stdc++.h>
using namespace std;
#define ll long long
const int N=505;
ll f[N][N];
inline void Max(ll &a,ll b){if(a<b)a=b;}
#define ls (u<<1)
#define rs (u<<1|1)
int d[N],n,sz[N];
void dfs(int u){
	memset(f[u],-0x1f,(n+1)<<3);sz[u]=1;
	if(ls>n){f[u][1]=0;return;}
	else dfs(ls),sz[u]+=sz[ls];
	if(rs>n){
		for(int i=1;i<=sz[ls];++i){
			Max(f[u][i+1],f[ls][i]+d[ls]);
			Max(f[u][sz[ls]-i+1],f[ls][i]);
		}
	}else{
		dfs(rs);
		sz[u]+=sz[rs];
		for(int i=1;i<=sz[ls];++i){
			for(int j=1;j<=sz[rs];++j){
				Max(f[u][i+j+1],f[ls][i]+f[rs][j]+d[ls]+d[rs]);
				Max(f[u][sz[ls]-i+j+1],f[ls][i]+f[rs][j]+d[rs]);
				Max(f[u][sz[rs]-j+i+1],f[ls][i]+f[rs][j]+d[ls]);
				Max(f[u][sz[ls]-i+sz[rs]-j+1],f[ls][i]+f[rs][j]); 
			}
		}
	}
}
int main(){
	scanf("%d",&n);
	if(!n){puts("0");return 0;}
	for(int i=1;i<=n;++i)
		scanf("%d",&d[i]);
	dfs(1); 
	printf("%lld\n",f[1][n>>1]);
	return 0;
}