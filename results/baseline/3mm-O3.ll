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
  br i1 %15, label %.preheader75.us.preheader, label %.preheader72

.preheader75.us.preheader:                        ; preds = %.preheader75.lr.ph
  %wide.trip.count96 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %10, 1
  %17 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %10, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader75.us

.preheader75.us:                                  ; preds = %.preheader75.us.preheader, %._crit_edge.us
  %indvars.iv93 = phi i64 [ 0, %.preheader75.us.preheader ], [ %indvars.iv.next94, %._crit_edge.us ]
  %18 = mul nuw nsw i64 %indvars.iv93, %10
  %19 = getelementptr inbounds nuw double, ptr %5, i64 %18
  br i1 %17, label %._crit_edge.us.unr-lcssa, label %.preheader75.us.new

.preheader75.us.new:                              ; preds = %.preheader75.us, %.preheader75.us.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.preheader75.us.new ], [ 0, %.preheader75.us ]
  %niter = phi i64 [ %niter.next.1, %.preheader75.us.new ], [ 0, %.preheader75.us ]
  %20 = mul nuw nsw i64 %indvars.iv, %indvars.iv93
  %21 = trunc i64 %20 to i32
  %22 = or disjoint i32 %21, 1
  %23 = urem i32 %22, %0
  %24 = uitofp nneg i32 %23 to double
  %25 = fdiv double %24, %16
  %26 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv
  store double %25, ptr %26, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %27 = mul nuw nsw i64 %indvars.iv.next, %indvars.iv93
  %28 = trunc i64 %27 to i32
  %29 = add i32 %28, 1
  %30 = urem i32 %29, %0
  %31 = uitofp nneg i32 %30 to double
  %32 = fdiv double %31, %16
  %33 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv.next
  store double %32, ptr %33, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.us.unr-lcssa, label %.preheader75.us.new, !llvm.loop !8

._crit_edge.us.unr-lcssa:                         ; preds = %.preheader75.us.new, %.preheader75.us
  %indvars.iv.unr = phi i64 [ 0, %.preheader75.us ], [ %indvars.iv.next.1, %.preheader75.us.new ]
  br i1 %lcmp.mod.not, label %._crit_edge.us, label %._crit_edge.us.epilog-lcssa

._crit_edge.us.epilog-lcssa:                      ; preds = %._crit_edge.us.unr-lcssa
  %34 = mul nuw nsw i64 %indvars.iv.unr, %indvars.iv93
  %35 = trunc i64 %34 to i32
  %36 = add i32 %35, 1
  %37 = urem i32 %36, %0
  %38 = uitofp nneg i32 %37 to double
  %39 = fdiv double %38, %16
  %40 = getelementptr inbounds nuw double, ptr %19, i64 %indvars.iv.unr
  store double %39, ptr %40, align 8
  br label %._crit_edge.us

._crit_edge.us:                                   ; preds = %._crit_edge.us.unr-lcssa, %._crit_edge.us.epilog-lcssa
  %indvars.iv.next94 = add nuw nsw i64 %indvars.iv93, 1
  %exitcond97.not = icmp eq i64 %indvars.iv.next94, %wide.trip.count96
  br i1 %exitcond97.not, label %.preheader74, label %.preheader75.us, !llvm.loop !10

.preheader74:                                     ; preds = %._crit_edge.us, %9
  %41 = icmp sgt i32 %2, 0
  br i1 %41, label %.preheader73.lr.ph, label %.preheader72

.preheader73.lr.ph:                               ; preds = %.preheader74
  %42 = icmp sgt i32 %1, 0
  %43 = sitofp i32 %1 to double
  br i1 %42, label %.preheader73.us.preheader, label %.preheader70

.preheader73.us.preheader:                        ; preds = %.preheader73.lr.ph
  %xtraiter129 = and i64 %11, 1
  %44 = icmp eq i32 %1, 1
  %unroll_iter131 = and i64 %11, 2147483646
  %lcmp.mod130.not = icmp eq i64 %xtraiter129, 0
  br label %.preheader73.us

.preheader73.us:                                  ; preds = %.preheader73.us.preheader, %._crit_edge.us80
  %indvars.iv103 = phi i64 [ %indvars.iv.next104, %._crit_edge.us80 ], [ 0, %.preheader73.us.preheader ]
  %45 = mul nuw nsw i64 %indvars.iv103, %11
  %46 = getelementptr inbounds nuw double, ptr %6, i64 %45
  br i1 %44, label %._crit_edge.us80.unr-lcssa, label %.preheader73.us.new

