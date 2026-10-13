#include<bits/stdc++.h>
using namespace std;

// #define int long long
typedef long long ll;
typedef long double db;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
#define fi first
#define se second

const int N = 1e5+5;
const int M = (1<<8)+5;;
const ll inf = 5e18+5;
const int p = 998244353;

int h,n;
pii a[N];

signed main(){
    freopen("water.in","r",stdin);
    freopen("water.out","w",stdout);
    // ios::sync_with_stdio(false); cin.tie(0u); cout.tie(0u);
    cin >> h >> n;

    bool ok = 0;
    for (int i = 1; i <= n; i++){
        cin >> a[i].fi >> a[i].se;
        if (!a[i].se) ok = 1;
    }
    if (!ok){
        cout << "-1\n";
        return 0;
    }

    sort(a+1,a+n+1);
    
    db ans = 0;
    db now = h;
    
    priority_queue<int> q; 
    for (int i = 1; i <= n; i++){
        if (a[i].se >= now) continue;
        bool tt = 1;
        while (ans < a[i].fi){ // 当前时间
            if (q.size()){ 
                if (ans+(db)(now-q.top())/q.size() < a[i].fi){ // 到插入的下一个位置 之前到不了当前时间
                    ans += (db)(now-q.top())/q.size();
                    now = q.top();
                    q.pop();
                }else{ // 到插入的下一个位置 超越当前时间
                    // cout << i << endl;
                    db t = (db)(a[i].fi-ans)*q.size(); // 到当前时间，能走多远
                    now -= t;
                    ans = a[i].fi;
                }
            }else{
                ans = a[i].fi;
            }
            if (!now){
                printf("%.6Lf", ans);
                return 0;
            }
        }
        // cout << i << " " << ans << " " << now << '\n';
        if (now > a[i].se) q.push(a[i].se);
        // while(q.size() && q.top() > now) q.pop(); 
    }

    while(q.size()){
        ans += (now-q.top())/q.size();
        now = q.top();
        q.pop();
    }
    printf("%.6Lf", ans);

    
	return 0;
}