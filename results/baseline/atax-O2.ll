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
  br i1 %6, label %.lr.ph, label %.preheader25

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

.preheader25:                                     ; preds = %scalar.ph, %middle.block, %4
  %13 = icmp sgt i32 %0, 0
  br i1 %13, label %.preheader.lr.ph, label %._crit_edge30

.preheader.lr.ph:                                 ; preds = %.preheader25
  %14 = uitofp nneg i32 %0 to double
  %wide.trip.count40 = zext nneg i32 %0 to i64
  %min.iters.check43 = icmp eq i32 %1, 1
  %n.vec46 = and i64 %5, 2147483646
  %broadcast.splatinsert49 = insertelement <2 x double> poison, double %14, i64 0
  %broadcast.splat50 = shufflevector <2 x double> %broadcast.splatinsert49, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n57 = icmp eq i64 %n.vec46, %5
  br label %.preheader

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %15 = trunc nuw nsw i64 %indvars.iv to i32
  %16 = uitofp nneg i32 %15 to double
  %17 = fdiv double %16, %7
  %18 = fadd double %17, 1.000000e+00
  %19 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %18, ptr %19, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %5
  br i1 %exitcond.not, label %.preheader25, label %scalar.ph, !llvm.loop !12

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv37 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next38, %._crit_edge ]
  br i1 %6, label %.lr.ph28, label %._crit_edge

.lr.ph28:                                         ; preds = %.preheader
  %20 = trunc nuw nsw i64 %indvars.iv37 to i32
  %21 = uitofp nneg i32 %20 to double
  %22 = mul nuw nsw i64 %indvars.iv37, %5
  %23 = getelementptr inbounds nuw double, ptr %2, i64 %22
  br i1 %min.iters.check43, label %scalar.ph42.preheader, label %vector.ph44

vector.ph44:                                      ; preds = %.lr.ph28
  %broadcast.splatinsert47 = insertelement <2 x double> poison, double %21, i64 0
  %broadcast.splat48 = shufflevector <2 x double> %broadcast.splatinsert47, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body51

vector.body51:                                    ; preds = %vector.body51, %vector.ph44
  %index52 = phi i64 [ 0, %vector.ph44 ], [ %index.next54, %vector.body51 ]
  %vec.ind53 = phi <2 x i64> [ <i64 0, i64 1>, %vector.ph44 ], [ %vec.ind.next55, %vector.body51 ]
  %24 = trunc <2 x i64> %vec.ind53 to <2 x i32>
  %25 = add <2 x i32> %24, splat (i32 1)
  %26 = uitofp nneg <2 x i32> %25 to <2 x double>
  %27 = fmul <2 x double> %broadcast.splat48, %26
  %28 = fdiv <2 x double> %27, %broadcast.splat50
  %29 = getelementptr inbounds nuw double, ptr %23, i64 %index52
  store <2 x double> %28, ptr %29, align 8
  %index.next54 = add nuw i64 %index52, 2
  %vec.ind.next55 = add <2 x i64> %vec.ind53, splat (i64 2)
  %30 = icmp eq i64 %index.next54, %n.vec46
  br i1 %30, label %middle.block56, label %vector.body51, !llvm.loop !13

middle.block56:                                   ; preds = %vector.body51
  br i1 %cmp.n57, label %._crit_edge, label %scalar.ph42.preheader

scalar.ph42.preheader:                            ; preds = %.lr.ph28, %middle.block56
  %indvars.iv32.ph = phi i64 [ 0, %.lr.ph28 ], [ %n.vec46, %middle.block56 ]
  br label %scalar.ph42

scalar.ph42:                                      ; preds = %scalar.ph42.preheader, %scalar.ph42
  %indvars.iv32 = phi i64 [ %indvars.iv.next33, %scalar.ph42 ], [ %indvars.iv32.ph, %scalar.ph42.preheader ]
  %indvars.iv.next33 = add nuw nsw i64 %indvars.iv32, 1
  %31 = trunc nuw nsw i64 %indvars.iv.next33 to i32
  %32 = uitofp nneg i32 %31 to double
  %33 = fmul double %21, %32
  %34 = fdiv double %33, %14
  %35 = getelementptr inbounds nuw double, ptr %23, i64 %indvars.iv32
  store double %34, ptr %35, align 8
  %exitcond36.not = icmp eq i64 %indvars.iv.next33, %5
  br i1 %exitcond36.not, label %._crit_edge, label %scalar.ph42, !llvm.loop !14

._crit_edge:                                      ; preds = %scalar.ph42, %middle.block56, %.preheader
  %indvars.iv.next38 = add nuw nsw i64 %indvars.iv37, 1
  %exitcond41.not = icmp eq i64 %indvars.iv.next38, %wide.trip.count40
  br i1 %exitcond41.not, label %._crit_edge30, label %.preheader, !llvm.loop !15

