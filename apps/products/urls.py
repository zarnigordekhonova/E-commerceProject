from django.urls import path

from apps.products.api_endpoints import (
    CategoryListAPIView,
    ProductListByCategoryAPIView,
    ProductCreateAPIView,
    ProductsListAPIView,
    ProductDetailAPIView,
    ProductCommentCreateAPIView,
    ProductCommentDeleteAPIView,
    ProductRatingAddAPIView,
    ProductRatingDeleteAPIView,
    AddToWishlistAPIView,
    FavoriteListAPIView,
    AddProductVariantAPIView,
    OptionCreateAPIView,
    AddOptionValueAPIView,
    GetReviewsListAPIView,
    OptionsListAPIView,
)

app_name = "products"

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("category/<int:category_id>/products/", ProductListByCategoryAPIView.as_view(), name="category-products"),
    path("list/", ProductsListAPIView.as_view(), name="products-list"),
    path("<int:pk>/detail", ProductDetailAPIView.as_view(), name="product-detail"),
    path("comment/create/", ProductCommentCreateAPIView.as_view(), name="comment-create"),
    path("comment/<int:pk>/delete/", ProductCommentDeleteAPIView.as_view(), name="comment-delete"),
    path("add/rating/", ProductRatingAddAPIView.as_view(), name="add-rating"),
    path("delete/<int:pk>/rating/", ProductRatingDeleteAPIView.as_view(), name="rating-delete"),
    path("wishlist/<int:product_variant_id>/add/", AddToWishlistAPIView.as_view(), name="add-to-wishlist"),
    path("wishlist/", FavoriteListAPIView.as_view(), name="wishlist-list"),
    path("add/", ProductCreateAPIView.as_view(), name="product-add"),
    path("variant/add/", AddProductVariantAPIView.as_view(), name="product-variant-add"),
    path("option/add/", OptionCreateAPIView.as_view(), name="option-add"),
    path("option/value/add/", AddOptionValueAPIView.as_view(), name="option-value-add"),
    path("comments/<int:product_id>/list/", GetReviewsListAPIView.as_view(), name="comments-list"),
    path("options/list/", OptionsListAPIView.as_view(), name="options-list"),
]