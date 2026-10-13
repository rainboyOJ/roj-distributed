#include<bits/stdc++.h>
#define loop(i,from,to) for(int i=(from);i<=(to);++i)
#define rloop(i,from,to) for(int i=(from);i>=(to);--i)
#define rsloop(i,from,to,step) for(int i=(from);i>=(to);i-=(step))
using namespace std;
const int maxn=18;
int n,all,digit[maxn+1],a[1<<maxn],b[1<<maxn],c[1<<maxn],f[maxn+1][1<<maxn];
void read(int &x){
	x=0;
	char t=getchar();
	while(!isdigit(t))t=getchar();
	while(isdigit(t))x=x*10+t-'0',t=getchar();
	return;
}
void write(int x){
	digit[0]=0;
	do digit[++digit[0]]=x%10,x/=10;while(x);
	rloop(i,digit[0],1)putchar(digit[i]+'0');
	return;
}
void dfs(int depth,int now){
	c[now]=max(c[now],a[now]+f[depth][0]);
	for(int sub=all^now,comp=sub;sub;sub=comp&(sub-1))c[now|sub]=max(c[now|sub],a[now]+f[depth][sub]);
	loop(i,0,n-1){
		if(now&(1<<i))break;
		int to=now|(1<<i);
		for(int sub=all^to,comp=sub;sub;sub=comp&(sub-1))f[depth+1][sub]=max(f[depth][sub],f[depth][sub|(1<<i)]);
		f[depth+1][0]=max(f[depth][0],f[depth][1<<i]),dfs(depth+1,to);
	}
	return;
}
int main(){
    freopen("juanji.in","r",stdin);
    freopen("juanji.out","w",stdout);
	read(n),all=(1<<n)-1;
	loop(i,0,all)read(a[i]);
	loop(i,0,all)read(b[i]),f[0][i]=b[i];
	dfs(0,0);
	loop(i,0,all)write(c[i]),putchar(' ');
	return 0;
}