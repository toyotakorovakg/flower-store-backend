"""
Custom middleware for the application.

Defines middleware to apply rate limiting, RLS context and other security
controls. Use these middlewares to centralize cross‑cutting concerns.
"""
from __future__ import annotations

from typing import Callable

from fastapi import Request, Response


class RLSMiddleware:
    """Middleware that sets PostgreSQL session variables for row level security.

    For each incoming request, this middleware can set connection variables like
    `app.actor_role` based on the authenticated user. This example is a stub
    and does not implement actual user lookup.
    """

    def __init__(self, app: Callable) -> None:
        self.app = app

    async def __call__(self, request: Request) -> Response:
        # TODO: extract user information from request/session and set RLS variables.
        response = await self.app(request)
        return response
