
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {
        std::vector<int> v = {68, 40, 34, 83};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }
    