#include <iostream>
#include <vector>
#include <algorithm>
#include <utility>
#include <cstring>
#include <cmath>
#include <set>
#include <map>
#include <unordered_map>
using namespace std;
#define int long long
using pii = pair<int, int>;
using ull = unsigned long long;
// #define debug(x) cout << #x << ":" << x << endl
constexpr int M = 5e5 + 2;

int col[M], a[M];
int pri[M];
int prime[M];
int n, cnt, ans;

struct node
{
    int len, c;
};

node max1[M], max2[M];

void ols(int n)
{
    int i, j;
    for (i = 2; i <= n; i++)
    {
        if (!pri[i])
        {
            pri[i] = i;
            prime[cnt++] = i;
        }
        for (j = 0; i * prime[j] <= n; j++)
        {
            pri[i * prime[j]] = prime[j];
            if (i % prime[j] == 0)
            {
                break;
            }
        }
    }
}

vector<int> f(int x)
{
    vector<int> t;
    while (x > 1)
    {
        int p = pri[x];
        t.push_back(p);
        while (x % p == 0)
            x /= p;
    }
    return t;
}

void solve()
{
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i] >> col[i];

    ols(5e5);
    for (int i = 1; i <= n; i++)
    {
        auto v = f(a[i]);
        int curmax = 0;
		cerr<<i<<":"<<curmax<<endl; 
        for (auto &ele : v)
        {
        	cerr<<ele<<"ssss"<<endl;
            if (max1[ele].c == col[i])
                curmax = max(curmax, max2[ele].len);
            else
                curmax = max(curmax, max1[ele].len);
        }
        curmax++;
        
        ans = max(ans, curmax);
        for (auto &ele : v)
        {
            if (max1[ele].c == col[i])
                max1[ele].len = max(max1[ele].len, curmax);
            else
            {
                if (curmax > max1[ele].len)
                {
                    max2[ele] = max1[ele];
                    max1[ele] = {curmax, col[i]};
                }
                else if (curmax > max2[ele].len)
                {
                    max2[ele] = {curmax, col[i]};
                }
            }
        }
    }
    cout << ans << endl;
}

signed main()
{
    ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
    solve();
    return 0;
}
