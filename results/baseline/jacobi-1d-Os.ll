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
  %5 = ptrtoint ptr %2 to i64
  %6 = ptrtoint ptr %1 to i64
  %7 = uitofp nneg i32 %0 to double
  %wide.trip.count = zext nneg i32 %0 to i64
  %min.iters.check = icmp eq i32 %0, 1
  %8 = sub i64 %5, %6
  %diff.check = icmp ult i64 %8, 16
  %or.cond = or i1 %min.iters.check, %diff.check
  br i1 %or.cond, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %n.vec = and i64 %wide.trip.count, 2147483646
  %broadcast.splatinsert = insertelement <2 x double> poison, double %7, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %vec.ind15 = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next16, %vector.body ]
  %9 = add <2 x i32> %vec.ind, splat (i32 2)
  %10 = uitofp <2 x i32> %9 to <2 x double>
  %11 = fdiv <2 x double> %10, %broadcast.splat
  %12 = getelementptr inbounds nuw double, ptr %1, i64 %index
  store <2 x double> %11, ptr %12, align 8
  %13 = add <2 x i32> %vec.ind15, splat (i32 3)
  %14 = uitofp <2 x i32> %13 to <2 x double>
  %15 = fdiv <2 x double> %14, %broadcast.splat
  %16 = getelementptr inbounds nuw double, ptr %2, i64 %index
  store <2 x double> %15, ptr %16, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %vec.ind.next16 = add <2 x i32> %vec.ind15, splat (i32 2)
  %17 = icmp eq i64 %index.next, %n.vec
  br i1 %17, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  %cmp.n = icmp eq i64 %n.vec, %wide.trip.count
  br i1 %cmp.n, label %._crit_edge, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  %xtraiter = and i64 %wide.trip.count, 1
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %scalar.ph.prol.loopexit, label %scalar.ph.prol

scalar.ph.prol:                                   ; preds = %scalar.ph.preheader
  %18 = trunc nuw nsw i64 %indvars.iv.ph to i32
  %19 = add nuw i32 %18, 2
  %20 = uitofp i32 %19 to double
  %21 = fdiv double %20, %7
  %22 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv.ph
  store double %21, ptr %22, align 8
  %23 = trunc nuw nsw i64 %indvars.iv.ph to i32
  %24 = add nuw i32 %23, 3
  %25 = uitofp i32 %24 to double
  %26 = fdiv double %25, %7
  %27 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.ph
  store double %26, ptr %27, align 8
  %indvars.iv.next.prol = or disjoint i64 %indvars.iv.ph, 1
  br label %scalar.ph.prol.loopexit

scalar.ph.prol.loopexit:                          ; preds = %scalar.ph.prol, %scalar.ph.preheader
  %indvars.iv.unr = phi i64 [ %indvars.iv.ph, %scalar.ph.preheader ], [ %indvars.iv.next.prol, %scalar.ph.prol ]
  %28 = add nsw i64 %wide.trip.count, -1
  %29 = icmp eq i64 %indvars.iv.ph, %28
  br i1 %29, label %._crit_edge, label %scalar.ph

scalar.ph:                                        ; preds = %scalar.ph.prol.loopexit, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %scalar.ph ], [ %indvars.iv.unr, %scalar.ph.prol.loopexit ]
  %30 = trunc i64 %indvars.iv to i32
  %31 = add i32 %30, 2
  %32 = uitofp i32 %31 to double
  %33 = fdiv double %32, %7
  %34 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv
  store double %33, ptr %34, align 8
  %35 = trunc i64 %indvars.iv to i32
  %36 = add i32 %35, 3
  %37 = uitofp i32 %36 to double
  %38 = fdiv double %37, %7
  %39 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv
  store double %38, ptr %39, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %40 = trunc i64 %indvars.iv.next to i32
  %41 = add i32 %40, 2
  %42 = uitofp i32 %41 to double
  %43 = fdiv double %42, %7
  %44 = getelementptr inbounds nuw double, ptr %1, i64 %indvars.iv.next
  store double %43, ptr %44, align 8
  %45 = trunc i64 %indvars.iv.next to i32
  %46 = add i32 %45, 3
  %47 = uitofp i32 %46 to double
  %48 = fdiv double %47, %7
  %49 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next
  store double %48, ptr %49, align 8
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %exitcond.not.1 = icmp eq i64 %indvars.iv.next.1, %wide.trip.count
  br i1 %exitcond.not.1, label %._crit_edge, label %scalar.ph, !llvm.loop !12

