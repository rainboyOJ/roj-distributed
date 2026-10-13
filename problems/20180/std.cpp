#include<cstdio>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
inline long double Max(long double a,long double b){return a>b?a:b;}
const int o=1e6+10;
int n,h[o],cnt,a[o],fa[o];long double p[o],ans;
struct Edge{int v,p;}e[o];
inline void ad(int U,int V){e[++cnt].v=V;e[cnt].p=h[U];h[U]=cnt;}
struct Matrix{
	long double mat[3][3];
	Matrix operator*(Matrix A){
		Matrix B;
		for(int i=0;i<3;++i) for(int j=0;j<3;++j) B.mat[i][j]=0;
		for(int i=0;i<3;++i) for(int j=0;j<3;++j)
			for(int k=0;k<3;++k) B.mat[i][j]+=mat[i][k]*A.mat[k][j];
		return B;
	}
}m[o];
int main(){
	read(n);
	for(int i=2;i<=n;++i) read(fa[i]),ad(fa[i],i);
	for(int i=1;i<=n;++i) scanf("%Lf",&p[i]);
	for(int i=n;i;--i) for(int j=h[i];j;j=e[j].p) p[i]*=(1-p[e[j].v]);
	for(int i=1;i<=n;++i) read(a[i]);
	for(int i=1;i<=n;++i)
		m[i].mat[0][0]=m[i].mat[2][2]=1,m[i].mat[1][1]=-(m[i].mat[0][1]=p[fa[i]]/(1-p[i])),
		m[i].mat[1][2]=-(m[i].mat[0][2]=m[i].mat[0][1]*a[fa[i]]);
	m[1].mat[1][1]=1;
	for(int i=2;i<=n;++i) m[i]=m[i]*m[fa[i]];
	for(int i=1;i<=n;++i) ans+=Max(m[i].mat[0][2]+m[i].mat[1][2],0)*p[i];
	printf("%.6Lf",ans);
	return 0;
}