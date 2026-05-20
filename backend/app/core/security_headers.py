"""
Layer 8 — Security Headers Middleware
Adds critical HTTP security headers to every response.
All of these are free — they're just HTTP headers.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all HTTP responses.
    These headers protect against common web attacks:
    - XSS (Cross-Site Scripting)
    - Clickjacking
    - MIME sniffing
    - Protocol downgrade attacks
    """

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Prevent MIME-type sniffing (stops browser from guessing content types)
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking (stops your site from being embedded in iframes)
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS protection for older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Force HTTPS for 1 year (browsers will refuse HTTP connections)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Control what information is sent in the Referer header
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Prevent caching of sensitive responses
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"

        return response
