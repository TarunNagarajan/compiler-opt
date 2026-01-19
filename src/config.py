from pathlib import Path

LLVM_BIN_DIR = Path("C:/msys64/mingw64/bin")

CLANG = LLVM_BIN_DIR / "clang.exe"
OPT = LLVM_BIN_DIR / "opt.exe"
LLC = LLVM_BIN_DIR / "llc.exe"

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BENCHMARKS_DIR = DATA_DIR / "benchmarks"
IR_DIR = DATA_DIR / "ir"
MODELS_DIR = PROJECT_ROOT / "models"

FEATURE_DIM = 128

LLVM_PASSES = [
    "loop-unroll",
    "loop-vectorize",
    "loop-rotate",
    "licm",
    "inline",
    "mem2reg",
    "instcombine",
    "aggressive-instcombine",
    "dce",
    "adce",
    "sccp",
    "gvn",
    "simplifycfg",
    "sroa",
    "reassociate",
]


def verify_llvm_installation():
    missing = []
    for tool in [CLANG, OPT]:
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
    print("✓ LLVM installation verified!")
    print(f"  Clang: {CLANG}")
    print(f"  Opt:   {OPT}")
