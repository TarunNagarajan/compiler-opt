
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {
        std::vector<int> v = {14, 70, 74, 46};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }
    