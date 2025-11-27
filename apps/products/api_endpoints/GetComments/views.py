from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter

from apps.products.models import ProductComment
from .serializers import ProductCommentSerializer


class GetReviewsListAPIView(ListAPIView):
    serializer_class = ProductCommentSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "product_id"
    filter_backends = [OrderingFilter]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductComment.objects.filter(
            product_id=product_id
        ).select_related('user')
    

__all__ = [
    "GetReviewsListAPIView"
]

