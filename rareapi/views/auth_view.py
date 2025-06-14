from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rareapi.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterView(APIView):
    """
    View for user registration.
    Accepts: first_name, last_name, email, password
    Returns: User data (excluding password)
    """
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Get the serialized user data (password is write-only)
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    """
    View to list all users.
    Requires token authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
