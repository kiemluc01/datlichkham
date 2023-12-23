from rest_framework import viewsets

from .models import Post, Category
from .serializers import CategorySerializer, PostSerializer


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
