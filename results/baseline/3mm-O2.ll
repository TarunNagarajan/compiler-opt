; ModuleID = 'results\baseline\3mm_base.ll'
source_filename = "benchmarks\\3mm.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [26 x i8] c"3MM Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, i32 noundef %4, ptr noundef writeonly captures(none) %5, ptr noundef writeonly captures(none) %6, ptr noundef writeonly captures(none) %7, ptr noundef writeonly captures(none) %8) local_unnamed_addr #0 {
  %10 = zext i32 %2 to i64
  %11 = zext i32 %1 to i64
  %12 = zext i32 %4 to i64
  %13 = zext i32 %3 to i64
  %14 = icmp sgt i32 %0, 0
  br i1 %14, label %.preheader75.lr.ph, label %.preheader74

.preheader75.lr.ph:                               ; preds = %9
  %15 = icmp sgt i32 %2, 0
  %16 = uitofp nneg i32 %0 to double
  %wide.trip.count95 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %10, 1
  %17 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %10, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader75

.preheader75:                                     ; preds = %.preheader75.lr.ph, %._crit_edge
  %indvars.iv92 = phi i64 [ 0, %.preheader75.lr.ph ], [ %indvars.iv.next93, %._crit_edge ]
  br i1 %15, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader75
  %18 = mul nuw nsw i64 %indvars.iv92, %10
  %19 = getelementptr inbounds nuw double, ptr %5, i64 %18
  br i1 %17, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.preheader74:                                     ; preds = %._crit_edge, %9
  %20 = icmp sgt i32 %2, 0
  br i1 %20, label %.preheader73.lr.ph, label %.preheader72

.preheader73.lr.ph:                               ; preds = %.preheader74
  %21 = icmp sgt i32 %1, 0
  %22 = sitofp i32 %1 to double
  %xtraiter128 = and i64 %11, 1
  %23 = icmp eq i32 %1, 1
  %unroll_iter130 = and i64 %11, 2147483646
  %lcmp.mod129.not = icmp eq i64 %xtraiter128, 0
  br label %.preheader73

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %24 = mul nuw nsw i64 %indvars.iv, %indvars.iv92
  %25 = trunc i64 %24 to i32
  %26 = or disjoint i32 %25, 1
  %27 = urem i32 %26, %0
  %28 = uitofp nneg i32 %27 to double
  %29 = fdiv double %28, %16
  %30 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv
  store double %29, ptr %30, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %31 = mul nuw nsw i64 %indvars.iv.next, %indvars.iv92
  %32 = trunc i64 %31 to i32
  %33 = add i32 %32, 1
  %34 = urem i32 %33, %0
  %35 = uitofp nneg i32 %34 to double
  %36 = fdiv double %35, %16
  %37 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv.next
  store double %36, ptr %37, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !8

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.loopexit.epilog-lcssa

._crit_edge.loopexit.epilog-lcssa:                ; preds = %._crit_edge.loopexit.unr-lcssa
  %38 = mul nuw nsw i64 %indvars.iv.unr, %indvars.iv92
  %39 = trunc i64 %38 to i32
  %40 = add i32 %39, 1
  %41 = urem i32 %40, %0
  %42 = uitofp nneg i32 %41 to double
  %43 = fdiv double %42, %16
  %44 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv.unr
  store double %43, ptr %44, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.loopexit.epilog-lcssa, %._crit_edge.loopexit.unr-lcssa, %.preheader75
  %indvars.iv.next93 = add nuw nsw i64 %indvars.iv92, 1
  %exitcond96.not = icmp eq i64 %indvars.iv.next93, %wide.trip.count95
  br i1 %exitcond96.not, label %.preheader74, label %.preheader75, !llvm.loop !10

.preheader73:                                     ; preds = %.preheader73.lr.ph, %._crit_edge80
  %indvars.iv102 = phi i64 [ 0, %.preheader73.lr.ph ], [ %indvars.iv.next103, %._crit_edge80 ]
  br i1 %21, label %.lr.ph79, label %._crit_edge80

.lr.ph79:                                         ; preds = %.preheader73
  %45 = mul nuw nsw i64 %indvars.iv102, %11
  %46 = getelementptr inbounds nuw double, ptr %6, i64 %45
  br i1 %23, label %._crit_edge80.loopexit.unr-lcssa, label %.lr.ph79.new

