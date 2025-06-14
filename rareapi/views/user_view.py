from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rareapi.serializers import UserSerializer

class CurrentUserView(APIView):
    """View to manage the current authenticated user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET requests to retrieve the current user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Handle PUT requests to update the current user's profile."""
        user = request.user
        # UserSerializer has password as write_only
        
        data = request.data.copy()
        if 'password' in data:
            data.pop('password') 

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
