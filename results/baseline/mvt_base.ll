; ModuleID = 'benchmarks\mvt.c'
source_filename = "benchmarks\\mvt.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [26 x i8] c"MVT Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  store i32 %0, ptr %7, align 4
  store ptr %1, ptr %8, align 8
  store ptr %2, ptr %9, align 8
  store ptr %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %15 = load i32, ptr %7, align 4
  %16 = zext i32 %15 to i64
  %17 = load i32, ptr %7, align 4
  %18 = zext i32 %17 to i64
  %19 = load i32, ptr %7, align 4
  %20 = zext i32 %19 to i64
  %21 = load i32, ptr %7, align 4
  %22 = zext i32 %21 to i64
  %23 = load i32, ptr %7, align 4
  %24 = zext i32 %23 to i64
  %25 = load i32, ptr %7, align 4
  %26 = zext i32 %25 to i64
  store i32 0, ptr %13, align 4
  br label %27

27:                                               ; preds = %101, %6
  %28 = load i32, ptr %13, align 4
  %29 = load i32, ptr %7, align 4
  %30 = icmp slt i32 %28, %29
  br i1 %30, label %31, label %104

31:                                               ; preds = %27
  %32 = load i32, ptr %13, align 4
  %33 = sitofp i32 %32 to double
  %34 = load i32, ptr %7, align 4
  %35 = sitofp i32 %34 to double
  %36 = fdiv double %33, %35
  %37 = load ptr, ptr %8, align 8
  %38 = load i32, ptr %13, align 4
  %39 = sext i32 %38 to i64
  %40 = getelementptr inbounds double, ptr %37, i64 %39
  store double %36, ptr %40, align 8
  %41 = load i32, ptr %13, align 4
  %42 = add nsw i32 %41, 1
  %43 = load i32, ptr %7, align 4
  %44 = srem i32 %42, %43
  %45 = sitofp i32 %44 to double
  %46 = load i32, ptr %7, align 4
  %47 = sitofp i32 %46 to double
  %48 = fdiv double %45, %47
  %49 = load ptr, ptr %9, align 8
  %50 = load i32, ptr %13, align 4
  %51 = sext i32 %50 to i64
  %52 = getelementptr inbounds double, ptr %49, i64 %51
  store double %48, ptr %52, align 8
  %53 = load i32, ptr %13, align 4
  %54 = add nsw i32 %53, 3
  %55 = load i32, ptr %7, align 4
  %56 = srem i32 %54, %55
  %57 = sitofp i32 %56 to double
  %58 = load i32, ptr %7, align 4
  %59 = sitofp i32 %58 to double
  %60 = fdiv double %57, %59
  %61 = load ptr, ptr %10, align 8
  %62 = load i32, ptr %13, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds double, ptr %61, i64 %63
  store double %60, ptr %64, align 8
  %65 = load i32, ptr %13, align 4
  %66 = add nsw i32 %65, 4
  %67 = load i32, ptr %7, align 4
  %68 = srem i32 %66, %67
  %69 = sitofp i32 %68 to double
  %70 = load i32, ptr %7, align 4
  %71 = sitofp i32 %70 to double
  %72 = fdiv double %69, %71
  %73 = load ptr, ptr %11, align 8
  %74 = load i32, ptr %13, align 4
  %75 = sext i32 %74 to i64
  %76 = getelementptr inbounds double, ptr %73, i64 %75
  store double %72, ptr %76, align 8
  store i32 0, ptr %14, align 4
  br label %77

77:                                               ; preds = %97, %31
  %78 = load i32, ptr %14, align 4
  %79 = load i32, ptr %7, align 4
  %80 = icmp slt i32 %78, %79
  br i1 %80, label %81, label %100

81:                                               ; preds = %77
  %82 = load i32, ptr %13, align 4
  %83 = load i32, ptr %14, align 4
  %84 = mul nsw i32 %82, %83
  %85 = sitofp i32 %84 to double
  %86 = load i32, ptr %7, align 4
  %87 = sitofp i32 %86 to double
  %88 = fdiv double %85, %87
  %89 = load ptr, ptr %12, align 8
  %90 = load i32, ptr %13, align 4
  %91 = sext i32 %90 to i64
  %92 = mul nsw i64 %91, %26
  %93 = getelementptr inbounds double, ptr %89, i64 %92
  %94 = load i32, ptr %14, align 4
  %95 = sext i32 %94 to i64
  %96 = getelementptr inbounds double, ptr %93, i64 %95
  store double %88, ptr %96, align 8
  br label %97

