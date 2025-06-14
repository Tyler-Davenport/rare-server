from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rareapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class CategoryViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """Handle GET requests to retrieve all categories"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests to retrieve a single category by ID"""
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests to create a new category"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(
                label=serializer.validated_data['label']
            )
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.label = request.data.get('label')
        category.save()

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
