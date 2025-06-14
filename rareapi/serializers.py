from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user registration and responses"""
    password = serializers.CharField(write_only=True, required=True)
    created_on = serializers.DateField(read_only=True, format="%Y-%m-%d") # Explicitly define and format
    
    class Meta:
        """Meta class for UserSerializer"""
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'bio', 'profile_image_url', 'created_on')
        read_only_fields = ('id', 'created_on')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data.get('bio', ''),
            profile_image_url=validated_data.get('profile_image_url')
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        """Meta class for PostSerializer"""
        model = Post
        fields = ('id', 'rare_user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        """Meta class for CommentSerializer"""
        model = Comment
        fields = ('id', 'author_id', 'post_id', 'content', 'created_on')
        depth = 1  # Include related user and post data in the serialized output

