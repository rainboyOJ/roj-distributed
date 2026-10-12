#include<bits/stdc++.h>
using namespace std;
const int N=5e3+7;
int n,k,p,ans,a[N],g[N],f[N][N];
int main(){
	cin>>n>>k>>p,g[0]=1;
	for(int i=1;i<=n;i++) g[i]=g[i-1]*2%p;
	for(int i=1;i<=n;i++) cin>>a[i],ans=(ans+1ll*(a[i]/k)*g[n-1])%p,a[i]%=k;
	f[0][0]=1;
	for(int i=1;i<=n;i++){
		for(int j=0;j<k;j++) f[i][j]=f[i-1][j];
		for(int j=0;j<k;j++)
			if(j+a[i]>=k)
				ans=(ans+1ll*g[n-i]*f[i-1][j])%p,f[i][j+a[i]-k]=(f[i][j+a[i]-k]+f[i-1][j])%p;
			else
				f[i][j+a[i]]=(f[i][j+a[i]]+f[i-1][j])%p;
	}
	cout<<ans<<endl;
	return 0;
}
