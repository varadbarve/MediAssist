"""
Layer 3 — API Rate Limiting
Uses SlowAPI (free, MIT license) to prevent API abuse, DDoS attacks,
and runaway AI/voice API costs.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a global limiter instance keyed by client IP address
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
