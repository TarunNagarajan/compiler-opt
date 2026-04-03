; ModuleID = 'scripts\basicmath_linked.c0f67a36_combined.bc'
source_filename = "llvm-link"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.int_sqrt = type { i32, i32 }

@.str = private unnamed_addr constant [39 x i8] c"********* CUBIC FUNCTIONS ***********\0A\00", align 1
@.str.1 = private unnamed_addr constant [11 x i8] c"Solutions:\00", align 1
@.str.2 = private unnamed_addr constant [4 x i8] c" %f\00", align 1
@.str.3 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@.str.4 = private unnamed_addr constant [41 x i8] c"********* INTEGER SQR ROOTS ***********\0A\00", align 1
@.str.5 = private unnamed_addr constant [17 x i8] c"sqrt(%3d) = %2d\0A\00", align 1
@.str.6 = private unnamed_addr constant [17 x i8] c"\0Asqrt(%lX) = %X\0A\00", align 1
@.str.7 = private unnamed_addr constant [40 x i8] c"********* ANGLE CONVERSION ***********\0A\00", align 1
@.str.8 = private unnamed_addr constant [31 x i8] c"%3.0f degrees = %.12f radians\0A\00", align 1
@.str.9 = private unnamed_addr constant [1 x i8] zeroinitializer, align 1
@.str.10 = private unnamed_addr constant [31 x i8] c"%.12f radians = %3.0f degrees\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca double, align 8
  %3 = alloca double, align 8
  %4 = alloca double, align 8
  %5 = alloca double, align 8
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca double, align 8
  %12 = alloca double, align 8
  %13 = alloca double, align 8
  %14 = alloca double, align 8
  %15 = alloca double, align 8
  %16 = alloca double, align 8
  %17 = alloca double, align 8
  %18 = alloca [3 x double], align 16
  %19 = alloca double, align 8
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  %23 = alloca %struct.int_sqrt, align 4
  %24 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store double 1.000000e+00, ptr %2, align 8
  store double -1.050000e+01, ptr %3, align 8
  store double 3.200000e+01, ptr %4, align 8
  store double -3.000000e+01, ptr %5, align 8
  store double 1.000000e+00, ptr %6, align 8
  store double -4.500000e+00, ptr %7, align 8
  store double 1.700000e+01, ptr %8, align 8
  store double -3.000000e+01, ptr %9, align 8
  store double 1.000000e+00, ptr %10, align 8
  store double -3.500000e+00, ptr %11, align 8
  store double 2.200000e+01, ptr %12, align 8
  store double -3.100000e+01, ptr %13, align 8
  store double 1.000000e+00, ptr %14, align 8
  store double -1.370000e+01, ptr %15, align 8
  store double 1.000000e+00, ptr %16, align 8
  store double -3.500000e+01, ptr %17, align 8
  store i32 1072497001, ptr %22, align 4
  store i32 0, ptr %24, align 4
  %25 = call i32 (ptr, ...) @printf(ptr noundef @.str)
  %26 = load double, ptr %2, align 8
  %27 = load double, ptr %3, align 8
  %28 = load double, ptr %4, align 8
  %29 = load double, ptr %5, align 8
  %30 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 0
  call void @SolveCubic(double noundef %26, double noundef %27, double noundef %28, double noundef %29, ptr noundef %20, ptr noundef %30)
  %31 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  store i32 0, ptr %21, align 4
  br label %32

32:                                               ; preds = %42, %0
  %33 = load i32, ptr %21, align 4
  %34 = load i32, ptr %20, align 4
  %35 = icmp slt i32 %33, %34
  br i1 %35, label %36, label %45

36:                                               ; preds = %32
  %37 = load i32, ptr %21, align 4
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 %38
  %40 = load double, ptr %39, align 8
  %41 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, double noundef %40)
  br label %42

