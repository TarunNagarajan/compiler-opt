; ModuleID = 'benchmarks\diverse_synthetic\stencil\stencil_0000.c'
source_filename = "benchmarks\\diverse_synthetic\\stencil\\stencil_0000.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@u = dso_local global [812 x double] zeroinitializer, align 16
@v = dso_local global [812 x double] zeroinitializer, align 16

; Function Attrs: noinline nounwind uwtable
define dso_local void @fsink(double noundef %0) #0 {
  %2 = alloca double, align 8
  store double %0, ptr %2, align 8
  %3 = load double, ptr %2, align 8
  %4 = fcmp ogt double %3, 1.000000e+18
  br i1 %4, label %5, label %8

5:                                                ; preds = %1
  %6 = load double, ptr %2, align 8
  %7 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %6)
  br label %8

8:                                                ; preds = %5, %1
  ret void
}

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca double, align 8
  %7 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  br label %8

8:                                                ; preds = %18, %0
  %9 = load i32, ptr %2, align 4
  %10 = icmp slt i32 %9, 812
  br i1 %10, label %11, label %21

11:                                               ; preds = %8
  %12 = load i32, ptr %2, align 4
  %13 = sitofp i32 %12 to double
  %14 = fdiv double %13, 8.120000e+02
  %15 = load i32, ptr %2, align 4
  %16 = sext i32 %15 to i64
  %17 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %16
  store double %14, ptr %17, align 8
  br label %18

18:                                               ; preds = %11
  %19 = load i32, ptr %2, align 4
  %20 = add nsw i32 %19, 1
  store i32 %20, ptr %2, align 4
  br label %8, !llvm.loop !8

21:                                               ; preds = %8
  store i32 0, ptr %3, align 4
  br label %22

22:                                               ; preds = %81, %21
  %23 = load i32, ptr %3, align 4
  %24 = icmp slt i32 %23, 96
  br i1 %24, label %25, label %84

25:                                               ; preds = %22
  store i32 2, ptr %4, align 4
  br label %26

26:                                               ; preds = %62, %25
  %27 = load i32, ptr %4, align 4
  %28 = icmp slt i32 %27, 810
  br i1 %28, label %29, label %65

29:                                               ; preds = %26
  %30 = load i32, ptr %4, align 4
  %31 = sub nsw i32 %30, 2
  %32 = sext i32 %31 to i64
  %33 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %32
  %34 = load double, ptr %33, align 8
  %35 = fneg double %34
  %36 = load i32, ptr %4, align 4
  %37 = sub nsw i32 %36, 1
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %38
  %40 = load double, ptr %39, align 8
  %41 = call double @llvm.fmuladd.f64(double 4.000000e+00, double %40, double %35)
  %42 = load i32, ptr %4, align 4
  %43 = sext i32 %42 to i64
  %44 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %43
  %45 = load double, ptr %44, align 8
  %46 = call double @llvm.fmuladd.f64(double 1.000000e+01, double %45, double %41)
  %47 = load i32, ptr %4, align 4
  %48 = add nsw i32 %47, 1
  %49 = sext i32 %48 to i64
  %50 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %49
  %51 = load double, ptr %50, align 8
  %52 = call double @llvm.fmuladd.f64(double 4.000000e+00, double %51, double %46)
  %53 = load i32, ptr %4, align 4
  %54 = add nsw i32 %53, 2
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %55
  %57 = load double, ptr %56, align 8
  %58 = fsub double %52, %57
  %59 = load i32, ptr %4, align 4
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds [812 x double], ptr @v, i64 0, i64 %60
  store double %58, ptr %61, align 8
  br label %62

62:                                               ; preds = %29
  %63 = load i32, ptr %4, align 4
  %64 = add nsw i32 %63, 1
  store i32 %64, ptr %4, align 4
  br label %26, !llvm.loop !10

65:                                               ; preds = %26
  store i32 0, ptr %5, align 4
  br label %66

66:                                               ; preds = %77, %65
  %67 = load i32, ptr %5, align 4
  %68 = icmp slt i32 %67, 812
  br i1 %68, label %69, label %80

69:                                               ; preds = %66
  %70 = load i32, ptr %5, align 4
  %71 = sext i32 %70 to i64
  %72 = getelementptr inbounds [812 x double], ptr @v, i64 0, i64 %71
  %73 = load double, ptr %72, align 8
  %74 = load i32, ptr %5, align 4
  %75 = sext i32 %74 to i64
  %76 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %75
  store double %73, ptr %76, align 8
  br label %77

77:                                               ; preds = %69
  %78 = load i32, ptr %5, align 4
  %79 = add nsw i32 %78, 1
  store i32 %79, ptr %5, align 4
  br label %66, !llvm.loop !11

80:                                               ; preds = %66
  br label %81

81:                                               ; preds = %80
  %82 = load i32, ptr %3, align 4
  %83 = add nsw i32 %82, 1
  store i32 %83, ptr %3, align 4
  br label %22, !llvm.loop !12

84:                                               ; preds = %22
  store double 0.000000e+00, ptr %6, align 8
  store i32 0, ptr %7, align 4
  br label %85

85:                                               ; preds = %95, %84
  %86 = load i32, ptr %7, align 4
  %87 = icmp slt i32 %86, 812
  br i1 %87, label %88, label %98

88:                                               ; preds = %85
  %89 = load i32, ptr %7, align 4
  %90 = sext i32 %89 to i64
  %91 = getelementptr inbounds [812 x double], ptr @u, i64 0, i64 %90
  %92 = load double, ptr %91, align 8
  %93 = load double, ptr %6, align 8
  %94 = fadd double %93, %92
  store double %94, ptr %6, align 8
  br label %95

95:                                               ; preds = %88
  %96 = load i32, ptr %7, align 4
  %97 = add nsw i32 %96, 1
  store i32 %97, ptr %7, align 4
  br label %85, !llvm.loop !13

98:                                               ; preds = %85
  %99 = load double, ptr %6, align 8
  call void @fsink(double noundef %99)
  ret i32 0
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\diverse_synthetic\\stencil/stencil_0000.c", directory: "C:/Users/ultim/compiler-opt")
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
