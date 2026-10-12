#include <bits/stdc++.h>
#define endl '\n'
#define int long long
#define fi first
#define se second
using namespace std;
const int N=1e6+10;
const int inf=0x3f3f3f3f3f3f3f3f;
const int mod=1e9+7;
int n,m,k,T;
int ans[N];
int in[N];
vector<pair<int,int>> G[N];
void tops()
{
    queue<int> q;
    for(int i=1;i<=n;i++)
    {
        ans[i]=1;
        if(!in[i]) q.push(i);
    }
    while(!q.empty())
    {
        int u=q.front();
        q.pop();
        for(auto x:G[u])
        {
            int v=x.fi,c=x.se;
            ans[v]+=ans[u]*c%mod;//取模 
            ans[v]%=mod;
            if(!(--in[v])) q.push(v);//前驱处理完了,入队 
        }
    }
}
signed main()
{
	//freopen(".in","r",stdin);
    //freopen(".out","w",stdout);
	cin.tie(0);
	cout.tie(0);
	ios::sync_with_stdio(false);
	cin>>n>>m>>T;
	for(int i=1;i<=m;i++)
	{
	    int u,v,c;
	    cin>>u>>v>>c;
	    G[u].push_back({v,c});
	    in[v]++;
    }
    tops();//预处理 
    while(T--)
    {
        int s;
        cin>>s;
        cout<<ans[s]<<endl;//输出答案 
    }
    return 0;
}
