; ModuleID = 'scripts\bitcnts_linked.2aac2f15_combined.bc'
source_filename = "llvm-link"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%union.anon = type { i32 }
%struct.bfile = type { ptr, i8, i8, i8, i8 }

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
@bits = internal global [256 x i8] c"\00\01\01\02\01\02\02\03\01\02\02\03\02\03\03\04\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\04\05\05\06\05\06\06\07\05\06\06\07\06\07\07\08", align 16
@bits.13 = internal global [256 x i8] c"\00\01\01\02\01\02\02\03\01\02\02\03\02\03\03\04\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\01\02\02\03\02\03\03\04\02\03\03\04\03\04\04\05\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\02\03\03\04\03\04\04\05\03\04\04\05\04\05\05\06\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\03\04\04\05\04\05\05\06\04\05\05\06\05\06\06\07\04\05\05\06\05\06\06\07\05\06\06\07\06\07\07\08", align 16
@.str.14 = private unnamed_addr constant [3 x i8] c"01\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
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
  %22 = call i32 (ptr, ptr, ...) @__mingw_fprintf(ptr noundef %21, ptr noundef @.str.7) #7
  call void @exit(i32 noundef -1) #8
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
  br label %35, !llvm.loop !24

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
  br label %29, !llvm.loop !26

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

declare dllimport ptr @__acrt_iob_func(i32 noundef) #1

; Function Attrs: nounwind
declare dso_local i32 @__mingw_fprintf(ptr noundef, ptr noundef, ...) #2

; Function Attrs: noreturn nounwind
declare dso_local void @exit(i32 noundef) #3

declare dso_local i32 @atoi(ptr noundef) #1

declare dso_local i32 @puts(ptr noundef) #1

declare dso_local i32 @clock() #1

declare dso_local i32 @rand() #1

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind optnone uwtable
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
  br label %5, !llvm.loop !27

24:                                               ; preds = %12
  %25 = load i32, ptr %4, align 4
  ret i32 %25
}

; Function Attrs: noinline nounwind uwtable
define dso_local ptr @alloc_bit_array(i64 noundef %0) #4 {
  %2 = alloca i64, align 8
  %3 = alloca ptr, align 8
  store i64 %0, ptr %2, align 8
  %4 = load i64, ptr %2, align 8
  %5 = add i64 %4, 8
  %6 = sub i64 %5, 1
  %7 = udiv i64 %6, 8
  %8 = call ptr @calloc(i64 noundef %7, i64 noundef 1) #9
  store ptr %8, ptr %3, align 8
  %9 = load ptr, ptr %3, align 8
  ret ptr %9
}

; Function Attrs: allocsize(0,1)
declare dso_local ptr @calloc(i64 noundef, i64 noundef) #5

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @getbit(ptr noundef %0, i32 noundef %1) #4 {
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  store i32 %1, ptr %4, align 4
  %5 = load i32, ptr %4, align 4
  %6 = sdiv i32 %5, 8
  %7 = load ptr, ptr %3, align 8
  %8 = sext i32 %6 to i64
  %9 = getelementptr inbounds i8, ptr %7, i64 %8
  store ptr %9, ptr %3, align 8
  %10 = load ptr, ptr %3, align 8
  %11 = load i8, ptr %10, align 1
  %12 = sext i8 %11 to i32
  %13 = load i32, ptr %4, align 4
  %14 = srem i32 %13, 8
  %15 = shl i32 1, %14
  %16 = and i32 %12, %15
  %17 = icmp ne i32 %16, 0
  %18 = zext i1 %17 to i32
  ret i32 %18
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @setbit(ptr noundef %0, i32 noundef %1, i32 noundef %2) #4 {
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store i32 %2, ptr %6, align 4
  %7 = load i32, ptr %5, align 4
  %8 = sdiv i32 %7, 8
  %9 = load ptr, ptr %4, align 8
  %10 = sext i32 %8 to i64
  %11 = getelementptr inbounds i8, ptr %9, i64 %10
  store ptr %11, ptr %4, align 8
  %12 = load i32, ptr %6, align 4
  %13 = icmp ne i32 %12, 0
  br i1 %13, label %14, label %23

