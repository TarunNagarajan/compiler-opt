import pandas as pd
import numpy as np
import sys

def analyze_csv_log(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return
        
    print(f"Loaded CSV Log: {filepath} with {len(df)} transitions.")
    
    macro_counts = df['Macro_Action_ID'].value_counts().sort_index()
    print("\n--- Macro Action Distribution ---")
    for action, count in macro_counts.items():
        if action == 15:
            print(f"Action 15 (STOP)   : {count} ({count/len(df)*100:.2f}%)")
        else:
            print(f"Action {action:<12}: {count} ({count/len(df)*100:.2f}%)")
            
    print("\n--- Reward Statistics ---")
    print(f"Mean Reward: {df['Reward'].mean():.4f}")
    print(f"Min Reward : {df['Reward'].min():.4f}")
    print(f"Max Reward : {df['Reward'].max():.4f}")
    
    pos_rewards = df[df['Reward'] > 0]
    neg_rewards = df[df['Reward'] < 0]
    stop_rewards = df[df['Reward'] == 0.5]
    
    print(f"Rewards > 0: {len(pos_rewards)} ({len(pos_rewards)/len(df)*100:.2f}%)")
    print(f"Rewards < 0: {len(neg_rewards)} ({len(neg_rewards)/len(df)*100:.2f}%)")
    print(f"Rewards == 0.5: {len(stop_rewards)} ({len(stop_rewards)/len(df)*100:.2f}%)")

if __name__ == '__main__':
    log_file = sys.argv[1] if len(sys.argv) > 1 else "logs/optimization_log_20260223_095244.csv"
    analyze_csv_log(log_file)
