#include <iostream>
#include <vector>
#include <array>

using namespace std;

int main() {
	int n, q;
	cin >> n >> q;
	vector<int> arr(n + 1);
	vector<array<int, 21>> bit(n + 1);
	for(int i = 1; i <= n; ++i){
		cin >> arr[i];
		bit[i] = bit[i - 1];
		for(int j = 0; j < 21; ++j){
			if(arr[i] >> j & 1) ++bit[i][j];
		}
	}
	while(q--){
		int op, l, r;
		cin >> op >> l >> r;
		int res = 0;
		for(int j = 0; j <= 20; ++j){
			int cnt = bit[r][j] - bit[l - 1][j];
			if(op == 1){
				if(cnt & 1) res |= (1 << j);
			}else if(op == 2){
				if(cnt > 0) res |= (1 << j);
			}else{
				if(cnt == r - l + 1) res |= (1 << j);
			}
		}
		cout << res << '\n';
	}
}
