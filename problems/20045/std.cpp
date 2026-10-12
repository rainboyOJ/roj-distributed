#include<bits/stdc++.h>
using namespace std;
const int N=1002,p=998244353; 
int n,k,ans,f[N][4][4],g[N][4];
pair<int,int>F[N];
void solve(){
	for(int i=1;i<=n;i++){
		g[i][0]=F[i].first+F[i].second;
		g[i][1]=F[i].first-F[i].second;
		g[i][2]=-F[i].first+F[i].second;
		g[i][3]=-F[i].first-F[i].second;
	}
	for(int i=1;i<=k;i++){
		for(int j=0;j<=3;j++)
			for(int z=0;z<=3;z++)
				f[i][j][z]=-2e9;
	}
	for(int i=1;i<=n;i++){
		for(int q=0;q<=3;q++)
			for(int z=0;z<=3;z++)
				ans=max(ans,f[k-1][q][z]+g[i][3-z]+g[i][3-q]);
		for(int j=k-2;j>=1;j--)
			for(int q=0;q<=3;q++)
				for(int z=0;z<=3;z++)
					for(int t=0;t<=3;t++)
					f[j+1][q][t]=max(f[j+1][q][t],f[j][q][z]+g[i][3-z]+g[i][t]);
		for(int q=0;q<=3;q++)
			for(int z=0;z<=3;z++)
				f[1][q][z]=max(f[1][q][z],g[i][q]+g[i][z]);
	}
}
int main(){
//	freopen("5.in","r",stdin);
//	freopen("5.out","w",stdout); 
	int T;
	cin>>T;
	while(T--){
		cin>>n>>k,ans=0;
		for(int i=1;i<=n;i++) cin>>F[i].first;
		for(int i=1;i<=n;i++) cin>>F[i].second;
		for(int ii=1;ii<=1000;ii++){
			random_shuffle(F+1,F+n+1);
			solve();
		}
		cout<<ans<<endl;
	}
	return 0;
}
