; ModuleID = 'benchmarks\correlation.c'
source_filename = "benchmarks\\correlation.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [34 x i8] c"Correlation Execution Time: %f s\0A\00", align 1
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

13:                                               ; preds = %41, %3
  %14 = load i32, ptr %7, align 4
  %15 = load i32, ptr %4, align 4
  %16 = icmp slt i32 %14, %15
  br i1 %16, label %17, label %44

17:                                               ; preds = %13
  store i32 0, ptr %8, align 4
  br label %18

18:                                               ; preds = %37, %17
  %19 = load i32, ptr %8, align 4
  %20 = load i32, ptr %5, align 4
  %21 = icmp slt i32 %19, %20
  br i1 %21, label %22, label %40

22:                                               ; preds = %18
  %23 = load i32, ptr %7, align 4
  %24 = sitofp i32 %23 to double
  %25 = load i32, ptr %8, align 4
  %26 = sitofp i32 %25 to double
  %27 = fmul double %24, %26
  %28 = fdiv double %27, 1.000000e+03
  %29 = load ptr, ptr %6, align 8
  %30 = load i32, ptr %7, align 4
  %31 = sext i32 %30 to i64
  %32 = mul nsw i64 %31, %12
  %33 = getelementptr inbounds double, ptr %29, i64 %32
  %34 = load i32, ptr %8, align 4
  %35 = sext i32 %34 to i64
  %36 = getelementptr inbounds double, ptr %33, i64 %35
  store double %28, ptr %36, align 8
  br label %37

37:                                               ; preds = %22
  %38 = load i32, ptr %8, align 4
  %39 = add nsw i32 %38, 1
  store i32 %39, ptr %8, align 4
  br label %18, !llvm.loop !8

40:                                               ; preds = %18
  br label %41

41:                                               ; preds = %40
  %42 = load i32, ptr %7, align 4
  %43 = add nsw i32 %42, 1
  store i32 %43, ptr %7, align 4
  br label %13, !llvm.loop !10

44:                                               ; preds = %13
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @correlation(i32 noundef %0, i32 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5) #0 {
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca double, align 8
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  %18 = alloca i32, align 4
  %19 = alloca i32, align 4
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  store i32 %0, ptr %7, align 4
  store i32 %1, ptr %8, align 4
  store ptr %2, ptr %9, align 8
  store ptr %3, ptr %10, align 8
  store ptr %4, ptr %11, align 8
  store ptr %5, ptr %12, align 8
  %23 = load i32, ptr %7, align 4
  %24 = zext i32 %23 to i64
  %25 = load i32, ptr %8, align 4
  %26 = zext i32 %25 to i64
  %27 = load i32, ptr %7, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %7, align 4
  %30 = zext i32 %29 to i64
  %31 = load i32, ptr %7, align 4
  %32 = zext i32 %31 to i64
  %33 = load i32, ptr %7, align 4
  %34 = zext i32 %33 to i64
  store double 1.000000e-01, ptr %13, align 8
  store i32 0, ptr %14, align 4
  br label %35

35:                                               ; preds = %76, %6
  %36 = load i32, ptr %14, align 4
  %37 = load i32, ptr %7, align 4
  %38 = icmp slt i32 %36, %37
  br i1 %38, label %39, label %79

39:                                               ; preds = %35
  %40 = load ptr, ptr %10, align 8
  %41 = load i32, ptr %14, align 4
  %42 = sext i32 %41 to i64
  %43 = getelementptr inbounds double, ptr %40, i64 %42
  store double 0.000000e+00, ptr %43, align 8
  store i32 0, ptr %15, align 4
  br label %44

44:                                               ; preds = %64, %39
  %45 = load i32, ptr %15, align 4
  %46 = load i32, ptr %8, align 4
  %47 = icmp slt i32 %45, %46
  br i1 %47, label %48, label %67

48:                                               ; preds = %44
  %49 = load ptr, ptr %9, align 8
  %50 = load i32, ptr %15, align 4
  %51 = sext i32 %50 to i64
  %52 = mul nsw i64 %51, %26
  %53 = getelementptr inbounds double, ptr %49, i64 %52
  %54 = load i32, ptr %14, align 4
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds double, ptr %53, i64 %55
  %57 = load double, ptr %56, align 8
  %58 = load ptr, ptr %10, align 8
  %59 = load i32, ptr %14, align 4
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds double, ptr %58, i64 %60
  %62 = load double, ptr %61, align 8
  %63 = fadd double %62, %57
  store double %63, ptr %61, align 8
  br label %64

