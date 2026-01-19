; ModuleID = 'benchmarks\gemm.c'
source_filename = "benchmarks\\gemm.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"GEMM Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef %1, ptr noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  %9 = load i32, ptr %4, align 4
  %10 = zext i32 %9 to i64
  %11 = load i32, ptr %4, align 4
  %12 = zext i32 %11 to i64
  %13 = load i32, ptr %4, align 4
  %14 = zext i32 %13 to i64
  %15 = load i32, ptr %4, align 4
  %16 = zext i32 %15 to i64
  store i32 0, ptr %7, align 4
  br label %17

17:                                               ; preds = %63, %3
  %18 = load i32, ptr %7, align 4
  %19 = load i32, ptr %4, align 4
  %20 = icmp slt i32 %18, %19
  br i1 %20, label %21, label %66

21:                                               ; preds = %17
  store i32 0, ptr %8, align 4
  br label %22

22:                                               ; preds = %59, %21
  %23 = load i32, ptr %8, align 4
  %24 = load i32, ptr %4, align 4
  %25 = icmp slt i32 %23, %24
  br i1 %25, label %26, label %62

26:                                               ; preds = %22
  %27 = load i32, ptr %7, align 4
  %28 = sitofp i32 %27 to double
  %29 = load i32, ptr %8, align 4
  %30 = sitofp i32 %29 to double
  %31 = fmul double %28, %30
  %32 = load i32, ptr %4, align 4
  %33 = sitofp i32 %32 to double
  %34 = fdiv double %31, %33
  %35 = load ptr, ptr %5, align 8
  %36 = load i32, ptr %7, align 4
  %37 = sext i32 %36 to i64
  %38 = mul nsw i64 %37, %12
  %39 = getelementptr inbounds double, ptr %35, i64 %38
  %40 = load i32, ptr %8, align 4
  %41 = sext i32 %40 to i64
  %42 = getelementptr inbounds double, ptr %39, i64 %41
  store double %34, ptr %42, align 8
  %43 = load i32, ptr %7, align 4
  %44 = sitofp i32 %43 to double
  %45 = load i32, ptr %8, align 4
  %46 = sitofp i32 %45 to double
  %47 = fmul double %44, %46
  %48 = load i32, ptr %4, align 4
  %49 = sitofp i32 %48 to double
  %50 = fdiv double %47, %49
  %51 = load ptr, ptr %6, align 8
  %52 = load i32, ptr %7, align 4
  %53 = sext i32 %52 to i64
  %54 = mul nsw i64 %53, %16
  %55 = getelementptr inbounds double, ptr %51, i64 %54
  %56 = load i32, ptr %8, align 4
  %57 = sext i32 %56 to i64
  %58 = getelementptr inbounds double, ptr %55, i64 %57
  store double %50, ptr %58, align 8
  br label %59

59:                                               ; preds = %26
  %60 = load i32, ptr %8, align 4
  %61 = add nsw i32 %60, 1
  store i32 %61, ptr %8, align 4
  br label %22, !llvm.loop !8

62:                                               ; preds = %22
  br label %63

63:                                               ; preds = %62
  %64 = load i32, ptr %7, align 4
  %65 = add nsw i32 %64, 1
  store i32 %65, ptr %7, align 4
  br label %17, !llvm.loop !10

