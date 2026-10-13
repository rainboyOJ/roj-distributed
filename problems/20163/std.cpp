#include<iostream>
#include<algorithm>
#include<cstring>
#include<cstdio>
#include<bitset>
#include<cmath>
#include<ctime>
#include<queue>
#include<map>
#include<set>

#define fi first
#define se second
#define max Max
#define min Min
#define abs Abs
#define lc (x<<1)
#define rc (x<<1|1)
#define mid ((l+r)>>1)
#define lowbit(x) (x&(-x))
#define fan(x) (((x-1)^1)+1)
#define mp(x,y) make_pair(x,y)
#define clr(f,n) memset(f,0,sizeof(int)*(n))
#define cpy(f,g,n) memcpy(f,g,sizeof(int)*(n))
#define INF 0x3f3f3f3f3f3f3f3f

using namespace std;

#include<cctype>   //һ��Ҫ��cctype������ 

const int MB=1<<20;
struct FastIO
{
	char ib[MB+100],*p,*q;
	char ob[MB+100],*r,stk[128];
	int tp;
	
	FastIO(){p=q=ib,r=ob,tp=0;}
	~FastIO(){fwrite(ob,1,r-ob,stdout);} //�����������Զ�flush 
	
	char read_char() //����һ���ַ���ע������հ��ַ�������ո���
	{
		if(p==q)
		{
			p=ib,q=ib+fread(ib,1,MB,stdin);
			if(p==q)return 0;
		}
		return *p++;
	}
	template<typename T>
	void read_int(T& x) //����һ�����ͱ�����int,long long֮��Ķ��ܶ��� 
	{
		char c=read_char(),l=0;
		for(x=0;!isdigit(c);c=read_char())l=c;
		for(;isdigit(c);c=read_char())x=x*10-'0'+c;
		if(l=='-')x=-x;
	}
	
	void write_char(char c) //���һ���ַ� 
	{
		if(r-ob==MB)r=ob,fwrite(ob,1,MB,stdout);
		*r++=c;
	}
	template<typename T>
	void write_int(T x) //���һ�����ͱ�����int,long long֮��Ķ������ 
	{
		if(x<0)write_char('-'),x=-x;
		do stk[++tp]=x%10+'0';
		while(x/=10);
		while(tp)write_char(stk[tp--]);
	}
}IO;

inline void write(int x)
{
	if(x<0) putchar('-'),x=-x;
	if(x/10) write(x/10);
	putchar((char)(x%10)+'0');
}

template<typename T>inline T Abs(T a){return a>0?a:-a;};
template<typename T,typename TT>inline T Min(T a,TT b){return a<b?a:b;}
template<typename T,typename TT> inline T Max(T a,TT b){return a<b?b:a;}

const int N=1e6+5;
int n,m,vis[N],in[N],st[N],ok[N],top,col;

struct Edge
{
	int u,v,ne;
}e[N*2];
int head[N],tot;

inline void add(int u,int v);
void dfs(int u,int ls);

signed main()
{
	freopen("dag.in","r",stdin);
	freopen("dag.out","w",stdout);
	IO.read_int(n);
	IO.read_int(m);
	for(int i=1;i<=m;++i)
	{
		int u,v;
		IO.read_int(u);
		IO.read_int(v);
		add(u,v);
	}
	for(int i=1;i<=n;++i)
		col=i,dfs(i,-1);
	int sum=0;
	for(int i=1;i<=m;++i)
		sum+=(!ok[i]);
	IO.write_int(sum);
	IO.write_char('\n');
	for(int i=1;i<=m;++i)
		if(!ok[i])
		{
			IO.write_int(e[i].u);
			IO.write_char(' ');
			IO.write_int(e[i].v);
			IO.write_char('\n');
		}
	return 0;
}

inline void add(int u,int v)
{
	e[++tot]=(Edge){u,v,head[u]};
	head[u]=tot;
}

void dfs(int u,int ls)
{
	in[u]=1;
	for(int &i=head[u];i;i=e[i].ne)
	{
		int v=e[i].v;
		if(ok[i]) continue;
		if(in[v])
		{
			ok[i]=1;
			int x,tmp=top;
			do
			{
				x=st[tmp--];
				ok[x]=1;
			}while(e[x].u!=v);
			break;
		}
		else
		{
			st[++top]=i;
			dfs(v,i);--top;
		}
		if(ok[ls])
			break;
	}
	in[u]=0;
}