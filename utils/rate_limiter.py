class RateLimiter:
    """Token bucket rate limiter."""
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    async def allow_request(self) -> bool:
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.time_window]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