42:                                               ; preds = %36
  %43 = load i32, ptr %21, align 4
  %44 = add nsw i32 %43, 1
  store i32 %44, ptr %21, align 4
  br label %32, !llvm.loop !14

45:                                               ; preds = %32
  %46 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  %47 = load double, ptr %6, align 8
  %48 = load double, ptr %7, align 8
  %49 = load double, ptr %8, align 8
  %50 = load double, ptr %9, align 8
  %51 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 0
  call void @SolveCubic(double noundef %47, double noundef %48, double noundef %49, double noundef %50, ptr noundef %20, ptr noundef %51)
  %52 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  store i32 0, ptr %21, align 4
  br label %53

53:                                               ; preds = %63, %45
  %54 = load i32, ptr %21, align 4
  %55 = load i32, ptr %20, align 4
  %56 = icmp slt i32 %54, %55
  br i1 %56, label %57, label %66

57:                                               ; preds = %53
  %58 = load i32, ptr %21, align 4
  %59 = sext i32 %58 to i64
  %60 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 %59
  %61 = load double, ptr %60, align 8
  %62 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, double noundef %61)
  br label %63

63:                                               ; preds = %57
  %64 = load i32, ptr %21, align 4
  %65 = add nsw i32 %64, 1
  store i32 %65, ptr %21, align 4
  br label %53, !llvm.loop !16

66:                                               ; preds = %53
  %67 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  %68 = load double, ptr %10, align 8
  %69 = load double, ptr %11, align 8
  %70 = load double, ptr %12, align 8
  %71 = load double, ptr %13, align 8
  %72 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 0
  call void @SolveCubic(double noundef %68, double noundef %69, double noundef %70, double noundef %71, ptr noundef %20, ptr noundef %72)
  %73 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  store i32 0, ptr %21, align 4
  br label %74

74:                                               ; preds = %84, %66
  %75 = load i32, ptr %21, align 4
  %76 = load i32, ptr %20, align 4
  %77 = icmp slt i32 %75, %76
  br i1 %77, label %78, label %87

78:                                               ; preds = %74
  %79 = load i32, ptr %21, align 4
  %80 = sext i32 %79 to i64
  %81 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 %80
  %82 = load double, ptr %81, align 8
  %83 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, double noundef %82)
  br label %84

84:                                               ; preds = %78
  %85 = load i32, ptr %21, align 4
  %86 = add nsw i32 %85, 1
  store i32 %86, ptr %21, align 4
  br label %74, !llvm.loop !17

87:                                               ; preds = %74
  %88 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  %89 = load double, ptr %14, align 8
  %90 = load double, ptr %15, align 8
  %91 = load double, ptr %16, align 8
  %92 = load double, ptr %17, align 8
  %93 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 0
  call void @SolveCubic(double noundef %89, double noundef %90, double noundef %91, double noundef %92, ptr noundef %20, ptr noundef %93)
  %94 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  store i32 0, ptr %21, align 4
  br label %95

95:                                               ; preds = %105, %87
  %96 = load i32, ptr %21, align 4
  %97 = load i32, ptr %20, align 4
  %98 = icmp slt i32 %96, %97
  br i1 %98, label %99, label %108

99:                                               ; preds = %95
  %100 = load i32, ptr %21, align 4
  %101 = sext i32 %100 to i64
  %102 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 %101
  %103 = load double, ptr %102, align 8
  %104 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, double noundef %103)
  br label %105

105:                                              ; preds = %99
  %106 = load i32, ptr %21, align 4
  %107 = add nsw i32 %106, 1
  store i32 %107, ptr %21, align 4
  br label %95, !llvm.loop !18

108:                                              ; preds = %95
  %109 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  store double 1.000000e+00, ptr %2, align 8
  br label %110

110:                                              ; preds = %159, %108
  %111 = load double, ptr %2, align 8
  %112 = fcmp olt double %111, 1.000000e+01
  br i1 %112, label %113, label %162

