import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

from src.passes.metrics import MetricsCollector

collector = MetricsCollector()
count = collector.count_instructions('scripts/qsort_test.ll')
print(f"Instructions: {count}")