.preheader72:                                     ; preds = %._crit_edge80, %.preheader74
  %47 = icmp sgt i32 %1, 0
  br i1 %47, label %.preheader71.lr.ph, label %.preheader70

.preheader71.lr.ph:                               ; preds = %.preheader72
  %48 = icmp sgt i32 %4, 0
  %49 = sitofp i32 %4 to double
  %xtraiter133 = and i64 %12, 1
  %50 = icmp eq i32 %4, 1
  %unroll_iter135 = and i64 %12, 2147483646
  %lcmp.mod134.not = icmp eq i64 %xtraiter133, 0
  br label %.preheader71

.lr.ph79.new:                                     ; preds = %.lr.ph79, %.lr.ph79.new
  %indvars.iv97 = phi i64 [ %indvars.iv.next98.1, %.lr.ph79.new ], [ 0, %.lr.ph79 ]
  %niter131 = phi i64 [ %niter131.next.1, %.lr.ph79.new ], [ 0, %.lr.ph79 ]
  %indvars.iv.next98 = or disjoint i64 %indvars.iv97, 1
  %51 = mul nuw nsw i64 %indvars.iv.next98, %indvars.iv102
  %52 = trunc i64 %51 to i32
  %53 = add i32 %52, 2
  %54 = urem i32 %53, %1
  %55 = uitofp nneg i32 %54 to double
  %56 = fdiv double %55, %22
  %57 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv97
  store double %56, ptr %57, align 8
  %indvars.iv.next98.1 = add nuw nsw i64 %indvars.iv97, 2
  %58 = mul nuw nsw i64 %indvars.iv.next98.1, %indvars.iv102
  %59 = trunc i64 %58 to i32
  %60 = add i32 %59, 2
  %61 = urem i32 %60, %1
  %62 = uitofp nneg i32 %61 to double
  %63 = fdiv double %62, %22
  %64 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv.next98
  store double %63, ptr %64, align 8
  %niter131.next.1 = add i64 %niter131, 2
  %niter131.ncmp.1 = icmp eq i64 %niter131.next.1, %unroll_iter130
  br i1 %niter131.ncmp.1, label %._crit_edge80.loopexit.unr-lcssa, label %.lr.ph79.new, !llvm.loop !11

._crit_edge80.loopexit.unr-lcssa:                 ; preds = %.lr.ph79.new, %.lr.ph79
  %indvars.iv97.unr = phi i64 [ 0, %.lr.ph79 ], [ %indvars.iv.next98.1, %.lr.ph79.new ]
  br i1 %lcmp.mod129.not, label %._crit_edge80, label %._crit_edge80.loopexit.epilog-lcssa

._crit_edge80.loopexit.epilog-lcssa:              ; preds = %._crit_edge80.loopexit.unr-lcssa
  %indvars.iv.next98.epil = add nuw nsw i64 %indvars.iv97.unr, 1
  %65 = mul nuw nsw i64 %indvars.iv.next98.epil, %indvars.iv102
  %66 = trunc i64 %65 to i32
  %67 = add i32 %66, 2
  %68 = urem i32 %67, %1
  %69 = uitofp nneg i32 %68 to double
  %70 = fdiv double %69, %22
  %71 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv97.unr
  store double %70, ptr %71, align 8
  br label %._crit_edge80

._crit_edge80:                                    ; preds = %._crit_edge80.loopexit.epilog-lcssa, %._crit_edge80.loopexit.unr-lcssa, %.preheader73
  %indvars.iv.next103 = add nuw nsw i64 %indvars.iv102, 1
  %exitcond106.not = icmp eq i64 %indvars.iv.next103, %10
  br i1 %exitcond106.not, label %.preheader72, label %.preheader73, !llvm.loop !12

.preheader71:                                     ; preds = %.preheader71.lr.ph, %._crit_edge84
  %indvars.iv112 = phi i64 [ 0, %.preheader71.lr.ph ], [ %indvars.iv.next113, %._crit_edge84 ]
  br i1 %48, label %.lr.ph83, label %._crit_edge84

