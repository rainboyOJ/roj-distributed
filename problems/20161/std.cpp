#include <bits/stdc++.h>
#define to e[x][i]
using namespace std;
typedef long long ll;
const int N=1e5+5,inf=1e9;
int n,m,q,tot,fl,cnt,ans,f[N],r[N],h[N],a[N],sz[N],d[N],id[N],mx[2][N],mi[2][N];
vector<int> e[N];
int getf(int x) {return f[x]==x?x:f[x]=getf(f[x]);}
void ins(int x,int y){
	sz[x]+=sz[y];
	mi[0][x]=min(mi[0][x],mi[0][y]);mi[1][x]=min(mi[1][x],mi[1][y]);
	mx[0][x]=max(mx[0][x],mx[0][y]);mx[1][x]=max(mx[1][x],mx[1][y]);
}
void dfs1(int x,int fa){
	mi[0][x]=mi[1][x]=inf;mx[0][x]=mx[1][x]=0;
	sz[x]=1;r[x]=r[fa];d[x]=d[fa]^1;
	if(~id[x]) mi[d[x]^(id[x]&1)][x]=mx[d[x]^(id[x]&1)][x]=id[x];
	for(int i=0;i<e[x].size();i++)
		if(r[to]!=r[x]) dfs1(to,x),ins(x,to);
}
void dfs2(int x,int fa){
	h[x]=h[fa]^1;
	for(int i=0;i<e[x].size();i++)
		if(to!=fa){
			if(h[to]==-1){
				dfs2(to,x);
				if(fl==-1) return;
				if(fl){
					a[tot]=x;id[x]=tot++;
					if(fl==x) fl=-1;return;
				}
			}else if(h[x]^h[to]^1) {fl=to;a[tot]=x;id[x]=tot++;return;}
		}
}
void link(int x,int y){
	for(int i=x;getf(i)<y;i=getf(i)) f[getf(i)]=getf(i)+1,ans--;
}
void upd(int x){
	for(int i=0;i<2;i++)
		for(int j=0;j<2;j++) if(mi[i][x]<mx[j][x]){
			if(i^j) link(0,mi[i][x]),link(mx[j][x],tot);
			else link(mi[i][x],mx[j][x]);
		}
}
void add(int u,int v){
	scanf("%d%d",&u,&v);
	e[u].push_back(v);e[v].push_back(u);
	if(r[u]!=r[v]){
		if(sz[r[u]]<sz[r[v]]) swap(u,v);
		dfs1(v,u);ins(r[u],v);upd(r[u]);
		return;
	}
	if(d[u]!=d[v]) return;
	if(fl){
		if(~m) while(m--) scanf("%d%d",&u,&v);
		if(~q) while(q--){
			int op;scanf("%d",&op);
			if(op==2) puts("yes");else if(op==3) puts("0");
			else scanf("%d%d",&u,&v);
		}
		exit(0);
	}
	dfs2(u,h[0]=0);ans=tot;fl=1;
	for(int i=1;i<=tot;i++) f[i]=i;
	for(int k=0;k<tot;k++){
		int x=a[k];vector<int> t;
		for(int i=0;i<e[x].size();i++)
			if(to!=a[(k+1)%tot]&&to!=a[(k+tot-1)%tot]) t.push_back(to);
		e[x]=t;
	}
	memset(r,0,sizeof(r));
	for(int i=1;i<=n;i++)
		if(!r[i]) dfs1(i,r[i]=i),upd(i);
}
signed main(){
    freopen("charlie.in","r",stdin);
    freopen("charlie.out","w",stdout);
	memset(id,-1,sizeof(id));memset(h,-1,sizeof(h));
	scanf("%d%d%d",&n,&m,&q);cnt=m;
	for(int i=1;i<=n;i++) r[i]=i,sz[i]=1;
	while(m--) {int u,v;add(u,v);}
	while(q--){
		int op,u,v;scanf("%d",&op);
		if(op==1) add(u,v),cnt++;
		else if(op==2) puts(fl?"yes":"YES");
		else printf("%d\n",fl?ans:cnt);
	}
	return 0;
}