._crit_edge:                                      ; preds = %scalar.ph.prol.loopexit, %scalar.ph, %middle.block, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: readwrite) uwtable
define dso_local void @jacobi_1d(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3) local_unnamed_addr #1 {
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader29.lr.ph, label %._crit_edge34

.preheader29.lr.ph:                               ; preds = %4
  %6 = add i32 %1, -1
  %7 = icmp sgt i32 %1, 2
  %wide.trip.count = zext i32 %6 to i64
  %wide.trip.count39 = zext nneg i32 %6 to i64
  %scevgep = getelementptr i8, ptr %2, i64 8
  %8 = shl nuw nsw i64 %wide.trip.count, 3
  %scevgep42 = getelementptr i8, ptr %2, i64 %8
  %9 = getelementptr i8, ptr %3, i64 %8
  %scevgep43 = getelementptr i8, ptr %9, i64 8
  %10 = add nsw i64 %wide.trip.count, -1
  %scevgep50 = getelementptr i8, ptr %3, i64 8
  %11 = shl nuw nsw i64 %wide.trip.count, 3
  %scevgep51 = getelementptr i8, ptr %3, i64 %11
  %12 = getelementptr i8, ptr %2, i64 %11
  %scevgep52 = getelementptr i8, ptr %12, i64 8
  %min.iters.check57 = icmp ult i64 %10, 4
  %bound053 = icmp ult ptr %scevgep50, %scevgep52
  %bound154 = icmp ult ptr %2, %scevgep51
  %found.conflict55 = and i1 %bound053, %bound154
  %n.vec60 = and i64 %10, -4
  %13 = or disjoint i64 %n.vec60, 1
  %cmp.n72 = icmp eq i64 %10, %n.vec60
  %14 = and i32 %1, 1
  %lcmp.mod.not = icmp eq i32 %14, 0
  %15 = add nsw i64 %wide.trip.count, -1
  %min.iters.check = icmp ult i64 %10, 4
  %bound0 = icmp ult ptr %scevgep, %scevgep43
  %bound1 = icmp ult ptr %3, %scevgep42
  %found.conflict = and i1 %bound0, %bound1
  %n.vec = and i64 %10, -4
  %16 = or disjoint i64 %n.vec, 1
  %cmp.n = icmp eq i64 %10, %n.vec
  %17 = and i32 %1, 1
  %lcmp.mod77.not = icmp eq i32 %17, 0
  %18 = add nsw i64 %wide.trip.count, -1
  br label %.preheader29

.preheader29:                                     ; preds = %.preheader29.lr.ph, %._crit_edge
  %.02733 = phi i32 [ 0, %.preheader29.lr.ph ], [ %113, %._crit_edge ]
  br i1 %7, label %.lr.ph.preheader, label %._crit_edge

.lr.ph.preheader:                                 ; preds = %.preheader29
  %brmerge = select i1 %min.iters.check57, i1 true, i1 %found.conflict55
  br i1 %brmerge, label %.lr.ph.preheader75, label %vector.body61

