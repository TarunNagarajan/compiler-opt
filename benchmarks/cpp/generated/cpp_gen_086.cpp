
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 62 + y; };
        std::function<int(int, int)> g = f;
        return g(18, 8);
    }
    