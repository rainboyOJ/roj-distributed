#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int mod=1e9+7,N=1e5+10,iv=(mod+1)/2;
inline int ksm(int x,int y){
	int ret=1;
	for(;y;y>>=1,x=1ll*x*x%mod) if(y&1) ret=1ll*ret*x%mod;
	return ret;
}
inline int add(int x,int y){return (x+y>=mod)?x+y-mod:x+y;}
inline int dec(int x,int y){return (x-y<0)?x-y+mod:x-y;} 
int n,x[N],f[N],m,id[N],vis[N],stk[N],pos[N];
ll k;
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;++i) scanf("%d",&x[i]),f[i]=dec(x[i],x[i-1]),id[i]=i;
	scanf("%d%lld",&m,&k);
	for(int i=1,x;i<=m;++i) scanf("%d",&x),swap(id[x],id[x+1]);
	int del=ksm(2,1ll*m*(k%(mod-1))%(mod-1));
	for(int i=1;i<=n;++i){
		if(!vis[i]){
			int now=i,top=0;
			while(!vis[now]){
				vis[now]=1;stk[top++]=now;
				now=id[now];
			}
			for(int i=0;i<top;++i) x[stk[i]]=f[stk[(i+k)%top]];
		}
	}
	for(int i=1;i<=n;++i) x[i]=add(x[i-1],x[i]),printf("%d ",1ll*x[i]*del%mod);
	return 0;
}
