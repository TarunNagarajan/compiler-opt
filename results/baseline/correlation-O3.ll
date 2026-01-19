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
  %6 = icmp sgt i32 %1, 0
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %.preheader.us.preheader, label %._crit_edge15

.preheader.us.preheader:                          ; preds = %3
  %wide.trip.count21 = zext nneg i32 %0 to i64
  %min.iters.check = icmp ult i32 %1, 2
  %n.vec = and i64 %4, 2147483646
  %cmp.n = icmp eq i64 %n.vec, %4
  br label %.preheader.us

.preheader.us:                                    ; preds = %.preheader.us.preheader, %._crit_edge.us
  %indvars.iv18 = phi i64 [ 0, %.preheader.us.preheader ], [ %indvars.iv.next19, %._crit_edge.us ]
  %7 = trunc nuw nsw i64 %indvars.iv18 to i32
  %8 = uitofp nneg i32 %7 to double
  %9 = mul nuw nsw i64 %indvars.iv18, %4
  %10 = getelementptr inbounds nuw double, ptr %2, i64 %9
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.preheader.us
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
  br i1 %cmp.n, label %._crit_edge.us, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.preheader.us, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.preheader.us ], [ %n.vec, %middle.block ]
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
  br i1 %exitcond.not, label %._crit_edge.us, label %scalar.ph, !llvm.loop !12

._crit_edge.us:                                   ; preds = %scalar.ph, %middle.block
  %indvars.iv.next19 = add nuw nsw i64 %indvars.iv18, 1
  %exitcond22.not = icmp eq i64 %indvars.iv.next19, %wide.trip.count21
  br i1 %exitcond22.not, label %._crit_edge15, label %.preheader.us, !llvm.loop !13

._crit_edge15:                                    ; preds = %._crit_edge.us, %3
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
  br i1 %10, label %.lr.ph.us.preheader, label %.lr.ph121.split.preheader

.lr.ph.us.preheader:                              ; preds = %.lr.ph121
  %xtraiter225 = and i64 %7, 3
  %12 = icmp ult i32 %1, 4
  %unroll_iter228 = and i64 %7, 2147483644
  %lcmp.mod226.not = icmp eq i64 %xtraiter225, 0
  br label %.lr.ph.us

.lr.ph121.split.preheader:                        ; preds = %.lr.ph121
  %13 = fdiv double 0.000000e+00, %11
  %min.iters.check = icmp ult i32 %0, 4
  br i1 %min.iters.check, label %.lr.ph121.split.preheader224, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph121.split.preheader
  %n.vec = and i64 %8, 2147483644
  %broadcast.splatinsert = insertelement <2 x double> poison, double %13, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %14 = getelementptr inbounds nuw double, ptr %3, i64 %index
  %15 = getelementptr inbounds nuw i8, ptr %14, i64 16
  store <2 x double> %broadcast.splat, ptr %14, align 8
  store <2 x double> %broadcast.splat, ptr %15, align 8
  %index.next = add nuw i64 %index, 4
  %16 = icmp eq i64 %index.next, %n.vec
  br i1 %16, label %middle.block, label %vector.body, !llvm.loop !14

middle.block:                                     ; preds = %vector.body
  %cmp.n = icmp eq i64 %n.vec, %8
  br i1 %cmp.n, label %.lr.ph124.thread, label %.lr.ph121.split.preheader224

.lr.ph121.split.preheader224:                     ; preds = %.lr.ph121.split.preheader, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph121.split.preheader ], [ %n.vec, %middle.block ]
  br label %.lr.ph121.split

.lr.ph.us:                                        ; preds = %.lr.ph.us.preheader, %._crit_edge.us
  %indvars.iv153 = phi i64 [ %indvars.iv.next154, %._crit_edge.us ], [ 0, %.lr.ph.us.preheader ]
  %17 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv153
  store double 0.000000e+00, ptr %17, align 8
  %invariant.gep.us = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv153
  br i1 %12, label %._crit_edge.us.unr-lcssa, label %.lr.ph.us.new

