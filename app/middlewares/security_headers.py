"""
A module for security headers in the app.middlewares package.
"""

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding security headers to the response.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Dispatch the request with the security headers added to the response
        :param request: The HTTP request to be dispatched
        :type request: Request
        :param call_next: The call_next middleware function
        :type call_next: RequestResponseEndpoint
        :return: The response with the security headers added
        :rtype: Response
        """
        response: Response = await call_next(request)
        self.add_security_headers(response)
        return response

    @staticmethod
    def add_security_headers(response: Response) -> None:
        """
        Adds security headers to the response.
        :param response:
        :type response: Response
        :return: None
        :rtype: NoneType
        """
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
