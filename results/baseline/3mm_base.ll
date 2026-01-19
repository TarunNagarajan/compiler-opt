; ModuleID = 'benchmarks\3mm.c'
source_filename = "benchmarks\\3mm.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [26 x i8] c"3MM Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: noinline nounwind uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, i32 noundef %4, ptr noundef %5, ptr noundef %6, ptr noundef %7, ptr noundef %8) #0 {
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca ptr, align 8
  %16 = alloca ptr, align 8
  %17 = alloca ptr, align 8
  %18 = alloca ptr, align 8
  %19 = alloca i32, align 4
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  %23 = alloca i32, align 4
  %24 = alloca i32, align 4
  %25 = alloca i32, align 4
  %26 = alloca i32, align 4
  store i32 %0, ptr %10, align 4
  store i32 %1, ptr %11, align 4
  store i32 %2, ptr %12, align 4
  store i32 %3, ptr %13, align 4
  store i32 %4, ptr %14, align 4
  store ptr %5, ptr %15, align 8
  store ptr %6, ptr %16, align 8
  store ptr %7, ptr %17, align 8
  store ptr %8, ptr %18, align 8
  %27 = load i32, ptr %10, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %12, align 4
  %30 = zext i32 %29 to i64
  %31 = load i32, ptr %12, align 4
  %32 = zext i32 %31 to i64
  %33 = load i32, ptr %11, align 4
  %34 = zext i32 %33 to i64
  %35 = load i32, ptr %11, align 4
  %36 = zext i32 %35 to i64
  %37 = load i32, ptr %14, align 4
  %38 = zext i32 %37 to i64
  %39 = load i32, ptr %14, align 4
  %40 = zext i32 %39 to i64
  %41 = load i32, ptr %13, align 4
  %42 = zext i32 %41 to i64
  store i32 0, ptr %19, align 4
  br label %43

43:                                               ; preds = %75, %9
  %44 = load i32, ptr %19, align 4
  %45 = load i32, ptr %10, align 4
  %46 = icmp slt i32 %44, %45
  br i1 %46, label %47, label %78

47:                                               ; preds = %43
  store i32 0, ptr %20, align 4
  br label %48

48:                                               ; preds = %71, %47
  %49 = load i32, ptr %20, align 4
  %50 = load i32, ptr %12, align 4
  %51 = icmp slt i32 %49, %50
  br i1 %51, label %52, label %74

52:                                               ; preds = %48
  %53 = load i32, ptr %19, align 4
  %54 = load i32, ptr %20, align 4
  %55 = mul nsw i32 %53, %54
  %56 = add nsw i32 %55, 1
  %57 = load i32, ptr %10, align 4
  %58 = srem i32 %56, %57
  %59 = sitofp i32 %58 to double
  %60 = load i32, ptr %10, align 4
  %61 = sitofp i32 %60 to double
  %62 = fdiv double %59, %61
  %63 = load ptr, ptr %15, align 8
  %64 = load i32, ptr %19, align 4
  %65 = sext i32 %64 to i64
  %66 = mul nsw i64 %65, %30
  %67 = getelementptr inbounds double, ptr %63, i64 %66
  %68 = load i32, ptr %20, align 4
  %69 = sext i32 %68 to i64
  %70 = getelementptr inbounds double, ptr %67, i64 %69
  store double %62, ptr %70, align 8
  br label %71

71:                                               ; preds = %52
  %72 = load i32, ptr %20, align 4
  %73 = add nsw i32 %72, 1
  store i32 %73, ptr %20, align 4
  br label %48, !llvm.loop !8

74:                                               ; preds = %48
  br label %75

75:                                               ; preds = %74
  %76 = load i32, ptr %19, align 4
  %77 = add nsw i32 %76, 1
  store i32 %77, ptr %19, align 4
  br label %43, !llvm.loop !10

78:                                               ; preds = %43
  store i32 0, ptr %21, align 4
  br label %79

79:                                               ; preds = %112, %78
  %80 = load i32, ptr %21, align 4
  %81 = load i32, ptr %12, align 4
  %82 = icmp slt i32 %80, %81
  br i1 %82, label %83, label %115

83:                                               ; preds = %79
  store i32 0, ptr %22, align 4
  br label %84

84:                                               ; preds = %108, %83
  %85 = load i32, ptr %22, align 4
  %86 = load i32, ptr %11, align 4
  %87 = icmp slt i32 %85, %86
  br i1 %87, label %88, label %111

