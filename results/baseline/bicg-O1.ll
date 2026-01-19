; ModuleID = 'results\baseline\bicg_base.ll'
source_filename = "benchmarks\\bicg.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [27 x i8] c"BiCG Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef writeonly captures(none) %2, ptr noundef writeonly captures(none) %3, ptr noundef writeonly captures(none) %4) local_unnamed_addr #0 {
  %6 = zext i32 %1 to i64
  %7 = icmp sgt i32 %1, 0
  br i1 %7, label %.lr.ph, label %.preheader36

.lr.ph:                                           ; preds = %5
  %8 = sitofp i32 %1 to double
  %wide.trip.count = zext nneg i32 %1 to i64
  %xtraiter = and i64 %wide.trip.count, 3
  %9 = icmp ult i32 %1, 4
  br i1 %9, label %.preheader36.loopexit.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph
  %unroll_iter = and i64 %wide.trip.count, 2147483644
  br label %17

.preheader36.loopexit.unr-lcssa:                  ; preds = %17, %.lr.ph
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %17 ]
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %.preheader36, label %.epil.preheader

.epil.preheader:                                  ; preds = %.preheader36.loopexit.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %.preheader36.loopexit.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %.preheader36.loopexit.unr-lcssa ]
  %10 = trunc nuw nsw i64 %indvars.iv.epil to i32
  %11 = uitofp nneg i32 %10 to double
  %12 = fdiv double %11, %8
  %13 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.epil
  store double %12, ptr %13, align 8
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %.preheader36, label %.epil.preheader, !llvm.loop !8

.preheader36:                                     ; preds = %.preheader36.loopexit.unr-lcssa, %.epil.preheader, %5
  %14 = icmp sgt i32 %0, 0
  br i1 %14, label %.lr.ph39, label %.preheader35

.lr.ph39:                                         ; preds = %.preheader36
  %15 = sitofp i32 %0 to double
  %wide.trip.count48 = zext nneg i32 %0 to i64
  %xtraiter61 = and i64 %wide.trip.count48, 3
  %16 = icmp ult i32 %0, 4
  br i1 %16, label %.preheader35.loopexit.unr-lcssa, label %.lr.ph39.new

.lr.ph39.new:                                     ; preds = %.lr.ph39
  %unroll_iter64 = and i64 %wide.trip.count48, 2147483644
  br label %43

17:                                               ; preds = %17, %.lr.ph.new
  %indvars.iv = phi i64 [ 0, %.lr.ph.new ], [ %indvars.iv.next.3, %17 ]
  %niter = phi i64 [ 0, %.lr.ph.new ], [ %niter.next.3, %17 ]
  %18 = trunc nuw nsw i64 %indvars.iv to i32
  %19 = uitofp nneg i32 %18 to double
  %20 = fdiv double %19, %8
  %21 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %20, ptr %21, align 8
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %22 = trunc nuw nsw i64 %indvars.iv.next to i32
  %23 = uitofp nneg i32 %22 to double
  %24 = fdiv double %23, %8
  %25 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  store double %24, ptr %25, align 8
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %26 = trunc nuw nsw i64 %indvars.iv.next.1 to i32
  %27 = uitofp nneg i32 %26 to double
  %28 = fdiv double %27, %8
  %29 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next.1
  store double %28, ptr %29, align 8
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %30 = trunc nuw nsw i64 %indvars.iv.next.2 to i32
  %31 = uitofp nneg i32 %30 to double
  %32 = fdiv double %31, %8
  %33 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next.2
  store double %32, ptr %33, align 8
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %.preheader36.loopexit.unr-lcssa, label %17, !llvm.loop !10

.preheader35.loopexit.unr-lcssa:                  ; preds = %43, %.lr.ph39
  %indvars.iv45.unr = phi i64 [ 0, %.lr.ph39 ], [ %indvars.iv.next46.3, %43 ]
  %lcmp.mod63.not = icmp eq i64 %xtraiter61, 0
  br i1 %lcmp.mod63.not, label %.preheader35, label %.epil.preheader60

