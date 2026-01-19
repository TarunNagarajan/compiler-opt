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
  %7 = sitofp i32 %1 to double
  %wide.trip.count = zext nneg i32 %1 to i64
  %xtraiter = and i64 %wide.trip.count, 3
  %8 = icmp ult i32 %1, 4
  br i1 %8, label %.preheader25.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph
  %unroll_iter = and i64 %wide.trip.count, 2147483644
  br label %19

.preheader25.loopexit.unr-lcssa:                  ; preds = %19, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %19 ]
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %.preheader25, label %.epil.preheader

.epil.preheader:                                  ; preds = %.preheader25.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %.preheader25.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %.preheader25.loopexit.unr-lcssa ]
  %9 = trunc nuw nsw i64 %indvars.iv.epil to i32
  %10 = uitofp nneg i32 %9 to double
  %11 = fdiv double %10, %7
  %12 = fadd double %11, 1.000000e+00
  %13 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.epil
  store double %12, ptr %13, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %.preheader25, label %.epil.preheader, !llvm.loop !8

.preheader25:                                     ; preds = %.preheader25.loopexit.unr-lcssa, %.epil.preheader, %4
  %14 = icmp sgt i32 %0, 0
  br i1 %14, label %.preheader.lr.ph, label %._crit_edge30

.preheader.lr.ph:                                 ; preds = %.preheader25
  %15 = icmp sgt i32 %1, 0
  %16 = sitofp i32 %0 to double
  %wide.trip.count40 = zext nneg i32 %0 to i64
  %17 = zext i32 %1 to i64
  %xtraiter43 = and i64 %17, 3
  %18 = icmp ult i32 %1, 4
  %unroll_iter46 = and i64 %17, 2147483644
  %lcmp.mod45.not = icmp eq i64 %xtraiter43, 0
  br label %.preheader

19:                                               ; preds = %19, %.lr.ph.new
  %indvars.iv = phi i64 [ 0, %.lr.ph.new ], [ %indvars.iv.next.3, %19 ]
  %niter = phi i64 [ 0, %.lr.ph.new ], [ %niter.next.3, %19 ]
  %20 = trunc nuw nsw i64 %indvars.iv to i32
  %21 = uitofp nneg i32 %20 to double
  %22 = fdiv double %21, %7
  %23 = fadd double %22, 1.000000e+00
  %24 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %23, ptr %24, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %25 = trunc nuw nsw i64 %indvars.iv.next to i32
  %26 = uitofp nneg i32 %25 to double
  %27 = fdiv double %26, %7
  %28 = fadd double %27, 1.000000e+00
  %29 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  store double %28, ptr %29, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %30 = trunc nuw nsw i64 %indvars.iv.next.1 to i32
  %31 = uitofp nneg i32 %30 to double
  %32 = fdiv double %31, %7
  %33 = fadd double %32, 1.000000e+00
  %34 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next.1
  store double %33, ptr %34, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %35 = trunc nuw nsw i64 %indvars.iv.next.2 to i32
  %36 = uitofp nneg i32 %35 to double
  %37 = fdiv double %36, %7
  %38 = fadd double %37, 1.000000e+00
  %39 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next.2
  store double %38, ptr %39, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %.preheader25.loopexit.unr-lcssa, label %19, !llvm.loop !10

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv37 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next38, %._crit_edge ]
  br i1 %15, label %.lr.ph28, label %._crit_edge

.lr.ph28:                                         ; preds = %.preheader
  %40 = trunc nuw nsw i64 %indvars.iv37 to i32
  %41 = uitofp nneg i32 %40 to double
  %42 = mul nuw nsw i64 %indvars.iv37, %5
  %43 = getelementptr inbounds nuw double, ptr %2, i64 %42
  br i1 %18, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph28.new

