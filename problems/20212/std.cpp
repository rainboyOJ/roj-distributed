#include<bits/stdc++.h>
using namespace std;
const int N = 2e6+5;
int n;

vector<int> v[N];
bool f[N][4];
void dfs(int x){
    int sz = v[x].size();
    if (!sz){
        f[x][1] = f[x][2] = f[x][3] = 1;
        return;
    } 
    for (int y:v[x]){
        dfs(y);
    } 

    int pl0 = -1, pr0 = sz; 
    int pl3 = -1, pr3 = sz;
    
    while(pl0 < sz-1 && f[v[x][pl0+1]][0]) pl0++;
    while(pl3 < sz-1 && f[v[x][pl3+1]][3]) pl3++;
    while(pr0 > 0 && f[v[x][pr0-1]][0]) pr0--;
    while(pr3 > 0 && f[v[x][pr3-1]][3]) pr3--;

    int lst1 = -1, lst2 = -1; 
    for (int i = 0; i < sz; i++){
        int y = v[x][i];
        if (f[y][2] && lst1 != -1 && lst1-1 <= pl3 && i+1 >= pr3) f[x][3] = 1; 
        if (!f[y][0]) lst1 = -1; 
        if (f[y][1] && lst1 == -1) lst1 = i;  

        if (f[y][1] && lst2 != -1 && lst2-1 <= pl0 && i+1 >= pr0) f[x][0] = 1;
        if (!f[y][3]) lst2 = -1;
        if (f[y][2] && lst2 == -1) lst2 = i; 
    }

    
    for (int i = 0; i < sz; i++){ 
        int y = v[x][i];
        if (f[y][1] && i+1 >= pr0 && i-1 <= pl3) f[x][1] = 1;
        if (f[y][2] && i+1 >= pr3 && i-1 <= pl0) f[x][2] = 1;
    }
}

int T;
signed main(){
    freopen("tree.in","r",stdin);
    freopen("tree.out","w",stdout);
    ios::sync_with_stdio(false); cin.tie(0u); cout.tie(0u);
    cin >> T;
    while(T--){
        cin >> n;
        for (int i = 1; i <= n; i++){
            f[i][0] = f[i][1] = f[i][2] = f[i][3] = 0;
            v[i].clear();
        } 
        for (int i = 1; i <= n; i++){
            int k;
            cin >> k;
            for (int j = 1; j <= k; j++){
                int x;
                cin >> x;
                v[i].push_back(x);
            }
        }
        dfs(1);
        if (f[1][0]) cout << "YES" << '\n';
        else cout << "NO" << '\n';
    }
    return 0;
}