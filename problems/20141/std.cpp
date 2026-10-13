#include<bits/stdc++.h>
using namespace std;
namespace iobuff{
	const int LEN=1000000;
	char in[LEN+5],out[LEN+5];
	char *pin=in,*pout=out,*ed=in,*eout=out+LEN;
	inline char gc(void){
		return pin==ed&&(ed=(pin=in)+fread(in,1,LEN,stdin),ed==in)?EOF:*pin++;
	}
	inline void pc(char c){
		pout==eout&&(fwrite(out,1,LEN,stdout),pout=out);
		(*pout++)=c;
	}
	inline void flush(){fwrite(out,1,pout-out,stdout),pout=out;}
	template<typename T> inline void read(T &x){
		static int f;
		static char c;
		c=gc(),f=1,x=0;
		while(c<'0'||c>'9') f=(c=='-'?-1:1),c=gc();
		while(c>='0'&&c<='9') x=10*x+c-'0',c=gc();
		x*=f;
	}
	template<typename T> inline void putint(T x,char div){
		static char s[25];
		static int top;
		top=0;
		x<0?pc('-'),x=-x:0;
		while(x) s[top++]=x%10,x/=10;
		!top?pc('0'),0:0;
		while(top--) pc(s[top]+'0');
		pc(div);
	}
}
const int N=2e5+5;
int p[N<<1],q[N<<1],n,ans,tr[N<<2],lzy[N<<2];
inline void up(int x){tr[x]=min(tr[x<<1],tr[x<<1|1]);}
inline void down(int x){
	if(!lzy[x])return ;
	tr[x<<1]+=lzy[x];lzy[x<<1]+=lzy[x];
	tr[x<<1|1]+=lzy[x];lzy[x<<1|1]+=lzy[x];
	lzy[x]=0;
	return ;
}
void build(int now=1,int l=1,int r=n){
	tr[now]=2*l;lzy[now]=0;
	if(l==r)return ;
	int mid=(l+r)>>1;
	build(now<<1,l,mid);
	build(now<<1|1,mid+1,r);
}
inline void upd(int x,int y,int now=1,int l=1,int r=n){
	if(x<=l){tr[now]+=y;lzy[now]+=y;return ;}
	if(l==r)return ;
	int mid=(l+r)>>1;
	down(now);
	upd(x,y,now<<1|1,mid+1,r);
	if(x<=mid)upd(x,y,now<<1,l,mid);
	up(now);
}
inline void mdf(int x,int y){
	if(x==n+1)return ;
	x=min(2*n+2-x,x);
	upd(x,y);
}
using iobuff::read;
int main(){
    freopen("list.in","r",stdin);
    freopen("list.out","w",stdout);
	read(n);
	for(int i=1;i<=n*2+1;i++){
		read(p[i]);q[p[i]]=i;
	}build();
	for(int i=1,j=1;i<=2*n+1;i++){
		while(j<=2*n+1){
			mdf(q[j],-2);
			if(tr[1]<0){
				mdf(q[j],2);
				break;
			}
			j++;
		}
		ans=max(ans,j-i);
		mdf(q[i],2);
	}
	printf("%d\n",ans);
	return 0;
}