.preheader73.us.new:                              ; preds = %.preheader73.us, %.preheader73.us.new
  %indvars.iv98 = phi i64 [ %indvars.iv.next99.1, %.preheader73.us.new ], [ 0, %.preheader73.us ]
  %niter132 = phi i64 [ %niter132.next.1, %.preheader73.us.new ], [ 0, %.preheader73.us ]
  %indvars.iv.next99 = or disjoint i64 %indvars.iv98, 1
  %47 = mul nuw nsw i64 %indvars.iv.next99, %indvars.iv103
  %48 = trunc i64 %47 to i32
  %49 = add i32 %48, 2
  %50 = urem i32 %49, %1
  %51 = uitofp nneg i32 %50 to double
  %52 = fdiv double %51, %43
  %53 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv98
  store double %52, ptr %53, align 8
  %indvars.iv.next99.1 = add nuw nsw i64 %indvars.iv98, 2
  %54 = mul nuw nsw i64 %indvars.iv.next99.1, %indvars.iv103
  %55 = trunc i64 %54 to i32
  %56 = add i32 %55, 2
  %57 = urem i32 %56, %1
  %58 = uitofp nneg i32 %57 to double
  %59 = fdiv double %58, %43
  %60 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv.next99
  store double %59, ptr %60, align 8
  %niter132.next.1 = add i64 %niter132, 2
  %niter132.ncmp.1 = icmp eq i64 %niter132.next.1, %unroll_iter131
  br i1 %niter132.ncmp.1, label %._crit_edge.us80.unr-lcssa, label %.preheader73.us.new, !llvm.loop !11

._crit_edge.us80.unr-lcssa:                       ; preds = %.preheader73.us.new, %.preheader73.us
  %indvars.iv98.unr = phi i64 [ 0, %.preheader73.us ], [ %indvars.iv.next99.1, %.preheader73.us.new ]
  br i1 %lcmp.mod130.not, label %._crit_edge.us80, label %._crit_edge.us80.epilog-lcssa

._crit_edge.us80.epilog-lcssa:                    ; preds = %._crit_edge.us80.unr-lcssa
  %indvars.iv.next99.epil = add nuw nsw i64 %indvars.iv98.unr, 1
  %61 = mul nuw nsw i64 %indvars.iv.next99.epil, %indvars.iv103
  %62 = trunc i64 %61 to i32
  %63 = add i32 %62, 2
  %64 = urem i32 %63, %1
  %65 = uitofp nneg i32 %64 to double
  %66 = fdiv double %65, %43
  %67 = getelementptr inbounds nuw double, ptr %46, i64 %indvars.iv98.unr
  store double %66, ptr %67, align 8
  br label %._crit_edge.us80

._crit_edge.us80:                                 ; preds = %._crit_edge.us80.unr-lcssa, %._crit_edge.us80.epilog-lcssa
  %indvars.iv.next104 = add nuw nsw i64 %indvars.iv103, 1
  %exitcond107.not = icmp eq i64 %indvars.iv.next104, %10
  br i1 %exitcond107.not, label %.preheader72, label %.preheader73.us, !llvm.loop !12

.preheader72:                                     ; preds = %._crit_edge.us80, %.preheader75.lr.ph, %.preheader74
  %68 = icmp sgt i32 %1, 0
  br i1 %68, label %.preheader71.lr.ph, label %.preheader70

.preheader71.lr.ph:                               ; preds = %.preheader72
  %69 = icmp sgt i32 %4, 0
  %70 = sitofp i32 %4 to double
  br i1 %69, label %.preheader71.us.preheader, label %._crit_edge86

.preheader71.us.preheader:                        ; preds = %.preheader71.lr.ph
  %xtraiter134 = and i64 %12, 1
  %71 = icmp eq i32 %4, 1
  %unroll_iter136 = and i64 %12, 2147483646
  %lcmp.mod135.not = icmp eq i64 %xtraiter134, 0
  br label %.preheader71.us

.preheader71.us:                                  ; preds = %.preheader71.us.preheader, %._crit_edge.us83
  %indvars.iv113 = phi i64 [ %indvars.iv.next114, %._crit_edge.us83 ], [ 0, %.preheader71.us.preheader ]
  %72 = mul nuw nsw i64 %indvars.iv113, %12
  %73 = getelementptr inbounds nuw double, ptr %7, i64 %72
  br i1 %71, label %._crit_edge.us83.unr-lcssa, label %.preheader71.us.new

.preheader71.us.new:                              ; preds = %.preheader71.us
  %invariant.gep = getelementptr inbounds i8, ptr %73, i64 8
  br label %74

