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
  %6 = ptrtoint ptr %2 to i64
  %7 = ptrtoint ptr %1 to i64
  %8 = uitofp nneg i32 %0 to double
  %9 = sub i64 %6, %7
  %min.iters.check = icmp eq i32 %0, 1
  %diff.check = icmp ult i64 %9, 16
  %or.cond = or i1 %min.iters.check, %diff.check
  %n.vec = and i64 %4, 2147483646
  %broadcast.splatinsert32 = insertelement <2 x double> poison, double %8, i64 0
  %broadcast.splat33 = shufflevector <2 x double> %broadcast.splatinsert32, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n = icmp eq i64 %n.vec, %4
  %xtraiter = and i64 %4, 1
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %10 = add nsw i64 %4, -1
  br label %.lr.ph

.lr.ph:                                           ; preds = %._crit_edge, %.preheader.lr.ph
  %indvars.iv27 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next28, %._crit_edge ]
  %11 = trunc nuw nsw i64 %indvars.iv27 to i32
  %12 = uitofp nneg i32 %11 to double
  %13 = mul nuw nsw i64 %indvars.iv27, %4
  %14 = getelementptr inbounds nuw double, ptr %1, i64 %13
  %15 = getelementptr inbounds nuw double, ptr %2, i64 %13
  br i1 %or.cond, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %broadcast.splatinsert = insertelement <2 x double> poison, double %12, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %16 = uitofp nneg <2 x i32> %vec.ind to <2 x double>
  %17 = fmul <2 x double> %broadcast.splat, %16
  %18 = fdiv <2 x double> %17, %broadcast.splat33
  %19 = getelementptr inbounds nuw double, ptr %14, i64 %index
  store <2 x double> %18, ptr %19, align 8
  %20 = getelementptr inbounds nuw double, ptr %15, i64 %index
  store <2 x double> %18, ptr %20, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %21 = icmp eq i64 %index.next, %n.vec
  br i1 %21, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  br i1 %lcmp.mod.not, label %scalar.ph.prol.loopexit, label %scalar.ph.prol

scalar.ph.prol:                                   ; preds = %scalar.ph.preheader
  %22 = trunc nuw nsw i64 %indvars.iv.ph to i32
  %23 = uitofp nneg i32 %22 to double
  %24 = fmul double %12, %23
  %25 = fdiv double %24, %8
  %26 = getelementptr inbounds nuw double, ptr %14, i64 %indvars.iv.ph
  store double %25, ptr %26, align 8
  %27 = getelementptr inbounds nuw double, ptr %15, i64 %indvars.iv.ph
  store double %25, ptr %27, align 8
  %indvars.iv.next.prol = or disjoint i64 %indvars.iv.ph, 1
  br label %scalar.ph.prol.loopexit

scalar.ph.prol.loopexit:                          ; preds = %scalar.ph.prol, %scalar.ph.preheader
  %indvars.iv.unr = phi i64 [ %indvars.iv.ph, %scalar.ph.preheader ], [ %indvars.iv.next.prol, %scalar.ph.prol ]
  %28 = icmp eq i64 %indvars.iv.ph, %10
  br i1 %28, label %._crit_edge, label %scalar.ph

scalar.ph:                                        ; preds = %scalar.ph.prol.loopexit, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %scalar.ph ], [ %indvars.iv.unr, %scalar.ph.prol.loopexit ]
  %29 = trunc nuw nsw i64 %indvars.iv to i32
  %30 = uitofp nneg i32 %29 to double
  %31 = fmul double %12, %30
  %32 = fdiv double %31, %8
  %33 = getelementptr inbounds nuw double, ptr %14, i64 %indvars.iv
  store double %32, ptr %33, align 8
  %34 = getelementptr inbounds nuw double, ptr %15, i64 %indvars.iv
  store double %32, ptr %34, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %35 = trunc nuw nsw i64 %indvars.iv.next to i32
  %36 = uitofp nneg i32 %35 to double
  %37 = fmul double %12, %36
  %38 = fdiv double %37, %8
  %39 = getelementptr inbounds nuw double, ptr %14, i64 %indvars.iv.next
  store double %38, ptr %39, align 8
  %40 = getelementptr inbounds nuw double, ptr %15, i64 %indvars.iv.next
  store double %38, ptr %40, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %exitcond.not.1 = icmp eq i64 %indvars.iv.next.1, %4
  br i1 %exitcond.not.1, label %._crit_edge, label %scalar.ph, !llvm.loop !12