vector.body61:                                    ; preds = %.lr.ph.preheader, %vector.body61
  %index62 = phi i64 [ %index.next70, %vector.body61 ], [ 0, %.lr.ph.preheader ]
  %offset.idx63 = or disjoint i64 %index62, 1
  %19 = getelementptr double, ptr %2, i64 %offset.idx63
  %20 = getelementptr i8, ptr %19, i64 -8
  %21 = getelementptr i8, ptr %19, i64 8
  %wide.load64 = load <2 x double>, ptr %20, align 8, !alias.scope !13
  %wide.load65 = load <2 x double>, ptr %21, align 8, !alias.scope !13
  %22 = getelementptr i8, ptr %19, i64 16
  %wide.load66 = load <2 x double>, ptr %19, align 8, !alias.scope !13
  %wide.load67 = load <2 x double>, ptr %22, align 8, !alias.scope !13
  %23 = fadd <2 x double> %wide.load64, %wide.load66
  %24 = fadd <2 x double> %wide.load65, %wide.load67
  %25 = getelementptr inbounds nuw double, ptr %2, i64 %index62
  %26 = getelementptr inbounds nuw i8, ptr %25, i64 16
  %27 = getelementptr inbounds nuw i8, ptr %25, i64 32
  %wide.load68 = load <2 x double>, ptr %26, align 8, !alias.scope !13
  %wide.load69 = load <2 x double>, ptr %27, align 8, !alias.scope !13
  %28 = fadd <2 x double> %23, %wide.load68
  %29 = fadd <2 x double> %24, %wide.load69
  %30 = fmul <2 x double> %28, splat (double 3.333300e-01)
  %31 = fmul <2 x double> %29, splat (double 3.333300e-01)
  %32 = getelementptr inbounds nuw double, ptr %3, i64 %offset.idx63
  %33 = getelementptr inbounds nuw i8, ptr %32, i64 16
  store <2 x double> %30, ptr %32, align 8, !alias.scope !16, !noalias !13
  store <2 x double> %31, ptr %33, align 8, !alias.scope !16, !noalias !13
  %index.next70 = add nuw i64 %index62, 4
  %34 = icmp eq i64 %index.next70, %n.vec60
  br i1 %34, label %middle.block71, label %vector.body61, !llvm.loop !18

middle.block71:                                   ; preds = %vector.body61
  br i1 %cmp.n72, label %.lr.ph32.preheader, label %.lr.ph.preheader75

.lr.ph.preheader75:                               ; preds = %.lr.ph.preheader, %middle.block71
  %indvars.iv.ph = phi i64 [ 1, %.lr.ph.preheader ], [ %13, %middle.block71 ]
  br i1 %lcmp.mod.not, label %.lr.ph.prol.loopexit, label %.lr.ph.prol

.lr.ph.prol:                                      ; preds = %.lr.ph.preheader75
  %35 = getelementptr double, ptr %2, i64 %indvars.iv.ph
  %36 = getelementptr i8, ptr %35, i64 -8
  %37 = load double, ptr %36, align 8
  %38 = load double, ptr %35, align 8
  %39 = fadd double %37, %38
  %indvars.iv.next.prol = add nuw nsw i64 %indvars.iv.ph, 1
  %40 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next.prol
  %41 = load double, ptr %40, align 8
  %42 = fadd double %39, %41
  %43 = fmul double %42, 3.333300e-01
  %44 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.ph
  store double %43, ptr %44, align 8
  br label %.lr.ph.prol.loopexit

.lr.ph.prol.loopexit:                             ; preds = %.lr.ph.prol, %.lr.ph.preheader75
  %indvars.iv.unr = phi i64 [ %indvars.iv.ph, %.lr.ph.preheader75 ], [ %indvars.iv.next.prol, %.lr.ph.prol ]
  %45 = icmp eq i64 %indvars.iv.ph, %15
  br i1 %45, label %.lr.ph32.preheader, label %.lr.ph

