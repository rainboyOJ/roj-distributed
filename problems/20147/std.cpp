#include <cstdio>
#include <cstring>
#include <algorithm>
#define ll long long
#define INF ((ll)1e18+1)
const int N=805;
int lim=800;
ll l, r, tf[N], tg[N], f[200][500][N], g[200][500][N];
int rcnt[N];
int is[N], pr[N], top;
char s[100]="vector<vector<int>>ans={";
inline void init(int n)
{
	for(int i=2; i<=n; ++i)
	{
		if(!is[i]) pr[++top]=i;
		for(int j=1; j<=top&&i*pr[j]<=n; ++j)
		{
			is[i*pr[j]]=1;
			if(i%pr[j]==0) break;
		}
	}
}
char ans[200000010], ans1[10005], tp1;
int tp, ok;
int sum, cnt, stk[N], cur;
ll resl, resr;
void dfs(int u)
{
	static int top;
	if(!cnt)
	{
		ok=1;
		for(int i=1; i<=top; ++i)
		{
			ans[++tp]=i>1?',':'{';
			int u=stk[i];
			if(pr[u]/100) ans[++tp]=pr[u]/100+'0', ans[++tp]=pr[u]/10%10+'0', ans[++tp]=pr[u]%10+'0';
			else if(pr[u]/10) ans[++tp]=pr[u]/10+'0', ans[++tp]=pr[u]%10+'0';
			else ans[++tp]=pr[u]+'0';
			if(tp>=resr) break;
		}
		ans[++tp]='}';
		ans[++tp]=',';
		return;
	}
	if(cnt&&sum>=pr[u]&&f[u][cnt-1][sum-pr[u]])
	{
		cur+=rcnt[u];
		ll t=f[u][cnt-1][sum-pr[u]]*(2+cur)+g[u][cnt-1][sum-pr[u]];
		if(!ok&&resl>t) resl-=t, resr-=t;
		else
		{
			stk[++top]=u;
			--cnt;
			sum-=pr[u];
			dfs(u);
			++cnt;
			sum+=pr[u];
			--top;
		}
		cur-=rcnt[u];
	}
	if(tp>=resr) return;
	if(f[u+1][cnt][sum])
	{
		ll t=f[u+1][cnt][sum]*(2+cur)+g[u+1][cnt][sum];
		if(!ok&&resl>t) resl-=t, resr-=t;
		else
		{
			dfs(u+1);
		}
	}
}
int main()
{
	freopen("dabiao.in","r",stdin);
	freopen("dabiao.out","w",stdout);
	scanf("%lld %lld", &l, &r);
	int len=strlen(s);
	if(l<=len) for(int i=l; i<=len; ++i) ans1[++tp1]=s[i-1];
	if(r<=len)
	{
		ans1[r-l+2]=0;
		puts(ans1+1);
		return 0;
	}
	l=std::max(1ll, l-len), r-=len;
	init(lim);
	tf[0]=1;
	for(int i=top; i; --i)
	{
		int x=pr[i];
		rcnt[i]=2+(x/10!=0)+(x/100!=0);
		for(int j=x; j<=lim; ++j)
		{
			tf[j]=std::min(tf[j]+tf[j-x], INF);
			tg[j]=std::min(tg[j]+tg[j-x]+rcnt[i]*tf[j-x], INF);
		}
	}
	f[top+1][0][0]=1;
	for(int i=top; i; --i)
	{
		int x=pr[i];
		for(int t=0; x*t<=lim; ++t) std::copy(f[i+1][t], f[i+1][t]+lim+1, f[i][t]);
		for(int t=0; x*t<=lim; ++t) std::copy(g[i+1][t], g[i+1][t]+lim+1, g[i][t]);
		for(int t=0; t*x<=lim; ++t)
		{
			for(int j=x; j<=lim; ++j)
			{
				f[i][t+1][j]+=f[i][t][j-x];
				g[i][t+1][j]+=g[i][t][j-x]+rcnt[i]*f[i][t][j-x];
			}
		}
	}
	int x=1;
	while(l>tg[x]+tf[x]*2)
	{
		ll t=tg[x]+tf[x]*2;
		l-=t;
		r-=t;
		++x;
	}
	resl=l, resr=r;
	while(resr>tp)
	{
		for(int i=0; i<=180; ++i) tf[i]=f[1][i][x], tg[i]=g[1][i][x];
		for(int i=1; i<=180&&resr>tp; ++i) if(tf[i])
		{
			if(!ok&&tf[i]*2+tg[i]<resl)
			{
				ll t=tf[i]*2+tg[i];
				resl-=t;
				resr-=t;
			}
			else
			{
				sum=x, cnt=i;
				dfs(1);
			}
		}
		++x;
	}
	if(tp1) printf("%s", ans1+1);
	ans[resr+1]=0;
	puts(ans+resl);
	return 0;
}