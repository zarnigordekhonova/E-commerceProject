from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.products.models import ProductComment


class ProductCommentDeleteAPIView(DestroyAPIView):
    """
    Generic APIView endpoint for deleting a personal comment.
    DELETE api/products/comment/id/delete/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(204 No Content):
    {
        "detail": "Comment deleted successfully."
    }
    """
    queryset = ProductComment.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    

__all__ = [
    "ProductCommentDeleteAPIView"
]