._crit_edge:                                      ; preds = %scalar.ph.prol.loopexit, %scalar.ph, %middle.block
  %indvars.iv.next28 = add nuw nsw i64 %indvars.iv27, 1
  %exitcond31.not = icmp eq i64 %indvars.iv.next28, %4
  br i1 %exitcond31.not, label %._crit_edge25, label %.lr.ph, !llvm.loop !13

._crit_edge25:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @gemm(i32 noundef %0, double noundef %1, double noundef %2, ptr noundef captures(none) %3, ptr noundef readonly captures(none) %4, ptr noundef readonly captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %0 to i64
  %8 = icmp sgt i32 %0, 0
  br i1 %8, label %.lr.ph33.preheader, label %._crit_edge36

.lr.ph33.preheader:                               ; preds = %6
  %xtraiter = and i64 %7, 1
  %9 = icmp eq i32 %0, 1
  %unroll_iter = and i64 %7, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br label %.lr.ph33

.lr.ph33:                                         ; preds = %.lr.ph33.preheader, %._crit_edge34
  %indvars.iv43 = phi i64 [ %indvars.iv.next44, %._crit_edge34 ], [ 0, %.lr.ph33.preheader ]
  %10 = mul nuw nsw i64 %indvars.iv43, %7
  %11 = getelementptr inbounds nuw double, ptr %3, i64 %10
  %12 = getelementptr inbounds nuw double, ptr %4, i64 %10
  br label %.lr.ph

.lr.ph:                                           ; preds = %.lr.ph33, %._crit_edge
  %indvars.iv38 = phi i64 [ 0, %.lr.ph33 ], [ %indvars.iv.next39, %._crit_edge ]
  %13 = getelementptr inbounds nuw double, ptr %11, i64 %indvars.iv38
  %14 = load double, ptr %13, align 8
  %15 = fmul double %2, %14
  store double %15, ptr %13, align 8
  %invariant.gep = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv38
  br i1 %9, label %._crit_edge.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %16 = phi double [ %28, %.lr.ph.new ], [ %15, %.lr.ph ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph.new ], [ 0, %.lr.ph ]
  %17 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv
  %18 = load double, ptr %17, align 8
  %19 = fmul double %1, %18
  %20 = mul nuw nsw i64 %indvars.iv, %7
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %20
  %21 = load double, ptr %gep, align 8
  %22 = tail call double @llvm.fmuladd.f64(double %19, double %21, double %16)
  store double %22, ptr %13, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %23 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.next
  %24 = load double, ptr %23, align 8
  %25 = fmul double %1, %24
  %26 = mul nuw nsw i64 %indvars.iv.next, %7
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %26
  %27 = load double, ptr %gep.1, align 8
  %28 = tail call double @llvm.fmuladd.f64(double %25, double %27, double %22)
  store double %28, ptr %13, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %._crit_edge.unr-lcssa, label %.lr.ph.new, !llvm.loop !14

._crit_edge.unr-lcssa:                            ; preds = %.lr.ph.new, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.1, %.lr.ph.new ]
  %.unr = phi double [ %15, %.lr.ph ], [ %28, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %._crit_edge, label %._crit_edge.epilog-lcssa

._crit_edge.epilog-lcssa:                         ; preds = %._crit_edge.unr-lcssa
  %29 = getelementptr inbounds nuw double, ptr %12, i64 %indvars.iv.unr
  %30 = load double, ptr %29, align 8
  %31 = fmul double %1, %30
  %32 = mul nuw nsw i64 %indvars.iv.unr, %7
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %32
  %33 = load double, ptr %gep.epil, align 8
  %34 = tail call double @llvm.fmuladd.f64(double %31, double %33, double %.unr)
  store double %34, ptr %13, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.unr-lcssa, %._crit_edge.epilog-lcssa
  %indvars.iv.next39 = add nuw nsw i64 %indvars.iv38, 1
  %exitcond42.not = icmp eq i64 %indvars.iv.next39, %7
  br i1 %exitcond42.not, label %._crit_edge34, label %.lr.ph, !llvm.loop !15

._crit_edge34:                                    ; preds = %._crit_edge
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  %exitcond47.not = icmp eq i64 %indvars.iv.next44, %7
  br i1 %exitcond47.not, label %._crit_edge36, label %.lr.ph33, !llvm.loop !16

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
!8 = distinct !{!8, !9, !10, !11}
!9 = !{!"llvm.loop.mustprogress"}
!10 = !{!"llvm.loop.isvectorized", i32 1}
!11 = !{!"llvm.loop.unroll.runtime.disable"}
!12 = distinct !{!12, !9, !10}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !9}
