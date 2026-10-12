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
const int N = 81;

int A,B,C,D,n,m;
bool f[2][N][N][N][N];
signed main(){
    // freopen("game2.in","r",stdin);
    // freopen("game10.out","w",stdout);
    ios::sync_with_stdio(false); cin.tie(0u); cout.tie(0u);
    cin >> A >> B >> C >> D;
    cin >> n;
    f[0][0][0][0][0] = 1;
    int tot = 0;
    for (int i = 1; i <= n; i++){
        char o,o2;
        int x;
        cin >> o >> x >> o2;
        tot += x;
        for (int d = 0; d <= A; d++){
            for (int c = 0; c <= B; c++){
                for (int h = 0; h <= C; h++){
                    int s = tot-d-c-h;
                    f[i%2][d][c][h][s] = 0;
                }
            }
        }
        for (int d = 0; d <= A; d++){
            for (int c = 0; c <= B; c++){
                for (int h = 0; h <= C; h++){
                    int s = tot-d-c-h;
                    if (s < 0 || s > D) continue;
                    if ((o == 'D'&& o2 == 'T') || (o != 'D'&& o2 == 'F')) if (d >= x) f[i%2][d][c][h][s] |= f[(i&1)^1][d-x][c][h][s];
                    if ((o == 'C'&& o2 == 'T') || (o != 'C'&& o2 == 'F')) if (c >= x) f[i%2][d][c][h][s]  |= f[(i&1)^1][d][c-x][h][s];
                    if ((o == 'H'&& o2 == 'T') || (o != 'H'&& o2 == 'F')) if (h >= x) f[i%2][d][c][h][s] |=  f[(i&1)^1][d][c][h-x][s];
                    if ((o == 'S'&& o2 == 'T') || (o != 'S'&& o2 == 'F')) if (s >= x) f[i%2][d][c][h][s] |= f[(i&1)^1][d][c][h][s-x];
                }
            }
        }
    }
    // cout << f[0][40][60][20][80] << endl;
    cin >> m;
    for (int i = 1; i <= m; i++){
        char o;
        int x;
        cin >> o >> x;
        int if0 = 1, if1 = 1;
        int noo = 1;
        for (int d = 0; d <= A; d++){
            for (int c = 0; c <= B; c++){
                for (int h = 0; h <= C; h++){
                    int s = tot-d-c-h;
                    if (d > A-x && c > B-x && h > C-x && s > D-x) continue;
                    if (f[n%2][d][c][h][s]){
                        noo = 0;
                        if (o == 'D'){
                            if (d <= A-x) if0 = 0;
                            if (d <= A-x && c > B-x && h > C-x && s > D-x);
                            else if1 = 0;
                        }
                        if (o == 'C'){
                            if (c <= B-x) if0 = 0;
                            if (d > A-x && c <= B-x && h > C-x && s > D-x);
                            else if1 = 0;
                        }
                        if (o == 'H'){
                            if (h <= C-x) if0 = 0;
                            if (d > A-x && c > B-x && h <= C-x && s > D-x);
                            else if1 = 0;
                        }
                        if (o == 'S'){
                            if (s <= D-x) if0 = 0;
                            if (d > A-x && c > B-x && h > C-x && s <= D-x);
                            else if1 = 0;
                        }
                    }
                    
                }
            }
        } 
        if (noo == 1) cout << "ERROR" << endl;
        else if (if0) cout << "F" << endl;
        else if (if1) cout << 'T' << endl;
        else cout << "NG" << endl;
    }
    return 0;
}