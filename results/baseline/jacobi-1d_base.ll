; ModuleID = 'benchmarks\jacobi-1d.c'
source_filename = "benchmarks\\jacobi-1d.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [32 x i8] c"Jacobi-1D Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef %1, ptr noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  %8 = load i32, ptr %4, align 4
  %9 = zext i32 %8 to i64
  %10 = load i32, ptr %4, align 4
  %11 = zext i32 %10 to i64
  store i32 0, ptr %7, align 4
  br label %12

12:                                               ; preds = %37, %3
  %13 = load i32, ptr %7, align 4
  %14 = load i32, ptr %4, align 4
  %15 = icmp slt i32 %13, %14
  br i1 %15, label %16, label %40

16:                                               ; preds = %12
  %17 = load i32, ptr %7, align 4
  %18 = sitofp i32 %17 to double
  %19 = fadd double %18, 2.000000e+00
  %20 = load i32, ptr %4, align 4
  %21 = sitofp i32 %20 to double
  %22 = fdiv double %19, %21
  %23 = load ptr, ptr %5, align 8
  %24 = load i32, ptr %7, align 4
  %25 = sext i32 %24 to i64
  %26 = getelementptr inbounds double, ptr %23, i64 %25
  store double %22, ptr %26, align 8
  %27 = load i32, ptr %7, align 4
  %28 = sitofp i32 %27 to double
  %29 = fadd double %28, 3.000000e+00
  %30 = load i32, ptr %4, align 4
  %31 = sitofp i32 %30 to double
  %32 = fdiv double %29, %31
  %33 = load ptr, ptr %6, align 8
  %34 = load i32, ptr %7, align 4
  %35 = sext i32 %34 to i64
  %36 = getelementptr inbounds double, ptr %33, i64 %35
  store double %32, ptr %36, align 8
  br label %37

37:                                               ; preds = %16
  %38 = load i32, ptr %7, align 4
  %39 = add nsw i32 %38, 1
  store i32 %39, ptr %7, align 4
  br label %12, !llvm.loop !8

40:                                               ; preds = %12
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @jacobi_1d(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3) #0 {
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
  %12 = load i32, ptr %6, align 4
  %13 = zext i32 %12 to i64
  %14 = load i32, ptr %6, align 4
  %15 = zext i32 %14 to i64
  store i32 0, ptr %9, align 4
  br label %16

16:                                               ; preds = %89, %4
  %17 = load i32, ptr %9, align 4
  %18 = load i32, ptr %5, align 4
  %19 = icmp slt i32 %17, %18
  br i1 %19, label %20, label %92

20:                                               ; preds = %16
  store i32 1, ptr %10, align 4
  br label %21

21:                                               ; preds = %51, %20
  %22 = load i32, ptr %10, align 4
  %23 = load i32, ptr %6, align 4
  %24 = sub nsw i32 %23, 1
  %25 = icmp slt i32 %22, %24
  br i1 %25, label %26, label %54

26:                                               ; preds = %21
  %27 = load ptr, ptr %7, align 8
  %28 = load i32, ptr %10, align 4
  %29 = sub nsw i32 %28, 1
  %30 = sext i32 %29 to i64
  %31 = getelementptr inbounds double, ptr %27, i64 %30
  %32 = load double, ptr %31, align 8
  %33 = load ptr, ptr %7, align 8
  %34 = load i32, ptr %10, align 4
  %35 = sext i32 %34 to i64
  %36 = getelementptr inbounds double, ptr %33, i64 %35
  %37 = load double, ptr %36, align 8
  %38 = fadd double %32, %37
  %39 = load ptr, ptr %7, align 8
  %40 = load i32, ptr %10, align 4
  %41 = add nsw i32 %40, 1
  %42 = sext i32 %41 to i64
  %43 = getelementptr inbounds double, ptr %39, i64 %42
  %44 = load double, ptr %43, align 8
  %45 = fadd double %38, %44
  %46 = fmul double 3.333300e-01, %45
  %47 = load ptr, ptr %8, align 8
  %48 = load i32, ptr %10, align 4
  %49 = sext i32 %48 to i64
  %50 = getelementptr inbounds double, ptr %47, i64 %49
  store double %46, ptr %50, align 8
  br label %51

51:                                               ; preds = %26
  %52 = load i32, ptr %10, align 4
  %53 = add nsw i32 %52, 1
  store i32 %53, ptr %10, align 4
  br label %21, !llvm.loop !10