74:                                               ; preds = %74, %.preheader71.us.new
  %indvars.iv108 = phi i64 [ 0, %.preheader71.us.new ], [ %indvars.iv.next109.1, %74 ]
  %niter137 = phi i64 [ 0, %.preheader71.us.new ], [ %niter137.next.1, %74 ]
  %75 = add nuw nsw i64 %indvars.iv108, 3
  %76 = mul nuw nsw i64 %75, %indvars.iv113
  %77 = trunc nuw i64 %76 to i32
  %78 = urem i32 %77, %4
  %79 = uitofp nneg i32 %78 to double
  %80 = fdiv double %79, %70
  %81 = getelementptr inbounds nuw double, ptr %73, i64 %indvars.iv108
  store double %80, ptr %81, align 8
  %82 = add nuw nsw i64 %indvars.iv108, 4
  %83 = mul nuw nsw i64 %82, %indvars.iv113
  %84 = trunc nuw i64 %83 to i32
  %85 = urem i32 %84, %4
  %86 = uitofp nneg i32 %85 to double
  %87 = fdiv double %86, %70
  %gep = getelementptr inbounds double, ptr %invariant.gep, i64 %indvars.iv108
  store double %87, ptr %gep, align 8
  %indvars.iv.next109.1 = add nuw nsw i64 %indvars.iv108, 2
  %niter137.next.1 = add i64 %niter137, 2
  %niter137.ncmp.1 = icmp eq i64 %niter137.next.1, %unroll_iter136
  br i1 %niter137.ncmp.1, label %._crit_edge.us83.unr-lcssa, label %74, !llvm.loop !13

._crit_edge.us83.unr-lcssa:                       ; preds = %74, %.preheader71.us
  %indvars.iv108.unr = phi i64 [ 0, %.preheader71.us ], [ %indvars.iv.next109.1, %74 ]
  br i1 %lcmp.mod135.not, label %._crit_edge.us83, label %._crit_edge.us83.epilog-lcssa

._crit_edge.us83.epilog-lcssa:                    ; preds = %._crit_edge.us83.unr-lcssa
  %88 = add nuw nsw i64 %indvars.iv108.unr, 3
  %89 = mul nuw nsw i64 %88, %indvars.iv113
  %90 = trunc nuw i64 %89 to i32
  %91 = urem i32 %90, %4
  %92 = uitofp nneg i32 %91 to double
  %93 = fdiv double %92, %70
  %94 = getelementptr inbounds nuw double, ptr %73, i64 %indvars.iv108.unr
  store double %93, ptr %94, align 8
  br label %._crit_edge.us83

._crit_edge.us83:                                 ; preds = %._crit_edge.us83.unr-lcssa, %._crit_edge.us83.epilog-lcssa
  %indvars.iv.next114 = add nuw nsw i64 %indvars.iv113, 1
  %exitcond117.not = icmp eq i64 %indvars.iv.next114, %11
  br i1 %exitcond117.not, label %.preheader70, label %.preheader71.us, !llvm.loop !14

.preheader70:                                     ; preds = %._crit_edge.us83, %.preheader73.lr.ph, %.preheader72
  %95 = icmp sgt i32 %4, 0
  br i1 %95, label %.preheader.lr.ph, label %._crit_edge86

.preheader.lr.ph:                                 ; preds = %.preheader70
  %96 = icmp sgt i32 %3, 0
  %97 = sitofp i32 %3 to double
  br i1 %96, label %.preheader.us.preheader, label %._crit_edge86

.preheader.us.preheader:                          ; preds = %.preheader.lr.ph
  %xtraiter139 = and i64 %13, 1
  %98 = icmp eq i32 %3, 1
  %unroll_iter141 = and i64 %13, 2147483646
  %lcmp.mod140.not = icmp eq i64 %xtraiter139, 0
  br label %.preheader.us

.preheader.us:                                    ; preds = %.preheader.us.preheader, %._crit_edge.us87
  %indvars.iv123 = phi i64 [ %indvars.iv.next124, %._crit_edge.us87 ], [ 0, %.preheader.us.preheader ]
  %99 = mul nuw nsw i64 %indvars.iv123, %13
  %100 = getelementptr inbounds nuw double, ptr %8, i64 %99
  br i1 %98, label %._crit_edge.us87.unr-lcssa, label %.preheader.us.new

.preheader.us.new:                                ; preds = %.preheader.us
  %invariant.gep143 = getelementptr inbounds i8, ptr %100, i64 8
  br label %101

