from django.urls import path

from apps.blog.api_endpoints import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateGetAPIView,
    PostAndProductListAPIView,
)

app_name="blog"

urlpatterns = [
    path("post/create/", PostCreateAPIView.as_view(), name="post-create"),
    path("post/list/", PostListAPIView.as_view(), name="post-list"),
    path("post/<int:pk>/detail/", PostDetailAPIView.as_view(), name="post-detail"),
    path("post/<int:pk>/delete/", PostDeleteAPIView.as_view(), name="post-delete"),
    path("post/<int:pk>/update/", PostUpdateGetAPIView.as_view(), name="post-update"),
    path("posts/products/list/", PostAndProductListAPIView.as_view(), name="posts-products-list")
]