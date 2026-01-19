; ModuleID = 'results\baseline\atax_base.ll'
source_filename = "benchmarks\\atax.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"ATAX Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef writeonly captures(none) %2, ptr noundef writeonly captures(none) %3) local_unnamed_addr #0 {
  %5 = zext i32 %1 to i64
  %6 = icmp sgt i32 %1, 0
  br i1 %6, label %.lr.ph, label %._crit_edge30

.lr.ph:                                           ; preds = %4
  %7 = uitofp nneg i32 %1 to double
  %min.iters.check = icmp eq i32 %1, 1
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %n.vec = and i64 %5, 2147483646
  %broadcast.splatinsert = insertelement <2 x double> poison, double %7, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %8 = uitofp nneg <2 x i32> %vec.ind to <2 x double>
  %9 = fdiv <2 x double> %8, %broadcast.splat
  %10 = fadd <2 x double> %9, splat (double 1.000000e+00)
  %11 = getelementptr inbounds nuw double, ptr %3, i64 %index
  store <2 x double> %10, ptr %11, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %12 = icmp eq i64 %index.next, %n.vec
  br i1 %12, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  %cmp.n = icmp eq i64 %n.vec, %5
  br i1 %cmp.n, label %.preheader25, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  br label %scalar.ph

.preheader25:                                     ; preds = %scalar.ph, %middle.block
  %13 = icmp sgt i32 %0, 0
  br i1 %13, label %.preheader.lr.ph, label %._crit_edge30

.preheader.lr.ph:                                 ; preds = %.preheader25
  %14 = uitofp nneg i32 %0 to double
  %wide.trip.count41 = zext nneg i32 %0 to i64
  %min.iters.check44 = icmp eq i32 %1, 1
  %n.vec47 = and i64 %5, 2147483646
  %broadcast.splatinsert50 = insertelement <2 x double> poison, double %14, i64 0
  %broadcast.splat51 = shufflevector <2 x double> %broadcast.splatinsert50, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n58 = icmp eq i64 %n.vec47, %5
  br label %.preheader.us

.preheader.us:                                    ; preds = %.preheader.lr.ph, %._crit_edge.us
  %indvars.iv38 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next39, %._crit_edge.us ]
  %15 = trunc nuw nsw i64 %indvars.iv38 to i32
  %16 = uitofp nneg i32 %15 to double
  %17 = mul nuw nsw i64 %indvars.iv38, %5
  %18 = getelementptr inbounds nuw double, ptr %2, i64 %17
  br i1 %min.iters.check44, label %scalar.ph43.preheader, label %vector.ph45

vector.ph45:                                      ; preds = %.preheader.us
  %broadcast.splatinsert48 = insertelement <2 x double> poison, double %16, i64 0
  %broadcast.splat49 = shufflevector <2 x double> %broadcast.splatinsert48, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body52

vector.body52:                                    ; preds = %vector.body52, %vector.ph45
  %index53 = phi i64 [ 0, %vector.ph45 ], [ %index.next55, %vector.body52 ]
  %vec.ind54 = phi <2 x i64> [ <i64 0, i64 1>, %vector.ph45 ], [ %vec.ind.next56, %vector.body52 ]
  %19 = trunc <2 x i64> %vec.ind54 to <2 x i32>
  %20 = add <2 x i32> %19, splat (i32 1)
  %21 = uitofp nneg <2 x i32> %20 to <2 x double>
  %22 = fmul <2 x double> %broadcast.splat49, %21
  %23 = fdiv <2 x double> %22, %broadcast.splat51
  %24 = getelementptr inbounds nuw double, ptr %18, i64 %index53
  store <2 x double> %23, ptr %24, align 8
  %index.next55 = add nuw i64 %index53, 2
  %vec.ind.next56 = add <2 x i64> %vec.ind54, splat (i64 2)
  %25 = icmp eq i64 %index.next55, %n.vec47
  br i1 %25, label %middle.block57, label %vector.body52, !llvm.loop !12

middle.block57:                                   ; preds = %vector.body52
  br i1 %cmp.n58, label %._crit_edge.us, label %scalar.ph43.preheader

scalar.ph43.preheader:                            ; preds = %.preheader.us, %middle.block57
  %indvars.iv33.ph = phi i64 [ 0, %.preheader.us ], [ %n.vec47, %middle.block57 ]
  br label %scalar.ph43

