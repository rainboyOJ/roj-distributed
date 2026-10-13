#include<algorithm>
#include<cstdio>
#include<iostream>
#include<cstring>
using namespace std;
typedef long long ll;

const int N=4000+15;
const int mod=1e9+7;
int n;
ll dp[N][N],pre[N][N],back[N][N],tmp[N][N],a[N];
struct node
{
	ll x,y;
}e[N];
inline ll read()
{
	char ch=getchar();
	ll s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
bool cmp(node a,node b){return a.y>b.y;}
int main()
{
	freopen("refract.in","r",stdin);
	freopen("refract.out","w",stdout);
	n=read();
	for (int i=1;i<=n;i++) {e[i].x=read();e[i].y=read();a[i]=e[i].x;}
	sort(a+1,a+1+n);
	int len=unique(a+1,a+1+n)-a-1;
	for (int i=1;i<=n;i++) e[i].x=lower_bound(a+1,a+1+n,e[i].x)-a;
	sort(e+1,e+1+n,cmp);
	for (int i=1;i<=n;i++) dp[i][0]=1;
	for (int i=2;i<=n;i++)
	{
		for (int j=1;j<i;j++)
		{
			if (e[i].y==e[j].y) continue;
			if (e[i].x>e[j].x) (dp[i][j]+=back[j][e[i].x+1]+1)%=mod;
			if (e[i].x<e[j].x) (dp[i][j]+=pre[j][e[i].x-1]+1)%=mod;
		}
		for (int j=1;j<n;j++)
		{
			(tmp[i][e[j].x]+=dp[i][j])%=mod;
		}
		for (int j=1;j<=n;j++) 
		{
			(pre[i][j]=tmp[i][j]+pre[i][j-1])%=mod;
			(back[i][n-j+1]=tmp[i][n-j+1]+back[i][n-j+2])%=mod;
		}
	}
	ll ans=0;
	for (int i=1;i<=n;i++)
	{
		for (int j=0;j<i;j++) (ans+=dp[i][j])%=mod;
	}
	printf("%lld\n",ans);
	return 0;
}
