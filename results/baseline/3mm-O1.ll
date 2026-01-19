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
  %16 = sitofp i32 %0 to double
  %wide.trip.count95 = zext nneg i32 %0 to i64
  %17 = zext i32 %2 to i64
  %xtraiter = and i64 %17, 1
  %18 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %17, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader75

.preheader75:                                     ; preds = %.preheader75.lr.ph, %._crit_edge
  %indvars.iv92 = phi i64 [ 0, %.preheader75.lr.ph ], [ %indvars.iv.next93, %._crit_edge ]
  br i1 %15, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader75
  %19 = mul nuw nsw i64 %indvars.iv92, %10
  %20 = getelementptr inbounds nuw double, ptr %5, i64 %19
  br i1 %18, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.preheader74:                                     ; preds = %._crit_edge, %9
  %21 = icmp sgt i32 %2, 0
  br i1 %21, label %.preheader73.lr.ph, label %.preheader72

.preheader73.lr.ph:                               ; preds = %.preheader74
  %22 = icmp sgt i32 %1, 0
  %23 = sitofp i32 %1 to double
  %wide.trip.count105 = zext nneg i32 %2 to i64
  %24 = zext i32 %1 to i64
  %xtraiter128 = and i64 %24, 1
  %25 = icmp eq i32 %1, 1
  %unroll_iter130 = and i64 %24, 2147483646
  %lcmp.mod129.not = icmp eq i64 %xtraiter128, 0
  br label %.preheader73

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %26 = mul nuw nsw i64 %indvars.iv, %indvars.iv92
  %27 = trunc i64 %26 to i32
  %28 = or disjoint i32 %27, 1
  %29 = urem i32 %28, %0
  %30 = uitofp nneg i32 %29 to double
  %31 = fdiv double %30, %16
  %32 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv
  store double %31, ptr %32, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %33 = mul nuw nsw i64 %indvars.iv.next, %indvars.iv92
  %34 = trunc i64 %33 to i32
  %35 = add i32 %34, 1
  %36 = urem i32 %35, %0
  %37 = uitofp nneg i32 %36 to double
  %38 = fdiv double %37, %16
  %39 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv.next
  store double %38, ptr %39, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !8

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.loopexit.epilog-lcssa

._crit_edge.loopexit.epilog-lcssa:                ; preds = %._crit_edge.loopexit.unr-lcssa
  %40 = mul nuw nsw i64 %indvars.iv.unr, %indvars.iv92
  %41 = trunc i64 %40 to i32
  %42 = add i32 %41, 1
  %43 = urem i32 %42, %0
  %44 = uitofp nneg i32 %43 to double
  %45 = fdiv double %44, %16
  %46 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv.unr
  store double %45, ptr %46, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.loopexit.epilog-lcssa, %._crit_edge.loopexit.unr-lcssa, %.preheader75
  %indvars.iv.next93 = add nuw nsw i64 %indvars.iv92, 1
  %exitcond96.not = icmp eq i64 %indvars.iv.next93, %wide.trip.count95
  br i1 %exitcond96.not, label %.preheader74, label %.preheader75, !llvm.loop !10

.preheader73:                                     ; preds = %.preheader73.lr.ph, %._crit_edge80
  %indvars.iv102 = phi i64 [ 0, %.preheader73.lr.ph ], [ %indvars.iv.next103, %._crit_edge80 ]
  br i1 %22, label %.lr.ph79, label %._crit_edge80

.lr.ph79:                                         ; preds = %.preheader73
  %47 = mul nuw nsw i64 %indvars.iv102, %11
  %48 = getelementptr inbounds nuw double, ptr %6, i64 %47
  br i1 %25, label %._crit_edge80.loopexit.unr-lcssa, label %.lr.ph79.new

.preheader72:                                     ; preds = %._crit_edge80, %.preheader74
  %49 = icmp sgt i32 %1, 0
  br i1 %49, label %.preheader71.lr.ph, label %.preheader70

