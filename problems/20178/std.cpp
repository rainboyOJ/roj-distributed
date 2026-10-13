#include <cstdio>
#include <vector>
#include <algorithm>
#define ll long long
#define pb emplace_back
#define INF 0x3f3f3f3f3f3f3f3f

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
		static char s[20];
		static int top;
		top=0;
		x<0?pc('-'), x=-x:0;
		while(x) s[top++]=x%10, x/=10;
		!top?pc('0'), 0:0;
		while(top--) pc(s[top]+'0');
		pc(div);
	}
}
using namespace iobuff;

using std::vector;
const int N=200005;
int T;
int n, a[N], pa[N], rt;
ll sz[N], mn, tot, dis[N], ans;
struct edge{
	int nxt, to, w;
}e[N*2];
int head[N], ttp;
inline void adde(int x, int y, int w)
{
	e[++ttp]=edge{head[x], y, w};
	head[x]=ttp;
}
int p[N];
ll cur[N], sd[N];
int tp;
ll f[N], rs[N];
ll grt(int u, int fa)
{
	ll sz=a[u], mx=0;
	for(int i=head[u]; i; i=e[i].nxt) if(e[i].to!=fa)
	{
		int v=e[i].to;
		ll tsz=grt(v, u);
		mx=std::max(mx, tsz);
		sz+=tsz;
	}
	mx=std::max(mx, tot-sz);
	if(mx<mn) rt=u, mn=mx;
	return sz;
}
void dfs(int u, int fa)
{
	pa[u]=fa;
	sz[u]=a[u];
	sd[u]=1ll*a[u]*dis[u];
	for(int i=head[u]; i; i=e[i].nxt)
	{
		int v=e[i].to, c=e[i].w;
		if(v==fa) continue;
		dis[v]=dis[u]+c;
		dfs(v, u);
		sd[u]+=sd[v];
		sz[u]+=sz[v];
	}
}
void dfs1(int u, int fa)
{
	int id=0;
	for(int i=head[u]; i; i=e[i].nxt) if(e[i].to!=fa)
	{
		int v=e[i].to;
		if(sz[v]>sz[id]) id=v;
		dfs1(v, u);
	}
	if(!id) { cur[u]=0, p[u]=u; return; }
	int x=p[id];
	ll c=cur[id];
	c-=2*(sz[u]-sz[id])*dis[u];
	while(sz[x]*2<sz[u])
	{
		int pr=x;
		x=pa[x];
		c+=2*(sz[x]-sz[pr])*dis[x];
	}
	p[u]=x;
	cur[u]=c;
}
int deb[N];
inline void fix(int u)
{
	int x=p[u];
	ll cur=::cur[u];
	tp=0;
	while(x)
	{
		int f=pa[x];
		rs[++tp]=(f?sz[x]*2-sz[u]:INF);
		::f[tp]=f?cur+(sz[rt]-2*sz[x])*dis[x]:0;
		deb[tp]=x;
		if(tp>1&&rs[tp]<=rs[tp-1]) ::f[tp-1]=cur, --tp;
		cur+=2*(sz[pa[x]]-sz[x])*dis[pa[x]];
		x=pa[x];
	}
}
ll rsz;
void rdfs(int u, int fa, int pr=1)
{
	int t=std::upper_bound(rs+pr, rs+tp+1, rsz-sz[u])-rs;
	int x=deb[t];
	ans=std::min(ans, sd[rt]+cur[u]+(sz[u]-2*sz[p[u]])*dis[p[u]]-sz[u]*dis[x]+f[t]);
	for(int i=head[u]; i; i=e[i].nxt) if(e[i].to!=fa)
	{
		int v=e[i].to;
		rdfs(v, u, t);
	}
}
int main()
{
	scan(T);
	while(T--)
	{
		scan(n);
		tot=0;
		ttp=0;
		for(int i=1; i<=n; ++i) head[i]=0;
		for(int i=1; i<=n; ++i) scan(a[i]), tot+=a[i];
		mn=INF, ans=INF;
		for(int i=1, x, y, z; i<n; ++i)
		{
			scan(x), scan(y), scan(z);
			adde(x, y, z);
			adde(y, x, z);
		}
		if(n==1) return puts("0"), 0;
		grt(1, 0);
		dis[rt]=0;
		dfs(rt, 0);
		dfs1(rt, 0);
		int id=0, id1=0;
		for(int i=head[rt]; i; i=e[i].nxt)
		{
			int v=e[i].to;
			if(sz[v]>sz[id]) id1=id, id=v;
			else if(sz[v]>sz[id1]) id1=v;
			ans=std::min(ans, cur[v]+sd[rt]+(sz[v]-2*sz[p[v]])*dis[p[v]]);
		}
		fix(id);
		rsz=sz[rt]-sz[id];
		for(int i=head[rt]; i; i=e[i].nxt) if(e[i].to!=id)
		{
			int v=e[i].to;
			rdfs(v, rt);
		}
		if(id1)
		{
			fix(id1);
			rsz=sz[rt]-sz[id1];
			rdfs(id, rt);
		}
		putint(ans, '\n');
	}
	flush();
	return 0;
}