14:                                               ; preds = %3
  %15 = load i32, ptr %5, align 4
  %16 = srem i32 %15, 8
  %17 = shl i32 1, %16
  %18 = load ptr, ptr %4, align 8
  %19 = load i8, ptr %18, align 1
  %20 = sext i8 %19 to i32
  %21 = or i32 %20, %17
  %22 = trunc i32 %21 to i8
  store i8 %22, ptr %18, align 1
  br label %33

23:                                               ; preds = %3
  %24 = load i32, ptr %5, align 4
  %25 = srem i32 %24, 8
  %26 = shl i32 1, %25
  %27 = xor i32 %26, -1
  %28 = load ptr, ptr %4, align 8
  %29 = load i8, ptr %28, align 1
  %30 = sext i8 %29 to i32
  %31 = and i32 %30, %27
  %32 = trunc i32 %31 to i8
  store i8 %32, ptr %28, align 1
  br label %33

33:                                               ; preds = %23, %14
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @flipbit(ptr noundef %0, i32 noundef %1) #4 {
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  store i32 %1, ptr %4, align 4
  %5 = load i32, ptr %4, align 4
  %6 = sdiv i32 %5, 8
  %7 = load ptr, ptr %3, align 8
  %8 = sext i32 %6 to i64
  %9 = getelementptr inbounds i8, ptr %7, i64 %8
  store ptr %9, ptr %3, align 8
  %10 = load i32, ptr %4, align 4
  %11 = srem i32 %10, 8
  %12 = shl i32 1, %11
  %13 = load ptr, ptr %3, align 8
  %14 = load i8, ptr %13, align 1
  %15 = sext i8 %14 to i32
  %16 = xor i32 %15, %12
  %17 = trunc i32 %16 to i8
  store i8 %17, ptr %13, align 1
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @bit_count(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  store i32 0, ptr %3, align 4
  %4 = load i32, ptr %2, align 4
  %5 = icmp ne i32 %4, 0
  br i1 %5, label %6, label %17

6:                                                ; preds = %1
  br label %7

7:                                                ; preds = %10, %6
  %8 = load i32, ptr %3, align 4
  %9 = add nsw i32 %8, 1
  store i32 %9, ptr %3, align 4
  br label %10

10:                                               ; preds = %7
  %11 = load i32, ptr %2, align 4
  %12 = load i32, ptr %2, align 4
  %13 = sub nsw i32 %12, 1
  %14 = and i32 %11, %13
  store i32 %14, ptr %2, align 4
  %15 = icmp ne i32 0, %14
  br i1 %15, label %7, label %16, !llvm.loop !28

16:                                               ; preds = %10
  br label %17

17:                                               ; preds = %16, %1
  %18 = load i32, ptr %3, align 4
  ret i32 %18
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @bitcount(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = and i32 %3, -1431655766
  %5 = lshr i32 %4, 1
  %6 = load i32, ptr %2, align 4
  %7 = and i32 %6, 1431655765
  %8 = add i32 %5, %7
  store i32 %8, ptr %2, align 4
  %9 = load i32, ptr %2, align 4
  %10 = and i32 %9, -858993460
  %11 = lshr i32 %10, 2
  %12 = load i32, ptr %2, align 4
  %13 = and i32 %12, 858993459
  %14 = add i32 %11, %13
  store i32 %14, ptr %2, align 4
  %15 = load i32, ptr %2, align 4
  %16 = and i32 %15, -252645136
  %17 = lshr i32 %16, 4
  %18 = load i32, ptr %2, align 4
  %19 = and i32 %18, 252645135
  %20 = add i32 %17, %19
  store i32 %20, ptr %2, align 4
  %21 = load i32, ptr %2, align 4
  %22 = and i32 %21, -16711936
  %23 = lshr i32 %22, 8
  %24 = load i32, ptr %2, align 4
  %25 = and i32 %24, 16711935
  %26 = add i32 %23, %25
  store i32 %26, ptr %2, align 4
  %27 = load i32, ptr %2, align 4
  %28 = and i32 %27, -65536
  %29 = lshr i32 %28, 16
  %30 = load i32, ptr %2, align 4
  %31 = and i32 %30, 65535
  %32 = add i32 %29, %31
  store i32 %32, ptr %2, align 4
  %33 = load i32, ptr %2, align 4
  ret i32 %33
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @ntbl_bitcount(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = and i32 %3, 15
  %5 = sext i32 %4 to i64
  %6 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %5
  %7 = load i8, ptr %6, align 1
  %8 = sext i8 %7 to i32
  %9 = load i32, ptr %2, align 4
  %10 = and i32 %9, 240
  %11 = lshr i32 %10, 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %12
  %14 = load i8, ptr %13, align 1
  %15 = sext i8 %14 to i32
  %16 = add nsw i32 %8, %15
  %17 = load i32, ptr %2, align 4
  %18 = and i32 %17, 3840
  %19 = lshr i32 %18, 8
  %20 = sext i32 %19 to i64
  %21 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %20
  %22 = load i8, ptr %21, align 1
  %23 = sext i8 %22 to i32
  %24 = add nsw i32 %16, %23
  %25 = load i32, ptr %2, align 4
  %26 = and i32 %25, 61440
  %27 = lshr i32 %26, 12
  %28 = sext i32 %27 to i64
  %29 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %28
  %30 = load i8, ptr %29, align 1
  %31 = sext i8 %30 to i32
  %32 = add nsw i32 %24, %31
  %33 = load i32, ptr %2, align 4
  %34 = and i32 %33, 983040
  %35 = lshr i32 %34, 16
  %36 = sext i32 %35 to i64
  %37 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %36
  %38 = load i8, ptr %37, align 1
  %39 = sext i8 %38 to i32
  %40 = add nsw i32 %32, %39
  %41 = load i32, ptr %2, align 4
  %42 = and i32 %41, 15728640
  %43 = lshr i32 %42, 20
  %44 = sext i32 %43 to i64
  %45 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %44
  %46 = load i8, ptr %45, align 1
  %47 = sext i8 %46 to i32
  %48 = add nsw i32 %40, %47
  %49 = load i32, ptr %2, align 4
  %50 = and i32 %49, 251658240
  %51 = lshr i32 %50, 24
  %52 = sext i32 %51 to i64
  %53 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %52
  %54 = load i8, ptr %53, align 1
  %55 = sext i8 %54 to i32
  %56 = add nsw i32 %48, %55
  %57 = load i32, ptr %2, align 4
  %58 = and i32 %57, -268435456
  %59 = lshr i32 %58, 28
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds [256 x i8], ptr @bits, i64 0, i64 %60
  %62 = load i8, ptr %61, align 1
  %63 = sext i8 %62 to i32
  %64 = add nsw i32 %56, %63
  ret i32 %64
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @BW_btbl_bitcount(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  %3 = alloca %union.anon, align 4
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  store i32 %4, ptr %3, align 4
  %5 = getelementptr inbounds [4 x i8], ptr %3, i64 0, i64 0
  %6 = load i8, ptr %5, align 4
  %7 = zext i8 %6 to i64
  %8 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %7
  %9 = load i8, ptr %8, align 1
  %10 = sext i8 %9 to i32
  %11 = getelementptr inbounds [4 x i8], ptr %3, i64 0, i64 1
  %12 = load i8, ptr %11, align 1
  %13 = zext i8 %12 to i64
  %14 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %13
  %15 = load i8, ptr %14, align 1
  %16 = sext i8 %15 to i32
  %17 = add nsw i32 %10, %16
  %18 = getelementptr inbounds [4 x i8], ptr %3, i64 0, i64 3
  %19 = load i8, ptr %18, align 1
  %20 = zext i8 %19 to i64
  %21 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %20
  %22 = load i8, ptr %21, align 1
  %23 = sext i8 %22 to i32
  %24 = add nsw i32 %17, %23
  %25 = getelementptr inbounds [4 x i8], ptr %3, i64 0, i64 2
  %26 = load i8, ptr %25, align 2
  %27 = zext i8 %26 to i64
  %28 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %27
  %29 = load i8, ptr %28, align 1
  %30 = sext i8 %29 to i32
  %31 = add nsw i32 %24, %30
  ret i32 %31
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @AR_btbl_bitcount(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  store ptr %2, ptr %3, align 8
  %5 = load ptr, ptr %3, align 8
  %6 = getelementptr inbounds nuw i8, ptr %5, i32 1
  store ptr %6, ptr %3, align 8
  %7 = load i8, ptr %5, align 1
  %8 = zext i8 %7 to i64
  %9 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %8
  %10 = load i8, ptr %9, align 1
  %11 = sext i8 %10 to i32
  store i32 %11, ptr %4, align 4
  %12 = load ptr, ptr %3, align 8
  %13 = getelementptr inbounds nuw i8, ptr %12, i32 1
  store ptr %13, ptr %3, align 8
  %14 = load i8, ptr %12, align 1
  %15 = zext i8 %14 to i64
  %16 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %15
  %17 = load i8, ptr %16, align 1
  %18 = sext i8 %17 to i32
  %19 = load i32, ptr %4, align 4
  %20 = add nsw i32 %19, %18
  store i32 %20, ptr %4, align 4
  %21 = load ptr, ptr %3, align 8
  %22 = getelementptr inbounds nuw i8, ptr %21, i32 1
  store ptr %22, ptr %3, align 8
  %23 = load i8, ptr %21, align 1
  %24 = zext i8 %23 to i64
  %25 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %24
  %26 = load i8, ptr %25, align 1
  %27 = sext i8 %26 to i32
  %28 = load i32, ptr %4, align 4
  %29 = add nsw i32 %28, %27
  store i32 %29, ptr %4, align 4
  %30 = load ptr, ptr %3, align 8
  %31 = load i8, ptr %30, align 1
  %32 = zext i8 %31 to i64
  %33 = getelementptr inbounds nuw [256 x i8], ptr @bits, i64 0, i64 %32
  %34 = load i8, ptr %33, align 1
  %35 = sext i8 %34 to i32
  %36 = load i32, ptr %4, align 4
  %37 = add nsw i32 %36, %35
  store i32 %37, ptr %4, align 4
  %38 = load i32, ptr %4, align 4
  ret i32 %38
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @ntbl_bitcnt(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = and i32 %4, 15
  %6 = sext i32 %5 to i64
  %7 = getelementptr inbounds [256 x i8], ptr @bits.13, i64 0, i64 %6
  %8 = load i8, ptr %7, align 1
  %9 = sext i8 %8 to i32
  store i32 %9, ptr %3, align 4
  %10 = load i32, ptr %2, align 4
  %11 = ashr i32 %10, 4
  store i32 %11, ptr %2, align 4
  %12 = icmp ne i32 0, %11
  br i1 %12, label %13, label %18

13:                                               ; preds = %1
  %14 = load i32, ptr %2, align 4
  %15 = call i32 @ntbl_bitcnt(i32 noundef %14)
  %16 = load i32, ptr %3, align 4
  %17 = add nsw i32 %16, %15
  store i32 %17, ptr %3, align 4
  br label %18

18:                                               ; preds = %13, %1
  %19 = load i32, ptr %3, align 4
  ret i32 %19
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @btbl_bitcnt(i32 noundef %0) #4 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %4 = getelementptr inbounds i8, ptr %2, i64 0
  %5 = load i8, ptr %4, align 4
  %6 = sext i8 %5 to i32
  %7 = and i32 %6, 255
  %8 = sext i32 %7 to i64
  %9 = getelementptr inbounds [256 x i8], ptr @bits.13, i64 0, i64 %8
  %10 = load i8, ptr %9, align 1
  %11 = sext i8 %10 to i32
  store i32 %11, ptr %3, align 4
  %12 = load i32, ptr %2, align 4
  %13 = ashr i32 %12, 8
  store i32 %13, ptr %2, align 4
  %14 = icmp ne i32 0, %13
  br i1 %14, label %15, label %20

15:                                               ; preds = %1
  %16 = load i32, ptr %2, align 4
  %17 = call i32 @btbl_bitcnt(i32 noundef %16)
  %18 = load i32, ptr %3, align 4
  %19 = add nsw i32 %18, %17
  store i32 %19, ptr %3, align 4
  br label %20

20:                                               ; preds = %15, %1
  %21 = load i32, ptr %3, align 4
  ret i32 %21
}

; Function Attrs: noinline nounwind uwtable
define dso_local ptr @bfopen(ptr noundef %0, ptr noundef %1) #4 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  store ptr %0, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  %7 = call ptr @malloc(i64 noundef 16) #10
  store ptr %7, ptr %6, align 8
  %8 = load ptr, ptr %6, align 8
  %9 = icmp eq ptr null, %8
  br i1 %9, label %10, label %11

10:                                               ; preds = %2
  store ptr null, ptr %3, align 8
  br label %29

11:                                               ; preds = %2
  %12 = load ptr, ptr %4, align 8
  %13 = load ptr, ptr %5, align 8
  %14 = call ptr @fopen(ptr noundef %12, ptr noundef %13)
  %15 = load ptr, ptr %6, align 8
  %16 = getelementptr inbounds nuw %struct.bfile, ptr %15, i32 0, i32 0
  store ptr %14, ptr %16, align 8
  %17 = load ptr, ptr %6, align 8
  %18 = getelementptr inbounds nuw %struct.bfile, ptr %17, i32 0, i32 0
  %19 = load ptr, ptr %18, align 8
  %20 = icmp eq ptr null, %19
  br i1 %20, label %21, label %23

21:                                               ; preds = %11
  %22 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %22)
  store ptr null, ptr %3, align 8
  br label %29

23:                                               ; preds = %11
  %24 = load ptr, ptr %6, align 8
  %25 = getelementptr inbounds nuw %struct.bfile, ptr %24, i32 0, i32 2
  store i8 0, ptr %25, align 1
  %26 = load ptr, ptr %6, align 8
  %27 = getelementptr inbounds nuw %struct.bfile, ptr %26, i32 0, i32 4
  store i8 0, ptr %27, align 1
  %28 = load ptr, ptr %6, align 8
  store ptr %28, ptr %3, align 8
  br label %29

29:                                               ; preds = %23, %21, %10
  %30 = load ptr, ptr %3, align 8
  ret ptr %30
}

; Function Attrs: allocsize(0)
declare dso_local ptr @malloc(i64 noundef) #6

declare dso_local ptr @fopen(ptr noundef, ptr noundef) #1

declare dso_local void @free(ptr noundef) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @bfread(ptr noundef %0) #4 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  %4 = getelementptr inbounds nuw %struct.bfile, ptr %3, i32 0, i32 2
  %5 = load i8, ptr %4, align 1
  %6 = sext i8 %5 to i32
  %7 = icmp eq i32 0, %6
  br i1 %7, label %8, label %18

8:                                                ; preds = %1
  %9 = load ptr, ptr %2, align 8
  %10 = getelementptr inbounds nuw %struct.bfile, ptr %9, i32 0, i32 0
  %11 = load ptr, ptr %10, align 8
  %12 = call i32 @fgetc(ptr noundef %11)
  %13 = trunc i32 %12 to i8
  %14 = load ptr, ptr %2, align 8
  %15 = getelementptr inbounds nuw %struct.bfile, ptr %14, i32 0, i32 1
  store i8 %13, ptr %15, align 8
  %16 = load ptr, ptr %2, align 8
  %17 = getelementptr inbounds nuw %struct.bfile, ptr %16, i32 0, i32 2
  store i8 8, ptr %17, align 1
  br label %18

18:                                               ; preds = %8, %1
  %19 = load ptr, ptr %2, align 8
  %20 = getelementptr inbounds nuw %struct.bfile, ptr %19, i32 0, i32 2
  %21 = load i8, ptr %20, align 1
  %22 = add i8 %21, -1
  store i8 %22, ptr %20, align 1
  %23 = load ptr, ptr %2, align 8
  %24 = getelementptr inbounds nuw %struct.bfile, ptr %23, i32 0, i32 1
  %25 = load i8, ptr %24, align 8
  %26 = sext i8 %25 to i32
  %27 = load ptr, ptr %2, align 8
  %28 = getelementptr inbounds nuw %struct.bfile, ptr %27, i32 0, i32 2
  %29 = load i8, ptr %28, align 1
  %30 = sext i8 %29 to i32
  %31 = shl i32 1, %30
  %32 = and i32 %26, %31
  %33 = icmp ne i32 %32, 0
  %34 = zext i1 %33 to i32
  ret i32 %34
}

declare dso_local i32 @fgetc(ptr noundef) #1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bfwrite(i32 noundef %0, ptr noundef %1) #4 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store i32 %0, ptr %3, align 4
  store ptr %1, ptr %4, align 8
  %5 = load ptr, ptr %4, align 8
  %6 = getelementptr inbounds nuw %struct.bfile, ptr %5, i32 0, i32 4
  %7 = load i8, ptr %6, align 1
  %8 = sext i8 %7 to i32
  %9 = icmp eq i32 8, %8
  br i1 %9, label %10, label %21

10:                                               ; preds = %2
  %11 = load ptr, ptr %4, align 8
  %12 = getelementptr inbounds nuw %struct.bfile, ptr %11, i32 0, i32 3
  %13 = load i8, ptr %12, align 2
  %14 = sext i8 %13 to i32
  %15 = load ptr, ptr %4, align 8
  %16 = getelementptr inbounds nuw %struct.bfile, ptr %15, i32 0, i32 0
  %17 = load ptr, ptr %16, align 8
  %18 = call i32 @fputc(i32 noundef %14, ptr noundef %17)
  %19 = load ptr, ptr %4, align 8
  %20 = getelementptr inbounds nuw %struct.bfile, ptr %19, i32 0, i32 4
  store i8 0, ptr %20, align 1
  br label %21

21:                                               ; preds = %10, %2
  %22 = load ptr, ptr %4, align 8
  %23 = getelementptr inbounds nuw %struct.bfile, ptr %22, i32 0, i32 4
  %24 = load i8, ptr %23, align 1
  %25 = add i8 %24, 1
  store i8 %25, ptr %23, align 1
  %26 = load ptr, ptr %4, align 8
  %27 = getelementptr inbounds nuw %struct.bfile, ptr %26, i32 0, i32 3
  %28 = load i8, ptr %27, align 2
  %29 = sext i8 %28 to i32
  %30 = shl i32 %29, 1
  %31 = trunc i32 %30 to i8
  store i8 %31, ptr %27, align 2
  %32 = load i32, ptr %3, align 4
  %33 = and i32 %32, 1
  %34 = load ptr, ptr %4, align 8
  %35 = getelementptr inbounds nuw %struct.bfile, ptr %34, i32 0, i32 3
  %36 = load i8, ptr %35, align 2
  %37 = sext i8 %36 to i32
  %38 = or i32 %37, %33
  %39 = trunc i32 %38 to i8
  store i8 %39, ptr %35, align 2
  ret void
}

declare dso_local i32 @fputc(i32 noundef, ptr noundef) #1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bfclose(ptr noundef %0) #4 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  %4 = getelementptr inbounds nuw %struct.bfile, ptr %3, i32 0, i32 0
  %5 = load ptr, ptr %4, align 8
  %6 = call i32 @fclose(ptr noundef %5)
  %7 = load ptr, ptr %2, align 8
  call void @free(ptr noundef %7)
  ret void
}

