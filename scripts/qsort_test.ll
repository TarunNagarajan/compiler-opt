; ModuleID = 'c:\Users\ultim\compiler-opt\benchmarks\mibench\mibench-master\automotive\qsort\qsort_small.c'
source_filename = "c:\\Users\\ultim\\compiler-opt\\benchmarks\\mibench\\mibench-master\\automotive\\qsort\\qsort_small.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.myStringStruct = type { [128 x i8] }

@.str = private unnamed_addr constant [27 x i8] c"Usage: qsort_small <file>\0A\00", align 1
@.str.1 = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.3 = private unnamed_addr constant [24 x i8] c"\0ASorting %d elements.\0A\0A\00", align 1
@.str.4 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @compare(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  store ptr %1, ptr %4, align 8
  %6 = load ptr, ptr %3, align 8
  %7 = getelementptr inbounds nuw %struct.myStringStruct, ptr %6, i32 0, i32 0
  %8 = getelementptr inbounds [128 x i8], ptr %7, i64 0, i64 0
  %9 = load ptr, ptr %4, align 8
  %10 = getelementptr inbounds nuw %struct.myStringStruct, ptr %9, i32 0, i32 0
  %11 = getelementptr inbounds [128 x i8], ptr %10, i64 0, i64 0
  %12 = call i32 @strcmp(ptr noundef %8, ptr noundef %11) #4
  store i32 %12, ptr %5, align 4
  %13 = load i32, ptr %5, align 4
  %14 = icmp slt i32 %13, 0
  br i1 %14, label %15, label %16

15:                                               ; preds = %2
  br label %21

16:                                               ; preds = %2
  %17 = load i32, ptr %5, align 4
  %18 = icmp eq i32 %17, 0
  %19 = zext i1 %18 to i64
  %20 = select i1 %18, i32 0, i32 -1
  br label %21

21:                                               ; preds = %16, %15
  %22 = phi i32 [ 1, %15 ], [ %20, %16 ]
  ret i32 %22
}

; Function Attrs: nounwind
declare dso_local i32 @strcmp(ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca [60000 x %struct.myStringStruct], align 16
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store i32 0, ptr %9, align 4
  %10 = load i32, ptr %4, align 4
  %11 = icmp slt i32 %10, 2
  br i1 %11, label %12, label %15

12:                                               ; preds = %2
  %13 = call ptr @__acrt_iob_func(i32 noundef 2)
  %14 = call i32 (ptr, ptr, ...) @__mingw_fprintf(ptr noundef %13, ptr noundef @.str) #4
  call void @exit(i32 noundef -1) #5
  unreachable

15:                                               ; preds = %2
  %16 = load ptr, ptr %5, align 8
  %17 = getelementptr inbounds ptr, ptr %16, i64 1
  %18 = load ptr, ptr %17, align 8
  %19 = call ptr @fopen(ptr noundef %18, ptr noundef @.str.1)
  store ptr %19, ptr %7, align 8
  br label %20

20:                                               ; preds = %33, %15
  %21 = load ptr, ptr %7, align 8
  %22 = load i32, ptr %9, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds [60000 x %struct.myStringStruct], ptr %6, i64 0, i64 %23
  %25 = getelementptr inbounds nuw %struct.myStringStruct, ptr %24, i32 0, i32 0
  %26 = call i32 (ptr, ptr, ...) @__mingw_fscanf(ptr noundef %21, ptr noundef @.str.2, ptr noundef %25)
  %27 = icmp eq i32 %26, 1
  br i1 %27, label %28, label %31

28:                                               ; preds = %20
  %29 = load i32, ptr %9, align 4
  %30 = icmp slt i32 %29, 60000
  br label %31

31:                                               ; preds = %28, %20
  %32 = phi i1 [ false, %20 ], [ %30, %28 ]
  br i1 %32, label %33, label %36

33:                                               ; preds = %31
  %34 = load i32, ptr %9, align 4
  %35 = add nsw i32 %34, 1
  store i32 %35, ptr %9, align 4
  br label %20, !llvm.loop !8

36:                                               ; preds = %31
  br label %37

37:                                               ; preds = %36
  %38 = load i32, ptr %9, align 4
  %39 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.3, i32 noundef %38)
  %40 = getelementptr inbounds [60000 x %struct.myStringStruct], ptr %6, i64 0, i64 0
  %41 = load i32, ptr %9, align 4
  %42 = sext i32 %41 to i64
  call void @qsort(ptr noundef %40, i64 noundef %42, i64 noundef 128, ptr noundef @compare)
  store i32 0, ptr %8, align 4
  br label %43

43:                                               ; preds = %54, %37
  %44 = load i32, ptr %8, align 4
  %45 = load i32, ptr %9, align 4
  %46 = icmp slt i32 %44, %45
  br i1 %46, label %47, label %57

47:                                               ; preds = %43
  %48 = load i32, ptr %8, align 4
  %49 = sext i32 %48 to i64
  %50 = getelementptr inbounds [60000 x %struct.myStringStruct], ptr %6, i64 0, i64 %49
  %51 = getelementptr inbounds nuw %struct.myStringStruct, ptr %50, i32 0, i32 0
  %52 = getelementptr inbounds [128 x i8], ptr %51, i64 0, i64 0
  %53 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.4, ptr noundef %52)
  br label %54

54:                                               ; preds = %47
  %55 = load i32, ptr %8, align 4
  %56 = add nsw i32 %55, 1
  store i32 %56, ptr %8, align 4
  br label %43, !llvm.loop !10

57:                                               ; preds = %43
  ret i32 0
}

; Function Attrs: nounwind
declare dso_local i32 @__mingw_fprintf(ptr noundef, ptr noundef, ...) #1

declare dllimport ptr @__acrt_iob_func(i32 noundef) #2

; Function Attrs: noreturn nounwind
declare dso_local void @exit(i32 noundef) #3

declare dso_local ptr @fopen(ptr noundef, ptr noundef) #2

declare dso_local i32 @__mingw_fscanf(ptr noundef, ptr noundef, ...) #2

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #2

declare dso_local void @qsort(ptr noundef, i64 noundef, i64 noundef, ptr noundef) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { noreturn nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nounwind }
attributes #5 = { noreturn nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "c:\\Users\\ultim\\compiler-opt\\benchmarks\\mibench\\mibench-master\\automotive\\qsort/qsort_small.c", directory: "C:/Users/ultim/compiler-opt")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 21.1.8"}
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !9}
