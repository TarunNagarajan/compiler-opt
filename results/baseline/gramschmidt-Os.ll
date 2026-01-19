; ModuleID = 'results\baseline\gramschmidt_base.ll'
source_filename = "benchmarks\\gramschmidt.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@.str = private unnamed_addr constant [34 x i8] c"Gramschmidt Execution Time: %f s\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Result check: %f\0A\00", align 1

; Function Attrs: nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable
define dso_local void @init_array(i32 noundef %0, i32 noundef %1, ptr noundef writeonly captures(none) %2) local_unnamed_addr #0 {
  %4 = zext i32 %1 to i64
  %5 = icmp sgt i32 %0, 0
  br i1 %5, label %.preheader.lr.ph, label %._crit_edge17

.preheader.lr.ph:                                 ; preds = %3
  %6 = icmp sgt i32 %1, 0
  %7 = uitofp nneg i32 %0 to double
  %wide.trip.count22 = zext nneg i32 %0 to i64
  %min.iters.check = icmp eq i32 %1, 1
  %n.vec = and i64 %4, 2147483646
  %broadcast.splatinsert24 = insertelement <2 x double> poison, double %7, i64 0
  %broadcast.splat25 = shufflevector <2 x double> %broadcast.splatinsert24, <2 x double> poison, <2 x i32> zeroinitializer
  %cmp.n = icmp eq i64 %n.vec, %4
  br label %.preheader

.preheader:                                       ; preds = %.preheader.lr.ph, %._crit_edge
  %indvars.iv19 = phi i64 [ 0, %.preheader.lr.ph ], [ %indvars.iv.next20, %._crit_edge ]
  br i1 %6, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader
  %8 = trunc nuw nsw i64 %indvars.iv19 to i32
  %9 = uitofp nneg i32 %8 to double
  %10 = mul nuw nsw i64 %indvars.iv19, %4
  %11 = getelementptr inbounds nuw double, ptr %2, i64 %10
  br i1 %min.iters.check, label %scalar.ph.preheader, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph
  %broadcast.splatinsert = insertelement <2 x double> poison, double %9, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.ind = phi <2 x i32> [ <i32 0, i32 1>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %12 = uitofp nneg <2 x i32> %vec.ind to <2 x double>
  %13 = fmul <2 x double> %broadcast.splat, %12
  %14 = fdiv <2 x double> %13, %broadcast.splat25
  %15 = getelementptr inbounds nuw double, ptr %11, i64 %index
  store <2 x double> %14, ptr %15, align 8
  %index.next = add nuw i64 %index, 2
  %vec.ind.next = add <2 x i32> %vec.ind, splat (i32 2)
  %16 = icmp eq i64 %index.next, %n.vec
  br i1 %16, label %middle.block, label %vector.body, !llvm.loop !8

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge, label %scalar.ph.preheader

scalar.ph.preheader:                              ; preds = %.lr.ph, %middle.block
  %indvars.iv.ph = phi i64 [ 0, %.lr.ph ], [ %n.vec, %middle.block ]
  br label %scalar.ph

scalar.ph:                                        ; preds = %scalar.ph.preheader, %scalar.ph
  %indvars.iv = phi i64 [ %indvars.iv.next, %scalar.ph ], [ %indvars.iv.ph, %scalar.ph.preheader ]
  %17 = trunc nuw nsw i64 %indvars.iv to i32
  %18 = uitofp nneg i32 %17 to double
  %19 = fmul double %9, %18
  %20 = fdiv double %19, %7
  %21 = getelementptr inbounds nuw double, ptr %11, i64 %indvars.iv
  store double %20, ptr %21, align 8
  %indvars.iv.next = add nuw nsw i64 %indvars.iv, 1
  %exitcond.not = icmp eq i64 %indvars.iv.next, %4
  br i1 %exitcond.not, label %._crit_edge, label %scalar.ph, !llvm.loop !12

._crit_edge:                                      ; preds = %scalar.ph, %middle.block, %.preheader
  %indvars.iv.next20 = add nuw nsw i64 %indvars.iv19, 1
  %exitcond23.not = icmp eq i64 %indvars.iv.next20, %wide.trip.count22
  br i1 %exitcond23.not, label %._crit_edge17, label %.preheader, !llvm.loop !13

._crit_edge17:                                    ; preds = %._crit_edge, %3
  ret void
}

