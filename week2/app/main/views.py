from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, ProjectMemberSerializer #BlockChangeSerializer
from .models import MainUser, Project, Task, ProjectMember


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        return serializer.save(creator=self.request.user)


class TaskListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'project_id'

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs[self.lookup_field])

    def perform_create(self, serializer):
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
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        if self.request.user == self.get_object().creator:
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

    # class ProjectListCreate(APIView):
    #     permission_classes = (IsAuthenticated, )
    #     http_method_names = ['get', 'post']
    #
    #     def get(self, request):
    #         projects = Project.objects.all()
    #         serializer = ProjectListSerializer(projects, many=True)
    #         return Response(serializer.data)
    #
    #     def post(self, request):
    #         serializer = ProjectCreateSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(creator=request.user)
    #             return Response(serializer.data)
    #         return Response(serializer.errors)
    #
    #
    # class ProjectViewSet(mixins.RetrieveModelMixin,
    #                      viewsets.GenericViewSet):
    #     http_method_names = ['get', 'post']
    #     queryset = Project.objects.all()
    #     permission_classes = (IsAuthenticated,)
    #
    #     def get_serializer_class(self):
    #         if self.action == 'retrieve':
    #             return ProjectDetailedSerializer
    #         return ProjectListSerializer
    #
    #     @action(methods=['GET'], detail=True)
    #     def tasks(self, request, pk):
    #         instance = self.get_object()
    #         tasks = Task.objects.filter(block__project=instance)
    #         serializer = TaskSerializer(tasks, many=True)
    #         return Response(serializer.data)
    #
    #     @action(methods=['GET', 'POST'], detail=True)
    #     def blocks(self, request, pk):
    #         if request.method == 'GET':
    #             instance = self.get_object()
    #             blocks = Block.objects.filter(project=instance)
    #             serializer = BlockListSerializer(blocks, many=True)
    #             return Response(serializer.data)
    #         if request.method == 'POST':
    #             instance = self.get_object()
    #             serializer = BlockCreateSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save(project=instance)
    #                 return Response(serializer.data)
    #             return Response(serializer.errors)
    #
    #
    # class ProjectRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    #     http_method_names = ['get', 'put', 'patch', 'delete']
    #     serializer_class = ProjectCreateSerializer
    #     queryset = Project.objects.all()
    #
    #     def get_permissions(self):
    #         if self.request.method in ['put', 'patch', 'delete']:
    #             self.permission_classes = [IsOwner, ]
    #         else:
    #             self.permission_classes = [IsAuthenticated, ]
    #         return super(ProjectRetrieveUpdateDelete, self).get_permissions()
    #
    #
    # class BlockViewSet(mixins.ListModelMixin,
    #                     mixins.RetrieveModelMixin,
    #                     mixins.UpdateModelMixin,
    #                     mixins.DestroyModelMixin,
    #                     viewsets.GenericViewSet):
    #     http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    #     queryset = Block.objects.all()
    #     permission_classes = (BlockPermission, )
    #
    #     def get_serializer_class(self):
    #         if self.action == 'list':
    #             return BlockListSerializer
    #         if self.action == 'retrieve':
    #             return BlockDetailSerializer
    #         return BlockCreateSerializer
    #
    #     @action(methods=['GET', 'POST'], detail=True)
    #     def tasks(self, request, pk):
    #         if request.method == 'GET':
    #             instance = self.get_object()
    #             tasks = Task.objects.filter(block=instance)
    #             serializer = TaskListSerializer(tasks, many=True)
    #             return Response(serializer.data)
    #         if request.method == 'POST':
    #             instance = self.get_object()
    #             serializer = TaskCreateSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save(block=instance, creator=request.user)
    #                 return Response(serializer.data)
    #             return Response(serializer.errors)
    #
    #
    # class TaskViewSet(mixins.ListModelMixin,
    #                     mixins.RetrieveModelMixin,
    #                     mixins.UpdateModelMixin,
    #                     mixins.DestroyModelMixin,
    #                     viewsets.GenericViewSet):
    #     http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    #     queryset = Task.objects.all()
    #     serializer_class = TaskSerializer
    #     permission_classes = (TaskPermission, )
    #
    #     @action(methods=['GET'], detail=False)
    #     def my(self, request):
    #         tasks = Task.objects.filter(creator=self.request.user)
    #         serializer = self.get_serializer(tasks, many=True)
    #         return Response(serializer.data)
    #
    #     @action(methods=['GET', 'POST'], detail=True)
    #     def comments(self, request, pk):
    #         if request.method == 'GET':
    #             instance = self.get_object()
    #             comments = TaskComment.objects.filter(task=instance)
    #             serializer = TaskCommentListSerializer(comments, many=True)
    #             return Response(serializer.data)
    #         if request.method == 'POST':
    #             instance = self.get_object()
    #             serializer = TaskCommentSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save(creator=request.user, task=instance)
    #                 return Response(serializer.data)
    #             return Response(serializer.errors)
    #
    #     @action(methods=['GET', 'POST'], detail=True)
    #     def documents(self, request, pk):
    #         if request.method == 'GET':
    #             instance = self.get_object()
    #             docs = TaskDocument.objects.filter(task=instance)
    #             serializer = TaskDocumentListSerializer(docs, many=True)
    #             return Response(serializer.data)
    #         if request.method == 'POST':
    #             instance = self.get_object()
    #             serializer = TaskDocumentSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save(creator=request.user, task=instance)
    #                 return Response(serializer.data)
    #             return Response(serializer.errors)
    #
    #
    # class TaskCommentViewSet(mixins.RetrieveModelMixin,
    #                     mixins.DestroyModelMixin,
    #                     viewsets.GenericViewSet):
    #     http_method_names = ['get', 'post', 'delete']
    #     queryset = TaskComment.objects.all()
    #     serializer_class = TaskCommentSerializer
    #     permission_classes = (TaskInsidePermission, )
    #
    #
    # class TaskDocumentViewSet(mixins.RetrieveModelMixin,
    #                     mixins.DestroyModelMixin,
    #                     viewsets.GenericViewSet):
    #     http_method_names = ['get', 'post', 'delete']
    #     queryset = TaskDocument.objects.all()
    #     serializer_class = TaskDocumentSerializer
    #     permission_classes = (TaskInsidePermission, )