declare dso_local i32 @fclose(ptr noundef) #1

; Function Attrs: noinline nounwind uwtable
define dso_local void @bitstring(ptr noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3) #4 {
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  store ptr %0, ptr %5, align 8
  store i32 %1, ptr %6, align 4
  store i32 %2, ptr %7, align 4
  store i32 %3, ptr %8, align 4
  %11 = load i32, ptr %8, align 4
  %12 = load i32, ptr %7, align 4
  %13 = load i32, ptr %7, align 4
  %14 = ashr i32 %13, 2
  %15 = add nsw i32 %12, %14
  %16 = load i32, ptr %7, align 4
  %17 = srem i32 %16, 4
  %18 = icmp ne i32 %17, 0
  %19 = zext i1 %18 to i64
  %20 = select i1 %18, i32 0, i32 1
  %21 = sub nsw i32 %15, %20
  %22 = sub nsw i32 %11, %21
  store i32 %22, ptr %10, align 4
  store i32 0, ptr %9, align 4
  br label %23

23:                                               ; preds = %30, %4
  %24 = load i32, ptr %9, align 4
  %25 = load i32, ptr %10, align 4
  %26 = icmp slt i32 %24, %25
  br i1 %26, label %27, label %33

27:                                               ; preds = %23
  %28 = load ptr, ptr %5, align 8
  %29 = getelementptr inbounds nuw i8, ptr %28, i32 1
  store ptr %29, ptr %5, align 8
  store i8 32, ptr %28, align 1
  br label %30