.lr.ph28.new:                                     ; preds = %.lr.ph28, %.lr.ph28.new
  %indvars.iv32 = phi i64 [ %indvars.iv.next33.3, %.lr.ph28.new ], [ 0, %.lr.ph28 ]
  %niter47 = phi i64 [ %niter47.next.3, %.lr.ph28.new ], [ 0, %.lr.ph28 ]
  %indvars.iv.next33 = or disjoint i64 %indvars.iv32, 1
  %44 = trunc nuw nsw i64 %indvars.iv.next33 to i32
  %45 = uitofp nneg i32 %44 to double
  %46 = fmul double %41, %45
  %47 = fdiv double %46, %16
  %48 = getelementptr inbounds nuw double, ptr %43, i64 %indvars.iv32
  store double %47, ptr %48, align 8
  %indvars.iv.next33.1 = or disjoint i64 %indvars.iv32, 2
  %49 = trunc nuw nsw i64 %indvars.iv.next33.1 to i32
  %50 = uitofp nneg i32 %49 to double
  %51 = fmul double %41, %50
  %52 = fdiv double %51, %16
  %53 = getelementptr inbounds nuw double, ptr %43, i64 %indvars.iv.next33
  store double %52, ptr %53, align 8
  %indvars.iv.next33.2 = or disjoint i64 %indvars.iv32, 3
  %54 = trunc nuw nsw i64 %indvars.iv.next33.2 to i32
  %55 = uitofp nneg i32 %54 to double
  %56 = fmul double %41, %55
  %57 = fdiv double %56, %16
  %58 = getelementptr inbounds nuw double, ptr %43, i64 %indvars.iv.next33.1
  store double %57, ptr %58, align 8
  %indvars.iv.next33.3 = add nuw nsw i64 %indvars.iv32, 4
  %59 = trunc nuw nsw i64 %indvars.iv.next33.3 to i32
  %60 = uitofp nneg i32 %59 to double
  %61 = fmul double %41, %60
  %62 = fdiv double %61, %16
  %63 = getelementptr inbounds nuw double, ptr %43, i64 %indvars.iv.next33.2
  store double %62, ptr %63, align 8
  %niter47.next.3 = add i64 %niter47, 4
  %niter47.ncmp.3 = icmp eq i64 %niter47.next.3, %unroll_iter46
  br i1 %niter47.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph28.new, !llvm.loop !12

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph28.new, %.lr.ph28
  %indvars.iv32.unr = phi i64 [ 0, %.lr.ph28 ], [ %indvars.iv.next33.3, %.lr.ph28.new ]
  br i1 %lcmp.mod45.not, label %._crit_edge, label %.epil.preheader42