.lr.ph83:                                         ; preds = %.preheader71
  %72 = mul nuw nsw i64 %indvars.iv112, %12
  %73 = getelementptr inbounds nuw double, ptr %7, i64 %72
  br i1 %50, label %._crit_edge84.loopexit.unr-lcssa, label %.lr.ph83.new

.lr.ph83.new:                                     ; preds = %.lr.ph83
  %invariant.gep = getelementptr inbounds i8, ptr %73, i64 8
  br label %78

.preheader70:                                     ; preds = %._crit_edge84, %.preheader72
  %74 = icmp sgt i32 %4, 0
  br i1 %74, label %.preheader.lr.ph, label %._crit_edge90

.preheader.lr.ph:                                 ; preds = %.preheader70
  %75 = icmp sgt i32 %3, 0
  %76 = sitofp i32 %3 to double
  %xtraiter138 = and i64 %13, 1
  %77 = icmp eq i32 %3, 1
  %unroll_iter140 = and i64 %13, 2147483646
  %lcmp.mod139.not = icmp eq i64 %xtraiter138, 0
  br label %.preheader

78:                                               ; preds = %78, %.lr.ph83.new
  %indvars.iv107 = phi i64 [ 0, %.lr.ph83.new ], [ %indvars.iv.next108.1, %78 ]
  %niter136 = phi i64 [ 0, %.lr.ph83.new ], [ %niter136.next.1, %78 ]
  %79 = add nuw nsw i64 %indvars.iv107, 3
  %80 = mul nuw nsw i64 %79, %indvars.iv112
  %81 = trunc nuw i64 %80 to i32
  %82 = urem i32 %81, %4
  %83 = uitofp nneg i32 %82 to double
  %84 = fdiv double %83, %49
  %85 = getelementptr inbounds nuw double, ptr %73, i64 %indvars.iv107
  store double %84, ptr %85, align 8
  %86 = add nuw nsw i64 %indvars.iv107, 4
  %87 = mul nuw nsw i64 %86, %indvars.iv112
  %88 = trunc nuw i64 %87 to i32
  %89 = urem i32 %88, %4
  %90 = uitofp nneg i32 %89 to double
  %91 = fdiv double %90, %49
  %gep = getelementptr inbounds double, ptr %invariant.gep, i64 %indvars.iv107
  store double %91, ptr %gep, align 8
  %indvars.iv.next108.1 = add nuw nsw i64 %indvars.iv107, 2
  %niter136.next.1 = add i64 %niter136, 2
  %niter136.ncmp.1 = icmp eq i64 %niter136.next.1, %unroll_iter135
  br i1 %niter136.ncmp.1, label %._crit_edge84.loopexit.unr-lcssa, label %78, !llvm.loop !13

._crit_edge84.loopexit.unr-lcssa:                 ; preds = %78, %.lr.ph83
  %indvars.iv107.unr = phi i64 [ 0, %.lr.ph83 ], [ %indvars.iv.next108.1, %78 ]
  br i1 %lcmp.mod134.not, label %._crit_edge84, label %._crit_edge84.loopexit.epilog-lcssa

._crit_edge84.loopexit.epilog-lcssa:              ; preds = %._crit_edge84.loopexit.unr-lcssa
  %92 = add nuw nsw i64 %indvars.iv107.unr, 3
  %93 = mul nuw nsw i64 %92, %indvars.iv112
  %94 = trunc nuw i64 %93 to i32
  %95 = urem i32 %94, %4
  %96 = uitofp nneg i32 %95 to double
  %97 = fdiv double %96, %49
  %98 = getelementptr inbounds nuw double, ptr %73, i64 %indvars.iv107.unr
  store double %97, ptr %98, align 8
  br label %._crit_edge84

._crit_edge84:                                    ; preds = %._crit_edge84.loopexit.epilog-lcssa, %._crit_edge84.loopexit.unr-lcssa, %.preheader71
  %indvars.iv.next113 = add nuw nsw i64 %indvars.iv112, 1
  %exitcond116.not = icmp eq i64 %indvars.iv.next113, %11
  br i1 %exitcond116.not, label %.preheader70, label %.preheader71, !llvm.loop !14

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge88
  %indvars.iv122 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next123, %._crit_edge88 ]
  br i1 %75, label %.lr.ph87, label %._crit_edge88