.lr.ph.us.new:                                    ; preds = %.lr.ph.us, %.lr.ph.us.new
  %indvars.iv148 = phi i64 [ %indvars.iv.next149.3, %.lr.ph.us.new ], [ 0, %.lr.ph.us ]
  %18 = phi double [ %30, %.lr.ph.us.new ], [ 0.000000e+00, %.lr.ph.us ]
  %niter229 = phi i64 [ %niter229.next.3, %.lr.ph.us.new ], [ 0, %.lr.ph.us ]
  %19 = mul nuw nsw i64 %indvars.iv148, %7
  %gep.us = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %19
  %20 = load double, ptr %gep.us, align 8
  %21 = fadd double %20, %18
  store double %21, ptr %17, align 8
  %indvars.iv.next149 = or disjoint i64 %indvars.iv148, 1
  %22 = mul nuw nsw i64 %indvars.iv.next149, %7
  %gep.us.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %22
  %23 = load double, ptr %gep.us.1, align 8
  %24 = fadd double %23, %21
  store double %24, ptr %17, align 8
  %indvars.iv.next149.1 = or disjoint i64 %indvars.iv148, 2
  %25 = mul nuw nsw i64 %indvars.iv.next149.1, %7
  %gep.us.2 = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %25
  %26 = load double, ptr %gep.us.2, align 8
  %27 = fadd double %26, %24
  store double %27, ptr %17, align 8
  %indvars.iv.next149.2 = or disjoint i64 %indvars.iv148, 3
  %28 = mul nuw nsw i64 %indvars.iv.next149.2, %7
  %gep.us.3 = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %28
  %29 = load double, ptr %gep.us.3, align 8
  %30 = fadd double %29, %27
  store double %30, ptr %17, align 8
  %indvars.iv.next149.3 = add nuw nsw i64 %indvars.iv148, 4
  %niter229.next.3 = add i64 %niter229, 4
  %niter229.ncmp.3 = icmp eq i64 %niter229.next.3, %unroll_iter228
  br i1 %niter229.ncmp.3, label %._crit_edge.us.unr-lcssa, label %.lr.ph.us.new, !llvm.loop !15

._crit_edge.us.unr-lcssa:                         ; preds = %.lr.ph.us.new, %.lr.ph.us
  %.lcssa222.ph = phi double [ poison, %.lr.ph.us ], [ %30, %.lr.ph.us.new ]
  %indvars.iv148.unr = phi i64 [ 0, %.lr.ph.us ], [ %indvars.iv.next149.3, %.lr.ph.us.new ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph.us ], [ %30, %.lr.ph.us.new ]
  br i1 %lcmp.mod226.not, label %._crit_edge.us, label %.epil.preheader

.epil.preheader:                                  ; preds = %._crit_edge.us.unr-lcssa, %.epil.preheader
  %indvars.iv148.epil = phi i64 [ %indvars.iv.next149.epil, %.epil.preheader ], [ %indvars.iv148.unr, %._crit_edge.us.unr-lcssa ]
  %31 = phi double [ %34, %.epil.preheader ], [ %.unr, %._crit_edge.us.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %._crit_edge.us.unr-lcssa ]
  %32 = mul nuw nsw i64 %indvars.iv148.epil, %7
  %gep.us.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %32
  %33 = load double, ptr %gep.us.epil, align 8
  %34 = fadd double %33, %31
  store double %34, ptr %17, align 8
  %indvars.iv.next149.epil = add nuw nsw i64 %indvars.iv148.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter225
  br i1 %epil.iter.cmp.not, label %._crit_edge.us, label %.epil.preheader, !llvm.loop !16

._crit_edge.us:                                   ; preds = %.epil.preheader, %._crit_edge.us.unr-lcssa
  %.lcssa222 = phi double [ %.lcssa222.ph, %._crit_edge.us.unr-lcssa ], [ %34, %.epil.preheader ]
  %35 = fdiv double %.lcssa222, %11
  store double %35, ptr %17, align 8
  %indvars.iv.next154 = add nuw nsw i64 %indvars.iv153, 1
  %exitcond157.not = icmp eq i64 %indvars.iv.next154, %8
  br i1 %exitcond157.not, label %.lr.ph124, label %.lr.ph.us, !llvm.loop !18

.lr.ph124:                                        ; preds = %._crit_edge.us
  %36 = sitofp i32 %1 to double
  %xtraiter231 = and i64 %7, 1
  %37 = icmp eq i32 %1, 1
  %unroll_iter236 = and i64 %7, 2147483646
  %lcmp.mod234.not = icmp eq i64 %xtraiter231, 0
  br label %.lr.ph.us127