88:                                               ; preds = %84
  %89 = load i32, ptr %21, align 4
  %90 = load i32, ptr %22, align 4
  %91 = add nsw i32 %90, 1
  %92 = mul nsw i32 %89, %91
  %93 = add nsw i32 %92, 2
  %94 = load i32, ptr %11, align 4
  %95 = srem i32 %93, %94
  %96 = sitofp i32 %95 to double
  %97 = load i32, ptr %11, align 4
  %98 = sitofp i32 %97 to double
  %99 = fdiv double %96, %98
  %100 = load ptr, ptr %16, align 8
  %101 = load i32, ptr %21, align 4
  %102 = sext i32 %101 to i64
  %103 = mul nsw i64 %102, %34
  %104 = getelementptr inbounds double, ptr %100, i64 %103
  %105 = load i32, ptr %22, align 4
  %106 = sext i32 %105 to i64
  %107 = getelementptr inbounds double, ptr %104, i64 %106
  store double %99, ptr %107, align 8
  br label %108

108:                                              ; preds = %88
  %109 = load i32, ptr %22, align 4
  %110 = add nsw i32 %109, 1
  store i32 %110, ptr %22, align 4
  br label %84, !llvm.loop !11

111:                                              ; preds = %84
  br label %112

112:                                              ; preds = %111
  %113 = load i32, ptr %21, align 4
  %114 = add nsw i32 %113, 1
  store i32 %114, ptr %21, align 4
  br label %79, !llvm.loop !12

115:                                              ; preds = %79
  store i32 0, ptr %23, align 4
  br label %116

116:                                              ; preds = %148, %115
  %117 = load i32, ptr %23, align 4
  %118 = load i32, ptr %11, align 4
  %119 = icmp slt i32 %117, %118
  br i1 %119, label %120, label %151

120:                                              ; preds = %116
  store i32 0, ptr %24, align 4
  br label %121

121:                                              ; preds = %144, %120
  %122 = load i32, ptr %24, align 4
  %123 = load i32, ptr %14, align 4
  %124 = icmp slt i32 %122, %123
  br i1 %124, label %125, label %147

125:                                              ; preds = %121
  %126 = load i32, ptr %23, align 4
  %127 = load i32, ptr %24, align 4
  %128 = add nsw i32 %127, 3
  %129 = mul nsw i32 %126, %128
  %130 = load i32, ptr %14, align 4
  %131 = srem i32 %129, %130
  %132 = sitofp i32 %131 to double
  %133 = load i32, ptr %14, align 4
  %134 = sitofp i32 %133 to double
  %135 = fdiv double %132, %134
  %136 = load ptr, ptr %17, align 8
  %137 = load i32, ptr %23, align 4
  %138 = sext i32 %137 to i64
  %139 = mul nsw i64 %138, %38
  %140 = getelementptr inbounds double, ptr %136, i64 %139
  %141 = load i32, ptr %24, align 4
  %142 = sext i32 %141 to i64
  %143 = getelementptr inbounds double, ptr %140, i64 %142
  store double %135, ptr %143, align 8
  br label %144

144:                                              ; preds = %125
  %145 = load i32, ptr %24, align 4
  %146 = add nsw i32 %145, 1
  store i32 %146, ptr %24, align 4
  br label %121, !llvm.loop !13

147:                                              ; preds = %121
  br label %148

148:                                              ; preds = %147
  %149 = load i32, ptr %23, align 4
  %150 = add nsw i32 %149, 1
  store i32 %150, ptr %23, align 4
  br label %116, !llvm.loop !14

151:                                              ; preds = %116
  store i32 0, ptr %25, align 4
  br label %152

152:                                              ; preds = %185, %151
  %153 = load i32, ptr %25, align 4
  %154 = load i32, ptr %14, align 4
  %155 = icmp slt i32 %153, %154
  br i1 %155, label %156, label %188

156:                                              ; preds = %152
  store i32 0, ptr %26, align 4
  br label %157

157:                                              ; preds = %181, %156
  %158 = load i32, ptr %26, align 4
  %159 = load i32, ptr %13, align 4
  %160 = icmp slt i32 %158, %159
  br i1 %160, label %161, label %184

