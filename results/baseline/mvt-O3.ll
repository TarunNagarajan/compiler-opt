; ModuleID = 'results\baseline\mvt_base.ll'
source_filename = "benchmarks\\mvt.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [26 x i8] c"MVT Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef writeonly captures(none) %1, ptr noundef writeonly captures(none) %2, ptr noundef writeonly captures(none) %3, ptr noundef writeonly captures(none) %4, ptr noundef writeonly captures(none) %5) local_unnamed_addr #0 {
  %7 = zext i32 %0 to i64
  %8 = icmp sgt i32 %0, 0
  br i1 %8, label %.lr.ph40, label %._crit_edge

.lr.ph40:                                         ; preds = %6
  %9 = uitofp nneg i32 %0 to double
  %min.iters.check = icmp eq i32 %0, 1
  %n.vec = and i64 %7, 2147483646
  %broadcast.splatinsert47 = insertelement <2 x double> poison, double %9, i64 0
  %broadcast.splat48 = shufflevector <2 x double> %broadcast.splatinsert47, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n = icmp eq i64 %n.vec, %7
  br label %.lr.ph.us

.lr.ph.us:                                        ; preds = %..loopexit_crit_edge.us, %.lr.ph40
  %indvars.iv42 = phi i64 [ %indvars.iv.next43, %..loopexit_crit_edge.us ], [ 0, %.lr.ph40 ]
  %10 = trunc nuw nsw i64 %indvars.iv42 to i32
  %11 = uitofp nneg i32 %10 to double
  %12 = fdiv double %11, %9
  %13 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv42
  store double %12, ptr %13, align 8
  %indvars.iv.next43 = add nuw nsw i64 %indvars.iv42, 1
  %14 = icmp eq i64 %indvars.iv.next43, %7
  %15 = trunc nuw nsw i64 %indvars.iv.next43 to i32
  %16 = uitofp nneg i32 %15 to double
  %17 = select i1 %14, double 0.000000e+00, double %16
  %18 = fdiv double %17, %9
  %19 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv42
  store double %18, ptr %19, align 8
  %20 = trunc i64 %indvars.iv42 to i32
  %21 = add i32 %20, 3
  %22 = urem i32 %21, %0
  %23 = uitofp nneg i32 %22 to double
  %24 = fdiv double %23, %9
  %25 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv42
  store double %24, ptr %25, align 8
  %26 = trunc i64 %indvars.iv42 to i32
  %27 = add i32 %26, 4
  %28 = urem i32 %27, %0
  %29 = uitofp nneg i32 %28 to double
  %30 = fdiv double %29, %9
  %31 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv42
  store double %30, ptr %31, align 8
  %32 = mul nuw nsw i64 %indvars.iv42, %7
  %33 = getelementptr inbounds nuw double, ptr %5, i64 %32
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph.us
  %broadcast.splatinsert = insertelement <2 x i64> poison, i64 %indvars.iv42, i64 0
  %broadcast.splat = shufflevector <2 x i64> %broadcast.splatinsert, <2 x i64> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i64> [ <i64 0, i64 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %34 = mul nuw nsw <2 x i64> %vec.ind, %broadcast.splat
  %35 = trunc nuw <2 x i64> %34 to <2 x i32>
  %36 = uitofp nneg <2 x i32> %35 to <2 x double>
  %37 = fdiv <2 x double> %36, %broadcast.splat48
  %38 = getelementptr inbounds nuw double, ptr %33, i64 %index
  store <2 x double> %37, ptr %38, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i64> %vec.ind, splat (i64 2)
  %39 = icmp eq i64 %index.next, %n.vec
  br i1 %39, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %..loopexit_crit_edge.us, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph.us, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph.us ], [ %n.vec, %middle.block ]
  br label %scalar.ph

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %40 = mul nuw nsw i64 %indvars.iv, %indvars.iv42
  %41 = trunc nuw i64 %40 to i32
  %42 = uitofp nneg i32 %41 to double
  %43 = fdiv double %42, %9
  %44 = getelementptr inbounds nuw double, ptr %33, i64 %indvars.iv
  store double %43, ptr %44, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %7
  br i1 %exitcond.not, label %..loopexit_crit_edge.us, label %scalar.ph, !llvm.loop !12

