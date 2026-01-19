; ModuleID = 'data/test_programs/simple_test.ll'
source_filename = "data/test_programs/simple_test.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [25 x i8] c"Sum of squares 1-10: %d\0A\00", align 1
@__const.main.a = private unnamed_addr constant [3 x [3 x i32]] [[3 x i32] [i32 1, i32 2, i32 3], [3 x i32] [i32 4, i32 5, i32 6], [3 x i32] [i32 7, i32 8, i32 9]], align 16
@__const.main.b = private unnamed_addr constant [3 x [3 x i32]] [[3 x i32] [i32 9, i32 8, i32 7], [3 x i32] [i32 6, i32 5, i32 4], [3 x i32] [i32 3, i32 2, i32 1]], align 16
@.str.1 = private unnamed_addr constant [20 x i8] c"Matrix C[0][0]: %d\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @square(i32 noundef %0) #0 {
  %2 = mul nsw i32 %0, %0
  ret i32 %2
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @sum_of_squares(i32 noundef %0) #0 {
  br label %2

2:                                                ; preds = %7, %1
  %.01 = phi i32 [ 0, %1 ], [ %6, %7 ]
  %.0 = phi i32 [ 1, %1 ], [ %8, %7 ]
  %3 = icmp sle i32 %.0, %0
  br i1 %3, label %4, label %9

4:                                                ; preds = %2
  %5 = call i32 @square(i32 noundef %.0)
  %6 = add nsw i32 %.01, %5
  br label %7

7:                                                ; preds = %4
  %8 = add nsw i32 %.0, 1
  br label %2, !llvm.loop !8

9:                                                ; preds = %2
  ret i32 %.01
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @matrix_multiply(ptr noundef %0, ptr noundef %1, ptr noundef %2) #0 {
  br label %4

4:                                                ; preds = %40, %3
  %.02 = phi i32 [ 0, %3 ], [ %41, %40 ]
  %5 = icmp slt i32 %.02, 3
  br i1 %5, label %6, label %42

6:                                                ; preds = %4
  br label %7

7:                                                ; preds = %37, %6
  %.01 = phi i32 [ 0, %6 ], [ %38, %37 ]
  %8 = icmp slt i32 %.01, 3
  br i1 %8, label %9, label %39

9:                                                ; preds = %7
  %10 = sext i32 %.02 to i64
  %11 = getelementptr inbounds [3 x i32], ptr %2, i64 %10
  %12 = sext i32 %.01 to i64
  %13 = getelementptr inbounds [3 x i32], ptr %11, i64 0, i64 %12
  store i32 0, ptr %13, align 4
  br label %14

14:                                               ; preds = %34, %9
  %.0 = phi i32 [ 0, %9 ], [ %35, %34 ]
  %15 = icmp slt i32 %.0, 3
  br i1 %15, label %16, label %36

16:                                               ; preds = %14
  %17 = sext i32 %.02 to i64
  %18 = getelementptr inbounds [3 x i32], ptr %0, i64 %17
  %19 = sext i32 %.0 to i64
  %20 = getelementptr inbounds [3 x i32], ptr %18, i64 0, i64 %19
  %21 = load i32, ptr %20, align 4
  %22 = sext i32 %.0 to i64
  %23 = getelementptr inbounds [3 x i32], ptr %1, i64 %22
  %24 = sext i32 %.01 to i64
  %25 = getelementptr inbounds [3 x i32], ptr %23, i64 0, i64 %24
  %26 = load i32, ptr %25, align 4
  %27 = mul nsw i32 %21, %26
  %28 = sext i32 %.02 to i64
  %29 = getelementptr inbounds [3 x i32], ptr %2, i64 %28
  %30 = sext i32 %.01 to i64
  %31 = getelementptr inbounds [3 x i32], ptr %29, i64 0, i64 %30
  %32 = load i32, ptr %31, align 4
  %33 = add nsw i32 %32, %27
  store i32 %33, ptr %31, align 4
  br label %34

34:                                               ; preds = %16
  %35 = add nsw i32 %.0, 1
  br label %14, !llvm.loop !10

36:                                               ; preds = %14
  br label %37

37:                                               ; preds = %36
  %38 = add nsw i32 %.01, 1
  br label %7, !llvm.loop !11

39:                                               ; preds = %7
  br label %40

40:                                               ; preds = %39
  %41 = add nsw i32 %.02, 1
  br label %4, !llvm.loop !12

42:                                               ; preds = %4
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca [3 x [3 x i32]], align 16
  %2 = alloca [3 x [3 x i32]], align 16
  %3 = alloca [3 x [3 x i32]], align 16
  %4 = call i32 @sum_of_squares(i32 noundef 10)
  %5 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, i32 noundef %4)
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %1, ptr align 16 @__const.main.a, i64 36, i1 false)
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.b, i64 36, i1 false)
  %6 = getelementptr inbounds [3 x [3 x i32]], ptr %1, i64 0, i64 0
  %7 = getelementptr inbounds [3 x [3 x i32]], ptr %2, i64 0, i64 0
  %8 = getelementptr inbounds [3 x [3 x i32]], ptr %3, i64 0, i64 0
  call void @matrix_multiply(ptr noundef %6, ptr noundef %7, ptr noundef %8)
  %9 = getelementptr inbounds [3 x [3 x i32]], ptr %3, i64 0, i64 0
  %10 = getelementptr inbounds [3 x i32], ptr %9, i64 0, i64 0
  %11 = load i32, ptr %10, align 16
  %12 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, i32 noundef %11)
  ret i32 0
}

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #1

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nocallback nofree nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "data/test_programs/simple_test.c", directory: "C:/Users/ultim/compiler-opt")
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
