; ModuleID = 'benchmarks\diverse_synthetic\deep_call_chain\deep_call_chain_0000.c'
source_filename = "benchmarks\\diverse_synthetic\\deep_call_chain\\deep_call_chain_0000.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @sink(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = icmp eq i32 %3, 2147483647
  br i1 %4, label %5, label %8

5:                                                ; preds = %1
  %6 = load i32, ptr %2, align 4
  %7 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, i32 noundef %6)
  br label %8

8:                                                ; preds = %5, %1
  ret void
}

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_0(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 2
  %13 = add nsw i32 %12, 10
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 3
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_2(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_1(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_2(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 4
  %13 = add nsw i32 %12, 2
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 2
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_4(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_3(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_1(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 2
  %13 = add nsw i32 %12, 8
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 2
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_3(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_2(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_3(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 2
  %13 = add nsw i32 %12, 9
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 5
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_5(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_4(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_4(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 4
  %13 = add nsw i32 %12, 4
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 5
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_0(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_5(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @state_5(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %2
  %9 = load i32, ptr %4, align 4
  store i32 %9, ptr %3, align 4
  br label %27

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  %12 = mul nsw i32 %11, 2
  %13 = add nsw i32 %12, 2
  store i32 %13, ptr %4, align 4
  %14 = load i32, ptr %4, align 4
  %15 = srem i32 %14, 4
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %17, label %22

17:                                               ; preds = %10
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %5, align 4
  %20 = sub nsw i32 %19, 1
  %21 = call i32 @state_1(i32 noundef %18, i32 noundef %20)
  store i32 %21, ptr %3, align 4
  br label %27

22:                                               ; preds = %10
  %23 = load i32, ptr %4, align 4
  %24 = load i32, ptr %5, align 4
  %25 = sub nsw i32 %24, 1
  %26 = call i32 @state_0(i32 noundef %23, i32 noundef %25)
  store i32 %26, ptr %3, align 4
  br label %27

27:                                               ; preds = %22, %17, %8
  %28 = load i32, ptr %3, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %2 = call i32 @state_0(i32 noundef 1, i32 noundef 169)
  call void @sink(i32 noundef %2)
  ret i32 0
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\diverse_synthetic\\deep_call_chain/deep_call_chain_0000.c", directory: "C:/Users/ultim/compiler-opt")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 21.1.8"}
