#include<bits/stdc++.h>
#define LL long long
using namespace std;
LL a,b,c,P;
LL Pow(LL x,LL kx){
	LL y=1;
	while(kx){
		if(kx & 1) y=y*x%P;
		kx>>=1; x=x*x%P;
	}
	return y;
}
LL s1(LL n,LL c){
	if(!n) return 1;
	LL bf=s1(n>>1,c); bf=(bf+Pow(Pow(10,(n>>1)),c)*(bf-1+P))%P;
	if(n & 1) (bf+=Pow(Pow(10,n),c))%=P;
	return bf;
}
LL s2(LL n){
	if(!n) return 1;
	LL bf=s2(n>>1); bf=(bf+Pow(10,n>>1)*(bf-1+P)%P)%P;
	if(n & 1) (bf+=Pow(10,n))%=P;
	return bf;
}
int main(){
	scanf("%lld%lld%lld",&a,&b,&P); c=__gcd(a,b); a/=c; b/=c;
	LL res=s1(a-1,c)*s1(b-1,c)%P*s2(c-1)%P;
	printf("%lld",res);
	return 0;
}
