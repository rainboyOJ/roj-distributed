#include<algorithm>
#include<cstdio>
#include<cstring>
#include<iostream>
using namespace std;

const int N=30+15;
int n,k,cnt1,cnt2;
int a[N],vis[N],tmp[N];
double ans,re;
char ch[N];
void dfs1(int x,int now)
{
	if (x==k+1)
	{
		re=max(re,(double)now);
		return;
	}
	int pt=0,pos;
	for (int i=1;i<=n;i++)
	{
		if (vis[i]) continue;
		++pt;
		if (pt==a[x]) {pos=i;break;}
	}
	vis[pos]=1;
	if (tmp[pos]==1) dfs1(x+1,now+1);
	else dfs1(x+1,now);
	vis[pos]=0;
	pt=0;
	for (int i=n;i>=1;i--)
	{
		if (vis[i]) continue;
		++pt;
		if (pt==a[x]) {pos=i;break;}
	}
	vis[pos]=1;
	if (tmp[pos]==1) dfs1(x+1,now+1);
	else dfs1(x+1,now);
	vis[pos]=0;
}
double calc()
{
	re=0;
	//for (int i=1;i<=k;i++) printf("%d ",a[i]);
	//printf("\n");
	dfs1(1,0);
	//printf("%lf\n",re);
	return re;
}
void dfs(int x)
{
	if (x==k+1)
	{
		ans+=calc();
		return;
	}
	for (int i=1;i<=n-x+1;i++)
	{
		a[x]=i;
		dfs(x+1);
	}
}
int main()
{
	freopen("v.in","r",stdin);
	freopen("v.out","w",stdout);
	scanf("%d%d",&n,&k);
	scanf("%s",ch+1);
	for (int i=1;i<=n;i++)
	{
		if (ch[i]=='W') {cnt1++;tmp[i]=1;}
		else {cnt2++;tmp[i]=2;}
	}
	//for (int i=1;i<=n;i++) printf("%d ",tmp[i]);
	if (k==0) {puts("0.0000000");return 0;}
	if (k==n) {printf("%.10lf\n",(double)cnt1);return 0;}
	if (cnt2==n) {puts("0.0000000");return 0;}
	if (cnt1==n) {printf("%.10lf\n",(double)k);return 0;}
	dfs(1);
	double re=1;
	for (int i=n;i>=n-k+1;i--) re*=(double)i;
	printf("%.10f",ans/re);
	return 0;
}
