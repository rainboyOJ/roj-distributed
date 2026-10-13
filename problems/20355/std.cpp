#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;
typedef long long ll;

const int N=1e4+15;
const int M=50;
const int inf=2515;
const int mod=1e9+7;
int n;
int vis[M][M][M][M],fx[N],fy[N],prex[N],prey[N];
struct node
{
	int x,y;
}p[N];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
int main()
{
	freopen("rectangle.in","r",stdin);
	freopen("rectangle.out","w",stdout);
	n=read();
	for (int i=1;i<=n;i++)
	{
		p[i].x=read();p[i].y=read();
		fx[i]=p[i].x;fy[i]=p[i].y;
	}
	sort(fx+1,fx+1+n);
	sort(fy+1,fy+1+n);
	int len1=unique(fx+1,fx+1+n)-fx-1;
	int len2=unique(fy+1,fy+1+n)-fy-1;
	for (int i=1;i<=n;i++)
	{
		int q=lower_bound(fx+1,fx+1+len1,p[i].x)-fx;
		prex[q]=p[i].x;
		p[i].x=q;
		q=lower_bound(fy+1,fy+1+len2,p[i].y)-fy;
		prey[q]=p[i].y;
		p[i].y=q;
	}
	int S=1<<n;
	ll ans=0;
	for (int i=1;i<S;i++)
	{
		int tx=inf,dx=-1,ty=inf,dy=-1;
		for (int j=0;j<n;j++)
		{
			if (i&(1<<j))
			{
				tx=min(tx,p[j+1].x);
				ty=min(ty,p[j+1].y);
				dx=max(dx,p[j+1].x);
				dy=max(dy,p[j+1].y);
			}
		}
		if (!vis[dx][tx][dy][ty]) (ans+=1ll*(prex[dx]-prex[tx])*(prey[dy]-prey[ty]))%=mod;
		vis[dx][tx][dy][ty]=1;
	}
	printf("%lld\n",ans);
	return 0;
}