.preheader71.lr.ph:                               ; preds = %.preheader72
  %50 = icmp sgt i32 %4, 0
  %51 = sitofp i32 %4 to double
  %wide.trip.count115 = zext nneg i32 %1 to i64
  %52 = zext i32 %4 to i64
  %xtraiter133 = and i64 %52, 1
  %53 = icmp eq i32 %4, 1
  %unroll_iter135 = and i64 %52, 2147483646
  %lcmp.mod134.not = icmp eq i64 %xtraiter133, 0
  br label %.preheader71

.lr.ph79.new:                                     ; preds = %.lr.ph79, %.lr.ph79.new
  %indvars.iv97 = phi i64 [ %indvars.iv.next98.1, %.lr.ph79.new ], [ 0, %.lr.ph79 ]
  %niter131 = phi i64 [ %niter131.next.1, %.lr.ph79.new ], [ 0, %.lr.ph79 ]
  %indvars.iv.next98 = or disjoint i64 %indvars.iv97, 1
  %54 = mul nuw nsw i64 %indvars.iv.next98, %indvars.iv102
  %55 = trunc i64 %54 to i32
  %56 = add i32 %55, 2
  %57 = urem i32 %56, %1
  %58 = uitofp nneg i32 %57 to double
  %59 = fdiv double %58, %23
  %60 = getelementptr inbounds nuw double, ptr %48, i64 %indvars.iv97
  store double %59, ptr %60, align 8
  %indvars.iv.next98.1 = add nuw nsw i64 %indvars.iv97, 2
  %61 = mul nuw nsw i64 %indvars.iv.next98.1, %indvars.iv102
  %62 = trunc i64 %61 to i32
  %63 = add i32 %62, 2
  %64 = urem i32 %63, %1
  %65 = uitofp nneg i32 %64 to double
  %66 = fdiv double %65, %23
  %67 = getelementptr inbounds nuw double, ptr %48, i64 %indvars.iv.next98
  store double %66, ptr %67, align 8
  %niter131.next.1 = add i64 %niter131, 2
  %niter131.ncmp.1 = icmp eq i64 %niter131.next.1, %unroll_iter130
  br i1 %niter131.ncmp.1, label %._crit_edge80.loopexit.unr-lcssa, label %.lr.ph79.new, !llvm.loop !11

._crit_edge80.loopexit.unr-lcssa:                 ; preds = %.lr.ph79.new, %.lr.ph79
  %indvars.iv97.unr = phi i64 [ 0, %.lr.ph79 ], [ %indvars.iv.next98.1, %.lr.ph79.new ]
  br i1 %lcmp.mod129.not, label %._crit_edge80, label %._crit_edge80.loopexit.epilog-lcssa

._crit_edge80.loopexit.epilog-lcssa:              ; preds = %._crit_edge80.loopexit.unr-lcssa
  %indvars.iv.next98.epil = add nuw nsw i64 %indvars.iv97.unr, 1
  %68 = mul nuw nsw i64 %indvars.iv.next98.epil, %indvars.iv102
  %69 = trunc i64 %68 to i32
  %70 = add i32 %69, 2
  %71 = urem i32 %70, %1
  %72 = uitofp nneg i32 %71 to double
  %73 = fdiv double %72, %23
  %74 = getelementptr inbounds nuw double, ptr %48, i64 %indvars.iv97.unr
  store double %73, ptr %74, align 8
  br label %._crit_edge80

._crit_edge80:                                    ; preds = %._crit_edge80.loopexit.epilog-lcssa, %._crit_edge80.loopexit.unr-lcssa, %.preheader73
  %indvars.iv.next103 = add nuw nsw i64 %indvars.iv102, 1
  %exitcond106.not = icmp eq i64 %indvars.iv.next103, %wide.trip.count105
  br i1 %exitcond106.not, label %.preheader72, label %.preheader73, !llvm.loop !12

