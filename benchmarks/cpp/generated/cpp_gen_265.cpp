
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 77 + y; };
        std::function<int(int, int)> g = f;
        return g(71, 62);
    }
    