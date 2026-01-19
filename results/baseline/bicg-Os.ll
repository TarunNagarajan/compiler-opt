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
  %8 = uitofp nneg i32 %1 to double
  %min.iters.check = icmp eq i32 %1, 1
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %n.vec = and i64 %6, 2147483646
  %broadcast.splatinsert = insertelement <2 x double> poison, double %8, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %9 = uitofp nneg <2 x i32> %vec.ind to <2 x double>
  %10 = fdiv <2 x double> %9, %broadcast.splat
  %11 = getelementptr inbounds nuw double, ptr %3, i64 %index
  store <2 x double> %10, ptr %11, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %12 = icmp eq i64 %index.next, %n.vec
  br i1 %12, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  %cmp.n = icmp eq i64 %n.vec, %6
  br i1 %cmp.n, label %.preheader36, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  br label %scalar.ph

.preheader36:                                     ; preds = %scalar.ph, %middle.block, %5
  %13 = icmp sgt i32 %0, 0
  br i1 %13, label %.lr.ph39, label %._crit_edge43

.lr.ph39:                                         ; preds = %.preheader36
  %14 = uitofp nneg i32 %0 to double
  %wide.trip.count48 = zext nneg i32 %0 to i64
  %min.iters.check61 = icmp eq i32 %0, 1
  br i1 %min.iters.check61, label %scalar.ph60.preheader, label %vector.ph62

vector.ph62:                                      ; preds = %.lr.ph39
  %n.vec64 = and i64 %wide.trip.count48, 2147483646
  %broadcast.splatinsert65 = insertelement <2 x double> poison, double %14, i64 0
  %broadcast.splat66 = shufflevector <2 x double> %broadcast.splatinsert65, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body67

vector.body67:                                    ; preds = %vector.body67, %vector.ph62
  %index68 = phi i64 [ 0, %vector.ph62 ], [ %index.next70, %vector.body67 ]
  %vec.ind69 = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph62 ], [ %vec.ind.next71, %vector.body67 ]
  %15 = uitofp nneg <2 x i32> %vec.ind69 to <2 x double>
  %16 = fdiv <2 x double> %15, %broadcast.splat66
  %17 = getelementptr inbounds nuw double, ptr %4, i64 %index68
  store <2 x double> %16, ptr %17, align 8
  %index.next70 = add nuw i64 %index68, 2
  %vec.ind.next71 = add <2 x i32> %vec.ind69, splat (i32 2)
  %18 = icmp eq i64 %index.next70, %n.vec64
  br i1 %18, label %middle.block72, label %vector.body67, !llvm.loop !12

middle.block72:                                   ; preds = %vector.body67
  %cmp.n73 = icmp eq i64 %n.vec64, %wide.trip.count48
  br i1 %cmp.n73, label %.preheader.lr.ph, label %scalar.ph60.preheader

scalar.ph60.preheader:                            ; preds = %.lr.ph39, %middle.block72
  %indvars.iv45.ph = phi i64 [ 0, %.lr.ph39 ], [ %n.vec64, %middle.block72 ]
  br label %scalar.ph60

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %19 = trunc nuw nsw i64 %indvars.iv to i32
  %20 = uitofp nneg i32 %19 to double
  %21 = fdiv double %20, %8
  %22 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %21, ptr %22, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %6
  br i1 %exitcond.not, label %.preheader36, label %scalar.ph, !llvm.loop !13

.preheader.lr.ph:                                 ; preds = %scalar.ph60, %middle.block72
  %23 = uitofp nneg i32 %0 to double
  %wide.trip.count58 = zext nneg i32 %0 to i64
  %min.iters.check76 = icmp eq i32 %1, 1
  %n.vec79 = and i64 %6, 2147483646
  %broadcast.splatinsert82 = insertelement <2 x double> poison, double %23, i64 0
  %broadcast.splat83 = shufflevector <2 x double> %broadcast.splatinsert82, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n90 = icmp eq i64 %n.vec79, %6
  br label %.preheader

