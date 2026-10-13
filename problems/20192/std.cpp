#include <cstdio>
#include <algorithm>
const int N=300005;

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

int n, m, a[N], b[N], mx;
int is[N], pr[N], top, mu[N], f[N];
unsigned int g[N];
void init(int n)
{
	mu[1]=1;
	for(int i=2; i<=n; ++i)
	{
		if(!is[i]) pr[++top]=i, mu[i]=-1;
		for(int j=1; j<=top&&pr[j]*i<=n; ++j)
		{
			int x=pr[j]*i;
			is[x]=1;
			if(i%pr[j]==0) break;
			mu[x]=-mu[i];
		}
	}
}
int main()
{
	freopen("sor.in", "r", stdin);
	freopen("sor.out", "w", stdout);
	scan(n), scan(m);
	for(int i=1, x; i<=n; ++i) scan(x), ++a[x], mx=std::max(mx, x);
	n=mx;
	init(mx);
//	for(int i=1; i<=n; ++i) printf("mu %d %d\n", i, mu[i]);
	for(int i=1; i<=n; ++i) for(int j=i; j<=n; j+=i)
		b[i]+=a[j];
//	printf("b %d\n", b[1]);
	for(int i=n; i; --i)
	{
		if(a[i]) { f[i]=1; continue; }
		f[i]=0x3f3f3f3f;
		int lim=n/i;
		std::fill(g+1, g+lim+1, 0);
		for(int t=1; t<=lim; ++t) if(mu[t])
		{
			int v=b[i*t]*mu[t];
			for(int j=t; j<=lim; j+=t) g[j]+=v;
		}
		for(int j=2; j<=lim; ++j) if(g[j])
			f[i]=std::min(f[i], f[i*j]+1);
	}
	for(int i=1; i<=m; ++i)
	{
		if(f[i]==0x3f3f3f3f) putint(-1, ' '), putint(-1, '\n');
		else putint(f[i], ' '), putint(b[i], '\n');
	}
	flush();
	return 0;
}