101:                                              ; preds = %101, %.preheader.us.new
  %indvars.iv118 = phi i64 [ 0, %.preheader.us.new ], [ %indvars.iv.next119.1, %101 ]
  %niter142 = phi i64 [ 0, %.preheader.us.new ], [ %niter142.next.1, %101 ]
  %102 = add nuw nsw i64 %indvars.iv118, 2
  %103 = mul nuw nsw i64 %102, %indvars.iv123
  %104 = trunc i64 %103 to i32
  %105 = add i32 %104, 2
  %106 = urem i32 %105, %3
  %107 = uitofp nneg i32 %106 to double
  %108 = fdiv double %107, %97
  %109 = getelementptr inbounds nuw double, ptr %100, i64 %indvars.iv118
  store double %108, ptr %109, align 8
  %110 = add nuw nsw i64 %indvars.iv118, 3
  %111 = mul nuw nsw i64 %110, %indvars.iv123
  %112 = trunc i64 %111 to i32
  %113 = add i32 %112, 2
  %114 = urem i32 %113, %3
  %115 = uitofp nneg i32 %114 to double
  %116 = fdiv double %115, %97
  %gep144 = getelementptr inbounds double, ptr %invariant.gep143, i64 %indvars.iv118
  store double %116, ptr %gep144, align 8
  %indvars.iv.next119.1 = add nuw nsw i64 %indvars.iv118, 2
  %niter142.next.1 = add i64 %niter142, 2
  %niter142.ncmp.1 = icmp eq i64 %niter142.next.1, %unroll_iter141
  br i1 %niter142.ncmp.1, label %._crit_edge.us87.unr-lcssa, label %101, !llvm.loop !15

._crit_edge.us87.unr-lcssa:                       ; preds = %101, %.preheader.us
  %indvars.iv118.unr = phi i64 [ 0, %.preheader.us ], [ %indvars.iv.next119.1, %101 ]
  br i1 %lcmp.mod140.not, label %._crit_edge.us87, label %._crit_edge.us87.epilog-lcssa

._crit_edge.us87.epilog-lcssa:                    ; preds = %._crit_edge.us87.unr-lcssa
  %117 = add nuw nsw i64 %indvars.iv118.unr, 2
  %118 = mul nuw nsw i64 %117, %indvars.iv123
  %119 = trunc i64 %118 to i32
  %120 = add i32 %119, 2
  %121 = urem i32 %120, %3
  %122 = uitofp nneg i32 %121 to double
  %123 = fdiv double %122, %97
  %124 = getelementptr inbounds nuw double, ptr %100, i64 %indvars.iv118.unr
  store double %123, ptr %124, align 8
  br label %._crit_edge.us87

._crit_edge.us87:                                 ; preds = %._crit_edge.us87.unr-lcssa, %._crit_edge.us87.epilog-lcssa
  %indvars.iv.next124 = add nuw nsw i64 %indvars.iv123, 1
  %exitcond127.not = icmp eq i64 %indvars.iv.next124, %12
  br i1 %exitcond127.not, label %._crit_edge86, label %.preheader.us, !llvm.loop !16

._crit_edge86:                                    ; preds = %._crit_edge.us87, %.preheader71.lr.ph, %.preheader.lr.ph, %.preheader70
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
  br i1 %18, label %.preheader89.lr.ph.split.us, label %.preheader.lr.ph.thread

.preheader89.lr.ph.split.us:                      ; preds = %.preheader89.lr.ph
  %19 = icmp sgt i32 %2, 0
  %wide.trip.count141 = zext nneg i32 %0 to i64
  br i1 %19, label %.preheader89.us.us.preheader, label %.preheader88.thread

.preheader89.us.us.preheader:                     ; preds = %.preheader89.lr.ph.split.us
  %xtraiter = and i64 %14, 1
  %20 = icmp eq i32 %2, 1
  %unroll_iter = and i64 %14, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader89.us.us

.preheader88.thread:                              ; preds = %.preheader89.lr.ph.split.us
  %21 = mul nuw nsw i64 %13, %wide.trip.count141
  %22 = shl i64 %21, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %5, i8 0, i64 %22, i1 false)
  br label %.preheader87.lr.ph

.preheader89.us.us:                               ; preds = %.preheader89.us.us.preheader, %._crit_edge93.split.us.us.us
  %indvars.iv138 = phi i64 [ %indvars.iv.next139, %._crit_edge93.split.us.us.us ], [ 0, %.preheader89.us.us.preheader ]
  %23 = mul nuw nsw i64 %indvars.iv138, %13
  %24 = getelementptr inbounds nuw double, ptr %5, i64 %23
  %25 = mul nuw nsw i64 %indvars.iv138, %14
  %26 = getelementptr inbounds nuw double, ptr %6, i64 %25
  br label %.lr.ph.us.us.us

.lr.ph.us.us.us:                                  ; preds = %._crit_edge.us.us.us, %.preheader89.us.us
  %indvars.iv133 = phi i64 [ %indvars.iv.next134, %._crit_edge.us.us.us ], [ 0, %.preheader89.us.us ]
  %27 = getelementptr inbounds nuw double, ptr %24, i64 %indvars.iv133
  store double 0.000000e+00, ptr %27, align 8
  %invariant.gep.us.us.us = getelementptr inbounds nuw double, ptr %7, i64 %indvars.iv133
  br i1 %20, label %._crit_edge.us.us.us.unr-lcssa, label %.lr.ph.us.us.us.new