scalar.ph60:                                      ; preds = %scalar.ph60.preheader, %scalar.ph60
  %indvars.iv45 = phi i64 [ %indvars.iv.next46, %scalar.ph60 ], [ %indvars.iv45.ph, %scalar.ph60.preheader ]
  %24 = trunc nuw nsw i64 %indvars.iv45 to i32
  %25 = uitofp nneg i32 %24 to double
  %26 = fdiv double %25, %14
  %27 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv45
  store double %26, ptr %27, align 8
  %indvars.iv.next46 = add nuw nsw i64 %indvars.iv45, 1
  %exitcond49.not = icmp eq i64 %indvars.iv.next46, %wide.trip.count48
  br i1 %exitcond49.not, label %.preheader.lr.ph, label %scalar.ph60, !llvm.loop !14

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv55 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next56, %._crit_edge ]
  br i1 %7, label %.lr.ph41, label %._crit_edge

.lr.ph41:                                         ; preds = %.preheader
  %28 = mul nuw nsw i64 %indvars.iv55, %6
  %29 = getelementptr inbounds nuw double, ptr %2, i64 %28
  br i1 %min.iters.check76, label %scalar.ph75.preheader, label %vector.ph77

vector.ph77:                                      ; preds = %.lr.ph41
  %broadcast.splatinsert80 = insertelement <2 x i64> poison, i64 %indvars.iv55, i64 0
  %broadcast.splat81 = shufflevector <2 x i64> %broadcast.splatinsert80, <2 x i64> poison, <2 x i32> zeroinitializer
  br label %vector.body84

vector.body84:                                    ; preds = %vector.body84, %vector.ph77
  %index85 = phi i64 [ 0, %vector.ph77 ], [ %index.next87, %vector.body84 ]
  %vec.ind86 = phi <2 x i64> [ <i64 0, i64 1>, %vector.ph77 ], [ %vec.ind.next88, %vector.body84 ]
  %30 = add nuw nsw <2 x i64> %vec.ind86, splat (i64 1)
  %31 = mul nuw nsw <2 x i64> %30, %broadcast.splat81
  %32 = trunc nuw <2 x i64> %31 to <2 x i32>
  %33 = uitofp nneg <2 x i32> %32 to <2 x double>
  %34 = fdiv <2 x double> %33, %broadcast.splat83
  %35 = getelementptr inbounds nuw double, ptr %29, i64 %index85
  store <2 x double> %34, ptr %35, align 8
  %index.next87 = add nuw i64 %index85, 2
  %vec.ind.next88 = add <2 x i64> %vec.ind86, splat (i64 2)
  %36 = icmp eq i64 %index.next87, %n.vec79
  br i1 %36, label %middle.block89, label %vector.body84, !llvm.loop !15

middle.block89:                                   ; preds = %vector.body84
  br i1 %cmp.n90, label %._crit_edge, label %scalar.ph75.preheader

scalar.ph75.preheader:                            ; preds = %.lr.ph41, %middle.block89
  %indvars.iv50.ph = phi i64 [ 0, %.lr.ph41 ], [ %n.vec79, %middle.block89 ]
  br label %scalar.ph75

scalar.ph75:                                      ; preds = %scalar.ph75.preheader, %scalar.ph75
  %indvars.iv50 = phi i64 [ %indvars.iv.next51, %scalar.ph75 ], [ %indvars.iv50.ph, %scalar.ph75.preheader ]
  %indvars.iv.next51 = add nuw nsw i64 %indvars.iv50, 1
  %37 = mul nuw nsw i64 %indvars.iv.next51, %indvars.iv55
  %38 = trunc nuw i64 %37 to i32
  %39 = uitofp nneg i32 %38 to double
  %40 = fdiv double %39, %23
  %41 = getelementptr inbounds nuw double, ptr %29, i64 %indvars.iv50
  store double %40, ptr %41, align 8
  %exitcond54.not = icmp eq i64 %indvars.iv.next51, %6
  br i1 %exitcond54.not, label %._crit_edge, label %scalar.ph75, !llvm.loop !16

