MACRO_ACTIONS = [
    # --- Discovered via n-gram analysis on 5,412 benchmarks (v5 Dataset) ---
    ["function(sroa)", "function(simplifycfg)"],             # Action 0 (Top Rank)
    ["function(mem2reg)", "function(sroa)"],                # Action 1
    ["function(sroa)", "function(instcombine<no-verify-fixpoint>)"], # Action 2
    ["function(mem2reg)", "function(simplifycfg)"],          # Action 3
    ["function(sroa)", "function(early-cse)"],               # Action 4
    ["function(mem2reg)", "function(instcombine<no-verify-fixpoint>)"], # Action 5
    ["function(early-cse)", "function(sroa)"],              # Action 6
    ["function(instcombine<no-verify-fixpoint>)", "function(sroa)"], # Action 7
    ["function(early-cse)", "function(mem2reg)"],            # Action 8
    ["function(mem2reg)", "function(early-cse)"],            # Action 9
    ["function(sroa)", "function(gvn)"],                    # Action 10
    ["function(simplifycfg)", "function(sroa)"],            # Action 11
    ["function(sroa)", "function(mem2reg)"],                # Action 12
    ["function(instcombine<no-verify-fixpoint>)", "function(simplifycfg)"], # Action 13
    ["function(newgvn)", "function(mem2reg)"],              # Action 14
    ["function(sroa)", "function(indvars)"],                # Action 15
    ["function(mem2reg)", "function(gvn)"],                  # Action 16
    ["function(sroa)", "function(reassociate)"],            # Action 17
    ["function(instcombine<no-verify-fixpoint>)", "function(gvn)"], # Action 18
    ["function(gvn)", "function(sroa)"],                    # Action 19
    ["function(simplifycfg)", "function(mem2reg)"],          # Action 20
    ["function(sroa)", "function(newgvn)"],                 # Action 21
    ["function(mem2reg)", "function(jump-threading)"],       # Action 22
    ["ipsccp", "function(sroa)"],                           # Action 23
    ["globalopt", "function(sroa)"],                        # Action 24
    
    # --- Action 25: TERMINATE ---
    ["TERMINATE"]
]
