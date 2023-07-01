from book.models.book import Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from book.api.serializers import BookSerializer
from book.permissions import IsAuthor
from rest_framework.exceptions import PermissionDenied


class BookView(APIView):
    """
    View class for handling CRUD operations on Book objects.

    This view class allows users to create, retrieve, update, and delete Book objects.
    Users can only access Books they have created, and attempting to access a Book created by another user will result in a PermissionDenied exception.

    Args:
        APIView (rest_framework.views.APIView): The base view class to extend.

    Returns:
        django.http.HttpResponse: The HTTP response.
    """

    permission_classes = [IsAuthor]

    def get(self, request, pk=None):
        """
        Retrieve a list of books or a single book.

        If a `pk` is provided, the method retrieves the book with the corresponding ID. Otherwise, the method retrieves all books.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            pk (int, optional): The ID of the book to retrieve. Defaults to None.

        Returns:
            django.http.HttpResponse: The HTTP response containing the book(s).

        Raises:
            Exception: If there is an error retrieving the book(s).
        """
        try:
            if pk is None:
                queryset = Book.objects.all()
                serializer = BookSerializer(queryset, many=True)
            else:
                queryset = Book.objects.filter(id=pk)
                serializer = BookSerializer(queryset, many=True)

            return Response(
                {
                    "success": True,
                    "message": "Books retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to retrieve books",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Create a new book.

        The method expects a JSON payload with the book data in the request body. The `author` field is automatically set to the ID of the authenticated user.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.

        Returns:
            django.http.HttpResponse: The HTTP response containing the newly created book.

        Raises:
            serializers.ValidationError: If the book data is not valid.
            Exception: If there is an error creating the book.
        """
        try:
            book_data = request.data
            book_data["author"] = request.user.id
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Book created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": "Invalid book data",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to create book",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, pk):
        """
        Update a book with partial data.

        The method retrieves the book with the corresponding ID and updates it with the provided partial data. The method also checks if the authenticated user has permission to update the book.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            pk (int): The ID of the book to update.

        Returns:
            django.http.HttpResponse: The HTTP response containing the updated book.

        Raises:
            serializers.ValidationError: If the book data is not valid.
            PermissionDenied: If the authenticated user does not have permission to update the book.
            Exception: If there is an error updating the book.
        """
        try:
            instance = Book.objects.get(id=pk)
            self.check_object_permissions(request, instance)
            serializer = BookSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Book updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": "Invalid book data",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to update this book",
                    "error": str(e),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update book",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk):
        """
        Delete a book.

        The method retrieves the book with the corresponding ID and deletes it. The method also checks if the authenticated user has permission to delete the book.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            pk (int): The ID of the book to delete.

        Returns:
            django.http.HttpResponse: The HTTP response containing the remaining books.

        Raises:
            PermissionDenied: If the authenticated user does not have permission to delete the book.
            Exception: If there is an error deleting the book.
        """
        try:
            instance = Book.objects.get(id=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            remaining_data = Book.objects.all()
            serializer = BookSerializer(remaining_data, many=True)
            return Response(
                {
                    "success": True,
                    "message": "Book deleted successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to delete this book",
                    "error": str(e),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete book",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
