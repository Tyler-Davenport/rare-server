from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Post, User, Category
from rareapi.serializers import PostSerializer


class PostView(ViewSet):
  """RARE API posts view"""
  
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
    """Handles GET requests for all post objects
    
    Returns:
      Response -- JSON serialized list of posts"""
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST requests for post
    
    Returns:
      Response -- JSON serialized post instance"""
      
    rare_user = User.objects.get(pk=request.data["rare_user_id"])
    category = Category.objects.get(pk=request.data["category_id"])
    
    post = Post.objects.create(
      rare_user = rare_user,
      category = category,
      title = request.data["title"],
      publication_date = request.data["publication_date"], # replace with datetime.now or equivalent for date?
      image_url = request.data["image_url"],
      content = request.data["content"],
      approved = request.data["approved"],
    )
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Handle PUT requests for a post
    
    Returns:
      Response -- Empty body with 204 status code"""
      
    post = Post.objects.get(pk=pk)
    
    post_rare_user = User.objects.get(pk=request.data["rare_user_id"])
    post_category = Category.objects.get(pk=request.data["category_id"])
    
    post.rare_user = post_rare_user
    post.category = post_category
    post.title = request.data["title"]
    post.publication_date = request.data["publication_date"]
    post.image_url = request.data["image_url"]
    post.content = request.data["content"]
    post.approved = request.data["approved"]
    post.save()
    
    serializer = PostSerializer(post)
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    """Handle DELETE requests for a post
    
    Returns:
      Response -- Empty body with 204 status code"""
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    