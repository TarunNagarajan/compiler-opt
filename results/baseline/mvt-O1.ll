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
  %9 = sitofp i32 %0 to double
  %10 = zext nneg i32 %0 to i64
  %wide.trip.count45 = zext nneg i32 %0 to i64
  %11 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %11, 3
  %12 = icmp ult i32 %0, 4
  %unroll_iter = and i64 %11, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.lr.ph

.loopexit.unr-lcssa:                              ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %.loopexit, label %.epil.preheader

.epil.preheader:                                  ; preds = %.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %.loopexit.unr-lcssa ]
  %13 = mul nuw nsw i64 %indvars.iv.epil, %indvars.iv42
  %14 = trunc nuw i64 %13 to i32
  %15 = uitofp nneg i32 %14 to double
  %16 = fdiv double %15, %9
  %17 = getelementptr inbounds nuw double, ptr %41, i64 %indvars.iv.epil
  store double %16, ptr %17, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %.loopexit, label %.epil.preheader, !llvm.loop !8

.loopexit:                                        ; preds = %.epil.preheader, %.loopexit.unr-lcssa
  %exitcond46.not = icmp eq i64 %indvars.iv.next43, %wide.trip.count45
  br i1 %exitcond46.not, label %._crit_edge, label %.lr.ph, !llvm.loop !10

.lr.ph:                                           ; preds = %.lr.ph40, %.loopexit
  %indvars.iv42 = phi i64 [ 0, %.lr.ph40 ], [ %indvars.iv.next43, %.loopexit ]
  %18 = trunc nuw nsw i64 %indvars.iv42 to i32
  %19 = uitofp nneg i32 %18 to double
  %20 = fdiv double %19, %9
  %21 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv42
  store double %20, ptr %21, align 8
  %indvars.iv.next43 = add nuw nsw i64 %indvars.iv42, 1
  %22 = icmp eq i64 %indvars.iv.next43, %10
  %23 = trunc nuw nsw i64 %indvars.iv.next43 to i32
  %24 = uitofp nneg i32 %23 to double
  %25 = select i1 %22, double 0.000000e+00, double %24
  %26 = fdiv double %25, %9
  %27 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv42
  store double %26, ptr %27, align 8
  %28 = trunc i64 %indvars.iv42 to i32
  %29 = add i32 %28, 3
  %30 = urem i32 %29, %0
  %31 = uitofp nneg i32 %30 to double
  %32 = fdiv double %31, %9
  %33 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv42
  store double %32, ptr %33, align 8
  %34 = trunc i64 %indvars.iv42 to i32
  %35 = add i32 %34, 4
  %36 = urem i32 %35, %0
  %37 = uitofp nneg i32 %36 to double
  %38 = fdiv double %37, %9
  %39 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv42
  store double %38, ptr %39, align 8
  %40 = mul nuw nsw i64 %indvars.iv42, %7
  %41 = getelementptr inbounds nuw double, ptr %5, i64 %40
  br i1 %12, label %.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %42 = mul nuw nsw i64 %indvars.iv, %indvars.iv42
  %43 = trunc nuw i64 %42 to i32
  %44 = uitofp nneg i32 %43 to double
  %45 = fdiv double %44, %9
  %46 = getelementptr inbounds nuw double, ptr %41, i64 %indvars.iv
  store double %45, ptr %46, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %47 = mul nuw nsw i64 %indvars.iv.next, %indvars.iv42
  %48 = trunc nuw i64 %47 to i32
  %49 = uitofp nneg i32 %48 to double
  %50 = fdiv double %49, %9
  %51 = getelementptr inbounds nuw double, ptr %41, i64 %indvars.iv.next
  store double %50, ptr %51, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %52 = mul nuw nsw i64 %indvars.iv.next.1, %indvars.iv42
  %53 = trunc nuw i64 %52 to i32
  %54 = uitofp nneg i32 %53 to double
  %55 = fdiv double %54, %9
  %56 = getelementptr inbounds nuw double, ptr %41, i64 %indvars.iv.next.1
  store double %55, ptr %56, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %57 = mul nuw nsw i64 %indvars.iv.next.2, %indvars.iv42
  %58 = trunc nuw i64 %57 to i32
  %59 = uitofp nneg i32 %58 to double
  %60 = fdiv double %59, %9
  %61 = getelementptr inbounds nuw double, ptr %41, i64 %indvars.iv.next.2
  store double %60, ptr %61, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %.loopexit.unr-lcssa, label %.lr.ph.new, !llvm.loop !12

