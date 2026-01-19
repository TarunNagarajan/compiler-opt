; ModuleID = 'benchmarks\gramschmidt.c'
source_filename = "benchmarks\\gramschmidt.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [34 x i8] c"Gramschmidt Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  store ptr %2, ptr %6, align 8
  %9 = load i32, ptr %4, align 4
  %10 = zext i32 %9 to i64
  %11 = load i32, ptr %5, align 4
  %12 = zext i32 %11 to i64
  store i32 0, ptr %7, align 4
  br label %13

13:                                               ; preds = %43, %3
  %14 = load i32, ptr %7, align 4
  %15 = load i32, ptr %4, align 4
  %16 = icmp slt i32 %14, %15
  br i1 %16, label %17, label %46

17:                                               ; preds = %13
  store i32 0, ptr %8, align 4
  br label %18

18:                                               ; preds = %39, %17
  %19 = load i32, ptr %8, align 4
  %20 = load i32, ptr %5, align 4
  %21 = icmp slt i32 %19, %20
  br i1 %21, label %22, label %42

22:                                               ; preds = %18
  %23 = load i32, ptr %7, align 4
  %24 = sitofp i32 %23 to double
  %25 = load i32, ptr %8, align 4
  %26 = sitofp i32 %25 to double
  %27 = fmul double %24, %26
  %28 = load i32, ptr %4, align 4
  %29 = sitofp i32 %28 to double
  %30 = fdiv double %27, %29
  %31 = load ptr, ptr %6, align 8
  %32 = load i32, ptr %7, align 4
  %33 = sext i32 %32 to i64
  %34 = mul nsw i64 %33, %12
  %35 = getelementptr inbounds double, ptr %31, i64 %34
  %36 = load i32, ptr %8, align 4
  %37 = sext i32 %36 to i64
  %38 = getelementptr inbounds double, ptr %35, i64 %37
  store double %30, ptr %38, align 8
  br label %39

39:                                               ; preds = %22
  %40 = load i32, ptr %8, align 4
  %41 = add nsw i32 %40, 1
  store i32 %41, ptr %8, align 4
  br label %18, !llvm.loop !8

42:                                               ; preds = %18
  br label %43

43:                                               ; preds = %42
  %44 = load i32, ptr %7, align 4
  %45 = add nsw i32 %44, 1
  store i32 %45, ptr %7, align 4
  br label %13, !llvm.loop !10

46:                                               ; preds = %13
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @gramschmidt(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4) #0 {
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca i32, align 4
  %12 = alloca double, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  store i32 %0, ptr %6, align 4
  store i32 %1, ptr %7, align 4
  store ptr %2, ptr %8, align 8
  store ptr %3, ptr %9, align 8
  store ptr %4, ptr %10, align 8
  %18 = load i32, ptr %6, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %7, align 4
  %21 = zext i32 %20 to i64
  %22 = load i32, ptr %7, align 4
  %23 = zext i32 %22 to i64
  %24 = load i32, ptr %7, align 4
  %25 = zext i32 %24 to i64
  %26 = load i32, ptr %6, align 4
  %27 = zext i32 %26 to i64
  %28 = load i32, ptr %7, align 4
  %29 = zext i32 %28 to i64
  store i32 0, ptr %11, align 4
  br label %30

30:                                               ; preds = %212, %5
  %31 = load i32, ptr %11, align 4
  %32 = load i32, ptr %7, align 4
  %33 = icmp slt i32 %31, %32
  br i1 %33, label %34, label %215

34:                                               ; preds = %30
  store double 0.000000e+00, ptr %12, align 8
  store i32 0, ptr %13, align 4
  br label %35

35:                                               ; preds = %60, %34
  %36 = load i32, ptr %13, align 4
  %37 = load i32, ptr %6, align 4
  %38 = icmp slt i32 %36, %37
  br i1 %38, label %39, label %63