.preheader71:                                     ; preds = %.preheader71.lr.ph, %._crit_edge84
  %indvars.iv112 = phi i64 [ 0, %.preheader71.lr.ph ], [ %indvars.iv.next113, %._crit_edge84 ]
  br i1 %50, label %.lr.ph83, label %._crit_edge84

.lr.ph83:                                         ; preds = %.preheader71
  %75 = mul nuw nsw i64 %indvars.iv112, %12
  %76 = getelementptr inbounds nuw double, ptr %7, i64 %75
  br i1 %53, label %._crit_edge84.loopexit.unr-lcssa, label %.lr.ph83.new

.lr.ph83.new:                                     ; preds = %.lr.ph83
  %invariant.gep = getelementptr inbounds i8, ptr %76, i64 8
  br label %82

.preheader70:                                     ; preds = %._crit_edge84, %.preheader72
  %77 = icmp sgt i32 %4, 0
  br i1 %77, label %.preheader.lr.ph, label %._crit_edge90

.preheader.lr.ph:                                 ; preds = %.preheader70
  %78 = icmp sgt i32 %3, 0
  %79 = sitofp i32 %3 to double
  %wide.trip.count125 = zext nneg i32 %4 to i64
  %80 = zext i32 %3 to i64
  %xtraiter138 = and i64 %80, 1
  %81 = icmp eq i32 %3, 1
  %unroll_iter140 = and i64 %80, 2147483646
  %lcmp.mod139.not = icmp eq i64 %xtraiter138, 0
  br label %.preheader

82:                                               ; preds = %82, %.lr.ph83.new
  %indvars.iv107 = phi i64 [ 0, %.lr.ph83.new ], [ %indvars.iv.next108.1, %82 ]
  %niter136 = phi i64 [ 0, %.lr.ph83.new ], [ %niter136.next.1, %82 ]
  %83 = add nuw nsw i64 %indvars.iv107, 3
  %84 = mul nuw nsw i64 %83, %indvars.iv112
  %85 = trunc nuw i64 %84 to i32
  %86 = urem i32 %85, %4
  %87 = uitofp nneg i32 %86 to double
  %88 = fdiv double %87, %51
  %89 = getelementptr inbounds nuw double, ptr %76, i64 %indvars.iv107
  store double %88, ptr %89, align 8
  %90 = add nuw nsw i64 %indvars.iv107, 4
  %91 = mul nuw nsw i64 %90, %indvars.iv112
  %92 = trunc nuw i64 %91 to i32
  %93 = urem i32 %92, %4
  %94 = uitofp nneg i32 %93 to double
  %95 = fdiv double %94, %51
  %gep = getelementptr inbounds double, ptr %invariant.gep, i64 %indvars.iv107
  store double %95, ptr %gep, align 8
  %indvars.iv.next108.1 = add nuw nsw i64 %indvars.iv107, 2
  %niter136.next.1 = add i64 %niter136, 2
  %niter136.ncmp.1 = icmp eq i64 %niter136.next.1, %unroll_iter135
  br i1 %niter136.ncmp.1, label %._crit_edge84.loopexit.unr-lcssa, label %82, !llvm.loop !13

._crit_edge84.loopexit.unr-lcssa:                 ; preds = %82, %.lr.ph83
  %indvars.iv107.unr = phi i64 [ 0, %.lr.ph83 ], [ %indvars.iv.next108.1, %82 ]
  br i1 %lcmp.mod134.not, label %._crit_edge84, label %._crit_edge84.loopexit.epilog-lcssa

._crit_edge84.loopexit.epilog-lcssa:              ; preds = %._crit_edge84.loopexit.unr-lcssa
  %96 = add nuw nsw i64 %indvars.iv107.unr, 3
  %97 = mul nuw nsw i64 %96, %indvars.iv112
  %98 = trunc nuw i64 %97 to i32
  %99 = urem i32 %98, %4
  %100 = uitofp nneg i32 %99 to double
  %101 = fdiv double %100, %51
  %102 = getelementptr inbounds nuw double, ptr %76, i64 %indvars.iv107.unr
  store double %101, ptr %102, align 8
  br label %._crit_edge84

