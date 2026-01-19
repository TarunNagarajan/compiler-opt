; ModuleID = 'benchmarks\atax.c'
source_filename = "benchmarks\\atax.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"ATAX Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3) #0 {
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  store i32 %0, ptr %5, align 4
  store i32 %1, ptr %6, align 4
  store ptr %2, ptr %7, align 8
  store ptr %3, ptr %8, align 8
  %12 = load i32, ptr %5, align 4
  %13 = zext i32 %12 to i64
  %14 = load i32, ptr %6, align 4
  %15 = zext i32 %14 to i64
  %16 = load i32, ptr %6, align 4
  %17 = zext i32 %16 to i64
  store i32 0, ptr %9, align 4
  br label %18

18:                                               ; preds = %33, %4
  %19 = load i32, ptr %9, align 4
  %20 = load i32, ptr %6, align 4
  %21 = icmp slt i32 %19, %20
  br i1 %21, label %22, label %36

22:                                               ; preds = %18
  %23 = load i32, ptr %9, align 4
  %24 = sitofp i32 %23 to double
  %25 = load i32, ptr %6, align 4
  %26 = sitofp i32 %25 to double
  %27 = fdiv double %24, %26
  %28 = fadd double 1.000000e+00, %27
  %29 = load ptr, ptr %8, align 8
  %30 = load i32, ptr %9, align 4
  %31 = sext i32 %30 to i64
  %32 = getelementptr inbounds double, ptr %29, i64 %31
  store double %28, ptr %32, align 8
  br label %33

33:                                               ; preds = %22
  %34 = load i32, ptr %9, align 4
  %35 = add nsw i32 %34, 1
  store i32 %35, ptr %9, align 4
  br label %18, !llvm.loop !8

36:                                               ; preds = %18
  store i32 0, ptr %10, align 4
  br label %37

37:                                               ; preds = %68, %36
  %38 = load i32, ptr %10, align 4
  %39 = load i32, ptr %5, align 4
  %40 = icmp slt i32 %38, %39
  br i1 %40, label %41, label %71

41:                                               ; preds = %37
  store i32 0, ptr %11, align 4
  br label %42

42:                                               ; preds = %64, %41
  %43 = load i32, ptr %11, align 4
  %44 = load i32, ptr %6, align 4
  %45 = icmp slt i32 %43, %44
  br i1 %45, label %46, label %67

46:                                               ; preds = %42
  %47 = load i32, ptr %10, align 4
  %48 = sitofp i32 %47 to double
  %49 = load i32, ptr %11, align 4
  %50 = add nsw i32 %49, 1
  %51 = sitofp i32 %50 to double
  %52 = fmul double %48, %51
  %53 = load i32, ptr %5, align 4
  %54 = sitofp i32 %53 to double
  %55 = fdiv double %52, %54
  %56 = load ptr, ptr %7, align 8
  %57 = load i32, ptr %10, align 4
  %58 = sext i32 %57 to i64
  %59 = mul nsw i64 %58, %15
  %60 = getelementptr inbounds double, ptr %56, i64 %59
  %61 = load i32, ptr %11, align 4
  %62 = sext i32 %61 to i64
  %63 = getelementptr inbounds double, ptr %60, i64 %62
  store double %55, ptr %63, align 8
  br label %64

64:                                               ; preds = %46
  %65 = load i32, ptr %11, align 4
  %66 = add nsw i32 %65, 1
  store i32 %66, ptr %11, align 4
  br label %42, !llvm.loop !10

67:                                               ; preds = %42
  br label %68

68:                                               ; preds = %67
  %69 = load i32, ptr %10, align 4
  %70 = add nsw i32 %69, 1
  store i32 %70, ptr %10, align 4
  br label %37, !llvm.loop !11

