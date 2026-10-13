#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;
typedef long long ll;

const int N=1e3+15;
const int M=1e6+15;
const int Q=3e5+15;
int n,q;
inline ll read()
{
	char ch=getchar();
	ll s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}

namespace func1{
	ll a[N][N];
	void main()
	{
		while (q--)
		{
			int r=read(),c=read(),l=read(),s=read();
			for (int i=r;i<min(r+l,n+1);i++)
			{
				for (int j=c;j<=min(i-r+c,n);j++)
				{
					a[i][j]+=s;
				}
			}
		}
		ll ans=0;
		for (int i=1;i<=n;i++)
		{
			//printf("%lld\n",ans);
			for (int j=1;j<=n;j++) ans^=a[i][j];
		}
		printf("%lld\n",ans);
	}
}
/*ll calc(ll x,int y)
{
	if (y<=0) return 0;
	ll re=0;
	for (;y;x=x^x,y>>=1) if (y&1) re=re^x;
	return re;
}
namespace func2{
	int cnt;
	int lx[M<<2],rx[M<<2],rt[N];
	ll sum[M<<2],lazy[M<<2];
	void pushdown(int o,int l,int r)
	{
		if (!lazy[o]) return;
		ll p=lazy[o];
		int mid=l+r>>1;
		lazy[o]=0;
		lazy[lx[o]]^=p;
		lazy[rx[o]]^=p;
		sum[lx[o]]^=calc(p,mid-l+1);
		sum[rx[o]]^=calc(p,r-mid);
	}
	void pushup(int o)
	{
		sum[o]=sum[lx[o]]^sum[rx[o]];
	}
	void update(int &o,int l,int r,int x,int y,ll z)
	{
		if (!o) o=++cnt;
		if (l>=x&&r<=y)
		{
			sum[o]^=calc(z,r-l+1);
			lazy[o]^=z;
			return;
		}
		if (!lx[o]) lx[o]=++cnt;
		if (!rx[o]) rx[o]=++cnt;
		pushdown(o,l,r);
		int mid=l+r>>1;
		if (x<=mid) update(lx[o],l,mid,x,y,z);
		if (y>mid) update(rx[o],mid+1,r,x,y,z);
		pushup(o);
	}
	void main()
	{
		while (q--)
		{
			int r=read(),c=read(),l=read();
			ll s=read();
			for (int i=r;i<min(r+l,n+1);i++)
			{
				update(rt[i],1,n,c,min(i-r+c,n),s);
			}
		}
		ll ans=0;
		for (int i=1;i<=n;i++)
		{
			ans^=sum[rt[i]];
		}
		printf("%lld\n",ans);
	}	
}

int r[Q],c[Q],l[Q];
ll s[Q];
namespace func3{
	ll sum[M<<2],pre[M<<2];
	void pushdown(int o,int l,int r)
	{
		if (!pre[o]) return;
		ll p=pre[o];
		int mid=l+r>>1,len1=mid-l+1,len2=r-mid;
		pre[o]=0;
		pre[o<<1]^=p;
		pre[o<<1|1]^=calc(p,mid-l+1+1);
		sum[o<<1]^=calc(p,(len1+1)*len1/2);
		sum[o<<1|1]^=calc(calc(p,mid-l+1+1),(len2+1)*len2/2);
	}
	void pushup(int o)
	{
		sum[o]=sum[o<<1]^sum[o<<1|1];
	}
	void update(int o,int l,int r,int x,int y,ll z)
	{
		if (l>=x&&r<=y)
		{
			pre[o]^=z;
			sum[o]^=calc(z,(r-l+2)*(r-l+1)/2);
			return;
		}
		pushdown(o,l,r);
		int mid=l+r>>1;
		if (x<=mid) update(o<<1,l,mid,x,y,z);
		if (y>mid) 
		{
			if (x<=mid) update(o<<1|1,mid+1,r,x,y,calc(z,mid-x+1+1));
			else update(o<<1|1,mid+1,r,x,y,z);
		}
		pushup(o);
	}
	void main()
	{
		for (int i=1;i<=q;i++)
		{
			update(1,1,n,1,l[i],s[i]);
		}
		ll ans=0;
		for (int i=1;i<=n;i++)
		{
			ans^=sum[i];
		}
		printf("%lld\n",ans);
	}
}*/
int main()
{
	freopen("u.in","r",stdin);
	freopen("u.out","w",stdout);
	n=read();q=read();
	func1::main();
	/*if (n<=300||q==0) {func1::main();return 0;}
	if (n<=1000&&q<=2000) {func2::main();return 0;}
	int fl1=1,fl2=1;
	for (int i=1;i<=q;i++)
	{
		r[i]=read();c[i]=read();l[i]=read();s[i]=read();
		if (r[i]+l[i]!=n+1) fl1=0;
		if (c[i]!=1) fl1=0;
	}
	if (!fl1&&!fl2)	{func3:main();return 0;}*/
	return 0;
}
