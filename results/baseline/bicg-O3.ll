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
  %wide.trip.count49 = zext nneg i32 %0 to i64
  %min.iters.check62 = icmp eq i32 %0, 1
  br i1 %min.iters.check62, label %scalar.ph61.preheader, label %vector.ph63

vector.ph63:                                      ; preds = %.lr.ph39
  %n.vec65 = and i64 %wide.trip.count49, 2147483646
  %broadcast.splatinsert66 = insertelement <2 x double> poison, double %14, i64 0
  %broadcast.splat67 = shufflevector <2 x double> %broadcast.splatinsert66, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body68

vector.body68:                                    ; preds = %vector.body68, %vector.ph63
  %index69 = phi i64 [ 0, %vector.ph63 ], [ %index.next71, %vector.body68 ]
  %vec.ind70 = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph63 ], [ %vec.ind.next72, %vector.body68 ]
  %15 = uitofp nneg <2 x i32> %vec.ind70 to <2 x double>
  %16 = fdiv <2 x double> %15, %broadcast.splat67
  %17 = getelementptr inbounds nuw double, ptr %4, i64 %index69
  store <2 x double> %16, ptr %17, align 8
  %index.next71 = add nuw i64 %index69, 2
  %vec.ind.next72 = add <2 x i32> %vec.ind70, splat (i32 2)
  %18 = icmp eq i64 %index.next71, %n.vec65
  br i1 %18, label %middle.block73, label %vector.body68, !llvm.loop !12

middle.block73:                                   ; preds = %vector.body68
  %cmp.n74 = icmp eq i64 %n.vec65, %wide.trip.count49
  br i1 %cmp.n74, label %.preheader.lr.ph, label %scalar.ph61.preheader

scalar.ph61.preheader:                            ; preds = %.lr.ph39, %middle.block73
  %indvars.iv46.ph = phi i64 [ 0, %.lr.ph39 ], [ %n.vec65, %middle.block73 ]
  br label %scalar.ph61

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

.preheader.lr.ph:                                 ; preds = %scalar.ph61, %middle.block73
  %23 = uitofp nneg i32 %0 to double
  br i1 %7, label %.preheader.us.preheader, label %._crit_edge43

.preheader.us.preheader:                          ; preds = %.preheader.lr.ph
  %wide.trip.count59 = zext nneg i32 %0 to i64
  %min.iters.check77 = icmp eq i32 %1, 1
  %n.vec80 = and i64 %6, 2147483646
  %broadcast.splatinsert83 = insertelement <2 x double> poison, double %23, i64 0
  %broadcast.splat84 = shufflevector <2 x double> %broadcast.splatinsert83, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n91 = icmp eq i64 %n.vec80, %6
  br label %.preheader.us

.preheader.us:                                    ; preds = %.preheader.us.preheader, %._crit_edge.us
  %indvars.iv56 = phi i64 [ 0, %.preheader.us.preheader ], [ %indvars.iv.next57, %._crit_edge.us ]
  %24 = mul nuw nsw i64 %indvars.iv56, %6
  %25 = getelementptr inbounds nuw double, ptr %2, i64 %24
  br i1 %min.iters.check77, label %scalar.ph76.preheader, label %vector.ph78

vector.ph78:                                      ; preds = %.preheader.us
  %broadcast.splatinsert81 = insertelement <2 x i64> poison, i64 %indvars.iv56, i64 0
  %broadcast.splat82 = shufflevector <2 x i64> %broadcast.splatinsert81, <2 x i64> poison, <2 x i32> zeroinitializer
  br label %vector.body85

vector.body85:                                    ; preds = %vector.body85, %vector.ph78
  %index86 = phi i64 [ 0, %vector.ph78 ], [ %index.next88, %vector.body85 ]
  %vec.ind87 = phi <2 x i64> [ <i64 0, i64 1>, %vector.ph78 ], [ %vec.ind.next89, %vector.body85 ]
  %26 = add nuw nsw <2 x i64> %vec.ind87, splat (i64 1)
  %27 = mul nuw nsw <2 x i64> %26, %broadcast.splat82
  %28 = trunc nuw <2 x i64> %27 to <2 x i32>
  %29 = uitofp nneg <2 x i32> %28 to <2 x double>
  %30 = fdiv <2 x double> %29, %broadcast.splat84
  %31 = getelementptr inbounds nuw double, ptr %25, i64 %index86
  store <2 x double> %30, ptr %31, align 8
  %index.next88 = add nuw i64 %index86, 2
  %vec.ind.next89 = add <2 x i64> %vec.ind87, splat (i64 2)
  %32 = icmp eq i64 %index.next88, %n.vec80
  br i1 %32, label %middle.block90, label %vector.body85, !llvm.loop !14

middle.block90:                                   ; preds = %vector.body85
  br i1 %cmp.n91, label %._crit_edge.us, label %scalar.ph76.preheader

scalar.ph76.preheader:                            ; preds = %.preheader.us, %middle.block90
  %indvars.iv51.ph = phi i64 [ 0, %.preheader.us ], [ %n.vec80, %middle.block90 ]
  br label %scalar.ph76