._crit_edge84:                                    ; preds = %._crit_edge84.loopexit.epilog-lcssa, %._crit_edge84.loopexit.unr-lcssa, %.preheader71
  %indvars.iv.next113 = add nuw nsw i64 %indvars.iv112, 1
  %exitcond116.not = icmp eq i64 %indvars.iv.next113, %wide.trip.count115
  br i1 %exitcond116.not, label %.preheader70, label %.preheader71, !llvm.loop !14

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge88
  %indvars.iv122 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next123, %._crit_edge88 ]
  br i1 %78, label %.lr.ph87, label %._crit_edge88

.lr.ph87:                                         ; preds = %.preheader
  %103 = mul nuw nsw i64 %indvars.iv122, %13
  %104 = getelementptr inbounds nuw double, ptr %8, i64 %103
  br i1 %81, label %._crit_edge88.loopexit.unr-lcssa, label %.lr.ph87.new

.lr.ph87.new:                                     ; preds = %.lr.ph87
  %invariant.gep142 = getelementptr inbounds i8, ptr %104, i64 8
  br label %105

105:                                              ; preds = %105, %.lr.ph87.new
  %indvars.iv117 = phi i64 [ 0, %.lr.ph87.new ], [ %indvars.iv.next118.1, %105 ]
  %niter141 = phi i64 [ 0, %.lr.ph87.new ], [ %niter141.next.1, %105 ]
  %106 = add nuw nsw i64 %indvars.iv117, 2
  %107 = mul nuw nsw i64 %106, %indvars.iv122
  %108 = trunc i64 %107 to i32
  %109 = add i32 %108, 2
  %110 = urem i32 %109, %3
  %111 = uitofp nneg i32 %110 to double
  %112 = fdiv double %111, %79
  %113 = getelementptr inbounds nuw double, ptr %104, i64 %indvars.iv117
  store double %112, ptr %113, align 8
  %114 = add nuw nsw i64 %indvars.iv117, 3
  %115 = mul nuw nsw i64 %114, %indvars.iv122
  %116 = trunc i64 %115 to i32
  %117 = add i32 %116, 2
  %118 = urem i32 %117, %3
  %119 = uitofp nneg i32 %118 to double
  %120 = fdiv double %119, %79
  %gep143 = getelementptr inbounds double, ptr %invariant.gep142, i64 %indvars.iv117
  store double %120, ptr %gep143, align 8
  %indvars.iv.next118.1 = add nuw nsw i64 %indvars.iv117, 2
  %niter141.next.1 = add i64 %niter141, 2
  %niter141.ncmp.1 = icmp eq i64 %niter141.next.1, %unroll_iter140
  br i1 %niter141.ncmp.1, label %._crit_edge88.loopexit.unr-lcssa, label %105, !llvm.loop !15

._crit_edge88.loopexit.unr-lcssa:                 ; preds = %105, %.lr.ph87
  %indvars.iv117.unr = phi i64 [ 0, %.lr.ph87 ], [ %indvars.iv.next118.1, %105 ]
  br i1 %lcmp.mod139.not, label %._crit_edge88, label %._crit_edge88.loopexit.epilog-lcssa

._crit_edge88.loopexit.epilog-lcssa:              ; preds = %._crit_edge88.loopexit.unr-lcssa
  %121 = add nuw nsw i64 %indvars.iv117.unr, 2
  %122 = mul nuw nsw i64 %121, %indvars.iv122
  %123 = trunc i64 %122 to i32
  %124 = add i32 %123, 2
  %125 = urem i32 %124, %3
  %126 = uitofp nneg i32 %125 to double
  %127 = fdiv double %126, %79
  %128 = getelementptr inbounds nuw double, ptr %104, i64 %indvars.iv117.unr
  store double %127, ptr %128, align 8
  br label %._crit_edge88

