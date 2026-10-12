#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <set>
#include <map>
#include <stack>
#include <queue>
#include <deque>

using namespace std;

const int SIZE = 3e2 + 5;

char str[SIZE];
int s;
int dp[SIZE][SIZE];

int main() {
    
    scanf("%s", str + 1);
    scanf("%d", &s);

    int n = (int) strlen(str + 1);

    for (int r = 1; r <= n; ++ r) {
        for (int l = r; l >= 0; -- l) {
            // printf("Processing substring: %s\n", string(str + l, str + r + 1).c_str()); // Debugging line to check the current substring
            dp[l][r] = r - l + 1;

            for (int k = l; k < r; ++ k) 
                dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r]);

            if (str[l] == 'm') {
                for (int k = l + 1; k <= r; ++ k) {
                    if (str[k] == 'x' && dp[l + 1][k - 1] == 0) {
                        dp[l][r] = min(dp[l][r], max(0, dp[k + 1][r] - s));
                    }
                }
            }
        }
    }

    printf("%d\n", dp[1][n]);
    return 0;
}