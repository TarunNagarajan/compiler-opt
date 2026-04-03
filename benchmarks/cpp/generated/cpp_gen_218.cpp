
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {
        std::vector<int> v = {18, 38, 55, 93};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }
    