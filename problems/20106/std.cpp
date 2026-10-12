#include <iostream>
#include <string>
#include <queue>
#include <cstring>

using namespace std;
typedef long long ll;

struct Item {
	int ch, freq;
	bool operator<(const Item &o) const {
		return freq > o.freq;
	}
};

int main() {
	int cases;
	cin >> cases;
	while(cases--) {
		string str;
		cin >> str;
		int freq[26] = {};
		int len = str.size();
		priority_queue<Item> pq;
		for(int i=0;i<len;++i){
			if(str[i]!='*') ++freq[str[i]-'A'];
		}
		for(int i=0;i<26;++i){
			pq.push({i,freq[i]});
		}
		for(int i=0;i<len;++i){
			if(str[i]=='*'){
				auto x=pq.top(); pq.pop();
				++freq[x.ch];
				pq.push({x.ch,freq[x.ch]});
			}
		}
		ll res=0;
		for(int i=0;i<26;i++) cerr<<freq[i]<<","; cout<<endl; 
		for(int i=0;i<26;++i)
			res+=1LL*(len-freq[i])*freq[i];
		cout<<res/2<<'\n';
	}
}
