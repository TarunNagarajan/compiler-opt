
import csv
import json
import argparse
from pathlib import Path

def recover(csv_path: str, output_json: str):
    csv_path = Path(csv_path)
    output_json = Path(output_json)
    
    if not csv_path.exists():
        print(f"Error: CSV file {csv_path} not found.")
        return

    data = []
    print(f"Reading from {csv_path}...")
    
    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Reconstruct the structure used in optimization_dataset.json
                    entry = {
                        "benchmark": row['benchmark'],
                        "category": row['category'],
                        "sequence_id": int(row['sequence_id']),
                        "pass_count": int(row['pass_count']),
                        "passes": row['passes'].split(';'),
                        "metrics": {
                            "inst_reduction": float(row['inst_reduction']),
                            "size_reduction": float(row['size_reduction']),
                            "compile_time": float(row['compile_time'])
                        }
                    }
                    data.append(entry)
                except (ValueError, KeyError) as e:
                    print(f"Skipping malformed row: {row} ({e})")
                    continue
                    
        with open(output_json, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Success! Recovered {len(data)} entries to {output_json}")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recover dataset JSON from CSV log")
    parser.add_argument("csv_file", help="Input CSV log file (e.g., optimization_log.csv)")
    parser.add_argument("output_file", help="Output JSON file (e.g., dataset/recovered.json)")
    args = parser.parse_args()
    
    recover(args.csv_file, args.output_file)