..loopexit_crit_edge.us:                          ; preds = %scalar.ph, %middle.block
  %exitcond46.not = icmp eq i64 %indvars.iv.next43, %7
  br i1 %exitcond46.not, label %._crit_edge, label %.lr.ph.us, !llvm.loop !13

._crit_edge:                                      ; preds = %..loopexit_crit_edge.us, %6
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @mvt(i32 noundef %0, ptr noundef captures(none) %1, ptr noundef captures(none) %2, ptr noundef readonly captures(none) %3, ptr noundef readonly captures(none) %4, ptr noundef readonly captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %0 to i64
  %8 = icmp sgt i32 %0, 0
  br i1 %8, label %.preheader36.us.preheader, label %._crit_edge41

.preheader36.us.preheader:                        ; preds = %6
  %9 = add nsw i64 %7, -1
  %xtraiter = and i64 %7, 1
  %10 = icmp eq i64 %9, 0
  %unroll_iter = and i64 %7, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader36.us

.preheader36.us:                                  ; preds = %.preheader36.us.preheader, %._crit_edge.us
  %indvars.iv45 = phi i64 [ %indvars.iv.next46, %._crit_edge.us ], [ 0, %.preheader36.us.preheader ]
  %11 = mul nuw nsw i64 %indvars.iv45, %7
  %12 = getelementptr inbounds nuw double, ptr %5, i64 %11
  %13 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv45
  %.promoted.us = load double, ptr %13, align 8
  br i1 %10, label %._crit_edge.us.unr-lcssa, label %.preheader36.us.new

.preheader36.us.new:                              ; preds = %.preheader36.us, %.preheader36.us.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.preheader36.us.new ], [ 0, %.preheader36.us ]
  %14 = phi double [ %24, %.preheader36.us.new ], [ %.promoted.us, %.preheader36.us ]
  %niter = phi i64 [ %niter.next.1, %.preheader36.us.new ], [ 0, %.preheader36.us ]
  %15 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv
  %16 = load double, ptr %15, align 8
  %17 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %18 = load double, ptr %17, align 8
  %19 = tail call double @llvm.fmuladd.f64(double %16, double %18, double %14)
  store double %19, ptr %13, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %20 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next
  %21 = load double, ptr %20, align 8
  %22 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  %23 = load double, ptr %22, align 8
  %24 = tail call double @llvm.fmuladd.f64(double %21, double %23, double %19)
  store double %24, ptr %13, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.us.unr-lcssa, label %.preheader36.us.new, !llvm.loop !14

._crit_edge.us.unr-lcssa:                         ; preds = %.preheader36.us.new, %.preheader36.us
  %indvars.iv.unr = phi i64 [ 0, %.preheader36.us ], [ %indvars.iv.next.1, %.preheader36.us.new ]
  %.unr = phi double [ %.promoted.us, %.preheader36.us ], [ %24, %.preheader36.us.new ]
  br i1 %lcmp.mod.not, label %._crit_edge.us, label %._crit_edge.us.epilog-lcssa

._crit_edge.us.epilog-lcssa:                      ; preds = %._crit_edge.us.unr-lcssa
  %25 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.unr
  %26 = load double, ptr %25, align 8
  %27 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  %28 = load double, ptr %27, align 8
  %29 = tail call double @llvm.fmuladd.f64(double %26, double %28, double %.unr)
  store double %29, ptr %13, align 8
  br label %._crit_edge.us

._crit_edge.us:                                   ; preds = %._crit_edge.us.unr-lcssa, %._crit_edge.us.epilog-lcssa
  %indvars.iv.next46 = add nuw nsw i64 %indvars.iv45, 1
  %exitcond49.not = icmp eq i64 %indvars.iv.next46, %7
  br i1 %exitcond49.not, label %.preheader.us.preheader, label %.preheader36.us, !llvm.loop !15

.preheader.us.preheader:                          ; preds = %._crit_edge.us
  %xtraiter61 = and i64 %7, 1
  %30 = icmp eq i64 %9, 0
  %unroll_iter64 = and i64 %7, 2147483646
  %lcmp.mod63.not = icmp eq i64 %xtraiter61, 0
  br label %.preheader.us

.preheader.us:                                    ; preds = %.preheader.us.preheader, %._crit_edge.us43
  %indvars.iv55 = phi i64 [ %indvars.iv.next56, %._crit_edge.us43 ], [ 0, %.preheader.us.preheader ]
  %invariant.gep.us = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv55
  %31 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv55
  %.promoted.us42 = load double, ptr %31, align 8
  br i1 %30, label %._crit_edge.us43.unr-lcssa, label %.preheader.us.new