.lr.ph:                                           ; preds = %.lr.ph.prol.loopexit, %.lr.ph
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %.lr.ph ], [ %indvars.iv.unr, %.lr.ph.prol.loopexit ]
  %46 = getelementptr double, ptr %2, i64 %indvars.iv
  %47 = getelementptr i8, ptr %46, i64 -8
  %48 = load double, ptr %47, align 8
  %49 = load double, ptr %46, align 8
  %50 = fadd double %48, %49
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %51 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next
  %52 = load double, ptr %51, align 8
  %53 = fadd double %50, %52
  %54 = fmul double %53, 3.333300e-01
  %55 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %54, ptr %55, align 8
  %56 = getelementptr double, ptr %2, i64 %indvars.iv.next
  %57 = getelementptr i8, ptr %56, i64 -8
  %58 = load double, ptr %57, align 8
  %59 = load double, ptr %56, align 8
  %60 = fadd double %58, %59
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %61 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next.1
  %62 = load double, ptr %61, align 8
  %63 = fadd double %60, %62
  %64 = fmul double %63, 3.333300e-01
  %65 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  store double %64, ptr %65, align 8
  %exitcond.not.1 = icmp eq i64 %indvars.iv.next.1, %wide.trip.count
  br i1 %exitcond.not.1, label %.lr.ph32.preheader, label %.lr.ph, !llvm.loop !19

.lr.ph32.preheader:                               ; preds = %.lr.ph.prol.loopexit, %.lr.ph, %middle.block71
  %brmerge78 = select i1 %min.iters.check, i1 true, i1 %found.conflict
  br i1 %brmerge78, label %.lr.ph32.preheader74, label %vector.body

vector.body:                                      ; preds = %.lr.ph32.preheader, %vector.body
  %index = phi i64 [ %index.next, %vector.body ], [ 0, %.lr.ph32.preheader ]
  %offset.idx = or disjoint i64 %index, 1
  %66 = getelementptr double, ptr %3, i64 %offset.idx
  %67 = getelementptr i8, ptr %66, i64 -8
  %68 = getelementptr i8, ptr %66, i64 8
  %wide.load = load <2 x double>, ptr %67, align 8, !alias.scope !20
  %wide.load44 = load <2 x double>, ptr %68, align 8, !alias.scope !20
  %69 = getelementptr i8, ptr %66, i64 16
  %wide.load45 = load <2 x double>, ptr %66, align 8, !alias.scope !20
  %wide.load46 = load <2 x double>, ptr %69, align 8, !alias.scope !20
  %70 = fadd <2 x double> %wide.load, %wide.load45
  %71 = fadd <2 x double> %wide.load44, %wide.load46
  %72 = getelementptr inbounds nuw double, ptr %3, i64 %index
  %73 = getelementptr inbounds nuw i8, ptr %72, i64 16
  %74 = getelementptr inbounds nuw i8, ptr %72, i64 32
  %wide.load47 = load <2 x double>, ptr %73, align 8, !alias.scope !20
  %wide.load48 = load <2 x double>, ptr %74, align 8, !alias.scope !20
  %75 = fadd <2 x double> %70, %wide.load47
  %76 = fadd <2 x double> %71, %wide.load48
  %77 = fmul <2 x double> %75, splat (double 3.333300e-01)
  %78 = fmul <2 x double> %76, splat (double 3.333300e-01)
  %79 = getelementptr inbounds nuw double, ptr %2, i64 %offset.idx
  %80 = getelementptr inbounds nuw i8, ptr %79, i64 16
  store <2 x double> %77, ptr %79, align 8, !alias.scope !23, !noalias !20
  store <2 x double> %78, ptr %80, align 8, !alias.scope !23, !noalias !20
  %index.next = add nuw i64 %index, 4
  %81 = icmp eq i64 %index.next, %n.vec
  br i1 %81, label %middle.block, label %vector.body, !llvm.loop !25

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge, label %.lr.ph32.preheader74

.lr.ph32.preheader74:                             ; preds = %.lr.ph32.preheader, %middle.block
  %indvars.iv36.ph = phi i64 [ 1, %.lr.ph32.preheader ], [ %16, %middle.block ]
  br i1 %lcmp.mod77.not, label %.lr.ph32.prol.loopexit, label %.lr.ph32.prol

