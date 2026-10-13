#include<algorithm>
#include<cstdio>
#include<cstring>
#include<iostream>
using namespace std;

const int N=400+15;
int n,m;
int u[N],v[N];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
namespace task_1{
	const int M=22;
	int dp[M][1<<M],vis[M][M];
	void main()
	{
		for (int i=1;i<=m;i++) u[i]--,v[i]--;
		dp[1][(1<<n)-1]=1;
		for (int i=1;i<=m;i++)	
			for (int j=0;j<1<<n;j++)
			{
				if (!dp[i][j]) continue; 
				if (j&(1<<u[i])) dp[i+1][j^(1<<u[i])]|=dp[i][j];
				if (j&(1<<v[i])) dp[i+1][j^(1<<v[i])]|=dp[i][j];
				if ((j&(1<<u[i]))==0&&(j&(1<<v[i]))==0) dp[i+1][j]|=dp[i][j];
			}
		int ans=0;
		for (int k=0;k<1<<n;k++)
		{
			if (!dp[m+1][k]) continue;
			for (int i=0;i<n;i++)	
				for (int j=i+1;j<n;j++)
				{
					if ((k&(1<<i))==0) continue;
					if ((k&(1<<j))==0) continue;
					if (!vis[i][j]) ans++;
					vis[i][j]=1;
				}
		}
		printf("%d\n",ans);
	}
}
int main()
{	
	freopen("c.in","r",stdin);
	freopen("c.out","w",stdout);
	n=read();m=read();
	for (int i=1;i<=m;i++) 
	{
		u[i]=read();v[i]=read();
	}
	task_1::main();
	return 0;
}