.epil.preheader60:                                ; preds = %.preheader35.loopexit.unr-lcssa, %.epil.preheader60
  %indvars.iv45.epil = phi i64 [ %indvars.iv.next46.epil, %.epil.preheader60 ], [ %indvars.iv45.unr, %.preheader35.loopexit.unr-lcssa ]
  %epil.iter62 = phi i64 [ %epil.iter62.next, %.epil.preheader60 ], [ 0, %.preheader35.loopexit.unr-lcssa ]
  %34 = trunc nuw nsw i64 %indvars.iv45.epil to i32
  %35 = uitofp nneg i32 %34 to double
  %36 = fdiv double %35, %15
  %37 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv45.epil
  store double %36, ptr %37, align 8
  %indvars.iv.next46.epil = add nuw nsw i64 %indvars.iv45.epil, 1
  %epil.iter62.next = add i64 %epil.iter62, 1
  %epil.iter62.cmp.not = icmp eq i64 %epil.iter62.next, %xtraiter61
  br i1 %epil.iter62.cmp.not, label %.preheader35, label %.epil.preheader60, !llvm.loop !12

.preheader35:                                     ; preds = %.preheader35.loopexit.unr-lcssa, %.epil.preheader60, %.preheader36
  %38 = icmp sgt i32 %0, 0
  br i1 %38, label %.preheader.lr.ph, label %._crit_edge43

.preheader.lr.ph:                                 ; preds = %.preheader35
  %39 = icmp sgt i32 %1, 0
  %40 = sitofp i32 %0 to double
  %wide.trip.count58 = zext nneg i32 %0 to i64
  %41 = zext i32 %1 to i64
  %xtraiter67 = and i64 %41, 3
  %42 = icmp ult i32 %1, 4
  %unroll_iter70 = and i64 %41, 2147483644
  %lcmp.mod69.not = icmp eq i64 %xtraiter67, 0
  br label %.preheader

43:                                               ; preds = %43, %.lr.ph39.new
  %indvars.iv45 = phi i64 [ 0, %.lr.ph39.new ], [ %indvars.iv.next46.3, %43 ]
  %niter65 = phi i64 [ 0, %.lr.ph39.new ], [ %niter65.next.3, %43 ]
  %44 = trunc nuw nsw i64 %indvars.iv45 to i32
  %45 = uitofp nneg i32 %44 to double
  %46 = fdiv double %45, %15
  %47 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv45
  store double %46, ptr %47, align 8
  %indvars.iv.next46 = or disjoint i64 %indvars.iv45, 1
  %48 = trunc nuw nsw i64 %indvars.iv.next46 to i32
  %49 = uitofp nneg i32 %48 to double
  %50 = fdiv double %49, %15
  %51 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next46
  store double %50, ptr %51, align 8
  %indvars.iv.next46.1 = or disjoint i64 %indvars.iv45, 2
  %52 = trunc nuw nsw i64 %indvars.iv.next46.1 to i32
  %53 = uitofp nneg i32 %52 to double
  %54 = fdiv double %53, %15
  %55 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next46.1
  store double %54, ptr %55, align 8
  %indvars.iv.next46.2 = or disjoint i64 %indvars.iv45, 3
  %56 = trunc nuw nsw i64 %indvars.iv.next46.2 to i32
  %57 = uitofp nneg i32 %56 to double
  %58 = fdiv double %57, %15
  %59 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv.next46.2
  store double %58, ptr %59, align 8
  %indvars.iv.next46.3 = add nuw nsw i64 %indvars.iv45, 4
  %niter65.next.3 = add i64 %niter65, 4
  %niter65.ncmp.3 = icmp eq i64 %niter65.next.3, %unroll_iter64
  br i1 %niter65.ncmp.3, label %.preheader35.loopexit.unr-lcssa, label %43, !llvm.loop !13

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv55 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next56, %._crit_edge ]
  br i1 %39, label %.lr.ph41, label %._crit_edge

.lr.ph41:                                         ; preds = %.preheader
  %60 = mul nuw nsw i64 %indvars.iv55, %6
  %61 = getelementptr inbounds nuw double, ptr %2, i64 %60
  br i1 %42, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph41.new

