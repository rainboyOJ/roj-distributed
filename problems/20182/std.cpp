#include <bits/stdc++.h>
#define fi first
#define se second
#define mp make_pair
#define lc pos<<1
#define rc pos<<1|1
using namespace std;
typedef long long ll;
typedef pair<ll,int> pl;
typedef pair<ll,pair<int,int> > pli;
const int N=1e5+5;
int n,m,a[N];
ll tag[N<<2];
struct sb{
	pl mi,mx;pli ans;
	sb operator + (const sb&x) const{
		sb res;
		res.mi=min(mi,x.mi);res.mx=max(mx,x.mx);
		res.ans=max(mp(mx.fi-x.mi.fi,mp(mx.se,x.mi.se)),max(ans,x.ans));
		return res;
	}
}t[N<<2];
void pushup(int pos) {t[pos]=t[lc]+t[rc];}
void inc(int pos,ll x) {tag[pos]+=x;t[pos].mi.fi+=x;t[pos].mx.fi+=x;}
void pushdown(int pos){
	if(tag[pos]) inc(lc,tag[pos]),inc(rc,tag[pos]),tag[pos]=0;
}
void build(int l,int r,int pos){
	if(l==r) {t[pos].mi=t[pos].mx=mp(a[l],l);t[pos].ans=mp(0,mp(l,l));return;}
	int mid=l+r>>1;build(l,mid,lc);build(mid+1,r,rc);pushup(pos);
}
void add(int l,int r,int pos,int L,int R,int x){
	if(L<=l&&r<=R) return inc(pos,x);
	int mid=l+r>>1;pushdown(pos);
	if(L<=mid) add(l,mid,lc,L,R,x);if(R>mid) add(mid+1,r,rc,L,R,x);
	pushup(pos);
}
sb query(int l,int r,int pos,int L,int R){
	if(L<=l&&r<=R) return t[pos];
	int mid=l+r>>1;pushdown(pos);
	if(R<=mid) return query(l,mid,lc,L,R);
	if(L>mid) return query(mid+1,r,rc,L,R);
	return query(l,mid,lc,L,R)+query(mid+1,r,rc,L,R);
}
struct np{
	int l0,r0,l1,r1;pli s;
	np(int l0,int r0,int l1,int r1):l0(l0),r0(r0),l1(l1),r1(r1){}
	bool operator < (const np&x) const {return s<x.s;}
};
priority_queue<np> q;
void nxt(int l0,int r0,int l1,int r1){
	np x(l0,r0,l1,r1);
	if(l0==l1&&r0==r1) x.s=query(1,n,1,l0,r0).ans;
	else{
		sb ls=query(1,n,1,l0,r0),rs=query(1,n,1,l1,r1);
		x.s=mp(ls.mx.fi-rs.mi.fi,mp(ls.mx.se,rs.mi.se));
	}
	q.push(x);
}
signed main(){
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++) scanf("%d",&a[i]);
	build(1,n,1);
	while(m--){
		int op,x,y,k;scanf("%d%d%d%d",&op,&x,&y,&k);
		if(op==1) add(1,n,1,x,y,k);
		else{
			while(!q.empty()) q.pop();
			nxt(x,y,x,y);ll ans=0;
			while(k--){
				np x=q.top();q.pop();ans+=x.s.fi;
				int l=x.s.se.fi,r=x.s.se.se,l0=x.l0,l1=x.l1,r0=x.r0,r1=x.r1;
				if(l0==l1&&r0==r1){
					if(l0<l) nxt(l0,l-1,l0,l-1),nxt(l0,l-1,l,r0);
					if(l!=r) nxt(l,l,l,l);if(l+1<=r-1) nxt(l,l,l+1,r-1);
					if(r+1<=r0) nxt(l,l,r+1,r0);if(l+1<=r0) nxt(l+1,r0,l+1,r0);
				}else{
					if(l0<l) nxt(l0,l-1,l1,r1);if(l+1<=r0) nxt(l+1,r0,l1,r1);
					if(l1<r) nxt(l,l,l1,r-1);if(r+1<=r1) nxt(l,l,r+1,r1);
				}
			}
			printf("%lld\n",ans);
		}
	} 
	return 0;
}