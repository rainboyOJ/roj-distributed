#include<bits/stdc++.h>
using namespace std;
typedef long long ull;
ull gcd(ull a,ull b){ return b>0?gcd(b,a%b):a; }
void print(ull a,ull b,char end='\n'){
	ull d=gcd(a,b);
	a/=d; b/=d;
	if(b==1) printf("%lld",a);
	else printf("%lld/%lld",a,b);
	printf("%c",end);
}
int main(){
	int n; scanf("%d",&n);
	ull sum=0,sum2=0;
	for(int i=1;i<=n;++i){
		int x; scanf("%d",&x);
		sum+=x; sum2+=1ll*x*x;
		print(sum,1,' ');
		print(sum,i,' ');
		print(sum2*i-sum*sum,1ll*i*i,'\n');
	}
	return 0;
}