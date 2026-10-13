#include<cstdio>
#include<queue>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
const int o=5e4+10,dx[]={-1,0,1,0},dy[]={0,1,0,-1};
int n,m,k,q,col[o],vis[o],h[o],cnt;bool st[o];char s[o];queue<int> qx,qy;
struct Edge{int v,p;}e[o];
inline void ad(int U,int V){e[++cnt].v=V;e[cnt].p=h[U];h[U]=cnt;}
inline int hsh(int x,int y){return (x-1)*m+y;}
void dfs(int nw){for(int i=h[nw];i;i=e[i].p) if(vis[e[i].v]^cnt) vis[e[i].v]=cnt,dfs(e[i].v);}
int main(){
	read(n);read(m);read(k);read(q);
	for(int i=1;i<=n;++i){
		scanf("%s",s+1);
		for(int j=1;j<=m;++j) st[hsh(i,j)]=(s[j]^'.');
	}
	for(int i=1;i<=n;++i) for(int j=1;j<=m;++j) if(!st[hsh(i,j)]&&!col[hsh(i,j)])
		for(col[hsh(i,j)]=++cnt,qx.push(i),qy.push(j);!qx.empty();qx.pop(),qy.pop())
			for(int i=0,tx,ty;i<4;++i) if((tx=qx.front()+dx[i])&&(ty=qy.front()+dy[i]))
				if(tx<=n&&ty<=m&&!col[hsh(tx,ty)]&&!st[hsh(tx,ty)])
					col[hsh(tx,ty)]=cnt,qx.push(tx),qy.push(ty);
	cnt=0;
	for(int i1,i2,j1,j2;k--;){
		read(i1);read(i2);read(j1);read(j2);
		if((i1=col[hsh(i1,i2)])^(j1=col[hsh(j1,j2)])) ad(i1,j1);
	}
	cnt=0;
	for(int i1,i2,j1,j2;q--;){
		read(i1);read(i2);read(j1);read(j2);
		vis[i1=col[hsh(i1,i2)]]=++cnt;dfs(i1);
		printf("%d\n",vis[col[hsh(j1,j2)]]==cnt);
	}
	return 0;
}