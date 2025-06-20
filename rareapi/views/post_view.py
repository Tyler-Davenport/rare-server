from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rareapi.models import Post, User, Category
from rareapi.serializers import PostSerializer


class PostView(ViewSet):
    """RARE API posts view"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk):
        """Handles GET requests for a single post object

        Returns:
            Response -- JSON serialized post"""

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'No post exists with specified ID': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handles GET requests for all post objects or filters by categoryId if provided

        Returns:
            Response -- JSON serialized list of posts"""
        category_id = request.query_params.get('categoryId', None)
        if category_id:
            posts = Post.objects.filter(category_id=category_id)
        else:
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for post

        Returns:
            Response -- JSON serialized post instance"""

        # TODO: Associate post with request.user instead of request.data["rare_user_id"]
        rare_user = User.objects.get(pk=request.data["rare_user_id"])
        category = Category.objects.get(pk=request.data["category_id"])

        post = Post.objects.create(
            rare_user_id=rare_user,
            category_id=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=request.data["approved"],
        )
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code"""

        post = Post.objects.get(pk=pk)

        # TODO: Check if request.user is the author of the post before allowing update
        # TODO: Avoid changing author via request.data["rare_user_id"]
        # post_rare_user = User.objects.get(pk=request.data["rare_user_id"])
        # post.rare_user = post_rare_user

        post_category = Category.objects.get(pk=request.data["category_id"])

        post.category = post_category # Make sure this aligns with model field name (category or category_id)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a post

        Returns:
            Response -- Empty body with 204 status code"""
        post = Post.objects.get(pk=pk)
        # TODO: Check if request.user is the author of the post before allowing delete
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