scalar.ph43:                                      ; preds = %scalar.ph43.preheader, %scalar.ph43
  %indvars.iv33 = phi i64 [ %indvars.iv.next34, %scalar.ph43 ], [ %indvars.iv33.ph, %scalar.ph43.preheader ]
  %indvars.iv.next34 = add nuw nsw i64 %indvars.iv33, 1
  %26 = trunc nuw nsw i64 %indvars.iv.next34 to i32
  %27 = uitofp nneg i32 %26 to double
  %28 = fmul double %16, %27
  %29 = fdiv double %28, %14
  %30 = getelementptr inbounds nuw double, ptr %18, i64 %indvars.iv33
  store double %29, ptr %30, align 8
  %exitcond37.not = icmp eq i64 %indvars.iv.next34, %5
  br i1 %exitcond37.not, label %._crit_edge.us, label %scalar.ph43, !llvm.loop !13

._crit_edge.us:                                   ; preds = %scalar.ph43, %middle.block57
  %indvars.iv.next39 = add nuw nsw i64 %indvars.iv38, 1
  %exitcond42.not = icmp eq i64 %indvars.iv.next39, %wide.trip.count41
  br i1 %exitcond42.not, label %._crit_edge30, label %.preheader.us, !llvm.loop !14

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %31 = trunc nuw nsw i64 %indvars.iv to i32
  %32 = uitofp nneg i32 %31 to double
  %33 = fdiv double %32, %7
  %34 = fadd double %33, 1.000000e+00
  %35 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %34, ptr %35, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %5
  br i1 %exitcond.not, label %.preheader25, label %scalar.ph, !llvm.loop !15

._crit_edge30:                                    ; preds = %._crit_edge.us, %4, %.preheader25
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @atax(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef readonly captures(none) %3, ptr noundef captures(none) %4, ptr noundef captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %1 to i64
  %8 = icmp sgt i32 %1, 0
  br i1 %8, label %.preheader38, label %.preheader38.thread

.preheader38:                                     ; preds = %6
  %9 = shl nuw nsw i64 %7, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %4, i8 0, i64 %9, i1 false)
  %10 = icmp sgt i32 %0, 0
  br i1 %10, label %.lr.ph41.us.us.preheader, label %._crit_edge46

.preheader38.thread:                              ; preds = %6
  %11 = icmp sgt i32 %0, 0
  br i1 %11, label %.preheader.preheader, label %._crit_edge46

.preheader.preheader:                             ; preds = %.preheader38.thread
  %12 = zext nneg i32 %0 to i64
  %13 = shl nuw nsw i64 %12, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %5, i8 0, i64 %13, i1 false)
  br label %._crit_edge46

.lr.ph41.us.us.preheader:                         ; preds = %.preheader38
  %wide.trip.count64 = zext nneg i32 %0 to i64
  %14 = shl nuw nsw i64 %7, 3
  %scevgep = getelementptr i8, ptr %4, i64 %14
  %15 = mul nuw nsw i64 %7, %wide.trip.count64
  %16 = shl i64 %15, 3
  %scevgep66 = getelementptr i8, ptr %2, i64 %16
  %17 = shl nuw nsw i64 %wide.trip.count64, 3
  %scevgep67 = getelementptr i8, ptr %5, i64 %17
  %xtraiter = and i64 %7, 1
  %18 = icmp eq i32 %1, 1
  %unroll_iter = and i64 %7, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %min.iters.check = icmp ult i32 %1, 4
  %bound0 = icmp ult ptr %4, %scevgep66
  %bound1 = icmp ult ptr %2, %scevgep
  %found.conflict = and i1 %bound0, %bound1
  %bound068 = icmp ult ptr %4, %scevgep67
  %bound169 = icmp ult ptr %5, %scevgep
  %found.conflict70 = and i1 %bound068, %bound169
  %conflict.rdx = or i1 %found.conflict, %found.conflict70
  %n.vec = and i64 %7, 2147483644
  %cmp.n = icmp eq i64 %n.vec, %7
  %xtraiter75 = and i64 %7, 1
  %lcmp.mod76.not = icmp eq i64 %xtraiter75, 0
  %19 = add nsw i64 %7, -1
  br label %.lr.ph41.us.us

.lr.ph41.us.us:                                   ; preds = %.lr.ph41.us.us.preheader, %._crit_edge.us.us
  %indvars.iv61 = phi i64 [ 0, %.lr.ph41.us.us.preheader ], [ %indvars.iv.next62, %._crit_edge.us.us ]
  %20 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv61
  store double 0.000000e+00, ptr %20, align 8
  %21 = mul nuw nsw i64 %indvars.iv61, %7
  %22 = getelementptr inbounds nuw double, ptr %2, i64 %21
  br i1 %18, label %..preheader_crit_edge.us.us.preheader.unr-lcssa, label %.lr.ph41.us.us.new

