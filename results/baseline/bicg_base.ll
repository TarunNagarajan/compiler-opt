; ModuleID = 'benchmarks\bicg.c'
source_filename = "benchmarks\\bicg.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"BiCG Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4) #0 {
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  store i32 %0, ptr %6, align 4
  store i32 %1, ptr %7, align 4
  store ptr %2, ptr %8, align 8
  store ptr %3, ptr %9, align 8
  store ptr %4, ptr %10, align 8
  %15 = load i32, ptr %6, align 4
  %16 = zext i32 %15 to i64
  %17 = load i32, ptr %7, align 4
  %18 = zext i32 %17 to i64
  %19 = load i32, ptr %7, align 4
  %20 = zext i32 %19 to i64
  %21 = load i32, ptr %6, align 4
  %22 = zext i32 %21 to i64
  store i32 0, ptr %11, align 4
  br label %23

23:                                               ; preds = %37, %5
  %24 = load i32, ptr %11, align 4
  %25 = load i32, ptr %7, align 4
  %26 = icmp slt i32 %24, %25
  br i1 %26, label %27, label %40

27:                                               ; preds = %23
  %28 = load i32, ptr %11, align 4
  %29 = sitofp i32 %28 to double
  %30 = load i32, ptr %7, align 4
  %31 = sitofp i32 %30 to double
  %32 = fdiv double %29, %31
  %33 = load ptr, ptr %9, align 8
  %34 = load i32, ptr %11, align 4
  %35 = sext i32 %34 to i64
  %36 = getelementptr inbounds double, ptr %33, i64 %35
  store double %32, ptr %36, align 8
  br label %37

37:                                               ; preds = %27
  %38 = load i32, ptr %11, align 4
  %39 = add nsw i32 %38, 1
  store i32 %39, ptr %11, align 4
  br label %23, !llvm.loop !8

40:                                               ; preds = %23
  store i32 0, ptr %12, align 4
  br label %41

41:                                               ; preds = %55, %40
  %42 = load i32, ptr %12, align 4
  %43 = load i32, ptr %6, align 4
  %44 = icmp slt i32 %42, %43
  br i1 %44, label %45, label %58

45:                                               ; preds = %41
  %46 = load i32, ptr %12, align 4
  %47 = sitofp i32 %46 to double
  %48 = load i32, ptr %6, align 4
  %49 = sitofp i32 %48 to double
  %50 = fdiv double %47, %49
  %51 = load ptr, ptr %10, align 8
  %52 = load i32, ptr %12, align 4
  %53 = sext i32 %52 to i64
  %54 = getelementptr inbounds double, ptr %51, i64 %53
  store double %50, ptr %54, align 8
  br label %55

55:                                               ; preds = %45
  %56 = load i32, ptr %12, align 4
  %57 = add nsw i32 %56, 1
  store i32 %57, ptr %12, align 4
  br label %41, !llvm.loop !10

58:                                               ; preds = %41
  store i32 0, ptr %13, align 4
  br label %59

59:                                               ; preds = %89, %58
  %60 = load i32, ptr %13, align 4
  %61 = load i32, ptr %6, align 4
  %62 = icmp slt i32 %60, %61
  br i1 %62, label %63, label %92

63:                                               ; preds = %59
  store i32 0, ptr %14, align 4
  br label %64

64:                                               ; preds = %85, %63
  %65 = load i32, ptr %14, align 4
  %66 = load i32, ptr %7, align 4
  %67 = icmp slt i32 %65, %66
  br i1 %67, label %68, label %88

68:                                               ; preds = %64
  %69 = load i32, ptr %13, align 4
  %70 = load i32, ptr %14, align 4
  %71 = add nsw i32 %70, 1
  %72 = mul nsw i32 %69, %71
  %73 = sitofp i32 %72 to double
  %74 = load i32, ptr %6, align 4
  %75 = sitofp i32 %74 to double
  %76 = fdiv double %73, %75
  %77 = load ptr, ptr %8, align 8
  %78 = load i32, ptr %13, align 4
  %79 = sext i32 %78 to i64
  %80 = mul nsw i64 %79, %18
  %81 = getelementptr inbounds double, ptr %77, i64 %80
  %82 = load i32, ptr %14, align 4
  %83 = sext i32 %82 to i64
  %84 = getelementptr inbounds double, ptr %81, i64 %83
  store double %76, ptr %84, align 8
  br label %85

85:                                               ; preds = %68
  %86 = load i32, ptr %14, align 4
  %87 = add nsw i32 %86, 1
  store i32 %87, ptr %14, align 4
  br label %64, !llvm.loop !11