39:                                               ; preds = %35
  %40 = load ptr, ptr %8, align 8
  %41 = load i32, ptr %13, align 4
  %42 = sext i32 %41 to i64
  %43 = mul nsw i64 %42, %21
  %44 = getelementptr inbounds double, ptr %40, i64 %43
  %45 = load i32, ptr %11, align 4
  %46 = sext i32 %45 to i64
  %47 = getelementptr inbounds double, ptr %44, i64 %46
  %48 = load double, ptr %47, align 8
  %49 = load ptr, ptr %8, align 8
  %50 = load i32, ptr %13, align 4
  %51 = sext i32 %50 to i64
  %52 = mul nsw i64 %51, %21
  %53 = getelementptr inbounds double, ptr %49, i64 %52
  %54 = load i32, ptr %11, align 4
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds double, ptr %53, i64 %55
  %57 = load double, ptr %56, align 8
  %58 = load double, ptr %12, align 8
  %59 = call double @llvm.fmuladd.f64(double %48, double %57, double %58)
  store double %59, ptr %12, align 8
  br label %60

60:                                               ; preds = %39
  %61 = load i32, ptr %13, align 4
  %62 = add nsw i32 %61, 1
  store i32 %62, ptr %13, align 4
  br label %35, !llvm.loop !11

63:                                               ; preds = %35
  %64 = load double, ptr %12, align 8
  %65 = call double @sqrt(double noundef %64) #5
  %66 = load ptr, ptr %9, align 8
  %67 = load i32, ptr %11, align 4
  %68 = sext i32 %67 to i64
  %69 = mul nsw i64 %68, %25
  %70 = getelementptr inbounds double, ptr %66, i64 %69
  %71 = load i32, ptr %11, align 4
  %72 = sext i32 %71 to i64
  %73 = getelementptr inbounds double, ptr %70, i64 %72
  store double %65, ptr %73, align 8
  store i32 0, ptr %14, align 4
  br label %74

74:                                               ; preds = %106, %63
  %75 = load i32, ptr %14, align 4
  %76 = load i32, ptr %6, align 4
  %77 = icmp slt i32 %75, %76
  br i1 %77, label %78, label %109

78:                                               ; preds = %74
  %79 = load ptr, ptr %8, align 8
  %80 = load i32, ptr %14, align 4
  %81 = sext i32 %80 to i64
  %82 = mul nsw i64 %81, %21
  %83 = getelementptr inbounds double, ptr %79, i64 %82
  %84 = load i32, ptr %11, align 4
  %85 = sext i32 %84 to i64
  %86 = getelementptr inbounds double, ptr %83, i64 %85
  %87 = load double, ptr %86, align 8
  %88 = load ptr, ptr %9, align 8
  %89 = load i32, ptr %11, align 4
  %90 = sext i32 %89 to i64
  %91 = mul nsw i64 %90, %25
  %92 = getelementptr inbounds double, ptr %88, i64 %91
  %93 = load i32, ptr %11, align 4
  %94 = sext i32 %93 to i64
  %95 = getelementptr inbounds double, ptr %92, i64 %94
  %96 = load double, ptr %95, align 8
  %97 = fdiv double %87, %96
  %98 = load ptr, ptr %10, align 8
  %99 = load i32, ptr %14, align 4
  %100 = sext i32 %99 to i64
  %101 = mul nsw i64 %100, %29
  %102 = getelementptr inbounds double, ptr %98, i64 %101
  %103 = load i32, ptr %11, align 4
  %104 = sext i32 %103 to i64
  %105 = getelementptr inbounds double, ptr %102, i64 %104
  store double %97, ptr %105, align 8
  br label %106

106:                                              ; preds = %78
  %107 = load i32, ptr %14, align 4
  %108 = add nsw i32 %107, 1
  store i32 %108, ptr %14, align 4
  br label %74, !llvm.loop !12

109:                                              ; preds = %74
  %110 = load i32, ptr %11, align 4
  %111 = add nsw i32 %110, 1
  store i32 %111, ptr %15, align 4
  br label %112

112:                                              ; preds = %208, %109
  %113 = load i32, ptr %15, align 4
  %114 = load i32, ptr %7, align 4
  %115 = icmp slt i32 %113, %114
  br i1 %115, label %116, label %211

116:                                              ; preds = %112
  %117 = load ptr, ptr %9, align 8
  %118 = load i32, ptr %11, align 4
  %119 = sext i32 %118 to i64
  %120 = mul nsw i64 %119, %25
  %121 = getelementptr inbounds double, ptr %117, i64 %120
  %122 = load i32, ptr %15, align 4
  %123 = sext i32 %122 to i64
  %124 = getelementptr inbounds double, ptr %121, i64 %123
  store double 0.000000e+00, ptr %124, align 8
  store i32 0, ptr %16, align 4
  br label %125