161:                                              ; preds = %157
  %162 = load i32, ptr %25, align 4
  %163 = load i32, ptr %26, align 4
  %164 = add nsw i32 %163, 2
  %165 = mul nsw i32 %162, %164
  %166 = add nsw i32 %165, 2
  %167 = load i32, ptr %13, align 4
  %168 = srem i32 %166, %167
  %169 = sitofp i32 %168 to double
  %170 = load i32, ptr %13, align 4
  %171 = sitofp i32 %170 to double
  %172 = fdiv double %169, %171
  %173 = load ptr, ptr %18, align 8
  %174 = load i32, ptr %25, align 4
  %175 = sext i32 %174 to i64
  %176 = mul nsw i64 %175, %42
  %177 = getelementptr inbounds double, ptr %173, i64 %176
  %178 = load i32, ptr %26, align 4
  %179 = sext i32 %178 to i64
  %180 = getelementptr inbounds double, ptr %177, i64 %179
  store double %172, ptr %180, align 8
  br label %181

181:                                              ; preds = %161
  %182 = load i32, ptr %26, align 4
  %183 = add nsw i32 %182, 1
  store i32 %183, ptr %26, align 4
  br label %157, !llvm.loop !15

184:                                              ; preds = %157
  br label %185

185:                                              ; preds = %184
  %186 = load i32, ptr %25, align 4
  %187 = add nsw i32 %186, 1
  store i32 %187, ptr %25, align 4
  br label %152, !llvm.loop !16

188:                                              ; preds = %152
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @mm3(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, i32 noundef %4, ptr noundef %5, ptr noundef %6, ptr noundef %7, ptr noundef %8, ptr noundef %9, ptr noundef %10, ptr noundef %11) #0 {
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  %18 = alloca ptr, align 8
  %19 = alloca ptr, align 8
  %20 = alloca ptr, align 8
  %21 = alloca ptr, align 8
  %22 = alloca ptr, align 8
  %23 = alloca ptr, align 8
  %24 = alloca ptr, align 8
  %25 = alloca i32, align 4
  %26 = alloca i32, align 4
  %27 = alloca i32, align 4
  %28 = alloca i32, align 4
  %29 = alloca i32, align 4
  %30 = alloca i32, align 4
  %31 = alloca i32, align 4
  %32 = alloca i32, align 4
  %33 = alloca i32, align 4
  store i32 %0, ptr %13, align 4
  store i32 %1, ptr %14, align 4
  store i32 %2, ptr %15, align 4
  store i32 %3, ptr %16, align 4
  store i32 %4, ptr %17, align 4
  store ptr %5, ptr %18, align 8
  store ptr %6, ptr %19, align 8
  store ptr %7, ptr %20, align 8
  store ptr %8, ptr %21, align 8
  store ptr %9, ptr %22, align 8
  store ptr %10, ptr %23, align 8
  store ptr %11, ptr %24, align 8
  %34 = load i32, ptr %13, align 4
  %35 = zext i32 %34 to i64
  %36 = load i32, ptr %14, align 4
  %37 = zext i32 %36 to i64
  %38 = load i32, ptr %13, align 4
  %39 = zext i32 %38 to i64
  %40 = load i32, ptr %15, align 4
  %41 = zext i32 %40 to i64
  %42 = load i32, ptr %15, align 4
  %43 = zext i32 %42 to i64
  %44 = load i32, ptr %14, align 4
  %45 = zext i32 %44 to i64
  %46 = load i32, ptr %14, align 4
  %47 = zext i32 %46 to i64
  %48 = load i32, ptr %16, align 4
  %49 = zext i32 %48 to i64
  %50 = load i32, ptr %14, align 4
  %51 = zext i32 %50 to i64
  %52 = load i32, ptr %17, align 4
  %53 = zext i32 %52 to i64
  %54 = load i32, ptr %17, align 4
  %55 = zext i32 %54 to i64
  %56 = load i32, ptr %16, align 4
  %57 = zext i32 %56 to i64
  %58 = load i32, ptr %13, align 4
  %59 = zext i32 %58 to i64
  %60 = load i32, ptr %16, align 4
  %61 = zext i32 %60 to i64
  store i32 0, ptr %25, align 4
  br label %62

62:                                               ; preds = %121, %12
  %63 = load i32, ptr %25, align 4
  %64 = load i32, ptr %13, align 4
  %65 = icmp slt i32 %63, %64
  br i1 %65, label %66, label %124

66:                                               ; preds = %62
  store i32 0, ptr %26, align 4
  br label %67

