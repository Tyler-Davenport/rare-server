from rest_framework import serializers
from .models import Post
from .models import Comment

class PostSerializer(serializers.ModelSerializer):
  """JSON serializer for posts"""
  class Meta:
    model = Post
    fields = ('id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') # rare_user_id was omitted to hide user id in requests

class CommentSerializer(serializers.ModelSerializer):
  """JSON serializer for comments"""
  class Meta:
    model = Comment
    fields = ('id', 'author_id', 'post_id', 'content', 'created_on')
    depth = 1  # Include related user and post data in the serialized output
