#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = (1LL << 60);
inline ll count_arith(ll s,ll p,ll L,ll R){
    if(s>R) return 0;
    ll k_min=0;
    if(L>s) k_min=(L-s+p-1)/p;
    ll k_max=(R-s)/p;
    return k_max>=k_min?k_max-k_min+1:0;
}
struct Edge{int to;int w;};
struct State{
    ll d;
    int v,parity,has1;
    bool operator<(const State&other)const{return d>other.d;}
};
template<typename T> void out(T*a,int l,int r){for(int i=l;i<=r;++i)cout<<*(a+i)<<' ';puts("");}
void out(vector<ll> wyx,int l,int r){for(int i=l;i<=r;++i)cout<<wyx[i]<<' ';puts("");}
int main(){
    int n,m;
    if(!(cin>>n>>m)) return 0;
    vector<vector<Edge>> G(n+1);
    for(int i=0;i<m;++i){
        int x,y,o;
        cin>>x>>y>>o;
        int w=(o==0?1:2);
        G[x].push_back({y,w});
        G[y].push_back({x,w});
    }
    static ll dist[100005][2][2];
    for(int v=1;v<=n;++v)
        dist[v][0][0]=dist[v][0][1]=dist[v][1][0]=dist[v][1][1]=INF;
    priority_queue<State> pq;
    dist[1][0][0]=0;
    pq.push({0,1,0,0});
    while(!pq.empty()){
        auto cur=pq.top();pq.pop();
        if(cur.d!=dist[cur.v][cur.parity][cur.has1]) continue;
        for(auto e:G[cur.v]){
            int np=cur.parity^(e.w&1);
            int nh=cur.has1|(e.w==1);
            ll nd=cur.d+e.w;
            if(nd<dist[e.to][np][nh]){
                dist[e.to][np][nh]=nd;
                pq.push({nd,e.to,np,nh});
            }
        }
    }
    vector<ll> dOdd(n+1,INF),dEven1(n+1,INF),dEven0(n+1,INF);
    for(int v=1;v<=n;++v){
        dOdd[v]=min(dist[v][1][0],dist[v][1][1]);
        dEven1[v]=dist[v][0][1];
        dEven0[v]=dist[v][0][0];
    }
    int q;cin>>q;
    while(q--){
        int x;ll L,R;cin>>x>>L>>R;
        ll ans=0;
        if(dOdd[x]<INF) ans+=count_arith(dOdd[x],2,L,R);
        if(dEven1[x]<INF) ans+=count_arith(dEven1[x],2,L,R);
        if(dEven0[x]<INF) ans+=count_arith(dEven0[x],4,L,R);
        if(dEven0[x]<INF&&dEven1[x]<INF){
            ll rmod=dEven0[x]&3;
            ll first=max(dEven0[x],dEven1[x]);
            if((first&3)!=rmod) first+=2;
            ans-=count_arith(first,4,L,R);
        }
        cout<<ans<<'\n';
    }
    return 0;
}
