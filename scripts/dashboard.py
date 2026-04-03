import os
import sys
import glob
import time
import pandas as pd
from collections import deque
from pathlib import Path
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.text import Text
import asciichartpy as plot

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import LOGS_DIR
from src.actions.macro_actions import MACRO_ACTIONS

def get_latest_log():
    logs = glob.glob(str(LOGS_DIR) + "/optimization_log_*.csv")
    if not logs:
        return None
    return max(logs, key=os.path.getmtime)

def generate_layout(df, step_history, reward_history, stop_prob_history):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main")
    )
    layout["main"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="chart_reward", ratio=1),
        Layout(name="chart_stop", ratio=1)
    )

    # HEADER
    total_steps = len(df)
    latest_reward = df['Reward'].iloc[-1] if not df.empty else 0.0
    avg_reward = df['Reward'].tail(100).mean() if not df.empty else 0.0
    
    header_text = Text(f"🚀 ANTIGRAVITY AI - HRL Live Training Dashboard | Total Steps: {total_steps} | Latest Reward: {latest_reward:.4f} | Avg(100): {avg_reward:.4f}", style="bold cyan")
    layout["header"].update(Panel(header_text))

    # REWARD CHART
    if len(reward_history) > 2:
        reward_chart = plot.plot(list(reward_history), {'height': 10, 'colors': [plot.green]})
        layout["chart_reward"].update(Panel(reward_chart, title="[green]Episode Reward (Last 100)", border_style="green"))
    else:
        layout["chart_reward"].update(Panel("Waiting for more data...", title="[green]Episode Reward", border_style="green"))

    # STOP ACTION TREND CHART
    if len(stop_prob_history) > 2:
        stop_chart = plot.plot(list(stop_prob_history), {'height': 10, 'colors': [plot.red]})
        layout["chart_stop"].update(Panel(stop_chart, title="[red]STOP Action % (Last 100)", border_style="red"))
    else:
        layout["chart_stop"].update(Panel("Waiting for more data...", title="[red]STOP Action %", border_style="red"))

    # ACTION DISTRIBUTION TABLE
    action_table = Table(title="Recent Macro Actions (Last 200)", expand=True)
    action_table.add_column("Action Name", justify="left", style="cyan", no_wrap=True)
    action_table.add_column("Count", justify="right", style="magenta")
    action_table.add_column("% Selection", justify="right", style="green")

    if not df.empty:
        recent_df = df.tail(200)
        action_counts = recent_df['Macro_Name'].value_counts()
        total_recent = len(recent_df)
        
        for action_name, count in action_counts.items():
            pct = (count / total_recent) * 100
            action_table.add_row(str(action_name), str(count), f"{pct:.1f}%")

    layout["right"].update(Panel(action_table, border_style="cyan"))

    return layout

def main():
    console = Console()
    console.clear()
    
    log_file = get_latest_log()
    if not log_file:
        print("Waiting for training to generate a CSV log...")
        while not log_file:
            time.sleep(2)
            log_file = get_latest_log()
            
    print(f"Tracking Log: {Path(log_file).name}")
    
    reward_history = deque(maxlen=100)
    stop_prob_history = deque(maxlen=100)
    step_history = deque(maxlen=100)
    
    last_processed_idx = 0

    with Live(refresh_per_second=2, screen=True) as live:
        while True:
            try:
                # Read CSV robustly avoiding locking issues
                df = pd.read_csv(log_file, on_bad_lines='skip')
                
                if len(df) > last_processed_idx:
                    new_rows = df.iloc[last_processed_idx:]
                    last_processed_idx = len(df)
                    
                    for _, row in new_rows.iterrows():
                        reward_history.append(row['Reward'])
                        step_history.append(row['Step'])

                    # Calculate rolling STOP probability over last 100 steps
                    recent_actions = df['Macro_Action_ID'].tail(100)
                    if len(recent_actions) > 0:
                        stop_count = sum(recent_actions == (len(MACRO_ACTIONS) - 1))
                        stop_pct = (stop_count / len(recent_actions)) * 100
                        stop_prob_history.append(stop_pct)
                    else:
                        stop_prob_history.append(0.0)

                live.update(generate_layout(df, list(step_history), list(reward_history), list(stop_prob_history)))
                time.sleep(1)
                
            except Exception as e:
                time.sleep(1) # Ignore transient file lock reading errors from pandas

if __name__ == "__main__":
    main()