66:                                               ; preds = %17
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @gemm(i32 noundef %0, double noundef %1, double noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca i32, align 4
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  store i32 %0, ptr %7, align 4
  store double %1, ptr %8, align 8
  store double %2, ptr %9, align 8
  store ptr %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %16 = load i32, ptr %7, align 4
  %17 = zext i32 %16 to i64
  %18 = load i32, ptr %7, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %7, align 4
  %21 = zext i32 %20 to i64
  %22 = load i32, ptr %7, align 4
  %23 = zext i32 %22 to i64
  %24 = load i32, ptr %7, align 4
  %25 = zext i32 %24 to i64
  %26 = load i32, ptr %7, align 4
  %27 = zext i32 %26 to i64
  store i32 0, ptr %13, align 4
  br label %28

28:                                               ; preds = %92, %6
  %29 = load i32, ptr %13, align 4
  %30 = load i32, ptr %7, align 4
  %31 = icmp slt i32 %29, %30
  br i1 %31, label %32, label %95

32:                                               ; preds = %28
  store i32 0, ptr %14, align 4
  br label %33

33:                                               ; preds = %88, %32
  %34 = load i32, ptr %14, align 4
  %35 = load i32, ptr %7, align 4
  %36 = icmp slt i32 %34, %35
  br i1 %36, label %37, label %91

37:                                               ; preds = %33
  %38 = load double, ptr %9, align 8
  %39 = load ptr, ptr %10, align 8
  %40 = load i32, ptr %13, align 4
  %41 = sext i32 %40 to i64
  %42 = mul nsw i64 %41, %19
  %43 = getelementptr inbounds double, ptr %39, i64 %42
  %44 = load i32, ptr %14, align 4
  %45 = sext i32 %44 to i64
  %46 = getelementptr inbounds double, ptr %43, i64 %45
  %47 = load double, ptr %46, align 8
  %48 = fmul double %47, %38
  store double %48, ptr %46, align 8
  store i32 0, ptr %15, align 4
  br label %49

49:                                               ; preds = %84, %37
  %50 = load i32, ptr %15, align 4
  %51 = load i32, ptr %7, align 4
  %52 = icmp slt i32 %50, %51
  br i1 %52, label %53, label %87

53:                                               ; preds = %49
  %54 = load double, ptr %8, align 8
  %55 = load ptr, ptr %11, align 8
  %56 = load i32, ptr %13, align 4
  %57 = sext i32 %56 to i64
  %58 = mul nsw i64 %57, %23
  %59 = getelementptr inbounds double, ptr %55, i64 %58
  %60 = load i32, ptr %15, align 4
  %61 = sext i32 %60 to i64
  %62 = getelementptr inbounds double, ptr %59, i64 %61
  %63 = load double, ptr %62, align 8
  %64 = fmul double %54, %63
  %65 = load ptr, ptr %12, align 8
  %66 = load i32, ptr %15, align 4
  %67 = sext i32 %66 to i64
  %68 = mul nsw i64 %67, %27
  %69 = getelementptr inbounds double, ptr %65, i64 %68
  %70 = load i32, ptr %14, align 4
  %71 = sext i32 %70 to i64
  %72 = getelementptr inbounds double, ptr %69, i64 %71
  %73 = load double, ptr %72, align 8
  %74 = load ptr, ptr %10, align 8
  %75 = load i32, ptr %13, align 4
  %76 = sext i32 %75 to i64
  %77 = mul nsw i64 %76, %19
  %78 = getelementptr inbounds double, ptr %74, i64 %77
  %79 = load i32, ptr %14, align 4
  %80 = sext i32 %79 to i64
  %81 = getelementptr inbounds double, ptr %78, i64 %80
  %82 = load double, ptr %81, align 8
  %83 = call double @llvm.fmuladd.f64(double %64, double %73, double %82)
  store double %83, ptr %81, align 8
  br label %84

84:                                               ; preds = %53
  %85 = load i32, ptr %15, align 4
  %86 = add nsw i32 %85, 1
  store i32 %86, ptr %15, align 4
  br label %49, !llvm.loop !11

87:                                               ; preds = %49
  br label %88

88:                                               ; preds = %87
  %89 = load i32, ptr %14, align 4
  %90 = add nsw i32 %89, 1
  store i32 %90, ptr %14, align 4
  br label %33, !llvm.loop !12

91:                                               ; preds = %33
  br label %92

92:                                               ; preds = %91
  %93 = load i32, ptr %13, align 4
  %94 = add nsw i32 %93, 1
  store i32 %94, ptr %13, align 4
  br label %28, !llvm.loop !13

95:                                               ; preds = %28
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca double, align 8
  %8 = alloca double, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store i32 512, ptr %6, align 4
  store double 1.500000e+00, ptr %7, align 8
  store double 1.200000e+00, ptr %8, align 8
  %14 = load i32, ptr %6, align 4
  %15 = zext i32 %14 to i64
  %16 = load i32, ptr %6, align 4
  %17 = zext i32 %16 to i64
  %18 = load i32, ptr %6, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %6, align 4
  %21 = zext i32 %20 to i64
  %22 = mul nuw i64 %19, %21
  %23 = mul nuw i64 8, %22
  %24 = call ptr @malloc(i64 noundef %23) #4
  store ptr %24, ptr %9, align 8
  %25 = load i32, ptr %6, align 4
  %26 = zext i32 %25 to i64
  %27 = load i32, ptr %6, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %6, align 4
  %30 = zext i32 %29 to i64
  %31 = load i32, ptr %6, align 4
  %32 = zext i32 %31 to i64
  %33 = mul nuw i64 %30, %32
  %34 = mul nuw i64 8, %33
  %35 = call ptr @malloc(i64 noundef %34) #4
  store ptr %35, ptr %10, align 8
  %36 = load i32, ptr %6, align 4
  %37 = zext i32 %36 to i64
  %38 = load i32, ptr %6, align 4
  %39 = zext i32 %38 to i64
  %40 = load i32, ptr %6, align 4
  %41 = zext i32 %40 to i64
  %42 = load i32, ptr %6, align 4
  %43 = zext i32 %42 to i64
  %44 = mul nuw i64 %41, %43
  %45 = mul nuw i64 8, %44
  %46 = call ptr @malloc(i64 noundef %45) #4
  store ptr %46, ptr %11, align 8
  %47 = load i32, ptr %6, align 4
  %48 = load ptr, ptr %9, align 8
  %49 = load ptr, ptr %10, align 8
  call void @init_array(i32 noundef %47, ptr noundef %48, ptr noundef %49)
  %50 = call i32 @clock()
  store i32 %50, ptr %12, align 4
  %51 = load i32, ptr %6, align 4
  %52 = load double, ptr %7, align 8
  %53 = load double, ptr %8, align 8
  %54 = load ptr, ptr %11, align 8
  %55 = load ptr, ptr %9, align 8
  %56 = load ptr, ptr %10, align 8
  call void @gemm(i32 noundef %51, double noundef %52, double noundef %53, ptr noundef %54, ptr noundef %55, ptr noundef %56)
  %57 = call i32 @clock()
  store i32 %57, ptr %13, align 4
  %58 = load i32, ptr %13, align 4
  %59 = load i32, ptr %12, align 4
  %60 = sub nsw i32 %58, %59
  %61 = sitofp i32 %60 to double
  %62 = fdiv double %61, 1.000000e+03
  %63 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %62)
  %64 = load ptr, ptr %11, align 8
  %65 = mul nsw i64 0, %39
  %66 = getelementptr inbounds double, ptr %64, i64 %65
  %67 = getelementptr inbounds double, ptr %66, i64 0
  %68 = load double, ptr %67, align 8
  %69 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %68)
  %70 = load ptr, ptr %9, align 8
  call void @free(ptr noundef %70)
  %71 = load ptr, ptr %10, align 8
  call void @free(ptr noundef %71)
  %72 = load ptr, ptr %11, align 8
  call void @free(ptr noundef %72)
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
!1 = !DIFile(filename: "benchmarks/gemm.c", directory: "C:/Users/ultim/compiler-opt")
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
