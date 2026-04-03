
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 44 + y; };
        std::function<int(int, int)> g = f;
        return g(8, 90);
    }
    