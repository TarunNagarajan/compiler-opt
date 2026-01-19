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
  %6 = icmp sgt i32 %1, 2
  %or.cond = and i1 %5, %6
  br i1 %or.cond, label %.preheader29.us.us.preheader, label %._crit_edge34

.preheader29.us.us.preheader:                     ; preds = %4
  %7 = add nsw i32 %1, -1
  %wide.trip.count = zext i32 %7 to i64
  %scevgep = getelementptr i8, ptr %2, i64 8
  %8 = shl nuw nsw i64 %wide.trip.count, 3
  %scevgep48 = getelementptr i8, ptr %2, i64 %8
  %9 = getelementptr i8, ptr %3, i64 %8
  %scevgep49 = getelementptr i8, ptr %9, i64 8
  %10 = add nsw i64 %wide.trip.count, -1
  %scevgep56 = getelementptr i8, ptr %3, i64 8
  %11 = shl nuw nsw i64 %wide.trip.count, 3
  %scevgep57 = getelementptr i8, ptr %3, i64 %11
  %12 = getelementptr i8, ptr %2, i64 %11
  %scevgep58 = getelementptr i8, ptr %12, i64 8
  %min.iters.check63 = icmp ult i64 %10, 4
  %bound059 = icmp ult ptr %scevgep56, %scevgep58
  %bound160 = icmp ult ptr %2, %scevgep57
  %found.conflict61 = and i1 %bound059, %bound160
  %n.vec66 = and i64 %10, -4
  %13 = or disjoint i64 %n.vec66, 1
  %cmp.n78 = icmp eq i64 %10, %n.vec66
  %14 = and i32 %1, 1
  %lcmp.mod.not = icmp eq i32 %14, 0
  %15 = add nsw i64 %wide.trip.count, -1
  %min.iters.check = icmp ult i64 %10, 4
  %bound0 = icmp ult ptr %scevgep, %scevgep49
  %bound1 = icmp ult ptr %3, %scevgep48
  %found.conflict = and i1 %bound0, %bound1
  %n.vec = and i64 %10, -4
  %16 = or disjoint i64 %n.vec, 1
  %cmp.n = icmp eq i64 %10, %n.vec
  %17 = and i32 %1, 1
  %lcmp.mod82.not = icmp eq i32 %17, 0
  %18 = add nsw i64 %wide.trip.count, -1
  br label %.preheader29.us.us

.preheader29.us.us:                               ; preds = %.preheader29.us.us.preheader, %._crit_edge.us.us
  %.02733.us.us = phi i32 [ %113, %._crit_edge.us.us ], [ 0, %.preheader29.us.us.preheader ]
  %brmerge = select i1 %min.iters.check63, i1 true, i1 %found.conflict61
  br i1 %brmerge, label %scalar.ph62.preheader, label %vector.body67

vector.body67:                                    ; preds = %.preheader29.us.us, %vector.body67
  %index68 = phi i64 [ %index.next76, %vector.body67 ], [ 0, %.preheader29.us.us ]
  %offset.idx69 = or disjoint i64 %index68, 1
  %19 = getelementptr double, ptr %2, i64 %offset.idx69
  %20 = getelementptr i8, ptr %19, i64 -8
  %21 = getelementptr i8, ptr %19, i64 8
  %wide.load70 = load <2 x double>, ptr %20, align 8, !alias.scope !13
  %wide.load71 = load <2 x double>, ptr %21, align 8, !alias.scope !13
  %22 = getelementptr i8, ptr %19, i64 16
  %wide.load72 = load <2 x double>, ptr %19, align 8, !alias.scope !13
  %wide.load73 = load <2 x double>, ptr %22, align 8, !alias.scope !13
  %23 = fadd <2 x double> %wide.load70, %wide.load72
  %24 = fadd <2 x double> %wide.load71, %wide.load73
  %25 = getelementptr inbounds nuw double, ptr %2, i64 %index68
  %26 = getelementptr inbounds nuw i8, ptr %25, i64 16
  %27 = getelementptr inbounds nuw i8, ptr %25, i64 32
  %wide.load74 = load <2 x double>, ptr %26, align 8, !alias.scope !13
  %wide.load75 = load <2 x double>, ptr %27, align 8, !alias.scope !13
  %28 = fadd <2 x double> %23, %wide.load74
  %29 = fadd <2 x double> %24, %wide.load75
  %30 = fmul <2 x double> %28, splat (double 3.333300e-01)
  %31 = fmul <2 x double> %29, splat (double 3.333300e-01)
  %32 = getelementptr inbounds nuw double, ptr %3, i64 %offset.idx69
  %33 = getelementptr inbounds nuw i8, ptr %32, i64 16
  store <2 x double> %30, ptr %32, align 8, !alias.scope !16, !noalias !13
  store <2 x double> %31, ptr %33, align 8, !alias.scope !16, !noalias !13
  %index.next76 = add nuw i64 %index68, 4
  %34 = icmp eq i64 %index.next76, %n.vec66
  br i1 %34, label %middle.block77, label %vector.body67, !llvm.loop !18

