
    #include <functional>
    int main() {
        auto f = [](int x, int y) { return x * 41 + y; };
        std::function<int(int, int)> g = f;
        return g(45, 37);
    }
    