.lr.ph.us.us.us.new:                              ; preds = %.lr.ph.us.us.us, %.lr.ph.us.us.us.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.us.us.us.new ], [ 0, %.lr.ph.us.us.us ]
  %28 = phi double [ %38, %.lr.ph.us.us.us.new ], [ 0.000000e+00, %.lr.ph.us.us.us ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.us.us.us.new ], [ 0, %.lr.ph.us.us.us ]
  %29 = getelementptr inbounds nuw double, ptr %26, i64 %indvars.iv
  %30 = load double, ptr %29, align 8
  %31 = mul nuw nsw i64 %indvars.iv, %13
  %gep.us.us.us = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us, i64 %31
  %32 = load double, ptr %gep.us.us.us, align 8
  %33 = tail call double @llvm.fmuladd.f64(double %30, double %32, double %28)
  store double %33, ptr %27, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %34 = getelementptr inbounds nuw double, ptr %26, i64 %indvars.iv.next
  %35 = load double, ptr %34, align 8
  %36 = mul nuw nsw i64 %indvars.iv.next, %13
  %gep.us.us.us.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us, i64 %36
  %37 = load double, ptr %gep.us.us.us.1, align 8
  %38 = tail call double @llvm.fmuladd.f64(double %35, double %37, double %33)
  store double %38, ptr %27, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.us.us.us.unr-lcssa, label %.lr.ph.us.us.us.new, !llvm.loop !17

._crit_edge.us.us.us.unr-lcssa:                   ; preds = %.lr.ph.us.us.us.new, %.lr.ph.us.us.us
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph.us.us.us ], [ %indvars.iv.next.1, %.lr.ph.us.us.us.new ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph.us.us.us ], [ %38, %.lr.ph.us.us.us.new ]
  br i1 %lcmp.mod.not, label %._crit_edge.us.us.us, label %._crit_edge.us.us.us.epilog-lcssa

._crit_edge.us.us.us.epilog-lcssa:                ; preds = %._crit_edge.us.us.us.unr-lcssa
  %39 = getelementptr inbounds nuw double, ptr %26, i64 %indvars.iv.unr
  %40 = load double, ptr %39, align 8
  %41 = mul nuw nsw i64 %indvars.iv.unr, %13
  %gep.us.us.us.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us, i64 %41
  %42 = load double, ptr %gep.us.us.us.epil, align 8
  %43 = tail call double @llvm.fmuladd.f64(double %40, double %42, double %.unr)
  store double %43, ptr %27, align 8
  br label %._crit_edge.us.us.us

._crit_edge.us.us.us:                             ; preds = %._crit_edge.us.us.us.unr-lcssa, %._crit_edge.us.us.us.epilog-lcssa
  %indvars.iv.next134 = add nuw nsw i64 %indvars.iv133, 1
  %exitcond137.not = icmp eq i64 %indvars.iv.next134, %13
  br i1 %exitcond137.not, label %._crit_edge93.split.us.us.us, label %.lr.ph.us.us.us, !llvm.loop !18

._crit_edge93.split.us.us.us:                     ; preds = %._crit_edge.us.us.us
  %indvars.iv.next139 = add nuw nsw i64 %indvars.iv138, 1
  %exitcond142.not = icmp eq i64 %indvars.iv.next139, %wide.trip.count141
  br i1 %exitcond142.not, label %.preheader88, label %.preheader89.us.us, !llvm.loop !19

.preheader88:                                     ; preds = %._crit_edge93.split.us.us.us, %12
  %44 = icmp sgt i32 %1, 0
  br i1 %44, label %.preheader87.lr.ph, label %.preheader86

.preheader87.lr.ph:                               ; preds = %.preheader88.thread, %.preheader88
  %45 = icmp sgt i32 %3, 0
  br i1 %45, label %.preheader87.lr.ph.split.us, label %.preheader86

.preheader87.lr.ph.split.us:                      ; preds = %.preheader87.lr.ph
  %46 = icmp sgt i32 %4, 0
  br i1 %46, label %.preheader87.us.us.preheader, label %.preheader87.us.preheader

.preheader87.us.us.preheader:                     ; preds = %.preheader87.lr.ph.split.us
  %xtraiter183 = and i64 %16, 1
  %47 = icmp eq i32 %4, 1
  %unroll_iter186 = and i64 %16, 2147483646
  %lcmp.mod185.not = icmp eq i64 %xtraiter183, 0
  br label %.preheader87.us.us