64:                                               ; preds = %48
  %65 = load i32, ptr %15, align 4
  %66 = add nsw i32 %65, 1
  store i32 %66, ptr %15, align 4
  br label %44, !llvm.loop !11

67:                                               ; preds = %44
  %68 = load i32, ptr %8, align 4
  %69 = sitofp i32 %68 to double
  %70 = load ptr, ptr %10, align 8
  %71 = load i32, ptr %14, align 4
  %72 = sext i32 %71 to i64
  %73 = getelementptr inbounds double, ptr %70, i64 %72
  %74 = load double, ptr %73, align 8
  %75 = fdiv double %74, %69
  store double %75, ptr %73, align 8
  br label %76

76:                                               ; preds = %67
  %77 = load i32, ptr %14, align 4
  %78 = add nsw i32 %77, 1
  store i32 %78, ptr %14, align 4
  br label %35, !llvm.loop !12

79:                                               ; preds = %35
  store i32 0, ptr %16, align 4
  br label %80

80:                                               ; preds = %165, %79
  %81 = load i32, ptr %16, align 4
  %82 = load i32, ptr %7, align 4
  %83 = icmp slt i32 %81, %82
  br i1 %83, label %84, label %168

84:                                               ; preds = %80
  %85 = load ptr, ptr %11, align 8
  %86 = load i32, ptr %16, align 4
  %87 = sext i32 %86 to i64
  %88 = getelementptr inbounds double, ptr %85, i64 %87
  store double 0.000000e+00, ptr %88, align 8
  store i32 0, ptr %17, align 4
  br label %89

89:                                               ; preds = %130, %84
  %90 = load i32, ptr %17, align 4
  %91 = load i32, ptr %8, align 4
  %92 = icmp slt i32 %90, %91
  br i1 %92, label %93, label %133

93:                                               ; preds = %89
  %94 = load ptr, ptr %9, align 8
  %95 = load i32, ptr %17, align 4
  %96 = sext i32 %95 to i64
  %97 = mul nsw i64 %96, %26
  %98 = getelementptr inbounds double, ptr %94, i64 %97
  %99 = load i32, ptr %16, align 4
  %100 = sext i32 %99 to i64
  %101 = getelementptr inbounds double, ptr %98, i64 %100
  %102 = load double, ptr %101, align 8
  %103 = load ptr, ptr %10, align 8
  %104 = load i32, ptr %16, align 4
  %105 = sext i32 %104 to i64
  %106 = getelementptr inbounds double, ptr %103, i64 %105
  %107 = load double, ptr %106, align 8
  %108 = fsub double %102, %107
  %109 = load ptr, ptr %9, align 8
  %110 = load i32, ptr %17, align 4
  %111 = sext i32 %110 to i64
  %112 = mul nsw i64 %111, %26
  %113 = getelementptr inbounds double, ptr %109, i64 %112
  %114 = load i32, ptr %16, align 4
  %115 = sext i32 %114 to i64
  %116 = getelementptr inbounds double, ptr %113, i64 %115
  %117 = load double, ptr %116, align 8
  %118 = load ptr, ptr %10, align 8
  %119 = load i32, ptr %16, align 4
  %120 = sext i32 %119 to i64
  %121 = getelementptr inbounds double, ptr %118, i64 %120
  %122 = load double, ptr %121, align 8
  %123 = fsub double %117, %122
  %124 = load ptr, ptr %11, align 8
  %125 = load i32, ptr %16, align 4
  %126 = sext i32 %125 to i64
  %127 = getelementptr inbounds double, ptr %124, i64 %126
  %128 = load double, ptr %127, align 8
  %129 = call double @llvm.fmuladd.f64(double %108, double %123, double %128)
  store double %129, ptr %127, align 8
  br label %130

130:                                              ; preds = %93
  %131 = load i32, ptr %17, align 4
  %132 = add nsw i32 %131, 1
  store i32 %132, ptr %17, align 4
  br label %89, !llvm.loop !13

