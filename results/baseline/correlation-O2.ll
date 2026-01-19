; ModuleID = 'results\baseline\correlation_base.ll'
source_filename = "benchmarks\\correlation.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [34 x i8] c"Correlation Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef writeonly captures(none) %2) local_unnamed_addr #0 {
  %4 = zext i32 %1 to i64
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader.lr.ph, label %._crit_edge15

.preheader.lr.ph:                                 ; preds = %3
  %6 = icmp sgt i32 %1, 0
  %wide.trip.count20 = zext nneg i32 %0 to i64
  %min.iters.check = icmp eq i32 %1, 1
  %n.vec = and i64 %4, 2147483646
  %cmp.n = icmp eq i64 %n.vec, %4
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv17 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next18, %._crit_edge ]
  br i1 %6, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader
  %7 = trunc nuw nsw i64 %indvars.iv17 to i32
  %8 = uitofp nneg i32 %7 to double
  %9 = mul nuw nsw i64 %indvars.iv17, %4
  %10 = getelementptr inbounds nuw double, ptr %2, i64 %9
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %broadcast.splatinsert = insertelement <2 x double> poison, double %8, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %11 = uitofp nneg <2 x i32> %vec.ind to <2 x double>
  %12 = fmul <2 x double> %broadcast.splat, %11
  %13 = fdiv <2 x double> %12, splat (double 1.000000e+03)
  %14 = getelementptr inbounds nuw double, ptr %10, i64 %index
  store <2 x double> %13, ptr %14, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %15 = icmp eq i64 %index.next, %n.vec
  br i1 %15, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  br label %scalar.ph

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %16 = trunc nuw nsw i64 %indvars.iv to i32
  %17 = uitofp nneg i32 %16 to double
  %18 = fmul double %8, %17
  %19 = fdiv double %18, 1.000000e+03
  %20 = getelementptr inbounds nuw double, ptr %10, i64 %indvars.iv
  store double %19, ptr %20, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %4
  br i1 %exitcond.not, label %._crit_edge, label %scalar.ph, !llvm.loop !12

._crit_edge:                                      ; preds = %scalar.ph, %middle.block, %.preheader
  %indvars.iv.next18 = add nuw nsw i64 %indvars.iv17, 1
  %exitcond21.not = icmp eq i64 %indvars.iv.next18, %wide.trip.count20
  br i1 %exitcond21.not, label %._crit_edge15, label %.preheader, !llvm.loop !13