67:                                               ; preds = %117, %66
  %68 = load i32, ptr %26, align 4
  %69 = load i32, ptr %14, align 4
  %70 = icmp slt i32 %68, %69
  br i1 %70, label %71, label %120

71:                                               ; preds = %67
  %72 = load ptr, ptr %18, align 8
  %73 = load i32, ptr %25, align 4
  %74 = sext i32 %73 to i64
  %75 = mul nsw i64 %74, %37
  %76 = getelementptr inbounds double, ptr %72, i64 %75
  %77 = load i32, ptr %26, align 4
  %78 = sext i32 %77 to i64
  %79 = getelementptr inbounds double, ptr %76, i64 %78
  store double 0.000000e+00, ptr %79, align 8
  store i32 0, ptr %27, align 4
  br label %80

80:                                               ; preds = %113, %71
  %81 = load i32, ptr %27, align 4
  %82 = load i32, ptr %15, align 4
  %83 = icmp slt i32 %81, %82
  br i1 %83, label %84, label %116

84:                                               ; preds = %80
  %85 = load ptr, ptr %19, align 8
  %86 = load i32, ptr %25, align 4
  %87 = sext i32 %86 to i64
  %88 = mul nsw i64 %87, %41
  %89 = getelementptr inbounds double, ptr %85, i64 %88
  %90 = load i32, ptr %27, align 4
  %91 = sext i32 %90 to i64
  %92 = getelementptr inbounds double, ptr %89, i64 %91
  %93 = load double, ptr %92, align 8
  %94 = load ptr, ptr %20, align 8
  %95 = load i32, ptr %27, align 4
  %96 = sext i32 %95 to i64
  %97 = mul nsw i64 %96, %45
  %98 = getelementptr inbounds double, ptr %94, i64 %97
  %99 = load i32, ptr %26, align 4
  %100 = sext i32 %99 to i64
  %101 = getelementptr inbounds double, ptr %98, i64 %100
  %102 = load double, ptr %101, align 8
  %103 = load ptr, ptr %18, align 8
  %104 = load i32, ptr %25, align 4
  %105 = sext i32 %104 to i64
  %106 = mul nsw i64 %105, %37
  %107 = getelementptr inbounds double, ptr %103, i64 %106
  %108 = load i32, ptr %26, align 4
  %109 = sext i32 %108 to i64
  %110 = getelementptr inbounds double, ptr %107, i64 %109
  %111 = load double, ptr %110, align 8
  %112 = call double @llvm.fmuladd.f64(double %93, double %102, double %111)
  store double %112, ptr %110, align 8
  br label %113

113:                                              ; preds = %84
  %114 = load i32, ptr %27, align 4
  %115 = add nsw i32 %114, 1
  store i32 %115, ptr %27, align 4
  br label %80, !llvm.loop !17

116:                                              ; preds = %80
  br label %117

117:                                              ; preds = %116
  %118 = load i32, ptr %26, align 4
  %119 = add nsw i32 %118, 1
  store i32 %119, ptr %26, align 4
  br label %67, !llvm.loop !18

120:                                              ; preds = %67
  br label %121

121:                                              ; preds = %120
  %122 = load i32, ptr %25, align 4
  %123 = add nsw i32 %122, 1
  store i32 %123, ptr %25, align 4
  br label %62, !llvm.loop !19

124:                                              ; preds = %62
  store i32 0, ptr %28, align 4
  br label %125

125:                                              ; preds = %184, %124
  %126 = load i32, ptr %28, align 4
  %127 = load i32, ptr %14, align 4
  %128 = icmp slt i32 %126, %127
  br i1 %128, label %129, label %187

129:                                              ; preds = %125
  store i32 0, ptr %29, align 4
  br label %130

130:                                              ; preds = %180, %129
  %131 = load i32, ptr %29, align 4
  %132 = load i32, ptr %16, align 4
  %133 = icmp slt i32 %131, %132
  br i1 %133, label %134, label %183

134:                                              ; preds = %130
  %135 = load ptr, ptr %21, align 8
  %136 = load i32, ptr %28, align 4
  %137 = sext i32 %136 to i64
  %138 = mul nsw i64 %137, %49
  %139 = getelementptr inbounds double, ptr %135, i64 %138
  %140 = load i32, ptr %29, align 4
  %141 = sext i32 %140 to i64
  %142 = getelementptr inbounds double, ptr %139, i64 %141
  store double 0.000000e+00, ptr %142, align 8
  store i32 0, ptr %30, align 4
  br label %143