.lr.ph87:                                         ; preds = %.preheader
  %99 = mul nuw nsw i64 %indvars.iv122, %13
  %100 = getelementptr inbounds nuw double, ptr %8, i64 %99
  br i1 %77, label %._crit_edge88.loopexit.unr-lcssa, label %.lr.ph87.new

.lr.ph87.new:                                     ; preds = %.lr.ph87
  %invariant.gep142 = getelementptr inbounds i8, ptr %100, i64 8
  br label %101

101:                                              ; preds = %101, %.lr.ph87.new
  %indvars.iv117 = phi i64 [ 0, %.lr.ph87.new ], [ %indvars.iv.next118.1, %101 ]
  %niter141 = phi i64 [ 0, %.lr.ph87.new ], [ %niter141.next.1, %101 ]
  %102 = add nuw nsw i64 %indvars.iv117, 2
  %103 = mul nuw nsw i64 %102, %indvars.iv122
  %104 = trunc i64 %103 to i32
  %105 = add i32 %104, 2
  %106 = urem i32 %105, %3
  %107 = uitofp nneg i32 %106 to double
  %108 = fdiv double %107, %76
  %109 = getelementptr inbounds nuw double, ptr %100, i64 %indvars.iv117
  store double %108, ptr %109, align 8
  %110 = add nuw nsw i64 %indvars.iv117, 3
  %111 = mul nuw nsw i64 %110, %indvars.iv122
  %112 = trunc i64 %111 to i32
  %113 = add i32 %112, 2
  %114 = urem i32 %113, %3
  %115 = uitofp nneg i32 %114 to double
  %116 = fdiv double %115, %76
  %gep143 = getelementptr inbounds double, ptr %invariant.gep142, i64 %indvars.iv117
  store double %116, ptr %gep143, align 8
  %indvars.iv.next118.1 = add nuw nsw i64 %indvars.iv117, 2
  %niter141.next.1 = add i64 %niter141, 2
  %niter141.ncmp.1 = icmp eq i64 %niter141.next.1, %unroll_iter140
  br i1 %niter141.ncmp.1, label %._crit_edge88.loopexit.unr-lcssa, label %101, !llvm.loop !15

._crit_edge88.loopexit.unr-lcssa:                 ; preds = %101, %.lr.ph87
  %indvars.iv117.unr = phi i64 [ 0, %.lr.ph87 ], [ %indvars.iv.next118.1, %101 ]
  br i1 %lcmp.mod139.not, label %._crit_edge88, label %._crit_edge88.loopexit.epilog-lcssa

._crit_edge88.loopexit.epilog-lcssa:              ; preds = %._crit_edge88.loopexit.unr-lcssa
  %117 = add nuw nsw i64 %indvars.iv117.unr, 2
  %118 = mul nuw nsw i64 %117, %indvars.iv122
  %119 = trunc i64 %118 to i32
  %120 = add i32 %119, 2
  %121 = urem i32 %120, %3
  %122 = uitofp nneg i32 %121 to double
  %123 = fdiv double %122, %76
  %124 = getelementptr inbounds nuw double, ptr %100, i64 %indvars.iv117.unr
  store double %123, ptr %124, align 8
  br label %._crit_edge88

._crit_edge88:                                    ; preds = %._crit_edge88.loopexit.epilog-lcssa, %._crit_edge88.loopexit.unr-lcssa, %.preheader
  %indvars.iv.next123 = add nuw nsw i64 %indvars.iv122, 1
  %exitcond126.not = icmp eq i64 %indvars.iv.next123, %12
  br i1 %exitcond126.not, label %._crit_edge90, label %.preheader, !llvm.loop !16

._crit_edge90:                                    ; preds = %._crit_edge88, %.preheader70
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @mm3(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, i32 noundef %4, ptr noundef captures(none) %5, ptr noundef readonly captures(none) %6, ptr noundef readonly captures(none) %7, ptr noundef captures(none) %8, ptr noundef readonly captures(none) %9, ptr noundef readonly captures(none) %10, ptr noundef writeonly captures(none) %11) local_unnamed_addr #1 {
  %13 = zext i32 %1 to i64
  %14 = zext i32 %2 to i64
  %15 = zext i32 %3 to i64
  %16 = zext i32 %4 to i64
  %17 = icmp sgt i32 %0, 0
  br i1 %17, label %.preheader89.lr.ph, label %.preheader88

