
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {
        std::vector<int> v = {74, 55, 34, 51};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }
    