113:                                              ; preds = %110
  store double 1.000000e+01, ptr %3, align 8
  br label %114

114:                                              ; preds = %155, %113
  %115 = load double, ptr %3, align 8
  %116 = fcmp ogt double %115, 0.000000e+00
  br i1 %116, label %117, label %158

117:                                              ; preds = %114
  store double 5.000000e+00, ptr %4, align 8
  br label %118

118:                                              ; preds = %151, %117
  %119 = load double, ptr %4, align 8
  %120 = fcmp olt double %119, 1.500000e+01
  br i1 %120, label %121, label %154

121:                                              ; preds = %118
  store double -1.000000e+00, ptr %5, align 8
  br label %122

122:                                              ; preds = %147, %121
  %123 = load double, ptr %5, align 8
  %124 = fcmp ogt double %123, -1.100000e+01
  br i1 %124, label %125, label %150

125:                                              ; preds = %122
  %126 = load double, ptr %2, align 8
  %127 = load double, ptr %3, align 8
  %128 = load double, ptr %4, align 8
  %129 = load double, ptr %5, align 8
  %130 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 0
  call void @SolveCubic(double noundef %126, double noundef %127, double noundef %128, double noundef %129, ptr noundef %20, ptr noundef %130)
  %131 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  store i32 0, ptr %21, align 4
  br label %132

132:                                              ; preds = %142, %125
  %133 = load i32, ptr %21, align 4
  %134 = load i32, ptr %20, align 4
  %135 = icmp slt i32 %133, %134
  br i1 %135, label %136, label %145

136:                                              ; preds = %132
  %137 = load i32, ptr %21, align 4
  %138 = sext i32 %137 to i64
  %139 = getelementptr inbounds [3 x double], ptr %18, i64 0, i64 %138
  %140 = load double, ptr %139, align 8
  %141 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, double noundef %140)
  br label %142

142:                                              ; preds = %136
  %143 = load i32, ptr %21, align 4
  %144 = add nsw i32 %143, 1
  store i32 %144, ptr %21, align 4
  br label %132, !llvm.loop !19

145:                                              ; preds = %132
  %146 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  br label %147

147:                                              ; preds = %145
  %148 = load double, ptr %5, align 8
  %149 = fadd double %148, -1.000000e+00
  store double %149, ptr %5, align 8
  br label %122, !llvm.loop !20

150:                                              ; preds = %122
  br label %151

151:                                              ; preds = %150
  %152 = load double, ptr %4, align 8
  %153 = fadd double %152, 5.000000e-01
  store double %153, ptr %4, align 8
  br label %118, !llvm.loop !21

154:                                              ; preds = %118
  br label %155

155:                                              ; preds = %154
  %156 = load double, ptr %3, align 8
  %157 = fadd double %156, -1.000000e+00
  store double %157, ptr %3, align 8
  br label %114, !llvm.loop !22

158:                                              ; preds = %114
  br label %159

159:                                              ; preds = %158
  %160 = load double, ptr %2, align 8
  %161 = fadd double %160, 1.000000e+00
  store double %161, ptr %2, align 8
  br label %110, !llvm.loop !23

162:                                              ; preds = %110
  %163 = call i32 (ptr, ...) @printf(ptr noundef @.str.4)
  store i32 0, ptr %21, align 4
  br label %164

164:                                              ; preds = %173, %162
  %165 = load i32, ptr %21, align 4
  %166 = icmp slt i32 %165, 1001
  br i1 %166, label %167, label %176

167:                                              ; preds = %164
  %168 = load i32, ptr %21, align 4
  call void @usqrt(i32 noundef %168, ptr noundef %23)
  %169 = load i32, ptr %21, align 4
  %170 = getelementptr inbounds nuw %struct.int_sqrt, ptr %23, i32 0, i32 0
  %171 = load i32, ptr %170, align 4
  %172 = call i32 (ptr, ...) @printf(ptr noundef @.str.5, i32 noundef %169, i32 noundef %171)
  br label %173

