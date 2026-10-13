#include<bits/stdc++.h>
using namespace std;
namespace iobuff{
	const int LEN=1000000;
	char in[LEN+5], out[LEN+5];
	char *pin=in, *pout=out, *ed=in, *eout=out+LEN;
	inline char gc(void)
	{
		return pin==ed&&(ed=(pin=in)+fread(in, 1, LEN, stdin), ed==in)?EOF:*pin++;
	}
	inline void pc(char c)
	{
		pout==eout&&(fwrite(out, 1, LEN, stdout), pout=out);
		(*pout++)=c;
	}
	inline void flush()
	{ fwrite(out, 1, pout-out, stdout), pout=out; }
	template<typename T> inline void scan(T &x)
	{
		static int f;
		static char c;
		c=gc(), f=1, x=0;
		while(c<'0'||c>'9') f=(c=='-'?-1:1), c=gc();
		while(c>='0'&&c<='9') x=10*x+c-'0', c=gc();
		x*=f;
	}
	template<typename T> inline void putint(T x, char div)
	{
		static char s[15];
		static int top;
		top=0;
		x<0?pc('-'), x=-x:0;
		while(x) s[top++]=x%10, x/=10;
		!top?pc('0'), 0:0;
		while(top--) pc(s[top]+'0');
		pc(div);
	}
}
using iobuff::putint;
using iobuff::pc;
const int N=1e5+5,M=1e6+5;
int n,a[N],b[N],sta[N],top;
inline bool isok()
{
	for(int i=1;i<=n;++i)b[i]=a[i];
	sort(b+1,b+n+1);top=0;int t=1;
	for(int i=n;i;--i)
	{
		if(a[i]==b[t])++t;
		else sta[++top]=a[i];
		while(top&&b[t]==sta[top])++t,--top;
	}
	return top?false:true;
}
int op[M],x[M],y[M],z[M],cnt;
inline void ins(int aa,int bb,int cc,int dd)
{
	if(aa==1&&cc==0)return;
	if(aa==3&&dd==0)return;
	op[++cnt]=aa,x[cnt]=bb,y[cnt]=cc,z[cnt]=dd;
}
inline void print()
{
	putint(cnt,'\n');
	for(int i=1;i<=cnt;++i,pc('\n'))
	{
		putint(op[i],' ');putint(x[i],' ');
		if(op[i]==1||op[i]==3)putint(y[i],' ');
		if(op[i]==3)putint(z[i],' ');
	}
}
inline void s1()
{
	putint(1,'\n');cnt=0;top=0;int t=1;
	for(int i=n;i;--i)
	{
		if(a[i]==b[t])
		{
			ins(1,1,1,0),ins(2,1,0,0);
			++t;
		}
		else sta[++top]=a[i],ins(1,1,1,0);
		while(top&&b[t]==sta[top])ins(2,1,0,0),++t,--top;
	}
	return print();
}
int c[N];
inline void clear(){for(int i=1;i<=n;++i)c[i]=0;}
inline int lb(int u){return u&(-u);}
inline void upd(int u,int v){for(;u;u-=lb(u))c[u]+=v;}
inline int query(int u){int ret=0;for(;u<=n;u+=lb(u))ret+=c[u];return ret;}
int rk[N],pos[N];pair<int,int>tmp[N];
inline void s2()
{
	putint(2,'\n');top=0;cnt=0;
	for(int i=1;i<=n;++i)
		tmp[i]=make_pair(a[i],i);
	sort(tmp+1,tmp+n+1);
	for(int i=1;i<=n;++i)rk[i]=tmp[i].second;
	for(int i=1,now=n;i<=n;++i)
	{
		if(rk[i]<=now)
		{
			for(int j=now;j>rk[i];--j)
				pos[j]=++top,upd(top,1);
			ins(1,1,now-rk[i]+1,0),ins(2,1,0,0);
			now=rk[i]-1;
		}
		else
		{
			int u=pos[rk[i]],num=query(u);
			ins(3,1,2,num-1),ins(2,1,0,0),ins(3,2,1,num-1);
			upd(u,-1);
		}
	}print();clear();
}
int main()
{
    freopen("sort.in","r",stdin);
    freopen("sort.out","w",stdout);
	int T;scanf("%d",&T);
	while(T--)
	{
		scanf("%d",&n);
		for(int i=1;i<=n;++i)scanf("%d",a+i);
		isok()?s1():s2();
	}iobuff::flush();
	return 0;
}