.lr.ph.us127:                                     ; preds = %.lr.ph124, %._crit_edge.us128
  %indvars.iv168 = phi i64 [ %indvars.iv.next169, %._crit_edge.us128 ], [ 0, %.lr.ph124 ]
  %38 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv168
  store double 0.000000e+00, ptr %38, align 8
  %invariant.gep.us125 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv168
  %39 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv168
  br i1 %37, label %._crit_edge.us128.unr-lcssa, label %.lr.ph.us127.new

.lr.ph.us127.new:                                 ; preds = %.lr.ph.us127, %.lr.ph.us127.new
  %40 = phi double [ %50, %.lr.ph.us127.new ], [ 0.000000e+00, %.lr.ph.us127 ]
  %indvars.iv163 = phi i64 [ %indvars.iv.next164.1, %.lr.ph.us127.new ], [ 0, %.lr.ph.us127 ]
  %niter237 = phi i64 [ %niter237.next.1, %.lr.ph.us127.new ], [ 0, %.lr.ph.us127 ]
  %41 = mul nuw nsw i64 %indvars.iv163, %7
  %gep.us126 = getelementptr inbounds nuw double, ptr %invariant.gep.us125, i64 %41
  %42 = load double, ptr %gep.us126, align 8
  %43 = load double, ptr %39, align 8
  %44 = fsub double %42, %43
  %45 = tail call double @llvm.fmuladd.f64(double %44, double %44, double %40)
  store double %45, ptr %38, align 8
  %indvars.iv.next164 = or disjoint i64 %indvars.iv163, 1
  %46 = mul nuw nsw i64 %indvars.iv.next164, %7
  %gep.us126.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us125, i64 %46
  %47 = load double, ptr %gep.us126.1, align 8
  %48 = load double, ptr %39, align 8
  %49 = fsub double %47, %48
  %50 = tail call double @llvm.fmuladd.f64(double %49, double %49, double %45)
  store double %50, ptr %38, align 8
  %indvars.iv.next164.1 = add nuw nsw i64 %indvars.iv163, 2
  %niter237.next.1 = add i64 %niter237, 2
  %niter237.ncmp.1 = icmp eq i64 %niter237.next.1, %unroll_iter236
  br i1 %niter237.ncmp.1, label %._crit_edge.us128.unr-lcssa, label %.lr.ph.us127.new, !llvm.loop !19

._crit_edge.us128.unr-lcssa:                      ; preds = %.lr.ph.us127.new, %.lr.ph.us127
  %.lcssa221.ph = phi double [ poison, %.lr.ph.us127 ], [ %50, %.lr.ph.us127.new ]
  %.unr233 = phi double [ 0.000000e+00, %.lr.ph.us127 ], [ %50, %.lr.ph.us127.new ]
  %indvars.iv163.unr = phi i64 [ 0, %.lr.ph.us127 ], [ %indvars.iv.next164.1, %.lr.ph.us127.new ]
  br i1 %lcmp.mod234.not, label %._crit_edge.us128, label %._crit_edge.us128.epilog-lcssa

._crit_edge.us128.epilog-lcssa:                   ; preds = %._crit_edge.us128.unr-lcssa
  %51 = mul nuw nsw i64 %indvars.iv163.unr, %7
  %gep.us126.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us125, i64 %51
  %52 = load double, ptr %gep.us126.epil, align 8
  %53 = load double, ptr %39, align 8
  %54 = fsub double %52, %53
  %55 = tail call double @llvm.fmuladd.f64(double %54, double %54, double %.unr233)
  store double %55, ptr %38, align 8
  br label %._crit_edge.us128

._crit_edge.us128:                                ; preds = %._crit_edge.us128.unr-lcssa, %._crit_edge.us128.epilog-lcssa
  %.lcssa221 = phi double [ %.lcssa221.ph, %._crit_edge.us128.unr-lcssa ], [ %55, %._crit_edge.us128.epilog-lcssa ]
  %56 = fdiv double %.lcssa221, %36
  %57 = tail call double @sqrt(double noundef %56) #8
  %58 = fcmp ugt double %57, 1.000000e-01
  %storemerge.us = select i1 %58, double %57, double 1.000000e+00
  store double %storemerge.us, ptr %38, align 8
  %indvars.iv.next169 = add nuw nsw i64 %indvars.iv168, 1
  %exitcond172.not = icmp eq i64 %indvars.iv.next169, %8
  br i1 %exitcond172.not, label %.preheader116, label %.lr.ph.us127, !llvm.loop !20

