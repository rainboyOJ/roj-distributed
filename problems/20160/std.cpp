#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
ll n,m,d,w,a,b;
int inv(ll x){
	ll res=1,y=w-2;x%=w;
	while(y){
		if(y&1) (res*=x)%=w;
		(x*=x)%=w;y>>=1;
	}
	return res;
}
void solve(){
	scanf("%lld%lld%lld%lld%lld",&m,&d,&w,&a,&b);
	(a+=d)%=w;(b+=d)%=w;n=min(m,d);
	if((d-1)*(d+1)%w==0){
		ll ans=0;
		if(((d-1)%w&&(a+b)%w)||((d+1)%w&&a!=b)) return(void) puts("0");
		if((d+1)%w==0) (a+=n+1)%=w;
		if(n/w<=10){
			for(ll i=a;i<=n*2;i+=w) if(i>1) ans+=min(i-1,n*2-i+1);
		}else{
			ll s0,s1,s2,s3;
			s1=(n+1)/w*w+a;if(s1>n+1) s1-=w;
			s3=(n*2)/w*w+a;if(s3>n*2) s3-=w;
			s2=s1+w;s0=a;while(s0<2) s0+=w;
			s0--;s1--;s2=n*2+1-s2;s3=n*2+1-s3;
			ans=(s0+s1)*((s1-s0)/w+1)/2+(s2+s3)*((s2-s3)/w+1)/2;
		}
		printf("%lld\n",ans);
	}else{
		ll xl=(d*a+w-b)%w*inv(d*d-1)%w,yl=(d*b+w-a)%w*inv(d*d-1)%w,xr=(n/w*w+xl),yr=(n/w*w+yl);
		if(!xl) xl+=w;if(!yl) yl+=w;if(xr>n) xr-=w;if(yr>n) yr-=w;
		printf("%lld\n",((xr-xl)/w+1)*((yr-yl)/w+1));
	}
}
signed main(){
    freopen("bob.in","r",stdin);
    freopen("bob.out","w",stdout);
	int t;scanf("%d",&t);
	while(t--) solve();
	return 0;
}