.preheader89.lr.ph:                               ; preds = %12
  %18 = icmp sgt i32 %1, 0
  %19 = icmp sgt i32 %2, 0
  %wide.trip.count127 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %14, 1
  %20 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %14, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader89

.preheader89:                                     ; preds = %.preheader89.lr.ph, %._crit_edge93
  %indvars.iv124 = phi i64 [ 0, %.preheader89.lr.ph ], [ %indvars.iv.next125, %._crit_edge93 ]
  br i1 %18, label %.lr.ph92, label %._crit_edge93

.lr.ph92:                                         ; preds = %.preheader89
  %21 = mul nuw nsw i64 %indvars.iv124, %13
  %22 = getelementptr inbounds nuw double, ptr %5, i64 %21
  %23 = mul nuw nsw i64 %indvars.iv124, %14
  %24 = getelementptr inbounds nuw double, ptr %6, i64 %23
  br label %29

.preheader88:                                     ; preds = %._crit_edge93, %12
  %25 = icmp sgt i32 %1, 0
  br i1 %25, label %.preheader87.lr.ph, label %.preheader86

.preheader87.lr.ph:                               ; preds = %.preheader88
  %26 = icmp sgt i32 %3, 0
  %27 = icmp sgt i32 %4, 0
  %xtraiter159 = and i64 %16, 1
  %28 = icmp eq i32 %4, 1
  %unroll_iter162 = and i64 %16, 2147483646
  %lcmp.mod161.not = icmp eq i64 %xtraiter159, 0
  br label %.preheader87

29:                                               ; preds = %.lr.ph92, %._crit_edge
  %indvars.iv119 = phi i64 [ 0, %.lr.ph92 ], [ %indvars.iv.next120, %._crit_edge ]
  %30 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv119
  store double 0.000000e+00, ptr %30, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %7, i64 %indvars.iv119
  br i1 %19, label %.lr.ph.preheader, label %._crit_edge

.lr.ph.preheader:                                 ; preds = %29
  br i1 %20, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph

