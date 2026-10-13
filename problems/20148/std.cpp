#include <cstdio>
#include <algorithm>
const int N=200005, MOD=998244353;
inline int mval(int x) { return x>=MOD?x-MOD:x; }
inline int fix(int x) { return x+(x>>31&MOD); }
inline void inc(int &x, int a) { x=mval(x+a); }
inline void dec(int &x, int a) { x=fix(x-a); }

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

int T, n, m, s[N], nxt[N], pw[N], ans;
int main()
{
	freopen("x.in","r",stdin);
	freopen("x.out","w",stdout);
	scan(T);
	while(T--)
	{
		scan(m), scan(n);
		pw[0]=1;
		for(int i=1; i<=n; ++i) scan(s[i]), pw[i]=1ll*pw[i-1]*m%MOD;
		for(int i=2, j=0; i<=n; ++i)
		{
			while(j&&s[j+1]!=s[i]) j=nxt[j];
			if(s[j+1]==s[i]) ++j;
			nxt[i]=j;
		}
		ans=0;
		for(int x=n; x; x=nxt[x]) inc(ans, pw[x]);
		putint(ans, '\n');
	}
	flush();
	return 0;
}