scalar.ph76:                                      ; preds = %scalar.ph76.preheader, %scalar.ph76
  %indvars.iv51 = phi i64 [ %indvars.iv.next52, %scalar.ph76 ], [ %indvars.iv51.ph, %scalar.ph76.preheader ]
  %indvars.iv.next52 = add nuw nsw i64 %indvars.iv51, 1
  %33 = mul nuw nsw i64 %indvars.iv.next52, %indvars.iv56
  %34 = trunc nuw i64 %33 to i32
  %35 = uitofp nneg i32 %34 to double
  %36 = fdiv double %35, %23
  %37 = getelementptr inbounds nuw double, ptr %25, i64 %indvars.iv51
  store double %36, ptr %37, align 8
  %exitcond55.not = icmp eq i64 %indvars.iv.next52, %6
  br i1 %exitcond55.not, label %._crit_edge.us, label %scalar.ph76, !llvm.loop !15

._crit_edge.us:                                   ; preds = %scalar.ph76, %middle.block90
  %indvars.iv.next57 = add nuw nsw i64 %indvars.iv56, 1
  %exitcond60.not = icmp eq i64 %indvars.iv.next57, %wide.trip.count59
  br i1 %exitcond60.not, label %._crit_edge43, label %.preheader.us, !llvm.loop !16

scalar.ph61:                                      ; preds = %scalar.ph61.preheader, %scalar.ph61
  %indvars.iv46 = phi i64 [ %indvars.iv.next47, %scalar.ph61 ], [ %indvars.iv46.ph, %scalar.ph61.preheader ]
  %38 = trunc nuw nsw i64 %indvars.iv46 to i32
  %39 = uitofp nneg i32 %38 to double
  %40 = fdiv double %39, %14
  %41 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv46
  store double %40, ptr %41, align 8
  %indvars.iv.next47 = add nuw nsw i64 %indvars.iv46, 1
  %exitcond50.not = icmp eq i64 %indvars.iv.next47, %wide.trip.count49
  br i1 %exitcond50.not, label %.preheader.lr.ph, label %scalar.ph61, !llvm.loop !17

._crit_edge43:                                    ; preds = %._crit_edge.us, %.preheader.lr.ph, %.preheader36
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @bicg(i32 noundef %0, i32 noundef %1, ptr noundef readonly captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4, ptr noundef readonly captures(none) %5, ptr noundef readonly captures(none) %6) local_unnamed_addr #1 {
  %8 = zext i32 %1 to i64
  %9 = icmp sgt i32 %1, 0
  br i1 %9, label %.preheader, label %.preheader.thread

.preheader:                                       ; preds = %7
  %10 = shl nuw nsw i64 %8, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %3, i8 0, i64 %10, i1 false)
  %11 = icmp sgt i32 %0, 0
  br i1 %11, label %.lr.ph37.us.preheader, label %._crit_edge40

.preheader.thread:                                ; preds = %7
  %12 = icmp sgt i32 %0, 0
  br i1 %12, label %.lr.ph39.split.preheader, label %._crit_edge40

.lr.ph39.split.preheader:                         ; preds = %.preheader.thread
  %13 = zext nneg i32 %0 to i64
  %14 = shl nuw nsw i64 %13, 3
  tail call void @llvm.memset.p0.i64(ptr align 8 %4, i8 0, i64 %14, i1 false)
  br label %._crit_edge40

.lr.ph37.us.preheader:                            ; preds = %.preheader
  %wide.trip.count48 = zext nneg i32 %0 to i64
  br label %.lr.ph37.us

.lr.ph37.us:                                      ; preds = %.lr.ph37.us.preheader, %._crit_edge.us
  %indvars.iv45 = phi i64 [ 0, %.lr.ph37.us.preheader ], [ %indvars.iv.next46, %._crit_edge.us ]
  %15 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv45
  store double 0.000000e+00, ptr %15, align 8
  %16 = getelementptr inbounds nuw double, ptr %6, i64 %indvars.iv45
  %17 = mul nuw nsw i64 %indvars.iv45, %8
  %18 = getelementptr inbounds nuw double, ptr %2, i64 %17
  br label %19

19:                                               ; preds = %.lr.ph37.us, %19
  %indvars.iv = phi i64 [ 0, %.lr.ph37.us ], [ %indvars.iv.next, %19 ]
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
  %exitcond.not = icmp eq i64 %indvars.iv.next, %8
  br i1 %exitcond.not, label %._crit_edge.us, label %19, !llvm.loop !18

._crit_edge.us:                                   ; preds = %19
  %indvars.iv.next46 = add nuw nsw i64 %indvars.iv45, 1
  %exitcond49.not = icmp eq i64 %indvars.iv.next46, %wide.trip.count48
  br i1 %exitcond49.not, label %._crit_edge40, label %.lr.ph37.us, !llvm.loop !19

._crit_edge40:                                    ; preds = %._crit_edge.us, %.preheader.thread, %.lr.ph39.split.preheader, %.preheader
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
!14 = distinct !{!14, !9, !10, !11}
!15 = distinct !{!15, !9, !11, !10}
!16 = distinct !{!16, !9}
!17 = distinct !{!17, !9, !11, !10}
!18 = distinct !{!18, !9}
!19 = distinct !{!19, !9}
