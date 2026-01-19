; ModuleID = 'results\baseline\gemm_base.ll'
source_filename = "benchmarks\\gemm.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"GEMM Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, ptr noundef writeonly captures(none) %1, ptr noundef writeonly captures(none) %2) local_unnamed_addr #0 {
  %4 = zext i32 %0 to i64
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader.lr.ph, label %._crit_edge25

.preheader.lr.ph:                                 ; preds = %3
  %6 = sitofp i32 %0 to double
  %wide.trip.count30 = zext nneg i32 %0 to i64
  %7 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %7, 1
  %8 = icmp eq i32 %0, 1
  %unroll_iter = and i64 %7, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv27 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next28, %._crit_edge ]
  %9 = trunc nuw nsw i64 %indvars.iv27 to i32
  %10 = uitofp nneg i32 %9 to double
  %11 = mul nuw nsw i64 %indvars.iv27, %4
  %12 = getelementptr inbounds nuw double, ptr %1, i64 %11
  %13 = getelementptr inbounds nuw double, ptr %2, i64 %11
  br i1 %8, label %._crit_edge.unr-lcssa, label %.preheader.new

.preheader.new:                                   ; preds = %.preheader, %.preheader.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.preheader.new ], [ 0, %.preheader ]
  %niter = phi i64 [ %niter.next.1, %.preheader.new ], [ 0, %.preheader ]
  %14 = trunc nuw nsw i64 %indvars.iv to i32
  %15 = uitofp nneg i32 %14 to double
  %16 = fmul double %10, %15
  %17 = fdiv double %16, %6
  %18 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv
  store double %17, ptr %18, align 8
  %19 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv
  store double %17, ptr %19, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %20 = trunc nuw nsw i64 %indvars.iv.next to i32
  %21 = uitofp nneg i32 %20 to double
  %22 = fmul double %10, %21
  %23 = fdiv double %22, %6
  %24 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next
  store double %23, ptr %24, align 8
  %25 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.next
  store double %23, ptr %25, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.unr-lcssa, label %.preheader.new, !llvm.loop !8

