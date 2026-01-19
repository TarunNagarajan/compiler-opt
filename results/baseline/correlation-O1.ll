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
  %7 = zext i32 %1 to i64
  %xtraiter = and i64 %7, 3
  %8 = icmp ult i32 %1, 4
  %unroll_iter = and i64 %7, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv17 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next18, %._crit_edge ]
  br i1 %6, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader
  %9 = trunc nuw nsw i64 %indvars.iv17 to i32
  %10 = uitofp nneg i32 %9 to double
  %11 = mul nuw nsw i64 %indvars.iv17, %4
  %12 = getelementptr inbounds nuw double, ptr %2, i64 %11
  br i1 %8, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %13 = trunc nuw nsw i64 %indvars.iv to i32
  %14 = uitofp nneg i32 %13 to double
  %15 = fmul double %10, %14
  %16 = fdiv double %15, 1.000000e+03
  %17 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv
  store double %16, ptr %17, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %18 = trunc nuw nsw i64 %indvars.iv.next to i32
  %19 = uitofp nneg i32 %18 to double
  %20 = fmul double %10, %19
  %21 = fdiv double %20, 1.000000e+03
  %22 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next
  store double %21, ptr %22, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %23 = trunc nuw nsw i64 %indvars.iv.next.1 to i32
  %24 = uitofp nneg i32 %23 to double
  %25 = fmul double %10, %24
  %26 = fdiv double %25, 1.000000e+03
  %27 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next.1
  store double %26, ptr %27, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %28 = trunc nuw nsw i64 %indvars.iv.next.2 to i32
  %29 = uitofp nneg i32 %28 to double
  %30 = fmul double %10, %29
  %31 = fdiv double %30, 1.000000e+03
  %32 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next.2
  store double %31, ptr %32, align 8
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
  %33 = trunc nuw nsw i64 %indvars.iv.epil to i32
  %34 = uitofp nneg i32 %33 to double
  %35 = fmul double %10, %34
  %36 = fdiv double %35, 1.000000e+03
  %37 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.epil
  store double %36, ptr %37, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %._crit_edge, label %.epil.preheader, !llvm.loop !10

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader, %.preheader
  %indvars.iv.next18 = add nuw nsw i64 %indvars.iv17, 1
  %exitcond21.not = icmp eq i64 %indvars.iv.next18, %wide.trip.count20
  br i1 %exitcond21.not, label %._crit_edge15, label %.preheader, !llvm.loop !12