.preheader.us.new:                                ; preds = %.preheader.us, %.preheader.us.new
  %indvars.iv50 = phi i64 [ %indvars.iv.next51.1, %.preheader.us.new ], [ 0, %.preheader.us ]
  %32 = phi double [ %42, %.preheader.us.new ], [ %.promoted.us42, %.preheader.us ]
  %niter65 = phi i64 [ %niter65.next.1, %.preheader.us.new ], [ 0, %.preheader.us ]
  %33 = mul nuw nsw i64 %indvars.iv50, %7
  %gep.us = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %33
  %34 = load double, ptr %gep.us, align 8
  %35 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv50
  %36 = load double, ptr %35, align 8
  %37 = tail call double @llvm.fmuladd.f64(double %34, double %36, double %32)
  store double %37, ptr %31, align 8
  %indvars.iv.next51 = or disjoint i64 %indvars.iv50, 1
  %38 = mul nuw nsw i64 %indvars.iv.next51, %7
  %gep.us.1 = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %38
  %39 = load double, ptr %gep.us.1, align 8
  %40 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next51
  %41 = load double, ptr %40, align 8
  %42 = tail call double @llvm.fmuladd.f64(double %39, double %41, double %37)
  store double %42, ptr %31, align 8
  %indvars.iv.next51.1 = add nuw nsw i64 %indvars.iv50, 2
  %niter65.next.1 = add i64 %niter65, 2
  %niter65.ncmp.1 = icmp eq i64 %niter65.next.1, %unroll_iter64
  br i1 %niter65.ncmp.1, label %._crit_edge.us43.unr-lcssa, label %.preheader.us.new, !llvm.loop !16

._crit_edge.us43.unr-lcssa:                       ; preds = %.preheader.us.new, %.preheader.us
  %indvars.iv50.unr = phi i64 [ 0, %.preheader.us ], [ %indvars.iv.next51.1, %.preheader.us.new ]
  %.unr62 = phi double [ %.promoted.us42, %.preheader.us ], [ %42, %.preheader.us.new ]
  br i1 %lcmp.mod63.not, label %._crit_edge.us43, label %._crit_edge.us43.epilog-lcssa

._crit_edge.us43.epilog-lcssa:                    ; preds = %._crit_edge.us43.unr-lcssa
  %43 = mul nuw nsw i64 %indvars.iv50.unr, %7
  %gep.us.epil = getelementptr inbounds nuw double, ptr %invariant.gep.us, i64 %43
  %44 = load double, ptr %gep.us.epil, align 8
  %45 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv50.unr
  %46 = load double, ptr %45, align 8
  %47 = tail call double @llvm.fmuladd.f64(double %44, double %46, double %.unr62)
  store double %47, ptr %31, align 8
  br label %._crit_edge.us43

._crit_edge.us43:                                 ; preds = %._crit_edge.us43.unr-lcssa, %._crit_edge.us43.epilog-lcssa
  %indvars.iv.next56 = add nuw nsw i64 %indvars.iv55, 1
  %exitcond59.not = icmp eq i64 %indvars.iv.next56, %7
  br i1 %exitcond59.not, label %._crit_edge41, label %.preheader.us, !llvm.loop !17

._crit_edge41:                                    ; preds = %._crit_edge.us43, %6
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #3 {
  %1 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #7
  %2 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #7
  %3 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #7
  %4 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #7
  %5 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #7
  tail call void @init_array(i32 noundef 512, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5)
  %6 = tail call i32 @clock() #8
  tail call void @mvt(i32 noundef 512, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5)
  %7 = tail call i32 @clock() #8
  %8 = sub nsw i32 %7, %6
  %9 = sitofp i32 %8 to double
  %10 = fdiv double %9, 1.000000e+03
  %11 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %10) #8
  %12 = load double, ptr %1, align 8
  %13 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %12) #8
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  tail call void @free(ptr noundef %4)
  tail call void @free(ptr noundef %5)
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
!1 = !DIFile(filename: "benchmarks/mvt.c", directory: "C:/Users/ultim/compiler-opt")
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
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !9}
!17 = distinct !{!17, !9}
