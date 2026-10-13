#include<cstdio>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
const int o=1010;
int T,q,n,k,f[o][o],c[o][o];
int main(){
	read(T);read(q);
	n=k=300;
	for(int i=c[0][0]=1;i<=n;++i)
		for(int j=c[i][0]=1;j<=i;++j) c[i][j]=(c[i-1][j-1]+c[i-1][j])%q;
	for(int i=0;i<=k;++i) f[0][i]=f[1][i]=1;
	for(int i=2;i<=n;++i) for(int j=f[i][0]=1;j<=k;++j)
		for(int $=1;$<=i;++$) f[i][j]=(f[i][j]+f[$-1][j-1]*1ll*c[i-1][$-1]%q*f[i-$][j-1])%q;
	for(;T--;printf("%d\n",f[n][k-1])) read(n),read(k);
	return 0;
}