.lr.ph41.new:                                     ; preds = %.lr.ph41, %.lr.ph41.new
  %indvars.iv50 = phi i64 [ %indvars.iv.next51.3, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %niter71 = phi i64 [ %niter71.next.3, %.lr.ph41.new ], [ 0, %.lr.ph41 ]
  %indvars.iv.next51 = or disjoint i64 %indvars.iv50, 1
  %62 = mul nuw nsw i64 %indvars.iv.next51, %indvars.iv55
  %63 = trunc nuw i64 %62 to i32
  %64 = uitofp nneg i32 %63 to double
  %65 = fdiv double %64, %40
  %66 = getelementptr inbounds nuw double, ptr %61, i64 %indvars.iv50
  store double %65, ptr %66, align 8
  %indvars.iv.next51.1 = or disjoint i64 %indvars.iv50, 2
  %67 = mul nuw nsw i64 %indvars.iv.next51.1, %indvars.iv55
  %68 = trunc nuw i64 %67 to i32
  %69 = uitofp nneg i32 %68 to double
  %70 = fdiv double %69, %40
  %71 = getelementptr inbounds nuw double, ptr %61, i64 %indvars.iv.next51
  store double %70, ptr %71, align 8
  %indvars.iv.next51.2 = or disjoint i64 %indvars.iv50, 3
  %72 = mul nuw nsw i64 %indvars.iv.next51.2, %indvars.iv55
  %73 = trunc nuw i64 %72 to i32
  %74 = uitofp nneg i32 %73 to double
  %75 = fdiv double %74, %40
  %76 = getelementptr inbounds nuw double, ptr %61, i64 %indvars.iv.next51.1
  store double %75, ptr %76, align 8
  %indvars.iv.next51.3 = add nuw nsw i64 %indvars.iv50, 4
  %77 = mul nuw nsw i64 %indvars.iv.next51.3, %indvars.iv55
  %78 = trunc nuw i64 %77 to i32
  %79 = uitofp nneg i32 %78 to double
  %80 = fdiv double %79, %40
  %81 = getelementptr inbounds nuw double, ptr %61, i64 %indvars.iv.next51.2
  store double %80, ptr %81, align 8
  %niter71.next.3 = add i64 %niter71, 4
  %niter71.ncmp.3 = icmp eq i64 %niter71.next.3, %unroll_iter70
  br i1 %niter71.ncmp.3, label %._crit_edge.loopexit.unr-lcssa, label %.lr.ph41.new, !llvm.loop !14

._crit_edge.loopexit.unr-lcssa:                   ; preds = %.lr.ph41.new, %.lr.ph41
  %indvars.iv50.unr = phi i64 [ 0, %.lr.ph41 ], [ %indvars.iv.next51.3, %.lr.ph41.new ]
  br i1 %lcmp.mod69.not, label %._crit_edge, label %.epil.preheader66

.epil.preheader66:                                ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader66
  %indvars.iv50.epil = phi i64 [ %indvars.iv.next51.epil, %.epil.preheader66 ], [ %indvars.iv50.unr, %._crit_edge.loopexit.unr-lcssa ]
  %epil.iter68 = phi i64 [ %epil.iter68.next, %.epil.preheader66 ], [ 0, %._crit_edge.loopexit.unr-lcssa ]
  %indvars.iv.next51.epil = add nuw nsw i64 %indvars.iv50.epil, 1
  %82 = mul nuw nsw i64 %indvars.iv.next51.epil, %indvars.iv55
  %83 = trunc nuw i64 %82 to i32
  %84 = uitofp nneg i32 %83 to double
  %85 = fdiv double %84, %40
  %86 = getelementptr inbounds nuw double, ptr %61, i64 %indvars.iv50.epil
  store double %85, ptr %86, align 8
  %epil.iter68.next = add i64 %epil.iter68, 1
  %epil.iter68.cmp.not = icmp eq i64 %epil.iter68.next, %xtraiter67
  br i1 %epil.iter68.cmp.not, label %._crit_edge, label %.epil.preheader66, !llvm.loop !15

._crit_edge:                                      ; preds = %._crit_edge.loopexit.unr-lcssa, %.epil.preheader66, %.preheader
  %indvars.iv.next56 = add nuw nsw i64 %indvars.iv55, 1
  %exitcond59.not = icmp eq i64 %indvars.iv.next56, %wide.trip.count58
  br i1 %exitcond59.not, label %._crit_edge43, label %.preheader, !llvm.loop !16

._crit_edge43:                                    ; preds = %._crit_edge, %.preheader35
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @bicg(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4, ptr noundef readonly captures(none) %5, ptr noundef readonly captures(none) %6) local_unnamed_addr #1 {
  %8 = zext i32 %1 to i64
  %9 = icmp sgt i32 %1, 0
  br i1 %9, label %.lr.ph.preheader, label %.preheader

.lr.ph.preheader:                                 ; preds = %7
  %10 = zext nneg i32 %1 to i64
  %11 = shl nuw nsw i64 %10, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %3, i8 0, i64 %11, i1 false)
  br label %.preheader

