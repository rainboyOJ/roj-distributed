#include<cstdio>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
const int o=1010;
int n,m,a[o],fa[o],ans[o],h[o],cnt;bool vis[o][o];
struct Edge{int v,p;}e[o*o];
inline void ad(int U,int V){e[++cnt].v=V;e[cnt].p=h[U];h[U]=cnt;}
int fr(int x){return fa[x]==x?x:fa[x]=fr(fa[x]);}
inline void merge(int x,int y){if((x=fr(x))^(y=fr(y))) fa[x]=y;}
int main(){
	read(n);read(m);
	for(int i=1;i<=n;++i) fa[i]=i;
	for(int i,j,k,t;m--;){
		read(i);read(j);read(k);
		for(int p1=i,p2=j;p1<i+k;++p1,++p2) merge(p1,p2);
		if(i+k<=n&&j+k<=n) ad(i+k,j+k),ad(j+k,i+k);
	}
	for(int i=1;i<=n;++i) for(int j=h[i];j;j=e[j].p)
		if(fr(i)==fr(e[j].v)){printf("-1");return 0;}
	for(int i=1;i<=n;++i) for(int j=h[i];j;j=e[j].p) ad(fr(i),fr(e[j].v)); 
	for(int i=1,j;i<=n;++i){
		if(!ans[j=fr(i)]) for(ans[j]=1;vis[j][ans[j]];++ans[j]);
		ans[i]=ans[j];
		for(int k=h[fr(i)];k;k=e[k].p) vis[fr(e[k].v)][ans[i]]=1;
	}
	for(int i=1;i<=n;++i) printf("%d ",ans[i]-1);
	return 0;
}