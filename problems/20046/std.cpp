#include<bits/stdc++.h>
using namespace std;

typedef unsigned long long ull;
typedef long long ll;
typedef long double db;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
#define fi first
#define se second
#define endl '\n'


const int N = 2e5+5;

int n,m;
map<int,int> m1,m2;
map<pii,int> m3;
signed main(){
    ios::sync_with_stdio(false); cin.tie(0u); cout.tie(0u);
    cin >> n >> m;
    for (int i = 1; i <= n; i++){
        int x,y;
        cin >> x >> y;
        if (m1.count(x+y)) m1[x+y]++;
        else m1[x+y] = 1;
        if (m2.count(x-y)) m2[x-y]++;
        else m2[x-y] = 1;
        m3[{x,y}] = 1;
    }
    for (int i = 1; i <= m; i++){
        int x, y;
        cin >> x >> y;
        int ans = m1[x+y]+m2[x-y];
        if (m3.count({x,y})) ans--;
        cout << ans << endl;
    }
    return 0;
}