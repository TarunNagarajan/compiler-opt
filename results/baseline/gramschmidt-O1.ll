; ModuleID = 'results\baseline\gramschmidt_base.ll'
source_filename = "benchmarks\\gramschmidt.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [34 x i8] c"Gramschmidt Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef writeonly captures(none) %2) local_unnamed_addr #0 {
  %4 = zext i32 %1 to i64
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader.lr.ph, label %._crit_edge17

.preheader.lr.ph:                                 ; preds = %3
  %6 = icmp sgt i32 %1, 0
  %7 = sitofp i32 %0 to double
  %wide.trip.count22 = zext nneg i32 %0 to i64
  %8 = zext i32 %1 to i64
  %xtraiter = and i64 %8, 3
  %9 = icmp ult i32 %1, 4
  %unroll_iter = and i64 %8, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv19 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next20, %._crit_edge ]
  br i1 %6, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader
  %10 = trunc nuw nsw i64 %indvars.iv19 to i32
  %11 = uitofp nneg i32 %10 to double
  %12 = mul nuw nsw i64 %indvars.iv19, %4
  %13 = getelementptr inbounds nuw double, ptr %2, i64 %12
  br i1 %9, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %14 = trunc nuw nsw i64 %indvars.iv to i32
  %15 = uitofp nneg i32 %14 to double
  %16 = fmul double %11, %15
  %17 = fdiv double %16, %7
  %18 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv
  store double %17, ptr %18, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %19 = trunc nuw nsw i64 %indvars.iv.next to i32
  %20 = uitofp nneg i32 %19 to double
  %21 = fmul double %11, %20
  %22 = fdiv double %21, %7
  %23 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.next
  store double %22, ptr %23, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %24 = trunc nuw nsw i64 %indvars.iv.next.1 to i32
  %25 = uitofp nneg i32 %24 to double
  %26 = fmul double %11, %25
  %27 = fdiv double %26, %7
  %28 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.next.1
  store double %27, ptr %28, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %29 = trunc nuw nsw i64 %indvars.iv.next.2 to i32
  %30 = uitofp nneg i32 %29 to double
  %31 = fmul double %11, %30
  %32 = fdiv double %31, %7
  %33 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.next.2
  store double %32, ptr %33, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !8

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %.epil.preheader

.epil.preheader:                                  ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %34 = trunc nuw nsw i64 %indvars.iv.epil to i32
  %35 = uitofp nneg i32 %34 to double
  %36 = fmul double %11, %35
  %37 = fdiv double %36, %7
  %38 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.epil
  store double %37, ptr %38, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %._crit_edge, label %.epil.preheader, !llvm.loop !10

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader, %.preheader
  %indvars.iv.next20 = add nuw nsw i64 %indvars.iv19, 1
  %exitcond23.not = icmp eq i64 %indvars.iv.next20, %wide.trip.count22
  br i1 %exitcond23.not, label %._crit_edge17, label %.preheader, !llvm.loop !12

._crit_edge17:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable
define dso_local void @gramschmidt(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4) local_unnamed_addr #1 {
  %6 = zext i32 %1 to i64
  %7 = icmp sgt i32 %1, 0
  br i1 %7, label %.preheader76.lr.ph, label %._crit_edge105

.preheader76.lr.ph:                               ; preds = %5
  %8 = icmp sgt i32 %0, 0
  %9 = icmp sgt i32 %0, 0
  %10 = icmp sgt i32 %0, 0
  %11 = icmp sgt i32 %0, 0
  %12 = zext nneg i32 %1 to i64
  %wide.trip.count132 = zext nneg i32 %1 to i64
  %13 = zext i32 %0 to i64
  %14 = add nsw i64 %13, -1
  %xtraiter = and i64 %13, 3
  %15 = icmp ult i32 %0, 4
  %unroll_iter = and i64 %13, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %xtraiter135 = and i64 %13, 1
  %16 = icmp eq i64 %14, 0
  %unroll_iter138 = and i64 %13, 2147483646
  %lcmp.mod137.not = icmp eq i64 %xtraiter135, 0
  %wide.trip.count127 = zext nneg i32 %1 to i64
  %xtraiter141 = and i64 %13, 1
  %17 = icmp eq i64 %14, 0
  %unroll_iter144 = and i64 %13, 2147483646
  %lcmp.mod143.not = icmp eq i64 %xtraiter141, 0
  %xtraiter146 = and i64 %13, 1
  %18 = icmp eq i64 %14, 0
  %unroll_iter149 = and i64 %13, 2147483646
  %lcmp.mod148.not = icmp eq i64 %xtraiter146, 0
  br label %.preheader76