.preheader:                                       ; preds = %.lr.ph.preheader, %7
  %12 = icmp sgt i32 %0, 0
  br i1 %12, label %.lr.ph39, label %._crit_edge40

.lr.ph39:                                         ; preds = %.preheader
  %13 = icmp sgt i32 %1, 0
  %wide.trip.count46 = zext nneg i32 %0 to i64
  %wide.trip.count = zext nneg i32 %1 to i64
  br label %14

14:                                               ; preds = %.lr.ph39, %._crit_edge
  %indvars.iv43 = phi i64 [ 0, %.lr.ph39 ], [ %indvars.iv.next44, %._crit_edge ]
  %15 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv43
  store double 0.000000e+00, ptr %15, align 8
  br i1 %13, label %.lr.ph37, label %._crit_edge

.lr.ph37:                                         ; preds = %14
  %16 = getelementptr inbounds nuw double, ptr %6, i64 %indvars.iv43
  %17 = mul nuw nsw i64 %indvars.iv43, %8
  %18 = getelementptr inbounds nuw double, ptr %2, i64 %17
  br label %19

19:                                               ; preds = %.lr.ph37, %19
  %indvars.iv = phi i64 [ 0, %.lr.ph37 ], [ %indvars.iv.next, %19 ]
  %20 = load double, ptr %16, align 8
  %21 = getelementptr inbounds nuw double, ptr %18, i64 %indvars.iv
  %22 = load double, ptr %21, align 8
  %23 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %24 = load double, ptr %23, align 8
  %25 = tail call double @llvm.fmuladd.f64(double %20, double %22, double %24)
  store double %25, ptr %23, align 8
  %26 = load double, ptr %21, align 8
  %27 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv
  %28 = load double, ptr %27, align 8
  %29 = load double, ptr %15, align 8
  %30 = tail call double @llvm.fmuladd.f64(double %26, double %28, double %29)
  store double %30, ptr %15, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %wide.trip.count
  br i1 %exitcond.not, label %._crit_edge, label %19, !llvm.loop !17

._crit_edge:                                      ; preds = %19, %14
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  %exitcond47.not = icmp eq i64 %indvars.iv.next44, %wide.trip.count46
  br i1 %exitcond47.not, label %._crit_edge40, label %14, !llvm.loop !18

._crit_edge40:                                    ; preds = %._crit_edge, %.preheader
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
  %5 = tail call dereferenceable_or_null(4096) ptr @malloc(i64 noundef 4096) #8
  tail call void @init_array(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %4, ptr noundef %5)
  %6 = tail call i32 @clock() #9
  tail call void @bicg(i32 noundef 512, i32 noundef 512, ptr noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4, ptr noundef %5)
  %7 = tail call i32 @clock() #9
  %8 = sub nsw i32 %7, %6
  %9 = sitofp i32 %8 to double
  %10 = fdiv double %9, 1.000000e+03
  %11 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %10) #9
  %12 = load double, ptr %2, align 8
  %13 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %12) #9
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
!1 = !DIFile(filename: "benchmarks/bicg.c", directory: "C:/Users/ultim/compiler-opt")
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
!12 = distinct !{!12, !9}
!13 = distinct !{!13, !11}
!14 = distinct !{!14, !11}
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !11}
!17 = distinct !{!17, !11}
!18 = distinct !{!18, !11}