._crit_edge15:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable
define dso_local void @correlation(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4, ptr noundef captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %1 to i64
  %8 = zext i32 %0 to i64
  %9 = icmp sgt i32 %0, 0
  br i1 %9, label %.lr.ph121, label %.preheader117

.lr.ph121:                                        ; preds = %6
  %10 = icmp sgt i32 %1, 0
  %11 = sitofp i32 %1 to double
  %wide.trip.count151 = zext nneg i32 %0 to i64
  %12 = zext i32 %1 to i64
  %xtraiter = and i64 %12, 3
  %13 = icmp ult i32 %1, 4
  %unroll_iter = and i64 %12, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %18

.preheader117:                                    ; preds = %._crit_edge, %6
  %14 = icmp sgt i32 %0, 0
  br i1 %14, label %.lr.ph129, label %.preheader116

.lr.ph129:                                        ; preds = %.preheader117
  %15 = icmp sgt i32 %1, 0
  %16 = sitofp i32 %1 to double
  %wide.trip.count161 = zext nneg i32 %0 to i64
  %xtraiter191 = and i64 %7, 1
  %17 = icmp eq i32 %1, 1
  %unroll_iter194 = and i64 %7, 2147483646
  %lcmp.mod193.not = icmp eq i64 %xtraiter191, 0
  br label %44

18:                                               ; preds = %.lr.ph121, %._crit_edge
  %indvars.iv148 = phi i64 [ 0, %.lr.ph121 ], [ %indvars.iv.next149, %._crit_edge ]
  %19 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv148
  store double 0.000000e+00, ptr %19, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv148
  br i1 %10, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %18
  %.promoted = load double, ptr %19, align 8
  br i1 %13, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %20 = phi double [ %32, %.lr.ph.new ], [ %.promoted, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %21 = mul nuw nsw i64 %indvars.iv, %7
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %21
  %22 = load double, ptr %gep, align 8
  %23 = fadd double %22, %20
  store double %23, ptr %19, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %24 = mul nuw nsw i64 %indvars.iv.next, %7
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %24
  %25 = load double, ptr %gep.1, align 8
  %26 = fadd double %25, %23
  store double %26, ptr %19, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %27 = mul nuw nsw i64 %indvars.iv.next.1, %7
  %gep.2 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %27
  %28 = load double, ptr %gep.2, align 8
  %29 = fadd double %28, %26
  store double %29, ptr %19, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %30 = mul nuw nsw i64 %indvars.iv.next.2, %7
  %gep.3 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %30
  %31 = load double, ptr %gep.3, align 8
  %32 = fadd double %31, %29
  store double %32, ptr %19, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !13

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %.lr.ph.new ]
  %.unr = phi double [ %.promoted, %.lr.ph ], [ %32, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %.epil.preheader

.epil.preheader:                                  ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %._crit_edge.loopexit.unr-lcssa ]
  %33 = phi double [ %36, %.epil.preheader ], [ %.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %34 = mul nuw nsw i64 %indvars.iv.epil, %7
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %34
  %35 = load double, ptr %gep.epil, align 8
  %36 = fadd double %35, %33
  store double %36, ptr %19, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %._crit_edge, label %.epil.preheader, !llvm.loop !14

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader, %18
  %37 = load double, ptr %19, align 8
  %38 = fdiv double %37, %11
  store double %38, ptr %19, align 8
  %indvars.iv.next149 = add nuw nsw i64 %indvars.iv148, 1
  %exitcond152.not = icmp eq i64 %indvars.iv.next149, %wide.trip.count151
  br i1 %exitcond152.not, label %.preheader117, label %18, !llvm.loop !15

.preheader116:                                    ; preds = %._crit_edge127, %.preheader117
  %39 = icmp sgt i32 %1, 0
  br i1 %39, label %.preheader115.lr.ph, label %.preheader

.preheader115.lr.ph:                              ; preds = %.preheader116
  %40 = icmp sgt i32 %0, 0
  %41 = sitofp i32 %1 to double
  %wide.trip.count171 = zext nneg i32 %1 to i64
  %42 = zext i32 %0 to i64
  %xtraiter197 = and i64 %42, 1
  %43 = icmp eq i32 %0, 1
  %unroll_iter200 = and i64 %42, 2147483646
  %lcmp.mod199.not = icmp eq i64 %xtraiter197, 0
  br label %.preheader115

44:                                               ; preds = %.lr.ph129, %._crit_edge127
  %indvars.iv158 = phi i64 [ 0, %.lr.ph129 ], [ %indvars.iv.next159, %._crit_edge127 ]
  %45 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv158
  store double 0.000000e+00, ptr %45, align 8
  %invariant.gep122 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv158
  br i1 %15, label %.lr.ph126, label %._crit_edge127

.lr.ph126:                                        ; preds = %44
  %46 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv158
  br i1 %17, label %._crit_edge127.loopexit.unr-lcssa, label %.lr.ph126.new

.lr.ph126.new:                                    ; preds = %.lr.ph126, %.lr.ph126.new
  %indvars.iv153 = phi i64 [ %indvars.iv.next154.1, %.lr.ph126.new ], [ 0, %.lr.ph126 ]
  %niter195 = phi i64 [ %niter195.next.1, %.lr.ph126.new ], [ 0, %.lr.ph126 ]
  %47 = mul nuw nsw i64 %indvars.iv153, %7
  %gep123 = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %47
  %48 = load double, ptr %gep123, align 8
  %49 = load double, ptr %46, align 8
  %50 = fsub double %48, %49
  %51 = load double, ptr %45, align 8
  %52 = tail call double @llvm.fmuladd.f64(double %50, double %50, double %51)
  store double %52, ptr %45, align 8
  %indvars.iv.next154 = or disjoint i64 %indvars.iv153, 1
  %53 = mul nuw nsw i64 %indvars.iv.next154, %7
  %gep123.1 = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %53
  %54 = load double, ptr %gep123.1, align 8
  %55 = load double, ptr %46, align 8
  %56 = fsub double %54, %55
  %57 = load double, ptr %45, align 8
  %58 = tail call double @llvm.fmuladd.f64(double %56, double %56, double %57)
  store double %58, ptr %45, align 8
  %indvars.iv.next154.1 = add nuw nsw i64 %indvars.iv153, 2
  %niter195.next.1 = add i64 %niter195, 2
  %niter195.ncmp.1 = icmp eq i64 %niter195.next.1, %unroll_iter194
  br i1 %niter195.ncmp.1, label %._crit_edge127.loopexit.unr-lcssa, label %.lr.ph126.new, !llvm.loop !16

._crit_edge127.loopexit.unr-lcssa:                ; preds = %.lr.ph126.new, %.lr.ph126
  %indvars.iv153.unr = phi i64 [ 0, %.lr.ph126 ], [ %indvars.iv.next154.1, %.lr.ph126.new ]
  br i1 %lcmp.mod193.not, label %._crit_edge127, label %._crit_edge127.loopexit.epilog-lcssa

._crit_edge127.loopexit.epilog-lcssa:             ; preds = %._crit_edge127.loopexit.unr-lcssa
  %59 = mul nuw nsw i64 %indvars.iv153.unr, %7
  %gep123.epil = getelementptr inbounds nuw double, ptr %invariant.gep122, i64 %59
  %60 = load double, ptr %gep123.epil, align 8
  %61 = load double, ptr %46, align 8
  %62 = fsub double %60, %61
  %63 = load double, ptr %45, align 8
  %64 = tail call double @llvm.fmuladd.f64(double %62, double %62, double %63)
  store double %64, ptr %45, align 8
  br label %._crit_edge127

._crit_edge127:                                   ; preds = %._crit_edge127.loopexit.epilog-lcssa, %._crit_edge127.loopexit.unr-lcssa, %44
  %65 = load double, ptr %45, align 8
  %66 = fdiv double %65, %16
  %67 = tail call double @sqrt(double noundef %66) #8
  %68 = fcmp ugt double %67, 1.000000e-01
  %storemerge = select i1 %68, double %67, double 1.000000e+00
  store double %storemerge, ptr %45, align 8
  %indvars.iv.next159 = add nuw nsw i64 %indvars.iv158, 1
  %exitcond162.not = icmp eq i64 %indvars.iv.next159, %wide.trip.count161
  br i1 %exitcond162.not, label %.preheader116, label %44, !llvm.loop !17

.preheader115:                                    ; preds = %.preheader115.lr.ph, %._crit_edge132
  %indvars.iv168 = phi i64 [ 0, %.preheader115.lr.ph ], [ %indvars.iv.next169, %._crit_edge132 ]
  br i1 %40, label %.lr.ph131, label %._crit_edge132

.lr.ph131:                                        ; preds = %.preheader115
  %69 = mul nuw nsw i64 %indvars.iv168, %7
  %70 = getelementptr inbounds nuw double, ptr %2, i64 %69
  br i1 %43, label %._crit_edge132.loopexit.unr-lcssa, label %.lr.ph131.new

.preheader:                                       ; preds = %._crit_edge132, %.preheader116
  %71 = add i32 %0, -1
  %72 = icmp sgt i32 %0, 1
  br i1 %72, label %.lr.ph145, label %._crit_edge146

.lr.ph145:                                        ; preds = %.preheader
  %73 = icmp sgt i32 %1, 0
  %wide.trip.count188 = zext i32 %71 to i64
  %wide.trip.count183 = zext nneg i32 %0 to i64
  %xtraiter203 = and i64 %7, 1
  %74 = icmp eq i32 %1, 1
  %unroll_iter207 = and i64 %7, 2147483646
  %lcmp.mod206.not = icmp eq i64 %xtraiter203, 0
  br label %.lr.ph143.preheader

.lr.ph131.new:                                    ; preds = %.lr.ph131, %.lr.ph131.new
  %indvars.iv163 = phi i64 [ %indvars.iv.next164.1, %.lr.ph131.new ], [ 0, %.lr.ph131 ]
  %niter201 = phi i64 [ %niter201.next.1, %.lr.ph131.new ], [ 0, %.lr.ph131 ]
  %75 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv163
  %76 = load double, ptr %75, align 8
  %77 = getelementptr inbounds nuw double, ptr %70, i64 %indvars.iv163
  %78 = load double, ptr %77, align 8
  %79 = fsub double %78, %76
  store double %79, ptr %77, align 8
  %80 = tail call double @sqrt(double noundef %41) #8
  %81 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv163
  %82 = load double, ptr %81, align 8
  %83 = fmul double %80, %82
  %84 = load double, ptr %77, align 8
  %85 = fdiv double %84, %83
  store double %85, ptr %77, align 8
  %indvars.iv.next164 = or disjoint i64 %indvars.iv163, 1
  %86 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next164
  %87 = load double, ptr %86, align 8
  %88 = getelementptr inbounds nuw double, ptr %70, i64 %indvars.iv.next164
  %89 = load double, ptr %88, align 8
  %90 = fsub double %89, %87
  store double %90, ptr %88, align 8
  %91 = tail call double @sqrt(double noundef %41) #8
  %92 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next164
  %93 = load double, ptr %92, align 8
  %94 = fmul double %91, %93
  %95 = load double, ptr %88, align 8
  %96 = fdiv double %95, %94
  store double %96, ptr %88, align 8
  %indvars.iv.next164.1 = add nuw nsw i64 %indvars.iv163, 2
  %niter201.next.1 = add i64 %niter201, 2
  %niter201.ncmp.1 = icmp eq i64 %niter201.next.1, %unroll_iter200
  br i1 %niter201.ncmp.1, label %._crit_edge132.loopexit.unr-lcssa, label %.lr.ph131.new, !llvm.loop !18

._crit_edge132.loopexit.unr-lcssa:                ; preds = %.lr.ph131.new, %.lr.ph131
  %indvars.iv163.unr = phi i64 [ 0, %.lr.ph131 ], [ %indvars.iv.next164.1, %.lr.ph131.new ]
  br i1 %lcmp.mod199.not, label %._crit_edge132, label %._crit_edge132.loopexit.epilog-lcssa

._crit_edge132.loopexit.epilog-lcssa:             ; preds = %._crit_edge132.loopexit.unr-lcssa
  %97 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv163.unr
  %98 = load double, ptr %97, align 8
  %99 = getelementptr inbounds nuw double, ptr %70, i64 %indvars.iv163.unr
  %100 = load double, ptr %99, align 8
  %101 = fsub double %100, %98
  store double %101, ptr %99, align 8
  %102 = tail call double @sqrt(double noundef %41) #8
  %103 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv163.unr
  %104 = load double, ptr %103, align 8
  %105 = fmul double %102, %104
  %106 = load double, ptr %99, align 8
  %107 = fdiv double %106, %105
  store double %107, ptr %99, align 8
  br label %._crit_edge132

._crit_edge132:                                   ; preds = %._crit_edge132.loopexit.epilog-lcssa, %._crit_edge132.loopexit.unr-lcssa, %.preheader115
  %indvars.iv.next169 = add nuw nsw i64 %indvars.iv168, 1
  %exitcond172.not = icmp eq i64 %indvars.iv.next169, %wide.trip.count171
  br i1 %exitcond172.not, label %.preheader, label %.preheader115, !llvm.loop !19

.loopexit:                                        ; preds = %._crit_edge137
  %indvars.iv.next179 = add nuw nsw i64 %indvars.iv178, 1
  %exitcond189.not = icmp eq i64 %indvars.iv.next186, %wide.trip.count188
  br i1 %exitcond189.not, label %._crit_edge146, label %.lr.ph143.preheader, !llvm.loop !20

.lr.ph143.preheader:                              ; preds = %.lr.ph145, %.loopexit
  %indvars.iv185 = phi i64 [ 0, %.lr.ph145 ], [ %indvars.iv.next186, %.loopexit ]
  %indvars.iv178 = phi i64 [ 1, %.lr.ph145 ], [ %indvars.iv.next179, %.loopexit ]
  %108 = mul nuw nsw i64 %indvars.iv185, %8
  %109 = getelementptr inbounds nuw double, ptr %5, i64 %108
  %110 = getelementptr inbounds nuw double, ptr %109, i64 %indvars.iv185
  store double 1.000000e+00, ptr %110, align 8
  %indvars.iv.next186 = add nuw nsw i64 %indvars.iv185, 1
  %invariant.gep139 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv185
  br label %.lr.ph143

.lr.ph143:                                        ; preds = %.lr.ph143.preheader, %._crit_edge137
  %indvars.iv180 = phi i64 [ %indvars.iv178, %.lr.ph143.preheader ], [ %indvars.iv.next181, %._crit_edge137 ]
  %111 = getelementptr inbounds nuw double, ptr %109, i64 %indvars.iv180
  store double 0.000000e+00, ptr %111, align 8
  br i1 %73, label %.lr.ph136, label %._crit_edge137

.lr.ph136:                                        ; preds = %.lr.ph143
  %.promoted138 = load double, ptr %111, align 8
  br i1 %74, label %._crit_edge137.loopexit.unr-lcssa, label %.lr.ph136.new

.lr.ph136.new:                                    ; preds = %.lr.ph136, %.lr.ph136.new
  %indvars.iv173 = phi i64 [ %indvars.iv.next174.1, %.lr.ph136.new ], [ 0, %.lr.ph136 ]
  %112 = phi double [ %126, %.lr.ph136.new ], [ %.promoted138, %.lr.ph136 ]
  %niter208 = phi i64 [ %niter208.next.1, %.lr.ph136.new ], [ 0, %.lr.ph136 ]
  %113 = mul nuw nsw i64 %indvars.iv173, %7
  %114 = getelementptr inbounds nuw double, ptr %2, i64 %113
  %115 = getelementptr inbounds nuw double, ptr %114, i64 %indvars.iv185
  %116 = load double, ptr %115, align 8
  %117 = getelementptr inbounds nuw double, ptr %114, i64 %indvars.iv180
  %118 = load double, ptr %117, align 8
  %119 = tail call double @llvm.fmuladd.f64(double %116, double %118, double %112)
  store double %119, ptr %111, align 8
  %indvars.iv.next174 = or disjoint i64 %indvars.iv173, 1
  %120 = mul nuw nsw i64 %indvars.iv.next174, %7
  %121 = getelementptr inbounds nuw double, ptr %2, i64 %120
  %122 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv185
  %123 = load double, ptr %122, align 8
  %124 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv180
  %125 = load double, ptr %124, align 8
  %126 = tail call double @llvm.fmuladd.f64(double %123, double %125, double %119)
  store double %126, ptr %111, align 8
  %indvars.iv.next174.1 = add nuw nsw i64 %indvars.iv173, 2
  %niter208.next.1 = add i64 %niter208, 2
  %niter208.ncmp.1 = icmp eq i64 %niter208.next.1, %unroll_iter207
  br i1 %niter208.ncmp.1, label %._crit_edge137.loopexit.unr-lcssa, label %.lr.ph136.new, !llvm.loop !21

._crit_edge137.loopexit.unr-lcssa:                ; preds = %.lr.ph136.new, %.lr.ph136
  %indvars.iv173.unr = phi i64 [ 0, %.lr.ph136 ], [ %indvars.iv.next174.1, %.lr.ph136.new ]
  %.unr205 = phi double [ %.promoted138, %.lr.ph136 ], [ %126, %.lr.ph136.new ]
  br i1 %lcmp.mod206.not, label %._crit_edge137, label %._crit_edge137.loopexit.epilog-lcssa

._crit_edge137.loopexit.epilog-lcssa:             ; preds = %._crit_edge137.loopexit.unr-lcssa
  %127 = mul nuw nsw i64 %indvars.iv173.unr, %7
  %128 = getelementptr inbounds nuw double, ptr %2, i64 %127
  %129 = getelementptr inbounds nuw double, ptr %128, i64 %indvars.iv185
  %130 = load double, ptr %129, align 8
  %131 = getelementptr inbounds nuw double, ptr %128, i64 %indvars.iv180
  %132 = load double, ptr %131, align 8
  %133 = tail call double @llvm.fmuladd.f64(double %130, double %132, double %.unr205)
  store double %133, ptr %111, align 8
  br label %._crit_edge137

._crit_edge137:                                   ; preds = %._crit_edge137.loopexit.epilog-lcssa, %._crit_edge137.loopexit.unr-lcssa, %.lr.ph143
  %134 = load double, ptr %111, align 8
  %135 = mul nuw nsw i64 %indvars.iv180, %8
  %gep140 = getelementptr inbounds nuw double, ptr %invariant.gep139, i64 %135
  store double %134, ptr %gep140, align 8
  %indvars.iv.next181 = add nuw nsw i64 %indvars.iv180, 1
  %exitcond184.not = icmp eq i64 %indvars.iv.next181, %wide.trip.count183
  br i1 %exitcond184.not, label %.loopexit, label %.lr.ph143, !llvm.loop !22

._crit_edge146:                                   ; preds = %.loopexit, %.preheader
  %136 = sext i32 %71 to i64
  %137 = mul nsw i64 %136, %8
  %138 = getelementptr inbounds double, ptr %5, i64 %137
  %139 = getelementptr inbounds double, ptr %138, i64 %136
  store double 1.000000e+00, ptr %139, align 8
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
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !11}
!11 = !{!"llvm.loop.unroll.disable"}
!12 = distinct !{!12, !9}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !11}
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !9}
!17 = distinct !{!17, !9}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
!20 = distinct !{!20, !9}
!21 = distinct !{!21, !9}
!22 = distinct !{!22, !9}
