#include <bits/stdc++.h>
using namespace std;

static inline int gcd_int(int a, int b) {
    if (a == 0) return b;
    if (b == 0) return a;
    while (b) { int t = a % b; a = b; b = t; }
    return a;
}

static string classify(const string &s) {
    int cnt[26] = {0};
    for (char ch : s) cnt[ch - 'a']++;
    int odd = 0, g = 0;
    for (int i = 0; i < 26; ++i) {
        if (cnt[i] & 1) ++odd;
        if (cnt[i] > 0) g = gcd_int(g, cnt[i]);
    }
    bool pal = (odd <= 1);
    bool cyc = (g >= 2);

    if (pal && cyc) return "XL";
    if (pal) return "X";
    if (cyc) return "L";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> inputs;
    string first;
    if (!(cin >> first)) return 0;

    auto is_number = [](const string &t) {
        if (t.empty()) return false;
        for (char c : t) if (!isdigit(static_cast<unsigned char>(c))) return false;
        return true;
    };

    if (is_number(first)) {
        int T = stoi(first);
        inputs.reserve(T);
        for (int i = 0; i < T; ++i) {
            string s; cin >> s;
            inputs.push_back(s);
        }
    } else {
        inputs.push_back(first);
        string s;
        while (cin >> s) inputs.push_back(s);
    }

    for (auto &s : inputs) {
        cout << classify(s) << '\n';
    }
    return 0;
}
