#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
#include<queue>
using namespace std;

const int M=9000+15;
const int N=95;
const int Q=5e6+15;
int n,m,d,tot,ans;
int head[N],vis[Q];
struct EDGE
{
	int to,nxt,c;
}edge[M<<1];
struct node
{
	int now,d,bit;
};
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f; 
}
void add(int u,int v,int c)
{
	edge[++tot]=(EDGE){v,head[u],c};
	head[u]=tot;
}
void print(int x,int now)
{
	putchar('0'+(x&1));
	if (now!=d) print(x>>1,now+1);
}
void bfs(int s)
{
	queue <node> q;
	q.push(node{s,0,0});
	while (!q.empty())
	{
		node k=q.front();q.pop();
		if (k.d==d) 
		{
			if (!vis[k.bit]) ans++;//print(k.bit,1);putchar('\n');}
			vis[k.bit]=1;
			continue;
		}
		for (int i=head[k.now];i;i=edge[i].nxt)
		{
			int y=edge[i].to;
			q.push((node){y,k.d+1,k.bit|(edge[i].c<<k.d)});
		}
	}
}
int main()
{
//	freopen("y.in","r",stdin);
//	freopen("y.out","w",stdout);
	n=read();m=read();d=read();
	bool flag=true;
	for (int i=1,u,v,c;i<=m;i++)
	{
		u=read();v=read();c=read();
		if (c!=0) flag=false;
		add(u,v,c);add(v,u,c);
	}
	if (flag)
	{
		if (head[1]!=0) puts("1");
		else puts("0");
		return 0;
	}
	bfs(1);
	printf("%d\n",ans);
	return 0;
}