88:                                               ; preds = %64
  br label %89

89:                                               ; preds = %88
  %90 = load i32, ptr %13, align 4
  %91 = add nsw i32 %90, 1
  store i32 %91, ptr %13, align 4
  br label %59, !llvm.loop !12

92:                                               ; preds = %59
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @bicg(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5, ptr noundef %6) #0 {
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca ptr, align 8
  %14 = alloca ptr, align 8
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  store i32 %0, ptr %8, align 4
  store i32 %1, ptr %9, align 4
  store ptr %2, ptr %10, align 8
  store ptr %3, ptr %11, align 8
  store ptr %4, ptr %12, align 8
  store ptr %5, ptr %13, align 8
  store ptr %6, ptr %14, align 8
  %18 = load i32, ptr %8, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %9, align 4
  %21 = zext i32 %20 to i64
  %22 = load i32, ptr %9, align 4
  %23 = zext i32 %22 to i64
  %24 = load i32, ptr %8, align 4
  %25 = zext i32 %24 to i64
  %26 = load i32, ptr %9, align 4
  %27 = zext i32 %26 to i64
  %28 = load i32, ptr %8, align 4
  %29 = zext i32 %28 to i64
  store i32 0, ptr %15, align 4
  br label %30

30:                                               ; preds = %39, %7
  %31 = load i32, ptr %15, align 4
  %32 = load i32, ptr %9, align 4
  %33 = icmp slt i32 %31, %32
  br i1 %33, label %34, label %42

34:                                               ; preds = %30
  %35 = load ptr, ptr %11, align 8
  %36 = load i32, ptr %15, align 4
  %37 = sext i32 %36 to i64
  %38 = getelementptr inbounds double, ptr %35, i64 %37
  store double 0.000000e+00, ptr %38, align 8
  br label %39

39:                                               ; preds = %34
  %40 = load i32, ptr %15, align 4
  %41 = add nsw i32 %40, 1
  store i32 %41, ptr %15, align 4
  br label %30, !llvm.loop !13

42:                                               ; preds = %30
  store i32 0, ptr %16, align 4
  br label %43

43:                                               ; preds = %101, %42
  %44 = load i32, ptr %16, align 4
  %45 = load i32, ptr %8, align 4
  %46 = icmp slt i32 %44, %45
  br i1 %46, label %47, label %104

47:                                               ; preds = %43
  %48 = load ptr, ptr %12, align 8
  %49 = load i32, ptr %16, align 4
  %50 = sext i32 %49 to i64
  %51 = getelementptr inbounds double, ptr %48, i64 %50
  store double 0.000000e+00, ptr %51, align 8
  store i32 0, ptr %17, align 4
  br label %52

52:                                               ; preds = %97, %47
  %53 = load i32, ptr %17, align 4
  %54 = load i32, ptr %9, align 4
  %55 = icmp slt i32 %53, %54
  br i1 %55, label %56, label %100

56:                                               ; preds = %52
  %57 = load ptr, ptr %14, align 8
  %58 = load i32, ptr %16, align 4
  %59 = sext i32 %58 to i64
  %60 = getelementptr inbounds double, ptr %57, i64 %59
  %61 = load double, ptr %60, align 8
  %62 = load ptr, ptr %10, align 8
  %63 = load i32, ptr %16, align 4
  %64 = sext i32 %63 to i64
  %65 = mul nsw i64 %64, %21
  %66 = getelementptr inbounds double, ptr %62, i64 %65
  %67 = load i32, ptr %17, align 4
  %68 = sext i32 %67 to i64
  %69 = getelementptr inbounds double, ptr %66, i64 %68
  %70 = load double, ptr %69, align 8
  %71 = load ptr, ptr %11, align 8
  %72 = load i32, ptr %17, align 4
  %73 = sext i32 %72 to i64
  %74 = getelementptr inbounds double, ptr %71, i64 %73
  %75 = load double, ptr %74, align 8
  %76 = call double @llvm.fmuladd.f64(double %61, double %70, double %75)
  store double %76, ptr %74, align 8
  %77 = load ptr, ptr %10, align 8
  %78 = load i32, ptr %16, align 4
  %79 = sext i32 %78 to i64
  %80 = mul nsw i64 %79, %21
  %81 = getelementptr inbounds double, ptr %77, i64 %80
  %82 = load i32, ptr %17, align 4
  %83 = sext i32 %82 to i64
  %84 = getelementptr inbounds double, ptr %81, i64 %83
  %85 = load double, ptr %84, align 8
  %86 = load ptr, ptr %13, align 8
  %87 = load i32, ptr %17, align 4
  %88 = sext i32 %87 to i64
  %89 = getelementptr inbounds double, ptr %86, i64 %88
  %90 = load double, ptr %89, align 8
  %91 = load ptr, ptr %12, align 8
  %92 = load i32, ptr %16, align 4
  %93 = sext i32 %92 to i64
  %94 = getelementptr inbounds double, ptr %91, i64 %93
  %95 = load double, ptr %94, align 8
  %96 = call double @llvm.fmuladd.f64(double %85, double %90, double %95)
  store double %96, ptr %94, align 8
  br label %97