125:                                              ; preds = %158, %116
  %126 = load i32, ptr %16, align 4
  %127 = load i32, ptr %6, align 4
  %128 = icmp slt i32 %126, %127
  br i1 %128, label %129, label %161

129:                                              ; preds = %125
  %130 = load ptr, ptr %10, align 8
  %131 = load i32, ptr %16, align 4
  %132 = sext i32 %131 to i64
  %133 = mul nsw i64 %132, %29
  %134 = getelementptr inbounds double, ptr %130, i64 %133
  %135 = load i32, ptr %11, align 4
  %136 = sext i32 %135 to i64
  %137 = getelementptr inbounds double, ptr %134, i64 %136
  %138 = load double, ptr %137, align 8
  %139 = load ptr, ptr %8, align 8
  %140 = load i32, ptr %16, align 4
  %141 = sext i32 %140 to i64
  %142 = mul nsw i64 %141, %21
  %143 = getelementptr inbounds double, ptr %139, i64 %142
  %144 = load i32, ptr %15, align 4
  %145 = sext i32 %144 to i64
  %146 = getelementptr inbounds double, ptr %143, i64 %145
  %147 = load double, ptr %146, align 8
  %148 = load ptr, ptr %9, align 8
  %149 = load i32, ptr %11, align 4
  %150 = sext i32 %149 to i64
  %151 = mul nsw i64 %150, %25
  %152 = getelementptr inbounds double, ptr %148, i64 %151
  %153 = load i32, ptr %15, align 4
  %154 = sext i32 %153 to i64
  %155 = getelementptr inbounds double, ptr %152, i64 %154
  %156 = load double, ptr %155, align 8
  %157 = call double @llvm.fmuladd.f64(double %138, double %147, double %156)
  store double %157, ptr %155, align 8
  br label %158

158:                                              ; preds = %129
  %159 = load i32, ptr %16, align 4
  %160 = add nsw i32 %159, 1
  store i32 %160, ptr %16, align 4
  br label %125, !llvm.loop !13

161:                                              ; preds = %125
  store i32 0, ptr %17, align 4
  br label %162

162:                                              ; preds = %204, %161
  %163 = load i32, ptr %17, align 4
  %164 = load i32, ptr %6, align 4
  %165 = icmp slt i32 %163, %164
  br i1 %165, label %166, label %207

166:                                              ; preds = %162
  %167 = load ptr, ptr %8, align 8
  %168 = load i32, ptr %17, align 4
  %169 = sext i32 %168 to i64
  %170 = mul nsw i64 %169, %21
  %171 = getelementptr inbounds double, ptr %167, i64 %170
  %172 = load i32, ptr %15, align 4
  %173 = sext i32 %172 to i64
  %174 = getelementptr inbounds double, ptr %171, i64 %173
  %175 = load double, ptr %174, align 8
  %176 = load ptr, ptr %10, align 8
  %177 = load i32, ptr %17, align 4
  %178 = sext i32 %177 to i64
  %179 = mul nsw i64 %178, %29
  %180 = getelementptr inbounds double, ptr %176, i64 %179
  %181 = load i32, ptr %11, align 4
  %182 = sext i32 %181 to i64
  %183 = getelementptr inbounds double, ptr %180, i64 %182
  %184 = load double, ptr %183, align 8
  %185 = load ptr, ptr %9, align 8
  %186 = load i32, ptr %11, align 4
  %187 = sext i32 %186 to i64
  %188 = mul nsw i64 %187, %25
  %189 = getelementptr inbounds double, ptr %185, i64 %188
  %190 = load i32, ptr %15, align 4
  %191 = sext i32 %190 to i64
  %192 = getelementptr inbounds double, ptr %189, i64 %191
  %193 = load double, ptr %192, align 8
  %194 = fneg double %184
  %195 = call double @llvm.fmuladd.f64(double %194, double %193, double %175)
  %196 = load ptr, ptr %8, align 8
  %197 = load i32, ptr %17, align 4
  %198 = sext i32 %197 to i64
  %199 = mul nsw i64 %198, %21
  %200 = getelementptr inbounds double, ptr %196, i64 %199
  %201 = load i32, ptr %15, align 4
  %202 = sext i32 %201 to i64
  %203 = getelementptr inbounds double, ptr %200, i64 %202
  store double %195, ptr %203, align 8
  br label %204