..preheader_crit_edge.us.us:                      ; preds = %..preheader_crit_edge.us.us.prol.loopexit, %..preheader_crit_edge.us.us
  %indvars.iv56 = phi i64 [ %indvars.iv.next57.1, %..preheader_crit_edge.us.us ], [ %indvars.iv56.unr, %..preheader_crit_edge.us.us.prol.loopexit ]
  %23 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv56
  %24 = load double, ptr %23, align 8
  %25 = load double, ptr %20, align 8
  %26 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv56
  %27 = load double, ptr %26, align 8
  %28 = tail call double @llvm.fmuladd.f64(double %24, double %25, double %27)
  store double %28, ptr %26, align 8
  %indvars.iv.next57 = add nuw nsw i64 %indvars.iv56, 1
  %29 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv.next57
  %30 = load double, ptr %29, align 8
  %31 = load double, ptr %20, align 8
  %32 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next57
  %33 = load double, ptr %32, align 8
  %34 = tail call double @llvm.fmuladd.f64(double %30, double %31, double %33)
  store double %34, ptr %32, align 8
  %indvars.iv.next57.1 = add nuw nsw i64 %indvars.iv56, 2
  %exitcond60.not.1 = icmp eq i64 %indvars.iv.next57.1, %7
  br i1 %exitcond60.not.1, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us, !llvm.loop !16

.lr.ph41.us.us.new:                               ; preds = %.lr.ph41.us.us, %.lr.ph41.us.us.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph41.us.us.new ], [ 0, %.lr.ph41.us.us ]
  %35 = phi double [ %45, %.lr.ph41.us.us.new ], [ 0.000000e+00, %.lr.ph41.us.us ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph41.us.us.new ], [ 0, %.lr.ph41.us.us ]
  %36 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv
  %37 = load double, ptr %36, align 8
  %38 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %39 = load double, ptr %38, align 8
  %40 = tail call double @llvm.fmuladd.f64(double %37, double %39, double %35)
  store double %40, ptr %20, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %41 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv.next
  %42 = load double, ptr %41, align 8
  %43 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  %44 = load double, ptr %43, align 8
  %45 = tail call double @llvm.fmuladd.f64(double %42, double %44, double %40)
  store double %45, ptr %20, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %..preheader_crit_edge.us.us.preheader.unr-lcssa, label %.lr.ph41.us.us.new, !llvm.loop !17

..preheader_crit_edge.us.us.preheader.unr-lcssa:  ; preds = %.lr.ph41.us.us.new, %.lr.ph41.us.us
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph41.us.us ], [ %indvars.iv.next.1, %.lr.ph41.us.us.new ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph41.us.us ], [ %45, %.lr.ph41.us.us.new ]
  br i1 %lcmp.mod.not, label %..preheader_crit_edge.us.us.preheader, label %..preheader_crit_edge.us.us.preheader.epilog-lcssa

..preheader_crit_edge.us.us.preheader.epilog-lcssa: ; preds = %..preheader_crit_edge.us.us.preheader.unr-lcssa
  %46 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv.unr
  %47 = load double, ptr %46, align 8
  %48 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  %49 = load double, ptr %48, align 8
  %50 = tail call double @llvm.fmuladd.f64(double %47, double %49, double %.unr)
  store double %50, ptr %20, align 8
  br label %..preheader_crit_edge.us.us.preheader

..preheader_crit_edge.us.us.preheader:            ; preds = %..preheader_crit_edge.us.us.preheader.unr-lcssa, %..preheader_crit_edge.us.us.preheader.epilog-lcssa
  %brmerge = select i1 %min.iters.check, i1 true, i1 %conflict.rdx
  br i1 %brmerge, label %..preheader_crit_edge.us.us.preheader74, label %vector.ph