; Function Attrs: nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable
define dso_local void @gramschmidt(i32 noundef %0, i32 noundef %1, ptr noundef captures(none) %2, ptr noundef captures(none) %3, ptr noundef captures(none) %4) local_unnamed_addr #1 {
  %6 = zext i32 %1 to i64
  %7 = icmp sgt i32 %1, 0
  br i1 %7, label %.preheader76.lr.ph, label %._crit_edge105

.preheader76.lr.ph:                               ; preds = %5
  %8 = icmp sgt i32 %0, 0
  %9 = zext nneg i32 %1 to i64
  %wide.trip.count = zext i32 %0 to i64
  %wide.trip.count110 = zext nneg i32 %0 to i64
  %wide.trip.count120 = zext nneg i32 %0 to i64
  %10 = shl nuw nsw i64 %6, 3
  %11 = shl nuw nsw i64 %wide.trip.count, 3
  %12 = getelementptr i8, ptr %2, i64 %10
  %13 = getelementptr i8, ptr %12, i64 %11
  %scevgep140 = getelementptr i8, ptr %13, i64 -8
  %14 = add nuw nsw i64 %6, %wide.trip.count
  %15 = shl nuw nsw i64 %14, 3
  %16 = add nsw i64 %15, -8
  %scevgep154 = getelementptr i8, ptr %4, i64 %16
  %scevgep155 = getelementptr i8, ptr %2, i64 %16
  %17 = shl nuw nsw i64 %6, 4
  %18 = getelementptr i8, ptr %3, i64 %17
  %scevgep156 = getelementptr i8, ptr %18, i64 -8
  %invariant.gep194 = getelementptr i8, ptr %2, i64 8
  %19 = getelementptr i8, ptr %4, i64 %11
  %invariant.gep196 = getelementptr i8, ptr %3, i64 8
  %20 = getelementptr i8, ptr %3, i64 %10
  %xtraiter = and i64 %wide.trip.count, 3
  %21 = icmp ult i32 %0, 4
  %unroll_iter = and i64 %wide.trip.count, 2147483644
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  %min.iters.check165 = icmp ne i32 %0, 1
  %ident.check152.not = icmp eq i32 %1, 1
  %or.cond = and i1 %min.iters.check165, %ident.check152.not
  %bound0157 = icmp ult ptr %4, %scevgep155
  %bound1158 = icmp ult ptr %2, %scevgep154
  %found.conflict159 = and i1 %bound0157, %bound1158
  %bound0160 = icmp ult ptr %4, %scevgep156
  %bound1161 = icmp ult ptr %3, %scevgep154
  %found.conflict162 = and i1 %bound0160, %bound1161
  %conflict.rdx163 = or i1 %found.conflict159, %found.conflict162
  %n.vec168 = and i64 %wide.trip.count, 2147483646
  %cmp.n176 = icmp eq i64 %n.vec168, %wide.trip.count
  %xtraiter182 = and i64 %wide.trip.count, 1
  %lcmp.mod183.not = icmp eq i64 %xtraiter182, 0
  %22 = add nsw i64 %wide.trip.count, -1
  %xtraiter184 = and i64 %wide.trip.count, 1
  %23 = icmp eq i32 %0, 1
  %unroll_iter187 = and i64 %wide.trip.count, 2147483646
  %lcmp.mod186.not = icmp eq i64 %xtraiter184, 0
  %min.iters.check = icmp ugt i32 %0, 3
  %ident.check.not = icmp eq i32 %1, 1
  %or.cond178 = and i1 %min.iters.check, %ident.check.not
  %n.vec = and i64 %wide.trip.count, 2147483644
  %cmp.n = icmp eq i64 %n.vec, %wide.trip.count
  %xtraiter189 = and i64 %wide.trip.count, 1
  %lcmp.mod190.not = icmp eq i64 %xtraiter189, 0
  %24 = add nsw i64 %wide.trip.count, -1
  br label %.preheader76

.loopexit:                                        ; preds = %._crit_edge100, %._crit_edge86
  %indvars.iv.next123 = add nuw nsw i64 %indvars.iv122, 1
  %exitcond133.not = icmp eq i64 %indvars.iv.next130, %6
  br i1 %exitcond133.not, label %._crit_edge105, label %.preheader76, !llvm.loop !14