30:                                               ; preds = %27
  %31 = load i32, ptr %9, align 4
  %32 = add nsw i32 %31, 1
  store i32 %32, ptr %9, align 4
  br label %23, !llvm.loop !29

33:                                               ; preds = %23
  br label %34

34:                                               ; preds = %56, %33
  %35 = load i32, ptr %7, align 4
  %36 = add nsw i32 %35, -1
  store i32 %36, ptr %7, align 4
  %37 = icmp sge i32 %36, 0
  br i1 %37, label %38, label %57

38:                                               ; preds = %34
  %39 = load i32, ptr %6, align 4
  %40 = load i32, ptr %7, align 4
  %41 = ashr i32 %39, %40
  %42 = and i32 %41, 1
  %43 = add nsw i32 %42, 48
  %44 = trunc i32 %43 to i8
  %45 = load ptr, ptr %5, align 8
  %46 = getelementptr inbounds nuw i8, ptr %45, i32 1
  store ptr %46, ptr %5, align 8
  store i8 %44, ptr %45, align 1
  %47 = load i32, ptr %7, align 4
  %48 = srem i32 %47, 4
  %49 = icmp ne i32 %48, 0
  br i1 %49, label %56, label %50

50:                                               ; preds = %38
  %51 = load i32, ptr %7, align 4
  %52 = icmp ne i32 %51, 0
  br i1 %52, label %53, label %56