._crit_edge30:                                    ; preds = %._crit_edge, %.preheader25
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @atax(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef readonly captures(none) %3, ptr noundef captures(none) %4, ptr noundef captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %1 to i64
  %8 = icmp sgt i32 %1, 0
  br i1 %8, label %.lr.ph.preheader, label %.preheader38

.lr.ph.preheader:                                 ; preds = %6
  %9 = shl nuw nsw i64 %7, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %4, i8 0, i64 %9, i1 false)
  br label %.preheader38

.preheader38:                                     ; preds = %.lr.ph.preheader, %6
  %10 = icmp sgt i32 %0, 0
  br i1 %10, label %.lr.ph45, label %._crit_edge46

.lr.ph45:                                         ; preds = %.preheader38
  %wide.trip.count57 = zext nneg i32 %0 to i64
  %11 = shl nuw nsw i64 %7, 3
  %scevgep = getelementptr i8, ptr %4, i64 %11
  %12 = mul nuw nsw i64 %7, %wide.trip.count57
  %13 = shl i64 %12, 3
  %scevgep59 = getelementptr i8, ptr %2, i64 %13
  %14 = shl nuw nsw i64 %wide.trip.count57, 3
  %scevgep60 = getelementptr i8, ptr %5, i64 %14
  %xtraiter = and i64 %7, 1
  %15 = icmp eq i32 %1, 1
  %unroll_iter = and i64 %7, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %min.iters.check = icmp ult i32 %1, 4
  %bound0 = icmp ult ptr %4, %scevgep59
  %bound1 = icmp ult ptr %2, %scevgep
  %found.conflict = and i1 %bound0, %bound1
  %bound061 = icmp ult ptr %4, %scevgep60
  %bound162 = icmp ult ptr %5, %scevgep
  %found.conflict63 = and i1 %bound061, %bound162
  %conflict.rdx = or i1 %found.conflict, %found.conflict63
  %n.vec = and i64 %7, 2147483644
  %cmp.n = icmp eq i64 %n.vec, %7
  %xtraiter67 = and i64 %7, 1
  %lcmp.mod68.not = icmp eq i64 %xtraiter67, 0
  %16 = add nsw i64 %7, -1
  br label %17

17:                                               ; preds = %.lr.ph45, %._crit_edge
  %indvars.iv54 = phi i64 [ 0, %.lr.ph45 ], [ %indvars.iv.next55, %._crit_edge ]
  %18 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv54
  store double 0.000000e+00, ptr %18, align 8
  br i1 %8, label %.lr.ph41, label %._crit_edge

.lr.ph41:                                         ; preds = %17
  %19 = mul nuw nsw i64 %indvars.iv54, %7
  %20 = getelementptr inbounds nuw double, ptr %2, i64 %19
  br i1 %15, label %.lr.ph43.unr-lcssa, label %.lr.ph41.new

.lr.ph43.unr-lcssa:                               ; preds = %.lr.ph41.new, %.lr.ph41
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph41 ], [ %indvars.iv.next.1, %.lr.ph41.new ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph41 ], [ %53, %.lr.ph41.new ]
  br i1 %lcmp.mod.not, label %.lr.ph43, label %.lr.ph43.epilog-lcssa

.lr.ph43.epilog-lcssa:                            ; preds = %.lr.ph43.unr-lcssa
  %21 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv.unr
  %22 = load double, ptr %21, align 8
  %23 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  %24 = load double, ptr %23, align 8
  %25 = tail call double @llvm.fmuladd.f64(double %22, double %24, double %.unr)
  store double %25, ptr %18, align 8
  br label %.lr.ph43

.lr.ph43:                                         ; preds = %.lr.ph43.unr-lcssa, %.lr.ph43.epilog-lcssa
  %26 = mul nuw nsw i64 %indvars.iv54, %7
  %27 = getelementptr inbounds nuw double, ptr %2, i64 %26
  %brmerge = select i1 %min.iters.check, i1 true, i1 %conflict.rdx
  br i1 %brmerge, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph43
  %28 = load double, ptr %18, align 8, !alias.scope !16
  %broadcast.splatinsert = insertelement <2 x double> poison, double %28, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %29 = getelementptr inbounds nuw double, ptr %27, i64 %index
  %30 = getelementptr inbounds nuw i8, ptr %29, i64 16
  %wide.load = load <2 x double>, ptr %29, align 8, !alias.scope !19
  %wide.load64 = load <2 x double>, ptr %30, align 8, !alias.scope !19
  %31 = getelementptr inbounds nuw double, ptr %4, i64 %index
  %32 = getelementptr inbounds nuw i8, ptr %31, i64 16
  %wide.load65 = load <2 x double>, ptr %31, align 8, !alias.scope !21, !noalias !23
  %wide.load66 = load <2 x double>, ptr %32, align 8, !alias.scope !21, !noalias !23
  %33 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %wide.load, <2 x double> %broadcast.splat, <2 x double> %wide.load65)
  %34 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %wide.load64, <2 x double> %broadcast.splat, <2 x double> %wide.load66)
  store <2 x double> %33, ptr %31, align 8, !alias.scope !21, !noalias !23
  store <2 x double> %34, ptr %32, align 8, !alias.scope !21, !noalias !23
  %index.next = add nuw i64 %index, 4
  %35 = icmp eq i64 %index.next, %n.vec
  br i1 %35, label %middle.block, label %vector.body, !llvm.loop !24

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph43, %middle.block
  %indvars.iv49.ph = phi i64 [ 0, %.lr.ph43 ], [ %n.vec, %middle.block ]
  br i1 %lcmp.mod68.not, label %scalar.ph.prol.loopexit, label %scalar.ph.prol