.preheader87.us.preheader:                        ; preds = %.preheader87.lr.ph.split.us
  %48 = mul nuw nsw i64 %15, %13
  %49 = shl i64 %48, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %8, i8 0, i64 %49, i1 false)
  br label %.preheader86

.preheader87.us.us:                               ; preds = %.preheader87.us.us.preheader, %._crit_edge101.split.us.us.us
  %indvars.iv157 = phi i64 [ %indvars.iv.next158, %._crit_edge101.split.us.us.us ], [ 0, %.preheader87.us.us.preheader ]
  %50 = mul nuw nsw i64 %indvars.iv157, %15
  %51 = getelementptr inbounds nuw double, ptr %8, i64 %50
  %52 = mul nuw nsw i64 %indvars.iv157, %16
  %53 = getelementptr inbounds nuw double, ptr %9, i64 %52
  br label %.lr.ph.us.us.us106

.lr.ph.us.us.us106:                               ; preds = %._crit_edge.us.us.us110, %.preheader87.us.us
  %indvars.iv152 = phi i64 [ %indvars.iv.next153, %._crit_edge.us.us.us110 ], [ 0, %.preheader87.us.us ]
  %54 = getelementptr inbounds nuw double, ptr %51, i64 %indvars.iv152
  store double 0.000000e+00, ptr %54, align 8
  %invariant.gep.us.us.us107 = getelementptr inbounds nuw double, ptr %10, i64 %indvars.iv152
  br i1 %47, label %._crit_edge.us.us.us110.unr-lcssa, label %.lr.ph.us.us.us106.new

.lr.ph.us.us.us106.new:                           ; preds = %.lr.ph.us.us.us106, %.lr.ph.us.us.us106.new
  %indvars.iv147 = phi i64 [ %indvars.iv.next148.1, %.lr.ph.us.us.us106.new ], [ 0, %.lr.ph.us.us.us106 ]
  %55 = phi double [ %65, %.lr.ph.us.us.us106.new ], [ 0.000000e+00, %.lr.ph.us.us.us106 ]
  %niter187 = phi i64 [ %niter187.next.1, %.lr.ph.us.us.us106.new ], [ 0, %.lr.ph.us.us.us106 ]
  %56 = getelementptr inbounds nuw double, ptr %53, i64 %indvars.iv147
  %57 = load double, ptr %56, align 8
  %58 = mul nuw nsw i64 %indvars.iv147, %15
  %gep.us.us.us109 = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us107, i64 %58
  %59 = load double, ptr %gep.us.us.us109, align 8
  %60 = tail call double @llvm.fmuladd.f64(double %57, double %59, double %55)
  store double %60, ptr %54, align 8
  %indvars.iv.next148 = or disjoint i64 %indvars.iv147, 1
  %61 = getelementptr inbounds nuw double, ptr %53, i64 %indvars.iv.next148
  %62 = load double, ptr %61, align 8
  %63 = mul nuw nsw i64 %indvars.iv.next148, %15
  %gep.us.us.us109.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us107, i64 %63
  %64 = load double, ptr %gep.us.us.us109.1, align 8
  %65 = tail call double @llvm.fmuladd.f64(double %62, double %64, double %60)
  store double %65, ptr %54, align 8
  %indvars.iv.next148.1 = add nuw nsw i64 %indvars.iv147, 2
  %niter187.next.1 = add i64 %niter187, 2
  %niter187.ncmp.1 = icmp eq i64 %niter187.next.1, %unroll_iter186
  br i1 %niter187.ncmp.1, label %._crit_edge.us.us.us110.unr-lcssa, label %.lr.ph.us.us.us106.new, !llvm.loop !20

._crit_edge.us.us.us110.unr-lcssa:                ; preds = %.lr.ph.us.us.us106.new, %.lr.ph.us.us.us106
  %indvars.iv147.unr = phi i64 [ 0, %.lr.ph.us.us.us106 ], [ %indvars.iv.next148.1, %.lr.ph.us.us.us106.new ]
  %.unr184 = phi double [ 0.000000e+00, %.lr.ph.us.us.us106 ], [ %65, %.lr.ph.us.us.us106.new ]
  br i1 %lcmp.mod185.not, label %._crit_edge.us.us.us110, label %._crit_edge.us.us.us110.epilog-lcssa

._crit_edge.us.us.us110.epilog-lcssa:             ; preds = %._crit_edge.us.us.us110.unr-lcssa
  %66 = getelementptr inbounds nuw double, ptr %53, i64 %indvars.iv147.unr
  %67 = load double, ptr %66, align 8
  %68 = mul nuw nsw i64 %indvars.iv147.unr, %15
  %gep.us.us.us109.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us107, i64 %68
  %69 = load double, ptr %gep.us.us.us109.epil, align 8
  %70 = tail call double @llvm.fmuladd.f64(double %67, double %69, double %.unr184)
  store double %70, ptr %54, align 8
  br label %._crit_edge.us.us.us110