._crit_edge88:                                    ; preds = %._crit_edge88.loopexit.epilog-lcssa, %._crit_edge88.loopexit.unr-lcssa, %.preheader
  %indvars.iv.next123 = add nuw nsw i64 %indvars.iv122, 1
  %exitcond126.not = icmp eq i64 %indvars.iv.next123, %wide.trip.count125
  br i1 %exitcond126.not, label %._crit_edge90, label %.preheader, !llvm.loop !16

._crit_edge90:                                    ; preds = %._crit_edge88, %.preheader70
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @mm3(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, i32 noundef %4, ptr noundef captures(none) %5, ptr noundef readonly captures(none) %6, ptr noundef readonly captures(none) %7, ptr noundef captures(none) %8, ptr noundef readonly captures(none) %9, ptr noundef readonly captures(none) %10, ptr noundef captures(none) %11) local_unnamed_addr #1 {
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
  %20 = zext i32 %2 to i64
  %wide.trip.count122 = zext nneg i32 %1 to i64
  %xtraiter = and i64 %20, 1
  %21 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %20, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader89

.preheader89:                                     ; preds = %.preheader89.lr.ph, %._crit_edge93
  %indvars.iv124 = phi i64 [ 0, %.preheader89.lr.ph ], [ %indvars.iv.next125, %._crit_edge93 ]
  br i1 %18, label %.lr.ph92, label %._crit_edge93

.lr.ph92:                                         ; preds = %.preheader89
  %22 = mul nuw nsw i64 %indvars.iv124, %13
  %23 = getelementptr inbounds nuw double, ptr %5, i64 %22
  %24 = mul nuw nsw i64 %indvars.iv124, %14
  %25 = getelementptr inbounds nuw double, ptr %6, i64 %24
  br label %31

.preheader88:                                     ; preds = %._crit_edge93, %12
  %26 = icmp sgt i32 %1, 0
  br i1 %26, label %.preheader87.lr.ph, label %.preheader86

.preheader87.lr.ph:                               ; preds = %.preheader88
  %27 = icmp sgt i32 %3, 0
  %28 = icmp sgt i32 %4, 0
  %wide.trip.count142 = zext nneg i32 %1 to i64
  %29 = zext i32 %4 to i64
  %wide.trip.count137 = zext nneg i32 %3 to i64
  %xtraiter160 = and i64 %29, 1
  %30 = icmp eq i32 %4, 1
  %unroll_iter163 = and i64 %29, 2147483646
  %lcmp.mod162.not = icmp eq i64 %xtraiter160, 0
  br label %.preheader87

