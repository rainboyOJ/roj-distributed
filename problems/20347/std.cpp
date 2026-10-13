#include<algorithm>
#include<cstring>
#include<cstdio>
#include<iostream>
using namespace std;
typedef long long ll;

const int N=1e6+15;
const int mod=1e9+7;
int n,t,tot,pnt;
ll ans;
int a[N],vis[N],tmp1[N],tmp2[N],pp[N],pr[N];
inline int read()
{
	char ch=getchar();
	int s=0,f=1;
	while (ch<'0'||ch>'9') {if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9') {s=(s<<3)+(s<<1)+ch-'0';ch=getchar();}
	return s*f;
}
void pre(int x)
{
	for (int i=2;i*i<=x;i++)
	{
		if (x%i) continue;
		if (!pp[i]) pr[++tot]=i;
		pp[i]=1;
		while (x%i==0) x=x/i;
	}
	if (x>1) 
	{
		if (!pp[x]) pr[++tot]=x;
		pp[x]=1;
	}
}
void dfs(int x)
{
	if (x==tot+1) 
	{
		for (int i=1;i<=n;i++) {tmp1[i]=0;tmp2[i]=0;}
		int cnt=0;
		for (int i=1;i<=tot;i++)
			for (int j=1;j<=n;j++) 
				if (a[j]%pr[i]==0) 
				{
					if (vis[i]) {if (tmp1[j]==0) cnt++;tmp1[j]|=1;}
					else if (!vis[i]) tmp2[j]|=1;
				}
		if (cnt==n-pnt||cnt==0) return;
		bool flag=true;
		for (int i=1;i<=n;i++) if ((tmp1[i]&tmp2[i])==1) {flag=false;break;}
		if (!flag) return;
		(ans+=1)%=mod;
		//for (int i=1;i<=tot;i++) if (vis[i]) printf("%d ",pr[i]);
		//printf("\n");
		return;
	}
	for (int i=1;i>=0;i--)
	{
		vis[x]=i;
		dfs(x+1);
	}
}
void init()
{
	ans=tot=pnt=0;
	memset(pp,0,sizeof(pp));
}
ll qpow(int x,ll y)
{
	ll re=1;
	for (;y;y>>=1,x=x*x%mod) if (y&1) re=re*x%mod;
	return re;
} 
int gcd(int x,int y)
{
	if (!y) return x;
	return gcd(y,x%y);
}
namespace task
{
	int fa[N],check[N];
	int find(int x)
	{
		if (fa[x]!=x) fa[x]=find(fa[x]);
		return fa[x];
	}
	void main()
	{
		for (int i=1;i<=n;i++) fa[i]=i;
		for (int i=1;i<=n;i++)	
			for (int j=i+1;j<=n;j++)
			{
				if (gcd(a[i],a[j])!=1) 
				{
					int x=find(i),y=find(j);
					//printf("%d %d\n",i,j);
					if (x!=y) fa[x]=y;
				}
			}
		//printf("%d\n",gcd(8952,5858));
		memset(check,0,sizeof(check));
		int cnt=0;
		for (int i=1;i<=n;i++) 
			if (!check[find(i)]) 
			{
				check[fa[i]]=1;
				++cnt;
			}
		printf("%lld\n",(qpow(2,cnt)-2)%mod);
	}
}
int main()
{
//	freopen("x.in","r",stdin);
//	freopen("x.out","w",stdout);
	t=read();
	while (t--)
	{
		init();
		n=read();
		bool flag=true;
		for (int i=1;i<=n;i++) 
		{
			scanf("%d",a+i);
			if (a[i]>2) flag=false;
			pre(a[i]);
			if (a[i]==1) ++pnt;
		}
		//task::main();
		if (n>15&&!flag) 
		{
			task::main();
			continue;
		}
		dfs(1);
		sort(pr+1,pr+1+tot);
		//现在的ans是除了1之外不存在空的方案数 
		if (!pnt) {printf("%lld\n",ans);continue;}
		(ans*=qpow(2,pnt))%=mod; 
		//除了1之外可以为空 
		if (ans!=0) (ans+=2*qpow(2,pnt))%=mod;
		else (ans+=qpow(2,pnt))%=mod;
		(ans-=2)%=mod;//减掉有一边全是空的情况 
		printf("%lld\n",ans);
	}
	return 0;
}
