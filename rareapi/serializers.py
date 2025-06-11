from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
  """JSON serializer for posts"""
  class Meta:
    model = Post
    fields = ('id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') # rare_user_id was omitted to hide user id in requests
