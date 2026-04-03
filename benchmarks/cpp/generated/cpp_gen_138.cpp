
    #include <utility>
    #include <vector>
    class Buffer {
    public:
        Buffer(int s) : size(s), data(new int[s]) {}
        ~Buffer() { delete[] data; }
        Buffer(Buffer&& other) noexcept {
            data = other.data;
            size = other.size;
            other.data = nullptr;
        }
    private:
        int* data;
        int size;
    };
    int main() {
        std::vector<Buffer> vec;
        vec.push_back(Buffer(78));
        return vec.size() + 96;
    }
    