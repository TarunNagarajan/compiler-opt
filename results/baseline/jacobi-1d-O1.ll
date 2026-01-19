; ModuleID = 'results\baseline\jacobi-1d_base.ll'
source_filename = "benchmarks\\jacobi-1d.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [32 x i8] c"Jacobi-1D Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef writeonly captures(none) %1, ptr noundef writeonly captures(none) %2) local_unnamed_addr #0 {
  %4 = icmp sgt i32 %0, 0
  br i1 %4, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %3
  %5 = sitofp i32 %0 to double
  %wide.trip.count = zext nneg i32 %0 to i64
  %xtraiter = and i64 %wide.trip.count, 1
  %6 = icmp eq i32 %0, 1
  br i1 %6, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph
  %unroll_iter = and i64 %wide.trip.count, 2147483646
  br label %7

7:                                                ; preds = %7, %.lr.ph.new
  %indvars.iv = phi i64 [ 0, %.lr.ph.new ], [ %indvars.iv.next.1, %7 ]
  %niter = phi i64 [ 0, %.lr.ph.new ], [ %niter.next.1, %7 ]
  %8 = trunc i64 %indvars.iv to i32
  %9 = add i32 %8, 2
  %10 = uitofp i32 %9 to double
  %11 = fdiv double %10, %5
  %12 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv
  store double %11, ptr %12, align 8
  %13 = trunc i64 %indvars.iv to i32
  %14 = add i32 %13, 3
  %15 = uitofp i32 %14 to double
  %16 = fdiv double %15, %5
  %17 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv
  store double %16, ptr %17, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %18 = trunc i64 %indvars.iv.next to i32
  %19 = add i32 %18, 2
  %20 = uitofp i32 %19 to double
  %21 = fdiv double %20, %5
  %22 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv.next
  store double %21, ptr %22, align 8
  %23 = trunc i64 %indvars.iv.next to i32
  %24 = add i32 %23, 3
  %25 = uitofp i32 %24 to double
  %26 = fdiv double %25, %5
  %27 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next
  store double %26, ptr %27, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %7, !llvm.loop !8

._crit_edge.loopexit.unr-lcssa:                   ; preds = %7, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %7 ]
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.loopexit.epilog-lcssa

._crit_edge.loopexit.epilog-lcssa:                ; preds = %._crit_edge.loopexit.unr-lcssa
  %28 = trunc i64 %indvars.iv.unr to i32
  %29 = add i32 %28, 2
  %30 = uitofp i32 %29 to double
  %31 = fdiv double %30, %5
  %32 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv.unr
  store double %31, ptr %32, align 8
  %33 = trunc i64 %indvars.iv.unr to i32
  %34 = add i32 %33, 3
  %35 = uitofp i32 %34 to double
  %36 = fdiv double %35, %5
  %37 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.unr
  store double %36, ptr %37, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.loopexit.epilog-lcssa, %._crit_edge.loopexit.unr-lcssa, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @jacobi_1d(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3) local_unnamed_addr #1 {
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader29.lr.ph, label %._crit_edge34

.preheader29.lr.ph:                               ; preds = %4
  %6 = add i32 %1, -1
  %7 = icmp sgt i32 %1, 2
  %8 = icmp sgt i32 %1, 2
  %9 = zext i32 %6 to i64
  %10 = add nsw i64 %9, -1
  %11 = add nsw i64 %9, -2
  %xtraiter = and i64 %10, 1
  %12 = icmp eq i64 %11, 0
  %unroll_iter = and i64 %10, -2
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %invariant.gep = getelementptr i8, ptr %2, i64 8
  %xtraiter42 = and i64 %10, 1
  %13 = icmp eq i64 %11, 0
  %unroll_iter44 = and i64 %10, -2
  %lcmp.mod43.not = icmp eq i64 %xtraiter42, 0
  %invariant.gep46 = getelementptr i8, ptr %3, i64 8
  br label %.preheader29

