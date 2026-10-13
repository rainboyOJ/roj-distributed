#include<bits/stdc++.h>
using namespace std;
const int N=1e5+5;
vector<int>d[1005];int pr[200],cnt,id[1005];
inline void pre()
{
	for(int i=1;i<=1000;++i)
	{
		int u=i;
		for(int k=2;k*k<=u;++k)
			if(u%k==0)
			{
				d[i].push_back(k);
				while(u%k==0)u/=k;
			}
		if(u>1)d[i].push_back(u);
		if(i>1&&u==i)pr[++cnt]=i,id[i]=cnt;
	}
}
int n,q,a[N],go[N][200],p[1005],c[N],c0[N];
int main()
{
    freopen("gcd.in","r",stdin);
    freopen("gcd.out","w",stdout);
	pre();scanf("%d%d",&n,&q);
	for(int i=1;i<=n;++i)
	{
		scanf("%d",a+i),c[i]=c[i-1]+(a[i]>1);
		c0[i]=c0[i-1]+(a[i]==0);
	}
	for(int i=n;i;--i)
	{
		for(int t=1;t<=cnt;++t)go[i][t]=n+1;
		for(int c:d[a[i]])
		{
			if(p[c])
			{
				for(int t=1;t<=cnt;++t)
					go[i][t]=min(go[i][t],go[p[c]][t]);
				go[i][id[c]]=p[c];
			}
			p[c]=i;
		}
	}
	while(q--)
	{
		int x,y;scanf("%d%d",&x,&y);
		if(x==y)puts("Shi");
		else if(a[x]==1||a[y]==1)puts("Fou");
		else if(a[x]==0||a[y]==0)puts(c[y]-c[x-1]>0?"Shi":"Fou");
		else if(c0[y]-c0[x-1]>0)puts("Shi");
		else
		{
			bool flag=0;
			for(int c:d[a[y]])
				if(go[x][id[c]]<=y){flag=1;break;}
			puts(flag?"Shi":"Fou");
		}
	}
	return 0;
}