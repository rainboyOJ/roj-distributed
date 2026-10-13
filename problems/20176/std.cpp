#include<cstdio>
using namespace std;
template<class T>inline void read(T&a)
{char c=getchar();int f=1;for(;c>'9'||c<'0';c=getchar()) if(c=='-') f=-1;for(a=0;c<='9'&&c>='0';c=getchar()) a=a*10+c-48;a*=f;}
const int o=1e6+10;
int T,n,a[o],b[o],cnt,t1[o],t2[o];bool flg;
int main(){
	for(read(T);T--;){
		read(n);flg=cnt=0;
		for(int i=1;i<=n;++i) read(a[i]);
		for(int i=1;i<=n;++i) read(b[i]);
		for(int i=1,j,k;i<=n&&!flg;++i){
			for(j=i;j<=n&&a[j]-b[i];++j);
			if(j>n){printf("-1\n");flg=1;break;}
			for(--j;j>=i;--j)
				if(a[j]>a[j+1]) k=a[t1[++cnt]=j],a[j]=a[t2[cnt]=j+1],a[j+1]=k;
				else{printf("-1\n");flg=1;break;}
		}
		if(!flg){
			printf("0\n%d\n",cnt);
			for(int i=1;i<=cnt;++i) printf("%d %d\n",t1[i],t2[i]);
		}
	}
	return 0;
}