vector.ph:                                        ; preds = %..preheader_crit_edge.us.us.preheader
  %51 = load double, ptr %20, align 8, !alias.scope !18
  %broadcast.splatinsert = insertelement <2 x double> poison, double %51, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %52 = getelementptr inbounds nuw double, ptr %22, i64 %index
  %53 = getelementptr inbounds nuw i8, ptr %52, i64 16
  %wide.load = load <2 x double>, ptr %52, align 8, !alias.scope !21
  %wide.load71 = load <2 x double>, ptr %53, align 8, !alias.scope !21
  %54 = getelementptr inbounds nuw double, ptr %4, i64 %index
  %55 = getelementptr inbounds nuw i8, ptr %54, i64 16
  %wide.load72 = load <2 x double>, ptr %54, align 8, !alias.scope !23, !noalias !25
  %wide.load73 = load <2 x double>, ptr %55, align 8, !alias.scope !23, !noalias !25
  %56 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %wide.load, <2 x double> %broadcast.splat, <2 x double> %wide.load72)
  %57 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %wide.load71, <2 x double> %broadcast.splat, <2 x double> %wide.load73)
  store <2 x double> %56, ptr %54, align 8, !alias.scope !23, !noalias !25
  store <2 x double> %57, ptr %55, align 8, !alias.scope !23, !noalias !25
  %index.next = add nuw i64 %index, 4
  %58 = icmp eq i64 %index.next, %n.vec
  br i1 %58, label %middle.block, label %vector.body, !llvm.loop !26

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us.preheader74

..preheader_crit_edge.us.us.preheader74:          ; preds = %..preheader_crit_edge.us.us.preheader, %middle.block
  %indvars.iv56.ph = phi i64 [ 0, %..preheader_crit_edge.us.us.preheader ], [ %n.vec, %middle.block ]
  br i1 %lcmp.mod76.not, label %..preheader_crit_edge.us.us.prol.loopexit, label %..preheader_crit_edge.us.us.prol

..preheader_crit_edge.us.us.prol:                 ; preds = %..preheader_crit_edge.us.us.preheader74
  %59 = getelementptr inbounds nuw double, ptr %22, i64 %indvars.iv56.ph
  %60 = load double, ptr %59, align 8
  %61 = load double, ptr %20, align 8
  %62 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv56.ph
  %63 = load double, ptr %62, align 8
  %64 = tail call double @llvm.fmuladd.f64(double %60, double %61, double %63)
  store double %64, ptr %62, align 8
  %indvars.iv.next57.prol = or disjoint i64 %indvars.iv56.ph, 1
  br label %..preheader_crit_edge.us.us.prol.loopexit

..preheader_crit_edge.us.us.prol.loopexit:        ; preds = %..preheader_crit_edge.us.us.prol, %..preheader_crit_edge.us.us.preheader74
  %indvars.iv56.unr = phi i64 [ %indvars.iv56.ph, %..preheader_crit_edge.us.us.preheader74 ], [ %indvars.iv.next57.prol, %..preheader_crit_edge.us.us.prol ]
  %65 = icmp eq i64 %indvars.iv56.ph, %19
  br i1 %65, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us

._crit_edge.us.us:                                ; preds = %..preheader_crit_edge.us.us.prol.loopexit, %..preheader_crit_edge.us.us, %middle.block
  %indvars.iv.next62 = add nuw nsw i64 %indvars.iv61, 1
  %exitcond65.not = icmp eq i64 %indvars.iv.next62, %wide.trip.count64
  br i1 %exitcond65.not, label %._crit_edge46, label %.lr.ph41.us.us, !llvm.loop !27

._crit_edge46:                                    ; preds = %._crit_edge.us.us, %.preheader38.thread, %.preheader.preheader, %.preheader38
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #3 {
  %1 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #9
  %2 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #9
  %3 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #9
  %4 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #9
  tail call void @init_array(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %2)
  %5 = tail call i32 @clock() #10
  tail call void @atax(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4)
  %6 = tail call i32 @clock() #10
  %7 = sub nsw i32 %6, %5
  %8 = sitofp i32 %7 to double
  %9 = fdiv double %8, 1.000000e+03
  %10 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %9) #10
  %11 = load double, ptr %3, align 8
  %12 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %11) #10
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  tail call void @free(ptr noundef %4)
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

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare <2 x double> @llvm.fmuladd.v2f64(<2 x double>, <2 x double>, <2 x double>) #8

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nocallback nofree nounwind willreturn memory(argmem: write) }
attributes #8 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #9 = { allocsize(0) }
attributes #10 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/atax.c", directory: "C:/Users/ultim/compiler-opt")
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
!12 = distinct !{!12, !9, !10, !11}
!13 = distinct !{!13, !9, !11, !10}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !9, !11, !10}
!16 = distinct !{!16, !9, !10}
!17 = distinct !{!17, !9}
!18 = !{!19}
!19 = distinct !{!19, !20}
!20 = distinct !{!20, !"LVerDomain"}
!21 = !{!22}
!22 = distinct !{!22, !20}
!23 = !{!24}
!24 = distinct !{!24, !20}
!25 = !{!22, !19}
!26 = distinct !{!26, !9, !10, !11}
!27 = distinct !{!27, !9}
