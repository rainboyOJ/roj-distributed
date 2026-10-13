#include <bits/stdc++.h>
#define maxn 500000 * 31
using namespace std;
typedef long long LL;

int Cnt[31][2];

struct Trie {
	int relation[maxn][2], info[maxn];
	LL illegal[maxn];

	int root, cnt;
	int newnode() {
		relation[cnt][0] = relation[cnt][1] = -1;
		info[cnt] = illegal[cnt] = 0;
		return cnt++;
	}
	void init() {
		cnt = 0;
		root = newnode();
	}
	void insert(int x) {
		int cur = root;
		++info[cur];
		for (int i = 29; i >= 0; --i) {
			if (relation[cur][(x >> i) & 1] == -1)
				relation[cur][(x >> i) & 1] = newnode();
			cur = relation[cur][(x >> i) & 1];
			illegal[cur] += (Cnt[i][(x >> i) & 1]);
			++Cnt[i][(x >> i) & 1];
			++info[cur];
		}
	}
	LL query(int x) {
		LL ret = 0;
		int cur = root;
		for (int i = 29; i >= 0; --i) {
			int numb = ((x >> i) & 1), another = 1 - numb;
			int idx = relation[cur][another];
			LL c = info[idx];
			LL temp = c * (Cnt[i][another]) - c - illegal[idx];
			ret += temp;
			cur = relation[cur][numb];
			if (cur == -1)
				break;
		}
		return ret;
	}
};

Trie trie;

int main() {
	freopen("xor.in", "r", stdin);
	freopen("xor.out", "w", stdout);
	int T;
	LL ans = 0;
	int n;
	scanf("%d", &n);
	trie.init();
	memset(Cnt, 0, sizeof(Cnt));
	for (int i = 0; i < n; ++i) {
		int temp;
		scanf("%d", &temp);
		ans += trie.query(temp);
		trie.insert(temp);
	}
	printf("%lld\n", ans);
	return 0;
}