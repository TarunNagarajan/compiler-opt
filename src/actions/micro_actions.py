
from typing import List, Dict
import random

# Tactical passes that can be used to refine any Macro strategy
MICRO_PASSES = [
    "function(dce)",
    "function(instcombine<no-verify-fixpoint>)",
    "function(simplifycfg)",
    "function(early-cse)",
    "function(reassociate)",
    "function(sccp)"
]

class MicroRefiner:
    """
    Handles the refinement of a Macro action into a specific pass sequence.
    Now includes Parameter Tuning for 'Super-Human' optimization.
    """
    
    @staticmethod
    def apply_refinement(macro_seq: List[str], micro_action: int) -> List[str]:
        """
        Micro Actions:
        0-5:   Insert tactical MICRO_PASS at the BEGINNING
        6-11:  Insert tactical MICRO_PASS at the END
        12-14: Tune UNROLL: Set first loop-unroll in macro to factor <2>, <4>, or <8>
        15-17: Tune INLINE: Set inline threshold to <50>, <250>, or <500>
        18:    Reverse sequence
        19:    Identity (Do nothing)
        """
        refined = list(macro_seq)
        
        # Insertion
        if 0 <= micro_action <= 5:
            refined.insert(0, MICRO_PASSES[micro_action])
        elif 6 <= micro_action <= 11:
            refined.append(MICRO_PASSES[micro_action - 6])
            
        # Parameter Tuning: Unroll
        elif 12 <= micro_action <= 14:
            factors = [2, 4, 8]
            f = factors[micro_action - 12]
            for i, p in enumerate(refined):
                if "loop-unroll" in p:
                    refined[i] = f"function(loop-unroll<full-unroll-max={f}>)"
                    break
                    
        # Parameter Tuning: Inlining
        elif 15 <= micro_action <= 17:
            thresholds = [50, 250, 500]
            t = thresholds[micro_action - 15]
            for i, p in enumerate(refined):
                if "inline" in p:
                    refined[i] = f"inline<hint-threshold={t}>"
                    break
                    
        elif micro_action == 18:
            refined.reverse()
            
        return refined

NUM_MICRO_ACTIONS = 20