._crit_edge.us.us.us110:                          ; preds = %._crit_edge.us.us.us110.unr-lcssa, %._crit_edge.us.us.us110.epilog-lcssa
  %indvars.iv.next153 = add nuw nsw i64 %indvars.iv152, 1
  %exitcond156.not = icmp eq i64 %indvars.iv.next153, %15
  br i1 %exitcond156.not, label %._crit_edge101.split.us.us.us, label %.lr.ph.us.us.us106, !llvm.loop !21

._crit_edge101.split.us.us.us:                    ; preds = %._crit_edge.us.us.us110
  %indvars.iv.next158 = add nuw nsw i64 %indvars.iv157, 1
  %exitcond161.not = icmp eq i64 %indvars.iv.next158, %13
  br i1 %exitcond161.not, label %.preheader86, label %.preheader87.us.us, !llvm.loop !22

.preheader86:                                     ; preds = %._crit_edge101.split.us.us.us, %.preheader87.lr.ph, %.preheader87.us.preheader, %.preheader88
  %71 = phi i1 [ true, %.preheader87.us.preheader ], [ false, %.preheader88 ], [ true, %.preheader87.lr.ph ], [ true, %._crit_edge101.split.us.us.us ]
  %72 = icmp sgt i32 %3, 0
  %or.cond = and i1 %17, %72
  br i1 %or.cond, label %.preheader.lr.ph.split.us, label %._crit_edge

.preheader.lr.ph.thread:                          ; preds = %.preheader89.lr.ph
  %73 = icmp sgt i32 %3, 0
  br i1 %73, label %.preheader.us.preheader, label %._crit_edge

.preheader.lr.ph.split.us:                        ; preds = %.preheader86
  br i1 %71, label %.preheader.us.us.preheader, label %.preheader.us.preheader

.preheader.us.preheader:                          ; preds = %.preheader.lr.ph.thread, %.preheader.lr.ph.split.us
  %74 = zext nneg i32 %0 to i64
  %75 = mul nuw nsw i64 %15, %74
  %76 = shl i64 %75, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %11, i8 0, i64 %76, i1 false)
  br label %._crit_edge

.preheader.us.us.preheader:                       ; preds = %.preheader.lr.ph.split.us
  %wide.trip.count179 = zext nneg i32 %0 to i64
  %xtraiter189 = and i64 %13, 1
  %77 = icmp eq i32 %1, 1
  %unroll_iter192 = and i64 %13, 4294967294
  %lcmp.mod191.not = icmp eq i64 %xtraiter189, 0
  br label %.preheader.us.us

.preheader.us.us:                                 ; preds = %.preheader.us.us.preheader, %._crit_edge114.split.us.us.us
  %indvars.iv176 = phi i64 [ 0, %.preheader.us.us.preheader ], [ %indvars.iv.next177, %._crit_edge114.split.us.us.us ]
  %78 = mul nuw nsw i64 %indvars.iv176, %15
  %79 = getelementptr inbounds nuw double, ptr %11, i64 %78
  %80 = mul nuw nsw i64 %indvars.iv176, %13
  %81 = getelementptr inbounds nuw double, ptr %5, i64 %80
  br label %.lr.ph.us.us.us119

.lr.ph.us.us.us119:                               ; preds = %._crit_edge.us.us.us123, %.preheader.us.us
  %indvars.iv171 = phi i64 [ %indvars.iv.next172, %._crit_edge.us.us.us123 ], [ 0, %.preheader.us.us ]
  %82 = getelementptr inbounds nuw double, ptr %79, i64 %indvars.iv171
  store double 0.000000e+00, ptr %82, align 8
  %invariant.gep.us.us.us120 = getelementptr inbounds nuw double, ptr %8, i64 %indvars.iv171
  br i1 %77, label %._crit_edge.us.us.us123.unr-lcssa, label %.lr.ph.us.us.us119.new

