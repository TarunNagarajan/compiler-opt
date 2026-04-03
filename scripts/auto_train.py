"""
Automated Training & Evaluation Loop for World Model

This script orchestrates the training process by running N iterations 
at a time, stopping to run the diagnostic script, and analyzing the 
results. If the diagnostic shows collapse or averaging, it halts and 
alerts the user. Otherwise, it resumes training for the next chunk.
"""

import subprocess
import sys
import re
import argparse
from pathlib import Path

def run_training_chunk(chunk_size, total_iters_so_far, args):
    print(f"\n{'='*60}")
    print(f"▶ STARTING TRAINING CHUNK (Iters {total_iters_so_far+1} to {total_iters_so_far+chunk_size})")
    print(f"{'='*60}\n")
    
    cmd = [
        "uv", "run", "python", "scripts/train_world_model.py",
        "--iterations", str(total_iters_so_far + chunk_size),
        "--steps_per_iter", "2000",
        "--epochs_per_iter", "25",
        "--batch_size", "64",
        "--lr", "5e-4",
        "--name", args.name,
        "--gnn_layers", str(args.gnn_layers),
        "--resume", f"models/world_model_{args.name}_checkpoint.pth"
    ]
    
    # Run training, piping output to console
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training process failed with exit code {e.returncode}")
        return False

def run_diagnostic(args):
    print(f"\n{'='*60}")
    print(f"🔍 RUNNING DIAGNOSTIC EVALUATION")
    print(f"{'='*60}\n")
    
    cmd = [
        "uv", "run", "python", "scripts/diagnose_world_model.py",
        "--checkpoint", f"models/world_model_{args.name}_checkpoint.pth",
        "--gnn_layers", str(args.gnn_layers)
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = result.stdout
        print(output)
        
        # Parse results to determine if we should continue
        collapsed_emb = "❌ VERDICT: COLLAPSED" in output
        
        # Count how many actions are averaging vs program-aware
        averaging_count = len(re.findall(r"StdDev:.*?→ AVERAGING", output))
        aware_count = len(re.findall(r"StdDev:.*?→ PROGRAM-AWARE", output))
        
        print("\n--- DIAGNOSTIC SUMMARY ---")
        if collapsed_emb:
            print("❌ FAIL: Encoder embeddings collapsed!")
            return False
            
        print(f"   Action Predictions: {aware_count} Aware, {averaging_count} Averaging")
        
        # We want to see continuous improvement. If everything is averaging, we fail.
        # But if at least some actions are aware, we keep going to let it learn.
        if aware_count == 0 and averaging_count > 0:
            print("❌ FAIL: Model is completely averaging all action predictions!")
            return False
        elif averaging_count > 0:
            print("⚠️ WARNING: Some actions are still averaging. Continuing training to improve them.")
            return True
        else:
            print("✅ PASS: Model is fully program-aware across tested actions!")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Diagnostic failed with exit code {e.returncode}")
        print("Output logs:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Auto Train & Eval Loop")
    parser.add_argument("--name", type=str, default="antigravity_v4_L6")
    parser.add_argument("--gnn_layers", type=int, default=6)
    parser.add_argument("--chunk_size", type=int, default=5, help="Iters to run before eval")
    parser.add_argument("--total_target", type=int, default=50, help="Total iterations to reach")
    parser.add_argument("--start_iter", type=int, default=10, help="Current iteration count (approx)")
    args = parser.parse_args()
    
    iters_done = args.start_iter
    
    while iters_done < args.total_target:
        # 1. Run training chunk
        success = run_training_chunk(args.chunk_size, iters_done, args)
        if not success:
            print("Halting automation due to training failure.")
            sys.exit(1)
            
        iters_done += args.chunk_size
        
        # 2. Run diagnostic
        passed = run_diagnostic(args)
        if not passed:
            print(f"\n🛑 AUTOMATION HALTED at iteration {iters_done} due to diagnostic failure.")
            print("Please review the model state and adjust hyperparams.")
            sys.exit(1)
            
    print(f"\n🎉 SUCCESS: Reached target of {args.total_target} iterations with passing diagnostics.")

if __name__ == "__main__":
    main()
