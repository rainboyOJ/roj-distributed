#include <bits/stdc++.h>
using namespace std;
inline int read(){
	int s=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9')s=(s<<3)+(s<<1)+ch-'0',ch=getchar();
	return s*f;
}
const int N=(1<<20)+5;
int n,m,p[N],tot,a[N],b[N];
#define ll long long
namespace SGT{
	int ls[N<<1],rs[N<<1],tag[N<<1];
	ll *sum[N<<1],*d[N<<1];
	#define lid ls[id]
	#define rid rs[id]
	#define mid ((l+r)>>1)
	void build(int id,int l,int r,int dep){
		sum[id]=new ll[dep+1];d[id]=new ll[dep+1];
		if(l==r)return;
		lid=id<<1;rid=id<<1|1;
		build(lid,l,mid,dep-1);build(rid,mid+1,r,dep-1);
		for(int i=0;i<dep-1;++i)
			sum[id][i]=sum[lid][i]+sum[rid][i],
			d[id][i]=d[lid][i]+d[rid][i];
		sum[id][dep-1]=d[id][dep-1]=0;
		int i=l,j=mid+1,k=0,pre=0;
		for(;j<=r;++j){
			while(i<=mid&&a[i]<a[j])b[++k]=a[i++];
			if(j==mid+1||a[j]!=a[j-1]){
				pre=0;
				while(i<=mid&&a[i]==a[j])b[++k]=a[i++],++pre;
			}
			d[id][dep-1]+=pre;
			sum[id][dep-1]+=mid-i+1;
			b[++k]=a[j];
		}
		while(i<=mid)b[++k]=a[i++];
		memcpy(a+l,b+1,k<<2);
	}
	inline void update(int id,int dep){
		for(int i=0;i<dep-1;++i)sum[id][i]=sum[lid][i]+sum[rid][i];
	}
	inline void cover(int id,int tg,int dep){
		for(int i=0;i<dep;++i)
			if(tg&(1<<i))
				sum[id][i]=(1ll<<(dep+i-1))-d[id][i]-sum[id][i];
		if(tg&(1<<(dep-1)))swap(lid,rid);
		tag[id]^=tg;
	}
	inline void pushdown(int id,int dep){
		if(!tag[id])return;
		tag[id]&=(1<<(dep-1))-1;
		cover(lid,tag[id],dep-1);
		cover(rid,tag[id],dep-1);
		tag[id]=0;
	}
	void modify(int id,int l,int r,int dep,int L,int R,int q){
		if(L<=l&&r<=R){
			cover(id,(1<<q)-1,dep);
			return;
		}
		pushdown(id,dep);
		if(L<=mid)modify(lid,l,mid,dep-1,L,R,q);
		if(R>mid)modify(rid,mid+1,r,dep-1,L,R,q);
		update(id,dep);
	}
	inline ll query(){
		ll ret=0;
		for(int i=0;i<n;++i)ret+=sum[1][i];
		return ret;
	}
}
int main(){
	n=read();m=read();tot=(1<<n);
	for(int i=1;i<=tot;++i)a[i]=p[i]=read();
	SGT::build(1,1,tot,n);
	int l,r,q;
	while(m--){
		q=read();l=read();r=read();q=n-q;
		SGT::modify(1,1,tot,n,(l-1)*(1<<q)+1,r*(1<<q),q);
		printf("%lld\n",SGT::query());
	}
	return 0;
} 