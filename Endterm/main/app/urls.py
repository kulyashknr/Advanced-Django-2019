from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import Register, ArticleViewSet, FavoriteArticleAPIView


urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view()),
    path('articles/favorites/', FavoriteArticleAPIView.as_view())
]

router = routers.DefaultRouter()
router.register('articles', ArticleViewSet, base_name='app')

urlpatterns += router.urls