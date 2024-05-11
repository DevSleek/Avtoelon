from django.urls import path
from avto.views import PostListAPIView

urlpatterns = [
    path('', PostListAPIView.as_view()),
]