.lr.ph.us.us.us119.new:                           ; preds = %.lr.ph.us.us.us119, %.lr.ph.us.us.us119.new
  %indvars.iv166 = phi i64 [ %indvars.iv.next167.1, %.lr.ph.us.us.us119.new ], [ 0, %.lr.ph.us.us.us119 ]
  %83 = phi double [ %93, %.lr.ph.us.us.us119.new ], [ 0.000000e+00, %.lr.ph.us.us.us119 ]
  %niter193 = phi i64 [ %niter193.next.1, %.lr.ph.us.us.us119.new ], [ 0, %.lr.ph.us.us.us119 ]
  %84 = getelementptr inbounds nuw double, ptr %81, i64 %indvars.iv166
  %85 = load double, ptr %84, align 8
  %86 = mul nuw nsw i64 %indvars.iv166, %15
  %gep.us.us.us122 = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us120, i64 %86
  %87 = load double, ptr %gep.us.us.us122, align 8
  %88 = tail call double @llvm.fmuladd.f64(double %85, double %87, double %83)
  store double %88, ptr %82, align 8
  %indvars.iv.next167 = or disjoint i64 %indvars.iv166, 1
  %89 = getelementptr inbounds nuw double, ptr %81, i64 %indvars.iv.next167
  %90 = load double, ptr %89, align 8
  %91 = mul nuw nsw i64 %indvars.iv.next167, %15
  %gep.us.us.us122.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us120, i64 %91
  %92 = load double, ptr %gep.us.us.us122.1, align 8
  %93 = tail call double @llvm.fmuladd.f64(double %90, double %92, double %88)
  store double %93, ptr %82, align 8
  %indvars.iv.next167.1 = add nuw nsw i64 %indvars.iv166, 2
  %niter193.next.1 = add i64 %niter193, 2
  %niter193.ncmp.1 = icmp eq i64 %niter193.next.1, %unroll_iter192
  br i1 %niter193.ncmp.1, label %._crit_edge.us.us.us123.unr-lcssa, label %.lr.ph.us.us.us119.new, !llvm.loop !23

._crit_edge.us.us.us123.unr-lcssa:                ; preds = %.lr.ph.us.us.us119.new, %.lr.ph.us.us.us119
  %indvars.iv166.unr = phi i64 [ 0, %.lr.ph.us.us.us119 ], [ %indvars.iv.next167.1, %.lr.ph.us.us.us119.new ]
  %.unr190 = phi double [ 0.000000e+00, %.lr.ph.us.us.us119 ], [ %93, %.lr.ph.us.us.us119.new ]
  br i1 %lcmp.mod191.not, label %._crit_edge.us.us.us123, label %._crit_edge.us.us.us123.epilog-lcssa

._crit_edge.us.us.us123.epilog-lcssa:             ; preds = %._crit_edge.us.us.us123.unr-lcssa
  %94 = getelementptr inbounds nuw double, ptr %81, i64 %indvars.iv166.unr
  %95 = load double, ptr %94, align 8
  %96 = mul nuw nsw i64 %indvars.iv166.unr, %15
  %gep.us.us.us122.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us.us.us120, i64 %96
  %97 = load double, ptr %gep.us.us.us122.epil, align 8
  %98 = tail call double @llvm.fmuladd.f64(double %95, double %97, double %.unr190)
  store double %98, ptr %82, align 8
  br label %._crit_edge.us.us.us123

._crit_edge.us.us.us123:                          ; preds = %._crit_edge.us.us.us123.unr-lcssa, %._crit_edge.us.us.us123.epilog-lcssa
  %indvars.iv.next172 = add nuw nsw i64 %indvars.iv171, 1
  %exitcond175.not = icmp eq i64 %indvars.iv.next172, %15
  br i1 %exitcond175.not, label %._crit_edge114.split.us.us.us, label %.lr.ph.us.us.us119, !llvm.loop !24

._crit_edge114.split.us.us.us:                    ; preds = %._crit_edge.us.us.us123
  %indvars.iv.next177 = add nuw nsw i64 %indvars.iv176, 1
  %exitcond180.not = icmp eq i64 %indvars.iv.next177, %wide.trip.count179
  br i1 %exitcond180.not, label %._crit_edge, label %.preheader.us.us, !llvm.loop !25

._crit_edge:                                      ; preds = %._crit_edge114.split.us.us.us, %.preheader.lr.ph.thread, %.preheader.us.preheader, %.preheader86
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #3 {
  %1 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %2 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %3 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %4 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %5 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %6 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  %7 = tail call dereferenceable_or_null(131072) ptr @malloc(i64 noundef 131072) #8
  tail call void @init_array(i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4)
  %8 = tail call i32 @clock() #9
  tail call void @mm3(i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, i32 noundef 128, ptr noundef %5, ptr noundef %1, ptr noundef %2, ptr noundef %6, ptr noundef %3, ptr noundef %4, ptr noundef %7)
  %9 = tail call i32 @clock() #9
  %10 = sub nsw i32 %9, %8
  %11 = sitofp i32 %10 to double
  %12 = fdiv double %11, 1.000000e+03
  %13 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %12) #9
  %14 = load double, ptr %7, align 8
  %15 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %14) #9
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

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #7

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nocallback nofree nounwind willreturn memory(argmem: write) }
attributes #8 = { allocsize(0) }
attributes #9 = { nounwind }

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
