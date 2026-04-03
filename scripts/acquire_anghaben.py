import os
import requests
import tarfile
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# AnghaBench is huge (1M+). We need a strategy to get a subset without downloading 100GB.
# Strategy: Download a specific "shard" if available, or fetch from a curated list.
# Since we can't easily browse the 1M file repo, we will use a "seed" list or 
# clone a small sub-repo if one exists. 
# Alternatively, we can use the 'search' API to find C files with specific keywords 
# like "graph", "parser", "crypto" and download raw content.

# Better approach for this environment: 
# Use a known mirror or dataset of C files.
# Let's try to pull from a known "Awesome C" or "Algorithms in C" repo which serves as a proxy for AnghaBench quality.
# Actually, TheAlgorithms/C is a great source for clean, diverse implementations.

TARGET_DIR = Path("benchmarks/large_scale/anghaben")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

REPOS = [
    "https://github.com/TheAlgorithms/C/archive/refs/heads/master.tar.gz",
    "https://github.com/nothings/single_file_libs/archive/refs/heads/master.tar.gz" # Header only libs - complex!
]

def download_and_extract(url, idx):
    print(f"Fetching repo {idx+1}...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            tar_path = TARGET_DIR / f"repo_{idx}.tar.gz"
            with open(tar_path, 'wb') as f:
                f.write(response.raw.read())
            
            # Extract
            with tarfile.open(tar_path) as tar:
                for member in tar.getmembers():
                    if member.name.endswith(".c"):
                        member.name = os.path.basename(member.name) # Flatten
                        try:
                            tar.extract(member, TARGET_DIR)
                        except:
                            pass
            
            os.remove(tar_path)
            print(f"Repo {idx+1} processed.")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        for i, repo in enumerate(REPOS):
            executor.submit(download_and_extract, repo, i)
    
    # Count results
    files = list(TARGET_DIR.glob("*.c"))
    print(f"Acquired {len(files)} real-world C files.")