97:                                               ; preds = %81
  %98 = load i32, ptr %14, align 4
  %99 = add nsw i32 %98, 1
  store i32 %99, ptr %14, align 4
  br label %77, !llvm.loop !8

100:                                              ; preds = %77
  br label %101

101:                                              ; preds = %100
  %102 = load i32, ptr %13, align 4
  %103 = add nsw i32 %102, 1
  store i32 %103, ptr %13, align 4
  br label %27, !llvm.loop !10

104:                                              ; preds = %27
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @mvt(i32 noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  store i32 %0, ptr %7, align 4
  store ptr %1, ptr %8, align 8
  store ptr %2, ptr %9, align 8
  store ptr %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %17 = load i32, ptr %7, align 4
  %18 = zext i32 %17 to i64
  %19 = load i32, ptr %7, align 4
  %20 = zext i32 %19 to i64
  %21 = load i32, ptr %7, align 4
  %22 = zext i32 %21 to i64
  %23 = load i32, ptr %7, align 4
  %24 = zext i32 %23 to i64
  %25 = load i32, ptr %7, align 4
  %26 = zext i32 %25 to i64
  %27 = load i32, ptr %7, align 4
  %28 = zext i32 %27 to i64
  store i32 0, ptr %13, align 4
  br label %29

29:                                               ; preds = %63, %6
  %30 = load i32, ptr %13, align 4
  %31 = load i32, ptr %7, align 4
  %32 = icmp slt i32 %30, %31
  br i1 %32, label %33, label %66

33:                                               ; preds = %29
  store i32 0, ptr %14, align 4
  br label %34

34:                                               ; preds = %59, %33
  %35 = load i32, ptr %14, align 4
  %36 = load i32, ptr %7, align 4
  %37 = icmp slt i32 %35, %36
  br i1 %37, label %38, label %62

38:                                               ; preds = %34
  %39 = load ptr, ptr %12, align 8
  %40 = load i32, ptr %13, align 4
  %41 = sext i32 %40 to i64
  %42 = mul nsw i64 %41, %28
  %43 = getelementptr inbounds double, ptr %39, i64 %42
  %44 = load i32, ptr %14, align 4
  %45 = sext i32 %44 to i64
  %46 = getelementptr inbounds double, ptr %43, i64 %45
  %47 = load double, ptr %46, align 8
  %48 = load ptr, ptr %10, align 8
  %49 = load i32, ptr %14, align 4
  %50 = sext i32 %49 to i64
  %51 = getelementptr inbounds double, ptr %48, i64 %50
  %52 = load double, ptr %51, align 8
  %53 = load ptr, ptr %8, align 8
  %54 = load i32, ptr %13, align 4
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds double, ptr %53, i64 %55
  %57 = load double, ptr %56, align 8
  %58 = call double @llvm.fmuladd.f64(double %47, double %52, double %57)
  store double %58, ptr %56, align 8
  br label %59

59:                                               ; preds = %38
  %60 = load i32, ptr %14, align 4
  %61 = add nsw i32 %60, 1
  store i32 %61, ptr %14, align 4
  br label %34, !llvm.loop !11

62:                                               ; preds = %34
  br label %63

63:                                               ; preds = %62
  %64 = load i32, ptr %13, align 4
  %65 = add nsw i32 %64, 1
  store i32 %65, ptr %13, align 4
  br label %29, !llvm.loop !12

66:                                               ; preds = %29
  store i32 0, ptr %15, align 4
  br label %67

67:                                               ; preds = %101, %66
  %68 = load i32, ptr %15, align 4
  %69 = load i32, ptr %7, align 4
  %70 = icmp slt i32 %68, %69
  br i1 %70, label %71, label %104

71:                                               ; preds = %67
  store i32 0, ptr %16, align 4
  br label %72

72:                                               ; preds = %97, %71
  %73 = load i32, ptr %16, align 4
  %74 = load i32, ptr %7, align 4
  %75 = icmp slt i32 %73, %74
  br i1 %75, label %76, label %100

76:                                               ; preds = %72
  %77 = load ptr, ptr %12, align 8
  %78 = load i32, ptr %16, align 4
  %79 = sext i32 %78 to i64
  %80 = mul nsw i64 %79, %28
  %81 = getelementptr inbounds double, ptr %77, i64 %80
  %82 = load i32, ptr %15, align 4
  %83 = sext i32 %82 to i64
  %84 = getelementptr inbounds double, ptr %81, i64 %83
  %85 = load double, ptr %84, align 8
  %86 = load ptr, ptr %11, align 8
  %87 = load i32, ptr %16, align 4
  %88 = sext i32 %87 to i64
  %89 = getelementptr inbounds double, ptr %86, i64 %88
  %90 = load double, ptr %89, align 8
  %91 = load ptr, ptr %9, align 8
  %92 = load i32, ptr %15, align 4
  %93 = sext i32 %92 to i64
  %94 = getelementptr inbounds double, ptr %91, i64 %93
  %95 = load double, ptr %94, align 8
  %96 = call double @llvm.fmuladd.f64(double %85, double %90, double %95)
  store double %96, ptr %94, align 8
  br label %97

97:                                               ; preds = %76
  %98 = load i32, ptr %16, align 4
  %99 = add nsw i32 %98, 1
  store i32 %99, ptr %16, align 4
  br label %72, !llvm.loop !13

100:                                              ; preds = %72
  br label %101

101:                                              ; preds = %100
  %102 = load i32, ptr %15, align 4
  %103 = add nsw i32 %102, 1
  store i32 %103, ptr %15, align 4
  br label %67, !llvm.loop !14

104:                                              ; preds = %67
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 512, ptr %2, align 4
  %10 = load i32, ptr %2, align 4
  %11 = sext i32 %10 to i64
  %12 = mul i64 %11, 8
  %13 = call ptr @malloc(i64 noundef %12) #4
  store ptr %13, ptr %3, align 8
  %14 = load i32, ptr %2, align 4
  %15 = sext i32 %14 to i64
  %16 = mul i64 %15, 8
  %17 = call ptr @malloc(i64 noundef %16) #4
  store ptr %17, ptr %4, align 8
  %18 = load i32, ptr %2, align 4
  %19 = sext i32 %18 to i64
  %20 = mul i64 %19, 8
  %21 = call ptr @malloc(i64 noundef %20) #4
  store ptr %21, ptr %5, align 8
  %22 = load i32, ptr %2, align 4
  %23 = sext i32 %22 to i64
  %24 = mul i64 %23, 8
  %25 = call ptr @malloc(i64 noundef %24) #4
  store ptr %25, ptr %6, align 8
  %26 = load i32, ptr %2, align 4
  %27 = zext i32 %26 to i64
  %28 = load i32, ptr %2, align 4
  %29 = zext i32 %28 to i64
  %30 = load i32, ptr %2, align 4
  %31 = zext i32 %30 to i64
  %32 = mul nuw i64 %29, %31
  %33 = mul nuw i64 8, %32
  %34 = call ptr @malloc(i64 noundef %33) #4
  store ptr %34, ptr %7, align 8
  %35 = load i32, ptr %2, align 4
  %36 = load ptr, ptr %3, align 8
  %37 = load ptr, ptr %4, align 8
  %38 = load ptr, ptr %5, align 8
  %39 = load ptr, ptr %6, align 8
  %40 = load ptr, ptr %7, align 8
  call void @init_array(i32 noundef %35, ptr noundef %36, ptr noundef %37, ptr noundef %38, ptr noundef %39, ptr noundef %40)
  %41 = call i32 @clock()
  store i32 %41, ptr %8, align 4
  %42 = load i32, ptr %2, align 4
  %43 = load ptr, ptr %3, align 8
  %44 = load ptr, ptr %4, align 8
  %45 = load ptr, ptr %5, align 8
  %46 = load ptr, ptr %6, align 8
  %47 = load ptr, ptr %7, align 8
  call void @mvt(i32 noundef %42, ptr noundef %43, ptr noundef %44, ptr noundef %45, ptr noundef %46, ptr noundef %47)
  %48 = call i32 @clock()
  store i32 %48, ptr %9, align 4
  %49 = load i32, ptr %9, align 4
  %50 = load i32, ptr %8, align 4
  %51 = sub nsw i32 %49, %50
  %52 = sitofp i32 %51 to double
  %53 = fdiv double %52, 1.000000e+03
  %54 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %53)
  %55 = load ptr, ptr %3, align 8
  %56 = getelementptr inbounds double, ptr %55, i64 0
  %57 = load double, ptr %56, align 8
  %58 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %57)
  %59 = load ptr, ptr %3, align 8
  call void @free(ptr noundef %59)
  %60 = load ptr, ptr %4, align 8
  call void @free(ptr noundef %60)
  %61 = load ptr, ptr %5, align 8
  call void @free(ptr noundef %61)
  %62 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %62)
  %63 = load ptr, ptr %7, align 8
  call void @free(ptr noundef %63)
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
!1 = !DIFile(filename: "benchmarks/mvt.c", directory: "C:/Users/ultim/compiler-opt")
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