31:                                               ; preds = %.lr.ph92, %._crit_edge
  %indvars.iv119 = phi i64 [ 0, %.lr.ph92 ], [ %indvars.iv.next120, %._crit_edge ]
  %32 = getelementptr inbounds nuw double, ptr %23, i64 %indvars.iv119
  store double 0.000000e+00, ptr %32, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %7, i64 %indvars.iv119
  br i1 %19, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %31
  %.promoted = load double, ptr %32, align 8
  br i1 %21, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %33 = phi double [ %43, %.lr.ph.new ], [ %.promoted, %.lr.ph ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %34 = getelementptr inbounds nuw double, ptr %25, i64 %indvars.iv
  %35 = load double, ptr %34, align 8
  %36 = mul nuw nsw i64 %indvars.iv, %13
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %36
  %37 = load double, ptr %gep, align 8
  %38 = tail call double @llvm.fmuladd.f64(double %35, double %37, double %33)
  store double %38, ptr %32, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %39 = getelementptr inbounds nuw double, ptr %25, i64 %indvars.iv.next
  %40 = load double, ptr %39, align 8
  %41 = mul nuw nsw i64 %indvars.iv.next, %13
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %41
  %42 = load double, ptr %gep.1, align 8
  %43 = tail call double @llvm.fmuladd.f64(double %40, double %42, double %38)
  store double %43, ptr %32, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !17

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %.lr.ph.new ]
  %.unr = phi double [ %.promoted, %.lr.ph ], [ %43, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.loopexit.epilog-lcssa

._crit_edge.loopexit.epilog-lcssa:                ; preds = %._crit_edge.loopexit.unr-lcssa
  %44 = getelementptr inbounds nuw double, ptr %25, i64 %indvars.iv.unr
  %45 = load double, ptr %44, align 8
  %46 = mul nuw nsw i64 %indvars.iv.unr, %13
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %46
  %47 = load double, ptr %gep.epil, align 8
  %48 = tail call double @llvm.fmuladd.f64(double %45, double %47, double %.unr)
  store double %48, ptr %32, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.loopexit.epilog-lcssa, %._crit_edge.loopexit.unr-lcssa, %31
  %indvars.iv.next120 = add nuw nsw i64 %indvars.iv119, 1
  %exitcond123.not = icmp eq i64 %indvars.iv.next120, %wide.trip.count122
  br i1 %exitcond123.not, label %._crit_edge93, label %31, !llvm.loop !18

._crit_edge93:                                    ; preds = %._crit_edge, %.preheader89
  %indvars.iv.next125 = add nuw nsw i64 %indvars.iv124, 1
  %exitcond128.not = icmp eq i64 %indvars.iv.next125, %wide.trip.count127
  br i1 %exitcond128.not, label %.preheader88, label %.preheader89, !llvm.loop !19

.preheader87:                                     ; preds = %.preheader87.lr.ph, %._crit_edge104
  %indvars.iv139 = phi i64 [ 0, %.preheader87.lr.ph ], [ %indvars.iv.next140, %._crit_edge104 ]
  br i1 %27, label %.lr.ph103, label %._crit_edge104

.lr.ph103:                                        ; preds = %.preheader87
  %49 = mul nuw nsw i64 %indvars.iv139, %15
  %50 = getelementptr inbounds nuw double, ptr %8, i64 %49
  %51 = mul nuw nsw i64 %indvars.iv139, %16
  %52 = getelementptr inbounds nuw double, ptr %9, i64 %51
  br label %57

.preheader86:                                     ; preds = %._crit_edge104, %.preheader88
  %53 = icmp sgt i32 %0, 0
  br i1 %53, label %.preheader.lr.ph, label %._crit_edge117

.preheader.lr.ph:                                 ; preds = %.preheader86
  %54 = icmp sgt i32 %3, 0
  %55 = icmp sgt i32 %1, 0
  %wide.trip.count157 = zext nneg i32 %0 to i64
  %wide.trip.count152 = zext nneg i32 %3 to i64
  %xtraiter166 = and i64 %13, 1
  %56 = icmp eq i32 %1, 1
  %unroll_iter169 = and i64 %13, 2147483646
  %lcmp.mod168.not = icmp eq i64 %xtraiter166, 0
  br label %.preheader

57:                                               ; preds = %.lr.ph103, %._crit_edge100
  %indvars.iv134 = phi i64 [ 0, %.lr.ph103 ], [ %indvars.iv.next135, %._crit_edge100 ]
  %58 = getelementptr inbounds nuw double, ptr %50, i64 %indvars.iv134
  store double 0.000000e+00, ptr %58, align 8
  %invariant.gep95 = getelementptr inbounds nuw double, ptr %10, i64 %indvars.iv134
  br i1 %28, label %.lr.ph99, label %._crit_edge100

.lr.ph99:                                         ; preds = %57
  %.promoted101 = load double, ptr %58, align 8
  br i1 %30, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99.new

.lr.ph99.new:                                     ; preds = %.lr.ph99, %.lr.ph99.new
  %indvars.iv129 = phi i64 [ %indvars.iv.next130.1, %.lr.ph99.new ], [ 0, %.lr.ph99 ]
  %59 = phi double [ %69, %.lr.ph99.new ], [ %.promoted101, %.lr.ph99 ]
  %niter164 = phi i64 [ %niter164.next.1, %.lr.ph99.new ], [ 0, %.lr.ph99 ]
  %60 = getelementptr inbounds nuw double, ptr %52, i64 %indvars.iv129
  %61 = load double, ptr %60, align 8
  %62 = mul nuw nsw i64 %indvars.iv129, %15
  %gep96 = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %62
  %63 = load double, ptr %gep96, align 8
  %64 = tail call double @llvm.fmuladd.f64(double %61, double %63, double %59)
  store double %64, ptr %58, align 8
  %indvars.iv.next130 = or disjoint i64 %indvars.iv129, 1
  %65 = getelementptr inbounds nuw double, ptr %52, i64 %indvars.iv.next130
  %66 = load double, ptr %65, align 8
  %67 = mul nuw nsw i64 %indvars.iv.next130, %15
  %gep96.1 = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %67
  %68 = load double, ptr %gep96.1, align 8
  %69 = tail call double @llvm.fmuladd.f64(double %66, double %68, double %64)
  store double %69, ptr %58, align 8
  %indvars.iv.next130.1 = add nuw nsw i64 %indvars.iv129, 2
  %niter164.next.1 = add i64 %niter164, 2
  %niter164.ncmp.1 = icmp eq i64 %niter164.next.1, %unroll_iter163
  br i1 %niter164.ncmp.1, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99.new, !llvm.loop !20

._crit_edge100.loopexit.unr-lcssa:                ; preds = %.lr.ph99.new, %.lr.ph99
  %indvars.iv129.unr = phi i64 [ 0, %.lr.ph99 ], [ %indvars.iv.next130.1, %.lr.ph99.new ]
  %.unr161 = phi double [ %.promoted101, %.lr.ph99 ], [ %69, %.lr.ph99.new ]
  br i1 %lcmp.mod162.not, label %._crit_edge100, label %._crit_edge100.loopexit.epilog-lcssa

._crit_edge100.loopexit.epilog-lcssa:             ; preds = %._crit_edge100.loopexit.unr-lcssa
  %70 = getelementptr inbounds nuw double, ptr %52, i64 %indvars.iv129.unr
  %71 = load double, ptr %70, align 8
  %72 = mul nuw nsw i64 %indvars.iv129.unr, %15
  %gep96.epil = getelementptr inbounds nuw double, ptr %invariant.gep95, i64 %72
  %73 = load double, ptr %gep96.epil, align 8
  %74 = tail call double @llvm.fmuladd.f64(double %71, double %73, double %.unr161)
  store double %74, ptr %58, align 8
  br label %._crit_edge100

._crit_edge100:                                   ; preds = %._crit_edge100.loopexit.epilog-lcssa, %._crit_edge100.loopexit.unr-lcssa, %57
  %indvars.iv.next135 = add nuw nsw i64 %indvars.iv134, 1
  %exitcond138.not = icmp eq i64 %indvars.iv.next135, %wide.trip.count137
  br i1 %exitcond138.not, label %._crit_edge104, label %57, !llvm.loop !21

._crit_edge104:                                   ; preds = %._crit_edge100, %.preheader87
  %indvars.iv.next140 = add nuw nsw i64 %indvars.iv139, 1
  %exitcond143.not = icmp eq i64 %indvars.iv.next140, %wide.trip.count142
  br i1 %exitcond143.not, label %.preheader86, label %.preheader87, !llvm.loop !22

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge115
  %indvars.iv154 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next155, %._crit_edge115 ]
  br i1 %54, label %.lr.ph114, label %._crit_edge115

