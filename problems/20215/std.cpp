#include<cstdio>
#include<algorithm>
using namespace std;
typedef unsigned long long ull;
typedef unsigned int uint;
inline uint fast_pow(uint x,uint n,uint mod){
	uint ret=1;
	for(uint p=1;p<=n;p<<=1,x=(ull)x*x%mod){
		if(n&p) ret=(ull)ret*x%mod;
		if((ull)p+p>n) break;
	}
	return ret;
}
int main(){
	int T; scanf("%d",&T);
	while(T--){
		uint m,p; scanf("%u%u",&m,&p);
		if(m>=p) puts("0");
		else if(T<1000&&p<=1000000){
			uint ans=1;
			for(uint i=1;i<=m;++i)
				ans=(ull)ans*i%p;
			printf("%u\n",ans);
		}else{
			uint ans=p-1;
			for(uint i=p-1;i>m;--i)
				ans=(ull)ans*fast_pow(i,p-2,p)%p;
			printf("%u\n",ans);
		}
	}
	return 0;
}