97:                                               ; preds = %56
  %98 = load i32, ptr %17, align 4
  %99 = add nsw i32 %98, 1
  store i32 %99, ptr %17, align 4
  br label %52, !llvm.loop !14

100:                                              ; preds = %52
  br label %101

101:                                              ; preds = %100
  %102 = load i32, ptr %16, align 4
  %103 = add nsw i32 %102, 1
  store i32 %103, ptr %16, align 4
  br label %43, !llvm.loop !15

104:                                              ; preds = %43
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
  %8 = alloca ptr, align 8
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 512, ptr %2, align 4
  store i32 512, ptr %3, align 4
  %11 = load i32, ptr %3, align 4
  %12 = zext i32 %11 to i64
  %13 = load i32, ptr %2, align 4
  %14 = zext i32 %13 to i64
  %15 = load i32, ptr %3, align 4
  %16 = zext i32 %15 to i64
  %17 = mul nuw i64 %14, %16
  %18 = mul nuw i64 8, %17
  %19 = call ptr @malloc(i64 noundef %18) #4
  store ptr %19, ptr %4, align 8
  %20 = load i32, ptr %3, align 4
  %21 = sext i32 %20 to i64
  %22 = mul i64 %21, 8
  %23 = call ptr @malloc(i64 noundef %22) #4
  store ptr %23, ptr %5, align 8
  %24 = load i32, ptr %2, align 4
  %25 = sext i32 %24 to i64
  %26 = mul i64 %25, 8
  %27 = call ptr @malloc(i64 noundef %26) #4
  store ptr %27, ptr %6, align 8
  %28 = load i32, ptr %3, align 4
  %29 = sext i32 %28 to i64
  %30 = mul i64 %29, 8
  %31 = call ptr @malloc(i64 noundef %30) #4
  store ptr %31, ptr %7, align 8
  %32 = load i32, ptr %2, align 4
  %33 = sext i32 %32 to i64
  %34 = mul i64 %33, 8
  %35 = call ptr @malloc(i64 noundef %34) #4
  store ptr %35, ptr %8, align 8
  %36 = load i32, ptr %2, align 4
  %37 = load i32, ptr %3, align 4
  %38 = load ptr, ptr %4, align 8
  %39 = load ptr, ptr %7, align 8
  %40 = load ptr, ptr %8, align 8
  call void @init_array(i32 noundef %36, i32 noundef %37, ptr noundef %38, ptr noundef %39, ptr noundef %40)
  %41 = call i32 @clock()
  store i32 %41, ptr %9, align 4
  %42 = load i32, ptr %2, align 4
  %43 = load i32, ptr %3, align 4
  %44 = load ptr, ptr %4, align 8
  %45 = load ptr, ptr %5, align 8
  %46 = load ptr, ptr %6, align 8
  %47 = load ptr, ptr %7, align 8
  %48 = load ptr, ptr %8, align 8
  call void @bicg(i32 noundef %42, i32 noundef %43, ptr noundef %44, ptr noundef %45, ptr noundef %46, ptr noundef %47, ptr noundef %48)
  %49 = call i32 @clock()
  store i32 %49, ptr %10, align 4
  %50 = load i32, ptr %10, align 4
  %51 = load i32, ptr %9, align 4
  %52 = sub nsw i32 %50, %51
  %53 = sitofp i32 %52 to double
  %54 = fdiv double %53, 1.000000e+03
  %55 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %54)
  %56 = load ptr, ptr %5, align 8
  %57 = getelementptr inbounds double, ptr %56, i64 0
  %58 = load double, ptr %57, align 8
  %59 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %58)
  %60 = load ptr, ptr %4, align 8
  call void @free(ptr noundef %60)
  %61 = load ptr, ptr %5, align 8
  call void @free(ptr noundef %61)
  %62 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %62)
  %63 = load ptr, ptr %7, align 8
  call void @free(ptr noundef %63)
  %64 = load ptr, ptr %8, align 8
  call void @free(ptr noundef %64)
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
!1 = !DIFile(filename: "benchmarks/bicg.c", directory: "C:/Users/ultim/compiler-opt")
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