.lr.ph121.split:                                  ; preds = %.lr.ph121.split.preheader224, %.lr.ph121.split
  %indvars.iv = phi i64 [ %indvars.iv.next, %.lr.ph121.split ], [ %indvars.iv.ph, %.lr.ph121.split.preheader224 ]
  %59 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %13, ptr %59, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %8
  br i1 %exitcond.not, label %.lr.ph124.thread, label %.lr.ph121.split, !llvm.loop !21

.lr.ph124.thread:                                 ; preds = %.lr.ph121.split, %middle.block
  %60 = sitofp i32 %1 to double
  %61 = fdiv double 0.000000e+00, %60
  %xtraiter = and i64 %8, 1
  %62 = icmp eq i32 %0, 1
  br i1 %62, label %.preheader.loopexit223.unr-lcssa, label %.lr.ph124.thread.new

.lr.ph124.thread.new:                             ; preds = %.lr.ph124.thread
  %unroll_iter = and i64 %8, 2147483646
  %invariant.gep258 = getelementptr inbounds i8, ptr %4, i64 8
  br label %.lr.ph124.split

.preheader116:                                    ; preds = %._crit_edge.us128, %6
  %63 = icmp sgt i32 %1, 0
  br i1 %63, label %.preheader115.lr.ph, label %.preheader

.preheader115.lr.ph:                              ; preds = %.preheader116
  %64 = uitofp nneg i32 %1 to double
  br i1 %9, label %.preheader115.us.preheader, label %.preheader.thread

.preheader115.us.preheader:                       ; preds = %.preheader115.lr.ph
  %xtraiter239 = and i64 %8, 1
  %65 = icmp eq i32 %0, 1
  %unroll_iter242 = and i64 %8, 2147483646
  %lcmp.mod241.not = icmp eq i64 %xtraiter239, 0
  br label %.preheader115.us

.preheader.thread:                                ; preds = %.preheader115.lr.ph
  %66 = add i32 %0, -1
  br label %._crit_edge

.preheader115.us:                                 ; preds = %.preheader115.us.preheader, %._crit_edge.us132
  %indvars.iv178 = phi i64 [ %indvars.iv.next179, %._crit_edge.us132 ], [ 0, %.preheader115.us.preheader ]
  %67 = mul nuw nsw i64 %indvars.iv178, %7
  %68 = getelementptr inbounds nuw double, ptr %2, i64 %67
  br i1 %65, label %._crit_edge.us132.unr-lcssa, label %.preheader115.us.new

.preheader115.us.new:                             ; preds = %.preheader115.us, %.preheader115.us.new
  %indvars.iv173 = phi i64 [ %indvars.iv.next174.1, %.preheader115.us.new ], [ 0, %.preheader115.us ]
  %niter243 = phi i64 [ %niter243.next.1, %.preheader115.us.new ], [ 0, %.preheader115.us ]
  %69 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv173
  %70 = load double, ptr %69, align 8
  %71 = getelementptr inbounds nuw double, ptr %68, i64 %indvars.iv173
  %72 = load double, ptr %71, align 8
  %73 = fsub double %72, %70
  store double %73, ptr %71, align 8
  %74 = tail call double @sqrt(double noundef %64) #8
  %75 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv173
  %76 = load double, ptr %75, align 8
  %77 = fmul double %74, %76
  %78 = load double, ptr %71, align 8
  %79 = fdiv double %78, %77
  store double %79, ptr %71, align 8
  %indvars.iv.next174 = or disjoint i64 %indvars.iv173, 1
  %80 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next174
  %81 = load double, ptr %80, align 8
  %82 = getelementptr inbounds nuw double, ptr %68, i64 %indvars.iv.next174
  %83 = load double, ptr %82, align 8
  %84 = fsub double %83, %81
  store double %84, ptr %82, align 8
  %85 = tail call double @sqrt(double noundef %64) #8
  %86 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next174
  %87 = load double, ptr %86, align 8
  %88 = fmul double %85, %87
  %89 = load double, ptr %82, align 8
  %90 = fdiv double %89, %88
  store double %90, ptr %82, align 8
  %indvars.iv.next174.1 = add nuw nsw i64 %indvars.iv173, 2
  %niter243.next.1 = add i64 %niter243, 2
  %niter243.ncmp.1 = icmp eq i64 %niter243.next.1, %unroll_iter242
  br i1 %niter243.ncmp.1, label %._crit_edge.us132.unr-lcssa, label %.preheader115.us.new, !llvm.loop !22

