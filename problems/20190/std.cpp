#include <cstdio>
#include <algorithm>
const int N=1000005, MOD=1000000007;

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

inline int mval(int x) { return x>=MOD?x-MOD:x; }
inline int fix(int x) { return x+(x>>31&MOD); }
inline void inc(int &x, int a) { x=mval(x+a); }
inline void dec(int &x, int a) { x=fix(x-a); }
inline int qpow(int x, int p)
{ int ret=1; while(p) { if(p&1) ret=1ll*ret*x%MOD; p>>=1, x=1ll*x*x%MOD; } return ret; }

int n, a[N], cnt[N][22], lim[N], mx, ans;
int f[N], g[N], fac[N], inv[N];
int is[N], pr[N], rf[N], top;
inline int C(int n, int m) { return 1ll*fac[n]*inv[m]%MOD*inv[n-m]%MOD; }
inline void init(int n)
{
	inv[0]=inv[1]=fac[0]=1;
	for(int i=2; i<=n; ++i) inv[i]=MOD-1ll*(MOD/i)*inv[MOD%i]%MOD;
	for(int i=1; i<=n; ++i) fac[i]=1ll*i*fac[i-1]%MOD, inv[i]=1ll*inv[i-1]*inv[i]%MOD;
}
inline void initp(int n)
{
	for(int i=2; i<=n; ++i)
	{
		if(!is[i]) rf[i]=i, pr[++top]=i;
		for(int j=1; j<=top&&pr[j]*i<=n; ++j)
		{
			is[i*pr[j]]=1;
			rf[i*pr[j]]=pr[j];
			if(i%pr[j]==0) break;
		}
	}
}
int main()
{
	freopen("game.in","r",stdin);
	freopen("game.out","w",stdout);
	scan(n);
	for(int i=1; i<=n; ++i) scan(a[i]), mx=std::max(mx, a[i]);
	initp(mx), init(n);
	for(int i=1, cur=0; i<=n; ++i)
	{
		g[n-i]=1ll*(n-i)*cur%MOD;
		inc(cur, C(n-1, i-1));
		f[n-i]=1ll*(n-i)*cur%MOD;
	}
	for(int i=1; i<=n; ++i)
	{
		while(a[i]>1)
		{
			int x=rf[a[i]], cnt=0;
			while(a[i]%x==0)
				++cnt, a[i]/=x;
			++::cnt[x][cnt];
			lim[x]=std::max(lim[x], cnt);
		}
	}
	for(int i=2; i<=mx; ++i) if(!is[i]&&lim[i])
	{
		int l=lim[i];
		cnt[i][0]=n;
		for(int j=1; j<=l; ++j) cnt[i][0]-=cnt[i][j];
		int ret=0;
		for(int j=0, cur=0; j<=l; ++j)
		{
			cur+=cnt[i][j];
			inc(ret, f[cur]);
		}
		for(int j=l, cur=0; ~j; --j)
		{
			cur+=cnt[i][j];
			inc(ret, g[cur]);
		}
		inc(ans, ret);
	}
	printf("%d\n", ans);
	return 0;
}