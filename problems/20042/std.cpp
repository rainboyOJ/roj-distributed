#include <bits/stdc++.h>
using namespace std;

static inline long long id3(int n, int i, int j, int k) {
    return 1LL*(i-1)*n*n + 1LL*(j-1)*n + (k-1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    long long K;
    int xidx;
    if (!(cin >> n >> m >> K >> xidx)) return 0;

    vector<array<int,3>> pts(m);
    for (int t = 0; t < m; ++t) cin >> pts[t][0] >> pts[t][1] >> pts[t][2];

    int si = pts[xidx-1][0], sj = pts[xidx-1][1], sk = pts[xidx-1][2];

    long long N3 = 1LL*n*n*n;
    vector<char> occ(N3, 0);
    vector<vector<int>> occX(n*n), occY(n*n), occZ(n*n);

    for (int t = 0; t < m; ++t) if (t != xidx-1) {
        int i = pts[t][0], j = pts[t][1], k = pts[t][2];
        occ[id3(n,i,j,k)] = 1;
        occX[(j-1)*n + (k-1)].push_back(i); // x直线：固定(j,k)
        occY[(i-1)*n + (k-1)].push_back(j); // y直线：固定(i,k)
        occZ[(i-1)*n + (j-1)].push_back(k); // z直线：固定(i,j)
    }
    for (int u = 0; u < n*n; ++u) {
        auto &vx = occX[u]; if (vx.size() > 1) sort(vx.begin(), vx.end());
        auto &vy = occY[u]; if (vy.size() > 1) sort(vy.begin(), vy.end());
        auto &vz = occZ[u]; if (vz.size() > 1) sort(vz.begin(), vz.end());
    }

    vector<int> dist(N3, -1);
    deque<long long> q;
    long long sId = id3(n, si, sj, sk);
    dist[sId] = 0;
    q.push_back(sId);

    long long ans = 1;

    vector<char> usedX(2*n*n, 0), usedY(2*n*n, 0), usedZ(2*n*n, 0);

    auto expand_X = [&](int ui,int uj,int uk,int uid){
        int lid = (uj-1)*n + (uk-1);                  
        int c = int(upper_bound(occX[lid].begin(), occX[lid].end(), ui) - occX[lid].begin()) & 1;
        char &used = usedX[lid*2 + c];
        if (used) return;
        used = 1;

        int p = 0, sz = (int)occX[lid].size();
        int parity = 0;
        for (int t = 1; t <= n; ++t) {
            while (p < sz && occX[lid][p] < t) { parity ^= 1; ++p; }
            if (parity == c) {
                long long vid = id3(n, t, uj, uk);
                if (vid != uid && !occ[vid] && dist[vid] == -1) {
                    dist[vid] = dist[uid] + 1;
                    if (dist[vid] <= K) { q.push_back(vid); ++ans; }
                }
            }
        }
    };
    auto expand_Y = [&](int ui,int uj,int uk,int uid){
        int lid = (ui-1)*n + (uk-1);
        int c = int(upper_bound(occY[lid].begin(), occY[lid].end(), uj) - occY[lid].begin()) & 1;
        char &used = usedY[lid*2 + c];
        if (used) return;
        used = 1;

        int p = 0, sz = (int)occY[lid].size();
        int parity = 0;
        for (int t = 1; t <= n; ++t) {
            while (p < sz && occY[lid][p] < t) { parity ^= 1; ++p; }
            if (parity == c) {
                long long vid = id3(n, ui, t, uk);
                if (vid != uid && !occ[vid] && dist[vid] == -1) {
                    dist[vid] = dist[uid] + 1;
                    if (dist[vid] <= K) { q.push_back(vid); ++ans; }
                }
            }
        }
    };
    auto expand_Z = [&](int ui,int uj,int uk,int uid){
        int lid = (ui-1)*n + (uj-1);
        int c = int(upper_bound(occZ[lid].begin(), occZ[lid].end(), uk) - occZ[lid].begin()) & 1;
        char &used = usedZ[lid*2 + c];
        if (used) return;
        used = 1;

        int p = 0, sz = (int)occZ[lid].size();
        int parity = 0;
        for (int t = 1; t <= n; ++t) {
            while (p < sz && occZ[lid][p] < t) { parity ^= 1; ++p; }
            if (parity == c) {
                long long vid = id3(n, ui, uj, t);
                if (vid != uid && !occ[vid] && dist[vid] == -1) {
                    dist[vid] = dist[uid] + 1;
                    if (dist[vid] <= K) { q.push_back(vid); ++ans; }
                }
            }
        }
    };

    while (!q.empty()) {
        long long u = q.front(); q.pop_front();
        if (dist[u] == K) continue;

        int i = int(u / (1LL*n*n)) + 1;
        long long rem = u % (1LL*n*n);
        int j = int(rem / n) + 1;
        int k = int(rem % n) + 1;

        expand_X(i,j,k,(int)u);
        expand_Y(i,j,k,(int)u);
        expand_Z(i,j,k,(int)u);
    }

    cout << ans << '\n';
    return 0;
}