from rest_framework import generics,permissions
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.models import User
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    