.lr.ph:                                           ; preds = %.lr.ph.preheader, %.lr.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph ], [ 0, %.lr.ph.preheader ]
  %31 = phi double [ %41, %.lr.ph ], [ 0.000000e+00, %.lr.ph.preheader ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph ], [ 0, %.lr.ph.preheader ]
  %32 = getelementptr inbounds nuw double, ptr %24, i64 %indvars.iv
  %33 = load double, ptr %32, align 8
  %34 = mul nuw nsw i64 %indvars.iv, %13
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %34
  %35 = load double, ptr %gep, align 8
  %36 = tail call double @llvm.fmuladd.f64(double %33, double %35, double %31)
  store double %36, ptr %30, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %37 = getelementptr inbounds nuw double, ptr %24, i64 %indvars.iv.next
  %38 = load double, ptr %37, align 8
  %39 = mul nuw nsw i64 %indvars.iv.next, %13
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %39
  %40 = load double, ptr %gep.1, align 8
  %41 = tail call double @llvm.fmuladd.f64(double %38, double %40, double %36)
  store double %41, ptr %30, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph, !llvm.loop !17

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph, %.lr.ph.preheader
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph.preheader ], [ %indvars.iv.next.1, %.lr.ph ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph.preheader ], [ %41, %.lr.ph ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %.lr.ph.epil

.lr.ph.epil:                                      ; preds = %._crit_edge.loopexit.unr-lcssa
  %42 = getelementptr inbounds nuw double, ptr %24, i64 %indvars.iv.unr
  %43 = load double, ptr %42, align 8
  %44 = mul nuw nsw i64 %indvars.iv.unr, %13
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %44
  %45 = load double, ptr %gep.epil, align 8
  %46 = tail call double @llvm.fmuladd.f64(double %43, double %45, double %.unr)
  store double %46, ptr %30, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %.lr.ph.epil, %._crit_edge.loopexit.unr-lcssa, %29
  %indvars.iv.next120 = add nuw nsw i64 %indvars.iv119, 1
  %exitcond123.not = icmp eq i64 %indvars.iv.next120, %13
  br i1 %exitcond123.not, label %._crit_edge93, label %29, !llvm.loop !18

._crit_edge93:                                    ; preds = %._crit_edge, %.preheader89
  %indvars.iv.next125 = add nuw nsw i64 %indvars.iv124, 1
  %exitcond128.not = icmp eq i64 %indvars.iv.next125, %wide.trip.count127
  br i1 %exitcond128.not, label %.preheader88, label %.preheader89, !llvm.loop !19

.preheader87:                                     ; preds = %.preheader87.lr.ph, %._crit_edge104
  %indvars.iv139 = phi i64 [ 0, %.preheader87.lr.ph ], [ %indvars.iv.next140, %._crit_edge104 ]
  br i1 %26, label %.lr.ph103, label %._crit_edge104

.lr.ph103:                                        ; preds = %.preheader87
  %47 = mul nuw nsw i64 %indvars.iv139, %15
  %48 = getelementptr inbounds nuw double, ptr %8, i64 %47
  %49 = mul nuw nsw i64 %indvars.iv139, %16
  %50 = getelementptr inbounds nuw double, ptr %9, i64 %49
  br label %53

.preheader86:                                     ; preds = %._crit_edge104, %.preheader88
  br i1 %17, label %.preheader.lr.ph, label %._crit_edge117

.preheader.lr.ph:                                 ; preds = %.preheader86
  %51 = icmp sgt i32 %3, 0
  %wide.trip.count157 = zext nneg i32 %0 to i64
  %xtraiter164 = and i64 %13, 1
  %52 = icmp eq i32 %1, 1
  %unroll_iter167 = and i64 %13, 2147483646
  %lcmp.mod166.not = icmp eq i64 %xtraiter164, 0
  br label %.preheader

53:                                               ; preds = %.lr.ph103, %._crit_edge100
  %indvars.iv134 = phi i64 [ 0, %.lr.ph103 ], [ %indvars.iv.next135, %._crit_edge100 ]
  %54 = getelementptr inbounds nuw double, ptr %48, i64 %indvars.iv134
  store double 0.000000e+00, ptr %54, align 8
  %invariant.gep95 = getelementptr inbounds nuw double, ptr %10, i64 %indvars.iv134
  br i1 %27, label %.lr.ph99.preheader, label %._crit_edge100

.lr.ph99.preheader:                               ; preds = %53
  br i1 %28, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99

.lr.ph99:                                         ; preds = %.lr.ph99.preheader, %.lr.ph99
  %indvars.iv129 = phi i64 [ %indvars.iv.next130.1, %.lr.ph99 ], [ 0, %.lr.ph99.preheader ]
  %55 = phi double [ %65, %.lr.ph99 ], [ 0.000000e+00, %.lr.ph99.preheader ]
  %niter163 = phi i64 [ %niter163.next.1, %.lr.ph99 ], [ 0, %.lr.ph99.preheader ]
  %56 = getelementptr inbounds nuw double, ptr %50, i64 %indvars.iv129
  %57 = load double, ptr %56, align 8
  %58 = mul nuw nsw i64 %indvars.iv129, %15
  %gep96 = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %58
  %59 = load double, ptr %gep96, align 8
  %60 = tail call double @llvm.fmuladd.f64(double %57, double %59, double %55)
  store double %60, ptr %54, align 8
  %indvars.iv.next130 = or disjoint i64 %indvars.iv129, 1
  %61 = getelementptr inbounds nuw double, ptr %50, i64 %indvars.iv.next130
  %62 = load double, ptr %61, align 8
  %63 = mul nuw nsw i64 %indvars.iv.next130, %15
  %gep96.1 = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %63
  %64 = load double, ptr %gep96.1, align 8
  %65 = tail call double @llvm.fmuladd.f64(double %62, double %64, double %60)
  store double %65, ptr %54, align 8
  %indvars.iv.next130.1 = add nuw nsw i64 %indvars.iv129, 2
  %niter163.next.1 = add i64 %niter163, 2
  %niter163.ncmp.1 = icmp eq i64 %niter163.next.1, %unroll_iter162
  br i1 %niter163.ncmp.1, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99, !llvm.loop !20

._crit_edge100.loopexit.unr-lcssa:                ; preds = %.lr.ph99, %.lr.ph99.preheader
  %indvars.iv129.unr = phi i64 [ 0, %.lr.ph99.preheader ], [ %indvars.iv.next130.1, %.lr.ph99 ]
  %.unr160 = phi double [ 0.000000e+00, %.lr.ph99.preheader ], [ %65, %.lr.ph99 ]
  br i1 %lcmp.mod161.not, label %._crit_edge100, label %.lr.ph99.epil

.lr.ph99.epil:                                    ; preds = %._crit_edge100.loopexit.unr-lcssa
  %66 = getelementptr inbounds nuw double, ptr %50, i64 %indvars.iv129.unr
  %67 = load double, ptr %66, align 8
  %68 = mul nuw nsw i64 %indvars.iv129.unr, %15
  %gep96.epil = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %68
  %69 = load double, ptr %gep96.epil, align 8
  %70 = tail call double @llvm.fmuladd.f64(double %67, double %69, double %.unr160)
  store double %70, ptr %54, align 8
  br label %._crit_edge100

._crit_edge100:                                   ; preds = %.lr.ph99.epil, %._crit_edge100.loopexit.unr-lcssa, %53
  %indvars.iv.next135 = add nuw nsw i64 %indvars.iv134, 1
  %exitcond138.not = icmp eq i64 %indvars.iv.next135, %15
  br i1 %exitcond138.not, label %._crit_edge104, label %53, !llvm.loop !21

._crit_edge104:                                   ; preds = %._crit_edge100, %.preheader87
  %indvars.iv.next140 = add nuw nsw i64 %indvars.iv139, 1
  %exitcond143.not = icmp eq i64 %indvars.iv.next140, %13
  br i1 %exitcond143.not, label %.preheader86, label %.preheader87, !llvm.loop !22

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge115
  %indvars.iv154 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next155, %._crit_edge115 ]
  br i1 %51, label %.lr.ph114, label %._crit_edge115

