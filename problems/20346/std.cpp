#include<iostream>
#include<cstring>
#include<algorithm>
#include<cstdio>
using namespace std;

const int N=1e5+15;
int n,tot,ans;
int head[N];
struct EDGE
{
	int to,nxt,c,d;
}edge[N<<1];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
void add(int a,int b,int c,int d)
{
	edge[++tot]=(EDGE){b,head[a],c,d};
	head[a]=tot;
}
void dfs(int x,int f,int pre)
{
	for (int i=head[x];i;i=edge[i].nxt)
	{
		int y=edge[i].to;
		if (y==f) continue;
		if (edge[i].d==2) dfs(y,x,pre);
		else if ((edge[i].c^edge[i].d)==0) dfs(y,x,0);
		else if ((edge[i].c^edge[i].d)!=pre) {ans++;dfs(y,x,1);}
		else dfs(y,x,pre);
	}
}
int main()
{
	freopen("w.in","r",stdin);
	freopen("w.out","w",stdout);
	n=read();
	bool flag=1;
	for (int i=1,a,b,c,d;i<n;i++)
	{	
		a=read();b=read();c=read();d=read();
		if (d!=2) flag=0;
		add(a,b,c,d);
		add(b,a,c,d);
	}
	if (flag) {puts("0 0");return 0;}
	dfs(1,-1,-1);
	printf("%d\n",ans);
	return 0;
}
