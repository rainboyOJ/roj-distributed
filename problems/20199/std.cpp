#include <vector>
#include <iostream>
using namespace std;

int main() {
//	freopen("pack.in", "r", stdin);
//	freopen("pack.out", "w", stdout);
	cin.tie(0);
	ios_base::sync_with_stdio(false);
	int N, L;
	cin >> N >> L;
	vector<int> A(N);
	for (int i = 0; i < N; i++) {
		cin >> A[i];
	}
	
	vector<int> answer(N);
	int r = N, sum = 0;
	for (int i = N - 1; i >= 0; i--) {
		sum += A[i];
		while (sum > L) {
			r -= 1;
			sum -= A[r];
		}
		if (r == N) {
			answer[i] = 1;
		}
		else {
			answer[i] = answer[r] + 1;
		}
	}
	
	for (int i = 0; i < N; i++) {
		cout << answer[i] << ' ';
	}
	
	return 0;
}