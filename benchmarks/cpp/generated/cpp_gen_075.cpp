
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {
        std::vector<int> v = {63, 38, 48, 88};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }
    