.preheader76:                                     ; preds = %.preheader76.lr.ph, %.loopexit
  %indvars.iv129 = phi i64 [ 0, %.preheader76.lr.ph ], [ %indvars.iv.next130, %.loopexit ]
  %indvars.iv122 = phi i64 [ 1, %.preheader76.lr.ph ], [ %indvars.iv.next123, %.loopexit ]
  %25 = shl nuw nsw i64 %indvars.iv129, 3
  %gep195 = getelementptr i8, ptr %invariant.gep194, i64 %25
  %scevgep141 = getelementptr i8, ptr %4, i64 %25
  %scevgep142 = getelementptr i8, ptr %19, i64 %25
  %26 = shl nuw nsw i64 %indvars.iv129, 4
  %gep197 = getelementptr i8, ptr %invariant.gep196, i64 %26
  %scevgep144 = getelementptr i8, ptr %20, i64 %25
  br i1 %8, label %.lr.ph, label %._crit_edge

.lr.ph:                                           ; preds = %.preheader76
  %invariant.gep = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv129
  br i1 %21, label %.lr.ph85.preheader.unr-lcssa, label %.lr.ph.new

.lr.ph.new:                                       ; preds = %.lr.ph, %.lr.ph.new
  %indvars.iv = phi i64 [ %indvars.iv.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %.07277 = phi double [ %38, %.lr.ph.new ], [ 0.000000e+00, %.lr.ph ]
  %niter = phi i64 [ %niter.next.3, %.lr.ph.new ], [ 0, %.lr.ph ]
  %27 = mul nuw nsw i64 %indvars.iv, %6
  %gep = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %27
  %28 = load double, ptr %gep, align 8
  %29 = tail call double @llvm.fmuladd.f64(double %28, double %28, double %.07277)
  %indvars.iv.next = or disjoint i64 %indvars.iv, 1
  %30 = mul nuw nsw i64 %indvars.iv.next, %6
  %gep.1 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %30
  %31 = load double, ptr %gep.1, align 8
  %32 = tail call double @llvm.fmuladd.f64(double %31, double %31, double %29)
  %indvars.iv.next.1 = or disjoint i64 %indvars.iv, 2
  %33 = mul nuw nsw i64 %indvars.iv.next.1, %6
  %gep.2 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %33
  %34 = load double, ptr %gep.2, align 8
  %35 = tail call double @llvm.fmuladd.f64(double %34, double %34, double %32)
  %indvars.iv.next.2 = or disjoint i64 %indvars.iv, 3
  %36 = mul nuw nsw i64 %indvars.iv.next.2, %6
  %gep.3 = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %36
  %37 = load double, ptr %gep.3, align 8
  %38 = tail call double @llvm.fmuladd.f64(double %37, double %37, double %35)
  %indvars.iv.next.3 = add nuw nsw i64 %indvars.iv, 4
  %niter.next.3 = add i64 %niter, 4
  %niter.ncmp.3 = icmp eq i64 %niter.next.3, %unroll_iter
  br i1 %niter.ncmp.3, label %.lr.ph85.preheader.unr-lcssa, label %.lr.ph.new, !llvm.loop !15

._crit_edge:                                      ; preds = %.preheader76
  %39 = mul nuw nsw i64 %indvars.iv129, %6
  %40 = getelementptr inbounds nuw double, ptr %3, i64 %39
  %41 = getelementptr inbounds nuw double, ptr %40, i64 %indvars.iv129
  store double 0.000000e+00, ptr %41, align 8
  br label %._crit_edge86

.lr.ph85.preheader.unr-lcssa:                     ; preds = %.lr.ph.new, %.lr.ph
  %.lcssa.ph = phi double [ poison, %.lr.ph ], [ %38, %.lr.ph.new ]
  %indvars.iv.unr = phi i64 [ 0, %.lr.ph ], [ %indvars.iv.next.3, %.lr.ph.new ]
  %.07277.unr = phi double [ 0.000000e+00, %.lr.ph ], [ %38, %.lr.ph.new ]
  br i1 %lcmp.mod.not, label %.lr.ph85.preheader, label %.epil.preheader

.epil.preheader:                                  ; preds = %.lr.ph85.preheader.unr-lcssa, %.epil.preheader
  %indvars.iv.epil = phi i64 [ %indvars.iv.next.epil, %.epil.preheader ], [ %indvars.iv.unr, %.lr.ph85.preheader.unr-lcssa ]
  %.07277.epil = phi double [ %44, %.epil.preheader ], [ %.07277.unr, %.lr.ph85.preheader.unr-lcssa ]
  %epil.iter = phi i64 [ %epil.iter.next, %.epil.preheader ], [ 0, %.lr.ph85.preheader.unr-lcssa ]
  %42 = mul nuw nsw i64 %indvars.iv.epil, %6
  %gep.epil = getelementptr inbounds nuw double, ptr %invariant.gep, i64 %42
  %43 = load double, ptr %gep.epil, align 8
  %44 = tail call double @llvm.fmuladd.f64(double %43, double %43, double %.07277.epil)
  %indvars.iv.next.epil = add nuw nsw i64 %indvars.iv.epil, 1
  %epil.iter.next = add i64 %epil.iter, 1
  %epil.iter.cmp.not = icmp eq i64 %epil.iter.next, %xtraiter
  br i1 %epil.iter.cmp.not, label %.lr.ph85.preheader, label %.epil.preheader, !llvm.loop !16

.lr.ph85.preheader:                               ; preds = %.epil.preheader, %.lr.ph85.preheader.unr-lcssa
  %.lcssa = phi double [ %.lcssa.ph, %.lr.ph85.preheader.unr-lcssa ], [ %44, %.epil.preheader ]
  %45 = tail call double @sqrt(double noundef %.lcssa) #9
  %46 = mul nuw nsw i64 %indvars.iv129, %6
  %47 = getelementptr inbounds nuw double, ptr %3, i64 %46
  %48 = getelementptr inbounds nuw double, ptr %47, i64 %indvars.iv129
  store double %45, ptr %48, align 8
  %invariant.gep79135 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv129
  %invariant.gep81136 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %or.cond.not = xor i1 %or.cond, true
  %brmerge = select i1 %or.cond.not, i1 true, i1 %conflict.rdx163
  br i1 %brmerge, label %.lr.ph85.preheader180, label %vector.ph166

vector.ph166:                                     ; preds = %.lr.ph85.preheader
  %49 = load double, ptr %48, align 8, !alias.scope !18
  %broadcast.splatinsert172 = insertelement <2 x double> poison, double %49, i64 0
  %broadcast.splat173 = shufflevector <2 x double> %broadcast.splatinsert172, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body169

vector.body169:                                   ; preds = %vector.body169, %vector.ph166
  %index170 = phi i64 [ 0, %vector.ph166 ], [ %index.next174, %vector.body169 ]
  %50 = getelementptr inbounds nuw double, ptr %invariant.gep79135, i64 %index170
  %wide.load171 = load <2 x double>, ptr %50, align 8, !alias.scope !21
  %51 = fdiv <2 x double> %wide.load171, %broadcast.splat173
  %52 = getelementptr inbounds nuw double, ptr %invariant.gep81136, i64 %index170
  store <2 x double> %51, ptr %52, align 8, !alias.scope !23, !noalias !25
  %index.next174 = add nuw i64 %index170, 2
  %53 = icmp eq i64 %index.next174, %n.vec168
  br i1 %53, label %middle.block175, label %vector.body169, !llvm.loop !26

middle.block175:                                  ; preds = %vector.body169
  br i1 %cmp.n176, label %._crit_edge86, label %.lr.ph85.preheader180

.lr.ph85.preheader180:                            ; preds = %.lr.ph85.preheader, %middle.block175
  %indvars.iv107.ph = phi i64 [ 0, %.lr.ph85.preheader ], [ %n.vec168, %middle.block175 ]
  br i1 %lcmp.mod183.not, label %.lr.ph85.prol.loopexit, label %.lr.ph85.prol

.lr.ph85.prol:                                    ; preds = %.lr.ph85.preheader180
  %54 = mul nuw nsw i64 %indvars.iv107.ph, %6
  %gep80.prol = getelementptr inbounds nuw double, ptr %invariant.gep79135, i64 %54
  %55 = load double, ptr %gep80.prol, align 8
  %56 = load double, ptr %48, align 8
  %57 = fdiv double %55, %56
  %gep82.prol = getelementptr inbounds nuw double, ptr %invariant.gep81136, i64 %54
  store double %57, ptr %gep82.prol, align 8
  %indvars.iv.next108.prol = or disjoint i64 %indvars.iv107.ph, 1
  br label %.lr.ph85.prol.loopexit

.lr.ph85.prol.loopexit:                           ; preds = %.lr.ph85.prol, %.lr.ph85.preheader180
  %indvars.iv107.unr = phi i64 [ %indvars.iv107.ph, %.lr.ph85.preheader180 ], [ %indvars.iv.next108.prol, %.lr.ph85.prol ]
  %58 = icmp eq i64 %indvars.iv107.ph, %22
  br i1 %58, label %._crit_edge86, label %.lr.ph85

.lr.ph85:                                         ; preds = %.lr.ph85.prol.loopexit, %.lr.ph85
  %indvars.iv107 = phi i64 [ %indvars.iv.next108.1, %.lr.ph85 ], [ %indvars.iv107.unr, %.lr.ph85.prol.loopexit ]
  %59 = mul nuw nsw i64 %indvars.iv107, %6
  %gep80 = getelementptr inbounds nuw double, ptr %invariant.gep79135, i64 %59
  %60 = load double, ptr %gep80, align 8
  %61 = load double, ptr %48, align 8
  %62 = fdiv double %60, %61
  %gep82 = getelementptr inbounds nuw double, ptr %invariant.gep81136, i64 %59
  store double %62, ptr %gep82, align 8
  %indvars.iv.next108 = add nuw nsw i64 %indvars.iv107, 1
  %63 = mul nuw nsw i64 %indvars.iv.next108, %6
  %gep80.1 = getelementptr inbounds nuw double, ptr %invariant.gep79135, i64 %63
  %64 = load double, ptr %gep80.1, align 8
  %65 = load double, ptr %48, align 8
  %66 = fdiv double %64, %65
  %gep82.1 = getelementptr inbounds nuw double, ptr %invariant.gep81136, i64 %63
  store double %66, ptr %gep82.1, align 8
  %indvars.iv.next108.1 = add nuw nsw i64 %indvars.iv107, 2
  %exitcond111.not.1 = icmp eq i64 %indvars.iv.next108.1, %wide.trip.count110
  br i1 %exitcond111.not.1, label %._crit_edge86, label %.lr.ph85, !llvm.loop !27

._crit_edge86:                                    ; preds = %.lr.ph85.prol.loopexit, %.lr.ph85, %middle.block175, %._crit_edge
  %67 = phi i64 [ %39, %._crit_edge ], [ %46, %middle.block175 ], [ %46, %.lr.ph85 ], [ %46, %.lr.ph85.prol.loopexit ]
  %indvars.iv.next130 = add nuw nsw i64 %indvars.iv129, 1
  %68 = icmp samesign ult i64 %indvars.iv.next130, %9
  br i1 %68, label %.lr.ph103.preheader, label %.loopexit

.lr.ph103.preheader:                              ; preds = %._crit_edge86
  %69 = getelementptr inbounds nuw double, ptr %3, i64 %67
  %70 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %71 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %72 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %bound0 = icmp ult ptr %gep195, %scevgep142
  %bound1 = icmp ult ptr %scevgep141, %scevgep140
  %found.conflict = and i1 %bound0, %bound1
  %bound0145 = icmp ult ptr %gep195, %scevgep144
  %bound1146 = icmp ult ptr %gep197, %scevgep140
  %found.conflict147 = and i1 %bound0145, %bound1146
  %conflict.rdx = or i1 %found.conflict, %found.conflict147
  %73 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %74 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %75 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  %76 = getelementptr inbounds nuw double, ptr %4, i64 %indvars.iv129
  br label %.lr.ph103

.lr.ph103:                                        ; preds = %.lr.ph103.preheader, %._crit_edge100
  %indvars.iv124 = phi i64 [ %indvars.iv.next125, %._crit_edge100 ], [ %indvars.iv122, %.lr.ph103.preheader ]
  %77 = getelementptr inbounds nuw double, ptr %69, i64 %indvars.iv124
  store double 0.000000e+00, ptr %77, align 8
  %invariant.gep89 = getelementptr inbounds nuw double, ptr %2, i64 %indvars.iv124
  br i1 %8, label %.lr.ph93.preheader, label %._crit_edge100

.lr.ph93.preheader:                               ; preds = %.lr.ph103
  br i1 %23, label %.lr.ph99.preheader.unr-lcssa, label %.lr.ph93

.lr.ph93:                                         ; preds = %.lr.ph93.preheader, %.lr.ph93
  %indvars.iv112 = phi i64 [ %indvars.iv.next113.1, %.lr.ph93 ], [ 0, %.lr.ph93.preheader ]
  %78 = phi double [ %86, %.lr.ph93 ], [ 0.000000e+00, %.lr.ph93.preheader ]
  %niter188 = phi i64 [ %niter188.next.1, %.lr.ph93 ], [ 0, %.lr.ph93.preheader ]
  %79 = mul nuw nsw i64 %indvars.iv112, %6
  %gep88 = getelementptr inbounds nuw double, ptr %70, i64 %79
  %80 = load double, ptr %gep88, align 8
  %gep90 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %79
  %81 = load double, ptr %gep90, align 8
  %82 = tail call double @llvm.fmuladd.f64(double %80, double %81, double %78)
  store double %82, ptr %77, align 8
  %indvars.iv.next113 = or disjoint i64 %indvars.iv112, 1
  %83 = mul nuw nsw i64 %indvars.iv.next113, %6
  %gep88.1 = getelementptr inbounds nuw double, ptr %71, i64 %83
  %84 = load double, ptr %gep88.1, align 8
  %gep90.1 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %83
  %85 = load double, ptr %gep90.1, align 8
  %86 = tail call double @llvm.fmuladd.f64(double %84, double %85, double %82)
  store double %86, ptr %77, align 8
  %indvars.iv.next113.1 = add nuw nsw i64 %indvars.iv112, 2
  %niter188.next.1 = add i64 %niter188, 2
  %niter188.ncmp.1 = icmp eq i64 %niter188.next.1, %unroll_iter187
  br i1 %niter188.ncmp.1, label %.lr.ph99.preheader.unr-lcssa, label %.lr.ph93, !llvm.loop !28

.lr.ph99.preheader.unr-lcssa:                     ; preds = %.lr.ph93, %.lr.ph93.preheader
  %indvars.iv112.unr = phi i64 [ 0, %.lr.ph93.preheader ], [ %indvars.iv.next113.1, %.lr.ph93 ]
  %.unr = phi double [ 0.000000e+00, %.lr.ph93.preheader ], [ %86, %.lr.ph93 ]
  br i1 %lcmp.mod186.not, label %.lr.ph99.preheader, label %.lr.ph93.epil

.lr.ph93.epil:                                    ; preds = %.lr.ph99.preheader.unr-lcssa
  %87 = mul nuw nsw i64 %indvars.iv112.unr, %6
  %gep88.epil = getelementptr inbounds nuw double, ptr %72, i64 %87
  %88 = load double, ptr %gep88.epil, align 8
  %gep90.epil = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %87
  %89 = load double, ptr %gep90.epil, align 8
  %90 = tail call double @llvm.fmuladd.f64(double %88, double %89, double %.unr)
  store double %90, ptr %77, align 8
  br label %.lr.ph99.preheader

.lr.ph99.preheader:                               ; preds = %.lr.ph99.preheader.unr-lcssa, %.lr.ph93.epil
  %or.cond178.not = xor i1 %or.cond178, true
  %brmerge198 = select i1 %or.cond178.not, i1 true, i1 %conflict.rdx
  br i1 %brmerge198, label %.lr.ph99.preheader179, label %vector.ph

vector.ph:                                        ; preds = %.lr.ph99.preheader
  %91 = load double, ptr %77, align 8, !alias.scope !29
  %broadcast.splatinsert = insertelement <2 x double> poison, double %91, i64 0
  %broadcast.splat = shufflevector <2 x double> %broadcast.splatinsert, <2 x double> poison, <2 x i32> zeroinitializer
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i64 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %92 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %index
  %93 = getelementptr inbounds nuw i8, ptr %92, i64 16
  %wide.load = load <2 x double>, ptr %92, align 8, !alias.scope !32, !noalias !34
  %wide.load148 = load <2 x double>, ptr %93, align 8, !alias.scope !32, !noalias !34
  %94 = getelementptr inbounds nuw double, ptr %73, i64 %index
  %95 = getelementptr inbounds nuw i8, ptr %94, i64 16
  %wide.load149 = load <2 x double>, ptr %94, align 8, !alias.scope !36
  %wide.load150 = load <2 x double>, ptr %95, align 8, !alias.scope !36
  %96 = fneg <2 x double> %wide.load149
  %97 = fneg <2 x double> %wide.load150
  %98 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %96, <2 x double> %broadcast.splat, <2 x double> %wide.load)
  %99 = tail call <2 x double> @llvm.fmuladd.v2f64(<2 x double> %97, <2 x double> %broadcast.splat, <2 x double> %wide.load148)
  store <2 x double> %98, ptr %92, align 8, !alias.scope !32, !noalias !34
  store <2 x double> %99, ptr %93, align 8, !alias.scope !32, !noalias !34
  %index.next = add nuw i64 %index, 4
  %100 = icmp eq i64 %index.next, %n.vec
  br i1 %100, label %middle.block, label %vector.body, !llvm.loop !37