._crit_edge:                                      ; preds = %.loopexit, %6
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @mvt(i32 noundef %0, ptr noundef captures(none) %1, ptr noundef captures(none) %2, ptr noundef readonly captures(none) %3, ptr noundef readonly captures(none) %4, ptr noundef readonly captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %0 to i64
  %8 = icmp sgt i32 %0, 0
  br i1 %8, label %.preheader36.lr.ph, label %.preheader35

.preheader36.lr.ph:                               ; preds = %6
  %wide.trip.count49 = zext nneg i32 %0 to i64
  %9 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %9, 1
  %10 = icmp eq i32 %0, 1
  %unroll_iter = and i64 %9, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader36

.preheader36:                                     ; preds = %.preheader36.lr.ph, %._crit_edge
  %indvars.iv46 = phi i64 [ 0, %.preheader36.lr.ph ], [ %indvars.iv.next47, %._crit_edge ]
  %11 = mul nuw nsw i64 %indvars.iv46, %7
  %12 = getelementptr inbounds nuw double, ptr %5, i64 %11
  %13 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv46
  %.promoted = load double, ptr %13, align 8
  br i1 %10, label %._crit_edge.unr-lcssa, label %.preheader36.new

.preheader35:                                     ; preds = %._crit_edge, %6
  %14 = icmp sgt i32 %0, 0
  br i1 %14, label %.preheader.lr.ph, label %._crit_edge44

.preheader.lr.ph:                                 ; preds = %.preheader35
  %wide.trip.count59 = zext nneg i32 %0 to i64
  %xtraiter62 = and i64 %7, 1
  %15 = icmp eq i32 %0, 1
  %unroll_iter65 = and i64 %7, 2147483646
  %lcmp.mod64.not = icmp eq i64 %xtraiter62, 0
  br label %.preheader

.preheader36.new:                                 ; preds = %.preheader36, %.preheader36.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.preheader36.new ], [ 0, %.preheader36 ]
  %16 = phi double [ %26, %.preheader36.new ], [ %.promoted, %.preheader36 ]
  %niter = phi i64 [ %niter.next.1, %.preheader36.new ], [ 0, %.preheader36 ]
  %17 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv
  %18 = load double, ptr %17, align 8
  %19 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %20 = load double, ptr %19, align 8
  %21 = tail call double @llvm.fmuladd.f64(double %18, double %20, double %16)
  store double %21, ptr %13, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %22 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next
  %23 = load double, ptr %22, align 8
  %24 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  %25 = load double, ptr %24, align 8
  %26 = tail call double @llvm.fmuladd.f64(double %23, double %25, double %21)
  store double %26, ptr %13, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.unr-lcssa, label %.preheader36.new, !llvm.loop !13

._crit_edge.unr-lcssa:                            ; preds = %.preheader36.new, %.preheader36
  %indvars.iv.unr = phi i64 [ 0, %.preheader36 ], [ %indvars.iv.next.1, %.preheader36.new ]
  %.unr = phi double [ %.promoted, %.preheader36 ], [ %26, %.preheader36.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.epilog-lcssa

._crit_edge.epilog-lcssa:                         ; preds = %._crit_edge.unr-lcssa
  %27 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.unr
  %28 = load double, ptr %27, align 8
  %29 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  %30 = load double, ptr %29, align 8
  %31 = tail call double @llvm.fmuladd.f64(double %28, double %30, double %.unr)
  store double %31, ptr %13, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.unr-lcssa, %._crit_edge.epilog-lcssa
  %indvars.iv.next47 = add nuw nsw i64 %indvars.iv46, 1
  %exitcond50.not = icmp eq i64 %indvars.iv.next47, %wide.trip.count49
  br i1 %exitcond50.not, label %.preheader35, label %.preheader36, !llvm.loop !14

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge41
  %indvars.iv56 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next57, %._crit_edge41 ]
  %invariant.gep = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv56
  %32 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv56
  %.promoted42 = load double, ptr %32, align 8
  br i1 %15, label %._crit_edge41.unr-lcssa, label %.preheader.new