middle.block77:                                   ; preds = %vector.body67
  br i1 %cmp.n78, label %..preheader_crit_edge.us.us.preheader, label %scalar.ph62.preheader

scalar.ph62.preheader:                            ; preds = %.preheader29.us.us, %middle.block77
  %indvars.iv.ph = phi i64 [ 1, %.preheader29.us.us ], [ %13, %middle.block77 ]
  br i1 %lcmp.mod.not, label %scalar.ph62.prol.loopexit, label %scalar.ph62.prol

scalar.ph62.prol:                                 ; preds = %scalar.ph62.preheader
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
  br label %scalar.ph62.prol.loopexit

scalar.ph62.prol.loopexit:                        ; preds = %scalar.ph62.prol, %scalar.ph62.preheader
  %indvars.iv.unr = phi i64 [ %indvars.iv.ph, %scalar.ph62.preheader ], [ %indvars.iv.next.prol, %scalar.ph62.prol ]
  %45 = icmp eq i64 %indvars.iv.ph, %15
  br i1 %45, label %..preheader_crit_edge.us.us.preheader, label %scalar.ph62

..preheader_crit_edge.us.us:                      ; preds = %..preheader_crit_edge.us.us.prol.loopexit, %..preheader_crit_edge.us.us
  %indvars.iv42 = phi i64 [ %indvars.iv.next43.1, %..preheader_crit_edge.us.us ], [ %indvars.iv42.unr, %..preheader_crit_edge.us.us.prol.loopexit ]
  %46 = getelementptr double, ptr %3, i64 %indvars.iv42
  %47 = getelementptr i8, ptr %46, i64 -8
  %48 = load double, ptr %47, align 8
  %49 = load double, ptr %46, align 8
  %50 = fadd double %48, %49
  %indvars.iv.next43 = add nuw nsw i64 %indvars.iv42, 1
  %51 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next43
  %52 = load double, ptr %51, align 8
  %53 = fadd double %50, %52
  %54 = fmul double %53, 3.333300e-01
  %55 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv42
  store double %54, ptr %55, align 8
  %56 = getelementptr double, ptr %3, i64 %indvars.iv.next43
  %57 = getelementptr i8, ptr %56, i64 -8
  %58 = load double, ptr %57, align 8
  %59 = load double, ptr %56, align 8
  %60 = fadd double %58, %59
  %indvars.iv.next43.1 = add nuw nsw i64 %indvars.iv42, 2
  %61 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next43.1
  %62 = load double, ptr %61, align 8
  %63 = fadd double %60, %62
  %64 = fmul double %63, 3.333300e-01
  %65 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next43
  store double %64, ptr %65, align 8
  %exitcond46.not.1 = icmp eq i64 %indvars.iv.next43.1, %wide.trip.count
  br i1 %exitcond46.not.1, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us, !llvm.loop !19

scalar.ph62:                                      ; preds = %scalar.ph62.prol.loopexit, %scalar.ph62
  %indvars.iv = phi i64 [ %indvars.iv.next.1, %scalar.ph62 ], [ %indvars.iv.unr, %scalar.ph62.prol.loopexit ]
  %66 = getelementptr double, ptr %2, i64 %indvars.iv
  %67 = getelementptr i8, ptr %66, i64 -8
  %68 = load double, ptr %67, align 8
  %69 = load double, ptr %66, align 8
  %70 = fadd double %68, %69
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %71 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next
  %72 = load double, ptr %71, align 8
  %73 = fadd double %70, %72
  %74 = fmul double %73, 3.333300e-01
  %75 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv
  store double %74, ptr %75, align 8
  %76 = getelementptr double, ptr %2, i64 %indvars.iv.next
  %77 = getelementptr i8, ptr %76, i64 -8
  %78 = load double, ptr %77, align 8
  %79 = load double, ptr %76, align 8
  %80 = fadd double %78, %79
  %indvars.iv.next.1 = add nuw nsw i64 %indvars.iv, 2
  %81 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv.next.1
  %82 = load double, ptr %81, align 8
  %83 = fadd double %80, %82
  %84 = fmul double %83, 3.333300e-01
  %85 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next
  store double %84, ptr %85, align 8
  %exitcond.not.1 = icmp eq i64 %indvars.iv.next.1, %wide.trip.count
  br i1 %exitcond.not.1, label %..preheader_crit_edge.us.us.preheader, label %scalar.ph62, !llvm.loop !20

..preheader_crit_edge.us.us.preheader:            ; preds = %scalar.ph62.prol.loopexit, %scalar.ph62, %middle.block77
  %brmerge83 = select i1 %min.iters.check, i1 true, i1 %found.conflict
  br i1 %brmerge83, label %..preheader_crit_edge.us.us.preheader80, label %vector.body

