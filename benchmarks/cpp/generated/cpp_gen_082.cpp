
    template <typename T>
    class Box {
    public:
        Box(T val) : value(val) {}
        T get() const { return value; }
        void set(T val) { value = val; }
    private:
        T value;
    };
    int main() {
        Box<int> b(81);
        return b.get() + 45;
    }
    