middle.block:                                     ; preds = %vector.body
  br i1 %cmp.n, label %._crit_edge100, label %.lr.ph99.preheader179

.lr.ph99.preheader179:                            ; preds = %.lr.ph99.preheader, %middle.block
  %indvars.iv117.ph = phi i64 [ 0, %.lr.ph99.preheader ], [ %n.vec, %middle.block ]
  br i1 %lcmp.mod190.not, label %.lr.ph99.prol.loopexit, label %.lr.ph99.prol

.lr.ph99.prol:                                    ; preds = %.lr.ph99.preheader179
  %101 = mul nuw nsw i64 %indvars.iv117.ph, %6
  %gep95.prol = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %101
  %102 = load double, ptr %gep95.prol, align 8
  %gep97.prol = getelementptr inbounds nuw double, ptr %74, i64 %101
  %103 = load double, ptr %gep97.prol, align 8
  %104 = load double, ptr %77, align 8
  %105 = fneg double %103
  %106 = tail call double @llvm.fmuladd.f64(double %105, double %104, double %102)
  store double %106, ptr %gep95.prol, align 8
  %indvars.iv.next118.prol = or disjoint i64 %indvars.iv117.ph, 1
  br label %.lr.ph99.prol.loopexit

.lr.ph99.prol.loopexit:                           ; preds = %.lr.ph99.prol, %.lr.ph99.preheader179
  %indvars.iv117.unr = phi i64 [ %indvars.iv117.ph, %.lr.ph99.preheader179 ], [ %indvars.iv.next118.prol, %.lr.ph99.prol ]
  %107 = icmp eq i64 %indvars.iv117.ph, %24
  br i1 %107, label %._crit_edge100, label %.lr.ph99

