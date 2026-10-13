#include <bits/stdc++.h>
#define maxn 100005
using namespace std;
inline char nc(){
	static char buf[500005],*p1=buf,*p2=buf;
	return p1==p2&&(p2=(p1=buf)+fread(buf,1,500000,stdin),p1==p2)?EOF:*p1++;
}
inline int read(){
	char ch=nc(); int sum=0;
	for(;ch<'0'||ch>'9';ch=nc());
	while(ch>='0'&&ch<='9')sum=sum*10+ch-48,ch=nc();
	return sum;
}
int n,Q,a[maxn],pc[maxn]; bool ans[maxn];
struct node { int l,r,id; } q[maxn],T[maxn];
int A[maxn][31],O[maxn][31],c[maxn][31];
int ad[31],o[31],C[31];
void solve(int l,int r,int x,int y) {
	if(l>=r||x>y) return ; int mid=l+r>>1;
	for(int i=l;i<=r;i++) for(int j=0;j<=30;j++) A[i][j]=0x3fffffff,O[i][j]=c[i][j]=0;
	for(int i=mid+1;i<=r;i++) A[i][pc[i]]&=a[i],O[i][pc[i]]|=a[i],c[i][pc[i]]++,memcpy(A[i+1],A[i],124),memcpy(O[i+1],O[i],124),memcpy(c[i+1],c[i],124);
	for(int i=mid;i>=l;i--) A[i][pc[i]]&=a[i],O[i][pc[i]]|=a[i],c[i][pc[i]]++,memcpy(A[i-1],A[i],124),memcpy(O[i-1],O[i],124),memcpy(c[i-1],c[i],124);
	int pl=x-1,pr=y+1;
	for(int _=x;_<=y;_++) {
		if(q[_].r<=mid) T[++pl]=q[_]; else if(q[_].l>mid) T[--pr]=q[_];
		else {
			for(int i=0;i<=30;i++) ad[i]=A[q[_].l][i]&A[q[_].r][i],o[i]=O[q[_].r][i]|O[q[_].l][i],C[i]=c[q[_].l][i]+c[q[_].r][i];
			for(int i=0;i<=30;i++) if(ad[i]>=o[i]) {
				int L=0,R=0x3fffffff,cl=0,cr=0; for(int j=0;j<i;j++) L|=o[j],cl+=C[j]; for(int j=30;j>i;j--) R&=ad[j],cr+=C[j];
				ans[q[_].id]|=(C[i]==0)?(cl&&cr&&L==R):((C[i]==1)?((cl&&(L==(R&o[i])))||(cr&&(R==(L|o[i])))):((L|o[i])==(R&o[i])));
			}
		}
	} for(int i=x;i<=pl;i++) q[i]=T[i]; for(int i=pr;i<=y;i++) q[i]=T[i]; solve(l,mid,x,pl); solve(mid+1,r,pr,y);
}
int main() {
	n=read(),Q=read();
	for(int i=1;i<=n;i++) pc[i]=__builtin_popcount(a[i]=read());
	for(int i=1;i<=Q;i++) q[i].l=read(),q[i].r=read(),q[i].id=i;
	solve(1,n,1,Q);
	for(int i=1;i<=Q;i++) puts(ans[i]?"YES":"NO");
}