173:                                              ; preds = %167
  %174 = load i32, ptr %21, align 4
  %175 = add nsw i32 %174, 1
  store i32 %175, ptr %21, align 4
  br label %164, !llvm.loop !24

176:                                              ; preds = %164
  %177 = load i32, ptr %22, align 4
  call void @usqrt(i32 noundef %177, ptr noundef %23)
  %178 = load i32, ptr %22, align 4
  %179 = getelementptr inbounds nuw %struct.int_sqrt, ptr %23, i32 0, i32 0
  %180 = load i32, ptr %179, align 4
  %181 = call i32 (ptr, ...) @printf(ptr noundef @.str.6, i32 noundef %178, i32 noundef %180)
  %182 = call i32 (ptr, ...) @printf(ptr noundef @.str.7)
  store double 0.000000e+00, ptr %19, align 8
  br label %183

183:                                              ; preds = %194, %176
  %184 = load double, ptr %19, align 8
  %185 = fcmp ole double %184, 3.600000e+02
  br i1 %185, label %186, label %197

186:                                              ; preds = %183
  %187 = load double, ptr %19, align 8
  %188 = load double, ptr %19, align 8
  %189 = call double @atan(double noundef 1.000000e+00) #5
  %190 = fmul double 4.000000e+00, %189
  %191 = fmul double %188, %190
  %192 = fdiv double %191, 1.800000e+02
  %193 = call i32 (ptr, ...) @printf(ptr noundef @.str.8, double noundef %187, double noundef %192)
  br label %194

194:                                              ; preds = %186
  %195 = load double, ptr %19, align 8
  %196 = fadd double %195, 1.000000e+00
  store double %196, ptr %19, align 8
  br label %183, !llvm.loop !25

197:                                              ; preds = %183
  %198 = call i32 @puts(ptr noundef @.str.9)
  store double 0.000000e+00, ptr %19, align 8
  br label %199

199:                                              ; preds = %213, %197
  %200 = load double, ptr %19, align 8
  %201 = call double @atan(double noundef 1.000000e+00) #5
  %202 = fmul double 4.000000e+00, %201
  %203 = call double @llvm.fmuladd.f64(double 2.000000e+00, double %202, double 0x3EB0C6F7A0B5ED8D)
  %204 = fcmp ole double %200, %203
  br i1 %204, label %205, label %219

205:                                              ; preds = %199
  %206 = load double, ptr %19, align 8
  %207 = load double, ptr %19, align 8
  %208 = fmul double %207, 1.800000e+02
  %209 = call double @atan(double noundef 1.000000e+00) #5
  %210 = fmul double 4.000000e+00, %209
  %211 = fdiv double %208, %210
  %212 = call i32 (ptr, ...) @printf(ptr noundef @.str.10, double noundef %206, double noundef %211)
  br label %213

213:                                              ; preds = %205
  %214 = call double @atan(double noundef 1.000000e+00) #5
  %215 = fmul double 4.000000e+00, %214
  %216 = fdiv double %215, 1.800000e+02
  %217 = load double, ptr %19, align 8
  %218 = fadd double %217, %216
  store double %218, ptr %19, align 8
  br label %199, !llvm.loop !26

219:                                              ; preds = %199
  ret i32 0
}

declare dso_local i32 @printf(ptr noundef, ...) #1

; Function Attrs: nounwind
declare dso_local double @atan(double noundef) #2

declare dso_local i32 @puts(...) #1

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #3