._crit_edge.us132.unr-lcssa:                      ; preds = %.preheader115.us.new, %.preheader115.us
  %indvars.iv173.unr = phi i64 [ 0, %.preheader115.us ], [ %indvars.iv.next174.1, %.preheader115.us.new ]
  br i1 %lcmp.mod241.not, label %._crit_edge.us132, label %._crit_edge.us132.epilog-lcssa

._crit_edge.us132.epilog-lcssa:                   ; preds = %._crit_edge.us132.unr-lcssa
  %91 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv173.unr
  %92 = load double, ptr %91, align 8
  %93 = getelementptr inbounds nuw double, ptr %68, i64 %indvars.iv173.unr
  %94 = load double, ptr %93, align 8
  %95 = fsub double %94, %92
  store double %95, ptr %93, align 8
  %96 = tail call double @sqrt(double noundef %64) #8
  %97 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv173.unr
  %98 = load double, ptr %97, align 8
  %99 = fmul double %96, %98
  %100 = load double, ptr %93, align 8
  %101 = fdiv double %100, %99
  store double %101, ptr %93, align 8
  br label %._crit_edge.us132

._crit_edge.us132:                                ; preds = %._crit_edge.us132.unr-lcssa, %._crit_edge.us132.epilog-lcssa
  %indvars.iv.next179 = add nuw nsw i64 %indvars.iv178, 1
  %exitcond182.not = icmp eq i64 %indvars.iv.next179, %7
  br i1 %exitcond182.not, label %.preheader, label %.preheader115.us, !llvm.loop !23

.lr.ph124.split:                                  ; preds = %.lr.ph124.split, %.lr.ph124.thread.new
  %indvars.iv158 = phi i64 [ 0, %.lr.ph124.thread.new ], [ %indvars.iv.next159.1, %.lr.ph124.split ]
  %niter = phi i64 [ 0, %.lr.ph124.thread.new ], [ %niter.next.1, %.lr.ph124.split ]
  %102 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv158
  %103 = tail call double @sqrt(double noundef %61) #8
  %104 = fcmp ugt double %103, 1.000000e-01
  %storemerge = select i1 %104, double %103, double 1.000000e+00
  store double %storemerge, ptr %102, align 8
  %gep259 = getelementptr inbounds double, ptr %invariant.gep258, i64 %indvars.iv158
  %105 = tail call double @sqrt(double noundef %61) #8
  %106 = fcmp ugt double %105, 1.000000e-01
  %storemerge.1 = select i1 %106, double %105, double 1.000000e+00
  store double %storemerge.1, ptr %gep259, align 8
  %indvars.iv.next159.1 = add nuw nsw i64 %indvars.iv158, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %.preheader.loopexit223.unr-lcssa, label %.lr.ph124.split, !llvm.loop !20

.preheader.loopexit223.unr-lcssa:                 ; preds = %.lr.ph124.split, %.lr.ph124.thread
  %indvars.iv158.unr = phi i64 [ 0, %.lr.ph124.thread ], [ %indvars.iv.next159.1, %.lr.ph124.split ]
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %.preheader, label %.lr.ph124.split.epil

.lr.ph124.split.epil:                             ; preds = %.preheader.loopexit223.unr-lcssa
  %107 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv158.unr
  %108 = tail call double @sqrt(double noundef %61) #8
  %109 = fcmp ugt double %108, 1.000000e-01
  %storemerge.epil = select i1 %109, double %108, double 1.000000e+00
  store double %storemerge.epil, ptr %107, align 8
  br label %.preheader

.preheader:                                       ; preds = %.lr.ph124.split.epil, %.preheader.loopexit223.unr-lcssa, %._crit_edge.us132, %.preheader116
  %110 = phi i1 [ false, %.preheader116 ], [ true, %._crit_edge.us132 ], [ false, %.preheader.loopexit223.unr-lcssa ], [ false, %.lr.ph124.split.epil ]
  %111 = add i32 %0, -1
  %112 = icmp sgt i32 %0, 1
  br i1 %112, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader
  %wide.trip.count210 = zext nneg i32 %111 to i64
  br i1 %110, label %.lr.ph.us138.us.preheader.preheader, label %.lr.ph136.preheader.preheader

