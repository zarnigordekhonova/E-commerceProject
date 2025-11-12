from django.urls import path

from apps.blog.api_endpoints import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
)

app_name="blog"

urlpatterns = [
    path("post/create/", PostCreateAPIView.as_view(), name="post-create"),
    path("post/list/", PostListAPIView.as_view(), name="post-list"),
    path("post/<int:pk>/detail/", PostDetailAPIView.as_view(), name="post-detail"),
]