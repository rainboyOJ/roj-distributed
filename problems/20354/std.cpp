#include<cstdio>
#include<algorithm>
#include<cstring>
#include<iostream>
using namespace std;

const int N=1e6+15;
int n,q,tot;
int f[N],w[N],head[N];
struct EDGE
{
	int to,nxt,ww;
}edge[N<<1];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
void add(int u,int v,int ww)
{
	edge[++tot]=(EDGE){v,head[u],ww};
	head[u]=tot;
}
namespace task_1
{
	void main()
	{
		
	}
}
namespace task_2
{
	void main()
	{
		while (q--)
		{
			int opt=read();
			if (opt==1)
			{
				int u=read(),v=read(),s=read();
				if (u==v)
				{
					if (s&1) {puts("none");continue;}
					if (u==1) printf("%d\n",s/2);
					if (u==2) printf("%d\n",w[2]-s/2);
					continue;
				}
				if (s==w[2]) puts("inf");
				else puts("none");
			}
			if (opt==2)
			{
				int u=read(),W=read();
				w[u]=W;
			}
		}
	}
}
namespace task_3
{
	int ans,id;
	void dfs1(int x,int goal,int now,int pre,int las)
	{
		if (x==goal) 
		{
			ans=now;id=pre;
			return;
		}
		for (int i=head[x];i;i=edge[i].nxt)
		{
			int y=edge[i].to;
			if (y==las) continue;
			//printf("qq%d %d %d\n",x,y,edge[i].ww);
			if (pre==1) dfs1(y,goal,now+edge[i].ww,0,x);
			if (pre==0) dfs1(y,goal,now-edge[i].ww,1,x);
		}
	}
	void dfs2(int x,int now)
	{
		if (x==1)
		{
			printf("%d\n",now);
			return;
		}
		dfs2(f[x],w[x]-now);
	}
	void main()
	{
		while (q--)
		{
			int opt=read();
			if (opt==1)
			{
				int u=read(),v=read(),s=read();
				if (u==v) 
				{
					if (s&1) {puts("none");continue;}
					dfs2(u,s/2);
					continue;
				}
				dfs1(u,v,0,1,-1);
				//printf("qq%d %d\n",ans,id);
				if (id==1)//最后是减 
				{
					if ((ans+s)&1) {puts("none");continue;}
					//printf("%d\n",(ans+s)/2);
					dfs2(u,(ans+s)/2);
				}
				if (id==0)//最后是加 
				{
					if (ans!=s) {puts("none");continue;}
					if (ans==s) {puts("inf");continue;}
				}
			}
			if (opt==2)
			{
				int u=read(),W=read();
				w[u]=W;
			}
		}
	}
}
int main()
{		
	freopen("equation.in","r",stdin);
	freopen("equation.out","w",stdout);
	n=read();q=read();
	for (int i=1;i<n;i++)
	{
		f[i+1]=read();w[i+1]=read();
		add(i+1,f[i+1],w[i+1]);
		add(f[i+1],i+1,w[i+1]);
	}
	if (q==0) {task_1::main();return 0;}
	if (n==2) {task_2::main();return 0;}
	task_3::main();
	return 0;
}
