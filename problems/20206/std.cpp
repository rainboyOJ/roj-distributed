#include<bits/stdc++.h>

typedef long long ll;
typedef unsigned long long ull;

using namespace std;

const int MAXN=1E6+10;

char *TT,*mo,but[(1<<15)+2];
#define getchar() ((TT==mo&&(mo=((TT=but)+fread(but,1,1<<15,stdin)),TT==mo))?-1:*TT++)//*/
inline int rd() {
	int x;int c;while(!isdigit(c=getchar()));x=c-'0';
	while(isdigit(c=getchar()))x=x*10+(c-'0');return x;
}

int n,fa[MAXN];
set<int> S[MAXN];
map<ll,int> M;
queue<pair<int,int> > q;

int find(int x){return x==fa[x]?x:fa[x]=find(fa[x]);}

ll get(int u,int v)
{
	if(u>v)
		swap(u,v);
	return 1ll*MAXN*u+v;
}

void Add_Edge(int u,int v)
{
	S[u].insert(v);
	S[v].insert(u);
	if(++M[get(u,v)]==2)
		q.emplace(u,v);
}

void Erase_Edge(int u,int v)
{
	S[u].erase(v);
	S[v].erase(u);
	M.erase(get(u,v));
}

int main()
{
    freopen("ants.in","r",stdin);
    freopen("ants.out","w",stdout);
	ios::sync_with_stdio(false);
	n=rd();
	for(int i=1;i<=n;i++)
		fa[i]=i;
	for(int i=1,u,v;i<=2*n-2;i++)
	{
		u=rd(),v=rd();
		Add_Edge(u,v);
	}
	for(int i=1;i<n;i++)
	{
		// if(i%10000==0)
			// cerr<<i<<' '<<clock()<<endl;
		if(q.empty())
			return puts("NO"),0;
		int x=find(q.front().first),y=find(q.front().second);
		q.pop();
		if(S[x].size()<S[y].size())
			swap(x,y);
		Erase_Edge(x,y);
		for(set<int>::iterator it=S[y].begin(),nxt;it!=S[y].end();it=nxt)
		{
			int v=*it;
			nxt=it;nxt++;
			Erase_Edge(y,v);
			Add_Edge(x,v);
		}
		fa[y]=x;
	}
	puts("YES");
}