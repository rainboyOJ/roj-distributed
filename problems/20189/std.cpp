#include<cstdio>
#include<vector>
#include<utility>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
const int o=5e5+10;
int n,q,a[o],rev[o],b[o],s[o*8],ans[o],f[o];vector<pair<int,int> > v[o];vector<int> g[o];bool vis[o*2];
inline int lowbit(int x){return x&-x;}
inline void modify(int pos){for(;pos<=n;pos+=lowbit(pos)) ++b[pos];}
inline int query(int pos){int res=0;for(;pos;pos-=lowbit(pos)) res+=b[pos];return res;}
inline void chg(int pos,int val){
	if(vis[pos]&&val>0) return;
	if(!vis[pos]&&val<0) return;
	vis[pos]^=1;
	for(int id=1,l=1,r=n*2,md;1;){
		s[id]+=val;id=id<<1;
		if(l==r) return;
		if(pos<=(md=l+r>>1)) r=md;
		else l=md+1,id|=1;
	}
}
inline int ask(int pos){
	for(int id=1,l=1,r=n*2,md;1;){
		if(l==r) return l;
		md=l+r>>1;
		if(s[id<<1]>=pos) r=md,id<<=1;
		else pos-=s[id<<1],l=md+1,id=(id<<1)|1;
	}
}
int main(){
	freopen("bubble.in","r",stdin);
	freopen("bubble.out","w",stdout);
	read(n);
	for(int i=1;i<=n;++i)
		read(a[i]),g[rev[a[f[a[i]]=i]]=query(n-a[i]+1)].push_back(i),modify(n-a[i]+1);
	for(int i=1;i<=n;++i) b[i]=0;
	read(q);
	for(int i=1,k,x;i<=q;++i){
		read(k);read(x);
		if(rev[x]>=k) ans[i]=f[x]-k;
		else v[k].push_back(make_pair(x,i));
	}
	for(int i=0;i<n;chg(++i,-1),chg(i+n,1)){
		for(int j=0,k=v[i].size();j<k;++j) ans[v[i][j].second]=ask(query(v[i][j].first))-i;
		for(int j=0,k=g[i].size();j<k;++j) modify(a[g[i][j]]),chg(g[i][j],1);
	}
	for(int i=1;i<=q;++i) printf("%d\n",ans[i]);
	return 0;
}