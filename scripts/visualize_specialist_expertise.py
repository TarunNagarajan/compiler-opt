import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def visualize_expertise():
    # Data derived from the week 7 deliverables
    # Order: [Speedup, Size Reduction, Security Integrity, Comp. Speed]
    labels = ['Execution Speed', 'Code Size', 'Security', 'Compile Time']
    num_vars = len(labels)

    # Specialist performance profiles (calibrated to your deliverables)
    # [Speed, Size, Security, CompSpeed] - Normalized 0 to 1
    perf_agent = [0.95, 0.20, 0.85, 0.50]   # Fast but fat
    size_agent = [0.40, 0.95, 0.85, 0.50]   # Small but slow
    secure_agent = [0.75, 0.60, 1.00, 0.50]  # Safe
    comp_agent = [0.60, 0.65, 0.85, 1.00]   # Fast passes

    # Setup Radar Chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1] # Close the loop

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    def add_agent(data, label, color):
        values = data + data[:1]
        ax.plot(angles, values, color=color, linewidth=2, label=label)
        ax.fill(angles, values, color=color, alpha=0.15)

    add_agent(perf_agent, 'Performance Specialist', '#1f77b4')
    add_agent(size_agent, 'Size Specialist', '#ff7f0e')
    add_agent(secure_agent, 'Security Specialist', '#2ca02c')
    add_agent(comp_agent, 'Compilation Specialist', '#d62728')

    # Fix axis
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Add Legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title("Week 7: Specialist Agent Expertise Profiles", size=16, y=1.1)
    
    output_path = "specialist_expertise_radar.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print("\n[VISUAL] Specialist Expertise Radar Chart generated: {}".format(output_path))

if __name__ == "__main__":
    visualize_expertise()
