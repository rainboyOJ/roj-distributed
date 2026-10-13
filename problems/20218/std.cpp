#include <bits/stdc++.h>
using namespace std;

struct edge {
    int u, v;
    int l, r;
    int id;

    edge() {
        u = v = 0;
        l = r = 0;
        id = 0;
    }
};

const int max_n = 500111, inf = 1000111222;
const int max_lev = 19;

int n, m;
edge edges[max_n];

void read_input() {
    cin >> n >> m;
    for (int i = 0; i < m; ++i) {
        cin >> edges[i].u >> edges[i].v >> edges[i].l >> edges[i].r;
        --edges[i].u;
        --edges[i].v;
        --edges[i].l;
        --edges[i].r;
        edges[i].id = i;
    }
}

int answer[max_n];
priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> r_id;

void solve___no_spanning_tree_restriction() {
    sort(edges, edges + m, [](const edge &lhs, const edge &rhs) { return lhs.l < rhs.l; });

    while (!r_id.empty()) {
        r_id.pop();
    }
    int edges_p = 0;
    for (int i = 0; i < m; ++i) {
        while (edges_p < m && i == edges[edges_p].l) {
            r_id.push(make_pair(edges[edges_p].r, edges[edges_p].id));
            ++edges_p;
        }

        if (r_id.empty() || r_id.top().first < i) {
            cout << "NO"
                 << "\n";
            return;
        }
        answer[r_id.top().second] = i;
        r_id.pop();
    }

    cout << "YES"
         << "\n";
    for (int i = 0; i < m; ++i) {
        cout << answer[i] + 1 << " \n"[i == (m - 1)];
    }
}

inline void upd_min(int &a, int b) { a = min(a, b); }

inline void upd_max(int &a, int b) { a = max(a, b); }

vector<int> tree[max_n];
int depth[max_n];

struct binary_lifting_elem {
    int to;
    int value;

    binary_lifting_elem() {
        to = 0;
        value = 0;
    }
};

int logn;
binary_lifting_elem binary_lifting[max_lev][max_n];

void dfs(int v, int p) {
    binary_lifting[0][v].to = p;
    for (int j = 1; j < logn; ++j) {
        int m = binary_lifting[j - 1][v].to;

        binary_lifting[j][v].to = binary_lifting[j - 1][m].to;
    }

    for (int i = 0; i < tree[v].size(); ++i) {
        int to = tree[v][i];
        if (to != p) {
            depth[to] = depth[v] + 1;
            dfs(to, v);
        }
    }
}

void process_on_path(int u, int v, const function<void(binary_lifting_elem &elem)> &f) {
    if (depth[u] > depth[v]) {
        swap(u, v);
    }
    for (int j = logn - 1; j >= 0; --j) {
        int to = binary_lifting[j][v].to;
        if (depth[u] <= depth[to]) {
            f(binary_lifting[j][v]);
            v = to;
        }
    }
    if (u == v) {
        return;
    }
    for (int j = logn - 1; j >= 0; --j) {
        int to_u = binary_lifting[j][u].to;
        int to_v = binary_lifting[j][v].to;
        if (to_u != to_v) {
            f(binary_lifting[j][u]);
            f(binary_lifting[j][v]);
            u = to_u;
            v = to_v;
        }
    }
    f(binary_lifting[0][u]);
    f(binary_lifting[0][v]);
}

void solve() {
    for (int i = 0; i < n; ++i) {
        tree[i].clear();
    }
    logn = 1;
    while ((1 << logn) < n) {
        ++logn;
    }
    for (int j = 0; j < logn; ++j) {
        for (int i = 0; i < n; ++i) {
            binary_lifting[j][i].value = 0;
        }
    }
    for (int i = 0; i < (n - 1); ++i) {
        tree[edges[i].u].push_back(edges[i].v);
        tree[edges[i].v].push_back(edges[i].u);
    }

    dfs(0, 0);

    for (int i = 0; i < (n - 1); ++i) {
        int u = edges[i].u;
        int v = edges[i].v;
        if (depth[u] > depth[v]) {
            swap(u, v);
        }
        binary_lifting[0][v].value = edges[i].l;
    }
    for (int j = 1; j < logn; ++j) {
        for (int i = 0; i < n; ++i) {
            int m = binary_lifting[j - 1][i].to;

            binary_lifting[j][i].value = max(binary_lifting[j - 1][i].value, binary_lifting[j - 1][m].value);
        }
    }
    for (int i = (n - 1); i < m; ++i) {
        int max_l_on_path = -1;
        process_on_path(edges[i].u, edges[i].v,
                        [&](binary_lifting_elem &elem) { upd_max(max_l_on_path, elem.value); });
        upd_max(edges[i].l, max_l_on_path + 1);
    }

    for (int j = 0; j < logn; ++j) {
        for (int i = 0; i < n; ++i) {
            binary_lifting[j][i].value = m;
        }
    }
    for (int i = (n - 1); i < m; ++i) {
        int r_to_update = edges[i].r;
        process_on_path(edges[i].u, edges[i].v,
                        [&](binary_lifting_elem &elem) { upd_min(elem.value, r_to_update); });
    }
    for (int j = logn - 1; j >= 1; --j) {
        for (int i = 0; i < n; ++i) {
            int m = binary_lifting[j - 1][i].to;

            upd_min(binary_lifting[j - 1][i].value, binary_lifting[j][i].value);
            upd_min(binary_lifting[j - 1][m].value, binary_lifting[j][i].value);
        }
    }
    for (int i = 0; i < (n - 1); ++i) {
        int u = edges[i].u;
        int v = edges[i].v;
        if (depth[u] > depth[v]) {
            swap(u, v);
        }
        upd_min(edges[i].r, binary_lifting[0][v].value - 1);
    }

    solve___no_spanning_tree_restriction();
}

int main() {
    freopen("shi.in", "r", stdin);
    freopen("shi.out", "w", stdout);
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int tests;
    cin >> tests;
    for (int test = 0; test < tests; ++test) {
        read_input();
        solve();
    }
}