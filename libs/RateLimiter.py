# -*- coding: utf-8 -*-
"""
Digital Day CTF - Rate Limiter
================================
Sliding-window in-memory rate limiter for the flag submission endpoint.
Protects against brute-force flag guessing without any external dependency.

Usage (in a Tornado handler):
    from libs.RateLimiter import flag_rate_limiter
    allowed, wait_secs = flag_rate_limiter.check(user_uuid)
    if not allowed:
        self.set_status(429)
        ...
        return
"""

import time
import logging
from collections import deque, defaultdict
from threading import Lock


log = logging.getLogger(__name__)


class SlidingWindowRateLimiter:
    """
    Sliding-window rate limiter backed by an in-process deque per key.

    Parameters
    ----------
    max_requests : int
        Maximum number of requests allowed in the window.
    window_seconds : int
        Duration of the sliding window in seconds.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 30):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict[str, deque] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> tuple[bool, int]:
        """
        Check whether *key* is allowed to make a request right now.

        Returns
        -------
        (allowed: bool, retry_after: int)
            - allowed     : True if the request should proceed.
            - retry_after : Seconds the client must wait before retrying
                            (0 when allowed is True).
        """
        now = time.monotonic()
        cutoff = now - self.window_seconds

        with self._lock:
            bucket = self._buckets[key]

            # Evict timestamps outside the current window
            while bucket and bucket[0] < cutoff:
                bucket.popleft()

            if len(bucket) >= self.max_requests:
                # Oldest request in window tells us how long to wait
                oldest = bucket[0]
                retry_after = int(self.window_seconds - (now - oldest)) + 1
                log.warning(
                    "[RateLimiter] key=%s blocked — %d requests in %ds window. retry_after=%ds",
                    key,
                    len(bucket),
                    self.window_seconds,
                    retry_after,
                )
                return False, retry_after

            bucket.append(now)
            return True, 0

    def reset(self, key: str) -> None:
        """Clear the rate limit bucket for *key* (e.g. after a successful capture)."""
        with self._lock:
            self._buckets.pop(key, None)

    def stats(self, key: str) -> dict:
        """Return current window stats for *key* (diagnostic use)."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            bucket = self._buckets.get(key, deque())
            recent = [ts for ts in bucket if ts >= cutoff]
        return {
            "key": key,
            "requests_in_window": len(recent),
            "max_requests": self.max_requests,
            "window_seconds": self.window_seconds,
            "remaining": max(0, self.max_requests - len(recent)),
        }


# ---------------------------------------------------------------------------
# Singleton instances — import these in handlers
# ---------------------------------------------------------------------------

# 5 flag submissions per 30 s per user  →  brute-force proof
flag_rate_limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=30)

# Hint purchases: 3 per minute
hint_rate_limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=60)
