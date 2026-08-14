# ==========================================================
# PDF MASTER AI
# API Exceptions
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from fastapi import (
    HTTPException,
    status
)

# ----------------------------------------------------------
# API KEY INVALID
# ----------------------------------------------------------

class InvalidAPIKeyException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid API Key."

        )

# ----------------------------------------------------------
# API KEY EXPIRED
# ----------------------------------------------------------

class APIKeyExpiredException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="API Key has expired."

        )

# ----------------------------------------------------------
# API KEY DISABLED
# ----------------------------------------------------------

class APIKeyDisabledException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="API Key has been disabled."

        )

# ----------------------------------------------------------
# API RATE LIMIT
# ----------------------------------------------------------

class RateLimitExceededException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_429_TOO_MANY_REQUESTS,

            detail="Rate limit exceeded."

        )

# ----------------------------------------------------------
# ENDPOINT NOT FOUND
# ----------------------------------------------------------

class EndpointNotFoundException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="API endpoint not found."

        )

# ----------------------------------------------------------
# METHOD NOT ALLOWED
# ----------------------------------------------------------

class MethodNotAllowedException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,

            detail="HTTP method not allowed."

        )

# ----------------------------------------------------------
# API VERSION NOT SUPPORTED
# ----------------------------------------------------------

class APIVersionException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="API version is not supported."

        )

# ----------------------------------------------------------
# SERVICE UNAVAILABLE
# ----------------------------------------------------------

class ServiceUnavailableException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,

            detail="Service temporarily unavailable."

        )

# ----------------------------------------------------------
# TOO MANY REQUESTS
# ----------------------------------------------------------

class TooManyRequestsException(

    HTTPException

):

    def __init__(self):

        super().__init__(

            status_code=status.HTTP_429_TOO_MANY_REQUESTS,

            detail="Too many requests."

        )