._crit_edge.unr-lcssa:                            ; preds = %.preheader.new, %.preheader
  %indvars.iv.unr = phi i64 [ 0, %.preheader ], [ %indvars.iv.next.1, %.preheader.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.epilog-lcssa

._crit_edge.epilog-lcssa:                         ; preds = %._crit_edge.unr-lcssa
  %26 = trunc nuw nsw i64 %indvars.iv.unr to i32
  %27 = uitofp nneg i32 %26 to double
  %28 = fmul double %10, %27
  %29 = fdiv double %28, %6
  %30 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.unr
  store double %29, ptr %30, align 8
  %31 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.unr
  store double %29, ptr %31, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.unr-lcssa, %._crit_edge.epilog-lcssa
  %indvars.iv.next28 = add nuw nsw i64 %indvars.iv27, 1
  %exitcond31.not = icmp eq i64 %indvars.iv.next28, %wide.trip.count30
  br i1 %exitcond31.not, label %._crit_edge25, label %.preheader, !llvm.loop !10

._crit_edge25:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @gemm(i32 noundef %0, double noundef %1, double noundef %2, ptr noundef captures(none) %3, ptr noundef readonly captures(none) %4, ptr noundef readonly captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %0 to i64
  %8 = icmp sgt i32 %0, 0
  br i1 %8, label %.preheader.lr.ph, label %._crit_edge36

.preheader.lr.ph:                                 ; preds = %6
  %wide.trip.count46 = zext nneg i32 %0 to i64
  %9 = zext nneg i32 %0 to i64
  %wide.trip.count41 = zext nneg i32 %0 to i64
  %xtraiter = and i64 %9, 1
  %10 = icmp eq i32 %0, 1
  %unroll_iter = and i64 %9, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge34
  %indvars.iv43 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next44, %._crit_edge34 ]
  %11 = mul nuw nsw i64 %indvars.iv43, %7
  %12 = getelementptr inbounds nuw double, ptr %3, i64 %11
  %13 = getelementptr inbounds nuw double, ptr %4, i64 %11
  br label %.lr.ph

.lr.ph:                                           ; preds = %.preheader, %._crit_edge
  %indvars.iv38 = phi i64 [ 0, %.preheader ], [ %indvars.iv.next39, %._crit_edge ]
  %14 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv38
  %15 = load double, ptr %14, align 8
  %16 = fmul double %2, %15
  store double %16, ptr %14, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv38
  br i1 %10, label %._crit_edge.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %17 = phi double [ %29, %.lr.ph.new ], [ %16, %.lr.ph ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %18 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv
  %19 = load double, ptr %18, align 8
  %20 = fmul double %1, %19
  %21 = mul nuw nsw i64 %indvars.iv, %7
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %21
  %22 = load double, ptr %gep, align 8
  %23 = tail call double @llvm.fmuladd.f64(double %20, double %22, double %17)
  store double %23, ptr %14, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %24 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.next
  %25 = load double, ptr %24, align 8
  %26 = fmul double %1, %25
  %27 = mul nuw nsw i64 %indvars.iv.next, %7
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %27
  %28 = load double, ptr %gep.1, align 8
  %29 = tail call double @llvm.fmuladd.f64(double %26, double %28, double %23)
  store double %29, ptr %14, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.unr-lcssa, label %.lr.ph.new, !llvm.loop !11

._crit_edge.unr-lcssa:                            ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %.lr.ph.new ]
  %.unr = phi double [ %16, %.lr.ph ], [ %29, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.epilog-lcssa

._crit_edge.epilog-lcssa:                         ; preds = %._crit_edge.unr-lcssa
  %30 = getelementptr inbounds nuw double, ptr %13, i64 %indvars.iv.unr
  %31 = load double, ptr %30, align 8
  %32 = fmul double %1, %31
  %33 = mul nuw nsw i64 %indvars.iv.unr, %7
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %33
  %34 = load double, ptr %gep.epil, align 8
  %35 = tail call double @llvm.fmuladd.f64(double %32, double %34, double %.unr)
  store double %35, ptr %14, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.unr-lcssa, %._crit_edge.epilog-lcssa
  %indvars.iv.next39 = add nuw nsw i64 %indvars.iv38, 1
  %exitcond42.not = icmp eq i64 %indvars.iv.next39, %wide.trip.count41
  br i1 %exitcond42.not, label %._crit_edge34, label %.lr.ph, !llvm.loop !12

._crit_edge34:                                    ; preds = %._crit_edge
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  %exitcond47.not = icmp eq i64 %indvars.iv.next44, %wide.trip.count46
  br i1 %exitcond47.not, label %._crit_edge36, label %.preheader, !llvm.loop !13

._crit_edge36:                                    ; preds = %._crit_edge34, %6
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main(i32 noundef %0, ptr noundef readnone captures(none) %1) local_unnamed_addr #3 {
  %3 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #7
  %4 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #7
  %5 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #7
  tail call void @init_array(i32 noundef 512, ptr noundef %3, ptr noundef %4)
  %6 = tail call i32 @clock() #8
  tail call void @gemm(i32 noundef 512, double noundef 1.500000e+00, double noundef 1.200000e+00, ptr noundef %5, ptr noundef %3, ptr noundef %4)
  %7 = tail call i32 @clock() #8
  %8 = sub nsw i32 %7, %6
  %9 = sitofp i32 %8 to double
  %10 = fdiv double %9, 1.000000e+03
  %11 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %10) #8
  %12 = load double, ptr %5, align 8
  %13 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %12) #8
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
!1 = !DIFile(filename: "benchmarks/gemm.c", directory: "C:/Users/ultim/compiler-opt")
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
