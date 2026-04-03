import os
import shutil
from pathlib import Path
import glob
import zipfile

def archive_old_checkpoints(model_dir="models", archive_dir="models/checkpoints", keep_last_n=3):
    print("Checking for old checkpoints to archive...")
    os.makedirs(archive_dir, exist_ok=True)
    
    # Find all hrl checkpoints matching the pattern
    pattern = os.path.join(model_dir, "hrl_antigravity_v4_hrl_hour_*.pth")
    files = glob.glob(pattern)
    
    if len(files) <= keep_last_n:
        print(f"Found {len(files)} checkpoints, keeping all of them in main directory (threshold is {keep_last_n}).")
        return

    # Sort files by modification time (oldest first)
    files.sort(key=os.path.getmtime)
    
    # The ones we want to archive are everything EXCEPT the last N
    files_to_archive = files[:-keep_last_n]
    
    archived_bytes = 0
    for f in files_to_archive:
        basename = os.path.basename(f)
        zip_path = os.path.join(archive_dir, f"{basename}.zip")
        
        try:
            # Compress it to save space
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(f, basename)
            
            size = os.path.getsize(f)
            os.remove(f) # Remove uncompressed
            archived_bytes += size
            print(f"  -> Archived: {basename} to {zip_path}")
        except Exception as e:
            print(f"  -> Failed to archive {f}: {e}")
            
    print(f"\nArchive complete. Processed {archived_bytes / (1024*1024):.1f} MB of space.")
    print(f"Kept the {keep_last_n} most recent hourly checkpoints in main directory.")

if __name__ == "__main__":
    archive_old_checkpoints()
