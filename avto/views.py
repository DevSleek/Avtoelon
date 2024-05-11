from rest_framework.generics import ListAPIView
from avto.models import Post
from avto.serializers import PostSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    filterset_fields = ('subcategory__category',)