.lr.ph136.preheader.preheader:                    ; preds = %.lr.ph
  %113 = add nsw i64 %8, -2
  br label %.lr.ph136.preheader

.lr.ph.us138.us.preheader.preheader:              ; preds = %.lr.ph
  %xtraiter247 = and i64 %7, 1
  %114 = icmp eq i32 %1, 1
  %unroll_iter252 = and i64 %7, 4294967294
  %lcmp.mod250.not = icmp eq i64 %xtraiter247, 0
  br label %.lr.ph.us138.us.preheader

.lr.ph.us138.us.preheader:                        ; preds = %.lr.ph.us138.us.preheader.preheader, %.loopexit.us
  %indvars.iv207 = phi i64 [ %indvars.iv.next208, %.loopexit.us ], [ 0, %.lr.ph.us138.us.preheader.preheader ]
  %indvars.iv200 = phi i64 [ %indvars.iv.next201, %.loopexit.us ], [ 1, %.lr.ph.us138.us.preheader.preheader ]
  %115 = mul nuw nsw i64 %indvars.iv207, %8
  %116 = getelementptr inbounds nuw double, ptr %5, i64 %115
  %117 = getelementptr inbounds nuw double, ptr %116, i64 %indvars.iv207
  store double 1.000000e+00, ptr %117, align 8
  %indvars.iv.next208 = add nuw nsw i64 %indvars.iv207, 1
  %invariant.gep.us142 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv207
  br label %.lr.ph.us138.us

.loopexit.us:                                     ; preds = %._crit_edge.us140.us
  %indvars.iv.next201 = add nuw nsw i64 %indvars.iv200, 1
  %exitcond211.not = icmp eq i64 %indvars.iv.next208, %wide.trip.count210
  br i1 %exitcond211.not, label %._crit_edge, label %.lr.ph.us138.us.preheader, !llvm.loop !24

.lr.ph.us138.us:                                  ; preds = %.lr.ph.us138.us.preheader, %._crit_edge.us140.us
  %indvars.iv202 = phi i64 [ %indvars.iv200, %.lr.ph.us138.us.preheader ], [ %indvars.iv.next203, %._crit_edge.us140.us ]
  %118 = getelementptr inbounds nuw double, ptr %116, i64 %indvars.iv202
  store double 0.000000e+00, ptr %118, align 8
  br i1 %114, label %._crit_edge.us140.us.unr-lcssa, label %.lr.ph.us138.us.new

.lr.ph.us138.us.new:                              ; preds = %.lr.ph.us138.us, %.lr.ph.us138.us.new
  %indvars.iv195 = phi i64 [ %indvars.iv.next196.1, %.lr.ph.us138.us.new ], [ 0, %.lr.ph.us138.us ]
  %119 = phi double [ %133, %.lr.ph.us138.us.new ], [ 0.000000e+00, %.lr.ph.us138.us ]
  %niter253 = phi i64 [ %niter253.next.1, %.lr.ph.us138.us.new ], [ 0, %.lr.ph.us138.us ]
  %120 = mul nuw nsw i64 %indvars.iv195, %7
  %121 = getelementptr inbounds nuw double, ptr %2, i64 %120
  %122 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv207
  %123 = load double, ptr %122, align 8
  %124 = getelementptr inbounds nuw double, ptr %121, i64 %indvars.iv202
  %125 = load double, ptr %124, align 8
  %126 = tail call double @llvm.fmuladd.f64(double %123, double %125, double %119)
  store double %126, ptr %118, align 8
  %indvars.iv.next196 = or disjoint i64 %indvars.iv195, 1
  %127 = mul nuw nsw i64 %indvars.iv.next196, %7
  %128 = getelementptr inbounds nuw double, ptr %2, i64 %127
  %129 = getelementptr inbounds nuw double, ptr %128, i64 %indvars.iv207
  %130 = load double, ptr %129, align 8
  %131 = getelementptr inbounds nuw double, ptr %128, i64 %indvars.iv202
  %132 = load double, ptr %131, align 8
  %133 = tail call double @llvm.fmuladd.f64(double %130, double %132, double %126)
  store double %133, ptr %118, align 8
  %indvars.iv.next196.1 = add nuw nsw i64 %indvars.iv195, 2
  %niter253.next.1 = add i64 %niter253, 2
  %niter253.ncmp.1 = icmp eq i64 %niter253.next.1, %unroll_iter252
  br i1 %niter253.ncmp.1, label %._crit_edge.us140.us.unr-lcssa, label %.lr.ph.us138.us.new, !llvm.loop !25