133:                                              ; preds = %89
  %134 = load i32, ptr %8, align 4
  %135 = sitofp i32 %134 to double
  %136 = load ptr, ptr %11, align 8
  %137 = load i32, ptr %16, align 4
  %138 = sext i32 %137 to i64
  %139 = getelementptr inbounds double, ptr %136, i64 %138
  %140 = load double, ptr %139, align 8
  %141 = fdiv double %140, %135
  store double %141, ptr %139, align 8
  %142 = load ptr, ptr %11, align 8
  %143 = load i32, ptr %16, align 4
  %144 = sext i32 %143 to i64
  %145 = getelementptr inbounds double, ptr %142, i64 %144
  %146 = load double, ptr %145, align 8
  %147 = call double @sqrt(double noundef %146) #5
  %148 = load ptr, ptr %11, align 8
  %149 = load i32, ptr %16, align 4
  %150 = sext i32 %149 to i64
  %151 = getelementptr inbounds double, ptr %148, i64 %150
  store double %147, ptr %151, align 8
  %152 = load ptr, ptr %11, align 8
  %153 = load i32, ptr %16, align 4
  %154 = sext i32 %153 to i64
  %155 = getelementptr inbounds double, ptr %152, i64 %154
  %156 = load double, ptr %155, align 8
  %157 = load double, ptr %13, align 8
  %158 = fcmp ole double %156, %157
  br i1 %158, label %159, label %164

159:                                              ; preds = %133
  %160 = load ptr, ptr %11, align 8
  %161 = load i32, ptr %16, align 4
  %162 = sext i32 %161 to i64
  %163 = getelementptr inbounds double, ptr %160, i64 %162
  store double 1.000000e+00, ptr %163, align 8
  br label %164

164:                                              ; preds = %159, %133
  br label %165

165:                                              ; preds = %164
  %166 = load i32, ptr %16, align 4
  %167 = add nsw i32 %166, 1
  store i32 %167, ptr %16, align 4
  br label %80, !llvm.loop !14

168:                                              ; preds = %80
  store i32 0, ptr %18, align 4
  br label %169

169:                                              ; preds = %217, %168
  %170 = load i32, ptr %18, align 4
  %171 = load i32, ptr %8, align 4
  %172 = icmp slt i32 %170, %171
  br i1 %172, label %173, label %220

173:                                              ; preds = %169
  store i32 0, ptr %19, align 4
  br label %174

174:                                              ; preds = %213, %173
  %175 = load i32, ptr %19, align 4
  %176 = load i32, ptr %7, align 4
  %177 = icmp slt i32 %175, %176
  br i1 %177, label %178, label %216

178:                                              ; preds = %174
  %179 = load ptr, ptr %10, align 8
  %180 = load i32, ptr %19, align 4
  %181 = sext i32 %180 to i64
  %182 = getelementptr inbounds double, ptr %179, i64 %181
  %183 = load double, ptr %182, align 8
  %184 = load ptr, ptr %9, align 8
  %185 = load i32, ptr %18, align 4
  %186 = sext i32 %185 to i64
  %187 = mul nsw i64 %186, %26
  %188 = getelementptr inbounds double, ptr %184, i64 %187
  %189 = load i32, ptr %19, align 4
  %190 = sext i32 %189 to i64
  %191 = getelementptr inbounds double, ptr %188, i64 %190
  %192 = load double, ptr %191, align 8
  %193 = fsub double %192, %183
  store double %193, ptr %191, align 8
  %194 = load i32, ptr %8, align 4
  %195 = sitofp i32 %194 to double
  %196 = call double @sqrt(double noundef %195) #5
  %197 = load ptr, ptr %11, align 8
  %198 = load i32, ptr %19, align 4
  %199 = sext i32 %198 to i64
  %200 = getelementptr inbounds double, ptr %197, i64 %199
  %201 = load double, ptr %200, align 8
  %202 = fmul double %196, %201
  %203 = load ptr, ptr %9, align 8
  %204 = load i32, ptr %18, align 4
  %205 = sext i32 %204 to i64
  %206 = mul nsw i64 %205, %26
  %207 = getelementptr inbounds double, ptr %203, i64 %206
  %208 = load i32, ptr %19, align 4
  %209 = sext i32 %208 to i64
  %210 = getelementptr inbounds double, ptr %207, i64 %209
  %211 = load double, ptr %210, align 8
  %212 = fdiv double %211, %202
  store double %212, ptr %210, align 8
  br label %213

213:                                              ; preds = %178
  %214 = load i32, ptr %19, align 4
  %215 = add nsw i32 %214, 1
  store i32 %215, ptr %19, align 4
  br label %174, !llvm.loop !15

216:                                              ; preds = %174
  br label %217

217:                                              ; preds = %216
  %218 = load i32, ptr %18, align 4
  %219 = add nsw i32 %218, 1
  store i32 %219, ptr %18, align 4
  br label %169, !llvm.loop !16

220:                                              ; preds = %169
  store i32 0, ptr %20, align 4
  br label %221