vector.body:                                      ; preds = %..preheader_crit_edge.us.us.preheader, %vector.body
  %index = phi i64 [ %index.next, %vector.body ], [ 0, %..preheader_crit_edge.us.us.preheader ]
  %offset.idx = or disjoint i64 %index, 1
  %86 = getelementptr double, ptr %3, i64 %offset.idx
  %87 = getelementptr i8, ptr %86, i64 -8
  %88 = getelementptr i8, ptr %86, i64 8
  %wide.load = load <2 x double>, ptr %87, align 8, !alias.scope !21
  %wide.load50 = load <2 x double>, ptr %88, align 8, !alias.scope !21
  %89 = getelementptr i8, ptr %86, i64 16
  %wide.load51 = load <2 x double>, ptr %86, align 8, !alias.scope !21
  %wide.load52 = load <2 x double>, ptr %89, align 8, !alias.scope !21
  %90 = fadd <2 x double> %wide.load, %wide.load51
  %91 = fadd <2 x double> %wide.load50, %wide.load52
  %92 = getelementptr inbounds nuw double, ptr %3, i64 %index
  %93 = getelementptr inbounds nuw i8, ptr %92, i64 16
  %94 = getelementptr inbounds nuw i8, ptr %92, i64 32
  %wide.load53 = load <2 x double>, ptr %93, align 8, !alias.scope !21
  %wide.load54 = load <2 x double>, ptr %94, align 8, !alias.scope !21
  %95 = fadd <2 x double> %90, %wide.load53
  %96 = fadd <2 x double> %91, %wide.load54
  %97 = fmul <2 x double> %95, splat (double 3.333300e-01)
  %98 = fmul <2 x double> %96, splat (double 3.333300e-01)
  %99 = getelementptr inbounds nuw double, ptr %2, i64 %offset.idx
  %100 = getelementptr inbounds nuw i8, ptr %99, i64 16
  store <2 x double> %97, ptr %99, align 8, !alias.scope !24, !noalias !21
  store <2 x double> %98, ptr %100, align 8, !alias.scope !24, !noalias !21
  %index.next = add nuw i64 %index, 4
  %101 = icmp eq i64 %index.next, %n.vec
  br i1 %101, label %middle.block, label %vector.body, !llvm.loop !26

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us.preheader80

..preheader_crit_edge.us.us.preheader80:          ; preds = %..preheader_crit_edge.us.us.preheader, %middle.block
  %indvars.iv42.ph = phi i64 [ 1, %..preheader_crit_edge.us.us.preheader ], [ %16, %middle.block ]
  br i1 %lcmp.mod82.not, label %..preheader_crit_edge.us.us.prol.loopexit, label %..preheader_crit_edge.us.us.prol

..preheader_crit_edge.us.us.prol:                 ; preds = %..preheader_crit_edge.us.us.preheader80
  %102 = getelementptr double, ptr %3, i64 %indvars.iv42.ph
  %103 = getelementptr i8, ptr %102, i64 -8
  %104 = load double, ptr %103, align 8
  %105 = load double, ptr %102, align 8
  %106 = fadd double %104, %105
  %indvars.iv.next43.prol = add nuw nsw i64 %indvars.iv42.ph, 1
  %107 = getelementptr inbounds nuw double, ptr %3, i64 %indvars.iv.next43.prol
  %108 = load double, ptr %107, align 8
  %109 = fadd double %106, %108
  %110 = fmul double %109, 3.333300e-01
  %111 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv42.ph
  store double %110, ptr %111, align 8
  br label %..preheader_crit_edge.us.us.prol.loopexit

..preheader_crit_edge.us.us.prol.loopexit:        ; preds = %..preheader_crit_edge.us.us.prol, %..preheader_crit_edge.us.us.preheader80
  %indvars.iv42.unr = phi i64 [ %indvars.iv42.ph, %..preheader_crit_edge.us.us.preheader80 ], [ %indvars.iv.next43.prol, %..preheader_crit_edge.us.us.prol ]
  %112 = icmp eq i64 %indvars.iv42.ph, %18
  br i1 %112, label %._crit_edge.us.us, label %..preheader_crit_edge.us.us

._crit_edge.us.us:                                ; preds = %..preheader_crit_edge.us.us.prol.loopexit, %..preheader_crit_edge.us.us, %middle.block
  %113 = add nuw nsw i32 %.02733.us.us, 1
  %exitcond47.not = icmp eq i32 %113, %0
  br i1 %exitcond47.not, label %._crit_edge34, label %.preheader29.us.us, !llvm.loop !27

._crit_edge34:                                    ; preds = %._crit_edge.us.us, %4
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
!20 = distinct !{!20, !9, !10}
!21 = !{!22}
!22 = distinct !{!22, !23}
!23 = distinct !{!23, !"LVerDomain"}
!24 = !{!25}
!25 = distinct !{!25, !23}
!26 = distinct !{!26, !9, !10, !11}
!27 = distinct !{!27, !9}
