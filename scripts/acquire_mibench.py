
import os
import requests
import tarfile
from pathlib import Path

TARGET_DIR = Path("benchmarks/mibench")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# MiBench is old and scattered. We'll use a known clean mirror or subset.
# For this environment, we'll try to fetch a specific tarball if available, 
# or clone a minimal repo. 
# A good source is usually from university mirrors or github forks.
# Let's use a reliable github mirror:
REPO_URL = "https://github.com/embecosm/mibench/archive/refs/heads/master.tar.gz"

def acquire_mibench():
    print("Fetching MiBench...")
    try:
        response = requests.get(REPO_URL, stream=True)
        if response.status_code == 200:
            tar_path = TARGET_DIR / "mibench.tar.gz"
            with open(tar_path, 'wb') as f:
                f.write(response.raw.read())
            
            print("Extracting...")
            with tarfile.open(tar_path) as tar:
                # Filter for C files and headers
                for member in tar.getmembers():
                    if member.name.endswith(".c") or member.name.endswith(".h"):
                        # Flatten structure slightly? No, keep it to avoid conflicts
                        try:
                            tar.extract(member, TARGET_DIR)
                        except:
                            pass
            
            os.remove(tar_path)
            print("MiBench acquired.")
        else:
            print(f"Failed to download MiBench: {response.status_code}")
    except Exception as e:
        print(f"Error fetching MiBench: {e}")

if __name__ == "__main__":
    acquire_mibench()
