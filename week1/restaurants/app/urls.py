from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, Register
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view()),
    #path('task_list/<int:pk>/dishes/', DishesList),
    path('register/', Register.as_view()),
    path('login/', obtain_jwt_token),
]
