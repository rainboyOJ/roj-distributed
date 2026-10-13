#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<iostream>
#include<vector>
#include<algorithm>
#include<cmath>
#define P puts("lala")
#define cp cerr<<"lala"<<endl
#define ln putchar('\n')
#define pb push_back
#define fi first
#define se second 
#define mkp make_pair
using namespace std;
inline int read()
{
    char ch=getchar();int g=1,re=0;
    while(ch<'0'||ch>'9') {if(ch=='-')g=-1;ch=getchar();}
    while(ch<='9'&&ch>='0') re=(re<<1)+(re<<3)+(ch^48),ch=getchar();
    return re*g;
}
typedef long long ll;
typedef pair<int,int> pii;

const int N=100050;
const int mod=1e9+7;
ll qpow(ll a,int n)
{
	if(n<0) return 0;
	ll ans=1;
	for(;n;n>>=1,a=a*a%mod) if(n&1) ans=ans*a%mod;
	return ans;
}

int n,m,X[N],a[2];
int ans[10],s[10];
//Alice win ; Bob win ; first win ; second win;

void wj()
{
//	freopen("stone.in","r",stdin);
//	freopen("stone.out","w",stdout);
}
int main()
{
	wj();
	int i,j,opt,T;
	n=read(); a[0]=read(); a[1]=read();
	bool swa=0;
	if(a[0]>a[1]) swap(a[0],a[1]),swa=1;
	for(i=1;i<=n;++i) X[i]=read(),X[i]%=(a[0]+a[1]);
	for(i=1;i<=n;++i)
	{
		if(X[i]<a[0]) s[1]++;
		else if(a[0]<=X[i]&&X[i]<a[1]) s[2]++;
		else if(a[1]<=X[i]&&X[i]<2*a[0]) s[3]++;
		else s[4]++;
	}
	//ans[4]=(ans[4]+qpow(2,s[1]))%mod;
	ans[1]=(ans[1]+(qpow(2,s[2])-1ll+mod)*qpow(2,n-s[2])%mod)%mod;
	ans[1]=(ans[1]+(qpow(2,s[4])-s[4]-1ll+mod)*qpow(2,s[3])%mod*qpow(2,s[1])%mod)%mod;
	ans[1]=(ans[1]+s[4]*qpow(2,s[3]-1)%mod*qpow(2,s[1])%mod)%mod;
	ans[3]=(ans[3]+s[4]*qpow(2,s[3]==0?0:s[3]-1)%mod*qpow(2,s[1])%mod)%mod;
	ans[3]=(ans[3]+qpow(2,s[3]-1)*qpow(2,s[1])%mod)%mod;
	ans[4]=(ans[4]+qpow(2,s[3]==0?0:s[3]-1)*qpow(2,s[1])%mod)%mod;
	if(swa) swap(ans[1],ans[2]);
	printf("%d %d %d %d\n",ans[1],ans[2],ans[3],ans[4]);
	return 0;
}