from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
  """JSON serializer for posts"""
  class Meta:
    model = Post
    fields = ('id', 'rare_user_id','category_id', 'title', 'publication_date', 'image_url', 'content', 'approved')
    depth = 1
