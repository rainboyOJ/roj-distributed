#include<bits/stdc++.h>
#define loop(i,from,to) for(int i=(from);i<=(to);++i)
#define rloop(i,from,to) for(int i=(from);i>=(to);--i)
#define gloop(i,x) for(int i=head[x];i;i=suc[i])
using namespace std;
const int maxn=4e6,maxbuf=2e6;
int n,m,x,y,d,z,tot,ans,a[maxn+1],b[maxn+1],top[maxn+1],head[maxn+1],suc[maxn+1],to[maxn+1],len[maxn+1];
namespace IO{
	inline char getchar(){
		static char ibuf[maxbuf+1],*cur=ibuf+maxbuf;
	    return (cur==ibuf+maxbuf)?fread(cur=ibuf,1,maxbuf,stdin),*cur++:*cur++;
	}
	void read(int &x){
		x=0;
		char t=getchar();
		while(!isdigit(t))t=getchar();
		while(isdigit(t))x=x*10+t-'0',t=getchar();
		return;
	}
}
using namespace IO;
int find(int x){return x==top[x]?x:top[x]=find(top[x]);}
int main(){
    freopen("challenge.in","r",stdin);
    freopen("challenge.out","w",stdout);
	read(n),read(m);
	loop(i,1,n)read(a[i]),top[i]=i,a[i]+=a[i-1];
	loop(i,1,n)read(b[i]);
	loop(i,1,m)read(d),read(y),read(z),suc[++tot]=head[x+=d],head[x]=tot,to[tot]=y,len[tot]=z;
	ans=a[n];
	rloop(i,n,1){
		ans=min(ans,a[i]+b[0]);
		gloop(j,i){
			b[find(to[j])]-=len[j],b[0]+=len[j];
			for(int now=find(to[j]);b[now]<0;now=find(to[j]))b[top[now]=find(now-1)]+=b[now];
		}
		if(b[0]>=ans)break;
	}
	printf("%d",ans);
	return 0;
}