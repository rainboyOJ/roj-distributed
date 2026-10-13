#include<bits/stdc++.h>

using namespace std;

const int MX=50005;

int n;
unsigned int K,a[MX];

int main(){
    freopen("nim.in","r",stdin);
    freopen("nim.out","w",stdout);
	ios::sync_with_stdio(false);
	cin>>n>>K;
	for(int i=1;i<=n;i++)cin>>a[i];
	unsigned int xors=0;
	for(int i=1;i<=n;i++)xors^=a[i];
	if(!xors||(xors&-xors)>K)cout<<0<<endl;
	else{
		cout<<1<<endl;
		for(int i=1;i<=n;i++){
			vector<int> tmp;
			if(a[i]>(xors^a[i])&&a[i]-(xors^a[i])<=K)tmp.push_back(a[i]-(xors^a[i]));
			for(unsigned int t=2;t;t<<=1){
				unsigned int r=(a[i]-(xors^a[i])%t+t)%t;
				if(r&&r<=K&&r<=a[i]&&(((a[i]-r)^xors^a[i])&t))tmp.push_back(r);
			}
			sort(tmp.begin(),tmp.end());
			for(auto j:tmp)cout<<i<<' '<<j<<endl;
		}
	}
	return 0;
}