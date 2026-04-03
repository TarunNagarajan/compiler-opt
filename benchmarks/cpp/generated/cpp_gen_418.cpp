
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 28 + y; };
        std::function<int(int, int)> g = f;
        return g(57, 42);
    }
    