._crit_edge.us140.us.unr-lcssa:                   ; preds = %.lr.ph.us138.us.new, %.lr.ph.us138.us
  %.lcssa.ph = phi double [ poison, %.lr.ph.us138.us ], [ %133, %.lr.ph.us138.us.new ]
  %indvars.iv195.unr = phi i64 [ 0, %.lr.ph.us138.us ], [ %indvars.iv.next196.1, %.lr.ph.us138.us.new ]
  %.unr249 = phi double [ 0.000000e+00, %.lr.ph.us138.us ], [ %133, %.lr.ph.us138.us.new ]
  br i1 %lcmp.mod250.not, label %._crit_edge.us140.us, label %._crit_edge.us140.us.epilog-lcssa

._crit_edge.us140.us.epilog-lcssa:                ; preds = %._crit_edge.us140.us.unr-lcssa
  %134 = mul nuw nsw i64 %indvars.iv195.unr, %7
  %135 = getelementptr inbounds nuw double, ptr %2, i64 %134
  %136 = getelementptr inbounds nuw double, ptr %135, i64 %indvars.iv207
  %137 = load double, ptr %136, align 8
  %138 = getelementptr inbounds nuw double, ptr %135, i64 %indvars.iv202
  %139 = load double, ptr %138, align 8
  %140 = tail call double @llvm.fmuladd.f64(double %137, double %139, double %.unr249)
  store double %140, ptr %118, align 8
  br label %._crit_edge.us140.us

._crit_edge.us140.us:                             ; preds = %._crit_edge.us140.us.unr-lcssa, %._crit_edge.us140.us.epilog-lcssa
  %.lcssa = phi double [ %.lcssa.ph, %._crit_edge.us140.us.unr-lcssa ], [ %140, %._crit_edge.us140.us.epilog-lcssa ]
  %141 = mul nuw nsw i64 %indvars.iv202, %8
  %gep.us137.us = getelementptr inbounds nuw double, ptr %invariant.gep.us142, i64 %141
  store double %.lcssa, ptr %gep.us137.us, align 8
  %indvars.iv.next203 = add nuw nsw i64 %indvars.iv202, 1
  %exitcond206.not = icmp eq i64 %indvars.iv.next203, %8
  br i1 %exitcond206.not, label %.loopexit.us, label %.lr.ph.us138.us, !llvm.loop !26

.loopexit:                                        ; preds = %.lr.ph136, %.lr.ph136.prol.loopexit
  %indvars.iv.next184 = add nuw nsw i64 %indvars.iv183, 1
  %exitcond194.not = icmp eq i64 %indvars.iv.next191, %wide.trip.count210
  br i1 %exitcond194.not, label %._crit_edge, label %.lr.ph136.preheader, !llvm.loop !24

.lr.ph136.preheader:                              ; preds = %.lr.ph136.preheader.preheader, %.loopexit
  %indvars.iv190 = phi i64 [ %indvars.iv.next191, %.loopexit ], [ 0, %.lr.ph136.preheader.preheader ]
  %indvars.iv183 = phi i64 [ %indvars.iv.next184, %.loopexit ], [ 1, %.lr.ph136.preheader.preheader ]
  %142 = xor i64 %indvars.iv190, -1
  %143 = add nsw i64 %142, %8
  %144 = sub i64 %113, %indvars.iv190
  %145 = mul nuw nsw i64 %indvars.iv190, %8
  %146 = getelementptr inbounds nuw double, ptr %5, i64 %145
  %147 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv190
  store double 1.000000e+00, ptr %147, align 8
  %indvars.iv.next191 = add nuw nsw i64 %indvars.iv190, 1
  %invariant.gep = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv190
  %xtraiter244 = and i64 %143, 3
  %lcmp.mod245.not = icmp eq i64 %xtraiter244, 0
  br i1 %lcmp.mod245.not, label %.lr.ph136.prol.loopexit, label %.lr.ph136.prol

