#include <bits/stdc++.h>
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
}
using namespace iobuff;
inline int getc(){
	char ch=gc();
	while(ch<'A'||ch>'C')ch=gc();
	return ch-'A';
}
const int N=2e5+5;
struct per{
	char p[3];
	inline void init(){p[0]=0;p[1]=1;p[2]=2;}
	inline char& operator [](int x){return p[x];}
};
per base[3];
const int P[6][3]={{0,1,2},{1,0,2},{0,2,1},{1,2,0},{2,0,1},{2,1,0}};
int rk[3][3][3];
inline per operator +(per a,per b){
	per ret;
	ret[0]=b[a[0]];
	ret[1]=b[a[1]];
	ret[2]=b[a[2]];
	return ret;
}
inline bool isorg(per a){return a[0]==0&&a[1]==1&&a[2]==2;}
int pre[3],cur[3];
int a[N];
namespace SGT{
	per trans[N<<2][6],buc[6];
	per tag[N<<2];
	#define lid (id<<1)
	#define rid (id<<1|1)
	#define mid ((l+r)>>1)
	inline void add(int id,per t){
		pre[t[0]]=0;pre[t[1]]=1;pre[t[2]]=2;
		cur[pre[0]]=0;
		cur[pre[1]]=1;
		cur[pre[2]]=2;
		buc[0]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		cur[pre[0]]=1;
		cur[pre[1]]=0;
		cur[pre[2]]=2;
		buc[1]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		cur[pre[0]]=0;
		cur[pre[1]]=2;
		cur[pre[2]]=1;
		buc[2]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		cur[pre[0]]=1;
		cur[pre[1]]=2;
		cur[pre[2]]=0;
		buc[3]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		cur[pre[0]]=2;
		cur[pre[1]]=0;
		cur[pre[2]]=1;
		buc[4]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		cur[pre[0]]=2;
		cur[pre[1]]=1;
		cur[pre[2]]=0;
		buc[5]=trans[id][rk[cur[0]][cur[1]][cur[2]]];
		trans[id][0]=buc[0];
		trans[id][1]=buc[1];
		trans[id][2]=buc[2];
		trans[id][3]=buc[3];
		trans[id][4]=buc[4];
		trans[id][5]=buc[5];
		tag[id]=tag[id]+t;
	}
	inline void pushdown(int id){
		if(isorg(tag[id]))return;
		add(lid,tag[id]);
		add(rid,tag[id]);
		tag[id].init();
	}
	inline void update(int id){
		for(int i=0;i<6;++i)trans[id][i]=trans[lid][i]+trans[rid][i];
	}
	void build(int id,int l,int r){
		tag[id].init();
		if(l==r){
			for(int i=0;i<6;++i)
				trans[id][i]=base[P[i][a[l]]];
			return;
		}
		build(lid,l,mid);
		build(rid,mid+1,r);
		update(id);
	}
	void modify(int id,int l,int r,int L,int R,per p){
		if(L<=l&&r<=R){add(id,p);return;}
		pushdown(id);
		if(L<=mid)modify(lid,l,mid,L,R,p);
		if(R>mid)modify(rid,mid+1,r,L,R,p);
		update(id);
	}
	per query(int id,int l,int r,int L,int R){
		if(L<=l&&r<=R)return trans[id][0];
		pushdown(id);
		if(R<=mid)return query(lid,l,mid,L,R);
		if(L>mid)return query(rid,mid+1,r,L,R);
		else return query(lid,l,mid,L,R)+query(rid,mid+1,r,L,R);
	}
}
int n,m;
int main(){
	for(int i=0;i<3;++i)for(int j=0;j<3;++j)base[i][j]=i;
	base[0][2]=2;base[1][0]=0;base[2][1]=1;
	for(int i=0;i<3;++i)for(int j=0;j<3;++j)for(int p=0;p<3;++p){
		if(i==j||j==p||i==p)continue;
		for(int k=0;k<6;++k)if(P[k][0]==i&&P[k][1]==j&&P[k][2]==p)
			rk[i][j][p]=k;
	}
	read(n);read(m);
	for(int i=1;i<=n;++i)a[i]=getc();
	SGT::build(1,1,n);
	int opt,l,r,x,y;
	per add;
	while(m--){
		read(opt);read(l);read(r);x=getc();
		if(!opt){
			y=getc();
			add.init();
			add[x]=y;add[y]=x;
			SGT::modify(1,1,n,l,r,add);
		}else{
			pc('A'+SGT::query(1,1,n,l,r)[x]);
			pc('\n');
		}
	}
	flush();
	return 0;
}