143:                                              ; preds = %176, %134
  %144 = load i32, ptr %30, align 4
  %145 = load i32, ptr %17, align 4
  %146 = icmp slt i32 %144, %145
  br i1 %146, label %147, label %179

147:                                              ; preds = %143
  %148 = load ptr, ptr %22, align 8
  %149 = load i32, ptr %28, align 4
  %150 = sext i32 %149 to i64
  %151 = mul nsw i64 %150, %53
  %152 = getelementptr inbounds double, ptr %148, i64 %151
  %153 = load i32, ptr %30, align 4
  %154 = sext i32 %153 to i64
  %155 = getelementptr inbounds double, ptr %152, i64 %154
  %156 = load double, ptr %155, align 8
  %157 = load ptr, ptr %23, align 8
  %158 = load i32, ptr %30, align 4
  %159 = sext i32 %158 to i64
  %160 = mul nsw i64 %159, %57
  %161 = getelementptr inbounds double, ptr %157, i64 %160
  %162 = load i32, ptr %29, align 4
  %163 = sext i32 %162 to i64
  %164 = getelementptr inbounds double, ptr %161, i64 %163
  %165 = load double, ptr %164, align 8
  %166 = load ptr, ptr %21, align 8
  %167 = load i32, ptr %28, align 4
  %168 = sext i32 %167 to i64
  %169 = mul nsw i64 %168, %49
  %170 = getelementptr inbounds double, ptr %166, i64 %169
  %171 = load i32, ptr %29, align 4
  %172 = sext i32 %171 to i64
  %173 = getelementptr inbounds double, ptr %170, i64 %172
  %174 = load double, ptr %173, align 8
  %175 = call double @llvm.fmuladd.f64(double %156, double %165, double %174)
  store double %175, ptr %173, align 8
  br label %176

176:                                              ; preds = %147
  %177 = load i32, ptr %30, align 4
  %178 = add nsw i32 %177, 1
  store i32 %178, ptr %30, align 4
  br label %143, !llvm.loop !20

179:                                              ; preds = %143
  br label %180

180:                                              ; preds = %179
  %181 = load i32, ptr %29, align 4
  %182 = add nsw i32 %181, 1
  store i32 %182, ptr %29, align 4
  br label %130, !llvm.loop !21

183:                                              ; preds = %130
  br label %184

184:                                              ; preds = %183
  %185 = load i32, ptr %28, align 4
  %186 = add nsw i32 %185, 1
  store i32 %186, ptr %28, align 4
  br label %125, !llvm.loop !22

187:                                              ; preds = %125
  store i32 0, ptr %31, align 4
  br label %188

188:                                              ; preds = %247, %187
  %189 = load i32, ptr %31, align 4
  %190 = load i32, ptr %13, align 4
  %191 = icmp slt i32 %189, %190
  br i1 %191, label %192, label %250

192:                                              ; preds = %188
  store i32 0, ptr %32, align 4
  br label %193

193:                                              ; preds = %243, %192
  %194 = load i32, ptr %32, align 4
  %195 = load i32, ptr %16, align 4
  %196 = icmp slt i32 %194, %195
  br i1 %196, label %197, label %246

197:                                              ; preds = %193
  %198 = load ptr, ptr %24, align 8
  %199 = load i32, ptr %31, align 4
  %200 = sext i32 %199 to i64
  %201 = mul nsw i64 %200, %61
  %202 = getelementptr inbounds double, ptr %198, i64 %201
  %203 = load i32, ptr %32, align 4
  %204 = sext i32 %203 to i64
  %205 = getelementptr inbounds double, ptr %202, i64 %204
  store double 0.000000e+00, ptr %205, align 8
  store i32 0, ptr %33, align 4
  br label %206

206:                                              ; preds = %239, %197
  %207 = load i32, ptr %33, align 4
  %208 = load i32, ptr %14, align 4
  %209 = icmp slt i32 %207, %208
  br i1 %209, label %210, label %242