.lr.ph99:                                         ; preds = %.lr.ph99.prol.loopexit, %.lr.ph99
  %indvars.iv117 = phi i64 [ %indvars.iv.next118.1, %.lr.ph99 ], [ %indvars.iv117.unr, %.lr.ph99.prol.loopexit ]
  %108 = mul nuw nsw i64 %indvars.iv117, %6
  %gep95 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %108
  %109 = load double, ptr %gep95, align 8
  %gep97 = getelementptr inbounds nuw double, ptr %75, i64 %108
  %110 = load double, ptr %gep97, align 8
  %111 = load double, ptr %77, align 8
  %112 = fneg double %110
  %113 = tail call double @llvm.fmuladd.f64(double %112, double %111, double %109)
  store double %113, ptr %gep95, align 8
  %indvars.iv.next118 = add nuw nsw i64 %indvars.iv117, 1
  %114 = mul nuw nsw i64 %indvars.iv.next118, %6
  %gep95.1 = getelementptr inbounds nuw double, ptr %invariant.gep89, i64 %114
  %115 = load double, ptr %gep95.1, align 8
  %gep97.1 = getelementptr inbounds nuw double, ptr %76, i64 %114
  %116 = load double, ptr %gep97.1, align 8
  %117 = load double, ptr %77, align 8
  %118 = fneg double %116
  %119 = tail call double @llvm.fmuladd.f64(double %118, double %117, double %115)
  store double %119, ptr %gep95.1, align 8
  %indvars.iv.next118.1 = add nuw nsw i64 %indvars.iv117, 2
  %exitcond121.not.1 = icmp eq i64 %indvars.iv.next118.1, %wide.trip.count120
  br i1 %exitcond121.not.1, label %._crit_edge100, label %.lr.ph99, !llvm.loop !38

