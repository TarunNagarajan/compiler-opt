from pathlib import Path

LLVM_BIN_DIR = Path("C:/msys64/mingw64/bin")

CLANG = LLVM_BIN_DIR / "clang.exe"
CLANG_CXX = LLVM_BIN_DIR / "clang++.exe"
OPT = LLVM_BIN_DIR / "opt.exe"
LLC = LLVM_BIN_DIR / "llc.exe"
LLVM_LINK = LLVM_BIN_DIR / "llvm-link.exe"
LLVM_DIS = LLVM_BIN_DIR / "llvm-dis.exe"
LLVM_NM = LLVM_BIN_DIR / "llvm-nm.exe"

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
IR_DIR = DATA_DIR / "ir"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
RESULTS_DIR = PROJECT_ROOT / "results"

POLYBENCH_CATEGORIES = ["datamining", "linear-algebra", "medley", "stencils"]

# Dimension: 64 Scalar Features + 64 Graph Embedding (128 total)
FEATURE_DIM = 128

# Constraint Thresholds (Soft limits for PPO-Lagrangian)
CONSTRAINT_SIZE_LIMIT_PCT = 0.05  # Max 5% size increase allowed per step/episode
CONSTRAINT_TIME_LIMIT_MS = 500.0  # Max 500ms compile time per step

def get_benchmark_paths(categories=None):
    if categories is None:
        categories = POLYBENCH_CATEGORIES
    
    benchmarks = []
    seen = set()
    
    # 1. PolyBench categories (original)
    for category in categories:
        category_dir = BENCHMARKS_DIR / category
        if category_dir.exists():
            for f in category_dir.rglob("*.c"):
                if f.resolve() not in seen:
                    benchmarks.append(f)
                    seen.add(f.resolve())
            
    # 2. ALL other benchmark suites (synthetic, diverse_synthetic, large_scale, graphs, etc.)
    # Exclude suites with broken/non-standalone files (checked at any directory depth)
    EXCLUDED_SUITES = {"_quarantine", "anghaben"}  # Use anghaben_wrapped instead of raw anghaben
    if BENCHMARKS_DIR.exists():
        for subdir in BENCHMARKS_DIR.iterdir():
            if subdir.is_dir() and subdir.name not in categories and subdir.name not in EXCLUDED_SUITES:
                for ext in ["*.c", "*.cpp"]:
                    for f in subdir.rglob(ext):
                        # Skip files nested inside an excluded directory
                        if any(excl in f.parts for excl in EXCLUDED_SUITES):
                            continue
                        if f.resolve() not in seen:
                            benchmarks.append(f)
                            seen.add(f.resolve())
    
    return sorted(benchmarks)

LLVM_PASSES = [
    # --- Loop Optimizations ---
    "function(loop-unroll)",
    "function(loop-vectorize)",
    "function(loop(loop-rotate))",
    "function(loop-mssa(licm))",
    "function(loop-deletion)",
    "function(indvars)",
    "function(loop-idiom)",            # NEW: Recognizes loops as memset/memcpy
    "function(loop-interchange)",      # NEW: Swaps loop nesting for cache locality
    "function(simple-loop-unswitch)",  # NEW: Hoists loop-invariant branches
    
    # --- Vectorization ---
    "function(slp-vectorizer)",        # NEW: Straight-line vectorization
    
    # --- Inlining & Interprocedural ---
    "inline",
    "argpromotion",                    # NEW: Promotes pointer args to scalars
    "ipsccp",                          # NEW: Interprocedural constant propagation
    "globalopt",                       # NEW: Global variable optimization
    "function(tailcallelim)",          # NEW: Converts tail calls to loops (crucial for recursion)
    "function(callsite-splitting)",    # NEW: Specializes functions at call sites
    
    # --- Scalar/Memory ---
    "function(mem2reg)",
    "function(sroa)",
    "function(instcombine<no-verify-fixpoint>)",
    "function(aggressive-instcombine)",
    "function(reassociate)",
    "function(gvn)",
    "function(sccp)",
    "function(dce)",
    "function(adce)",
    "function(dse)",                   # NEW: Dead store elimination
    "function(memcpyopt)",             # NEW: Optimizes memory copies
    "function(bdce)",                  # NEW: Bit-tracking dead code elimination
    
    # --- Control Flow ---
    "function(simplifycfg)",
    "function(jump-threading)",        # NEW: Eliminates redundant branches
    "function(correlated-propagation)", # NEW: Uses branch info to simplify
    "function(lower-expect)",          # NEW: Better branch prediction hints
    
    # --- Type/Conversion ---
    "function(float2int)",             # NEW: Converts float ops to int where safe
    "function(lower-constant-intrinsics)", # NEW: Lowers constant intrinsics
    
    # --- Cleanup ---
    "function(early-cse)",             # NEW: Early common subexpression elimination
    "function(newgvn)",                # NEW: New GVN algorithm (sometimes better)
    "function(sink)",                  # NEW: Sinks instructions closer to uses
    "function(mergereturn)",           # NEW: Merges multiple return blocks
    "module(constmerge)",              # NEW: Merges duplicate constants
    "module(deadargelim)",             # NEW: Removes unused function arguments
    "module(strip-dead-prototypes)",   # NEW: Removes unused declarations
]

try:
    from .actions.macro_actions import MACRO_ACTIONS
except ImportError:
    MACRO_ACTIONS = []

NUM_ATOMIC_ACTIONS = len(LLVM_PASSES)
NUM_MACRO_ACTIONS = len(MACRO_ACTIONS)
NUM_ACTIONS = NUM_ATOMIC_ACTIONS + NUM_MACRO_ACTIONS


def verify_llvm_installation():
    missing = []
    for tool in [CLANG, CLANG_CXX, OPT, LLVM_LINK, LLVM_DIS, LLVM_NM]:
        if not tool.exists():
            missing.append(str(tool))
    
    if missing:
        raise FileNotFoundError(
            f"LLVM tools not found: {missing}\n"
            f"Please verify LLVM is installed at {LLVM_BIN_DIR}"
        )
    return True


if __name__ == "__main__":
    verify_llvm_installation()
    print("[AGENT] LLVM installation verified...")
    print(f"[AGENT] Clang: {CLANG}...")
    print(f"[AGENT] Opt:   {OPT}...")
