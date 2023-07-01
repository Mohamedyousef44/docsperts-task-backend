from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from .models import User
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.conf import settings


@api_view(["POST"])
def register_user(request):
    """
    View function for user registration.

    This view function takes a POST request with user information and attempts to create a new user.
    If the user data is valid, it creates a new user and returns a success response with the user data.
    If the user data is invalid, it returns an error response with a message indicating the reason for the failure.

    Args:
        request (django.http.HttpRequest): The incoming HTTP request.

    Returns:
        django.http.HttpResponse: The HTTP response.
    """
    serializer = UserSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return a success response with the user data
        return Response(
            {
                "success": True,
                "message": "User created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    except serializers.ValidationError as e:
        # Return an error response if the user data is invalid
        return Response(
            {
                "success": False,
                "message": "data is not valid",
                "errors": e.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        # Return an error response if an unexpected error occurs
        return Response(
            {
                "success": False,
                "message": "Failed to create User",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@ensure_csrf_cookie
def login_user(request):
    """
    View function for user login.

    This view function takes a POST request with the user's email and password and attempts to authenticate the user. If the authentication succeeds, it generates a JWT token with an expiration time of 1 week and returns it in the response. If the authentication fails, it returns an error response with a message indicating the reason for the failure.

    Args:
        request (django.http.HttpRequest): The incoming HTTP request.

    Returns:
        django.http.HttpResponse: The HTTP response.
    """
    try:
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise AuthenticationFailed("wrong password")

        # Generate a JWT token with an expiration time of 1 week
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_TOKEN_KEY, algorithm="HS256")

        # Return a success response with the JWT token
        return Response(
            {
                "success": True,
                "message": "Login Successfully",
                "data": token,
            },
            status=status.HTTP_200_OK,
        )

    except (AuthenticationFailed, User.DoesNotExist) as e:
        # Return an error response if the authentication fails
        return Response(
            {
                "success": False,
                "message": "Invalid Credentials",
                "error": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        # Return an error response if an unexpected error occurs
        return Response(
            {
                "success": False,
                "message": "Something wrong happens",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
