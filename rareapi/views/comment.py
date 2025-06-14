from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment
from rareapi.serializers import CommentSerializer

class CommentViewSet(ViewSet):
    def list(self, request):
        """Handle GET requests to retrieve all comments"""
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
            comment = Comment.objects.create(
                author_id=serializer.validated_data['author_id'],
                post_id=serializer.validated_data['post_id'],
                content=serializer.validated_data['content']
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data.get('content', comment.content)
        comment.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

