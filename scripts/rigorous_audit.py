import pandas as pd
import numpy as np
import sys
from pathlib import Path

def rigorous_audit(csv_path):
    print(f"--- RIGOROUS AUDIT: {Path(csv_path).name} ---")
    df = pd.read_csv(csv_path)
    
    # Basic Step Stats
    total_steps = len(df)
    pos_steps = len(df[df['Reward'] > 0])
    mean_reward = df['Reward'].mean()
    
    print(f"Total Steps: {total_steps}")
    print(f"Action Success Rate: {pos_steps/total_steps:.2%}")
    print(f"Mean Reward per Step: {mean_reward:.4f}")
    
    # Ferrari Pass Performance
    ferrari_macros = df[df['Macro_Name'].str.contains('loop-idiom|deadargelim', case=False, na=False)]
    if not ferrari_macros.empty:
        print("\n--- FERRARI PASS EFFICIENCY ---")
        # Fixed lambda to check reward > 0
        ferrari_stats = ferrari_macros.groupby('Macro_Name')['Reward'].agg(['count', 'mean', lambda x: (x > 0).mean()])
        ferrari_stats.columns = ['Usage', 'Mean_Reward', 'Success_Rate']
        print(ferrari_stats)
    
    # Episode Analysis
    episode_ends = df[df['Macro_Name'].str.contains('TERMINATE|LIMIT_EVAL|PATIENCE', na=False)].index.tolist()
    
    episodes = []
    start_idx = 0
    for end_idx in episode_ends:
        ep_df = df.iloc[start_idx:end_idx+1]
        if ep_df.empty: continue
        
        instr_start = ep_df.iloc[0]['Num_Instr_Before']
        instr_end = ep_df.iloc[-1]['Num_Instr_After']
        
        if instr_start > 0:
            improvement = (instr_start - instr_end) / instr_start
        else:
            improvement = 0
            
        episodes.append({
            'improvement': improvement,
            'steps': len(ep_df),
            'terminal_action': ep_df.iloc[-1]['Macro_Name'],
            'is_stencil': 'stencil' in str(ep_df.iloc[0]['Program']).lower()
        })
        start_idx = end_idx + 1
        
    ep_df = pd.DataFrame(episodes)
    if not ep_df.empty:
        print("\n--- EPISODE-LEVEL STRATEGY ---")
        print(f"Total Episodes Analyzed: {len(ep_df)}")
        print(f"Mean Program Improvement: {ep_df['improvement'].mean():.2%}")
        print(f"Median Program Improvement: {ep_df['improvement'].median():.2%}")
        print(f"Episode Win Rate (Net Gain > 0): {(ep_df['improvement'] > 0).mean():.2%}")
        print(f"Significant Win Rate (Net Gain > 5%): {(ep_df['improvement'] > 0.05).mean():.2%}")
        
        stencil_eps = ep_df[ep_df['is_stencil'] == True]
        if not stencil_eps.empty:
            print("\n--- STENCIL SPECIALIZATION ---")
            print(f"Stencil Episodes: {len(stencil_eps)}")
            print(f"Stencil Mean Improvement: {stencil_eps['improvement'].mean():.2%}")
            print(f"Stencil Win Rate: {(stencil_eps['improvement'] > 0).mean():.2%}")
        else:
            print("\nNo stencil episodes found in this log slice.")

        print("\n--- TERMINATION BREAKDOWN ---")
        print(ep_df['terminal_action'].value_counts())

    print("\n--- CRITIC CALIBRATION ---")
    correlation = df['Value'].corr(df['Reward'])
    print(f"Value-Reward Correlation: {correlation:.4f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rigorous_audit(sys.argv[1])
    else:
        print("Usage: python audit.py <csv_path>")
