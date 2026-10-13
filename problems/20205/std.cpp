#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<algorithm>

using namespace std;

typedef long long LL;
const int MX=1001111,md=998244353;
int r;
char s[MX];
int mxb[MX],c[MX],d[MX],cb[MX],n;
int cr[MX],inv[MX];

#define M(x,y) (x=(md+(x)-(y))%md)
#define A(x,y) (x=((x)+(y))%md)

int main(){
    freopen("string.in","r",stdin);
    freopen("string.out","w",stdout);
	scanf("%d%s",&r,s+1);
	n=strlen(s+1);
	mxb[1]=0;
	for(int i=2;i<=n;i++){
		int t=mxb[i-1];
		while(t&&s[t+1]!=s[i])t=mxb[t];
		mxb[i]=t+(s[t+1]==s[i]);
	}
	for(int i=0;i<=n;i++)c[i]=1;
	for(int i=n;i;i--)c[mxb[i]]+=c[i];
	inv[1]=1;
	for(int i=2;i<=n;i++)inv[i]=(LL)inv[md%i]*(md-md/i)%md;
	cr[r]=1;
	for(int i=r+1;i<=n+1;i++)cr[i]=(LL)cr[i-1]*i%md*inv[i-r]%md;
	for(int i=0;i<=n;i++)d[i]=cr[c[i]];
	for(int i=1;i<=n;i++)M(d[mxb[i]],cr[c[i]]);
	cb[0]=1;
	for(int i=1;i<=n;i++)cb[i]=cb[mxb[i]]+1;
	int ans=0;
	for(int i=0;i<=n;i++)A(ans,(LL)d[i]*cb[i]%md*cb[i]%md);
	printf("%d\n",ans);
	return 0;
}