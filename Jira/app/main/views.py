from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, ProjectMemberSerializer #BlockChangeSerializer
from .models import MainUser, Project, Task, ProjectMember

import logging

logger = logging.getLogger(__name__)


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{self.request.user} created")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        print(self.request.user)
        return MainUser.objects.all()


class ProjectListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        logger.info(f"{self.request.user} created project {self.request.data.get('name')}")
        return serializer.save(creator=self.request.user)


class TaskListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'project_id'
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs[self.lookup_field])

    def perform_create(self, serializer):
        logger.info(f"{self.request.user} created task {self.request.data.get('name')}")
        return serializer.save(creator=self.request.user, block_id=1, project_id=self.kwargs[self.lookup_field])


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsStaff, )
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = TaskSerializer
    lookup_field = 'task_id'

    def get_object(self):
        return Task.objects.get(id=self.kwargs[self.lookup_field])

    def perform_update(self, serializer):
        if self.request.user == self.get_object().creator:
            serializer.save()
            logger.info(f"{self.request.user} updated task {self.request.data.get('name')}")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        if self.request.user == self.get_object().creator:
            logger.info(f"{self.request.user} deleted task {self.request.data.get('name')}")
            instance.delete()

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BlockTaskListView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStaff, )
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = TaskSerializer
    lookup_field = 'block'

    def get_queryset(self):
        return Task.objects.filter(block=self.kwargs[self.lookup_field])


class MyTasksListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(executor_id=self.request.user)


# class ChangeBlockView(UpdateAPIView):
#     permission_classes = (IsAuthenticated, IsStaff, )
#     authentication_classes = (JSONWebTokenAuthentication, )
#     serializer_class = BlockChangeSerializer
#
#     def perform_update(self, serializer):
#         if self.request.user == self.get_object().executor:
#             serializer.save()
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class ProjectMembersListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsStaff, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()
    lookup_field = 'project_id'

    def get_queryset(self):
        return ProjectMember.objects.filter(project_id=self.kwargs[self.lookup_field])

    # def perform_create(self, serializer):
    #     if self.request.user == self.get_object().creator:
    #         serializer.save(creator=self.request.user)