.lr.ph136.prol:                                   ; preds = %.lr.ph136.preheader, %.lr.ph136.prol
  %indvars.iv185.prol = phi i64 [ %indvars.iv.next186.prol, %.lr.ph136.prol ], [ %indvars.iv183, %.lr.ph136.preheader ]
  %prol.iter = phi i64 [ %prol.iter.next, %.lr.ph136.prol ], [ 0, %.lr.ph136.preheader ]
  %148 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv185.prol
  store double 0.000000e+00, ptr %148, align 8
  %149 = mul nuw nsw i64 %indvars.iv185.prol, %8
  %gep.prol = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %149
  store double 0.000000e+00, ptr %gep.prol, align 8
  %indvars.iv.next186.prol = add nuw nsw i64 %indvars.iv185.prol, 1
  %prol.iter.next = add i64 %prol.iter, 1
  %prol.iter.cmp.not = icmp eq i64 %prol.iter.next, %xtraiter244
  br i1 %prol.iter.cmp.not, label %.lr.ph136.prol.loopexit, label %.lr.ph136.prol, !llvm.loop !27

.lr.ph136.prol.loopexit:                          ; preds = %.lr.ph136.prol, %.lr.ph136.preheader
  %indvars.iv185.unr = phi i64 [ %indvars.iv183, %.lr.ph136.preheader ], [ %indvars.iv.next186.prol, %.lr.ph136.prol ]
  %150 = icmp ult i64 %144, 3
  br i1 %150, label %.loopexit, label %.lr.ph136

.lr.ph136:                                        ; preds = %.lr.ph136.prol.loopexit, %.lr.ph136
  %indvars.iv185 = phi i64 [ %indvars.iv.next186.3, %.lr.ph136 ], [ %indvars.iv185.unr, %.lr.ph136.prol.loopexit ]
  %151 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv185
  store double 0.000000e+00, ptr %151, align 8
  %152 = mul nuw nsw i64 %indvars.iv185, %8
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %152
  store double 0.000000e+00, ptr %gep, align 8
  %indvars.iv.next186 = add nuw nsw i64 %indvars.iv185, 1
  %153 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv.next186
  store double 0.000000e+00, ptr %153, align 8
  %154 = mul nuw nsw i64 %indvars.iv.next186, %8
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %154
  store double 0.000000e+00, ptr %gep.1, align 8
  %indvars.iv.next186.1 = add nuw nsw i64 %indvars.iv185, 2
  %155 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv.next186.1
  store double 0.000000e+00, ptr %155, align 8
  %156 = mul nuw nsw i64 %indvars.iv.next186.1, %8
  %gep.2 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %156
  store double 0.000000e+00, ptr %gep.2, align 8
  %indvars.iv.next186.2 = add nuw nsw i64 %indvars.iv185, 3
  %157 = getelementptr inbounds nuw double, ptr %146, i64 %indvars.iv.next186.2
  store double 0.000000e+00, ptr %157, align 8
  %158 = mul nuw nsw i64 %indvars.iv.next186.2, %8
  %gep.3 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %158
  store double 0.000000e+00, ptr %gep.3, align 8
  %indvars.iv.next186.3 = add nuw nsw i64 %indvars.iv185, 4
  %exitcond189.not.3 = icmp eq i64 %indvars.iv.next186.3, %8
  br i1 %exitcond189.not.3, label %.loopexit, label %.lr.ph136, !llvm.loop !26

._crit_edge:                                      ; preds = %.loopexit, %.loopexit.us, %.preheader.thread, %.preheader
  %159 = phi i32 [ %66, %.preheader.thread ], [ %111, %.preheader ], [ %111, %.loopexit.us ], [ %111, %.loopexit ]
  %160 = sext i32 %159 to i64
  %161 = mul nsw i64 %160, %8
  %162 = getelementptr inbounds double, ptr %5, i64 %161
  %163 = getelementptr inbounds double, ptr %162, i64 %160
  store double 1.000000e+00, ptr %163, align 8
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
!14 = distinct !{!14, !9, !10, !11}
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !17}
!17 = !{!"llvm.loop.unroll.disable"}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
!20 = distinct !{!20, !9}
!21 = distinct !{!21, !9, !11, !10}
!22 = distinct !{!22, !9}
!23 = distinct !{!23, !9}
!24 = distinct !{!24, !9}
!25 = distinct !{!25, !9}
!26 = distinct !{!26, !9}
!27 = distinct !{!27, !17}