._crit_edge100:                                   ; preds = %.lr.ph99.prol.loopexit, %.lr.ph99, %middle.block, %.lr.ph103
  %indvars.iv.next125 = add nuw nsw i64 %indvars.iv124, 1
  %exitcond128.not = icmp eq i64 %indvars.iv.next125, %6
  br i1 %exitcond128.not, label %.loopexit, label %.lr.ph103, !llvm.loop !39

._crit_edge105:                                   ; preds = %.loopexit, %5
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #2

; Function Attrs: mustprogress nocallback nofree nounwind willreturn memory(errnomem: write)
declare dso_local double @sqrt(double noundef) local_unnamed_addr #3

; Function Attrs: noinline nounwind uwtable
define dso_local noundef i32 @main() local_unnamed_addr #4 {
  %1 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #10
  %2 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #10
  %3 = tail call dereferenceable_or_null(524288) ptr @malloc(i64 noundef 524288) #10
  tail call void @init_array(i32 noundef 256, i32 noundef 256, ptr noundef %1)
  %4 = tail call i32 @clock() #9
  tail call void @gramschmidt(i32 noundef 256, i32 noundef 256, ptr noundef %1, ptr noundef %2, ptr noundef %3)
  %5 = tail call i32 @clock() #9
  %6 = sub nsw i32 %5, %4
  %7 = sitofp i32 %6 to double
  %8 = fdiv double %7, 1.000000e+03
  %9 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str, double noundef %8) #9
  %10 = load double, ptr %2, align 8
  %11 = tail call i32 (ptr, ...) @__mingw_printf(ptr noundef nonnull @.str.1, double noundef %10) #9
  tail call void @free(ptr noundef %1)
  tail call void @free(ptr noundef %2)
  tail call void @free(ptr noundef %3)
  ret i32 0
}

