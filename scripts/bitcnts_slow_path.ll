; ModuleID = 'benchmarks\mibench\mibench-master\automotive\bitcount\bitcnts.c'
source_filename = "benchmarks\\mibench\\mibench-master\\automotive\\bitcount\\bitcnts.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@main.pBitCntFunc = internal global [7 x ptr] [ptr @bit_count, ptr @bitcount, ptr @ntbl_bitcnt, ptr @ntbl_bitcount, ptr @BW_btbl_bitcount, ptr @AR_btbl_bitcount, ptr @bit_shifter], align 16
@main.text = internal global [7 x ptr] [ptr @.str, ptr @.str.1, ptr @.str.2, ptr @.str.3, ptr @.str.4, ptr @.str.5, ptr @.str.6], align 16
@.str = private unnamed_addr constant [29 x i8] c"Optimized 1 bit/loop counter\00", align 1
@.str.1 = private unnamed_addr constant [26 x i8] c"Ratko's mystery algorithm\00", align 1
@.str.2 = private unnamed_addr constant [31 x i8] c"Recursive bit count by nybbles\00", align 1
@.str.3 = private unnamed_addr constant [35 x i8] c"Non-recursive bit count by nybbles\00", align 1
@.str.4 = private unnamed_addr constant [38 x i8] c"Non-recursive bit count by bytes (BW)\00", align 1
@.str.5 = private unnamed_addr constant [38 x i8] c"Non-recursive bit count by bytes (AR)\00", align 1
@.str.6 = private unnamed_addr constant [21 x i8] c"Shift and count bits\00", align 1
@.str.7 = private unnamed_addr constant [29 x i8] c"Usage: bitcnts <iterations>\0A\00", align 1
@.str.8 = private unnamed_addr constant [33 x i8] c"Bit counter algorithm benchmark\0A\00", align 1
@.str.9 = private unnamed_addr constant [36 x i8] c"%-38s> Time: %7.3f sec.; Bits: %ld\0A\00", align 1
@.str.10 = private unnamed_addr constant [13 x i8] c"\0ABest  > %s\0A\00", align 1
@.str.11 = private unnamed_addr constant [12 x i8] c"Worst > %s\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store double 0x7FEFFFFFFFFFFFFF, ptr %9, align 8
  store double 0.000000e+00, ptr %10, align 8
  %18 = load i32, ptr %4, align 4
  %19 = icmp slt i32 %18, 2
  br i1 %19, label %20, label %23

20:                                               ; preds = %2
  %21 = call ptr @__acrt_iob_func(i32 noundef 2)
  %22 = call i32 (ptr, ptr, ...) @__mingw_fprintf(ptr noundef %21, ptr noundef @.str.7) #4
  call void @exit(i32 noundef -1) #5
  unreachable

23:                                               ; preds = %2
  %24 = load ptr, ptr %5, align 8
  %25 = getelementptr inbounds ptr, ptr %24, i64 1
  %26 = load ptr, ptr %25, align 8
  %27 = call i32 @atoi(ptr noundef %26)
  store i32 %27, ptr %17, align 4
  %28 = call i32 @puts(ptr noundef @.str.8)
  store i32 0, ptr %11, align 4
  br label %29

29:                                               ; preds = %81, %23
  %30 = load i32, ptr %11, align 4
  %31 = icmp slt i32 %30, 7
  br i1 %31, label %32, label %84

32:                                               ; preds = %29
  %33 = call i32 @clock()
  store i32 %33, ptr %6, align 4
  store i32 0, ptr %15, align 4
  store i32 0, ptr %14, align 4
  %34 = call i32 @rand()
  store i32 %34, ptr %16, align 4
  br label %35

35:                                               ; preds = %48, %32
  %36 = load i32, ptr %14, align 4
  %37 = load i32, ptr %17, align 4
  %38 = icmp slt i32 %36, %37
  br i1 %38, label %39, label %53

39:                                               ; preds = %35
  %40 = load i32, ptr %11, align 4
  %41 = sext i32 %40 to i64
  %42 = getelementptr inbounds [7 x ptr], ptr @main.pBitCntFunc, i64 0, i64 %41
  %43 = load ptr, ptr %42, align 8
  %44 = load i32, ptr %16, align 4
  %45 = call i32 %43(i32 noundef %44)
  %46 = load i32, ptr %15, align 4
  %47 = add nsw i32 %46, %45
  store i32 %47, ptr %15, align 4
  br label %48

48:                                               ; preds = %39
  %49 = load i32, ptr %14, align 4
  %50 = add nsw i32 %49, 1
  store i32 %50, ptr %14, align 4
  %51 = load i32, ptr %16, align 4
  %52 = add nsw i32 %51, 13
  store i32 %52, ptr %16, align 4
  br label %35, !llvm.loop !8