._crit_edge15:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable
define dso_local void @correlation(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4, ptr noundef writeonly captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %1 to i64
  %8 = zext i32 %0 to i64
  %9 = icmp sgt i32 %0, 0
  br i1 %9, label %.lr.ph121, label %.preheader116

.lr.ph121:                                        ; preds = %6
  %10 = icmp sgt i32 %1, 0
  %11 = sitofp i32 %1 to double
  %xtraiter = and i64 %7, 3
  %12 = icmp ult i32 %1, 4
  %unroll_iter = and i64 %7, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %16

.lr.ph129:                                        ; preds = %._crit_edge
  %13 = icmp sgt i32 %1, 0
  %14 = sitofp i32 %1 to double
  %xtraiter197 = and i64 %7, 1
  %15 = icmp eq i32 %1, 1
  %unroll_iter202 = and i64 %7, 2147483646
  %lcmp.mod200.not = icmp eq i64 %xtraiter197, 0
  br label %40

16:                                               ; preds = %.lr.ph121, %._crit_edge
  %indvars.iv148 = phi i64 [ 0, %.lr.ph121 ], [ %indvars.iv.next149, %._crit_edge ]
  %17 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv148
  store double 0.000000e+00, ptr %17, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv148
  br i1 %10, label %.lr.ph.preheader, label %._crit_edge

.lr.ph.preheader:                                 ; preds = %16
  br i1 %12, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph

.lr.ph:                                           ; preds = %.lr.ph.preheader, %.lr.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph ], [ 0, %.lr.ph.preheader ]
  %18 = phi double [ %30, %.lr.ph ], [ 0.000000e+00, %.lr.ph.preheader ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph ], [ 0, %.lr.ph.preheader ]
  %19 = mul nuw nsw i64 %indvars.iv, %7
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %19
  %20 = load double, ptr %gep, align 8
  %21 = fadd double %20, %18
  store double %21, ptr %17, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %22 = mul nuw nsw i64 %indvars.iv.next, %7
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %22
  %23 = load double, ptr %gep.1, align 8
  %24 = fadd double %23, %21
  store double %24, ptr %17, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %25 = mul nuw nsw i64 %indvars.iv.next.1, %7
  %gep.2 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %25
  %26 = load double, ptr %gep.2, align 8
  %27 = fadd double %26, %24
  store double %27, ptr %17, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %28 = mul nuw nsw i64 %indvars.iv.next.2, %7
  %gep.3 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %28
  %29 = load double, ptr %gep.3, align 8
  %30 = fadd double %29, %27
  store double %30, ptr %17, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph, !llvm.loop !14

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph, %.lr.ph.preheader
  %.lcssa195.ph = phi double [ poison, %.lr.ph.preheader ], [ %30, %.lr.ph ]
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph.preheader ], [ %indvars.iv.next.3, %.lr.ph ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph.preheader ], [ %30, %.lr.ph ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %.lr.ph.epil

.lr.ph.epil:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.lr.ph.epil
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.lr.ph.epil ], [ %indvars.iv.unr, %._crit_edge.loopexit.unr-lcssa ]
  %31 = phi double [ %34, %.lr.ph.epil ], [ %.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.lr.ph.epil ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %32 = mul nuw nsw i64 %indvars.iv.epil, %7
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %32
  %33 = load double, ptr %gep.epil, align 8
  %34 = fadd double %33, %31
  store double %34, ptr %17, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %._crit_edge, label %.lr.ph.epil, !llvm.loop !15

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.lr.ph.epil, %16
  %35 = phi double [ 0.000000e+00, %16 ], [ %.lcssa195.ph, %._crit_edge.loopexit.unr-lcssa ], [ %34, %.lr.ph.epil ]
  %36 = fdiv double %35, %11
  store double %36, ptr %17, align 8
  %indvars.iv.next149 = add nuw nsw i64 %indvars.iv148, 1
  %exitcond152.not = icmp eq i64 %indvars.iv.next149, %8
  br i1 %exitcond152.not, label %.lr.ph129, label %16, !llvm.loop !17

.preheader116:                                    ; preds = %._crit_edge127, %6
  %37 = icmp sgt i32 %1, 0
  br i1 %37, label %.preheader115.lr.ph, label %.preheader

.preheader115.lr.ph:                              ; preds = %.preheader116
  %38 = uitofp nneg i32 %1 to double
  %xtraiter205 = and i64 %8, 1
  %39 = icmp eq i32 %0, 1
  %unroll_iter208 = and i64 %8, 2147483646
  %lcmp.mod207.not = icmp eq i64 %xtraiter205, 0
  br label %.preheader115

40:                                               ; preds = %.lr.ph129, %._crit_edge127
  %indvars.iv158 = phi i64 [ 0, %.lr.ph129 ], [ %indvars.iv.next159, %._crit_edge127 ]
  %41 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv158
  store double 0.000000e+00, ptr %41, align 8
  %invariant.gep122 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv158
  br i1 %13, label %.lr.ph126, label %._crit_edge127

.lr.ph126:                                        ; preds = %40
  %42 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv158
  br i1 %15, label %._crit_edge127.loopexit.unr-lcssa, label %.lr.ph126.new

.lr.ph126.new:                                    ; preds = %.lr.ph126, %.lr.ph126.new
  %43 = phi double [ %53, %.lr.ph126.new ], [ 0.000000e+00, %.lr.ph126 ]
  %indvars.iv153 = phi i64 [ %indvars.iv.next154.1, %.lr.ph126.new ], [ 0, %.lr.ph126 ]
  %niter203 = phi i64 [ %niter203.next.1, %.lr.ph126.new ], [ 0, %.lr.ph126 ]
  %44 = mul nuw nsw i64 %indvars.iv153, %7
  %gep123 = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %44
  %45 = load double, ptr %gep123, align 8
  %46 = load double, ptr %42, align 8
  %47 = fsub double %45, %46
  %48 = tail call double @llvm.fmuladd.f64(double %47, double %47, double %43)
  store double %48, ptr %41, align 8
  %indvars.iv.next154 = or disjoint i64 %indvars.iv153, 1
  %49 = mul nuw nsw i64 %indvars.iv.next154, %7
  %gep123.1 = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %49
  %50 = load double, ptr %gep123.1, align 8
  %51 = load double, ptr %42, align 8
  %52 = fsub double %50, %51
  %53 = tail call double @llvm.fmuladd.f64(double %52, double %52, double %48)
  store double %53, ptr %41, align 8
  %indvars.iv.next154.1 = add nuw nsw i64 %indvars.iv153, 2
  %niter203.next.1 = add i64 %niter203, 2
  %niter203.ncmp.1 = icmp eq i64 %niter203.next.1, %unroll_iter202
  br i1 %niter203.ncmp.1, label %._crit_edge127.loopexit.unr-lcssa, label %.lr.ph126.new, !llvm.loop !18

._crit_edge127.loopexit.unr-lcssa:                ; preds = %.lr.ph126.new, %.lr.ph126
  %.lcssa194.ph = phi double [ poison, %.lr.ph126 ], [ %53, %.lr.ph126.new ]
  %.unr199 = phi double [ 0.000000e+00, %.lr.ph126 ], [ %53, %.lr.ph126.new ]
  %indvars.iv153.unr = phi i64 [ 0, %.lr.ph126 ], [ %indvars.iv.next154.1, %.lr.ph126.new ]
  br i1 %lcmp.mod200.not, label %._crit_edge127, label %._crit_edge127.loopexit.epilog-lcssa

._crit_edge127.loopexit.epilog-lcssa:             ; preds = %._crit_edge127.loopexit.unr-lcssa
  %54 = mul nuw nsw i64 %indvars.iv153.unr, %7
  %gep123.epil = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %54
  %55 = load double, ptr %gep123.epil, align 8
  %56 = load double, ptr %42, align 8
  %57 = fsub double %55, %56
  %58 = tail call double @llvm.fmuladd.f64(double %57, double %57, double %.unr199)
  store double %58, ptr %41, align 8
  br label %._crit_edge127

._crit_edge127:                                   ; preds = %._crit_edge127.loopexit.epilog-lcssa, %._crit_edge127.loopexit.unr-lcssa, %40
  %59 = phi double [ 0.000000e+00, %40 ], [ %.lcssa194.ph, %._crit_edge127.loopexit.unr-lcssa ], [ %58, %._crit_edge127.loopexit.epilog-lcssa ]
  %60 = fdiv double %59, %14
  %61 = tail call double @sqrt(double noundef %60) #8
  %62 = fcmp ugt double %61, 1.000000e-01
  %storemerge = select i1 %62, double %61, double 1.000000e+00
  store double %storemerge, ptr %41, align 8
  %indvars.iv.next159 = add nuw nsw i64 %indvars.iv158, 1
  %exitcond162.not = icmp eq i64 %indvars.iv.next159, %8
  br i1 %exitcond162.not, label %.preheader116, label %40, !llvm.loop !19

.preheader115:                                    ; preds = %.preheader115.lr.ph, %._crit_edge132
  %indvars.iv168 = phi i64 [ 0, %.preheader115.lr.ph ], [ %indvars.iv.next169, %._crit_edge132 ]
  br i1 %9, label %.lr.ph131, label %._crit_edge132

.lr.ph131:                                        ; preds = %.preheader115
  %63 = mul nuw nsw i64 %indvars.iv168, %7
  %64 = getelementptr inbounds nuw double, ptr %2, i64 %63
  br i1 %39, label %._crit_edge132.loopexit.unr-lcssa, label %.lr.ph131.new

.preheader:                                       ; preds = %._crit_edge132, %.preheader116
  %65 = add i32 %0, -1
  %66 = icmp sgt i32 %0, 1
  br i1 %66, label %.lr.ph145, label %._crit_edge146

.lr.ph145:                                        ; preds = %.preheader
  %wide.trip.count188 = zext nneg i32 %65 to i64
  %xtraiter210 = and i64 %7, 1
  %67 = icmp eq i32 %1, 1
  %unroll_iter215 = and i64 %7, 2147483646
  %lcmp.mod213.not = icmp eq i64 %xtraiter210, 0
  br label %.lr.ph143.preheader

.lr.ph131.new:                                    ; preds = %.lr.ph131, %.lr.ph131.new
  %indvars.iv163 = phi i64 [ %indvars.iv.next164.1, %.lr.ph131.new ], [ 0, %.lr.ph131 ]
  %niter209 = phi i64 [ %niter209.next.1, %.lr.ph131.new ], [ 0, %.lr.ph131 ]
  %68 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv163
  %69 = load double, ptr %68, align 8
  %70 = getelementptr inbounds nuw double, ptr %64, i64 %indvars.iv163
  %71 = load double, ptr %70, align 8
  %72 = fsub double %71, %69
  store double %72, ptr %70, align 8
  %73 = tail call double @sqrt(double noundef %38) #8
  %74 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv163
  %75 = load double, ptr %74, align 8
  %76 = fmul double %73, %75
  %77 = load double, ptr %70, align 8
  %78 = fdiv double %77, %76
  store double %78, ptr %70, align 8
  %indvars.iv.next164 = or disjoint i64 %indvars.iv163, 1
  %79 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next164
  %80 = load double, ptr %79, align 8
  %81 = getelementptr inbounds nuw double, ptr %64, i64 %indvars.iv.next164
  %82 = load double, ptr %81, align 8
  %83 = fsub double %82, %80
  store double %83, ptr %81, align 8
  %84 = tail call double @sqrt(double noundef %38) #8
  %85 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next164
  %86 = load double, ptr %85, align 8
  %87 = fmul double %84, %86
  %88 = load double, ptr %81, align 8
  %89 = fdiv double %88, %87
  store double %89, ptr %81, align 8
  %indvars.iv.next164.1 = add nuw nsw i64 %indvars.iv163, 2
  %niter209.next.1 = add i64 %niter209, 2
  %niter209.ncmp.1 = icmp eq i64 %niter209.next.1, %unroll_iter208
  br i1 %niter209.ncmp.1, label %._crit_edge132.loopexit.unr-lcssa, label %.lr.ph131.new, !llvm.loop !20

._crit_edge132.loopexit.unr-lcssa:                ; preds = %.lr.ph131.new, %.lr.ph131
  %indvars.iv163.unr = phi i64 [ 0, %.lr.ph131 ], [ %indvars.iv.next164.1, %.lr.ph131.new ]
  br i1 %lcmp.mod207.not, label %._crit_edge132, label %._crit_edge132.loopexit.epilog-lcssa

._crit_edge132.loopexit.epilog-lcssa:             ; preds = %._crit_edge132.loopexit.unr-lcssa
  %90 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv163.unr
  %91 = load double, ptr %90, align 8
  %92 = getelementptr inbounds nuw double, ptr %64, i64 %indvars.iv163.unr
  %93 = load double, ptr %92, align 8
  %94 = fsub double %93, %91
  store double %94, ptr %92, align 8
  %95 = tail call double @sqrt(double noundef %38) #8
  %96 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv163.unr
  %97 = load double, ptr %96, align 8
  %98 = fmul double %95, %97
  %99 = load double, ptr %92, align 8
  %100 = fdiv double %99, %98
  store double %100, ptr %92, align 8
  br label %._crit_edge132

._crit_edge132:                                   ; preds = %._crit_edge132.loopexit.epilog-lcssa, %._crit_edge132.loopexit.unr-lcssa, %.preheader115
  %indvars.iv.next169 = add nuw nsw i64 %indvars.iv168, 1
  %exitcond172.not = icmp eq i64 %indvars.iv.next169, %7
  br i1 %exitcond172.not, label %.preheader, label %.preheader115, !llvm.loop !21

.loopexit:                                        ; preds = %._crit_edge137
  %indvars.iv.next179 = add nuw nsw i64 %indvars.iv178, 1
  %exitcond189.not = icmp eq i64 %indvars.iv.next186, %wide.trip.count188
  br i1 %exitcond189.not, label %._crit_edge146, label %.lr.ph143.preheader, !llvm.loop !22

.lr.ph143.preheader:                              ; preds = %.loopexit, %.lr.ph145
  %indvars.iv185 = phi i64 [ 0, %.lr.ph145 ], [ %indvars.iv.next186, %.loopexit ]
  %indvars.iv178 = phi i64 [ 1, %.lr.ph145 ], [ %indvars.iv.next179, %.loopexit ]
  %101 = mul nuw nsw i64 %indvars.iv185, %8
  %102 = getelementptr inbounds nuw double, ptr %5, i64 %101
  %103 = getelementptr inbounds nuw double, ptr %102, i64 %indvars.iv185
  store double 1.000000e+00, ptr %103, align 8
  %indvars.iv.next186 = add nuw nsw i64 %indvars.iv185, 1
  %invariant.gep139 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv185
  br label %.lr.ph143

.lr.ph143:                                        ; preds = %.lr.ph143.preheader, %._crit_edge137
  %indvars.iv180 = phi i64 [ %indvars.iv178, %.lr.ph143.preheader ], [ %indvars.iv.next181, %._crit_edge137 ]
  %104 = getelementptr inbounds nuw double, ptr %102, i64 %indvars.iv180
  store double 0.000000e+00, ptr %104, align 8
  br i1 %37, label %.lr.ph136.preheader, label %._crit_edge137

.lr.ph136.preheader:                              ; preds = %.lr.ph143
  br i1 %67, label %._crit_edge137.loopexit.unr-lcssa, label %.lr.ph136

.lr.ph136:                                        ; preds = %.lr.ph136.preheader, %.lr.ph136
  %indvars.iv173 = phi i64 [ %indvars.iv.next174.1, %.lr.ph136 ], [ 0, %.lr.ph136.preheader ]
  %105 = phi double [ %119, %.lr.ph136 ], [ 0.000000e+00, %.lr.ph136.preheader ]
  %niter216 = phi i64 [ %niter216.next.1, %.lr.ph136 ], [ 0, %.lr.ph136.preheader ]
  %106 = mul nuw nsw i64 %indvars.iv173, %7
  %107 = getelementptr inbounds nuw double, ptr %2, i64 %106
  %108 = getelementptr inbounds nuw double, ptr %107, i64 %indvars.iv185
  %109 = load double, ptr %108, align 8
  %110 = getelementptr inbounds nuw double, ptr %107, i64 %indvars.iv180
  %111 = load double, ptr %110, align 8
  %112 = tail call double @llvm.fmuladd.f64(double %109, double %111, double %105)
  store double %112, ptr %104, align 8
  %indvars.iv.next174 = or disjoint i64 %indvars.iv173, 1
  %113 = mul nuw nsw i64 %indvars.iv.next174, %7
  %114 = getelementptr inbounds nuw double, ptr %2, i64 %113
  %115 = getelementptr inbounds nuw double, ptr %114, i64 %indvars.iv185
  %116 = load double, ptr %115, align 8
  %117 = getelementptr inbounds nuw double, ptr %114, i64 %indvars.iv180
  %118 = load double, ptr %117, align 8
  %119 = tail call double @llvm.fmuladd.f64(double %116, double %118, double %112)
  store double %119, ptr %104, align 8
  %indvars.iv.next174.1 = add nuw nsw i64 %indvars.iv173, 2
  %niter216.next.1 = add i64 %niter216, 2
  %niter216.ncmp.1 = icmp eq i64 %niter216.next.1, %unroll_iter215
  br i1 %niter216.ncmp.1, label %._crit_edge137.loopexit.unr-lcssa, label %.lr.ph136, !llvm.loop !23

._crit_edge137.loopexit.unr-lcssa:                ; preds = %.lr.ph136, %.lr.ph136.preheader
  %.lcssa.ph = phi double [ poison, %.lr.ph136.preheader ], [ %119, %.lr.ph136 ]
  %indvars.iv173.unr = phi i64 [ 0, %.lr.ph136.preheader ], [ %indvars.iv.next174.1, %.lr.ph136 ]
  %.unr212 = phi double [ 0.000000e+00, %.lr.ph136.preheader ], [ %119, %.lr.ph136 ]
  br i1 %lcmp.mod213.not, label %._crit_edge137, label %.lr.ph136.epil

.lr.ph136.epil:                                   ; preds = %._crit_edge137.loopexit.unr-lcssa
  %120 = mul nuw nsw i64 %indvars.iv173.unr, %7
  %121 = getelementptr inbounds nuw double, ptr %2, i64 %120
  %122 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv185
  %123 = load double, ptr %122, align 8
  %124 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv180
  %125 = load double, ptr %124, align 8
  %126 = tail call double @llvm.fmuladd.f64(double %123, double %125, double %.unr212)
  store double %126, ptr %104, align 8
  br label %._crit_edge137

._crit_edge137:                                   ; preds = %.lr.ph136.epil, %._crit_edge137.loopexit.unr-lcssa, %.lr.ph143
  %127 = phi double [ 0.000000e+00, %.lr.ph143 ], [ %.lcssa.ph, %._crit_edge137.loopexit.unr-lcssa ], [ %126, %.lr.ph136.epil ]
  %128 = mul nuw nsw i64 %indvars.iv180, %8
  %gep140 = getelementptr inbounds nuw double, ptr %invariant.gep139, i64 %128
  store double %127, ptr %gep140, align 8
  %indvars.iv.next181 = add nuw nsw i64 %indvars.iv180, 1
  %exitcond184.not = icmp eq i64 %indvars.iv.next181, %8
  br i1 %exitcond184.not, label %.loopexit, label %.lr.ph143, !llvm.loop !24

._crit_edge146:                                   ; preds = %.loopexit, %.preheader
  %129 = sext i32 %65 to i64
  %130 = mul nsw i64 %129, %8
  %131 = getelementptr inbounds double, ptr %5, i64 %130
  %132 = getelementptr inbounds double, ptr %131, i64 %129
  store double 1.000000e+00, ptr %132, align 8
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: mustprogress nocallback nofree nounwind willreturn memory(errnomem: write)
declare dso_local double @sqrt(double noundef) local_unnamed_addr #3

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #4 {
  %1 = tail call dereferenceable_or_null(2000000) ptr @malloc(i64 noundef 2000000) #9
  %2 = tail call dereferenceable_or_null(4000) ptr @malloc(i64 noundef 4000) #9
  %3 = tail call dereferenceable_or_null(4000) ptr @malloc(i64 noundef 4000) #9
  %4 = tail call dereferenceable_or_null(2000000) ptr @malloc(i64 noundef 2000000) #9
  tail call void @init_array(i32 noundef 500, i32 noundef 500, ptr noundef %1)
  %5 = tail call i32 @clock() #8
  tail call void @correlation(i32 noundef 500, i32 noundef 500, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4)
  %6 = tail call i32 @clock() #8
  %7 = sub nsw i32 %6, %5
  %8 = sitofp i32 %7 to double
  %9 = fdiv double %8, 1.000000e+03
  %10 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %9) #8
  %11 = load double, ptr %4, align 8
  %12 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %11) #8
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  tail call void @free(ptr noundef %4)
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
!1 = !DIFile(filename: "benchmarks/correlation.c", directory: "C:/Users/ultim/compiler-opt")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 21.1.8"}
!8 = distinct !{!8, !9, !10, !11}
!9 = !{!"llvm.loop.mustprogress"}
!10 = !{!"llvm.loop.isvectorized", i32 1}
!11 = !{!"llvm.loop.unroll.runtime.disable"}
!12 = distinct !{!12, !9, !11, !10}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !16}
!16 = !{!"llvm.loop.unroll.disable"}
!17 = distinct !{!17, !9}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
!20 = distinct !{!20, !9}
!21 = distinct !{!21, !9}
!22 = distinct !{!22, !9}
!23 = distinct !{!23, !9}
!24 = distinct !{!24, !9}
