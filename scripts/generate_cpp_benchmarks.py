import os
import random
from pathlib import Path

OUTPUT_DIR = Path("benchmarks/cpp/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES = [
    # 1. Basic Template Class
    """
    template <typename T>
    class Box {{
    public:
        Box(T val) : value(val) {{}}
        T get() const {{ return value; }}
        void set(T val) {{ value = val; }}
    private:
        T value;
    }};
    int main() {{
        Box<int> b({val1});
        return b.get() + {val2};
    }}
    """,
    # 2. Inheritance and Virtual Methods
    """
    class Shape {{
    public:
        virtual int area() = 0;
        virtual ~Shape() {{}}
    }};
    class Square : public Shape {{
    public:
        Square(int s) : side(s) {{}}
        int area() override {{ return side * side; }}
    private:
        int side;
    }};
    int main() {{
        Shape* s = new Square({val1});
        int res = s->area();
        delete s;
        return res + {val2};
    }}
    """,
    # 3. STL Vector and Algorithms
    """
    #include <vector>
    #include <numeric>
    #include <algorithm>
    int main() {{
        std::vector<int> v = {{{val1}, {val2}, {val3}, {val4}}};
        std::sort(v.begin(), v.end());
        return std::accumulate(v.begin(), v.end(), 0);
    }}
    """,
    # 4. Lambda and Functional
    """
    #include <functional>
    int main() {{
        auto f = [](int x, int y) {{ return x * {val1} + y; }};
        std::function<int(int, int)> g = f;
        return g({val2}, {val3});
    }}
    """,
    # 5. Move Semantics
    """
    #include <utility>
    #include <vector>
    class Buffer {{
    public:
        Buffer(int s) : size(s), data(new int[s]) {{}}
        ~Buffer() {{ delete[] data; }}
        Buffer(Buffer&& other) noexcept {{
            data = other.data;
            size = other.size;
            other.data = nullptr;
        }}
    private:
        int* data;
        int size;
    }};
    int main() {{
        std::vector<Buffer> vec;
        vec.push_back(Buffer({val1}));
        return vec.size() + {val2};
    }}
    """
]

def generate_benchmarks(count=500):
    for i in range(count):
        template = random.choice(TEMPLATES)
        vals = {f"val{j}": random.randint(1, 100) for j in range(1, 10)}
        try:
            content = template.format(**vals)
            file_path = OUTPUT_DIR / f"cpp_gen_{i:03d}.cpp"
            with open(file_path, "w") as f:
                f.write(content)
        except:
            continue
    print(f"Generated {count} C++ benchmarks in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_benchmarks()