53:                                               ; preds = %50
  %54 = load ptr, ptr %5, align 8
  %55 = getelementptr inbounds nuw i8, ptr %54, i32 1
  store ptr %55, ptr %5, align 8
  store i8 32, ptr %54, align 1
  br label %56

56:                                               ; preds = %53, %50, %38
  br label %34, !llvm.loop !30

57:                                               ; preds = %34
  %58 = load ptr, ptr %5, align 8
  store i8 0, ptr %58, align 1
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @bstr_i(ptr noundef %0) #4 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  store i32 0, ptr %4, align 4
  br label %5

5:                                                ; preds = %21, %1
  %6 = load ptr, ptr %2, align 8
  %7 = icmp ne ptr %6, null
  br i1 %7, label %8, label %19

8:                                                ; preds = %5
  %9 = load ptr, ptr %2, align 8
  %10 = load i8, ptr %9, align 1
  %11 = sext i8 %10 to i32
  %12 = icmp ne i32 %11, 0
  br i1 %12, label %13, label %19

13:                                               ; preds = %8
  %14 = load ptr, ptr %2, align 8
  %15 = load i8, ptr %14, align 1
  %16 = sext i8 %15 to i32
  %17 = call ptr @strchr(ptr noundef @.str.14, i32 noundef %16) #7
  %18 = icmp ne ptr %17, null
  br label %19