.epil.preheader42:                                ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader42
  %indvars.iv32.epil = phi i64 [ %indvars.iv.next33.epil, %.epil.preheader42 ], [ %indvars.iv32.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter44 = phi i64 [ %epil.iter44.next, %.epil.preheader42 ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %indvars.iv.next33.epil = add nuw nsw i64 %indvars.iv32.epil, 1
  %64 = trunc nuw nsw i64 %indvars.iv.next33.epil to i32
  %65 = uitofp nneg i32 %64 to double
  %66 = fmul double %41, %65
  %67 = fdiv double %66, %16
  %68 = getelementptr inbounds nuw double, ptr %43, i64 %indvars.iv32.epil
  store double %67, ptr %68, align 8
  %epil.iter44.next = add i64 %epil.iter44, 1
  %epil.iter44.cmp.not = icmp eq i64 %epil.iter44.next, %xtraiter43
  br i1 %epil.iter44.cmp.not, label %._crit_edge, label %.epil.preheader42, !llvm.loop !13

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader42, %.preheader
  %indvars.iv.next38 = add nuw nsw i64 %indvars.iv37, 1
  %exitcond41.not = icmp eq i64 %indvars.iv.next38, %wide.trip.count40
  br i1 %exitcond41.not, label %._crit_edge30, label %.preheader, !llvm.loop !14

._crit_edge30:                                    ; preds = %._crit_edge, %.preheader25
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @atax(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef readonly captures(none) %3, ptr noundef captures(none) %4, ptr noundef captures(none) %5) local_unnamed_addr #1 {
  %7 = zext i32 %1 to i64
  %8 = icmp sgt i32 %1, 0
  br i1 %8, label %.lr.ph.preheader, label %.preheader38

.lr.ph.preheader:                                 ; preds = %6
  %9 = zext nneg i32 %1 to i64
  %10 = shl nuw nsw i64 %9, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %4, i8 0, i64 %10, i1 false)
  br label %.preheader38

.preheader38:                                     ; preds = %.lr.ph.preheader, %6
  %11 = icmp sgt i32 %0, 0
  br i1 %11, label %.lr.ph45, label %._crit_edge46

.lr.ph45:                                         ; preds = %.preheader38
  %12 = icmp sgt i32 %1, 0
  %13 = icmp sgt i32 %1, 0
  %wide.trip.count57 = zext nneg i32 %0 to i64
  %14 = zext i32 %1 to i64
  %15 = add nsw i64 %14, -1
  %xtraiter = and i64 %14, 1
  %16 = icmp eq i64 %15, 0
  %unroll_iter = and i64 %14, 2147483646
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %xtraiter60 = and i64 %14, 1
  %17 = icmp eq i64 %15, 0
  %unroll_iter62 = and i64 %14, 2147483646
  %lcmp.mod61.not = icmp eq i64 %xtraiter60, 0
  br label %18

18:                                               ; preds = %.lr.ph45, %._crit_edge
  %indvars.iv54 = phi i64 [ 0, %.lr.ph45 ], [ %indvars.iv.next55, %._crit_edge ]
  %19 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv54
  store double 0.000000e+00, ptr %19, align 8
  br i1 %12, label %.lr.ph41, label %.preheader

.lr.ph41:                                         ; preds = %18
  %20 = mul nuw nsw i64 %indvars.iv54, %7
  %21 = getelementptr inbounds nuw double, ptr %2, i64 %20
  %.promoted = load double, ptr %19, align 8
  br i1 %16, label %.preheader.loopexit.unr-lcssa, label %.lr.ph41.new

.preheader.loopexit.unr-lcssa:                    ; preds = %.lr.ph41.new, %.lr.ph41
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph41 ], [ %indvars.iv.next.1, %.lr.ph41.new ]
  %.unr = phi double [ %.promoted, %.lr.ph41 ], [ %39, %.lr.ph41.new ]
  br i1 %lcmp.mod.not, label %.preheader, label %.preheader.loopexit.epilog-lcssa

.preheader.loopexit.epilog-lcssa:                 ; preds = %.preheader.loopexit.unr-lcssa
  %22 = getelementptr inbounds nuw double, ptr %21, i64 %indvars.iv.unr
  %23 = load double, ptr %22, align 8
  %24 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.unr
  %25 = load double, ptr %24, align 8
  %26 = tail call double @llvm.fmuladd.f64(double %23, double %25, double %.unr)
  store double %26, ptr %19, align 8
  br label %.preheader

.preheader:                                       ; preds = %.preheader.loopexit.epilog-lcssa, %.preheader.loopexit.unr-lcssa, %18
  br i1 %13, label %.lr.ph43, label %._crit_edge

.lr.ph43:                                         ; preds = %.preheader
  %27 = mul nuw nsw i64 %indvars.iv54, %7
  %28 = getelementptr inbounds nuw double, ptr %2, i64 %27
  br i1 %17, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph43.new

