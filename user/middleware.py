import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.renderers import JSONRenderer


class JWTAuthenticationMiddleware:
    """
    Middleware class for JWT authentication.

    This middleware checks if the request requires authentication and validates the JWT token included in the Authorization header. If the token is valid, it decodes it and retrieves the user object from the database. If the token is invalid or the user does not exist, it returns an error response.

    Attributes:
        get_response (callable): The next middleware or view function in the chain.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the get_response function.

        Args:
            get_response (callable): The next middleware or view function in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Checks if the request requires authentication and validates the JWT token.

        If the requested path is excluded from authentication, the middleware returns the response without further processing. If the path requires authentication, the middleware checks if the request contains a valid JWT token in the Authorization header. If the token is valid, it decodes it and retrieves the user object from the database. If the token is invalid or the user does not exist, the middleware returns an error response.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.

        Returns:
            django.http.HttpResponse: The HTTP response.
        """
        excluded_paths = [
            "/user/register/",
            "/user/login/",
            "/user/logout/",
            "/api/schema/",
            "/api/docs/",
        ]
        path = request.path_info

        # Exclude paths that do not require authentication
        if path in excluded_paths:
            print(path)
            auth_header = request.headers.get("Authorization")
            response = self.get_response(request)
            return response

        auth_header = request.headers.get("Authorization")

        # Check if the request contains a valid JWT token
        if not auth_header or not auth_header.startswith("Bearer "):
            response = Response(
                {
                    "success": False,
                    "message": "Not Authenticated",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response

        try:
            # Decode the JWT token and retrieve the user object from the database
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])
            request.user = user

        except (jwt.DecodeError, User.DoesNotExist) as e:
            # Return an error response if the token is invalid or the user does not exist
            response = Response(
                {
                    "success": False,
                    "message": "Not Authenticated",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response

        # Call the next middleware or view function in the chain
        response = self.get_response(request)
        return response
