from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductRating


# Just in case
class ProductRatingDeleteAPIView(DestroyAPIView):
    """
    Generic APIView endpoint for deleting the rating.
    
    DELETE api/products/delete/id/rating/
    For id, make sure you enter the rating id, not product id.

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(204 No Content):
    {
        "detail": "Rating deleted successfully."
    }

    """
    queryset = ProductRating.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own rating.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Rating deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    

__all__ = [
    "ProductRatingDeleteAPIView"
]