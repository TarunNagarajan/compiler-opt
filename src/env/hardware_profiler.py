import platform
import psutil
import os
import subprocess
from dataclasses import dataclass
from typing import Dict

@dataclass
class HardwareProfile:
    name: str
    weight_size: float
    weight_speed: float
    weight_energy: float
    description: str

class HardwareProfiler:
    """
    Analyzes host hardware to recommend optimization weights.
    """
    
    def __init__(self):
        self.cpu_name = platform.processor()
        self.total_ram_gb = psutil.virtual_memory().total / (1024**3)
        self.os = platform.system()
        
    def detect_profile(self) -> HardwareProfile:
        # 1. Check for Deep Embedded Indicators (ARM + Low RAM)
        is_arm = "arm" in self.cpu_name.lower() or "aarch64" in platform.machine().lower()
        is_low_mem = self.total_ram_gb < 2.1
        
        if is_arm and is_low_mem:
            return HardwareProfile(
                name="Deep Economy (IoT)",
                weight_size=0.7,
                weight_speed=0.1,
                weight_energy=0.2,
                description="Economy (Deep): Flash/RAM is critical. Minimal speed overhead."
            )
        
        # 2. Economy Standard (Mobile, Edge, or Desktop-in-embedded-mode)
        # Even on desktop, if you choose 'embedded', it should be an Economy mission.
        return HardwareProfile(
            name="Standard Economy",
            weight_size=0.4,
            weight_speed=0.1,
            weight_energy=0.5,
            description="Economy (Standard): Prioritizes Energy and Size. Speed is secondary."
        )

    def print_summary(self):
        profile = self.detect_profile()
        print(f"--- Hardware Profile Detected ---")
        print(f"CPU:     {self.cpu_name}")
        print(f"RAM:     {self.total_ram_gb:.1f} GB")
        print(f"Profile: {profile.name}")
        print(f"Weights: Size={profile.weight_size:.2f}, Spd={profile.weight_speed:.2f}, Energy={profile.weight_energy:.2f}")
        print(f"Note:    {profile.description}")
        print(f"---------------------------------")

if __name__ == "__main__":
    profiler = HardwareProfiler()
    profiler.print_summary()