210:                                              ; preds = %206
  %211 = load ptr, ptr %18, align 8
  %212 = load i32, ptr %31, align 4
  %213 = sext i32 %212 to i64
  %214 = mul nsw i64 %213, %37
  %215 = getelementptr inbounds double, ptr %211, i64 %214
  %216 = load i32, ptr %33, align 4
  %217 = sext i32 %216 to i64
  %218 = getelementptr inbounds double, ptr %215, i64 %217
  %219 = load double, ptr %218, align 8
  %220 = load ptr, ptr %21, align 8
  %221 = load i32, ptr %33, align 4
  %222 = sext i32 %221 to i64
  %223 = mul nsw i64 %222, %49
  %224 = getelementptr inbounds double, ptr %220, i64 %223
  %225 = load i32, ptr %32, align 4
  %226 = sext i32 %225 to i64
  %227 = getelementptr inbounds double, ptr %224, i64 %226
  %228 = load double, ptr %227, align 8
  %229 = load ptr, ptr %24, align 8
  %230 = load i32, ptr %31, align 4
  %231 = sext i32 %230 to i64
  %232 = mul nsw i64 %231, %61
  %233 = getelementptr inbounds double, ptr %229, i64 %232
  %234 = load i32, ptr %32, align 4
  %235 = sext i32 %234 to i64
  %236 = getelementptr inbounds double, ptr %233, i64 %235
  %237 = load double, ptr %236, align 8
  %238 = call double @llvm.fmuladd.f64(double %219, double %228, double %237)
  store double %238, ptr %236, align 8
  br label %239

239:                                              ; preds = %210
  %240 = load i32, ptr %33, align 4
  %241 = add nsw i32 %240, 1
  store i32 %241, ptr %33, align 4
  br label %206, !llvm.loop !23

242:                                              ; preds = %206
  br label %243

243:                                              ; preds = %242
  %244 = load i32, ptr %32, align 4
  %245 = add nsw i32 %244, 1
  store i32 %245, ptr %32, align 4
  br label %193, !llvm.loop !24

246:                                              ; preds = %193
  br label %247

247:                                              ; preds = %246
  %248 = load i32, ptr %31, align 4
  %249 = add nsw i32 %248, 1
  store i32 %249, ptr %31, align 4
  br label %188, !llvm.loop !25

