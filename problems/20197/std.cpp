#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define db double
#define gc getchar
#define pc putchar
#define fs first
#define sc second
using namespace std;

ll read()
{
	ll x=0,f=1;
	char ch=gc();
	while(ch<'0'||ch>'9')
	{
		if(ch=='-')f=-1;
		ch=gc();
	}
	while(ch>='0'&&ch<='9')
		x=x*10+(ch^48),ch=gc();
	return x*f;
}
void print(ll x)
{
	if(x<0)pc('-'),x=-x;
	if(x>9)print(x/10);
	pc(x%10+48);
}

const int N=1e6+5;
int n,id,v[N],f[N],g[N],f1[N],f2[N],g1[N],g2[N],st[N],top,ans[N];
struct node{
	int x,y;
}p1[N],p2[N];

bool cmp(node i,node j){
	return i.y<j.y;
}

struct BIT
{
	#define lowbit(x) (x&(-x))
	
	int sum[N];
	void update(int x)
	{
		while(x<=n)
			sum[x]++,x+=lowbit(x);
	}
	int query(int x)
	{
		int res=0;
		while(x)
			res+=sum[x],x-=lowbit(x);
		return res;
	}
}T1,T2;

int main()
{
	freopen("interval.in","r",stdin);
	freopen("interval.out","w",stdout);
	
	n=read(),id=read();
	
	for(int i=1;i<=n;i++)
	{
		v[i]=read();
		f1[i]=f2[i]=n+1,g1[i]=g2[i]=0;
	}
	
	for(int i=1;i<=n;i++)
	{
		while(top&&v[i]<v[st[top]])
			f1[st[top--]]=i;
		st[++top]=i;
	}
	top=0;
	for(int i=1;i<=n;i++)
	{
		while(top&&v[i]>v[st[top]])
			f2[st[top--]]=i;
		st[++top]=i;
	}
	
	top=0;
	for(int i=n;i>=1;i--)
	{
		while(top&&v[i]<v[st[top]])
			g1[st[top--]]=i;
		st[++top]=i;
	}
	top=0;
	for(int i=n;i>=1;i--)
	{
		while(top&&v[i]>v[st[top]])
			g2[st[top--]]=i;
		st[++top]=i;
	}
	
	for(int i=1;i<=n;i++)
	{
		f[i]=max(f1[i],f2[i]);
		g[i]=min(g1[i],g2[i]);
		p1[i]={i,g[i]},p2[i]={i,f[i]};
	}
	
	sort(p1+1,p1+1+n,cmp);
	for(int i=n,j=n;i>=1;i--)
	{
		while(j>=1&&i<=p1[j].y)
			T1.update(p1[j--].x);
		ans[i]=n-j-T1.query(f[i]-1);
	}
	for(int i=1;i<=n;i++)
		print(ans[i]),pc(' ');
	pc('\n');
	
	sort(p2+1,p2+1+n,cmp);
	for(int i=1,j=1;i<=n;i++)
	{
		while(j<=n&&i>=p2[j].y)
			T2.update(p2[j++].x);
		ans[i]=T2.query(g[i]);
	}
	for(int i=1;i<=n;i++)
		print(ans[i]),pc(' ');
	
	return 0;
}