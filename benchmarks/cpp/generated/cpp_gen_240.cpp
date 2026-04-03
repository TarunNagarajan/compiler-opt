
    class Shape {
    public:
        virtual int area() = 0;
        virtual ~Shape() {}
    };
    class Square : public Shape {
    public:
        Square(int s) : side(s) {}
        int area() override { return side * side; }
    private:
        int side;
    };
    int main() {
        Shape* s = new Square(68);
        int res = s->area();
        delete s;
        return res + 10;
    }
    