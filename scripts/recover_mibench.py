import os
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
QUARANTINE_DIR = PROJECT_ROOT / "benchmarks" / "_quarantine" / "mibench" / "mibench-master"
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks" / "mibench" / "mibench-master"
CLANG = "clang"

# Get all directories in mibench-master to use as potential include paths
ALL_DIRS = [str(d) for d in BENCHMARKS_DIR.rglob("*") if d.is_dir()]

def recover():
    print(f"[RECOVER] Scanning quarantine for mibench files: {QUARANTINE_DIR}")
    if not QUARANTINE_DIR.exists():
        print("[RECOVER] Quarantine directory not found.")
        return

    recovered_count = 0
    total_scanned = 0

    for c_file in QUARANTINE_DIR.rglob("*.c"):
        total_scanned += 1
        rel_path = c_file.relative_to(QUARANTINE_DIR)
        
        # Aggressive include flags: current dev dir + its parent + specific common dirs
        include_flags = ["-I", str(c_file.parent)]
        # Add parent and grandparent
        include_flags.extend(["-I", str(c_file.parent.parent)])
        
        # Add a few high-probability dirs
        common_dirs = [
            BENCHMARKS_DIR / "telecomm/gsm/inc",
            BENCHMARKS_DIR / "consumer/jpeg/jpeg-6a",
            BENCHMARKS_DIR / "consumer/mad/mad-0.14.2b",
            BENCHMARKS_DIR / "office/ghostscript/src",
            BENCHMARKS_DIR / "security/pgp/src"
        ]
        for d in common_dirs:
            if d.exists():
                include_flags.extend(["-I", str(d)])

        # Try to compile
        try:
            cmd = [CLANG, "-S", "-emit-llvm", str(c_file), "-o", "nul", "-Wno-everything"] + include_flags
            r = subprocess.run(cmd, capture_output=True, timeout=5)
            
            if r.returncode == 0:
                dest = BENCHMARKS_DIR / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(c_file), str(dest))
                recovered_count += 1
                if recovered_count % 10 == 0:
                    print(f"  [OK] Recovered {rel_path} ({recovered_count} total)")
        except Exception as e:
            pass

    print(f"\n[RECOVER] Done! Recovered {recovered_count} files out of {total_scanned} scanned.")

if __name__ == "__main__":
    recover()
