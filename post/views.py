from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post, Category
from .serializers import CategorySerializer, PostSerializer


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny,]
    pagination_class = None

class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny,]