19:                                               ; preds = %13, %8, %5
  %20 = phi i1 [ false, %8 ], [ false, %5 ], [ %18, %13 ]
  br i1 %20, label %21, label %33

21:                                               ; preds = %19
  %22 = load ptr, ptr %2, align 8
  %23 = getelementptr inbounds nuw i8, ptr %22, i32 1
  store ptr %23, ptr %2, align 8
  %24 = load i8, ptr %22, align 1
  %25 = sext i8 %24 to i32
  %26 = sub nsw i32 %25, 48
  store i32 %26, ptr %3, align 4
  %27 = load i32, ptr %4, align 4
  %28 = shl i32 %27, 1
  store i32 %28, ptr %4, align 4
  %29 = load i32, ptr %3, align 4
  %30 = and i32 %29, 1
  %31 = load i32, ptr %4, align 4
  %32 = or i32 %31, %30
  store i32 %32, ptr %4, align 4
  br label %5, !llvm.loop !31

33:                                               ; preds = %19
  %34 = load i32, ptr %4, align 4
  ret i32 %34
}

; Function Attrs: nounwind
declare dso_local ptr @strchr(ptr noundef, i32 noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { noreturn nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { allocsize(0,1) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { allocsize(0) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nounwind }
attributes #8 = { noreturn nounwind }
attributes #9 = { allocsize(0,1) }
attributes #10 = { allocsize(0) }

!llvm.dbg.cu = !{!0, !2, !4, !6, !8, !10, !12, !14, !16}
!llvm.ident = !{!18, !18, !18, !18, !18, !18, !18, !18, !18}
!llvm.module.flags = !{!19, !20, !21, !22, !23}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnts.c", directory: "C:/Users/ultim/compiler-opt")
!2 = distinct !DICompileUnit(language: DW_LANG_C11, file: !3, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!3 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitarray.c", directory: "C:/Users/ultim/compiler-opt")
!4 = distinct !DICompileUnit(language: DW_LANG_C11, file: !5, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!5 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnt_1.c", directory: "C:/Users/ultim/compiler-opt")
!6 = distinct !DICompileUnit(language: DW_LANG_C11, file: !7, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!7 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnt_2.c", directory: "C:/Users/ultim/compiler-opt")
!8 = distinct !DICompileUnit(language: DW_LANG_C11, file: !9, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!9 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnt_3.c", directory: "C:/Users/ultim/compiler-opt")
!10 = distinct !DICompileUnit(language: DW_LANG_C11, file: !11, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!11 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitcnt_4.c", directory: "C:/Users/ultim/compiler-opt")
!12 = distinct !DICompileUnit(language: DW_LANG_C11, file: !13, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!13 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitfiles.c", directory: "C:/Users/ultim/compiler-opt")
!14 = distinct !DICompileUnit(language: DW_LANG_C11, file: !15, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!15 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bitstrng.c", directory: "C:/Users/ultim/compiler-opt")
!16 = distinct !DICompileUnit(language: DW_LANG_C11, file: !17, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!17 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\bitcount/bstr_i.c", directory: "C:/Users/ultim/compiler-opt")
!18 = !{!"clang version 21.1.8"}
!19 = !{i32 2, !"Debug Info Version", i32 3}
!20 = !{i32 1, !"wchar_size", i32 2}
!21 = !{i32 8, !"PIC Level", i32 2}
!22 = !{i32 7, !"uwtable", i32 2}
!23 = !{i32 1, !"MaxTLSAlign", i32 65536}
!24 = distinct !{!24, !25}
!25 = !{!"llvm.loop.mustprogress"}
!26 = distinct !{!26, !25}
!27 = distinct !{!27, !25}
!28 = distinct !{!28, !25}
!29 = distinct !{!29, !25}
!30 = distinct !{!30, !25}
!31 = distinct !{!31, !25}
