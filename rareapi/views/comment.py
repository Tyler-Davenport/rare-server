from rareapi.models import Comment, Post
from rareapi.models.user import User
from rareapi.serializers import CommentSerializer
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """Handle GET requests to retrieve all comments or filter by post_id"""
        post_id = request.query_params.get("post_id", None)
        if post_id:
            comments = Comment.objects.filter(post_id=post_id)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests to create a new comment"""
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                author = User.objects.get(pk=serializer.validated_data["author_id"])
                post = Post.objects.get(pk=serializer.validated_data["post_id"])
                comment = Comment.objects.create(
                    author=author,
                    post=post,
                    content=serializer.validated_data["content"],
                )
                return Response(
                    CommentSerializer(comment).data, status=status.HTTP_201_CREATED
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "Author not found."}, status=status.HTTP_400_BAD_REQUEST
                )
            except Post.DoesNotExist:
                return Response(
                    {"error": "Post not found."}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # TODO: Add check to ensure request.user is the author of the comment
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data.get("content", comment.content)
        comment.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        # TODO: Add check to ensure request.user is the author of the comment
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