.lr.ph41.new:                                     ; preds = %.lr.ph41, %.lr.ph41.new
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %29 = phi double [ %39, %.lr.ph41.new ], [ %.promoted, %.lr.ph41 ]
  %niter = phi i64 [ %niter.next.1, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %30 = getelementptr inbounds nuw double, ptr %21, i64 %indvars.iv
  %31 = load double, ptr %30, align 8
  %32 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %33 = load double, ptr %32, align 8
  %34 = tail call double @llvm.fmuladd.f64(double %31, double %33, double %29)
  store double %34, ptr %19, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %35 = getelementptr inbounds nuw double, ptr %21, i64 %indvars.iv.next
  %36 = load double, ptr %35, align 8
  %37 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  %38 = load double, ptr %37, align 8
  %39 = tail call double @llvm.fmuladd.f64(double %36, double %38, double %34)
  store double %39, ptr %19, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %niter.next.1 = add i64 %niter, 2
  %niter.ncmp.1 = icmp eq i64 %niter.next.1, %unroll_iter
  br i1 %niter.ncmp.1, label %.preheader.loopexit.unr-lcssa, label %.lr.ph41.new, !llvm.loop !15

.lr.ph43.new:                                     ; preds = %.lr.ph43, %.lr.ph43.new
  %indvars.iv49 = phi i64 [ %indvars.iv.next50.1, %.lr.ph43.new ], [ 0, %.lr.ph43 ]
  %niter63 = phi i64 [ %niter63.next.1, %.lr.ph43.new ], [ 0, %.lr.ph43 ]
  %40 = getelementptr inbounds nuw double, ptr %28, i64 %indvars.iv49
  %41 = load double, ptr %40, align 8
  %42 = load double, ptr %19, align 8
  %43 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv49
  %44 = load double, ptr %43, align 8
  %45 = tail call double @llvm.fmuladd.f64(double %41, double %42, double %44)
  store double %45, ptr %43, align 8
  %indvars.iv.next50 = or disjoint i64 %indvars.iv49, 1
  %46 = getelementptr inbounds nuw double, ptr %28, i64 %indvars.iv.next50
  %47 = load double, ptr %46, align 8
  %48 = load double, ptr %19, align 8
  %49 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next50
  %50 = load double, ptr %49, align 8
  %51 = tail call double @llvm.fmuladd.f64(double %47, double %48, double %50)
  store double %51, ptr %49, align 8
  %indvars.iv.next50.1 = add nuw nsw i64 %indvars.iv49, 2
  %niter63.next.1 = add i64 %niter63, 2
  %niter63.ncmp.1 = icmp eq i64 %niter63.next.1, %unroll_iter62
  br i1 %niter63.ncmp.1, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph43.new, !llvm.loop !16

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph43.new, %.lr.ph43
  %indvars.iv49.unr = phi i64 [ 0, %.lr.ph43 ], [ %indvars.iv.next50.1, %.lr.ph43.new ]
  br i1 %lcmp.mod61.not, label %._crit_edge, label %._crit_edge.loopexit.epilog-lcssa

._crit_edge.loopexit.epilog-lcssa:                ; preds = %._crit_edge.loopexit.unr-lcssa
  %52 = getelementptr inbounds nuw double, ptr %28, i64 %indvars.iv49.unr
  %53 = load double, ptr %52, align 8
  %54 = load double, ptr %19, align 8
  %55 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv49.unr
  %56 = load double, ptr %55, align 8
  %57 = tail call double @llvm.fmuladd.f64(double %53, double %54, double %56)
  store double %57, ptr %55, align 8
  br label %._crit_edge

._crit_edge:                                      ; preds = %._crit_edge.loopexit.epilog-lcssa, %._crit_edge.loopexit.unr-lcssa, %.preheader
  %indvars.iv.next55 = add nuw nsw i64 %indvars.iv54, 1
  %exitcond58.not = icmp eq i64 %indvars.iv.next55, %wide.trip.count57
  br i1 %exitcond58.not, label %._crit_edge46, label %18, !llvm.loop !17

._crit_edge46:                                    ; preds = %._crit_edge, %.preheader38
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #3 {
  %1 = tail call dereferenceable_or_null(2097152) ptr @malloc(i64 noundef 2097152) #8
  %2 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #8
  %3 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #8
  %4 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #8
  tail call void @init_array(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %2)
  %5 = tail call i32 @clock() #9
  tail call void @atax(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4)
  %6 = tail call i32 @clock() #9
  %7 = sub nsw i32 %6, %5
  %8 = sitofp i32 %7 to double
  %9 = fdiv double %8, 1.000000e+03
  %10 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %9) #9
  %11 = load double, ptr %3, align 8
  %12 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %11) #9
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

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nocallback nofree nounwind willreturn memory(argmem: write) }
attributes #8 = { allocsize(0) }
attributes #9 = { nounwind }

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
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.unroll.disable"}
!10 = distinct !{!10, !11}
!11 = !{!"llvm.loop.mustprogress"}
!12 = distinct !{!12, !11}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !11}
!15 = distinct !{!15, !11}
!16 = distinct !{!16, !11}
!17 = distinct !{!17, !11}
