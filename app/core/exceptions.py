"""
Custom exception classes for domain specific errors.

Raise these exceptions throughout the application instead of generic
exceptions to make error handling consistent.
"""


class AppError(Exception):
    """Base class for application exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
