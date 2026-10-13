#include<bits/stdc++.h>
#define loop(i,from,to) for(int i=(from);i<=(to);++i)
using namespace std;
using ll=long long;
const int maxn=4000,mod=998244353,inf=0x3f3f3f3f;
int m,n,k,tot,ans,power[maxn+1],x[maxn+1],y[maxn+1],minx[3],miny[3],maxx[3],maxy[3];
void dfs(int step){
	if(step>n){loop(i,0,2)if(maxx[i]-minx[i]>k||maxy[i]-miny[i]>k)return;++ans;return;}
	loop(i,0,2){
		int t1=minx[i],t2=miny[i],t3=maxx[i],t4=maxy[i];
		minx[i]=min(minx[i],x[step]),miny[i]=min(miny[i],y[step]),maxx[i]=max(maxx[i],x[step]),maxy[i]=max(maxy[i],y[step]),dfs(step+1),
		minx[i]=t1,miny[i]=t2,maxx[i]=t3,maxy[i]=t4;
	}
	return;
}
int main(){
	freopen("history.in", "r", stdin);
	freopen("history.out", "w", stdout);
	scanf("%d%d%d",&m,&n,&k);
	loop(i,1,n)scanf("%d%d",&x[i],&y[i]);
	if(m==3&&n<=14){
		loop(i,0,2)minx[i]=miny[i]=inf,maxx[i]=maxy[i]=-inf;
		dfs(1),printf("%d",ans);
		return 0;
	}
	else if(m==2){
		power[0]=1,minx[0]=miny[0]=inf,maxx[0]=maxy[0]=-inf;
		loop(i,1,n)power[i]=(power[i-1]<<1)%mod,minx[0]=min(minx[0],x[i]),miny[0]=min(miny[0],y[i]),maxx[0]=max(maxx[0],x[i]),maxy[0]=max(maxy[0],y[i]);
		if(maxx[0]-minx[0]<=k&&maxy[0]-miny[0]<=k)printf("%d",power[n]);
		else if(maxx[0]-minx[0]<=k){
			loop(i,1,n)if(y[i]-miny[0]<=k&&maxy[0]-y[i]<=k)++tot;
			printf("%d",power[tot+1]);
		}
		else if(maxy[0]-miny[0]<=k){
			loop(i,1,n)if(x[i]-minx[0]<=k&&maxx[0]-x[i]<=k)++tot;
			printf("%d",power[tot+1]);
		}
		else{
			int nowans=1;
			loop(i,1,n)
				if(x[i]-minx[0]<=k&&y[i]-miny[0]<=k&&maxx[0]-x[i]<=k&&maxy[0]-y[i]<=k)nowans=nowans*2%mod;
				else if((x[i]-minx[0]>k||y[i]-miny[0]>k)&&(maxx[0]-x[i]>k||maxy[0]-y[i]>k))nowans=0;
			ans=(ans+nowans*2%mod)%mod,nowans=1;
			loop(i,1,n)
				if(x[i]-minx[0]<=k&&y[i]-miny[0]<=k&&maxx[0]-x[i]<=k&&maxy[0]-y[i]<=k)nowans=nowans*2%mod;
				else if((x[i]-minx[0]>k||maxy[0]-y[i]>k)&&(maxx[0]-x[i]>k||y[i]-miny[0]>k))nowans=0;
			printf("%d",(ans+nowans*2%mod)%mod);
		}
	}
	return 0;
}