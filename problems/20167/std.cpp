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
#define ll long long
const ll inf=1e18;
const int N=1e6+5;
ll a[N],sum,mx;
int cnt,pre,suf,n;
bool flag=0;
inline int calc(int x){return x?(x>>1)+1:0;}
int main(){
	read(n);
	for(int i=1;i<=n;++i){
		read(a[i]);
		if(a[i]>=0)flag=1;
	}
	cnt=n;
	if(!flag){
		sum=-inf;
		for(int i=1;i<=n;++i){
			if(a[i]>sum){
				sum=a[i];
				cnt=calc(i-1)+calc(n-i);
			}else if(a[i]==sum){
				cnt=min(cnt,calc(i-1)+calc(n-i));
			}
		}
		printf("%lld\n%d",sum,cnt);
		return 0;
	}
	pre=n;suf=0;sum=0;
	ll ans=0;
	for(int i=1;i<=n;i+=2){
		if(a[i]>=0){
			pre=min(pre,i);
			suf=max(suf,i);
			sum+=a[i];
			if(sum>ans){
				ans=sum;
				cnt=calc(pre-1)+calc(n-suf)+((suf-pre)>>1);
			}else if(sum==ans){
				cnt=min(cnt,calc(pre-1)+calc(n-suf)+((suf-pre)>>1));
			}
		}
	}
	pre=n;suf=0;sum=0;
	for(int i=2;i<=n;i+=2){
		if(a[i]>=0){
			pre=min(pre,i);
			suf=max(suf,i);
			sum+=a[i];
			if(sum>ans){
				ans=sum;
				cnt=calc(pre-1)+calc(n-suf)+((suf-pre)>>1);
			}else if(sum==ans){
				cnt=min(cnt,calc(pre-1)+calc(n-suf)+((suf-pre)>>1));
			}
		}
	}
	printf("%lld\n%d",ans,cnt);
	return 0;
}