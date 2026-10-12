#include <bits/stdc++.h>
using namespace std;

int h, w;
string s[505];
bool a, b;
long long ans = 1;

int main() 
{
    // freopen("T2.in", "r", stdin);
    // freopen("T2.out", "w", stdout);
    cin >> h >> w;
    for (int i = 0; i < h; ++i) 
    {
        cin >> s[i];
    }

    for (int i = 0; i < h + w - 1; ++ i) 
    {
        a = 0, b = 0;
        for (int j = 0; j < min(i + 1, h); ++ j) 
        {
            if (i - j <= w) 
            {
                if (s[j][i - j] == 'B') 
                {
                    a = 1;
                }
                else if (s[j][i - j] == 'R') 
                {
                    b = 1;
                }
            }
        }

        if (a == 1 && b == 1) 
        {
            ans = 0;
        }
        else if (a == 0 && b == 0) 
        {
            ans = (ans * 2) % 998244353;
        }
    }

    cout << ans << endl;
    return 0;
}