.preheader29:                                     ; preds = %.preheader29.lr.ph, %._crit_edge
  %.02733 = phi i32 [ 0, %.preheader29.lr.ph ], [ %72, %._crit_edge ]
  br i1 %7, label %.lr.ph.preheader, label %.preheader

.lr.ph.preheader:                                 ; preds = %.preheader29
  br i1 %12, label %.preheader.loopexit.unr-lcssa, label %.lr.ph

.preheader.loopexit.unr-lcssa:                    ; preds = %.lr.ph, %.lr.ph.preheader
  %indvars.iv.unr = phi i64 [ 1, %.lr.ph.preheader ], [ %indvars.iv.next.1, %.lr.ph ]
  br i1 %lcmp.mod.not, label %.preheader, label %.lr.ph.epil

.lr.ph.epil:                                      ; preds = %.preheader.loopexit.unr-lcssa
  %14 = getelementptr double, ptr %2, i64 %indvars.iv.unr
  %15 = getelementptr i8, ptr %14, i64 -8
  %16 = load double, ptr %15, align 8
  %17 = load double, ptr %14, align 8
  %18 = fadd double %16, %17
  %gep = getelementptr double, ptr %invariant.gep, i64 %indvars.iv.unr
  %19 = load double, ptr %gep, align 8
  %20 = fadd double %18, %19
  %21 = fmul double %20, 3.333300e-01
  %22 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  store double %21, ptr %22, align 8
  br label %.preheader

.preheader:                                       ; preds = %.lr.ph.epil, %.preheader.loopexit.unr-lcssa, %.preheader29
  br i1 %8, label %.lr.ph32.preheader, label %._crit_edge

.lr.ph32.preheader:                               ; preds = %.preheader
  br i1 %13, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph32

.lr.ph:                                           ; preds = %.lr.ph.preheader, %.lr.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph ], [ 1, %.lr.ph.preheader ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph ], [ 0, %.lr.ph.preheader ]
  %23 = getelementptr double, ptr %2, i64 %indvars.iv
  %24 = getelementptr i8, ptr %23, i64 -8
  %25 = load double, ptr %24, align 8
  %26 = load double, ptr %23, align 8
  %27 = fadd double %25, %26
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %28 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next
  %29 = load double, ptr %28, align 8
  %30 = fadd double %27, %29
  %31 = fmul double %30, 3.333300e-01
  %32 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %31, ptr %32, align 8
  %33 = getelementptr double, ptr %2, i64 %indvars.iv.next
  %34 = getelementptr i8, ptr %33, i64 -8
  %35 = load double, ptr %34, align 8
  %36 = load double, ptr %33, align 8
  %37 = fadd double %35, %36
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %38 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next.1
  %39 = load double, ptr %38, align 8
  %40 = fadd double %37, %39
  %41 = fmul double %40, 3.333300e-01
  %42 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  store double %41, ptr %42, align 8
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %.preheader.loopexit.unr-lcssa, label %.lr.ph, !llvm.loop !10