._crit_edge:                                      ; preds = %scalar.ph75, %middle.block89, %.preheader
  %indvars.iv.next56 = add nuw nsw i64 %indvars.iv55, 1
  %exitcond59.not = icmp eq i64 %indvars.iv.next56, %wide.trip.count58
  br i1 %exitcond59.not, label %._crit_edge43, label %.preheader, !llvm.loop !17

._crit_edge43:                                    ; preds = %._crit_edge, %.preheader36
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @bicg(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4, ptr noundef readonly captures(none) %5, ptr noundef readonly captures(none) %6) local_unnamed_addr #1 {
  %8 = zext i32 %1 to i64
  %9 = icmp sgt i32 %1, 0
  br i1 %9, label %.lr.ph.preheader, label %.preheader

.lr.ph.preheader:                                 ; preds = %7
  %10 = shl nuw nsw i64 %8, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %3, i8 0, i64 %10, i1 false)
  br label %.preheader

.preheader:                                       ; preds = %.lr.ph.preheader, %7
  %11 = icmp sgt i32 %0, 0
  br i1 %11, label %.lr.ph39, label %._crit_edge40

.lr.ph39:                                         ; preds = %.preheader
  %wide.trip.count46 = zext nneg i32 %0 to i64
  br label %12

12:                                               ; preds = %.lr.ph39, %._crit_edge
  %indvars.iv43 = phi i64 [ 0, %.lr.ph39 ], [ %indvars.iv.next44, %._crit_edge ]
  %13 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv43
  store double 0.000000e+00, ptr %13, align 8
  br i1 %9, label %.lr.ph37, label %._crit_edge

.lr.ph37:                                         ; preds = %12
  %14 = getelementptr inbounds nuw double, ptr %6, i64 %indvars.iv43
  %15 = mul nuw nsw i64 %indvars.iv43, %8
  %16 = getelementptr inbounds nuw double, ptr %2, i64 %15
  br label %17

17:                                               ; preds = %.lr.ph37, %17
  %indvars.iv = phi i64 [ 0, %.lr.ph37 ], [ %indvars.iv.next, %17 ]
  %18 = load double, ptr %14, align 8
  %19 = getelementptr inbounds nuw double, ptr %16, i64 %indvars.iv
  %20 = load double, ptr %19, align 8
  %21 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  %22 = load double, ptr %21, align 8
  %23 = tail call double @llvm.fmuladd.f64(double %18, double %20, double %22)
  store double %23, ptr %21, align 8
  %24 = load double, ptr %19, align 8
  %25 = getelementptr inbounds nuw double, ptr %5, i64 %indvars.iv
  %26 = load double, ptr %25, align 8
  %27 = load double, ptr %13, align 8
  %28 = tail call double @llvm.fmuladd.f64(double %24, double %26, double %27)
  store double %28, ptr %13, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %8
  br i1 %exitcond.not, label %._crit_edge, label %17, !llvm.loop !18

._crit_edge:                                      ; preds = %17, %12
  %indvars.iv.next44 = add nuw nsw i64 %indvars.iv43, 1
  %exitcond47.not = icmp eq i64 %indvars.iv.next44, %wide.trip.count46
  br i1 %exitcond47.not, label %._crit_edge40, label %12, !llvm.loop !19

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
!8 = distinct !{!8, !9, !10, !11}
!9 = !{!"llvm.loop.mustprogress"}
!10 = !{!"llvm.loop.isvectorized", i32 1}
!11 = !{!"llvm.loop.unroll.runtime.disable"}
!12 = distinct !{!12, !9, !10, !11}
!13 = distinct !{!13, !9, !11, !10}
!14 = distinct !{!14, !9, !11, !10}
!15 = distinct !{!15, !9, !10, !11}
!16 = distinct !{!16, !9, !11, !10}
!17 = distinct !{!17, !9}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