54:                                               ; preds = %21
  store i32 1, ptr %11, align 4
  br label %55

55:                                               ; preds = %85, %54
  %56 = load i32, ptr %11, align 4
  %57 = load i32, ptr %6, align 4
  %58 = sub nsw i32 %57, 1
  %59 = icmp slt i32 %56, %58
  br i1 %59, label %60, label %88

60:                                               ; preds = %55
  %61 = load ptr, ptr %8, align 8
  %62 = load i32, ptr %11, align 4
  %63 = sub nsw i32 %62, 1
  %64 = sext i32 %63 to i64
  %65 = getelementptr inbounds double, ptr %61, i64 %64
  %66 = load double, ptr %65, align 8
  %67 = load ptr, ptr %8, align 8
  %68 = load i32, ptr %11, align 4
  %69 = sext i32 %68 to i64
  %70 = getelementptr inbounds double, ptr %67, i64 %69
  %71 = load double, ptr %70, align 8
  %72 = fadd double %66, %71
  %73 = load ptr, ptr %8, align 8
  %74 = load i32, ptr %11, align 4
  %75 = add nsw i32 %74, 1
  %76 = sext i32 %75 to i64
  %77 = getelementptr inbounds double, ptr %73, i64 %76
  %78 = load double, ptr %77, align 8
  %79 = fadd double %72, %78
  %80 = fmul double 3.333300e-01, %79
  %81 = load ptr, ptr %7, align 8
  %82 = load i32, ptr %11, align 4
  %83 = sext i32 %82 to i64
  %84 = getelementptr inbounds double, ptr %81, i64 %83
  store double %80, ptr %84, align 8
  br label %85

85:                                               ; preds = %60
  %86 = load i32, ptr %11, align 4
  %87 = add nsw i32 %86, 1
  store i32 %87, ptr %11, align 4
  br label %55, !llvm.loop !11

88:                                               ; preds = %55
  br label %89

89:                                               ; preds = %88
  %90 = load i32, ptr %9, align 4
  %91 = add nsw i32 %90, 1
  store i32 %91, ptr %9, align 4
  br label %16, !llvm.loop !12

92:                                               ; preds = %16
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store i32 2000, ptr %6, align 4
  store i32 100, ptr %7, align 4
  %12 = load i32, ptr %6, align 4
  %13 = sext i32 %12 to i64
  %14 = mul i64 %13, 8
  %15 = call ptr @malloc(i64 noundef %14) #3
  store ptr %15, ptr %8, align 8
  %16 = load i32, ptr %6, align 4
  %17 = sext i32 %16 to i64
  %18 = mul i64 %17, 8
  %19 = call ptr @malloc(i64 noundef %18) #3
  store ptr %19, ptr %9, align 8
  %20 = load i32, ptr %6, align 4
  %21 = load ptr, ptr %8, align 8
  %22 = load ptr, ptr %9, align 8
  call void @init_array(i32 noundef %20, ptr noundef %21, ptr noundef %22)
  %23 = call i32 @clock()
  store i32 %23, ptr %10, align 4
  %24 = load i32, ptr %7, align 4
  %25 = load i32, ptr %6, align 4
  %26 = load ptr, ptr %8, align 8
  %27 = load ptr, ptr %9, align 8
  call void @jacobi_1d(i32 noundef %24, i32 noundef %25, ptr noundef %26, ptr noundef %27)
  %28 = call i32 @clock()
  store i32 %28, ptr %11, align 4
  %29 = load i32, ptr %11, align 4
  %30 = load i32, ptr %10, align 4
  %31 = sub nsw i32 %29, %30
  %32 = sitofp i32 %31 to double
  %33 = fdiv double %32, 1.000000e+03
  %34 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %33)
  %35 = load ptr, ptr %8, align 8
  %36 = getelementptr inbounds double, ptr %35, i64 0
  %37 = load double, ptr %36, align 8
  %38 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %37)
  %39 = load ptr, ptr %8, align 8
  call void @free(ptr noundef %39)
  %40 = load ptr, ptr %9, align 8
  call void @free(ptr noundef %40)
  ret i32 0
}

; Function Attrs: allocsize(0)
declare dso_local ptr @malloc(i64 noundef) #1

declare dso_local i32 @clock() #2

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #2

declare dso_local void @free(ptr noundef) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { allocsize(0) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { allocsize(0) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/jacobi-1d.c", directory: "C:/Users/ultim/compiler-opt")
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