.lr.ph114:                                        ; preds = %.preheader
  %75 = mul nuw nsw i64 %indvars.iv154, %15
  %76 = getelementptr inbounds nuw double, ptr %11, i64 %75
  %77 = mul nuw nsw i64 %indvars.iv154, %13
  %78 = getelementptr inbounds nuw double, ptr %5, i64 %77
  br label %79

79:                                               ; preds = %.lr.ph114, %._crit_edge111
  %indvars.iv149 = phi i64 [ 0, %.lr.ph114 ], [ %indvars.iv.next150, %._crit_edge111 ]
  %80 = getelementptr inbounds nuw double, ptr %76, i64 %indvars.iv149
  store double 0.000000e+00, ptr %80, align 8
  %invariant.gep106 = getelementptr inbounds nuw double, ptr %8, i64 %indvars.iv149
  br i1 %55, label %.lr.ph110, label %._crit_edge111

.lr.ph110:                                        ; preds = %79
  %.promoted112 = load double, ptr %80, align 8
  br i1 %56, label %._crit_edge111.loopexit.unr-lcssa, label %.lr.ph110.new

.lr.ph110.new:                                    ; preds = %.lr.ph110, %.lr.ph110.new
  %indvars.iv144 = phi i64 [ %indvars.iv.next145.1, %.lr.ph110.new ], [ 0, %.lr.ph110 ]
  %81 = phi double [ %91, %.lr.ph110.new ], [ %.promoted112, %.lr.ph110 ]
  %niter170 = phi i64 [ %niter170.next.1, %.lr.ph110.new ], [ 0, %.lr.ph110 ]
  %82 = getelementptr inbounds nuw double, ptr %78, i64 %indvars.iv144
  %83 = load double, ptr %82, align 8
  %84 = mul nuw nsw i64 %indvars.iv144, %15
  %gep107 = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %84
  %85 = load double, ptr %gep107, align 8
  %86 = tail call double @llvm.fmuladd.f64(double %83, double %85, double %81)
  store double %86, ptr %80, align 8
  %indvars.iv.next145 = or disjoint i64 %indvars.iv144, 1
  %87 = getelementptr inbounds nuw double, ptr %78, i64 %indvars.iv.next145
  %88 = load double, ptr %87, align 8
  %89 = mul nuw nsw i64 %indvars.iv.next145, %15
  %gep107.1 = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %89
  %90 = load double, ptr %gep107.1, align 8
  %91 = tail call double @llvm.fmuladd.f64(double %88, double %90, double %86)
  store double %91, ptr %80, align 8
  %indvars.iv.next145.1 = add nuw nsw i64 %indvars.iv144, 2
  %niter170.next.1 = add i64 %niter170, 2
  %niter170.ncmp.1 = icmp eq i64 %niter170.next.1, %unroll_iter169
  br i1 %niter170.ncmp.1, label %._crit_edge111.loopexit.unr-lcssa, label %.lr.ph110.new, !llvm.loop !23

