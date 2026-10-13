#include<algorithm>
#include<cstdio>
#include<cstring>
#include<iostream>

const int N=1e5+15;
int n,m;
int ty[N],l[N],r[N];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
namespace task_1{
	const int M=1000+15;
	int a[M];
	void main()
	{
		memset(a,0,sizeof(a));
		for (int i=1;i<=m;i++)
		{
			if (ty[i]==1) for (int j=l[i];j<=r[i];j++) a[j]=1;
			if (ty[i]==2) for (int j=l[i];j<=r[i];j++) a[j]=0;
			if (ty[i]==3) for (int j=l[i];j<=r[i];j++) a[j]^=1;
			for (int i=1;i<=n+1;i++) if (a[i]==0) {printf("%d\n",i);break;}
		}
	}
}
namespace task_2{
	int tag[N<<2],rev[N<<2],s0[N<<2],s1[N<<2];
	void pushup(int o)
	{
		s0[o]=s0[o<<1]+s0[o<<1|1];
		s1[o]=s1[o<<1]+s1[o<<1|1];
	}
	void pushdown(int o,int l,int r)
	{
		if (rev[o])
		{
			std::swap(s0[o<<1],s1[o<<1]);
			std::swap(s0[o<<1|1],s1[o<<1|1]);
			rev[o<<1]^=1;rev[o<<1|1]^=1;
			if (tag[o<<1]!=-1) tag[o<<1]^=1;
			if (tag[o<<1|1]!=-1) tag[o<<1|1]^=1;
			rev[o]=0;
		}
		if (tag[o]!=-1)
		{
			int p=tag[o];
			tag[o]=-1;
			tag[o<<1]=p;tag[o<<1|1]=p;
			rev[o<<1]=0;rev[o<<1|1]=0;
			int mid=l+r>>1;
			if (p==0)
			{
				s0[o<<1]=mid-l+1;s1[o<<1]=0;
				s0[o<<1|1]=r-mid;s1[o<<1|1]=0;
			}
			if (p==1)
			{
				s1[o<<1]=mid-l+1;s0[o<<1]=0;
				s1[o<<1|1]=r-mid;s0[o<<1|1]=0;
			}
		}
	}
	void build(int o,int l,int r)
	{
		if (l==r)
		{
			s0[o]=1;s1[o]=0;
			tag[o]=-1;rev[o]=0;
			return;
		}
		int mid=l+r>>1;
		build(o<<1,l,mid);
		build(o<<1|1,mid+1,r);
		pushup(o);
	}
	void change(int o,int l,int r,int x,int y,int z)
	{
		if (l>=x&&r<=y)
		{
			tag[o]=z;rev[o]=0;
			if (z==0)
			{
				s0[o]=r-l+1;s1[o]=0;
			}
			if (z==1)
			{
				s1[o]=r-l+1;s0[o]=0;
			}
			return;
		}
		pushdown(o,l,r);
		int mid=l+r>>1;
		if (x<=mid) change(o<<1,l,mid,x,y,z);
		if (y>mid) change(o<<1|1,mid+1,r,x,y,z);
		pushup(o);
	}
	void rever(int o,int l,int r,int x,int y)
	{
		if (l>=x&&r<=y)
		{
			rev[o]^=1;
			std::swap(s0[o],s1[o]);
			if (tag[o]!=-1) tag[o]^=1;
			return;
		}
		pushdown(o,l,r);
		int mid=l+r>>1;
		if (x<=mid) rever(o<<1,l,mid,x,y);
		if (y>mid) rever(o<<1|1,mid+1,r,x,y);
		pushup(o);
	}
	int query(int o,int l,int r)
	{
		if (l==r) 
		{
			if (s0[o]==0) return -1;
			else return l;
		}
		pushdown(o,l,r);
		int mid=l+r>>1;
		if (s0[o<<1]>0) return query(o<<1,l,mid);
		else if (s0[o<<1|1]>0) return query(o<<1|1,mid+1,r);
		else return -1;
	}
	void main()
	{
		build(1,1,n);
		for (int i=1;i<=m;i++)
		{
			if (ty[i]==1) change(1,1,n,l[i],r[i],1);
			if (ty[i]==2) change(1,1,n,l[i],r[i],0);
			if (ty[i]==3) rever(1,1,n,l[i],r[i]);
			//printf("%d\n",s0[1]);
			int re=query(1,1,n);
			if (re==-1) printf("%d\n",n+1);
			else printf("%d\n",re);
		}
	}
}
int main()
{
	freopen("a.in","r",stdin);
	freopen("a.out","w",stdout);
	m=read();
	for (int i=1;i<=m;i++)
	{
		ty[i]=read();l[i]=read();r[i]=read();
		n=std::max(n,r[i]);
	}
	if (n<=1000&&m<=1000) {task_1::main();return 0;}
	if (n<=100000) {task_2::main();return 0;}
	return 0;
}