221:                                              ; preds = %308, %220
  %222 = load i32, ptr %20, align 4
  %223 = load i32, ptr %7, align 4
  %224 = sub nsw i32 %223, 1
  %225 = icmp slt i32 %222, %224
  br i1 %225, label %226, label %311

226:                                              ; preds = %221
  %227 = load ptr, ptr %12, align 8
  %228 = load i32, ptr %20, align 4
  %229 = sext i32 %228 to i64
  %230 = mul nsw i64 %229, %34
  %231 = getelementptr inbounds double, ptr %227, i64 %230
  %232 = load i32, ptr %20, align 4
  %233 = sext i32 %232 to i64
  %234 = getelementptr inbounds double, ptr %231, i64 %233
  store double 1.000000e+00, ptr %234, align 8
  %235 = load i32, ptr %20, align 4
  %236 = add nsw i32 %235, 1
  store i32 %236, ptr %21, align 4
  br label %237

237:                                              ; preds = %304, %226
  %238 = load i32, ptr %21, align 4
  %239 = load i32, ptr %7, align 4
  %240 = icmp slt i32 %238, %239
  br i1 %240, label %241, label %307

241:                                              ; preds = %237
  %242 = load ptr, ptr %12, align 8
  %243 = load i32, ptr %20, align 4
  %244 = sext i32 %243 to i64
  %245 = mul nsw i64 %244, %34
  %246 = getelementptr inbounds double, ptr %242, i64 %245
  %247 = load i32, ptr %21, align 4
  %248 = sext i32 %247 to i64
  %249 = getelementptr inbounds double, ptr %246, i64 %248
  store double 0.000000e+00, ptr %249, align 8
  store i32 0, ptr %22, align 4
  br label %250

250:                                              ; preds = %283, %241
  %251 = load i32, ptr %22, align 4
  %252 = load i32, ptr %8, align 4
  %253 = icmp slt i32 %251, %252
  br i1 %253, label %254, label %286

254:                                              ; preds = %250
  %255 = load ptr, ptr %9, align 8
  %256 = load i32, ptr %22, align 4
  %257 = sext i32 %256 to i64
  %258 = mul nsw i64 %257, %26
  %259 = getelementptr inbounds double, ptr %255, i64 %258
  %260 = load i32, ptr %20, align 4
  %261 = sext i32 %260 to i64
  %262 = getelementptr inbounds double, ptr %259, i64 %261
  %263 = load double, ptr %262, align 8
  %264 = load ptr, ptr %9, align 8
  %265 = load i32, ptr %22, align 4
  %266 = sext i32 %265 to i64
  %267 = mul nsw i64 %266, %26
  %268 = getelementptr inbounds double, ptr %264, i64 %267
  %269 = load i32, ptr %21, align 4
  %270 = sext i32 %269 to i64
  %271 = getelementptr inbounds double, ptr %268, i64 %270
  %272 = load double, ptr %271, align 8
  %273 = load ptr, ptr %12, align 8
  %274 = load i32, ptr %20, align 4
  %275 = sext i32 %274 to i64
  %276 = mul nsw i64 %275, %34
  %277 = getelementptr inbounds double, ptr %273, i64 %276
  %278 = load i32, ptr %21, align 4
  %279 = sext i32 %278 to i64
  %280 = getelementptr inbounds double, ptr %277, i64 %279
  %281 = load double, ptr %280, align 8
  %282 = call double @llvm.fmuladd.f64(double %263, double %272, double %281)
  store double %282, ptr %280, align 8
  br label %283

283:                                              ; preds = %254
  %284 = load i32, ptr %22, align 4
  %285 = add nsw i32 %284, 1
  store i32 %285, ptr %22, align 4
  br label %250, !llvm.loop !17

286:                                              ; preds = %250
  %287 = load ptr, ptr %12, align 8
  %288 = load i32, ptr %20, align 4
  %289 = sext i32 %288 to i64
  %290 = mul nsw i64 %289, %34
  %291 = getelementptr inbounds double, ptr %287, i64 %290
  %292 = load i32, ptr %21, align 4
  %293 = sext i32 %292 to i64
  %294 = getelementptr inbounds double, ptr %291, i64 %293
  %295 = load double, ptr %294, align 8
  %296 = load ptr, ptr %12, align 8
  %297 = load i32, ptr %21, align 4
  %298 = sext i32 %297 to i64
  %299 = mul nsw i64 %298, %34
  %300 = getelementptr inbounds double, ptr %296, i64 %299
  %301 = load i32, ptr %20, align 4
  %302 = sext i32 %301 to i64
  %303 = getelementptr inbounds double, ptr %300, i64 %302
  store double %295, ptr %303, align 8
  br label %304

