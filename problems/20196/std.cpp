#include<bits/stdc++.h>

using namespace std;

#define endl '\n'
// #define int long long
#define fi first
#define se second
typedef long long ll;
typedef unsigned long long ull;
typedef long double db;
typedef pair<int, int> pii;

const int N = 2e6+5;
const int inf = 1e9;
const int p = 1e9+7;

ll n,m;
int nxt[N], pre[N], hd[N], tot;

struct node{
    ll len, s, cs;
    bool is;
}a[N];
signed main(){
    freopen("dog.in","r",stdin);
    freopen("dog.out","w",stdout);
    ios::sync_with_stdio(false);cin.tie(0); cout.tie(0);
    cin >> n >> m;

    ll cnt = 0, k, val;
    for (int i = 1; i <= n; i++){
        cin >> k;
        hd[++tot] = ++cnt; a[cnt].is = 1;
        nxt[cnt] = cnt+1;

        for (int j = 1; j <= k; j++){
            cin >> val;
            a[++cnt] = {1, val, val,0};
            pre[cnt] = cnt-1;
            if (j < k) nxt[cnt] = cnt+1;
        }
    }
    auto get = [&](node x, node y){
        node t = {1,0,0,0};
        t.s = x.s+y.s;
        t.cs = x.cs+x.s*y.len+y.cs;
        t.len = x.len+y.len;
        return t;
    };
    auto merge = [&](int x, int y){
        a[x] = get(a[x],a[y]);
        nxt[x] = nxt[y]; pre[nxt[y]] = x;
        a[y].is = 1;
    };

    for (int i = 1; i <= tot; i++){
        for (int j = nxt[hd[i]]; j; j = nxt[j]){
            if (nxt[j] && a[j].s >= a[j].len*a[nxt[j]].s){
                merge(j, nxt[j]);
            }
            int jj = j;
            while (pre[jj] && !a[pre[jj]].is){
                if (a[pre[jj]].s*a[jj].len >= a[jj].s*a[pre[jj]].len) merge(pre[jj], jj);
                else break;
                jj = pre[jj];
                
            }
        }
    }

    sort(a+1,a+cnt+1,[&](node a, node b){
        if (a.is != b.is) return a.is < b.is;
        return a.s*b.len < b.s*a.len;
    });

    node t = {0,0,0,0};
    for (int i = 1; !a[i].is; i++){
        t = get(t,a[i]);
    }
    cout << (cnt-n)*m-t.cs << endl;
    return 0;
}