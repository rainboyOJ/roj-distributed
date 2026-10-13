#include<bits/stdc++.h>
#define rep(i,a,b) for(int i=a;i<=b;i++)
using namespace std; char s[10][100];
inline int chk(int a,int b,int c,int d,int e,int f)
{
	int x=s[1][a]-'0',y=s[3][c]-'0',z=(s[5][e]-'0')*10+s[6][f]-'0',u=0,v=0;
	char op1=s[2][b],op2=s[4][d]; if(op1=='/'&&y==0) return 0;
	if(op1=='+') u=x+y,v=z; if(op1=='-') u=x-y,v=z;
	if(op1=='*') u=x*y,v=z; if(op1=='/') u=x,v=z*y;
	return op2=='='?u==v:(op2=='<'?u<v:(u>v));
}
int main()
{
	int n,ans=0,cnt=0; scanf("%d",&n); rep(i,1,6) scanf("%s",s[i]);
	rep(i,0,n-1) rep(j,0,n-1) rep(k,0,n-1) rep(t,0,n-1) rep(l,0,n-1)
	{ rep(p,cnt=0,n-1) cnt+=chk(p,(p+i)%n,(p+j)%n,(p+k)%n,(p+t)%n,(p+l)%n); ans=max(ans,cnt); }
	return !printf("%d\n",ans);
}
