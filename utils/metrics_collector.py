# ==============================================================================
# File: utils/metrics_collector.py
# ==============================================================================
from collections import defaultdict

class MetricsCollector:
    """Collects and aggregates application metrics."""
    def __init__(self):
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)

    def record_command_processing(self, intent: str, duration: float, success: bool):
        self.counters[f"commands.processed.{intent}.{'success' if success else 'failure'}"] += 1
        self.timers[f"commands.duration.{intent}"].append(duration)