; Function Attrs: noinline nounwind uwtable
define dso_local void @SolveCubic(double noundef %0, double noundef %1, double noundef %2, double noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca double, align 8
  %8 = alloca double, align 8
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca x86_fp80, align 16
  %14 = alloca x86_fp80, align 16
  %15 = alloca x86_fp80, align 16
  %16 = alloca x86_fp80, align 16
  %17 = alloca x86_fp80, align 16
  %18 = alloca double, align 8
  %19 = alloca double, align 8
  store double %0, ptr %7, align 8
  store double %1, ptr %8, align 8
  store double %2, ptr %9, align 8
  store double %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %20 = load double, ptr %8, align 8
  %21 = load double, ptr %7, align 8
  %22 = fdiv double %20, %21
  %23 = fpext double %22 to x86_fp80
  store x86_fp80 %23, ptr %13, align 16
  %24 = load double, ptr %9, align 8
  %25 = load double, ptr %7, align 8
  %26 = fdiv double %24, %25
  %27 = fpext double %26 to x86_fp80
  store x86_fp80 %27, ptr %14, align 16
  %28 = load double, ptr %10, align 8
  %29 = load double, ptr %7, align 8
  %30 = fdiv double %28, %29
  %31 = fpext double %30 to x86_fp80
  store x86_fp80 %31, ptr %15, align 16
  %32 = load x86_fp80, ptr %13, align 16
  %33 = load x86_fp80, ptr %13, align 16
  %34 = load x86_fp80, ptr %14, align 16
  %35 = fmul x86_fp80 0xK4000C000000000000000, %34
  %36 = fneg x86_fp80 %35
  %37 = call x86_fp80 @llvm.fmuladd.f80(x86_fp80 %32, x86_fp80 %33, x86_fp80 %36)
  %38 = fdiv x86_fp80 %37, 0xK40029000000000000000
  store x86_fp80 %38, ptr %16, align 16
  %39 = load x86_fp80, ptr %13, align 16
  %40 = fmul x86_fp80 0xK40008000000000000000, %39
  %41 = load x86_fp80, ptr %13, align 16
  %42 = fmul x86_fp80 %40, %41
  %43 = load x86_fp80, ptr %13, align 16
  %44 = load x86_fp80, ptr %13, align 16
  %45 = fmul x86_fp80 0xK40029000000000000000, %44
  %46 = load x86_fp80, ptr %14, align 16
  %47 = fmul x86_fp80 %45, %46
  %48 = fneg x86_fp80 %47
  %49 = call x86_fp80 @llvm.fmuladd.f80(x86_fp80 %42, x86_fp80 %43, x86_fp80 %48)
  %50 = load x86_fp80, ptr %15, align 16
  %51 = call x86_fp80 @llvm.fmuladd.f80(x86_fp80 0xK4003D800000000000000, x86_fp80 %50, x86_fp80 %49)
  %52 = fdiv x86_fp80 %51, 0xK4004D800000000000000
  store x86_fp80 %52, ptr %17, align 16
  %53 = load x86_fp80, ptr %17, align 16
  %54 = load x86_fp80, ptr %17, align 16
  %55 = load x86_fp80, ptr %16, align 16
  %56 = load x86_fp80, ptr %16, align 16
  %57 = fmul x86_fp80 %55, %56
  %58 = load x86_fp80, ptr %16, align 16
  %59 = fmul x86_fp80 %57, %58
  %60 = fneg x86_fp80 %59
  %61 = call x86_fp80 @llvm.fmuladd.f80(x86_fp80 %53, x86_fp80 %54, x86_fp80 %60)
  %62 = fptrunc x86_fp80 %61 to double
  store double %62, ptr %18, align 8
  %63 = load double, ptr %18, align 8
  %64 = fcmp ole double %63, 0.000000e+00
  br i1 %64, label %65, label %130

65:                                               ; preds = %6
  %66 = load ptr, ptr %11, align 8
  store i32 3, ptr %66, align 4
  %67 = load x86_fp80, ptr %17, align 16
  %68 = load x86_fp80, ptr %16, align 16
  %69 = load x86_fp80, ptr %16, align 16
  %70 = fmul x86_fp80 %68, %69
  %71 = load x86_fp80, ptr %16, align 16
  %72 = fmul x86_fp80 %70, %71
  %73 = fptrunc x86_fp80 %72 to double
  %74 = call double @sqrt(double noundef %73) #5
  %75 = fpext double %74 to x86_fp80
  %76 = fdiv x86_fp80 %67, %75
  %77 = fptrunc x86_fp80 %76 to double
  %78 = call double @acos(double noundef %77) #5
  store double %78, ptr %19, align 8
  %79 = load x86_fp80, ptr %16, align 16
  %80 = fptrunc x86_fp80 %79 to double
  %81 = call double @sqrt(double noundef %80) #5
  %82 = fmul double -2.000000e+00, %81
  %83 = load double, ptr %19, align 8
  %84 = fdiv double %83, 3.000000e+00
  %85 = call double @cos(double noundef %84) #5
  %86 = fmul double %82, %85
  %87 = fpext double %86 to x86_fp80
  %88 = load x86_fp80, ptr %13, align 16
  %89 = fdiv x86_fp80 %88, 0xK4000C000000000000000
  %90 = fsub x86_fp80 %87, %89
  %91 = fptrunc x86_fp80 %90 to double
  %92 = load ptr, ptr %12, align 8
  %93 = getelementptr inbounds double, ptr %92, i64 0
  store double %91, ptr %93, align 8
  %94 = load x86_fp80, ptr %16, align 16
  %95 = fptrunc x86_fp80 %94 to double
  %96 = call double @sqrt(double noundef %95) #5
  %97 = fmul double -2.000000e+00, %96
  %98 = load double, ptr %19, align 8
  %99 = call double @atan(double noundef 1.000000e+00) #5
  %100 = fmul double 4.000000e+00, %99
  %101 = call double @llvm.fmuladd.f64(double 2.000000e+00, double %100, double %98)
  %102 = fdiv double %101, 3.000000e+00
  %103 = call double @cos(double noundef %102) #5
  %104 = fmul double %97, %103
  %105 = fpext double %104 to x86_fp80
  %106 = load x86_fp80, ptr %13, align 16
  %107 = fdiv x86_fp80 %106, 0xK4000C000000000000000
  %108 = fsub x86_fp80 %105, %107
  %109 = fptrunc x86_fp80 %108 to double
  %110 = load ptr, ptr %12, align 8
  %111 = getelementptr inbounds double, ptr %110, i64 1
  store double %109, ptr %111, align 8
  %112 = load x86_fp80, ptr %16, align 16
  %113 = fptrunc x86_fp80 %112 to double
  %114 = call double @sqrt(double noundef %113) #5
  %115 = fmul double -2.000000e+00, %114
  %116 = load double, ptr %19, align 8
  %117 = call double @atan(double noundef 1.000000e+00) #5
  %118 = fmul double 4.000000e+00, %117
  %119 = call double @llvm.fmuladd.f64(double 4.000000e+00, double %118, double %116)
  %120 = fdiv double %119, 3.000000e+00
  %121 = call double @cos(double noundef %120) #5
  %122 = fmul double %115, %121
  %123 = fpext double %122 to x86_fp80
  %124 = load x86_fp80, ptr %13, align 16
  %125 = fdiv x86_fp80 %124, 0xK4000C000000000000000
  %126 = fsub x86_fp80 %123, %125
  %127 = fptrunc x86_fp80 %126 to double
  %128 = load ptr, ptr %12, align 8
  %129 = getelementptr inbounds double, ptr %128, i64 2
  store double %127, ptr %129, align 8
  br label %170

130:                                              ; preds = %6
  %131 = load ptr, ptr %11, align 8
  store i32 1, ptr %131, align 4
  %132 = load double, ptr %18, align 8
  %133 = call double @sqrt(double noundef %132) #5
  %134 = load x86_fp80, ptr %17, align 16
  %135 = fptrunc x86_fp80 %134 to double
  %136 = call double @llvm.fabs.f64(double %135)
  %137 = fadd double %133, %136
  %138 = call double @pow(double noundef %137, double noundef 0x3FD5555555555555) #5
  %139 = load ptr, ptr %12, align 8
  %140 = getelementptr inbounds double, ptr %139, i64 0
  store double %138, ptr %140, align 8
  %141 = load x86_fp80, ptr %16, align 16
  %142 = load ptr, ptr %12, align 8
  %143 = getelementptr inbounds double, ptr %142, i64 0
  %144 = load double, ptr %143, align 8
  %145 = fpext double %144 to x86_fp80
  %146 = fdiv x86_fp80 %141, %145
  %147 = load ptr, ptr %12, align 8
  %148 = getelementptr inbounds double, ptr %147, i64 0
  %149 = load double, ptr %148, align 8
  %150 = fpext double %149 to x86_fp80
  %151 = fadd x86_fp80 %150, %146
  %152 = fptrunc x86_fp80 %151 to double
  store double %152, ptr %148, align 8
  %153 = load x86_fp80, ptr %17, align 16
  %154 = fcmp olt x86_fp80 %153, 0xK00000000000000000000
  %155 = zext i1 %154 to i64
  %156 = select i1 %154, i32 1, i32 -1
  %157 = sitofp i32 %156 to double
  %158 = load ptr, ptr %12, align 8
  %159 = getelementptr inbounds double, ptr %158, i64 0
  %160 = load double, ptr %159, align 8
  %161 = fmul double %160, %157
  store double %161, ptr %159, align 8
  %162 = load x86_fp80, ptr %13, align 16
  %163 = fdiv x86_fp80 %162, 0xK4000C000000000000000
  %164 = load ptr, ptr %12, align 8
  %165 = getelementptr inbounds double, ptr %164, i64 0
  %166 = load double, ptr %165, align 8
  %167 = fpext double %166 to x86_fp80
  %168 = fsub x86_fp80 %167, %163
  %169 = fptrunc x86_fp80 %168 to double
  store double %169, ptr %165, align 8
  br label %170

170:                                              ; preds = %130, %65
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare x86_fp80 @llvm.fmuladd.f80(x86_fp80, x86_fp80, x86_fp80) #3

; Function Attrs: nounwind
declare dso_local double @sqrt(double noundef) #2

; Function Attrs: nounwind
declare dso_local double @acos(double noundef) #2

; Function Attrs: nounwind
declare dso_local double @cos(double noundef) #2

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fabs.f64(double) #3

; Function Attrs: nounwind
declare dso_local double @pow(double noundef, double noundef) #2

; Function Attrs: noinline nounwind uwtable
define dso_local void @usqrt(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  store ptr %1, ptr %4, align 8
  store i32 0, ptr %5, align 4
  store i32 0, ptr %6, align 4
  store i32 0, ptr %7, align 4
  store i32 0, ptr %8, align 4
  br label %9

9:                                                ; preds = %36, %2
  %10 = load i32, ptr %8, align 4
  %11 = icmp slt i32 %10, 32
  br i1 %11, label %12, label %39

12:                                               ; preds = %9
  %13 = load i32, ptr %6, align 4
  %14 = shl i32 %13, 2
  %15 = load i32, ptr %3, align 4
  %16 = and i32 %15, -1073741824
  %17 = lshr i32 %16, 30
  %18 = add i32 %14, %17
  store i32 %18, ptr %6, align 4
  %19 = load i32, ptr %3, align 4
  %20 = shl i32 %19, 2
  store i32 %20, ptr %3, align 4
  %21 = load i32, ptr %5, align 4
  %22 = shl i32 %21, 1
  store i32 %22, ptr %5, align 4
  %23 = load i32, ptr %5, align 4
  %24 = shl i32 %23, 1
  %25 = add i32 %24, 1
  store i32 %25, ptr %7, align 4
  %26 = load i32, ptr %6, align 4
  %27 = load i32, ptr %7, align 4
  %28 = icmp uge i32 %26, %27
  br i1 %28, label %29, label %35

29:                                               ; preds = %12
  %30 = load i32, ptr %7, align 4
  %31 = load i32, ptr %6, align 4
  %32 = sub i32 %31, %30
  store i32 %32, ptr %6, align 4
  %33 = load i32, ptr %5, align 4
  %34 = add i32 %33, 1
  store i32 %34, ptr %5, align 4
  br label %35

35:                                               ; preds = %29, %12
  br label %36

36:                                               ; preds = %35
  %37 = load i32, ptr %8, align 4
  %38 = add nsw i32 %37, 1
  store i32 %38, ptr %8, align 4
  br label %9, !llvm.loop !27

39:                                               ; preds = %9
  %40 = load ptr, ptr %4, align 8
  call void @llvm.memcpy.p0.p0.i64(ptr align 4 %40, ptr align 4 %5, i64 4, i1 false)
  ret void
}

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #4

; Function Attrs: noinline nounwind uwtable
define dso_local double @rad2deg(double noundef %0) #0 {
  %2 = alloca double, align 8
  store double %0, ptr %2, align 8
  %3 = load double, ptr %2, align 8
  %4 = fmul double 1.800000e+02, %3
  %5 = call double @atan(double noundef 1.000000e+00) #5
  %6 = fmul double 4.000000e+00, %5
  %7 = fdiv double %4, %6
  ret double %7
}

