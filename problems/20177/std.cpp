#include<bits/stdc++.h>
using namespace std;
const int N=2010,mod=1e9+7;
int m,L,a[N],s=0,fac[N*N],inv[N*N],c[N][N];
inline int add(int x,int y){return (x+y>=mod)?x+y-mod:x+y;}
inline int dec(int x,int y){return (x-y<0)?x-y+mod:x-y;}
inline int ksm(int x,int y){
	int ret=1;
	for(;y;y>>=1,x=1ll*x*x%mod) if(y&1) ret=1ll*ret*x%mod;
	return ret;
}
inline void init(int s){
	for(int i=c[0][0]=1;i<=L;++i){
		c[i][0]=1;
		for(int j=1;j<=i;++j) c[i][j]=add(c[i-1][j],c[i-1][j-1]);
	}
	fac[0]=1;
	for(int i=1;i<=s;++i) fac[i]=1ll*fac[i-1]*i%mod;
	inv[s]=ksm(fac[s],mod-2);
	for(int i=s-1;i>=0;--i) inv[i]=1ll*inv[i+1]*(i+1)%mod;
}
inline int sgn(int x){return (x&1)?mod-1:1;}
inline int calc(int n,int l,int r){
	l+=n;r+=n;
	int ans=1ll*fac[r+1]*inv[n+1]%mod*inv[r-n]%mod;
	if(l>n) ans=dec(ans,1ll*fac[l]*inv[n+1]%mod*inv[l-n-1]%mod);
	return ans;
}
int main(){
	scanf("%d%d",&m,&L);
	for(int i=1;i<=L;++i) scanf("%d",&a[i]),s+=a[i];
	init(s+L);
	int ans=0;
	for(int i=1,now=0;i<L;now+=a[i],++i){
		int t=L-i,ql=s-now-(a[i]-1),qr=s-now;
		for(int k=0;k*m<=qr&&k<=t;++k) 
			ans=(ans+1ll*c[t][k]*sgn(k)%mod*calc(t-1,ql-k*m,qr-k*m))%mod; 
	}
	printf("%d\n",ans);
	return 0;
}
