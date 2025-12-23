from django.urls import path
from .api_views import PostListCreateAPIView,PostDetailAPIView

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="api-posts"),
    path("posts/<int:pk>/", PostDetailAPIView.as_view()),
]