; Function Attrs: noinline nounwind uwtable
define dso_local double @deg2rad(double noundef %0) #0 {
  %2 = alloca double, align 8
  store double %0, ptr %2, align 8
  %3 = call double @atan(double noundef 1.000000e+00) #5
  %4 = fmul double 4.000000e+00, %3
  %5 = load double, ptr %2, align 8
  %6 = fmul double %4, %5
  %7 = fdiv double %6, 1.800000e+02
  ret double %7
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #4 = { nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #5 = { nounwind }

!llvm.dbg.cu = !{!0, !2, !4, !6}
!llvm.ident = !{!8, !8, !8, !8}
!llvm.module.flags = !{!9, !10, !11, !12, !13}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\basicmath/basicmath_small.c", directory: "C:/Users/ultim/compiler-opt")
!2 = distinct !DICompileUnit(language: DW_LANG_C11, file: !3, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!3 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\basicmath/cubic.c", directory: "C:/Users/ultim/compiler-opt")
!4 = distinct !DICompileUnit(language: DW_LANG_C11, file: !5, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!5 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\basicmath/isqrt.c", directory: "C:/Users/ultim/compiler-opt")
!6 = distinct !DICompileUnit(language: DW_LANG_C11, file: !7, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!7 = !DIFile(filename: "benchmarks\\mibench\\mibench-master\\automotive\\basicmath/rad2deg.c", directory: "C:/Users/ultim/compiler-opt")
!8 = !{!"clang version 21.1.8"}
!9 = !{i32 2, !"Debug Info Version", i32 3}
!10 = !{i32 1, !"wchar_size", i32 2}
!11 = !{i32 8, !"PIC Level", i32 2}
!12 = !{i32 7, !"uwtable", i32 2}
!13 = !{i32 1, !"MaxTLSAlign", i32 65536}
!14 = distinct !{!14, !15}
!15 = !{!"llvm.loop.mustprogress"}
!16 = distinct !{!16, !15}
!17 = distinct !{!17, !15}
!18 = distinct !{!18, !15}
!19 = distinct !{!19, !15}
!20 = distinct !{!20, !15}
!21 = distinct !{!21, !15}
!22 = distinct !{!22, !15}
!23 = distinct !{!23, !15}
!24 = distinct !{!24, !15}
!25 = distinct !{!25, !15}
!26 = distinct !{!26, !15}
!27 = distinct !{!27, !15}
