#include<bits/stdc++.h>
using namespace std;
const int N=10005,mod=998244353;
inline int add(int x,int y){return x+y>=mod?x+y-mod:x+y;}
inline int dec(int x,int y){return x-y<0?x-y+mod:x-y;}
struct Matrix
{
	int c[30][30],t;
	inline void pre(int tt,int d=0)
	{
		t=tt;
		for(int i=1;i<=t;++i)
			memset(c[i],0,sizeof(int)*(t+1));
		if(d)for(int i=1;i<=t;++i)c[i][i]=d;
	}
	inline Matrix operator*(const Matrix&rhs)const
	{
		Matrix ret;ret.pre(t);
		for(int i=1;i<=t;++i)
			for(int j=1;j<=t;++j)
			{
				long long res=0ll;
				for(int k=1;k<=t;++k)
					res+=1ll*c[i][k]*rhs.c[k][j]%mod;
				ret.c[i][j]=res%mod;
			}
		return ret;
	}
}P;
inline Matrix qpow(Matrix x,char*s,int p)
{
	Matrix ret;ret.pre(x.t,1);
	int f=1;
	for(;;x=x*x)
	{
		if(s[p]&1)ret=ret*x;
		for(int i=f,tg=0;i<=p;++i)
		{
			if(tg)s[i]+=10;
			tg=(s[i]&1);s[i]>>=1;
		}
		while(!s[f]&&f<=p)++f;
		if(f>p)break;
	}
	return ret;
}
char l[N],r[N];int ll,lr,m,ct,tmp[30],id[1005],st;
bool vis[1005];vector<int>ans;
void dfs(int u,int d)
{
	if(d>=m)
	{
		if(!vis[u])ans.push_back(u);
		vis[u]=1;return;
	}bool pp=0;
	for(int i=d;i<m;++i)
		if(u&(1<<i))
		{
			pp=1;
			if(i<m-1&&(u&(1<<(i+1))))
				dfs(u^(1<<i)^(1<<(i+1)),d+2);
			dfs(u,d+1);break;
		}
	if(!pp)dfs(u,m);
}bool pd[1005];
inline void bfs()
{
	queue<int>q;q.push(0);pd[0]=1;
	while(!q.empty())
	{
		int u=q.front();q.pop();
		tmp[++ct]=u,id[u]=ct;u^=st-1;
		memset(vis,0,sizeof(bool)*st);
		ans.clear();dfs(u,0);
		for(int v:ans)if(!pd[v])pd[v]=1,q.push(v);
	}
}
inline int work(bool tp)
{
	return qpow(P,tp?r:l,tp?lr:ll).c[ct+1][1];
}
int main()
{
    freopen("decoration.in", "r", stdin);
    freopen("decoration.out", "w", stdout);
	scanf("%s%s",l+1,r+1);
	ll=strlen(l+1),lr=strlen(r+1);
	for(int i=1;i<=ll;++i)l[i]^='0';
	for(int i=1;i<=lr;++i)r[i]^='0';
	int p=ll;while(!l[p])--p;
	--l[p++];while(p<=ll)l[p]=9,++p;
	scanf("%d",&m);st=1<<m;bfs();
	P.pre(ct+1);
	for(int i=1;i<=ct;++i)
	{
		memset(vis,0,sizeof(bool)*st);
		ans.clear();dfs(tmp[i]^(st-1),0);
		for(int u:ans)++P.c[id[u]][i];
	}
	for(int i=1;i<=ct;++i)P.c[ct+1][i]=P.c[1][i];
	P.c[ct+1][ct+1]=1;
	printf("%d",dec(work(1),work(0)));
	return 0;
}