250:                                              ; preds = %188
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca ptr, align 8
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 128, ptr %2, align 4
  store i32 128, ptr %3, align 4
  store i32 128, ptr %4, align 4
  store i32 128, ptr %5, align 4
  store i32 128, ptr %6, align 4
  %16 = load i32, ptr %4, align 4
  %17 = zext i32 %16 to i64
  %18 = load i32, ptr %2, align 4
  %19 = zext i32 %18 to i64
  %20 = load i32, ptr %4, align 4
  %21 = zext i32 %20 to i64
  %22 = mul nuw i64 %19, %21
  %23 = mul nuw i64 8, %22
  %24 = call ptr @malloc(i64 noundef %23) #4
  store ptr %24, ptr %7, align 8
  %25 = load i32, ptr %3, align 4
  %26 = zext i32 %25 to i64
  %27 = load i32, ptr %4, align 4
  %28 = zext i32 %27 to i64
  %29 = load i32, ptr %3, align 4
  %30 = zext i32 %29 to i64
  %31 = mul nuw i64 %28, %30
  %32 = mul nuw i64 8, %31
  %33 = call ptr @malloc(i64 noundef %32) #4
  store ptr %33, ptr %8, align 8
  %34 = load i32, ptr %6, align 4
  %35 = zext i32 %34 to i64
  %36 = load i32, ptr %3, align 4
  %37 = zext i32 %36 to i64
  %38 = load i32, ptr %6, align 4
  %39 = zext i32 %38 to i64
  %40 = mul nuw i64 %37, %39
  %41 = mul nuw i64 8, %40
  %42 = call ptr @malloc(i64 noundef %41) #4
  store ptr %42, ptr %9, align 8
  %43 = load i32, ptr %5, align 4
  %44 = zext i32 %43 to i64
  %45 = load i32, ptr %6, align 4
  %46 = zext i32 %45 to i64
  %47 = load i32, ptr %5, align 4
  %48 = zext i32 %47 to i64
  %49 = mul nuw i64 %46, %48
  %50 = mul nuw i64 8, %49
  %51 = call ptr @malloc(i64 noundef %50) #4
  store ptr %51, ptr %10, align 8
  %52 = load i32, ptr %3, align 4
  %53 = zext i32 %52 to i64
  %54 = load i32, ptr %2, align 4
  %55 = zext i32 %54 to i64
  %56 = load i32, ptr %3, align 4
  %57 = zext i32 %56 to i64
  %58 = mul nuw i64 %55, %57
  %59 = mul nuw i64 8, %58
  %60 = call ptr @malloc(i64 noundef %59) #4
  store ptr %60, ptr %11, align 8
  %61 = load i32, ptr %5, align 4
  %62 = zext i32 %61 to i64
  %63 = load i32, ptr %3, align 4
  %64 = zext i32 %63 to i64
  %65 = load i32, ptr %5, align 4
  %66 = zext i32 %65 to i64
  %67 = mul nuw i64 %64, %66
  %68 = mul nuw i64 8, %67
  %69 = call ptr @malloc(i64 noundef %68) #4
  store ptr %69, ptr %12, align 8
  %70 = load i32, ptr %5, align 4
  %71 = zext i32 %70 to i64
  %72 = load i32, ptr %2, align 4
  %73 = zext i32 %72 to i64
  %74 = load i32, ptr %5, align 4
  %75 = zext i32 %74 to i64
  %76 = mul nuw i64 %73, %75
  %77 = mul nuw i64 8, %76
  %78 = call ptr @malloc(i64 noundef %77) #4
  store ptr %78, ptr %13, align 8
  %79 = load i32, ptr %2, align 4
  %80 = load i32, ptr %3, align 4
  %81 = load i32, ptr %4, align 4
  %82 = load i32, ptr %5, align 4
  %83 = load i32, ptr %6, align 4
  %84 = load ptr, ptr %7, align 8
  %85 = load ptr, ptr %8, align 8
  %86 = load ptr, ptr %9, align 8
  %87 = load ptr, ptr %10, align 8
  call void @init_array(i32 noundef %79, i32 noundef %80, i32 noundef %81, i32 noundef %82, i32 noundef %83, ptr noundef %84, ptr noundef %85, ptr noundef %86, ptr noundef %87)
  %88 = call i32 @clock()
  store i32 %88, ptr %14, align 4
  %89 = load i32, ptr %2, align 4
  %90 = load i32, ptr %3, align 4
  %91 = load i32, ptr %4, align 4
  %92 = load i32, ptr %5, align 4
  %93 = load i32, ptr %6, align 4
  %94 = load ptr, ptr %11, align 8
  %95 = load ptr, ptr %7, align 8
  %96 = load ptr, ptr %8, align 8
  %97 = load ptr, ptr %12, align 8
  %98 = load ptr, ptr %9, align 8
  %99 = load ptr, ptr %10, align 8
  %100 = load ptr, ptr %13, align 8
  call void @mm3(i32 noundef %89, i32 noundef %90, i32 noundef %91, i32 noundef %92, i32 noundef %93, ptr noundef %94, ptr noundef %95, ptr noundef %96, ptr noundef %97, ptr noundef %98, ptr noundef %99, ptr noundef %100)
  %101 = call i32 @clock()
  store i32 %101, ptr %15, align 4
  %102 = load i32, ptr %15, align 4
  %103 = load i32, ptr %14, align 4
  %104 = sub nsw i32 %102, %103
  %105 = sitofp i32 %104 to double
  %106 = fdiv double %105, 1.000000e+03
  %107 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str, double noundef %106)
  %108 = load ptr, ptr %13, align 8
  %109 = mul nsw i64 0, %71
  %110 = getelementptr inbounds double, ptr %108, i64 %109
  %111 = getelementptr inbounds double, ptr %110, i64 0
  %112 = load double, ptr %111, align 8
  %113 = call i32 (ptr, ...) @__mingw_printf(ptr noundef @.str.1, double noundef %112)
  %114 = load ptr, ptr %7, align 8
  call void @free(ptr noundef %114)
  %115 = load ptr, ptr %8, align 8
  call void @free(ptr noundef %115)
  %116 = load ptr, ptr %9, align 8
  call void @free(ptr noundef %116)
  %117 = load ptr, ptr %10, align 8
  call void @free(ptr noundef %117)
  %118 = load ptr, ptr %11, align 8
  call void @free(ptr noundef %118)
  %119 = load ptr, ptr %12, align 8
  call void @free(ptr noundef %119)
  %120 = load ptr, ptr %13, align 8
  call void @free(ptr noundef %120)
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
!1 = !DIFile(filename: "benchmarks/3mm.c", directory: "C:/Users/ultim/compiler-opt")
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
!20 = distinct !{!20, !9}
!21 = distinct !{!21, !9}
!22 = distinct !{!22, !9}
!23 = distinct !{!23, !9}
!24 = distinct !{!24, !9}
!25 = distinct !{!25, !9}