.lr.ph114:                                        ; preds = %.preheader
  %71 = mul nuw nsw i64 %indvars.iv154, %15
  %72 = getelementptr inbounds nuw double, ptr %11, i64 %71
  %73 = mul nuw nsw i64 %indvars.iv154, %13
  %74 = getelementptr inbounds nuw double, ptr %5, i64 %73
  br label %75

75:                                               ; preds = %.lr.ph114, %._crit_edge111
  %indvars.iv149 = phi i64 [ 0, %.lr.ph114 ], [ %indvars.iv.next150, %._crit_edge111 ]
  %76 = getelementptr inbounds nuw double, ptr %72, i64 %indvars.iv149
  store double 0.000000e+00, ptr %76, align 8
  %invariant.gep106 = getelementptr inbounds nuw double, ptr %8, i64 %indvars.iv149
  br i1 %25, label %.lr.ph110.preheader, label %._crit_edge111

.lr.ph110.preheader:                              ; preds = %75
  br i1 %52, label %._crit_edge111.loopexit.unr-lcssa, label %.lr.ph110

.lr.ph110:                                        ; preds = %.lr.ph110.preheader, %.lr.ph110
  %indvars.iv144 = phi i64 [ %indvars.iv.next145.1, %.lr.ph110 ], [ 0, %.lr.ph110.preheader ]
  %77 = phi double [ %87, %.lr.ph110 ], [ 0.000000e+00, %.lr.ph110.preheader ]
  %niter168 = phi i64 [ %niter168.next.1, %.lr.ph110 ], [ 0, %.lr.ph110.preheader ]
  %78 = getelementptr inbounds nuw double, ptr %74, i64 %indvars.iv144
  %79 = load double, ptr %78, align 8
  %80 = mul nuw nsw i64 %indvars.iv144, %15
  %gep107 = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %80
  %81 = load double, ptr %gep107, align 8
  %82 = tail call double @llvm.fmuladd.f64(double %79, double %81, double %77)
  store double %82, ptr %76, align 8
  %indvars.iv.next145 = or disjoint i64 %indvars.iv144, 1
  %83 = getelementptr inbounds nuw double, ptr %74, i64 %indvars.iv.next145
  %84 = load double, ptr %83, align 8
  %85 = mul nuw nsw i64 %indvars.iv.next145, %15
  %gep107.1 = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %85
  %86 = load double, ptr %gep107.1, align 8
  %87 = tail call double @llvm.fmuladd.f64(double %84, double %86, double %82)
  store double %87, ptr %76, align 8
  %indvars.iv.next145.1 = add nuw nsw i64 %indvars.iv144, 2
  %niter168.next.1 = add i64 %niter168, 2
  %niter168.ncmp.1 = icmp eq i64 %niter168.next.1, %unroll_iter167
  br i1 %niter168.ncmp.1, label %._crit_edge111.loopexit.unr-lcssa, label %.lr.ph110, !llvm.loop !23

