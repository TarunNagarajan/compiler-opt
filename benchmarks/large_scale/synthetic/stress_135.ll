; ModuleID = '/tmp/autogen.bc'
source_filename = "/tmp/autogen.bc"

define void @autogen_SD0(ptr %0, ptr %1, ptr %2, i32 %3, i64 %4, i8 %5) {
BB:
  %A4 = alloca <4 x i16>, align 8
  %A3 = alloca <4 x i64>, align 32
  %A2 = alloca <2 x float>, align 8
  %A1 = alloca <8 x i16>, align 16
  %A = alloca <4 x i32>, align 16
  %L = load <2 x i16>, ptr %A, align 4
  store i32 0, ptr %0, align 4
  %E = extractelement <1 x i32> zeroinitializer, i32 32529
  %Shuff = shufflevector <1 x i32> zeroinitializer, <1 x i32> zeroinitializer, <1 x i32> poison
  %I = insertelement <2 x i32> zeroinitializer, i32 0, i32 132849
  %B = udiv <4 x i8> zeroinitializer, zeroinitializer
  %Se = sext i8 77 to i16
  %Sl = select <16 x i1> <i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false>, <16 x i64> zeroinitializer, <16 x i64> zeroinitializer
  %L5 = load i8, ptr %0, align 1
  store <16 x double> <double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF>, ptr %A2, align 128
  %E6 = extractelement <16 x i64> %Sl, i32 132849
  %Shuff7 = shufflevector <16 x i64> zeroinitializer, <16 x i64> zeroinitializer, <16 x i32> <i32 2, i32 4, i32 6, i32 8, i32 10, i32 12, i32 14, i32 16, i32 18, i32 20, i32 22, i32 24, i32 26, i32 poison, i32 30, i32 0>
  %I8 = insertelement <4 x i8> zeroinitializer, i8 21, i32 %3
  %B9 = xor i64 251161, 251161
  %Tr = trunc <4 x i8> %B to <4 x i1>
  %Sl10 = select i1 true, <4 x i32> zeroinitializer, <4 x i32> zeroinitializer
  %Cmp = icmp ult <1 x i32> %Shuff, %Shuff
  %L11 = load i64, ptr %0, align 4
  store <4 x double> <double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF>, ptr %0, align 32
  %E12 = extractelement <1 x i32> zeroinitializer, i32 32529
  %Shuff13 = shufflevector <16 x i64> zeroinitializer, <16 x i64> zeroinitializer, <16 x i32> <i32 4, i32 6, i32 poison, i32 10, i32 12, i32 14, i32 16, i32 poison, i32 20, i32 22, i32 24, i32 26, i32 28, i32 30, i32 0, i32 2>
  %I14 = insertelement <1 x i32> %Shuff, i32 %E12, i32 132849
  %B15 = add i64 %4, %L11
  %FC = uitofp <4 x i64> zeroinitializer to <4 x float>
  %Sl16 = select i1 true, ptr %A4, ptr %0
  %Cmp17 = icmp ne <4 x i8> %B, %B
  %L18 = load i32, ptr %Sl16, align 4
  store <4 x i8> %B, ptr %Sl16, align 4
  %E19 = extractelement <16 x i64> %Sl, i32 %E
  %Shuff20 = shufflevector <4 x i8> %B, <4 x i8> %I8, <4 x i32> poison
  %I21 = insertelement <4 x i8> %B, i8 21, i32 %L18
  %B22 = fadd float 0xC4F0BB4480000000, 0xC4F0BB4480000000
  %PC = bitcast ptr %A2 to ptr
  %Sl23 = select i1 true, <1 x i32> zeroinitializer, <1 x i32> %Shuff
  %Cmp24 = icmp ugt i64 %E19, 251161
  br label %CF830

CF830:                                            ; preds = %BB
  %L25 = load i64, ptr %A3, align 4
  store <8 x i64> <i64 0, i64 -1, i64 0, i64 -1, i64 0, i64 -1, i64 0, i64 -1>, ptr %Sl16, align 64
  %E26 = extractelement <4 x i8> %I8, i32 %E12
  %Shuff27 = shufflevector <16 x i16> zeroinitializer, <16 x i16> zeroinitializer, <16 x i32> <i32 14, i32 poison, i32 18, i32 20, i32 22, i32 poison, i32 26, i32 28, i32 30, i32 0, i32 2, i32 poison, i32 poison, i32 8, i32 10, i32 12>
  %I28 = insertelement <16 x i16> zeroinitializer, i16 18437, i32 %E
  %B29 = xor i16 -2255, 18437
  %PC30 = bitcast ptr %0 to ptr
  %Sl31 = select i1 true, i8 77, i8 21
  %Cmp32 = fcmp ord double 0x18DF23FE11DD527C, 0xAE97BFB633957A34
  br label %CF782

CF782:                                            ; preds = %CF830
  %L33 = load <8 x i16>, ptr %Sl16, align 16
  store i64 251161, ptr %A3, align 4
  %E34 = extractelement <8 x i16> %L33, i32 %L18
  %Shuff35 = shufflevector <4 x i8> %I8, <4 x i8> %B, <4 x i32> <i32 1, i32 3, i32 5, i32 7>
  %I36 = insertelement <16 x i64> %Shuff7, i64 251161, i32 %3
  %B37 = shl <4 x i8> %I8, zeroinitializer
  %Tr38 = trunc <16 x i64> zeroinitializer to <16 x i32>
  %Sl39 = select <4 x i1> %Tr, <4 x i8> %I8, <4 x i8> zeroinitializer
  %Cmp40 = icmp slt i16 %B29, 18437
  br label %CF775

CF775:                                            ; preds = %CF775, %CF823, %CF782
  %L41 = load <8 x i32>, ptr %PC30, align 32
  store i64 251161, ptr %Sl16, align 4
  %E42 = extractelement <16 x i64> zeroinitializer, i32 %3
  %Shuff43 = shufflevector <4 x i8> zeroinitializer, <4 x i8> %B, <4 x i32> <i32 poison, i32 1, i32 poison, i32 5>
  %I44 = insertelement <16 x i64> %Shuff13, i64 251161, i32 32529
  %B45 = xor i32 132849, %3
  %FC46 = uitofp i16 %Se to double
  %Sl47 = select i1 %Cmp32, i1 %Cmp40, i1 %Cmp24
  br i1 %Sl47, label %CF775, label %CF823

CF823:                                            ; preds = %CF775
  %Cmp48 = fcmp oeq <4 x float> %FC, %FC
  %L49 = load i32, ptr %Sl16, align 4
  store <8 x i32> %L41, ptr %A4, align 32
  %E50 = extractelement <4 x i8> %Shuff43, i32 32529
  %Shuff51 = shufflevector <4 x i1> %Cmp48, <4 x i1> %Tr, <4 x i32> <i32 4, i32 6, i32 0, i32 2>
  %I52 = insertelement <4 x i8> %Shuff35, i8 21, i32 %E12
  %B53 = urem <2 x i32> %I, zeroinitializer
  %FC54 = uitofp <16 x i16> %I28 to <16 x double>
  %Sl55 = select i1 %Cmp40, i64 %4, i64 %E19
  %Cmp56 = icmp ugt i64 %E6, %E6
  br i1 %Cmp56, label %CF775, label %CF789

CF789:                                            ; preds = %CF789, %CF801, %CF823
  %L57 = load double, ptr %PC30, align 8
  %E58 = extractelement <16 x i16> zeroinitializer, i32 132849
  %Shuff59 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %Shuff, <1 x i32> <i32 1>
  %I60 = insertelement <4 x i8> %Shuff20, i8 %E26, i32 %B45
  %B61 = udiv <4 x i8> %I8, %Shuff43
  %Tr62 = trunc <1 x i32> %Sl23 to <1 x i8>
  %Sl63 = select <4 x i1> %Cmp48, <4 x i8> %B61, <4 x i8> %B
  %Cmp64 = icmp ule i16 %Se, -2255
  br i1 %Cmp64, label %CF789, label %CF801

CF801:                                            ; preds = %CF789
  %L65 = load <16 x double>, ptr %Sl16, align 128
  store float 0xC4F0BB4480000000, ptr %Sl16, align 4
  %E66 = extractelement <4 x i8> %Sl39, i32 %B45
  %Shuff67 = shufflevector <4 x float> %FC, <4 x float> %FC, <4 x i32> <i32 1, i32 3, i32 5, i32 poison>
  %I68 = insertelement <4 x i8> %Sl63, i8 21, i32 %B45
  %B69 = and i16 18761, 16293
  %PC70 = bitcast ptr %A1 to ptr
  %Sl71 = select i1 %Cmp24, i32 %E, i32 %B45
  %Cmp72 = icmp ult i16 %E34, %Se
  br i1 %Cmp72, label %CF789, label %CF796

CF796:                                            ; preds = %CF801
  %L73 = load i32, ptr %Sl16, align 4
  store <8 x i16> %L33, ptr %PC30, align 16
  %E74 = extractelement <4 x i8> %Shuff35, i32 %E12
  %Shuff75 = shufflevector <1 x i32> %Shuff59, <1 x i32> %Shuff, <1 x i32> zeroinitializer
  %I76 = insertelement <8 x i16> %L33, i16 %E58, i32 %Sl71
  %Tr77 = trunc <4 x i8> %Shuff20 to <4 x i1>
  %Sl78 = select i1 %Cmp40, i64 %B15, i64 %E6
  %Cmp79 = icmp ult i1 %Cmp72, %Cmp24
  br label %CF761

CF761:                                            ; preds = %CF761, %CF796
  %L80 = load i8, ptr %PC70, align 1
  store <2 x i8> <i8 0, i8 -1>, ptr %PC70, align 2
  %E81 = extractelement <16 x i64> zeroinitializer, i32 %Sl71
  %Shuff82 = shufflevector <8 x i16> %I76, <8 x i16> %L33, <8 x i32> <i32 12, i32 14, i32 0, i32 2, i32 4, i32 6, i32 8, i32 10>
  %I83 = insertelement <1 x i32> zeroinitializer, i32 %3, i32 %Sl71
  %B84 = shl i8 %L5, %E50
  %FC85 = sitofp i16 16293 to float
  %Sl86 = select i1 true, i1 true, i1 true
  br i1 %Sl86, label %CF761, label %CF776

CF776:                                            ; preds = %CF776, %CF811, %CF826, %CF761
  %L87 = load i1, ptr %0, align 1
  br i1 %L87, label %CF776, label %CF811

CF811:                                            ; preds = %CF776
  store <2 x i32> %B53, ptr %PC30, align 8
  %E88 = extractelement <16 x double> %FC54, i32 %E
  %Shuff89 = shufflevector <4 x i32> zeroinitializer, <4 x i32> zeroinitializer, <4 x i32> <i32 0, i32 poison, i32 4, i32 6>
  %I90 = insertelement <4 x i8> %Shuff43, i8 %E66, i32 %B45
  %B91 = lshr <4 x i8> %Shuff20, %I90
  %Se92 = sext <4 x i8> %I52 to <4 x i64>
  %Sl93 = select <16 x i1> <i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false>, <16 x double> %FC54, <16 x double> %FC54
  %Cmp94 = fcmp oeq <16 x double> %L65, %FC54
  %L95 = load <16 x float>, ptr %Sl16, align 64
  store i32 %B45, ptr %PC30, align 4
  %E96 = extractelement <4 x i1> %Shuff51, i32 %3
  br i1 %E96, label %CF776, label %CF791

CF791:                                            ; preds = %CF791, %CF811
  %Shuff97 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %Shuff, <1 x i32> <i32 1>
  %I98 = insertelement <8 x i16> zeroinitializer, i16 %B69, i32 %E12
  %FC99 = sitofp i16 18761 to float
  %Sl100 = select i1 true, <1 x i32> %I14, <1 x i32> %Shuff59
  %Cmp101 = icmp ule <1 x i32> %I14, %Shuff
  %L102 = load i64, ptr %0, align 4
  %E103 = extractelement <1 x i32> %Shuff75, i32 %E12
  %Shuff104 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %Shuff, <1 x i32> <i32 1>
  %I105 = insertelement <16 x i64> %Shuff7, i64 %E6, i32 32529
  %B106 = udiv <16 x i64> %I44, %I36
  %FC107 = sitofp <4 x i8> zeroinitializer to <4 x double>
  %Sl108 = select i1 %Cmp56, i16 18437, i16 %E58
  %Cmp109 = icmp eq <1 x i8> zeroinitializer, zeroinitializer
  %L110 = load <4 x i1>, ptr %Sl16, align 1
  store i32 0, ptr %0, align 4
  %E111 = extractelement <1 x i32> zeroinitializer, i32 %E103
  %Shuff112 = shufflevector <8 x i16> %L33, <8 x i16> %L33, <8 x i32> <i32 13, i32 15, i32 1, i32 3, i32 5, i32 7, i32 9, i32 11>
  %I113 = insertelement <4 x float> %Shuff67, float %FC85, i32 %B45
  %B114 = lshr <2 x i16> %L, %L
  %FC115 = sitofp <4 x i8> %B91 to <4 x double>
  %Sl116 = select i1 %Cmp56, i1 %Cmp64, i1 %Sl86
  br i1 %Sl116, label %CF791, label %CF817

CF817:                                            ; preds = %CF817, %CF791
  %Cmp117 = fcmp false double 0x58238842DB21C0C0, 0xAE97BFB633957A34
  br i1 %Cmp117, label %CF817, label %CF826

CF826:                                            ; preds = %CF817
  %L118 = load <8 x i16>, ptr %PC30, align 16
  store double %E88, ptr %0, align 8
  %E119 = extractelement <16 x i64> zeroinitializer, i32 %E
  %Shuff120 = shufflevector <16 x i64> %Shuff13, <16 x i64> %I36, <16 x i32> <i32 11, i32 13, i32 15, i32 poison, i32 poison, i32 poison, i32 23, i32 poison, i32 27, i32 29, i32 31, i32 1, i32 poison, i32 poison, i32 7, i32 9>
  %I121 = insertelement <4 x i8> %Sl63, i8 21, i32 %L49
  %Se122 = sext <2 x i16> %L to <2 x i32>
  %Sl123 = select <8 x i1> <i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false>, <8 x i16> %I76, <8 x i16> %Shuff112
  %Cmp124 = fcmp false <4 x float> %Shuff67, %I113
  %L125 = load <2 x i1>, ptr %0, align 1
  store i8 %E74, ptr %PC70, align 1
  %E126 = extractelement <1 x i32> %Shuff75, i32 %3
  %Shuff127 = shufflevector <4 x i1> %Tr, <4 x i1> %Cmp48, <4 x i32> <i32 1, i32 3, i32 5, i32 poison>
  %I128 = insertelement <8 x i16> %Shuff112, i16 %Sl108, i32 %E
  %B129 = sub <8 x i16> %I76, zeroinitializer
  %FC130 = fptosi <16 x double> %L65 to <16 x i16>
  %Sl131 = select i1 %Cmp24, <4 x i8> %Shuff20, <4 x i8> %B
  %Cmp132 = icmp sgt i16 %Sl108, %B69
  br i1 %Cmp132, label %CF776, label %CF786

CF786:                                            ; preds = %CF786, %CF826
  %L133 = load i64, ptr %PC70, align 4
  store <16 x double> %FC54, ptr %PC70, align 128
  %E134 = extractelement <1 x i32> zeroinitializer, i32 %Sl71
  %Shuff135 = shufflevector <1 x i32> %I14, <1 x i32> zeroinitializer, <1 x i32> zeroinitializer
  %I136 = insertelement <2 x i32> zeroinitializer, i32 %E126, i32 %B45
  %B137 = srem <4 x i64> zeroinitializer, %Se92
  %PC138 = bitcast ptr %0 to ptr
  %Sl139 = select i1 %Sl116, i32 32529, i32 %3
  %Cmp140 = icmp sge i64 %L133, %L102
  br i1 %Cmp140, label %CF786, label %CF810

CF810:                                            ; preds = %CF786
  %L141 = load <2 x i1>, ptr %Sl16, align 1
  store i1 %Cmp132, ptr %Sl16, align 1
  %E142 = extractelement <1 x i32> %I83, i32 %E12
  %Shuff143 = shufflevector <8 x i16> %Shuff82, <8 x i16> %L33, <8 x i32> <i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 1, i32 poison>
  %I144 = insertelement <4 x i8> %Shuff20, i8 %5, i32 %E103
  %FC145 = uitofp <4 x i8> %I144 to <4 x float>
  %Sl146 = select <8 x i1> <i1 true, i1 false, i1 true, i1 false, i1 true, i1 false, i1 true, i1 false>, <8 x i16> %L33, <8 x i16> %Shuff143
  %Cmp147 = icmp ult <1 x i32> %Shuff75, %Shuff59
  %L148 = load <1 x double>, ptr %PC70, align 8
  store i8 %L80, ptr %Sl16, align 1
  %E149 = extractelement <8 x i16> %L33, i32 %E12
  %Shuff150 = shufflevector <4 x float> %Shuff67, <4 x float> %I113, <4 x i32> <i32 3, i32 poison, i32 poison, i32 1>
  %I151 = insertelement <1 x i32> %Shuff59, i32 %E134, i32 132849
  %B152 = srem <16 x i32> %Tr38, %Tr38
  %Se153 = sext i1 %Sl86 to i16
  %Sl154 = select i1 %Cmp32, i8 77, i8 21
  %Cmp155 = icmp slt i1 true, %Cmp24
  br label %CF

CF:                                               ; preds = %CF, %CF795, %CF794, %CF821, %CF790, %CF785, %CF822, %CF810
  %L156 = load i64, ptr %PC138, align 4
  store <16 x i32> %Tr38, ptr %PC138, align 64
  %E157 = extractelement <4 x i8> %Shuff43, i32 %E134
  %Shuff158 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %I14, <1 x i32> poison
  %I159 = insertelement <4 x i32> %Sl10, i32 0, i32 0
  %B160 = or <4 x i8> %Shuff35, %I90
  %ZE = zext i1 true to i8
  %Sl161 = select i1 %Cmp132, <4 x float> %Shuff150, <4 x float> %I113
  %Cmp162 = icmp ugt i8 21, %L5
  br i1 %Cmp162, label %CF, label %CF795

CF795:                                            ; preds = %CF
  %L163 = load i64, ptr %Sl16, align 4
  %E164 = extractelement <16 x i16> zeroinitializer, i32 0
  %Shuff165 = shufflevector <16 x i64> %Shuff120, <16 x i64> zeroinitializer, <16 x i32> <i32 poison, i32 17, i32 19, i32 21, i32 poison, i32 25, i32 poison, i32 poison, i32 31, i32 1, i32 poison, i32 poison, i32 7, i32 9, i32 11, i32 13>
  %I166 = insertelement <4 x i32> %Shuff89, i32 0, i32 %L18
  %B167 = mul <16 x i64> %I44, %Shuff120
  %BC = bitcast float %FC99 to i32
  %Sl168 = select i1 %Sl116, <4 x i8> zeroinitializer, <4 x i8> %I8
  %Cmp169 = icmp ule <4 x i8> %B61, %B
  %L170 = load i1, ptr %PC70, align 1
  br i1 %L170, label %CF, label %CF774

CF774:                                            ; preds = %CF774, %CF819, %CF795
  %E171 = extractelement <1 x i32> %Shuff158, i32 %Sl71
  %Shuff172 = shufflevector <4 x double> %FC107, <4 x double> %FC107, <4 x i32> <i32 3, i32 5, i32 7, i32 1>
  %I173 = insertelement <1 x i32> %Shuff135, i32 %BC, i32 0
  %Se174 = sext <4 x i8> %I21 to <4 x i16>
  %Sl175 = select i1 %L170, i64 %B15, i64 %E19
  %Cmp176 = icmp sge <2 x i16> %L, %L
  %L177 = load i32, ptr %PC138, align 4
  store <8 x i64> <i64 0, i64 -1, i64 0, i64 -1, i64 0, i64 -1, i64 0, i64 -1>, ptr %0, align 64
  %E178 = extractelement <1 x i32> %Shuff97, i32 %L49
  %Shuff179 = shufflevector <16 x i64> %Shuff7, <16 x i64> %I36, <16 x i32> <i32 24, i32 26, i32 28, i32 30, i32 0, i32 2, i32 poison, i32 6, i32 8, i32 10, i32 poison, i32 14, i32 poison, i32 poison, i32 poison, i32 22>
  %I180 = insertelement <16 x i16> zeroinitializer, i16 %Sl108, i32 %Sl71
  %B181 = fsub <16 x float> %L95, %L95
  %FC182 = sitofp i64 %L102 to double
  %Sl183 = select i1 %Cmp140, <4 x i8> %Sl168, <4 x i8> zeroinitializer
  %Cmp184 = icmp ne <8 x i16> %Shuff112, %L33
  %L185 = load i1, ptr %Sl16, align 1
  br i1 %L185, label %CF774, label %CF819

CF819:                                            ; preds = %CF774
  store <4 x double> %Shuff172, ptr %PC30, align 32
  %E186 = extractelement <1 x i32> %Shuff59, i32 %E126
  %Shuff187 = shufflevector <8 x i16> %I128, <8 x i16> zeroinitializer, <8 x i32> <i32 6, i32 8, i32 poison, i32 12, i32 14, i32 0, i32 2, i32 poison>
  %I188 = insertelement <4 x i1> %Cmp124, i1 true, i32 %E126
  %B189 = and <2 x i16> %L, %L
  %Sl190 = select i1 %Sl47, ptr %PC, ptr %PC138
  %Cmp191 = icmp ne <16 x i32> %Tr38, %Tr38
  %L192 = load <8 x i1>, ptr %Sl190, align 1
  store double %E88, ptr %Sl16, align 8
  %E193 = extractelement <1 x i32> %Shuff75, i32 %Sl71
  %Shuff194 = shufflevector <16 x i1> %Cmp191, <16 x i1> %Cmp94, <16 x i32> <i32 1, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 poison, i32 19, i32 21, i32 23, i32 25, i32 27, i32 poison, i32 31>
  %I195 = insertelement <4 x i16> %Se174, i16 16293, i32 %E126
  %B196 = srem i16 %E58, %Se153
  %ZE197 = zext <1 x i1> %Cmp101 to <1 x i16>
  %Sl198 = select i1 %Sl116, ptr %2, ptr %Sl16
  %Cmp199 = icmp eq <1 x i32> %I173, zeroinitializer
  %L200 = load <2 x i1>, ptr %PC30, align 1
  store i16 %Sl108, ptr %PC138, align 2
  %E201 = extractelement <4 x i8> %Sl183, i32 %BC
  %Shuff202 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %Shuff97, <1 x i32> poison
  %I203 = insertelement <8 x i16> %L118, i16 %Sl108, i32 %E103
  %B204 = shl i64 %Sl78, %Sl55
  %BC205 = bitcast i32 %3 to float
  %Sl206 = select i1 %Cmp155, <2 x i32> %Se122, <2 x i32> zeroinitializer
  %Cmp207 = icmp ult i64 %L133, 251161
  br i1 %Cmp207, label %CF774, label %CF778

CF778:                                            ; preds = %CF778, %CF819
  %L208 = load i32, ptr %Sl198, align 4
  store <4 x i64> %Se92, ptr %Sl16, align 32
  %E209 = extractelement <1 x i32> %Shuff135, i32 %L177
  %Shuff210 = shufflevector <4 x i1> %Shuff127, <4 x i1> %Tr77, <4 x i32> <i32 6, i32 0, i32 2, i32 4>
  %I211 = insertelement <16 x i16> %I28, i16 %Sl108, i32 %BC
  %B212 = sub <1 x i32> %Sl23, %Shuff158
  %FC213 = fptosi double %FC182 to i64
  %Sl214 = select i1 %E96, i8 %E26, i8 %E66
  %Cmp215 = fcmp oge double 0xAE97BFB633957A34, %FC46
  br i1 %Cmp215, label %CF778, label %CF784

CF784:                                            ; preds = %CF784, %CF831, %CF829, %CF805, %CF778
  %L216 = load <2 x i32>, ptr %PC138, align 8
  store double %FC46, ptr %PC, align 8
  %E217 = extractelement <8 x i16> %Shuff82, i32 %L177
  %Shuff218 = shufflevector <4 x i8> %Shuff20, <4 x i8> %I144, <4 x i32> <i32 poison, i32 5, i32 7, i32 poison>
  %I219 = insertelement <4 x i8> %Sl63, i8 %E66, i32 %L177
  %PC220 = bitcast ptr %PC70 to ptr
  %Sl221 = select i1 %Cmp132, i32 %L49, i32 %L208
  %Cmp222 = icmp sgt <4 x i1> %Shuff51, %L110
  %L223 = load <4 x double>, ptr %PC138, align 32
  store i32 %E12, ptr %A, align 4
  %E224 = extractelement <16 x i64> %Shuff179, i32 132849
  %Shuff225 = shufflevector <1 x i32> %Sl23, <1 x i32> %Shuff59, <1 x i32> <i32 1>
  %I226 = insertelement <4 x i1> %Cmp48, i1 %Cmp215, i32 %Sl71
  %Tr227 = trunc i64 %B204 to i16
  %Sl228 = select i1 %Cmp32, i16 %E149, i16 %E149
  %Cmp229 = icmp ugt <8 x i16> %L33, %Shuff112
  %L230 = load i64, ptr %PC138, align 4
  store <8 x i16> %L33, ptr %PC, align 16
  %E231 = extractelement <4 x i1> %Cmp222, i32 %Sl71
  br i1 %E231, label %CF784, label %CF831

CF831:                                            ; preds = %CF784
  %Shuff232 = shufflevector <4 x i8> %Shuff43, <4 x i8> %Shuff20, <4 x i32> <i32 2, i32 4, i32 6, i32 0>
  %I233 = insertelement <16 x double> %Sl93, double %FC182, i32 %B45
  %B234 = ashr i16 16293, %B29
  %FC235 = uitofp <16 x i64> zeroinitializer to <16 x float>
  %Sl236 = select i1 %Cmp155, i1 true, i1 true
  br i1 %Sl236, label %CF784, label %CF829

CF829:                                            ; preds = %CF831
  %Cmp237 = icmp ugt <4 x i1> %Cmp17, %Cmp17
  %L238 = load float, ptr %PC30, align 4
  store <2 x i64> <i64 0, i64 -1>, ptr %PC138, align 16
  %E239 = extractelement <4 x i8> %I144, i32 %E12
  %Shuff240 = shufflevector <4 x i8> zeroinitializer, <4 x i8> %I52, <4 x i32> <i32 2, i32 4, i32 6, i32 0>
  %I241 = insertelement <4 x i1> %Cmp222, i1 %Cmp40, i32 %E
  %B242 = sdiv <8 x i16> %Shuff143, %Shuff187
  %Sl243 = select i1 %Cmp140, <4 x double> %FC115, <4 x double> %FC107
  %Cmp244 = icmp uge <1 x i8> zeroinitializer, %Tr62
  %L245 = load i64, ptr %Sl190, align 4
  store <4 x i16> %Se174, ptr %PC138, align 8
  %E246 = extractelement <8 x i16> %Sl146, i32 %BC
  %Shuff247 = shufflevector <4 x float> %FC, <4 x float> %FC, <4 x i32> <i32 6, i32 0, i32 2, i32 4>
  %I248 = insertelement <4 x i1> %Cmp222, i1 %Cmp24, i32 %BC
  %B249 = or <1 x i32> %Shuff158, %Shuff202
  %FC250 = fptoui <1 x double> %L148 to <1 x i8>
  %Sl251 = select <4 x i1> %Cmp48, <4 x i8> %Shuff232, <4 x i8> zeroinitializer
  %Cmp252 = icmp ult i1 %Cmp162, %Cmp24
  br i1 %Cmp252, label %CF784, label %CF805

CF805:                                            ; preds = %CF829
  %L253 = load <16 x float>, ptr %Sl16, align 64
  store i16 18437, ptr %0, align 2
  %E254 = extractelement <16 x double> %L65, i32 %E
  %Shuff255 = shufflevector <16 x i32> %B152, <16 x i32> %B152, <16 x i32> <i32 21, i32 poison, i32 25, i32 27, i32 29, i32 31, i32 poison, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 17, i32 19>
  %I256 = insertelement <1 x i32> zeroinitializer, i32 %B45, i32 %B45
  %B257 = and i64 %L11, %L163
  %ZE258 = fpext <4 x float> %Shuff67 to <4 x double>
  %Sl259 = select <8 x i1> %Cmp184, <8 x i16> %Shuff112, <8 x i16> zeroinitializer
  %Cmp260 = icmp sgt <8 x i16> %B129, zeroinitializer
  %L261 = load <4 x i16>, ptr %Sl190, align 8
  store float %BC205, ptr %Sl190, align 4
  %E262 = extractelement <8 x i1> %Cmp229, i32 %E
  br i1 %E262, label %CF784, label %CF794

CF794:                                            ; preds = %CF805
  %Shuff263 = shufflevector <2 x i32> %I136, <2 x i32> %B53, <2 x i32> <i32 3, i32 1>
  %I264 = insertelement <16 x i64> %Shuff7, i64 251161, i32 %3
  %Se265 = sext <2 x i32> zeroinitializer to <2 x i64>
  %Sl266 = select i1 %Cmp24, i1 %L87, i1 %Cmp32
  br i1 %Sl266, label %CF, label %CF767

CF767:                                            ; preds = %CF767, %CF818, %CF794
  %L267 = load <4 x i8>, ptr %A3, align 4
  store i16 %B234, ptr %PC138, align 2
  %E268 = extractelement <4 x float> %I113, i32 %E126
  %Shuff269 = shufflevector <16 x i64> %Shuff179, <16 x i64> zeroinitializer, <16 x i32> <i32 19, i32 21, i32 23, i32 25, i32 27, i32 29, i32 31, i32 1, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 poison>
  %I270 = insertelement <4 x i16> %I195, i16 %B29, i32 132849
  %B271 = udiv i16 %Tr227, %Se153
  %FC272 = fptoui double 0x5737B0566C35FAD4 to i1
  br i1 %FC272, label %CF767, label %CF818

CF818:                                            ; preds = %CF767
  %Sl273 = select <4 x i1> %L110, <4 x i8> %Sl63, <4 x i8> %Shuff20
  %Cmp274 = icmp ne i32 %Sl139, %3
  br i1 %Cmp274, label %CF767, label %CF772

CF772:                                            ; preds = %CF772, %CF818
  %L275 = load <4 x i16>, ptr %PC70, align 8
  store i1 %Cmp207, ptr %0, align 1
  %E276 = extractelement <4 x i1> %Cmp222, i32 %E
  br i1 %E276, label %CF772, label %CF821

CF821:                                            ; preds = %CF772
  %Shuff277 = shufflevector <1 x i32> %I151, <1 x i32> %Shuff59, <1 x i32> <i32 1>
  %I278 = insertelement <1 x i32> %Shuff135, i32 %L49, i32 %E
  %B279 = sub <1 x i32> %I278, %I14
  %FC280 = fptoui double 0x5737B0566C35FAD4 to i16
  %Sl281 = select i1 %Sl116, i8 %E74, i8 %Sl214
  %Cmp282 = icmp ugt <8 x i16> %B242, %Shuff187
  %L283 = load i64, ptr %PC30, align 4
  store <16 x i16> zeroinitializer, ptr %Sl16, align 32
  %E284 = extractelement <2 x i16> %B114, i32 %Sl221
  %Shuff285 = shufflevector <16 x i1> %Cmp94, <16 x i1> %Cmp191, <16 x i32> <i32 16, i32 18, i32 poison, i32 22, i32 24, i32 poison, i32 28, i32 30, i32 poison, i32 2, i32 4, i32 6, i32 8, i32 10, i32 12, i32 14>
  %I286 = insertelement <16 x i16> zeroinitializer, i16 16293, i32 %E126
  %B287 = ashr i16 -2255, %E58
  %FC288 = fptosi double %E254 to i16
  %Sl289 = select i1 %Cmp132, <4 x i16> %I195, <4 x i16> %I195
  %Cmp290 = icmp ule <8 x i16> zeroinitializer, %B242
  %L291 = load float, ptr %PC138, align 4
  store <16 x i8> <i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1>, ptr %Sl198, align 16
  %E292 = extractelement <16 x i64> %B167, i32 %3
  %Shuff293 = shufflevector <4 x i8> %Sl251, <4 x i8> %Sl131, <4 x i32> <i32 6, i32 0, i32 2, i32 4>
  %I294 = insertelement <1 x i1> %Cmp109, i1 %L87, i32 %E103
  %ZE295 = zext <4 x i8> zeroinitializer to <4 x i32>
  %Sl296 = select i1 true, i16 %E58, i16 %B69
  %Cmp297 = icmp ule i64 %E6, %L133
  br i1 %Cmp297, label %CF, label %CF766

CF766:                                            ; preds = %CF766, %CF802, %CF793, %CF779, %CF821
  %L298 = load <16 x i32>, ptr %Sl16, align 64
  store i8 %Sl214, ptr %PC138, align 1
  %E299 = extractelement <1 x i32> %Shuff135, i32 %Sl221
  %Shuff300 = shufflevector <4 x float> %Shuff247, <4 x float> %Shuff67, <4 x i32> <i32 3, i32 5, i32 7, i32 1>
  %I301 = insertelement <2 x i32> %Shuff263, i32 %E299, i32 %L208
  %B302 = udiv <4 x i8> %I60, %Sl183
  %FC303 = sitofp <1 x i8> %Tr62 to <1 x float>
  %Sl304 = select i1 %E231, <4 x i64> zeroinitializer, <4 x i64> %Se92
  %Cmp305 = icmp ugt <2 x i1> %Cmp176, %Cmp176
  %L306 = load i8, ptr %Sl190, align 1
  store <8 x i8> <i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1>, ptr %Sl16, align 8
  %E307 = extractelement <16 x float> %L253, i32 %E299
  %Shuff308 = shufflevector <1 x i8> zeroinitializer, <1 x i8> %FC250, <1 x i32> zeroinitializer
  %I309 = insertelement <16 x i64> %Shuff13, i64 %L245, i32 %E299
  %B310 = lshr i16 %Tr227, %E149
  %Tr311 = trunc <1 x i32> %B212 to <1 x i1>
  %Sl312 = select i1 %Cmp24, <1 x i1> %I294, <1 x i1> %Cmp244
  %Cmp313 = icmp eq <4 x i1> %Tr77, %Cmp17
  %L314 = load float, ptr %0, align 4
  store <4 x double> %FC107, ptr %Sl16, align 32
  %E315 = extractelement <4 x i8> %L267, i32 %Sl221
  %Shuff316 = shufflevector <2 x i32> %Sl206, <2 x i32> %Shuff263, <2 x i32> <i32 2, i32 0>
  %I317 = insertelement <2 x i32> %Shuff316, i32 %Sl221, i32 %BC
  %B318 = fadd float %BC205, %FC85
  %FC319 = sitofp i16 16293 to float
  %Sl320 = select i1 %E231, i16 -2255, i16 %E149
  %Cmp321 = icmp ugt <1 x i8> %Shuff308, %Tr62
  %L322 = load <8 x i32>, ptr %0, align 32
  store double 0xAE97BFB633957A34, ptr %Sl16, align 8
  %E323 = extractelement <1 x i32> %Shuff59, i32 %E299
  %Shuff324 = shufflevector <16 x i64> %Shuff120, <16 x i64> zeroinitializer, <16 x i32> <i32 19, i32 poison, i32 poison, i32 25, i32 27, i32 29, i32 31, i32 1, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 17>
  %I325 = insertelement <1 x i1> %Cmp199, i1 %E231, i32 %Sl221
  %FC326 = fptosi float %E268 to i16
  %Sl327 = select i1 %Sl116, <8 x i1> %Cmp290, <8 x i1> %Cmp184
  %Cmp328 = icmp eq i16 18437, 16293
  br i1 %Cmp328, label %CF766, label %CF799

CF799:                                            ; preds = %CF799, %CF820, %CF804, %CF766
  %L329 = load i32, ptr %A4, align 4
  store <2 x i64> %Se265, ptr %PC138, align 16
  %E330 = extractelement <1 x i32> zeroinitializer, i32 %E299
  %Shuff331 = shufflevector <4 x i8> %Shuff20, <4 x i8> %Shuff20, <4 x i32> <i32 0, i32 2, i32 4, i32 6>
  %I332 = insertelement <2 x i1> %L200, i1 %Cmp252, i32 %L49
  %B333 = sub i16 %E58, %B271
  %Se334 = sext <1 x i8> zeroinitializer to <1 x i16>
  %Sl335 = select <4 x i1> %Tr77, <4 x i1> %Cmp313, <4 x i1> %Tr
  %Cmp336 = icmp ugt i1 %E231, %Cmp328
  br i1 %Cmp336, label %CF799, label %CF820

CF820:                                            ; preds = %CF799
  %L337 = load <8 x i8>, ptr %0, align 8
  store float %L238, ptr %Sl16, align 4
  %E338 = extractelement <4 x float> %Sl161, i32 %L18
  %Shuff339 = shufflevector <1 x i32> %Shuff75, <1 x i32> zeroinitializer, <1 x i32> poison
  %I340 = insertelement <4 x i8> %Shuff218, i8 %Sl214, i32 %E299
  %B341 = xor <16 x i64> %Shuff165, %I36
  %Se342 = sext i16 %B69 to i32
  %Sl343 = select i1 %Cmp215, i8 %E66, i8 %Sl281
  %Cmp344 = icmp sgt <4 x i64> zeroinitializer, zeroinitializer
  %L345 = load i16, ptr %0, align 2
  store <4 x double> %FC107, ptr %0, align 32
  %E346 = extractelement <4 x i16> %Sl289, i32 %E299
  %Shuff347 = shufflevector <1 x i8> %Tr62, <1 x i8> %Tr62, <1 x i32> zeroinitializer
  %I348 = insertelement <1 x i32> zeroinitializer, i32 %E, i32 %E299
  %Sl349 = select i1 %Cmp24, <1 x i32> %I151, <1 x i32> %Shuff59
  %Cmp350 = icmp ne <1 x i8> zeroinitializer, %Tr62
  %L351 = load i64, ptr %Sl190, align 4
  store <2 x double> <double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF>, ptr %PC138, align 16
  %E352 = extractelement <8 x i16> %B242, i32 %E299
  %Shuff353 = shufflevector <16 x i16> zeroinitializer, <16 x i16> %I180, <16 x i32> <i32 poison, i32 24, i32 26, i32 28, i32 poison, i32 0, i32 2, i32 4, i32 poison, i32 8, i32 10, i32 12, i32 poison, i32 16, i32 18, i32 20>
  %I354 = insertelement <8 x i1> %Sl327, i1 %Cmp132, i32 132849
  %B355 = mul i16 %Sl320, %E217
  %ZE356 = zext i8 %E66 to i64
  %Sl357 = select i1 %Cmp132, i64 %L133, i64 251161
  %Cmp358 = icmp sgt i1 %E231, %Cmp252
  br i1 %Cmp358, label %CF799, label %CF804

CF804:                                            ; preds = %CF820
  %L359 = load <1 x i32>, ptr %PC70, align 4
  store i16 %B196, ptr %0, align 2
  %E360 = extractelement <1 x i32> %Shuff59, i32 %E
  %Shuff361 = shufflevector <8 x i1> %Cmp282, <8 x i1> %Cmp229, <8 x i32> <i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 poison>
  %I362 = insertelement <1 x i32> %Shuff158, i32 %E299, i32 %B45
  %B363 = or <8 x i32> %L322, %L322
  %FC364 = sitofp <4 x i1> %Cmp169 to <4 x float>
  %Sl365 = select i1 %Cmp328, i64 %ZE356, i64 %L245
  %Cmp366 = icmp uge <8 x i16> %Shuff143, zeroinitializer
  %L367 = load <4 x float>, ptr %PC70, align 16
  store float %B22, ptr %0, align 4
  %E368 = extractelement <1 x i32> %L359, i32 %E12
  %Shuff369 = shufflevector <1 x i32> %Sl349, <1 x i32> zeroinitializer, <1 x i32> <i32 1>
  %I370 = insertelement <16 x i64> %Shuff7, i64 %L351, i32 %BC
  %B371 = shl <8 x i16> %Shuff187, %L33
  %Tr372 = trunc <4 x i32> %I166 to <4 x i1>
  %Sl373 = select i1 true, float %FC85, float 0xC4F0BB4480000000
  %Cmp374 = icmp uge <8 x i1> %Cmp290, %Cmp229
  %L375 = load i32, ptr %PC138, align 4
  store <16 x double> %FC54, ptr %Sl16, align 128
  %E376 = extractelement <4 x i32> %Shuff89, i32 %E299
  %Shuff377 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %I173, <1 x i32> zeroinitializer
  %I378 = insertelement <1 x i32> %L359, i32 %Se342, i32 %E103
  %B379 = and i64 %FC213, 251161
  %BC380 = bitcast <2 x i32> %Se122 to <2 x float>
  %Sl381 = select i1 %E96, <2 x i32> %L216, <2 x i32> %Sl206
  %Cmp382 = icmp ne i64 %E224, %L351
  br i1 %Cmp382, label %CF799, label %CF800

CF800:                                            ; preds = %CF800, %CF804
  %L383 = load i8, ptr %0, align 1
  store <2 x i8> <i8 0, i8 -1>, ptr %Sl16, align 2
  %E384 = extractelement <8 x i1> %Cmp366, i32 %E299
  br i1 %E384, label %CF800, label %CF802

CF802:                                            ; preds = %CF800
  %Shuff385 = shufflevector <1 x i32> %L359, <1 x i32> %Shuff97, <1 x i32> zeroinitializer
  %I386 = insertelement <4 x float> %Shuff150, float 0xC4F0BB4480000000, i32 %E299
  %B387 = urem <4 x i8> %Shuff218, %Shuff293
  %ZE388 = zext i8 %B84 to i64
  %Sl389 = select i1 %Cmp155, <1 x i1> %Cmp350, <1 x i1> %Cmp101
  %Cmp390 = icmp sgt <16 x i64> %Shuff120, %I36
  %L391 = load float, ptr %PC138, align 4
  store <8 x i32> %L322, ptr %0, align 32
  %E392 = extractelement <1 x i8> zeroinitializer, i32 %L329
  %Shuff393 = shufflevector <4 x i64> %Se92, <4 x i64> zeroinitializer, <4 x i32> <i32 2, i32 4, i32 6, i32 0>
  %I394 = insertelement <1 x i16> %ZE197, i16 %E149, i32 %B45
  %B395 = shl <1 x i32> %Sl100, %Shuff339
  %FC396 = sitofp i16 %E352 to float
  %Sl397 = select i1 %L170, <8 x i32> %B363, <8 x i32> %L41
  %Cmp398 = icmp slt <4 x i1> %Cmp222, %Cmp17
  %L399 = load float, ptr %0, align 4
  store <8 x i16> %Sl259, ptr %PC70, align 16
  %E400 = extractelement <1 x i32> %Sl23, i32 %Sl71
  %Shuff401 = shufflevector <8 x i32> %L41, <8 x i32> %L322, <8 x i32> <i32 8, i32 10, i32 12, i32 14, i32 0, i32 2, i32 4, i32 poison>
  %I402 = insertelement <8 x i16> %Shuff82, i16 %B333, i32 %E400
  %FC403 = uitofp i8 %Sl281 to float
  %Sl404 = select i1 %Cmp382, i32 %Sl221, i32 %B45
  %Cmp405 = icmp sge i1 %E262, true
  br i1 %Cmp405, label %CF766, label %CF793

CF793:                                            ; preds = %CF802
  %L406 = load i64, ptr %Sl190, align 4
  %E407 = extractelement <1 x i32> %I14, i32 %E360
  %Shuff408 = shufflevector <4 x i8> %Shuff331, <4 x i8> %I121, <4 x i32> <i32 3, i32 5, i32 7, i32 1>
  %I409 = insertelement <1 x i32> %Shuff135, i32 %E323, i32 %Sl71
  %B410 = sub i32 %E400, %E299
  %Se411 = sext i1 %Cmp274 to i64
  %Sl412 = select <1 x i1> %Cmp101, <1 x i16> %ZE197, <1 x i16> %ZE197
  %Cmp413 = icmp ugt <16 x i32> %L298, %Tr38
  %L414 = load <4 x i8>, ptr %A, align 4
  store float %B22, ptr %0, align 4
  %E415 = extractelement <4 x float> %I386, i32 %E
  %Shuff416 = shufflevector <4 x i8> %I121, <4 x i8> %B160, <4 x i32> <i32 1, i32 poison, i32 poison, i32 poison>
  %I417 = insertelement <4 x i1> %Cmp344, i1 %Sl236, i32 %E103
  %B418 = shl i32 %E12, %E103
  %Tr419 = trunc i64 %B257 to i16
  %Sl420 = select i1 %Cmp297, i1 %Sl116, i1 %Cmp382
  br i1 %Sl420, label %CF766, label %CF779

CF779:                                            ; preds = %CF793
  %Cmp421 = icmp slt <4 x i16> %Se174, %Se174
  %L422 = load <4 x i64>, ptr %0, align 32
  store i1 %Sl116, ptr %0, align 1
  %E423 = extractelement <4 x float> %Shuff300, i32 %E323
  %Shuff424 = shufflevector <4 x i1> %Tr, <4 x i1> %Cmp398, <4 x i32> <i32 5, i32 7, i32 poison, i32 3>
  %I425 = insertelement <1 x i1> %Cmp244, i1 %Cmp328, i32 %E103
  %B426 = or <8 x i16> %Sl146, %B242
  %Sl427 = select i1 %Cmp336, i8 %E392, i8 %E66
  %Cmp428 = icmp uge i1 %L185, %Cmp56
  br i1 %Cmp428, label %CF766, label %CF771

CF771:                                            ; preds = %CF771, %CF807, %CF779
  %L429 = load <4 x i64>, ptr %PC220, align 32
  store i16 %E149, ptr %0, align 2
  %E430 = extractelement <1 x i32> %I173, i32 %Sl221
  %Shuff431 = shufflevector <1 x i32> %I409, <1 x i32> %B212, <1 x i32> <i32 1>
  %I432 = insertelement <4 x i1> %Cmp48, i1 %Cmp207, i32 %E299
  %B433 = srem i16 %B234, %FC326
  %FC434 = sitofp <1 x i1> %I425 to <1 x float>
  %Sl435 = select i1 %E231, <1 x i32> %Shuff97, <1 x i32> %Shuff369
  %Cmp436 = icmp ne <16 x i32> %L298, %Shuff255
  %L437 = load float, ptr %Sl190, align 4
  store <16 x i16> %Shuff353, ptr %PC30, align 32
  %E438 = extractelement <1 x i32> %Shuff135, i32 %E360
  %Shuff439 = shufflevector <16 x i64> %Shuff165, <16 x i64> %I309, <16 x i32> <i32 2, i32 4, i32 6, i32 poison, i32 poison, i32 12, i32 14, i32 poison, i32 18, i32 20, i32 poison, i32 24, i32 26, i32 28, i32 30, i32 0>
  %I440 = insertelement <2 x i32> %Shuff316, i32 %E299, i32 %Se342
  %B441 = urem i16 %B287, %Tr419
  %Se442 = sext <4 x i8> %I144 to <4 x i32>
  %Sl443 = select <1 x i1> %Cmp, <1 x i32> %I378, <1 x i32> %Shuff202
  %Cmp444 = icmp sge <1 x i32> %Shuff377, %I348
  %L445 = load <2 x i8>, ptr %0, align 2
  store i64 %L351, ptr %0, align 4
  %E446 = extractelement <1 x i32> %Sl443, i32 %E360
  %Shuff447 = shufflevector <1 x i8> %Shuff308, <1 x i8> %FC250, <1 x i32> poison
  %I448 = insertelement <16 x i64> %Shuff324, i64 %E224, i32 %E12
  %B449 = udiv i16 %E352, %B196
  %Tr450 = trunc i64 %FC213 to i8
  %Sl451 = select i1 %Cmp405, <4 x i8> %Shuff43, <4 x i8> %Shuff218
  %Cmp452 = icmp sgt i8 21, %E50
  br i1 %Cmp452, label %CF771, label %CF807

CF807:                                            ; preds = %CF771
  %L453 = load float, ptr %PC70, align 4
  %E454 = extractelement <4 x double> %Shuff172, i32 %E400
  %Shuff455 = shufflevector <8 x i32> %Shuff401, <8 x i32> %L322, <8 x i32> <i32 15, i32 1, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13>
  %I456 = insertelement <4 x i1> %Cmp344, i1 %Cmp252, i32 %E360
  %B457 = ashr i64 %L406, %B379
  %FC458 = fptoui float 0x44B9AA4D80000000 to i1
  br i1 %FC458, label %CF771, label %CF790

CF790:                                            ; preds = %CF807
  %Sl459 = select <8 x i1> %Cmp184, <8 x i1> %Cmp260, <8 x i1> %Cmp282
  %Cmp460 = icmp ult <4 x i8> %Shuff20, %L267
  %L461 = load <8 x float>, ptr %Sl16, align 32
  store i16 %FC280, ptr %0, align 2
  %E462 = extractelement <1 x i32> %Shuff158, i32 %E134
  %Shuff463 = shufflevector <1 x i32> zeroinitializer, <1 x i32> %Shuff339, <1 x i32> <i32 1>
  %I464 = insertelement <1 x float> %FC303, float %BC205, i32 %B45
  %B465 = sub i64 %L283, %B257
  %Tr466 = trunc i64 %L133 to i16
  %Sl467 = select i1 %Cmp428, <2 x i32> %I301, <2 x i32> %Shuff263
  %Cmp468 = icmp sgt <4 x i8> %I340, %I90
  %L469 = load i1, ptr %0, align 1
  br i1 %L469, label %CF, label %CF765

CF765:                                            ; preds = %CF765, %CF809, %CF815, %CF790
  store <16 x i8> <i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1, i8 0, i8 -1>, ptr %Sl16, align 16
  %E470 = extractelement <1 x i32> %Shuff104, i32 %Sl139
  %Shuff471 = shufflevector <4 x i8> %I68, <4 x i8> zeroinitializer, <4 x i32> <i32 poison, i32 6, i32 0, i32 2>
  %I472 = insertelement <1 x i16> %Sl412, i16 %Tr419, i32 0
  %FC473 = sitofp <16 x i64> %Shuff7 to <16 x float>
  %Sl474 = select i1 %Cmp32, <2 x i32> zeroinitializer, <2 x i32> %I
  %Cmp475 = icmp ult <4 x i8> %Sl251, %Shuff293
  %L476 = load i64, ptr %Sl198, align 4
  store <4 x i16> %Se174, ptr %0, align 8
  %E477 = extractelement <1 x i32> %Shuff59, i32 %E438
  %Shuff478 = shufflevector <1 x i32> %Shuff, <1 x i32> %I362, <1 x i32> zeroinitializer
  %I479 = insertelement <4 x i8> %Shuff408, i8 %Sl154, i32 %B45
  %B480 = and <16 x i32> %Shuff255, %Tr38
  %Se481 = sext <4 x i1> %I188 to <4 x i64>
  %Sl482 = select <4 x i1> %Tr, <4 x i8> %Shuff20, <4 x i8> %Shuff293
  %Cmp483 = icmp uge i64 %L351, %L283
  br i1 %Cmp483, label %CF765, label %CF806

CF806:                                            ; preds = %CF806, %CF765
  %L484 = load <1 x float>, ptr %0, align 4
  store i1 %Cmp56, ptr %PC220, align 1
  %E485 = extractelement <8 x i1> %Sl459, i32 %E12
  br i1 %E485, label %CF806, label %CF809

CF809:                                            ; preds = %CF806
  %Shuff486 = shufflevector <4 x i16> %L261, <4 x i16> %Se174, <4 x i32> <i32 3, i32 5, i32 7, i32 poison>
  %I487 = insertelement <4 x i1> %Cmp17, i1 %Sl420, i32 %E299
  %B488 = shl i16 %B310, %Se153
  %Tr489 = trunc <8 x i32> %Shuff401 to <8 x i8>
  %Sl490 = select <1 x i1> %Cmp101, <1 x i32> %Sl435, <1 x i32> %Shuff
  %Cmp491 = icmp eq <4 x i1> %Cmp468, %L110
  %L492 = load <8 x i8>, ptr %0, align 8
  store i32 %E299, ptr %0, align 4
  %E493 = extractelement <16 x i64> %Shuff13, i32 %E299
  %Shuff494 = shufflevector <4 x float> %Shuff247, <4 x float> %FC364, <4 x i32> <i32 poison, i32 3, i32 5, i32 7>
  %I495 = insertelement <1 x i32> %Shuff158, i32 %L208, i32 %L208
  %B496 = mul i64 %ZE356, %L406
  %FC497 = sitofp <16 x i64> %Shuff439 to <16 x float>
  %Sl498 = select i1 %Sl236, i16 %E284, i16 %B271
  %L499 = load i64, ptr %0, align 4
  store <4 x i32> zeroinitializer, ptr %0, align 16
  %E500 = extractelement <1 x i1> %Cmp321, i32 %E103
  br i1 %E500, label %CF765, label %CF770

CF770:                                            ; preds = %CF770, %CF808, %CF809
  %Shuff501 = shufflevector <8 x i1> %L192, <8 x i1> %Cmp184, <8 x i32> <i32 poison, i32 0, i32 2, i32 4, i32 poison, i32 8, i32 poison, i32 12>
  %I502 = insertelement <1 x i32> zeroinitializer, i32 %E446, i32 %E12
  %B503 = fmul <4 x float> %FC145, %Shuff300
  %FC504 = uitofp <1 x i8> %Tr62 to <1 x double>
  %Sl505 = select i1 %Cmp452, i32 %Se342, i32 %E299
  %Cmp506 = icmp sge <4 x i64> zeroinitializer, %Sl304
  %L507 = load i16, ptr %PC70, align 2
  %E508 = extractelement <2 x i32> %I, i32 %E462
  %Shuff509 = shufflevector <1 x i32> %Shuff75, <1 x i32> %I83, <1 x i32> poison
  %I510 = insertelement <16 x double> %Sl93, double %E454, i32 %E299
  %B511 = add <4 x i8> %Shuff471, %B387
  %FC512 = sitofp <1 x i32> %Shuff339 to <1 x double>
  %Sl513 = select i1 %FC272, float %Sl373, float %L291
  %Cmp514 = icmp sgt <4 x i8> %I121, %B511
  %L515 = load <8 x i8>, ptr %PC70, align 8
  store i64 %L283, ptr %0, align 4
  %E516 = extractelement <1 x i32> zeroinitializer, i32 %Sl505
  %Shuff517 = shufflevector <1 x i32> %I278, <1 x i32> %I173, <1 x i32> <i32 1>
  %I518 = insertelement <4 x i8> %Shuff43, i8 %Sl281, i32 %E134
  %B519 = frem double 0x58238842DB21C0C0, %FC182
  %ZE520 = zext <8 x i1> %Sl459 to <8 x i64>
  %Sl521 = select i1 %Cmp452, <4 x i1> %Cmp421, <4 x i1> %Cmp514
  %Cmp522 = icmp eq <16 x i32> %B152, %Tr38
  %L523 = load float, ptr %Sl16, align 4
  store <8 x i64> %ZE520, ptr %PC30, align 64
  %E524 = extractelement <4 x i64> %Shuff393, i32 %B410
  %Shuff525 = shufflevector <1 x i32> %Shuff158, <1 x i32> %Shuff478, <1 x i32> poison
  %I526 = insertelement <8 x i1> %Cmp374, i1 true, i32 %E103
  %B527 = fmul float %B318, %E307
  %Tr528 = trunc i64 %L102 to i8
  %Sl529 = select <1 x i1> %Cmp, <1 x i8> %Shuff347, <1 x i8> %Shuff308
  %Cmp530 = icmp slt <1 x i8> %Shuff447, %Shuff308
  %L531 = load <4 x i8>, ptr %PC138, align 4
  store float %L238, ptr %0, align 4
  %E532 = extractelement <16 x i64> zeroinitializer, i32 %E400
  %Shuff533 = shufflevector <4 x i1> %Shuff127, <4 x i1> %Cmp398, <4 x i32> <i32 3, i32 5, i32 7, i32 poison>
  %I534 = insertelement <16 x i1> %Shuff285, i1 %Sl86, i32 %E360
  %B535 = fadd double %FC182, %E454
  %Sl536 = select i1 %Cmp56, i32 0, i32 %E126
  %Cmp537 = icmp eq <4 x i64> %Sl304, zeroinitializer
  %L538 = load float, ptr %0, align 4
  store <8 x i32> %Shuff455, ptr %0, align 32
  %E539 = extractelement <8 x i16> %Shuff187, i32 %E299
  %Shuff540 = shufflevector <2 x i1> %L200, <2 x i1> %Cmp305, <2 x i32> <i32 2, i32 0>
  %I541 = insertelement <1 x i32> %Sl23, i32 %E438, i32 %E323
  %B542 = sdiv <1 x i32> %L359, %I83
  %Tr543 = trunc i16 %E164 to i1
  br i1 %Tr543, label %CF770, label %CF808

CF808:                                            ; preds = %CF770
  %Sl544 = select i1 %Cmp24, i16 %L507, i16 %Se153
  %Cmp545 = icmp sge <1 x i1> %Cmp101, %I425
  %L546 = load float, ptr %Sl190, align 4
  store <8 x double> <double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF, double 0.000000e+00, double 0xFFFFFFFFFFFFFFFF>, ptr %0, align 64
  %E547 = extractelement <8 x i1> %Shuff361, i32 %E323
  br i1 %E547, label %CF770, label %CF773

CF773:                                            ; preds = %CF773, %CF808
  %Shuff548 = shufflevector <4 x double> %Shuff172, <4 x double> %Shuff172, <4 x i32> <i32 6, i32 poison, i32 2, i32 4>
  %I549 = insertelement <4 x float> %Shuff247, float %E338, i32 %E126
  %B550 = shl <2 x i64> %Se265, %Se265
  %Tr551 = trunc i32 %E400 to i8
  %Sl552 = select <1 x i1> %I294, <1 x i32> %Shuff97, <1 x i32> %Shuff202
  %Cmp553 = icmp uge <1 x i32> %B212, %Shuff59
  %L554 = load <4 x double>, ptr %PC138, align 32
  store i8 %E239, ptr %Sl190, align 1
  %E555 = extractelement <1 x i32> %Shuff135, i32 %Sl505
  %Shuff556 = shufflevector <1 x i32> %Shuff525, <1 x i32> %Shuff, <1 x i32> <i32 1>
  %I557 = insertelement <1 x i32> %Shuff277, i32 %E186, i32 %Sl139
  %B558 = frem <1 x float> %L484, %FC303
  %ZE559 = zext <4 x i1> %Cmp344 to <4 x i8>
  %Sl560 = select i1 %Cmp483, i16 %E34, i16 %B234
  %Cmp561 = icmp sge <16 x i64> %I309, zeroinitializer
  %L562 = load <4 x i32>, ptr %PC30, align 16
  store i32 %E299, ptr %0, align 4
  %E563 = extractelement <8 x i32> %Shuff455, i32 %E126
  %Shuff564 = shufflevector <8 x i1> %Shuff361, <8 x i1> %Cmp184, <8 x i32> <i32 11, i32 poison, i32 15, i32 1, i32 3, i32 5, i32 7, i32 poison>
  %I565 = insertelement <4 x i1> %Cmp537, i1 %Cmp297, i32 0
  %B566 = fsub <4 x double> %Shuff172, %Shuff172
  %ZE567 = zext <4 x i8> %I68 to <4 x i16>
  %Sl568 = select i1 %Cmp405, <1 x float> %B558, <1 x float> %FC303
  %Cmp569 = icmp ne <4 x i1> %Cmp169, %Tr
  %L570 = load double, ptr %PC138, align 8
  store <4 x i8> %Shuff331, ptr %PC220, align 4
  %E571 = extractelement <8 x i1> %Cmp282, i32 %E462
  br i1 %E571, label %CF773, label %CF815

CF815:                                            ; preds = %CF773
  %Shuff572 = shufflevector <2 x i32> %Shuff316, <2 x i32> zeroinitializer, <2 x i32> <i32 2, i32 0>
  %I573 = insertelement <1 x i32> %Shuff377, i32 %Sl505, i32 %L329
  %B574 = udiv i16 %E539, %B29
  %Tr575 = fptrunc <1 x double> %FC512 to <1 x float>
  %Sl576 = select i1 %L469, i1 %FC272, i1 %Cmp328
  br i1 %Sl576, label %CF765, label %CF768

CF768:                                            ; preds = %CF768, %CF814, %CF815
  %Cmp577 = icmp sge <4 x i1> %Shuff533, %I456
  %L578 = load <4 x float>, ptr %0, align 16
  store float %E415, ptr %PC138, align 4
  %E579 = extractelement <8 x i32> %Shuff455, i32 %E508
  %Shuff580 = shufflevector <16 x float> %B181, <16 x float> %L95, <16 x i32> <i32 27, i32 29, i32 31, i32 1, i32 3, i32 poison, i32 7, i32 9, i32 11, i32 poison, i32 15, i32 17, i32 19, i32 21, i32 23, i32 poison>
  %I581 = insertelement <8 x i8> %Tr489, i8 %Tr450, i32 %E470
  %B582 = lshr i16 %E284, %B287
  %FC583 = uitofp i16 %B271 to float
  %Sl584 = select i1 true, i1 %Cmp79, i1 %E500
  br i1 %Sl584, label %CF768, label %CF812

CF812:                                            ; preds = %CF812, %CF816, %CF768
  %Cmp585 = icmp sge <4 x i32> %Sl10, %I159
  %L586 = load i32, ptr %Sl190, align 4
  store <8 x i8> %Tr489, ptr %PC138, align 8
  %E587 = extractelement <16 x i32> %Shuff255, i32 %Sl221
  %Shuff588 = shufflevector <4 x i8> %I144, <4 x i8> %Shuff240, <4 x i32> <i32 0, i32 2, i32 4, i32 6>
  %I589 = insertelement <1 x i8> %Sl529, i8 %E50, i32 132849
  %B590 = xor <8 x i16> %L33, %B426
  %FC591 = uitofp <4 x i1> %Cmp169 to <4 x double>
  %Sl592 = select i1 %Cmp382, i32 %E171, i32 %E126
  %Cmp593 = icmp ne <16 x i64> %Shuff439, %Shuff165
  %L594 = load i1, ptr %PC138, align 1
  br i1 %L594, label %CF812, label %CF816

CF816:                                            ; preds = %CF812
  store <2 x float> %BC380, ptr %0, align 8
  %E595 = extractelement <16 x float> %FC497, i32 %E323
  %Shuff596 = shufflevector <4 x i32> zeroinitializer, <4 x i32> %Se442, <4 x i32> <i32 6, i32 0, i32 poison, i32 4>
  %I597 = insertelement <4 x i1> %I487, i1 %Tr543, i32 %L177
  %FC598 = sitofp <1 x i32> %Shuff517 to <1 x double>
  %Sl599 = select i1 %Cmp382, <1 x i16> %Sl412, <1 x i16> %I472
  %Cmp600 = icmp slt <2 x i32> %Shuff316, %Sl206
  %L601 = load i64, ptr %Sl16, align 4
  store <2 x i16> %L, ptr %PC138, align 4
  %E602 = extractelement <8 x i16> zeroinitializer, i32 %E134
  %Shuff603 = shufflevector <8 x i1> %Cmp282, <8 x i1> %Cmp184, <8 x i32> <i32 4, i32 6, i32 8, i32 10, i32 12, i32 14, i32 poison, i32 2>
  %I604 = insertelement <16 x i16> %Shuff353, i16 %B433, i32 %E103
  %B605 = urem <8 x i32> %Shuff455, %Sl397
  %Tr606 = trunc <16 x i64> %Shuff165 to <16 x i1>
  %Sl607 = select i1 %FC272, <4 x i1> %Cmp460, <4 x i1> %I432
  %Cmp608 = icmp ne <16 x i1> %Cmp522, %Cmp561
  %L609 = load i8, ptr %0, align 1
  store <8 x float> %L461, ptr %0, align 32
  %E610 = extractelement <2 x i1> %Cmp600, i32 %E171
  br i1 %E610, label %CF812, label %CF814

CF814:                                            ; preds = %CF816
  %Shuff611 = shufflevector <1 x i32> %Shuff277, <1 x i32> %Shuff202, <1 x i32> zeroinitializer
  %I612 = insertelement <16 x float> %Shuff580, float %FC85, i32 %E299
  %FC613 = fptoui double %L570 to i16
  %Sl614 = select <4 x i1> %I565, <4 x i32> %Sl10, <4 x i32> %I159
  %Cmp615 = icmp ugt <1 x i32> %I256, %B212
  %L616 = load <8 x double>, ptr %0, align 64
  store i64 %B457, ptr %0, align 4
  %E617 = extractelement <4 x i1> %Cmp506, i32 %B45
  br i1 %E617, label %CF768, label %CF783

CF783:                                            ; preds = %CF783, %CF824, %CF803, %CF788, %CF814
  %Shuff618 = shufflevector <4 x i1> %I417, <4 x i1> %Tr, <4 x i32> <i32 1, i32 3, i32 5, i32 7>
  %I619 = insertelement <1 x i32> %Shuff556, i32 %E134, i32 %E299
  %B620 = sdiv <8 x i16> %L118, %I402
  %FC621 = fptoui float %L238 to i1
  br i1 %FC621, label %CF783, label %CF824

CF824:                                            ; preds = %CF783
  %Sl622 = select <16 x i1> %Cmp413, <16 x i64> %Shuff13, <16 x i64> %Shuff439
  %Cmp623 = icmp ule i16 %B449, %B271
  br i1 %Cmp623, label %CF783, label %CF798

CF798:                                            ; preds = %CF798, %CF824
  %L624 = load <1 x i16>, ptr %0, align 2
  store float %Sl373, ptr %0, align 4
  %E625 = extractelement <16 x double> %I510, i32 %E299
  %Shuff626 = shufflevector <4 x i1> %Cmp506, <4 x i1> %Cmp506, <4 x i32> <i32 7, i32 1, i32 3, i32 5>
  %I627 = insertelement <16 x float> %L95, float %FC85, i32 %Sl71
  %FC628 = sitofp i32 %E516 to double
  %Sl629 = select i1 true, <8 x double> %L616, <8 x double> %L616
  %Cmp630 = icmp uge i32 %B410, %E299
  br i1 %Cmp630, label %CF798, label %CF803

CF803:                                            ; preds = %CF798
  %L631 = load float, ptr %0, align 4
  %E632 = extractelement <1 x i32> %Shuff463, i32 %E323
  %Shuff633 = shufflevector <16 x i64> %Shuff165, <16 x i64> %I264, <16 x i32> <i32 27, i32 29, i32 31, i32 1, i32 3, i32 poison, i32 7, i32 9, i32 poison, i32 13, i32 15, i32 17, i32 19, i32 21, i32 poison, i32 25>
  %I634 = insertelement <4 x i32> %Se442, i32 %E178, i32 %Sl71
  %B635 = srem i32 %Sl505, %E632
  %ZE636 = zext <16 x i1> %Cmp561 to <16 x i32>
  %Sl637 = select i1 %Tr543, i1 %Cmp405, i1 %L185
  br i1 %Sl637, label %CF783, label %CF788

CF788:                                            ; preds = %CF803
  %Cmp638 = icmp uge i32 %E587, %E508
  br i1 %Cmp638, label %CF783, label %CF785

CF785:                                            ; preds = %CF788
  %L639 = load <8 x i32>, ptr %PC30, align 32
  store i16 %Sl228, ptr %0, align 2
  %E640 = extractelement <4 x i64> zeroinitializer, i32 %B45
  %Shuff641 = shufflevector <4 x i8> %Sl183, <4 x i8> %Sl451, <4 x i32> <i32 1, i32 3, i32 5, i32 poison>
  %I642 = insertelement <4 x i1> %Cmp577, i1 %Cmp215, i32 %E299
  %B643 = shl <16 x i64> %Sl, %I448
  %FC644 = sitofp <8 x i16> %B371 to <8 x double>
  %Sl645 = select i1 %Cmp155, <16 x i1> %I534, <16 x i1> %Cmp522
  %Cmp646 = icmp ult <4 x i1> %I226, %Cmp17
  %L647 = load double, ptr %Sl16, align 8
  store <8 x i64> %ZE520, ptr %0, align 64
  %E648 = extractelement <1 x i32> %Shuff517, i32 %BC
  %Shuff649 = shufflevector <8 x double> %Sl629, <8 x double> %L616, <8 x i32> <i32 0, i32 poison, i32 4, i32 6, i32 poison, i32 poison, i32 12, i32 14>
  %I650 = insertelement <8 x i8> %L337, i8 %Sl154, i32 %E299
  %FC651 = sitofp <8 x i32> %B363 to <8 x float>
  %Sl652 = select i1 %Cmp630, <4 x i64> %L422, <4 x i64> %Se92
  %Cmp653 = icmp slt <16 x i16> %FC130, %I604
  %L654 = load i64, ptr %PC138, align 4
  store <8 x double> %FC644, ptr %0, align 64
  %E655 = extractelement <8 x i32> %Sl397, i32 %E299
  %Shuff656 = shufflevector <1 x i32> zeroinitializer, <1 x i32> zeroinitializer, <1 x i32> zeroinitializer
  %I657 = insertelement <1 x i8> %Sl529, i8 %5, i32 %E632
  %B658 = mul i16 %Se, %B449
  %FC659 = sitofp i8 %Tr528 to double
  %Sl660 = select i1 %Cmp79, i8 %Tr450, i8 %Tr551
  %Cmp661 = icmp eq <8 x i32> %L639, %L322
  %L662 = load <4 x i64>, ptr %0, align 32
  store double 0xAE97BFB633957A34, ptr %0, align 8
  %E663 = extractelement <1 x i32> %Shuff75, i32 %E400
  %Shuff664 = shufflevector <1 x i32> %Shuff135, <1 x i32> %Shuff277, <1 x i32> <i32 1>
  %I665 = insertelement <4 x i64> %Shuff393, i64 %E640, i32 %Sl592
  %B666 = or i16 %Sl228, %E602
  %FC667 = fptoui float %L238 to i16
  %Sl668 = select i1 %Cmp358, i32 %Sl221, i32 %E103
  %Cmp669 = icmp slt <4 x i8> %I52, %Shuff588
  %L670 = load i1, ptr %Sl190, align 1
  br i1 %L670, label %CF, label %CF763

CF763:                                            ; preds = %CF763, %CF813, %CF785
  store <2 x i32> %I440, ptr %0, align 8
  %E671 = extractelement <1 x i32> %L359, i32 %Sl505
  %Shuff672 = shufflevector <1 x i8> %Shuff308, <1 x i8> %Shuff308, <1 x i32> zeroinitializer
  %I673 = insertelement <4 x double> %FC107, double %E625, i32 %Sl505
  %ZE674 = zext <8 x i1> %Shuff501 to <8 x i8>
  %Sl675 = select i1 %L469, ptr %1, ptr %Sl190
  %Cmp676 = fcmp olt float %E595, %FC403
  br i1 %Cmp676, label %CF763, label %CF813

CF813:                                            ; preds = %CF763
  %L677 = load <2 x i1>, ptr %Sl675, align 1
  store i64 %B457, ptr %Sl675, align 4
  %E678 = extractelement <16 x i32> %ZE636, i32 %E632
  %Shuff679 = shufflevector <1 x i32> %Shuff664, <1 x i32> %Shuff431, <1 x i32> <i32 1>
  %I680 = insertelement <1 x i32> %Shuff277, i32 %Sl536, i32 %E663
  %B681 = lshr <8 x i32> %Shuff455, %L322
  %Se682 = sext i1 %Tr543 to i64
  %Sl683 = select i1 %E500, i1 %Cmp428, i1 %Tr543
  br i1 %Sl683, label %CF763, label %CF764

CF764:                                            ; preds = %CF764, %CF813
  %Cmp684 = icmp uge <1 x i32> %I362, %Shuff277
  %L685 = load i1, ptr %Sl675, align 1
  br i1 %L685, label %CF764, label %CF822

CF822:                                            ; preds = %CF764
  store <8 x i16> %B242, ptr %Sl675, align 16
  %E686 = extractelement <1 x i32> %Shuff158, i32 %E632
  %Shuff687 = shufflevector <1 x i32> %Shuff656, <1 x i32> %I409, <1 x i32> zeroinitializer
  %I688 = insertelement <1 x i32> %Shuff75, i32 %E632, i32 %Sl536
  %B689 = or <1 x i32> %Sl552, %Sl443
  %Tr690 = trunc <2 x i16> %L to <2 x i1>
  %Sl691 = select i1 %E571, <1 x i16> %ZE197, <1 x i16> %Se334
  %Cmp692 = icmp slt i1 %Cmp32, %E610
  br i1 %Cmp692, label %CF, label %CF762

CF762:                                            ; preds = %CF762, %CF787, %CF828, %CF822
  %L693 = load i16, ptr %Sl675, align 2
  store <4 x i16> %Se174, ptr %Sl190, align 8
  %E694 = extractelement <16 x i16> %Shuff353, i32 %E142
  %Shuff695 = shufflevector <4 x float> %Sl161, <4 x float> %FC, <4 x i32> <i32 2, i32 4, i32 poison, i32 poison>
  %I696 = insertelement <16 x i1> %Cmp522, i1 %E610, i32 %E323
  %B697 = mul i32 %Sl505, %E470
  %Tr698 = trunc i64 %E224 to i32
  %Sl699 = select i1 %Cmp405, i1 true, i1 %Cmp328
  br i1 %Sl699, label %CF762, label %CF787

CF787:                                            ; preds = %CF762
  %Cmp700 = icmp sgt i1 %L594, %Sl637
  br i1 %Cmp700, label %CF762, label %CF780

CF780:                                            ; preds = %CF780, %CF787
  %L701 = load double, ptr %Sl190, align 8
  store <4 x i64> %Sl304, ptr %Sl675, align 32
  %E702 = extractelement <4 x i1> %Shuff210, i32 %BC
  br i1 %E702, label %CF780, label %CF828

CF828:                                            ; preds = %CF780
  %Shuff703 = shufflevector <8 x i1> %Cmp282, <8 x i1> %Cmp661, <8 x i32> <i32 poison, i32 0, i32 2, i32 4, i32 6, i32 8, i32 10, i32 12>
  %I704 = insertelement <16 x i64> %B167, i64 %E6, i32 %E299
  %B705 = ashr <16 x i32> %L298, %Shuff255
  %ZE706 = zext i1 %Cmp428 to i16
  %Sl707 = select i1 %Sl683, i16 %Sl108, i16 %FC613
  %Cmp708 = fcmp ord double %B519, %E454
  br i1 %Cmp708, label %CF762, label %CF769

CF769:                                            ; preds = %CF769, %CF827, %CF828
  %L709 = load <2 x i32>, ptr %Sl675, align 8
  store i32 %E299, ptr %Sl675, align 4
  %E710 = extractelement <4 x i8> %Shuff20, i32 %B697
  %Shuff711 = shufflevector <4 x i8> %I219, <4 x i8> %B387, <4 x i32> <i32 3, i32 5, i32 7, i32 poison>
  %I712 = insertelement <4 x i8> %Shuff588, i8 21, i32 %Se342
  %B713 = xor i8 %Tr551, %L609
  %PC714 = bitcast ptr %Sl675 to ptr
  %Sl715 = select i1 %Cmp24, float %L538, float %FC85
  %Cmp716 = fcmp une double 0x99ABD3CAB0A9A048, %E454
  br i1 %Cmp716, label %CF769, label %CF827

CF827:                                            ; preds = %CF769
  %L717 = load double, ptr %Sl675, align 8
  store <8 x i64> %ZE520, ptr %Sl675, align 64
  %E718 = extractelement <1 x i8> %Shuff672, i32 %Se342
  %Shuff719 = shufflevector <16 x i64> %Shuff269, <16 x i64> zeroinitializer, <16 x i32> <i32 poison, i32 0, i32 2, i32 4, i32 6, i32 8, i32 10, i32 12, i32 14, i32 16, i32 18, i32 20, i32 22, i32 poison, i32 26, i32 28>
  %I720 = insertelement <1 x i32> %Shuff104, i32 %E632, i32 %E462
  %B721 = add <1 x i32> %Sl435, %Shuff509
  %FC722 = sitofp i1 %L594 to float
  %Sl723 = select i1 %E610, <1 x i32> %B249, <1 x i32> %Shuff611
  %Cmp724 = icmp ult <1 x i1> %Cmp244, %Cmp615
  %L725 = load float, ptr %Sl675, align 4
  store <1 x double> %FC598, ptr %PC138, align 8
  %E726 = extractelement <1 x i32> %Shuff97, i32 %BC
  %Shuff727 = shufflevector <8 x i1> %Sl327, <8 x i1> %Cmp260, <8 x i32> <i32 12, i32 14, i32 0, i32 2, i32 4, i32 6, i32 8, i32 10>
  %I728 = insertelement <1 x i32> %Shuff135, i32 %E678, i32 %E111
  %FC729 = fptosi <16 x float> %L253 to <16 x i1>
  %Sl730 = select i1 %Cmp428, <2 x i32> %Sl474, <2 x i32> %Shuff316
  %Cmp731 = icmp ugt i16 %E149, %B666
  br i1 %Cmp731, label %CF769, label %CF777

CF777:                                            ; preds = %CF777, %CF825, %CF797, %CF827
  %L732 = load i64, ptr %Sl675, align 4
  store <8 x i32> %B681, ptr %Sl675, align 32
  %E733 = extractelement <1 x i32> %Shuff478, i32 %BC
  %Shuff734 = shufflevector <8 x i32> %Sl397, <8 x i32> %L322, <8 x i32> <i32 10, i32 poison, i32 poison, i32 0, i32 2, i32 4, i32 6, i32 8>
  %I735 = insertelement <1 x i1> %Cmp321, i1 %Cmp676, i32 %Se342
  %B736 = sub <4 x i32> %I166, %ZE295
  %Sl737 = select <8 x i1> %Cmp184, <8 x i1> %Cmp661, <8 x i1> %Sl459
  %Cmp738 = fcmp uge <8 x float> %L461, %L461
  %L739 = load <8 x float>, ptr %Sl190, align 32
  store float %FC722, ptr %Sl675, align 4
  %E740 = extractelement <4 x i8> %B61, i32 %Sl592
  %Shuff741 = shufflevector <1 x i32> %Shuff158, <1 x i32> %Shuff135, <1 x i32> <i32 1>
  %I742 = insertelement <16 x i64> %B643, i64 %E640, i32 %E632
  %B743 = srem <1 x i32> %Shuff135, %Sl23
  %FC744 = sitofp <1 x i32> %Shuff679 to <1 x float>
  %Sl745 = select i1 %Sl116, i8 %E74, i8 %E710
  %Cmp746 = icmp uge <1 x i32> %I541, %Shuff158
  %L747 = load <8 x i1>, ptr %Sl675, align 1
  store float %L291, ptr %Sl675, align 4
  %E748 = extractelement <4 x i8> %L267, i32 %Sl592
  %Shuff749 = shufflevector <2 x i32> %I317, <2 x i32> %Shuff572, <2 x i32> <i32 3, i32 1>
  %I750 = insertelement <4 x i1> %Shuff210, i1 %Cmp24, i32 %Sl221
  %Tr751 = trunc i32 %E430 to i1
  br i1 %Tr751, label %CF777, label %CF825

CF825:                                            ; preds = %CF777
  %Sl752 = select i1 %Cmp207, i32 %B635, i32 %E126
  %Cmp753 = icmp ule i32 %E209, %E299
  br i1 %Cmp753, label %CF777, label %CF797

CF797:                                            ; preds = %CF825
  %L754 = load i64, ptr %PC138, align 4
  store <2 x i8> %L445, ptr %PC714, align 2
  %E755 = extractelement <16 x i1> %Cmp436, i32 %E470
  br i1 %E755, label %CF777, label %CF781

CF781:                                            ; preds = %CF781, %CF797
  %Shuff756 = shufflevector <2 x i32> zeroinitializer, <2 x i32> %I440, <2 x i32> <i32 poison, i32 0>
  %I757 = insertelement <4 x i64> zeroinitializer, i64 %L732, i32 %E632
  %FC758 = fptosi <16 x float> %B181 to <16 x i32>
  %Sl759 = select i1 %FC272, <1 x i32> %L359, <1 x i32> %Shuff
  %Cmp760 = icmp slt i1 %Sl576, %L670
  br i1 %Cmp760, label %CF781, label %CF792

CF792:                                            ; preds = %CF781
  store double %L717, ptr %0, align 8
  store i16 %B271, ptr %PC70, align 2
  store double %E625, ptr %Sl675, align 8
  store i1 %Cmp630, ptr %Sl675, align 1
  store i64 %L25, ptr %Sl675, align 4
  ret void
}