.loopexit:                                        ; preds = %._crit_edge100, %._crit_edge86
  %indvars.iv.next123 = add nuw nsw i64 %indvars.iv122, 1
  %exitcond133.not = icmp eq i64 %indvars.iv.next130, %wide.trip.count132
  br i1 %exitcond133.not, label %._crit_edge105, label %.preheader76, !llvm.loop !13

.preheader76:                                     ; preds = %.preheader76.lr.ph, %.loopexit
  %indvars.iv129 = phi i64 [ 0, %.preheader76.lr.ph ], [ %indvars.iv.next130, %.loopexit ]
  %indvars.iv122 = phi i64 [ 1, %.preheader76.lr.ph ], [ %indvars.iv.next123, %.loopexit ]
  br i1 %8, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader76
  %invariant.gep = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv129
  br i1 %15, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %.07277 = phi double [ %30, %.lr.ph.new ], [ 0.000000e+00, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %19 = mul nuw nsw i64 %indvars.iv, %6
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %19
  %20 = load double, ptr %gep, align 8
  %21 = tail call double @llvm.fmuladd.f64(double %20, double %20, double %.07277)
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %22 = mul nuw nsw i64 %indvars.iv.next, %6
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %22
  %23 = load double, ptr %gep.1, align 8
  %24 = tail call double @llvm.fmuladd.f64(double %23, double %23, double %21)
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %25 = mul nuw nsw i64 %indvars.iv.next.1, %6
  %gep.2 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %25
  %26 = load double, ptr %gep.2, align 8
  %27 = tail call double @llvm.fmuladd.f64(double %26, double %26, double %24)
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %28 = mul nuw nsw i64 %indvars.iv.next.2, %6
  %gep.3 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %28
  %29 = load double, ptr %gep.3, align 8
  %30 = tail call double @llvm.fmuladd.f64(double %29, double %29, double %27)
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !14

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %.lcssa.ph = phi double [ poison, %.lr.ph ], [ %30, %.lr.ph.new ]
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %.lr.ph.new ]
  %.07277.unr = phi double [ 0.000000e+00, %.lr.ph ], [ %30, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %.epil.preheader

.epil.preheader:                                  ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %._crit_edge.loopexit.unr-lcssa ]
  %.07277.epil = phi double [ %33, %.epil.preheader ], [ %.07277.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %31 = mul nuw nsw i64 %indvars.iv.epil, %6
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %31
  %32 = load double, ptr %gep.epil, align 8
  %33 = tail call double @llvm.fmuladd.f64(double %32, double %32, double %.07277.epil)
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %._crit_edge, label %.epil.preheader, !llvm.loop !15

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader, %.preheader76
  %.072.lcssa = phi double [ 0.000000e+00, %.preheader76 ], [ %.lcssa.ph, %._crit_edge.loopexit.unr-lcssa ], [ %33, %.epil.preheader ]
  %34 = tail call double @sqrt(double noundef %.072.lcssa) #8
  %35 = mul nuw nsw i64 %indvars.iv129, %6
  %36 = getelementptr inbounds nuw double, ptr %3, i64 %35
  %37 = getelementptr inbounds nuw double, ptr %36, i64 %indvars.iv129
  store double %34, ptr %37, align 8
  %invariant.gep79 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv129
  %invariant.gep81 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  br i1 %9, label %.lr.ph85.preheader, label %._crit_edge86

.lr.ph85.preheader:                               ; preds = %._crit_edge
  br i1 %16, label %._crit_edge86.loopexit.unr-lcssa, label %.lr.ph85

.lr.ph85:                                         ; preds = %.lr.ph85.preheader, %.lr.ph85
  %indvars.iv107 = phi i64 [ %indvars.iv.next108.1, %.lr.ph85 ], [ 0, %.lr.ph85.preheader ]
  %niter139 = phi i64 [ %niter139.next.1, %.lr.ph85 ], [ 0, %.lr.ph85.preheader ]
  %38 = mul nuw nsw i64 %indvars.iv107, %6
  %gep80 = getelementptr inbounds nuw double, ptr %invariant.gep79, i64 %38
  %39 = load double, ptr %gep80, align 8
  %40 = load double, ptr %37, align 8
  %41 = fdiv double %39, %40
  %gep82 = getelementptr inbounds nuw double, ptr %invariant.gep81, i64 %38
  store double %41, ptr %gep82, align 8
  %indvars.iv.next108 = or disjoint i64 %indvars.iv107, 1
  %42 = mul nuw nsw i64 %indvars.iv.next108, %6
  %gep80.1 = getelementptr inbounds nuw double, ptr %invariant.gep79, i64 %42
  %43 = load double, ptr %gep80.1, align 8
  %44 = load double, ptr %37, align 8
  %45 = fdiv double %43, %44
  %gep82.1 = getelementptr inbounds nuw double, ptr %invariant.gep81, i64 %42
  store double %45, ptr %gep82.1, align 8
  %indvars.iv.next108.1 = add nuw nsw i64 %indvars.iv107, 2
  %niter139.next.1 = add i64 %niter139, 2
  %niter139.ncmp.1 = icmp eq i64 %niter139.next.1, %unroll_iter138
  br i1 %niter139.ncmp.1, label %._crit_edge86.loopexit.unr-lcssa, label %.lr.ph85, !llvm.loop !16

._crit_edge86.loopexit.unr-lcssa:                 ; preds = %.lr.ph85, %.lr.ph85.preheader
  %indvars.iv107.unr = phi i64 [ 0, %.lr.ph85.preheader ], [ %indvars.iv.next108.1, %.lr.ph85 ]
  br i1 %lcmp.mod137.not, label %._crit_edge86, label %.lr.ph85.epil

.lr.ph85.epil:                                    ; preds = %._crit_edge86.loopexit.unr-lcssa
  %46 = mul nuw nsw i64 %indvars.iv107.unr, %6
  %gep80.epil = getelementptr inbounds nuw double, ptr %invariant.gep79, i64 %46
  %47 = load double, ptr %gep80.epil, align 8
  %48 = load double, ptr %37, align 8
  %49 = fdiv double %47, %48
  %gep82.epil = getelementptr inbounds nuw double, ptr %invariant.gep81, i64 %46
  store double %49, ptr %gep82.epil, align 8
  br label %._crit_edge86

._crit_edge86:                                    ; preds = %.lr.ph85.epil, %._crit_edge86.loopexit.unr-lcssa, %._crit_edge
  %indvars.iv.next130 = add nuw nsw i64 %indvars.iv129, 1
  %50 = icmp samesign ult i64 %indvars.iv.next130, %12
  br i1 %50, label %.lr.ph103, label %.loopexit

.lr.ph103:                                        ; preds = %._crit_edge86
  %invariant.gep87 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %invariant.gep96 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  br label %51

51:                                               ; preds = %.lr.ph103, %._crit_edge100
  %indvars.iv124 = phi i64 [ %indvars.iv122, %.lr.ph103 ], [ %indvars.iv.next125, %._crit_edge100 ]
  %52 = getelementptr inbounds nuw double, ptr %36, i64 %indvars.iv124
  store double 0.000000e+00, ptr %52, align 8
  %invariant.gep89 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv124
  br i1 %10, label %.lr.ph93, label %.preheader

.lr.ph93:                                         ; preds = %51
  %.promoted = load double, ptr %52, align 8
  br i1 %17, label %.preheader.loopexit.unr-lcssa, label %.lr.ph93.new

.preheader.loopexit.unr-lcssa:                    ; preds = %.lr.ph93.new, %.lr.ph93
  %indvars.iv112.unr = phi i64 [ 0, %.lr.ph93 ], [ %indvars.iv.next113.1, %.lr.ph93.new ]
  %.unr = phi double [ %.promoted, %.lr.ph93 ], [ %65, %.lr.ph93.new ]
  br i1 %lcmp.mod143.not, label %.preheader, label %.preheader.loopexit.epilog-lcssa

.preheader.loopexit.epilog-lcssa:                 ; preds = %.preheader.loopexit.unr-lcssa
  %53 = mul nuw nsw i64 %indvars.iv112.unr, %6
  %gep88.epil = getelementptr inbounds nuw double, ptr %invariant.gep87, i64 %53
  %54 = load double, ptr %gep88.epil, align 8
  %gep90.epil = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %53
  %55 = load double, ptr %gep90.epil, align 8
  %56 = tail call double @llvm.fmuladd.f64(double %54, double %55, double %.unr)
  store double %56, ptr %52, align 8
  br label %.preheader

.preheader:                                       ; preds = %.preheader.loopexit.epilog-lcssa, %.preheader.loopexit.unr-lcssa, %51
  %invariant.gep94 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv124
  br i1 %11, label %.lr.ph99.preheader, label %._crit_edge100

.lr.ph99.preheader:                               ; preds = %.preheader
  br i1 %18, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99

.lr.ph93.new:                                     ; preds = %.lr.ph93, %.lr.ph93.new
  %indvars.iv112 = phi i64 [ %indvars.iv.next113.1, %.lr.ph93.new ], [ 0, %.lr.ph93 ]
  %57 = phi double [ %65, %.lr.ph93.new ], [ %.promoted, %.lr.ph93 ]
  %niter145 = phi i64 [ %niter145.next.1, %.lr.ph93.new ], [ 0, %.lr.ph93 ]
  %58 = mul nuw nsw i64 %indvars.iv112, %6
  %gep88 = getelementptr inbounds nuw double, ptr %invariant.gep87, i64 %58
  %59 = load double, ptr %gep88, align 8
  %gep90 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %58
  %60 = load double, ptr %gep90, align 8
  %61 = tail call double @llvm.fmuladd.f64(double %59, double %60, double %57)
  store double %61, ptr %52, align 8
  %indvars.iv.next113 = or disjoint i64 %indvars.iv112, 1
  %62 = mul nuw nsw i64 %indvars.iv.next113, %6
  %gep88.1 = getelementptr inbounds nuw double, ptr %invariant.gep87, i64 %62
  %63 = load double, ptr %gep88.1, align 8
  %gep90.1 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %62
  %64 = load double, ptr %gep90.1, align 8
  %65 = tail call double @llvm.fmuladd.f64(double %63, double %64, double %61)
  store double %65, ptr %52, align 8
  %indvars.iv.next113.1 = add nuw nsw i64 %indvars.iv112, 2
  %niter145.next.1 = add i64 %niter145, 2
  %niter145.ncmp.1 = icmp eq i64 %niter145.next.1, %unroll_iter144
  br i1 %niter145.ncmp.1, label %.preheader.loopexit.unr-lcssa, label %.lr.ph93.new, !llvm.loop !17

.lr.ph99:                                         ; preds = %.lr.ph99.preheader, %.lr.ph99
  %indvars.iv117 = phi i64 [ %indvars.iv.next118.1, %.lr.ph99 ], [ 0, %.lr.ph99.preheader ]
  %niter150 = phi i64 [ %niter150.next.1, %.lr.ph99 ], [ 0, %.lr.ph99.preheader ]
  %66 = mul nuw nsw i64 %indvars.iv117, %6
  %gep95 = getelementptr inbounds nuw double, ptr %invariant.gep94, i64 %66
  %67 = load double, ptr %gep95, align 8
  %gep97 = getelementptr inbounds nuw double, ptr %invariant.gep96, i64 %66
  %68 = load double, ptr %gep97, align 8
  %69 = load double, ptr %52, align 8
  %70 = fneg double %68
  %71 = tail call double @llvm.fmuladd.f64(double %70, double %69, double %67)
  store double %71, ptr %gep95, align 8
  %indvars.iv.next118 = or disjoint i64 %indvars.iv117, 1
  %72 = mul nuw nsw i64 %indvars.iv.next118, %6
  %gep95.1 = getelementptr inbounds nuw double, ptr %invariant.gep94, i64 %72
  %73 = load double, ptr %gep95.1, align 8
  %gep97.1 = getelementptr inbounds nuw double, ptr %invariant.gep96, i64 %72
  %74 = load double, ptr %gep97.1, align 8
  %75 = load double, ptr %52, align 8
  %76 = fneg double %74
  %77 = tail call double @llvm.fmuladd.f64(double %76, double %75, double %73)
  store double %77, ptr %gep95.1, align 8
  %indvars.iv.next118.1 = add nuw nsw i64 %indvars.iv117, 2
  %niter150.next.1 = add i64 %niter150, 2
  %niter150.ncmp.1 = icmp eq i64 %niter150.next.1, %unroll_iter149
  br i1 %niter150.ncmp.1, label %._crit_edge100.loopexit.unr-lcssa, label %.lr.ph99, !llvm.loop !18

._crit_edge100.loopexit.unr-lcssa:                ; preds = %.lr.ph99, %.lr.ph99.preheader
  %indvars.iv117.unr = phi i64 [ 0, %.lr.ph99.preheader ], [ %indvars.iv.next118.1, %.lr.ph99 ]
  br i1 %lcmp.mod148.not, label %._crit_edge100, label %.lr.ph99.epil

.lr.ph99.epil:                                    ; preds = %._crit_edge100.loopexit.unr-lcssa
  %78 = mul nuw nsw i64 %indvars.iv117.unr, %6
  %gep95.epil = getelementptr inbounds nuw double, ptr %invariant.gep94, i64 %78
  %79 = load double, ptr %gep95.epil, align 8
  %gep97.epil = getelementptr inbounds nuw double, ptr %invariant.gep96, i64 %78
  %80 = load double, ptr %gep97.epil, align 8
  %81 = load double, ptr %52, align 8
  %82 = fneg double %80
  %83 = tail call double @llvm.fmuladd.f64(double %82, double %81, double %79)
  store double %83, ptr %gep95.epil, align 8
  br label %._crit_edge100

._crit_edge100:                                   ; preds = %.lr.ph99.epil, %._crit_edge100.loopexit.unr-lcssa, %.preheader
  %indvars.iv.next125 = add nuw nsw i64 %indvars.iv124, 1
  %exitcond128.not = icmp eq i64 %indvars.iv.next125, %wide.trip.count127
  br i1 %exitcond128.not, label %.loopexit, label %51, !llvm.loop !19

._crit_edge105:                                   ; preds = %.loopexit, %5
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: mustprogress nocallback nofree nounwind willreturn memory(errnomem: write)
declare dso_local double @sqrt(double noundef) local_unnamed_addr #3

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #4 {
  %1 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #9
  %2 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #9
  %3 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #9
  tail call void @init_array(i32 noundef 256, i32 noundef 256, ptr noundef %1)
  %4 = tail call i32 @clock() #8
  tail call void @gramschmidt(i32 noundef 256, i32 noundef 256, ptr noundef %1, ptr noundef %2, ptr noundef %3)
  %5 = tail call i32 @clock() #8
  %6 = sub nsw i32 %5, %4
  %7 = sitofp i32 %6 to double
  %8 = fdiv double %7, 1.000000e+03
  %9 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %8) #8
  %10 = load double, ptr %2, align 8
  %11 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %10) #8
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  ret i32 0
}

; Function Attrs: mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite)
declare dso_local noalias noundef ptr @malloc(i64 noundef) local_unnamed_addr #5

declare dso_local i32 @clock() local_unnamed_addr #6

declare dso_local i32 @__mingw_printf(ptr noundef, ...) local_unnamed_addr #6

; Function Attrs: mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite)
declare dso_local void @free(ptr allocptr noundef captures(none)) local_unnamed_addr #7

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { mustprogress nocallback nofree nounwind willreturn memory(errnomem: write) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #8 = { nounwind }
attributes #9 = { allocsize(0) }

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
!10 = distinct !{!10, !11}
!11 = !{!"llvm.loop.unroll.disable"}
!12 = distinct !{!12, !9}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !11}
!16 = distinct !{!16, !9}
!17 = distinct !{!17, !9}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
