"""
Carbon Emissions Tracking for compiler optimization training.

Wraps CodeCarbon to track kgCO2 per training run and per compilation.
Install: pip install codecarbon>=2.3.0
"""

from contextlib import contextmanager


class CompilationCarbonTracker:

    def __init__(self, project_name="compiler-opt", output_dir=None):
        self._project_name = project_name
        self._output_dir = output_dir
        self._tracker = None
        self._available = False
        try:
            from codecarbon import EmissionsTracker
            self._tracker_cls = EmissionsTracker
            self._available = True
        except ImportError:
            self._tracker_cls = None

    @property
    def available(self) -> bool:
        return self._available

    def start(self):
        """Start tracking emissions for the training run."""
        if not self._available:
            return
        kwargs = {
            "project_name": self._project_name,
            "log_level": "warning",
            "save_to_api": False,
        }
        if self._output_dir:
            kwargs["output_dir"] = str(self._output_dir)
        self._tracker = self._tracker_cls(**kwargs)
        self._tracker.start()

    def stop(self) -> float:
        """Stop tracking and return total kgCO2."""
        if self._tracker is None:
            return 0.0
        emissions = self._tracker.stop()
        return float(emissions) if emissions else 0.0

    @contextmanager
    def track_episode(self):
        """Context manager for tracking a single episode's emissions."""
        if not self._available:
            yield 0.0
            return
        tracker = self._tracker_cls(
            project_name=f"{self._project_name}_episode",
            log_level="error",
            save_to_file=False,
        )
        tracker.start()
        try:
            yield tracker
        finally:
            tracker.stop()

    @staticmethod
    def savings_report(baseline_kg: float, optimized_kg: float) -> dict:
        return {
            "baseline_kg_co2": baseline_kg,
            "optimized_kg_co2": optimized_kg,
            "savings_pct": (baseline_kg - optimized_kg) / max(baseline_kg, 1e-12) * 100,
        }
