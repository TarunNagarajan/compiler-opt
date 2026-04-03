
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 53 + y; };
        std::function<int(int, int)> g = f;
        return g(31, 49);
    }
    