.lr.ph32:                                         ; preds = %.lr.ph32.preheader, %.lr.ph32
  %indvars.iv36 = phi i64 [ %indvars.iv.next37.1, %.lr.ph32 ], [ 1, %.lr.ph32.preheader ]
  %niter45 = phi i64 [ %niter45.next.1, %.lr.ph32 ], [ 0, %.lr.ph32.preheader ]
  %43 = getelementptr double, ptr %3, i64 %indvars.iv36
  %44 = getelementptr i8, ptr %43, i64 -8
  %45 = load double, ptr %44, align 8
  %46 = load double, ptr %43, align 8
  %47 = fadd double %45, %46
  %indvars.iv.next37 = add nuw nsw i64 %indvars.iv36, 1
  %48 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next37
  %49 = load double, ptr %48, align 8
  %50 = fadd double %47, %49
  %51 = fmul double %50, 3.333300e-01
  %52 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv36
  store double %51, ptr %52, align 8
  %53 = getelementptr double, ptr %3, i64 %indvars.iv.next37
  %54 = getelementptr i8, ptr %53, i64 -8
  %55 = load double, ptr %54, align 8
  %56 = load double, ptr %53, align 8
  %57 = fadd double %55, %56
  %indvars.iv.next37.1 = add nuw nsw i64 %indvars.iv36, 2
  %58 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next37.1
  %59 = load double, ptr %58, align 8
  %60 = fadd double %57, %59
  %61 = fmul double %60, 3.333300e-01
  %62 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next37
  store double %61, ptr %62, align 8
  %niter45.next.1 = add i64 %niter45, 2
  %niter45.ncmp.1 = icmp eq i64 %niter45.next.1, %unroll_iter44
  br i1 %niter45.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph32, !llvm.loop !11

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph32, %.lr.ph32.preheader
  %indvars.iv36.unr = phi i64 [ 1, %.lr.ph32.preheader ], [ %indvars.iv.next37.1, %.lr.ph32 ]
  br i1 %lcmp.mod43.not, label %._crit_edge, label %.lr.ph32.epil

.lr.ph32.epil:                                    ; preds = %._crit_edge.loopexit.unr-lcssa
  %63 = getelementptr double, ptr %3, i64 %indvars.iv36.unr
  %64 = getelementptr i8, ptr %63, i64 -8
  %65 = load double, ptr %64, align 8
  %66 = load double, ptr %63, align 8
  %67 = fadd double %65, %66
  %gep47 = getelementptr double, ptr %invariant.gep46, i64 %indvars.iv36.unr
  %68 = load double, ptr %gep47, align 8
  %69 = fadd double %67, %68
  %70 = fmul double %69, 3.333300e-01
  %71 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv36.unr
  store double %70, ptr %71, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %.lr.ph32.epil, %._crit_edge.loopexit.unr-lcssa, %.preheader
  %72 = add nuw nsw i32 %.02733, 1
  %exitcond41.not = icmp eq i32 %72, %0
  br i1 %exitcond41.not, label %._crit_edge34, label %.preheader29, !llvm.loop !12

._crit_edge34:                                    ; preds = %._crit_edge, %4
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main(i32 noundef %0, ptr noundef readnone captures(none) %1) local_unnamed_addr #2 {
  %3 = tail call dereferenceable_or_null(16000) ptr @malloc(i64 noundef 16000) #6
  %4 = tail call dereferenceable_or_null(16000) ptr @malloc(i64 noundef 16000) #6
  tail call void @init_array(i32 noundef 2000, ptr noundef %3, ptr noundef %4)
  %5 = tail call i32 @clock() #7
  tail call void @jacobi_1d(i32 noundef 100, i32 noundef 2000, ptr noundef %3, ptr noundef %4)
  %6 = tail call i32 @clock() #7
  %7 = sub nsw i32 %6, %5
  %8 = sitofp i32 %7 to double
  %9 = fdiv double %8, 1.000000e+03
  %10 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %9) #7
  %11 = load double, ptr %3, align 8
  %12 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %11) #7
  tail call void @free(ptr noundef %3)
  tail call void @free(ptr noundef %4)
  ret i32 0
}

; Function Attrs: mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite)
declare dso_local noalias noundef ptr @malloc(i64 noundef) local_unnamed_addr #3

declare dso_local i32 @clock() local_unnamed_addr #4

declare dso_local i32 @__mingw_printf(ptr noundef, ...) local_unnamed_addr #4

; Function Attrs: mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite)
declare dso_local void @free(ptr allocptr noundef captures(none)) local_unnamed_addr #5

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { allocsize(0) }
attributes #7 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/jacobi-1d.c", directory: "C:/Users/ultim/compiler-opt")
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
