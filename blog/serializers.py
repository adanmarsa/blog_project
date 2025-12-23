from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "category",
            "tags",
            "created_at",
        ]
        read_only_fields = ["slug", "created_at"]
