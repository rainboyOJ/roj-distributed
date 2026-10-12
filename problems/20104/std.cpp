#include<bits/stdc++.h>
using namespace std;
const int N=1e6+7;
int n,m,A,B,C,l1[N],r1[N],l2[N],r2[N];
vector<long long>dp[N],dg[N];
vector<long long>d1[N],d2[N];
string a,b;
long long getans(int x,int y){
	if(x<0||y<0) return -1e18;
//	cout<<x<<","<<y<<","<<l1[x]<<","<<r1[x]<<","<<l2[y]<<","<<r2[y]<<endl;
	while(l1[x]<r1[x]){
		int a=d1[x][l1[x]];
		int b=d1[x][l1[x]+1];
		if(dp[x][a]+1ll*A*(a-y)*(a-y)<=dp[x][b]+1ll*A*(b-y)*(b-y)) l1[x]++;
		else break;
	}
	while(l2[y]<r2[y]){
		int a=d2[y][l2[y]];
		int b=d2[y][l2[y]+1];
		if(dp[a][y]+1ll*A*(a-x)*(a-x)<=dp[b][y]+1ll*A*(b-x)*(b-x)) l2[y]++;
		else break;
	}
//	if(x==0&&y==2){
//		cerr<<l1[x]<<":"<<r1[x]<<","<<":"<<d1[x][l1[x]]<<","<<dp[x][0]<<","<<l2[y]<<","<<r2[y]<<","<<d2[y][l2[y]]<<endl;
//	}
	long long ans=-1e18,u;
//	int 
	if(l1[x]<=r1[x]) u=d1[x][l1[x]],ans=max(ans,dp[x][u]+1ll*A*(u-y)*(u-y));
	
	if(l2[y]<=r2[y]) u=d2[y][l2[y]],ans=max(ans,dp[u][y]+1ll*A*(u-x)*(u-x));
//	cerr<<x<<","<<y<<":"<<ans<<endl;
	return ans;
}
void add(int x,int y){
//	cerr<<x<<","<<y<<endl;
	while(l1[x]<r1[x]){
		int a=d1[x][r1[x]];
		int b=d1[x][r1[x]-1];
		if(1ll*(dp[x][y]-dp[x][a]+1ll*y*y*A-1ll*a*a*A)*(y-b)>=1ll*(dp[x][y]-dp[x][b]+1ll*y*y*A-1ll*b*b*A)*(y-a)) r1[x]--;
		else break;
	}
	d1[x][++r1[x]]=y;
	
	while(l2[y]<r2[y]){
		int a=d2[y][r2[y]];
		int b=d2[y][r2[y]-1];
		if(1ll*(dp[x][y]-dp[a][y]+1ll*x*x*A-1ll*a*a*A)*(x-b)>=1ll*(dp[x][y]-dp[b][y]+1ll*x*x*A-1ll*b*b*A)*(x-a)) r2[y]--;
		else break;
	}
	
	d2[y][++r2[y]]=x;
//	cerr<<x<<","<<y<<","<<r1[x]<<","<<r2[y]<<endl;
}
signed main(){
	ios::sync_with_stdio(false);
	cin.tie(0);cout.tie(0);
	cin>>n>>a;
	cin>>m>>b;
	cin>>C>>B>>A;
	a=" "+a,b=" "+b;
	
	for(int i=0;i<=n;i++) dp[i].resize(m+2),d1[i].resize(m+2),l1[i]=1,dg[i].resize(m+2);
	for(int i=0;i<=m;i++) d2[i].resize(n+2),l2[i]=1;
	for(int i=0;i<=n;i++)
		for(int j=0;j<=m;j++) dp[i][j]=-1e18,dg[i][j]=-1e18;
	dp[0][0]=0;
//	cout<<"sssss"<<endl;
	add(0,0);
	
	for(int x=1;x<=n+m;x++){
		for(int i=0;i<=n;i++){
			int j=x-i;
			
			if(j>m||j<0) continue;
//			cout<<i<<":"<<j<<endl;
//			cerr<<r1[0]<<","<<r2[0]<<"sssss"<<endl;
			long long c=-1e18;
			if(i-1>=0&&j-1>=0) c=dg[i-1][j-1];
			dp[i][j]=c;
			if(a[i]==b[j]) dp[i][j]+=C; else dp[i][j]+=B;
			add(i,j);
			dg[i][j]=getans(i,j);
//			cout<<i<<","<<j<<","<<dp[i][j]<<endl;
		}
//		cerr<<x<<"sssss"<<endl;
	}
//	cout<<dp[1][1]<<"wwww"<<endl;
//	cerr<<"sssss"<<endl;
	cout<<max(dp[n][m],getans(n,m))<<'\n';
	return 0;
}
//10 10
//2 2 4 5 5 6 7 8 9 10
//1 3 3 4 6 1 1 1 1 1
