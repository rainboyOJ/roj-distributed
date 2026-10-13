#include <cassert>
#include<bits/stdc++.h>
typedef unsigned int u32;
const int N=1e5+7,K=3;
int n,_l,_r,_t,_x;
struct node{
	u32 v[1<<K],a[K];
	node*lc,*rc;
	int L,R,M;
	void dn(){
		for(int i=0;i<K;++i)if(a[i]){
			lc->add(i,a[i]);
			rc->add(i,a[i]);
			a[i]=0;
		}
	}
	void add(int w,u32 x){
		a[w]+=x;
		for(int i=0,b=1<<w;i<(1<<K);++i)if(i&b)v[i]+=v[i-b]*x;
	}
	void up(){
		for(int i=0;i<(1<<K);++i)v[i]=lc->v[i]+rc->v[i];
	}
	void op(){
		if(_l<=L&&R<=_r)return add(_t,_x);
		dn();
		if(_l<=M)lc->op();
		if(_r>M)rc->op();
		up();
	}
}ns[N*2],*np=ns,*rt;
node*build(int L,int R){
	node*w=np++;
	w->L=L,w->R=R,w->v[0]=R-L+1;
	if(L<R){
		int M=w->M=(L+R)>>1;
		w->lc=build(L,M);
		w->rc=build(M+1,R);
	}
	return w;
}
struct seq{
	int a[N],s[N],sp,sgn;
	void init(int _sgn){
		sgn=_sgn;
		a[0]=sgn>0?1e9+1:-1;
		s[0]=sp=0;
	}
	void cal(int w,int t){
		_l=_r=w,_t=t,_x=a[w]*sgn,rt->op();
		while((_x=(a[w]-a[s[sp]])*sgn)>0){
			_l=s[sp-1]+1,_r=s[sp],rt->op();
			--sp;
		}
		s[++sp]=w;
	}
}mx[K],mn[K];
int main(){
	freopen("team.in","r",stdin);
	freopen("team.out","w",stdout);
	assert(scanf("%d",&n)==1&&1<=n&&n<=100000);
	rt=build(1,n);
	for(int t=0;t<K;++t){
		mx[t].init(1);
		mn[t].init(-1);
		for(int i=1,x;i<=n;++i){
			assert(scanf("%d",&x)==1&&1<=x&&x<=1000000000);
			mx[t].a[i]=mn[t].a[i]=x;
		}
	}
	u32 ans=0;
	for(int i=1;i<=n;++i){
		for(int t=0;t<K;++t){
			mx[t].cal(i,t);
			mn[t].cal(i,t);
		}
		ans+=rt->v[(1<<K)-1];
	}
	printf("%u\n",ans);
	return 0;
}