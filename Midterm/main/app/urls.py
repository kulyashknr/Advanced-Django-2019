from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import Register, ProductViewSet, ServiceViewSet


urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view())
]

router = routers.DefaultRouter()
router.register('products', ProductViewSet, base_name='app')
router.register('services', ServiceViewSet, base_name='app')

urlpatterns += router.urls