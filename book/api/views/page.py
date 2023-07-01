from rest_framework.views import APIView
from rest_framework import status
from book.models.book import Book
from book.models.page import Page
from rest_framework.response import Response
from book.api.serializers import PageSerializer
from rest_framework.exceptions import PermissionDenied
from book.permissions import IsAuthor


class PageView(APIView):
    """
    A view for retrieving pages for a book.

    The view handles GET requests for retrieving pages for a book with a specific ID. The view can retrieve all pages for a book or a specific page by number.

    Attributes:
        serializer_class (class): The serializer class to use for serializing and deserializing page data.
        permission_classes (list): The permission classes to use for authorizing access to the view.
    """

    serializer_class = PageSerializer
    permission_classes = [IsAuthor]

    def get(self, request, id, pk=None):
        """
        Retrieve pages for a book.

        The method retrieves pages for a book with the corresponding ID. If a page number is provided, the method retrieves a specific page.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            id (int): The ID of the book to retrieve pages for.
            pk (int, optional): The page number to retrieve.

        Returns:
            django.http.HttpResponse: The HTTP response containing the retrieved pages.

        Raises:
            Exception: If there is an error retrieving the pages.
        """
        try:
            if pk is None:
                queryset = Page.objects.filter(book=id)
                serializer = self.serializer_class(queryset, many=True)
            else:
                queryset = Page.objects.get(page_number=id)
                serializer = self.serializer_class(queryset)

            return Response(
                {
                    "success": True,
                    "message": "Pages retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to retrieve pages",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, id):
        """
        Create a new page for a book.

        The method creates a new page for the book with the corresponding ID. The method expects page data in the request body.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            id (int): The ID of the book to create a page for.

        Returns:
            django.http.HttpResponse: The HTTP response containing the created page.

        Raises:
            Book.DoesNotExist: If the book with the provided ID does not exist.
            Exception: If there is an error creating the page.
        """
        try:
            book = Book.objects.get(pk=id)
            page_data = request.data
            page_data["book"] = id
            serializer = self.serializer_class(data=page_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book)

            return Response(
                {
                    "success": True,
                    "message": "Page created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Book.DoesNotExist as e:
            return Response(
                {
                    "success": False,
                    "message": "Book not found",
                    "error": str(e),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to create page",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, id, pk):
        """
        Update an existing page for a book.

        The method updates an existing page with the provided page number for the book with the corresponding ID. The method expects page data in the request body.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            id (int): The ID of the book that the page belongs to.
            pk (int): The page number of the page to update.

        Returns:
            django.http.HttpResponse: The HTTP response containing the updated page.

        Raises:
            Page.DoesNotExist: If the page with the provided page number does not exist for the book with the provided ID.
            PermissionDenied: If the requesting user does not have permission to update the page.
            Exception: If there is an error updating the page.
        """
        try:
            instance = Page.objects.get(book=id, pk=pk)
            self.check_object_permissions(request, instance)
            serializer = self.serializer_class(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Page updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Page.DoesNotExist as e:
            return Response(
                {"success": False, "message": "Page not found", "error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except PermissionDenied as e:
            return Response(
                {
                    "success": False,
                    "message": "You are not authorized to update this page",
                    "error": str(e),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update page",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, id, pk):
        """
        Delete an existing page for a book.

        The method deletes an existing page with the provided page number for the book with the corresponding ID.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            id (int): The ID of the book that the page belongs to.
            pk (int): The page number of the page to delete.

        Returns:
            django.http.HttpResponse: The HTTP response indicating whether the page was deleted successfully.

        Raises:
            Page.DoesNotExist: If the page with the provided page number does not exist for the book with the provided ID.
            PermissionDenied: If the requesting user does not have permission to delete the page.
            Exception: If there is an error deleting the page.
        """
        try:
            instance = Page.objects.get(book=id, pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response(
                {"success": True, "message": "Page deleted successfully"},
                status=status.HTTP_200_OK,
            )

        except Page.DoesNotExist as e:
            return Response(
                {"success": False, "message": "Page not found", "error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied as e:
            return Response(
                {
                    "success": False,
                    "message": "You are not authorized to delete this page",
                    "error": str(e),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete page",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
