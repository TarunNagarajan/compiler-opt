import pandas as pd
import sys

def analyze_csv(filepath):
    print(f"Analyzing {filepath}...")
    try:
        df = pd.read_csv(filepath, header=0)
        if df.empty:
            print("File is empty.")
            return
            
        columns = ['step', 'file', 'action_idx', 'action_name', 'micro_idx', 'reward', 'value', 'prev_rt', 'new_rt']
        
        # In case the number of columns differs, just take the first len(columns)
        num_cols = len(df.columns)
        if num_cols < len(columns):
            print("Not enough columns in CSV")
            return
        df = df[df.columns[:len(columns)]]
        df.columns = columns
        
        # Calculate things
        total_steps = len(df)
        
        # Stop actions
        # Action 15 is TERMINATE
        stops = df[df['action_idx'] == 15]
        
        # Among stops, which are IGNORED FILE? (Reward == 0.0)
        ignored_stops = stops[stops['reward'] == 0.0]
        
        # Premature stops (-0.1 penalty)
        premature_stops = stops[stops['reward'] == -0.1]
        
        # Successful stops (Reward > ~0.0)
        successful_stops = stops[stops['reward'] > 0.0]
        
        # Errors or other stops (-2.0 penalty for cheating)
        other_stops = stops[(stops['reward'] < 0.0) & (stops['reward'] != -0.1)]
        
        print(f"Total actions taken: {total_steps}")
        print(f"Number of episodes (STOP actions): {len(stops)}")
        print(f"  - IGNORED (0 steps, 0 reward): {len(ignored_stops)} ({len(ignored_stops)/len(stops)*100:.1f}%)")
        print(f"  - PREMATURE (-0.1 penalty): {len(premature_stops)} ({len(premature_stops)/len(stops)*100:.1f}%)")
        print(f"  - IMPROVED (Positive reward): {len(successful_stops)} ({len(successful_stops)/len(stops)*100:.1f}%)")
        print(f"  - OTHER PENALTY: {len(other_stops)} ({len(other_stops)/len(stops)*100:.1f}%)")
        
        # For non-ignored episodes, what is the average episode length?
        files = df.groupby('file')
        episode_lengths = []
        for name, group in files:
            # count number of actions for this file
            l = len(group)
            if l > 1: # meaning it didn't just STOP immediately
                episode_lengths.append(l)
                
        if episode_lengths:
            print(f"\nAverage length of non-ignored episodes: {sum(episode_lengths)/len(episode_lengths):.2f} steps")
            print(f"Max episode length: {max(episode_lengths)} steps")
            print(f"Number of non-ignored episodes: {len(episode_lengths)}")
        
        # Show value distribution for IGNORED
        print(f"\nAverage value prediction for IGNORED stops: {ignored_stops['value'].mean():.4f}")
        print(f"Average value prediction for PREMATURE stops: {premature_stops['value'].mean():.4f}")
        print(f"Average value prediction for ACTIVE steps: {df[df['action_idx'] != 15]['value'].mean():.4f}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    analyze_csv(sys.argv[1])