._crit_edge111.loopexit.unr-lcssa:                ; preds = %.lr.ph110.new, %.lr.ph110
  %indvars.iv144.unr = phi i64 [ 0, %.lr.ph110 ], [ %indvars.iv.next145.1, %.lr.ph110.new ]
  %.unr167 = phi double [ %.promoted112, %.lr.ph110 ], [ %91, %.lr.ph110.new ]
  br i1 %lcmp.mod168.not, label %._crit_edge111, label %._crit_edge111.loopexit.epilog-lcssa

._crit_edge111.loopexit.epilog-lcssa:             ; preds = %._crit_edge111.loopexit.unr-lcssa
  %92 = getelementptr inbounds nuw double, ptr %78, i64 %indvars.iv144.unr
  %93 = load double, ptr %92, align 8
  %94 = mul nuw nsw i64 %indvars.iv144.unr, %15
  %gep107.epil = getelementptr inbounds nuw double, ptr %invariant.gep106, i64 %94
  %95 = load double, ptr %gep107.epil, align 8
  %96 = tail call double @llvm.fmuladd.f64(double %93, double %95, double %.unr167)
  store double %96, ptr %80, align 8
  br label %._crit_edge111

._crit_edge111:                                   ; preds = %._crit_edge111.loopexit.epilog-lcssa, %._crit_edge111.loopexit.unr-lcssa, %79
  %indvars.iv.next150 = add nuw nsw i64 %indvars.iv149, 1
  %exitcond153.not = icmp eq i64 %indvars.iv.next150, %wide.trip.count152
  br i1 %exitcond153.not, label %._crit_edge115, label %79, !llvm.loop !24

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
