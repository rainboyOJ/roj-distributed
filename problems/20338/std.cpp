#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;

const int N=1e5+15;
const int M=305;
int n,m;
int a[N],tmp[N][M];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
void function1()
{	
	for (int i=1;i<=n;i++) a[i]=read();
	for (int i=1;i<=m;i++)
	{
		int l=read(),r=read(),k=read();
		int mx=0;
		for (int i=l;i<=r;i++) mx=max(mx,a[i]%k);
		printf("%d\n",mx);
	}
}
/*5 5
1 2 3 4 5
1 3 2
1 3 3
1 4 4
5 5 5
3 5 3*/ 
int tot=0;
int tree[N],L[N<<5],R[N<<5],sz[N<<5];
int update(int pre,int l,int r,int x)
{
	int rt=++tot;
	L[rt]=L[pre];R[rt]=R[pre];sz[rt]=sz[pre]+1;
	if (l<r)
	{
		int mid=l+r>>1;
		if (x<=mid) L[rt]=update(L[pre],l,mid,x);
		else R[rt]=update(R[pre],mid+1,r,x);
	}
	return rt;
}
int query(int u,int v,int l,int r,int x)//找到小于等于x的最大的数 
{
	if (l==r) 
	{
		if (l<=x) return l;
		else return -1;
	}
	int li=sz[L[v]]-sz[L[u]];
	int ri=sz[R[v]]-sz[R[u]];
	int mid=l+r>>1,mx=-1;
	if (x<mid) 
	{
		if (li) mx=query(L[u],L[v],l,mid,x);
		else return -1;
	}
	else 
	{
		if (li) mx=max(mx,query(L[u],L[v],l,mid,x));
		if (ri) mx=max(mx,query(R[u],R[v],mid+1,r,x));
	}
	return mx;
}
void function3()
{
	int MAX=0;
	for (int i=1;i<=n;i++)
	{
		MAX=max(MAX,a[i]);
	}
	for (int i=1;i<=n;i++) tree[i]=update(tree[i-1],1,MAX,a[i]);
	for (int i=1;i<=m;i++)
	{
		int l=read(),r=read(),k=read();
		int mx=0;
		for (int j=1;(j-1)*k<=MAX;j++) 
		{
			int o=query(tree[l-1],tree[r],1,MAX,j*k-1);
			//printf("qq%d %d %d\n",i,j*k-1,o);
			if (o!=-1) mx=max(mx,o%k);
		} 
		printf("%d\n",mx);
	} 
}
void get(int x,int y,int z)
{
	for (int i=1;i<=M;i++) 
	{
		if (i==z) tmp[x][i]=tmp[y][i]+1;
		else tmp[x][i]=tmp[y][i];
	}
}
void function2()
{
	bool flag=true;
	for (int i=1;i<=n;i++) 
	{
		a[i]=read();
		if (a[i]>300) flag=false;
	}
	if (!flag) 
	{
		function3();
		return;	
	}
	for (int i=1;i<=n;i++) get(i,i-1,a[i]);
	for (int i=1;i<=m;i++)
	{
		int l=read(),r=read(),k=read();
		int mx=0;
		for (int i=1;i<=M;i++) if (tmp[r][i]-tmp[l-1][i]>=1) mx=max(mx,i%k);
		printf("%d\n",mx);
	}
}
int main()
{
	freopen("flower.in","r",stdin);
	freopen("flower.out","w",stdout);
	n=read();m=read();
	if (n<=4000) function1();
	else function2();
	return 0;
}