53:                                               ; preds = %35
  %54 = call i32 @clock()
  store i32 %54, ptr %7, align 4
  %55 = load i32, ptr %7, align 4
  %56 = load i32, ptr %6, align 4
  %57 = sub nsw i32 %55, %56
  %58 = sitofp i32 %57 to double
  %59 = fdiv double %58, 1.000000e+03
  store double %59, ptr %8, align 8
  %60 = load double, ptr %8, align 8
  %61 = load double, ptr %9, align 8
  %62 = fcmp olt double %60, %61
  br i1 %62, label %63, label %66

63:                                               ; preds = %53
  %64 = load double, ptr %8, align 8
  store double %64, ptr %9, align 8
  %65 = load i32, ptr %11, align 4
  store i32 %65, ptr %12, align 4
  br label %66

66:                                               ; preds = %63, %53
  %67 = load double, ptr %8, align 8
  %68 = load double, ptr %10, align 8
  %69 = fcmp ogt double %67, %68
  br i1 %69, label %70, label %73

70:                                               ; preds = %66
  %71 = load double, ptr %8, align 8
  store double %71, ptr %10, align 8
  %72 = load i32, ptr %11, align 4
  store i32 %72, ptr %13, align 4
  br label %73

73:                                               ; preds = %70, %66
  %74 = load i32, ptr %11, align 4
  %75 = sext i32 %74 to i64
  %76 = getelementptr inbounds [7 x ptr], ptr @main.text, i64 0, i64 %75
  %77 = load ptr, ptr %76, align 8
  %78 = load double, ptr %8, align 8
  %79 = load i32, ptr %15, align 4
  %80 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.9, ptr noundef %77, double noundef %78, i32 noundef %79)
  br label %81

81:                                               ; preds = %73
  %82 = load i32, ptr %11, align 4
  %83 = add nsw i32 %82, 1
  store i32 %83, ptr %11, align 4
  br label %29, !llvm.loop !10

84:                                               ; preds = %29
  %85 = load i32, ptr %12, align 4
  %86 = sext i32 %85 to i64
  %87 = getelementptr inbounds [7 x ptr], ptr @main.text, i64 0, i64 %86
  %88 = load ptr, ptr %87, align 8
  %89 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.10, ptr noundef %88)
  %90 = load i32, ptr %13, align 4
  %91 = sext i32 %90 to i64
  %92 = getelementptr inbounds [7 x ptr], ptr @main.text, i64 0, i64 %91
  %93 = load ptr, ptr %92, align 8
  %94 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.11, ptr noundef %93)
  ret i32 0
}

declare dso_local i32 @bit_count(i32 noundef) #1

declare dso_local i32 @bitcount(i32 noundef) #1

declare dso_local i32 @ntbl_bitcnt(i32 noundef) #1

declare dso_local i32 @ntbl_bitcount(i32 noundef) #1

declare dso_local i32 @BW_btbl_bitcount(i32 noundef) #1

declare dso_local i32 @AR_btbl_bitcount(i32 noundef) #1

; Function Attrs: noinline nounwind uwtable
define internal i32 @bit_shifter(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  store i32 0, ptr %4, align 4
  store i32 0, ptr %3, align 4
  br label %5

5:                                                ; preds = %19, %1
  %6 = load i32, ptr %2, align 4
  %7 = icmp ne i32 %6, 0
  br i1 %7, label %8, label %12

8:                                                ; preds = %5
  %9 = load i32, ptr %3, align 4
  %10 = sext i32 %9 to i64
  %11 = icmp ult i64 %10, 32
  br label %12

12:                                               ; preds = %8, %5
  %13 = phi i1 [ false, %5 ], [ %11, %8 ]
  br i1 %13, label %14, label %24

14:                                               ; preds = %12
  %15 = load i32, ptr %2, align 4
  %16 = and i32 %15, 1
  %17 = load i32, ptr %4, align 4
  %18 = add nsw i32 %17, %16
  store i32 %18, ptr %4, align 4
  br label %19

19:                                               ; preds = %14
  %20 = load i32, ptr %3, align 4
  %21 = add nsw i32 %20, 1
  store i32 %21, ptr %3, align 4
  %22 = load i32, ptr %2, align 4
  %23 = ashr i32 %22, 1
  store i32 %23, ptr %2, align 4
  br label %5, !llvm.loop !11

24:                                               ; preds = %12
  %25 = load i32, ptr %4, align 4
  ret i32 %25
}

; Function Attrs: nounwind
declare dso_local i32 @__mingw_fprintf(ptr noundef, ptr noundef, ...) #2

declare dllimport ptr @__acrt_iob_func(i32 noundef) #1

; Function Attrs: noreturn nounwind
declare dso_local void @exit(i32 noundef) #3

declare dso_local i32 @atoi(ptr noundef) #1

declare dso_local i32 @puts(ptr noundef) #1

declare dso_local i32 @clock() #1

declare dso_local i32 @rand() #1

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #1

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { noreturn nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nounwind }
attributes #5 = { noreturn nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnts.c", directory: "C:/Users/ultim/compiler-opt")
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