; Function Attrs: mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite)
declare dso_local noalias noundef ptr @malloc(i64 noundef) local_unnamed_addr #5

declare dso_local i32 @clock() local_unnamed_addr #6

declare dso_local i32 @__mingw_printf(ptr noundef, ...) local_unnamed_addr #6

; Function Attrs: mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite)
declare dso_local void @free(ptr allocptr noundef captures(none)) local_unnamed_addr #7

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare <2 x double> @llvm.fmuladd.v2f64(<2 x double>, <2 x double>, <2 x double>) #8

attributes #0 = { nofree noinline norecurse nosync nounwind memory(argmem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree noinline norecurse nounwind memory(argmem: readwrite, errnomem: write) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #3 = { mustprogress nocallback nofree nounwind willreturn memory(errnomem: write) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { mustprogress nounwind willreturn allockind("free") memory(argmem: readwrite, inaccessiblemem: readwrite) "alloc-family"="malloc" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #8 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #9 = { nounwind }
attributes #10 = { allocsize(0) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 21.1.8", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/gramschmidt.c", directory: "C:/Users/ultim/compiler-opt")
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
!12 = distinct !{!12, !9, !11, !10}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !9}
!16 = distinct !{!16, !17}
!17 = !{!"llvm.loop.unroll.disable"}
!18 = !{!19}
!19 = distinct !{!19, !20}
!20 = distinct !{!20, !"LVerDomain"}
!21 = !{!22}
!22 = distinct !{!22, !20}
!23 = !{!24}
!24 = distinct !{!24, !20}
!25 = !{!22, !19}
!26 = distinct !{!26, !9, !10, !11}
!27 = distinct !{!27, !9, !10}
!28 = distinct !{!28, !9}
!29 = !{!30}
!30 = distinct !{!30, !31}
!31 = distinct !{!31, !"LVerDomain"}
!32 = !{!33}
!33 = distinct !{!33, !31}
!34 = !{!35, !30}
!35 = distinct !{!35, !31}
!36 = !{!35}
!37 = distinct !{!37, !9, !10, !11}
!38 = distinct !{!38, !9, !10}
!39 = distinct !{!39, !9}