71:                                               ; preds = %37
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @atax(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  store i32 %0, ptr %7, align 4
  store i32 %1, ptr %8, align 4
  store ptr %2, ptr %9, align 8
  store ptr %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %17 = load i32, ptr %7, align 4
  %18 = zext i32 %17 to i64
  %19 = load i32, ptr %8, align 4
  %20 = zext i32 %19 to i64
  %21 = load i32, ptr %8, align 4
  %22 = zext i32 %21 to i64
  %23 = load i32, ptr %8, align 4
  %24 = zext i32 %23 to i64
  %25 = load i32, ptr %7, align 4
  %26 = zext i32 %25 to i64
  store i32 0, ptr %13, align 4
  br label %27

27:                                               ; preds = %36, %6
  %28 = load i32, ptr %13, align 4
  %29 = load i32, ptr %8, align 4
  %30 = icmp slt i32 %28, %29
  br i1 %30, label %31, label %39

31:                                               ; preds = %27
  %32 = load ptr, ptr %11, align 8
  %33 = load i32, ptr %13, align 4
  %34 = sext i32 %33 to i64
  %35 = getelementptr inbounds double, ptr %32, i64 %34
  store double 0.000000e+00, ptr %35, align 8
  br label %36

36:                                               ; preds = %31
  %37 = load i32, ptr %13, align 4
  %38 = add nsw i32 %37, 1
  store i32 %38, ptr %13, align 4
  br label %27, !llvm.loop !12

39:                                               ; preds = %27
  store i32 0, ptr %14, align 4
  br label %40

40:                                               ; preds = %107, %39
  %41 = load i32, ptr %14, align 4
  %42 = load i32, ptr %7, align 4
  %43 = icmp slt i32 %41, %42
  br i1 %43, label %44, label %110

44:                                               ; preds = %40
  %45 = load ptr, ptr %12, align 8
  %46 = load i32, ptr %14, align 4
  %47 = sext i32 %46 to i64
  %48 = getelementptr inbounds double, ptr %45, i64 %47
  store double 0.000000e+00, ptr %48, align 8
  store i32 0, ptr %15, align 4
  br label %49

49:                                               ; preds = %74, %44
  %50 = load i32, ptr %15, align 4
  %51 = load i32, ptr %8, align 4
  %52 = icmp slt i32 %50, %51
  br i1 %52, label %53, label %77

53:                                               ; preds = %49
  %54 = load ptr, ptr %9, align 8
  %55 = load i32, ptr %14, align 4
  %56 = sext i32 %55 to i64
  %57 = mul nsw i64 %56, %20
  %58 = getelementptr inbounds double, ptr %54, i64 %57
  %59 = load i32, ptr %15, align 4
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds double, ptr %58, i64 %60
  %62 = load double, ptr %61, align 8
  %63 = load ptr, ptr %10, align 8
  %64 = load i32, ptr %15, align 4
  %65 = sext i32 %64 to i64
  %66 = getelementptr inbounds double, ptr %63, i64 %65
  %67 = load double, ptr %66, align 8
  %68 = load ptr, ptr %12, align 8
  %69 = load i32, ptr %14, align 4
  %70 = sext i32 %69 to i64
  %71 = getelementptr inbounds double, ptr %68, i64 %70
  %72 = load double, ptr %71, align 8
  %73 = call double @llvm.fmuladd.f64(double %62, double %67, double %72)
  store double %73, ptr %71, align 8
  br label %74

74:                                               ; preds = %53
  %75 = load i32, ptr %15, align 4
  %76 = add nsw i32 %75, 1
  store i32 %76, ptr %15, align 4
  br label %49, !llvm.loop !13

77:                                               ; preds = %49
  store i32 0, ptr %16, align 4
  br label %78

78:                                               ; preds = %103, %77
  %79 = load i32, ptr %16, align 4
  %80 = load i32, ptr %8, align 4
  %81 = icmp slt i32 %79, %80
  br i1 %81, label %82, label %106

82:                                               ; preds = %78
  %83 = load ptr, ptr %9, align 8
  %84 = load i32, ptr %14, align 4
  %85 = sext i32 %84 to i64
  %86 = mul nsw i64 %85, %20
  %87 = getelementptr inbounds double, ptr %83, i64 %86
  %88 = load i32, ptr %16, align 4
  %89 = sext i32 %88 to i64
  %90 = getelementptr inbounds double, ptr %87, i64 %89
  %91 = load double, ptr %90, align 8
  %92 = load ptr, ptr %12, align 8
  %93 = load i32, ptr %14, align 4
  %94 = sext i32 %93 to i64
  %95 = getelementptr inbounds double, ptr %92, i64 %94
  %96 = load double, ptr %95, align 8
  %97 = load ptr, ptr %11, align 8
  %98 = load i32, ptr %16, align 4
  %99 = sext i32 %98 to i64
  %100 = getelementptr inbounds double, ptr %97, i64 %99
  %101 = load double, ptr %100, align 8
  %102 = call double @llvm.fmuladd.f64(double %91, double %96, double %101)
  store double %102, ptr %100, align 8
  br label %103

103:                                              ; preds = %82
  %104 = load i32, ptr %16, align 4
  %105 = add nsw i32 %104, 1
  store i32 %105, ptr %16, align 4
  br label %78, !llvm.loop !14

106:                                              ; preds = %78
  br label %107

107:                                              ; preds = %106
  %108 = load i32, ptr %14, align 4
  %109 = add nsw i32 %108, 1
  store i32 %109, ptr %14, align 4
  br label %40, !llvm.loop !15

110:                                              ; preds = %40
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 512, ptr %2, align 4
  store i32 512, ptr %3, align 4
  %10 = load i32, ptr %3, align 4
  %11 = zext i32 %10 to i64
  %12 = load i32, ptr %2, align 4
  %13 = zext i32 %12 to i64
  %14 = load i32, ptr %3, align 4
  %15 = zext i32 %14 to i64
  %16 = mul nuw i64 %13, %15
  %17 = mul nuw i64 8, %16
  %18 = call ptr @malloc(i64 noundef %17) #4
  store ptr %18, ptr %4, align 8
  %19 = load i32, ptr %3, align 4
  %20 = sext i32 %19 to i64
  %21 = mul i64 %20, 8
  %22 = call ptr @malloc(i64 noundef %21) #4
  store ptr %22, ptr %5, align 8
  %23 = load i32, ptr %3, align 4
  %24 = sext i32 %23 to i64
  %25 = mul i64 %24, 8
  %26 = call ptr @malloc(i64 noundef %25) #4
  store ptr %26, ptr %6, align 8
  %27 = load i32, ptr %2, align 4
  %28 = sext i32 %27 to i64
  %29 = mul i64 %28, 8
  %30 = call ptr @malloc(i64 noundef %29) #4
  store ptr %30, ptr %7, align 8
  %31 = load i32, ptr %2, align 4
  %32 = load i32, ptr %3, align 4
  %33 = load ptr, ptr %4, align 8
  %34 = load ptr, ptr %5, align 8
  call void @init_array(i32 noundef %31, i32 noundef %32, ptr noundef %33, ptr noundef %34)
  %35 = call i32 @clock()
  store i32 %35, ptr %8, align 4
  %36 = load i32, ptr %2, align 4
  %37 = load i32, ptr %3, align 4
  %38 = load ptr, ptr %4, align 8
  %39 = load ptr, ptr %5, align 8
  %40 = load ptr, ptr %6, align 8
  %41 = load ptr, ptr %7, align 8
  call void @atax(i32 noundef %36, i32 noundef %37, ptr noundef %38, ptr noundef %39, ptr noundef %40, ptr noundef %41)
  %42 = call i32 @clock()
  store i32 %42, ptr %9, align 4
  %43 = load i32, ptr %9, align 4
  %44 = load i32, ptr %8, align 4
  %45 = sub nsw i32 %43, %44
  %46 = sitofp i32 %45 to double
  %47 = fdiv double %46, 1.000000e+03
  %48 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %47)
  %49 = load ptr, ptr %6, align 8
  %50 = getelementptr inbounds double, ptr %49, i64 0
  %51 = load double, ptr %50, align 8
  %52 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %51)
  %53 = load ptr, ptr %4, align 8
  call void @free(ptr noundef %53)
  %54 = load ptr, ptr %5, align 8
  call void @free(ptr noundef %54)
  %55 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %55)
  %56 = load ptr, ptr %7, align 8
  call void @free(ptr noundef %56)
  ret i32 0
}

; Function Attrs: allocsize(0)
declare dso_local ptr @malloc(i64 noundef) #2

declare dso_local i32 @clock() #3

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #3

declare dso_local void @free(ptr noundef) #3

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { allocsize(0) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { allocsize(0) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/atax.c", directory: "C:/Users/ultim/compiler-opt")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 21.1.8"}
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !9}
!11 = distinct !{!11, !9}
!12 = distinct !{!12, !9}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !9}
