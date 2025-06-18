from django.contrib.auth import authenticate, get_user_model
from rareapi.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class LoginView(APIView):
    """
    Custom login view that handles email as username.
    Accepts: username (email), password
    Returns: token and user validation
    """

    def post(self, request):
        username = request.data.get("username")  # This will actually be an email
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Since our USERNAME_FIELD is email, we authenticate with email
        user = authenticate(username=username, password=password)

        if user:
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "valid": True, "user": UserSerializer(user).data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"valid": False, "error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


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