._crit_edge111.loopexit.unr-lcssa:                ; preds = %.lr.ph110, %.lr.ph110.preheader
  %indvars.iv144.unr = phi i64 [ 0, %.lr.ph110.preheader ], [ %indvars.iv.next145.1, %.lr.ph110 ]
  %.unr165 = phi double [ 0.000000e+00, %.lr.ph110.preheader ], [ %87, %.lr.ph110 ]
  br i1 %lcmp.mod166.not, label %._crit_edge111, label %.lr.ph110.epil

.lr.ph110.epil:                                   ; preds = %._crit_edge111.loopexit.unr-lcssa
  %88 = getelementptr inbounds nuw double, ptr %74, i64 %indvars.iv144.unr
  %89 = load double, ptr %88, align 8
  %90 = mul nuw nsw i64 %indvars.iv144.unr, %15
  %gep107.epil = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %90
  %91 = load double, ptr %gep107.epil, align 8
  %92 = tail call double @llvm.fmuladd.f64(double %89, double %91, double %.unr165)
  store double %92, ptr %76, align 8
  br label %._crit_edge111

._crit_edge111:                                   ; preds = %.lr.ph110.epil, %._crit_edge111.loopexit.unr-lcssa, %75
  %indvars.iv.next150 = add nuw nsw i64 %indvars.iv149, 1
  %exitcond153.not = icmp eq i64 %indvars.iv.next150, %15
  br i1 %exitcond153.not, label %._crit_edge115, label %75, !llvm.loop !24

._crit_edge115:                                   ; preds = %._crit_edge111, %.preheader
  %indvars.iv.next155 = add nuw nsw i64 %indvars.iv154, 1
  %exitcond158.not = icmp eq i64 %indvars.iv.next155, %wide.trip.count157
  br i1 %exitcond158.not, label %._crit_edge117, label %.preheader, !llvm.loop !25

._crit_edge117:                                   ; preds = %._crit_edge115, %.preheader86
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #3 {
  %1 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %2 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %3 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %4 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %5 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %6 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  %7 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #7
  tail call void @init_array(i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4)
  %8 = tail call i32 @clock() #8
  tail call void @mm3(i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, ptr noundef %5, ptr noundef %1, ptr noundef %2, ptr noundef %6, ptr noundef %3, ptr noundef %4, ptr noundef %7)
  %9 = tail call i32 @clock() #8
  %10 = sub nsw i32 %9, %8
  %11 = sitofp i32 %10 to double
  %12 = fdiv double %11, 1.000000e+03
  %13 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %12) #8
  %14 = load double, ptr %7, align 8
  %15 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %14) #8
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  tail call void @free(ptr noundef %4)
  tail call void @free(ptr noundef %5)
  tail call void @free(ptr noundef %6)
  tail call void @free(ptr noundef %7)
  ret i32 0
}

; Function Attrs: mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite)
declare dso_local noalias noundef ptr @malloc(i64 noundef) local_unnamed_addr #4

declare dso_local i32 @clock() local_unnamed_addr #5

declare dso_local i32 @__mingw_printf(ptr noundef, ...) local_unnamed_addr #5

; Function Attrs: mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite)
declare dso_local void @free(ptr allocptr noundef captures(none)) local_unnamed_addr #6

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { allocsize(0) }
attributes #8 = { nounwind }

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