.lr.ph32.prol:                                    ; preds = %.lr.ph32.preheader74
  %82 = getelementptr double, ptr %3, i64 %indvars.iv36.ph
  %83 = getelementptr i8, ptr %82, i64 -8
  %84 = load double, ptr %83, align 8
  %85 = load double, ptr %82, align 8
  %86 = fadd double %84, %85
  %indvars.iv.next37.prol = add nuw nsw i64 %indvars.iv36.ph, 1
  %87 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next37.prol
  %88 = load double, ptr %87, align 8
  %89 = fadd double %86, %88
  %90 = fmul double %89, 3.333300e-01
  %91 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv36.ph
  store double %90, ptr %91, align 8
  br label %.lr.ph32.prol.loopexit

.lr.ph32.prol.loopexit:                           ; preds = %.lr.ph32.prol, %.lr.ph32.preheader74
  %indvars.iv36.unr = phi i64 [ %indvars.iv36.ph, %.lr.ph32.preheader74 ], [ %indvars.iv.next37.prol, %.lr.ph32.prol ]
  %92 = icmp eq i64 %indvars.iv36.ph, %18
  br i1 %92, label %._crit_edge, label %.lr.ph32

.lr.ph32:                                         ; preds = %.lr.ph32.prol.loopexit, %.lr.ph32
  %indvars.iv36 = phi i64 [ %indvars.iv.next37.1, %.lr.ph32 ], [ %indvars.iv36.unr, %.lr.ph32.prol.loopexit ]
  %93 = getelementptr double, ptr %3, i64 %indvars.iv36
  %94 = getelementptr i8, ptr %93, i64 -8
  %95 = load double, ptr %94, align 8
  %96 = load double, ptr %93, align 8
  %97 = fadd double %95, %96
  %indvars.iv.next37 = add nuw nsw i64 %indvars.iv36, 1
  %98 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next37
  %99 = load double, ptr %98, align 8
  %100 = fadd double %97, %99
  %101 = fmul double %100, 3.333300e-01
  %102 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv36
  store double %101, ptr %102, align 8
  %103 = getelementptr double, ptr %3, i64 %indvars.iv.next37
  %104 = getelementptr i8, ptr %103, i64 -8
  %105 = load double, ptr %104, align 8
  %106 = load double, ptr %103, align 8
  %107 = fadd double %105, %106
  %indvars.iv.next37.1 = add nuw nsw i64 %indvars.iv36, 2
  %108 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next37.1
  %109 = load double, ptr %108, align 8
  %110 = fadd double %107, %109
  %111 = fmul double %110, 3.333300e-01
  %112 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next37
  store double %111, ptr %112, align 8
  %exitcond40.not.1 = icmp eq i64 %indvars.iv.next37.1, %wide.trip.count39
  br i1 %exitcond40.not.1, label %._crit_edge, label %.lr.ph32, !llvm.loop !26

._crit_edge:                                      ; preds = %.lr.ph32.prol.loopexit, %.lr.ph32, %middle.block, %.preheader29
  %113 = add nuw nsw i32 %.02733, 1
  %exitcond41.not = icmp eq i32 %113, %0
  br i1 %exitcond41.not, label %._crit_edge34, label %.preheader29, !llvm.loop !27

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
!8 = distinct !{!8, !9, !10, !11}
!9 = !{!"llvm.loop.mustprogress"}
!10 = !{!"llvm.loop.isvectorized", i32 1}
!11 = !{!"llvm.loop.unroll.runtime.disable"}
!12 = distinct !{!12, !9, !10}
!13 = !{!14}
!14 = distinct !{!14, !15}
!15 = distinct !{!15, !"LVerDomain"}
!16 = !{!17}
!17 = distinct !{!17, !15}
!18 = distinct !{!18, !9, !10, !11}
!19 = distinct !{!19, !9, !10}
!20 = !{!21}
!21 = distinct !{!21, !22}
!22 = distinct !{!22, !"LVerDomain"}
!23 = !{!24}
!24 = distinct !{!24, !22}
!25 = distinct !{!25, !9, !10, !11}
!26 = distinct !{!26, !9, !10}
!27 = distinct !{!27, !9}
