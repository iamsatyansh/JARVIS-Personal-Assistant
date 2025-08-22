# ==============================================================================
# File: utils/health_monitor.py
# ==============================================================================
class HealthMonitor:
    """System health monitoring service."""
    async def check_system_health(self) -> dict:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        health = {
            "cpu_usage_percent": cpu,
            "memory_usage_percent": mem.percent,
            "is_healthy": cpu < 90 and mem.percent < 90
        }
        if not health["is_healthy"]:
            logging.warning(f"System health alert: CPU={cpu}%, Memory={mem.percent}%")
        return health
