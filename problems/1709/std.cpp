// 一本通 1709《寻找好串》标程（C++17）
// 来源：https://www.cnblogs.com/betablewaloot/p/12158578.html （博客园「寻找好串」AC 代码，已改编重写）
// 思路：P = 所有 S 中串的前缀（trie 结点串，|P| = cnt）。好串集合 U = P·P。
//   无重复时 |U| = |P|²；两对 (p1,p2)≠(p1',p2') 生成同一串 w 时，较长的首段是较短首段的延伸、
//   较短的尾段是较长尾段加前缀。利用 AC 自动机 fail 树统计每个结点串作为「其他结点串后缀」的重数，
//   按题解的树上计数扣除重复对数即得答案。
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;

typedef long long ll;
const int N = 300005;

int n, cnt = 0;
int er[N][26], fail[N], fa[N];
int ru[N];        // fail 树入度
ll ren[N], sumv[N];

char c[35];

void insert() {
    int len = (int)strlen(c + 1), now = 0;
    for (int i = 1; i <= len; i++) {
        int idx = c[i] - 'a';
        if (!er[now][idx]) {
            er[now][idx] = ++cnt;
            fa[er[now][idx]] = now;
        }
        now = er[now][idx];
    }
}

void get_fail() {
    static queue<int> que;
    for (int i = 0; i < 26; i++)
        if (er[0][i]) que.push(er[0][i]);
    while (!que.empty()) {
        int now = que.front(); que.pop();
        ru[fail[now]]++;
        for (int i = 0; i < 26; i++) {
            if (er[now][i]) {
                fail[er[now][i]] = er[fail[now]][i];
                que.push(er[now][i]);
            } else {
                er[now][i] = er[fail[now]][i];
            }
        }
    }
}

void get_sum() {
    static queue<int> que;
    for (int i = 0; i <= cnt; i++) ren[i] = 1;
    for (int i = 0; i <= cnt; i++)
        if (ru[i] == 0) que.push(i);
    while (!que.empty()) {
        int now = que.front(); que.pop();
        ren[fail[now]] += ren[now];
        sumv[now] = ren[now] - 1;
        if (--ru[fail[now]] == 0) que.push(fail[now]);
    }
}

int main() {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        scanf("%s", c + 1);
        insert();
    }
    get_fail();
    get_sum();
    ll ans = (ll)cnt * cnt;
    for (int i = 1; i <= cnt; i++) {
        if (fail[i]) {
            int hu1 = i, hu2 = fail[i];
            while (hu2) {          // 走到「最长后缀非公共部分」对应的结点
                hu1 = fa[hu1];
                hu2 = fa[hu2];
            }
            ans -= sumv[hu1];
        }
    }
    printf("%lld\n", ans);
    return 0;
}
