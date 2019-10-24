from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import ProjectListCreateView, TaskListCreateView, TaskDetailView, MyTasksListView, BlockTaskListView, ProjectMembersListCreateView


from .views import RegisterUserAPIView, UserViewSet

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', RegisterUserAPIView.as_view()),
    path('projects/', ProjectListCreateView.as_view()),
    path('projects/<int:project_id>/', TaskListCreateView.as_view()),
    path('projects/<int:project_id>/members/', ProjectMembersListCreateView.as_view()),
    #path('projects/<int:project_id>/<str:block>/', BlockTaskListView.as_view()),
    path('projects/<int:project_id>/my/', MyTasksListView.as_view()),
    path('projects/<int:project_id>/<int:task_id>/', TaskDetailView.as_view()),

]


router = DefaultRouter()
router.register('users', UserViewSet, base_name='users')
urlpatterns += router.urls