204:                                              ; preds = %166
  %205 = load i32, ptr %17, align 4
  %206 = add nsw i32 %205, 1
  store i32 %206, ptr %17, align 4
  br label %162, !llvm.loop !14

207:                                              ; preds = %162
  br label %208

208:                                              ; preds = %207
  %209 = load i32, ptr %15, align 4
  %210 = add nsw i32 %209, 1
  store i32 %210, ptr %15, align 4
  br label %112, !llvm.loop !15

211:                                              ; preds = %112
  br label %212

212:                                              ; preds = %211
  %213 = load i32, ptr %11, align 4
  %214 = add nsw i32 %213, 1
  store i32 %214, ptr %11, align 4
  br label %30, !llvm.loop !16

215:                                              ; preds = %30
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: nounwind
declare dso_local double @sqrt(double noundef) #2

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 256, ptr %2, align 4
  store i32 256, ptr %3, align 4
  %9 = load i32, ptr %3, align 4
  %10 = zext i32 %9 to i64
  %11 = load i32, ptr %2, align 4
  %12 = zext i32 %11 to i64
  %13 = load i32, ptr %3, align 4
  %14 = zext i32 %13 to i64
  %15 = mul nuw i64 %12, %14
  %16 = mul nuw i64 8, %15
  %17 = call ptr @malloc(i64 noundef %16) #6
  store ptr %17, ptr %4, align 8
  %18 = load i32, ptr %3, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %3, align 4
  %21 = zext i32 %20 to i64
  %22 = load i32, ptr %3, align 4
  %23 = zext i32 %22 to i64
  %24 = mul nuw i64 %21, %23
  %25 = mul nuw i64 8, %24
  %26 = call ptr @malloc(i64 noundef %25) #6
  store ptr %26, ptr %5, align 8
  %27 = load i32, ptr %3, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %2, align 4
  %30 = zext i32 %29 to i64
  %31 = load i32, ptr %3, align 4
  %32 = zext i32 %31 to i64
  %33 = mul nuw i64 %30, %32
  %34 = mul nuw i64 8, %33
  %35 = call ptr @malloc(i64 noundef %34) #6
  store ptr %35, ptr %6, align 8
  %36 = load i32, ptr %2, align 4
  %37 = load i32, ptr %3, align 4
  %38 = load ptr, ptr %4, align 8
  call void @init_array(i32 noundef %36, i32 noundef %37, ptr noundef %38)
  %39 = call i32 @clock()
  store i32 %39, ptr %7, align 4
  %40 = load i32, ptr %2, align 4
  %41 = load i32, ptr %3, align 4
  %42 = load ptr, ptr %4, align 8
  %43 = load ptr, ptr %5, align 8
  %44 = load ptr, ptr %6, align 8
  call void @gramschmidt(i32 noundef %40, i32 noundef %41, ptr noundef %42, ptr noundef %43, ptr noundef %44)
  %45 = call i32 @clock()
  store i32 %45, ptr %8, align 4
  %46 = load i32, ptr %8, align 4
  %47 = load i32, ptr %7, align 4
  %48 = sub nsw i32 %46, %47
  %49 = sitofp i32 %48 to double
  %50 = fdiv double %49, 1.000000e+03
  %51 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %50)
  %52 = load ptr, ptr %5, align 8
  %53 = mul nsw i64 0, %19
  %54 = getelementptr inbounds double, ptr %52, i64 %53
  %55 = getelementptr inbounds double, ptr %54, i64 0
  %56 = load double, ptr %55, align 8
  %57 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %56)
  %58 = load ptr, ptr %4, align 8
  call void @free(ptr noundef %58)
  %59 = load ptr, ptr %5, align 8
  call void @free(ptr noundef %59)
  %60 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %60)
  ret i32 0
}

; Function Attrs: allocsize(0)
declare dso_local ptr @malloc(i64 noundef) #3

declare dso_local i32 @clock() #4

declare dso_local i32 @__mingw_printf(ptr noundef, ...) #4

declare dso_local void @free(ptr noundef) #4

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { allocsize(0) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { nounwind }
attributes #6 = { allocsize(0) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/gramschmidt.c", directory: "C:/Users/ultim/compiler-opt")
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
!16 = distinct !{!16, !9}
