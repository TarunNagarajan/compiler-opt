
define i32 @main() {
entry:
  %x = alloca i32
  store i32 0, i32* %x
  %val = load i32, i32* %x
  %res = add i32 %val, 42
  ret i32 %res
}