scalar.ph.prol:                                   ; preds = %scalar.ph.preheader
  %36 = getelementptr inbounds nuw double, ptr %27, i64 %indvars.iv49.ph
  %37 = load double, ptr %36, align 8
  %38 = load double, ptr %18, align 8
  %39 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv49.ph
  %40 = load double, ptr %39, align 8
  %41 = tail call double @llvm.fmuladd.f64(double %37, double %38, double %40)
  store double %41, ptr %39, align 8
  %indvars.iv.next50.prol = or disjoint i64 %indvars.iv49.ph, 1
  br label %scalar.ph.prol.loopexit

scalar.ph.prol.loopexit:                          ; preds = %scalar.ph.prol, %scalar.ph.preheader
  %indvars.iv49.unr = phi i64 [ %indvars.iv49.ph, %scalar.ph.preheader ], [ %indvars.iv.next50.prol, %scalar.ph.prol ]
  %42 = icmp eq i64 %indvars.iv49.ph, %16
  br i1 %42, label %._crit_edge, label %scalar.ph

.lr.ph41.new:                                     ; preds = %.lr.ph41, %.lr.ph41.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %43 = phi double [ %53, %.lr.ph41.new ], [ 0.000000e+00, %.lr.ph41 ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %44 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv
  %45 = load double, ptr %44, align 8
  %46 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %47 = load double, ptr %46, align 8
  %48 = tail call double @llvm.fmuladd.f64(double %45, double %47, double %43)
  store double %48, ptr %18, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %49 = getelementptr inbounds nuw double, ptr %20, i64 %indvars.iv.next
  %50 = load double, ptr %49, align 8
  %51 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  %52 = load double, ptr %51, align 8
  %53 = tail call double @llvm.fmuladd.f64(double %50, double %52, double %48)
  store double %53, ptr %18, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %.lr.ph43.unr-lcssa, label %.lr.ph41.new, !llvm.loop !25

scalar.ph:                                        ; preds = %scalar.ph.prol.loopexit, %scalar.ph
  %indvars.iv49 = phi i64 [ %indvars.iv.next50.1, %scalar.ph ], [ %indvars.iv49.unr, %scalar.ph.prol.loopexit ]
  %54 = getelementptr inbounds nuw double, ptr %27, i64 %indvars.iv49
  %55 = load double, ptr %54, align 8
  %56 = load double, ptr %18, align 8
  %57 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv49
  %58 = load double, ptr %57, align 8
  %59 = tail call double @llvm.fmuladd.f64(double %55, double %56, double %58)
  store double %59, ptr %57, align 8
  %indvars.iv.next50 = add nuw nsw i64 %indvars.iv49, 1
  %60 = getelementptr inbounds nuw double, ptr %27, i64 %indvars.iv.next50
  %61 = load double, ptr %60, align 8
  %62 = load double, ptr %18, align 8
  %63 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next50
  %64 = load double, ptr %63, align 8
  %65 = tail call double @llvm.fmuladd.f64(double %61, double %62, double %64)
  store double %65, ptr %63, align 8
  %indvars.iv.next50.1 = add nuw nsw i64 %indvars.iv49, 2
  %exitcond53.not.1 = icmp eq i64 %indvars.iv.next50.1, %7
  br i1 %exitcond53.not.1, label %._crit_edge, label %scalar.ph, !llvm.loop !26

._crit_edge:                                      ; preds = %scalar.ph.prol.loopexit, %scalar.ph, %middle.block, %17
  %indvars.iv.next55 = add nuw nsw i64 %indvars.iv54, 1
  %exitcond58.not = icmp eq i64 %indvars.iv.next55, %wide.trip.count57
  br i1 %exitcond58.not, label %._crit_edge46, label %17, !llvm.loop !27

._crit_edge46:                                    ; preds = %._crit_edge, %.preheader38
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
!12 = distinct !{!12, !9, !11, !10}
!13 = distinct !{!13, !9, !10, !11}
!14 = distinct !{!14, !9, !11, !10}
!15 = distinct !{!15, !9}
!16 = !{!17}
!17 = distinct !{!17, !18}
!18 = distinct !{!18, !"LVerDomain"}
!19 = !{!20}
!20 = distinct !{!20, !18}
!21 = !{!22}
!22 = distinct !{!22, !18}
!23 = !{!20, !17}
!24 = distinct !{!24, !9, !10, !11}
!25 = distinct !{!25, !9}
!26 = distinct !{!26, !9, !10}
!27 = distinct !{!27, !9}
