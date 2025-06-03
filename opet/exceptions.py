"""Custom exception classes for the Opet API client application.

This module defines specific exceptions that can be raised by the client
and related utility functions. This allows for more granular error handling
compared to using generic exceptions.
"""


class BaseError(Exception):
    """Base class for all custom exceptions in this application.

    Allows for catching all application-specific errors with a single
    `except BaseError:` block.
    """
    pass


class Http200Error(BaseError):
    """Raised when an HTTP request does not return a 200 OK status.

    This typically indicates an issue with the request itself or a server-side
    problem that prevented a successful response.
    """
    pass


class ProvinceNotFoundError(BaseError):
    """Raised when a specified province ID cannot be found.

    This can occur if the provided province ID (plaka kodu) does not correspond
    to any existing province in the Opet system.
    """
    pass