.preheader.new:                                   ; preds = %.preheader, %.preheader.new
  %indvars.iv51 = phi i64 [ %indvars.iv.next52.1, %.preheader.new ], [ 0, %.preheader ]
  %33 = phi double [ %43, %.preheader.new ], [ %.promoted42, %.preheader ]
  %niter66 = phi i64 [ %niter66.next.1, %.preheader.new ], [ 0, %.preheader ]
  %34 = mul nuw nsw i64 %indvars.iv51, %7
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %34
  %35 = load double, ptr %gep, align 8
  %36 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv51
  %37 = load double, ptr %36, align 8
  %38 = tail call double @llvm.fmuladd.f64(double %35, double %37, double %33)
  store double %38, ptr %32, align 8
  %indvars.iv.next52 = or disjoint i64 %indvars.iv51, 1
  %39 = mul nuw nsw i64 %indvars.iv.next52, %7
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %39
  %40 = load double, ptr %gep.1, align 8
  %41 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next52
  %42 = load double, ptr %41, align 8
  %43 = tail call double @llvm.fmuladd.f64(double %40, double %42, double %38)
  store double %43, ptr %32, align 8
  %indvars.iv.next52.1 = add nuw nsw i64 %indvars.iv51, 2
  %niter66.next.1 = add i64 %niter66, 2
  %niter66.ncmp.1 = icmp eq i64 %niter66.next.1, %unroll_iter65
  br i1 %niter66.ncmp.1, label %._crit_edge41.unr-lcssa, label %.preheader.new, !llvm.loop !15

._crit_edge41.unr-lcssa:                          ; preds = %.preheader.new, %.preheader
  %indvars.iv51.unr = phi i64 [ 0, %.preheader ], [ %indvars.iv.next52.1, %.preheader.new ]
  %.unr63 = phi double [ %.promoted42, %.preheader ], [ %43, %.preheader.new ]
  br i1 %lcmp.mod64.not, label %._crit_edge41, label %._crit_edge41.epilog-lcssa

._crit_edge41.epilog-lcssa:                       ; preds = %._crit_edge41.unr-lcssa
  %44 = mul nuw nsw i64 %indvars.iv51.unr, %7
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %44
  %45 = load double, ptr %gep.epil, align 8
  %46 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv51.unr
  %47 = load double, ptr %46, align 8
  %48 = tail call double @llvm.fmuladd.f64(double %45, double %47, double %.unr63)
  store double %48, ptr %32, align 8
  br label %._crit_edge41

._crit_edge41:                                    ; preds = %._crit_edge41.unr-lcssa, %._crit_edge41.epilog-lcssa
  %indvars.iv.next57 = add nuw nsw i64 %indvars.iv56, 1
  %exitcond60.not = icmp eq i64 %indvars.iv.next57, %wide.trip.count59
  br i1 %exitcond60.not, label %._crit_edge44, label %.preheader, !llvm.loop !16

._crit_edge44:                                    ; preds = %._crit_edge41, %.preheader35
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
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.unroll.disable"}
!10 = distinct !{!10, !11}
!11 = !{!"llvm.loop.mustprogress"}
!12 = distinct !{!12, !11}
!13 = distinct !{!13, !11}
!14 = distinct !{!14, !11}
!15 = distinct !{!15, !11}
!16 = distinct !{!16, !11}