304:                                              ; preds = %286
  %305 = load i32, ptr %21, align 4
  %306 = add nsw i32 %305, 1
  store i32 %306, ptr %21, align 4
  br label %237, !llvm.loop !18

307:                                              ; preds = %237
  br label %308

308:                                              ; preds = %307
  %309 = load i32, ptr %20, align 4
  %310 = add nsw i32 %309, 1
  store i32 %310, ptr %20, align 4
  br label %221, !llvm.loop !19

311:                                              ; preds = %221
  %312 = load ptr, ptr %12, align 8
  %313 = load i32, ptr %7, align 4
  %314 = sub nsw i32 %313, 1
  %315 = sext i32 %314 to i64
  %316 = mul nsw i64 %315, %34
  %317 = getelementptr inbounds double, ptr %312, i64 %316
  %318 = load i32, ptr %7, align 4
  %319 = sub nsw i32 %318, 1
  %320 = sext i32 %319 to i64
  %321 = getelementptr inbounds double, ptr %317, i64 %320
  store double 1.000000e+00, ptr %321, align 8
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
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 500, ptr %2, align 4
  store i32 500, ptr %3, align 4
  %10 = load i32, ptr %3, align 4
  %11 = zext i32 %10 to i64
  %12 = load i32, ptr %2, align 4
  %13 = zext i32 %12 to i64
  %14 = load i32, ptr %3, align 4
  %15 = zext i32 %14 to i64
  %16 = mul nuw i64 %13, %15
  %17 = mul nuw i64 8, %16
  %18 = call ptr @malloc(i64 noundef %17) #6
  store ptr %18, ptr %4, align 8
  %19 = load i32, ptr %2, align 4
  %20 = sext i32 %19 to i64
  %21 = mul i64 %20, 8
  %22 = call ptr @malloc(i64 noundef %21) #6
  store ptr %22, ptr %5, align 8
  %23 = load i32, ptr %2, align 4
  %24 = sext i32 %23 to i64
  %25 = mul i64 %24, 8
  %26 = call ptr @malloc(i64 noundef %25) #6
  store ptr %26, ptr %6, align 8
  %27 = load i32, ptr %2, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %2, align 4
  %30 = zext i32 %29 to i64
  %31 = load i32, ptr %2, align 4
  %32 = zext i32 %31 to i64
  %33 = mul nuw i64 %30, %32
  %34 = mul nuw i64 8, %33
  %35 = call ptr @malloc(i64 noundef %34) #6
  store ptr %35, ptr %7, align 8
  %36 = load i32, ptr %2, align 4
  %37 = load i32, ptr %3, align 4
  %38 = load ptr, ptr %4, align 8
  call void @init_array(i32 noundef %36, i32 noundef %37, ptr noundef %38)
  %39 = call i32 @clock()
  store i32 %39, ptr %8, align 4
  %40 = load i32, ptr %2, align 4
  %41 = load i32, ptr %3, align 4
  %42 = load ptr, ptr %4, align 8
  %43 = load ptr, ptr %5, align 8
  %44 = load ptr, ptr %6, align 8
  %45 = load ptr, ptr %7, align 8
  call void @correlation(i32 noundef %40, i32 noundef %41, ptr noundef %42, ptr noundef %43, ptr noundef %44, ptr noundef %45)
  %46 = call i32 @clock()
  store i32 %46, ptr %9, align 4
  %47 = load i32, ptr %9, align 4
  %48 = load i32, ptr %8, align 4
  %49 = sub nsw i32 %47, %48
  %50 = sitofp i32 %49 to double
  %51 = fdiv double %50, 1.000000e+03
  %52 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %51)
  %53 = load ptr, ptr %7, align 8
  %54 = mul nsw i64 0, %28
  %55 = getelementptr inbounds double, ptr %53, i64 %54
  %56 = getelementptr inbounds double, ptr %55, i64 0
  %57 = load double, ptr %56, align 8
  %58 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %57)
  %59 = load ptr, ptr %4, align 8
  call void @free(ptr noundef %59)
  %60 = load ptr, ptr %5, align 8
  call void @free(ptr noundef %60)
  %61 = load ptr, ptr %6, align 8
  call void @free(ptr noundef %61)
  %62 = load ptr, ptr %7, align 8
  call void @free(ptr noundef %62)
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
!1 = !DIFile(filename: "benchmarks/correlation.c", directory: "C:/Users/ultim/compiler-opt")
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
!17 = distinct !{!17, !9}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
