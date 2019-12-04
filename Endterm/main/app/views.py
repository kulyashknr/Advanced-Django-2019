from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .serializers import UserSerializer, FullArticleSerializer, ShortArticleSerializer, FavoriteArticleSerializer
from .models import Article, FavoriteArticle

import logging

logger = logging.getLogger(__name__)

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class Register(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Article.objects.all()
    serializer_class = FullArticleSerializer

    @action(methods=['POST'], detail=False)
    def perform_create(self, serializer):
        permission_classes = (IsAuthenticated,)
        #if self.request.user
        logger.info(f"{self.request.user} created article {self.request.data.get('name')}")
        return serializer.save(creator=self.request.user)

    @action(methods=['PUT'], detail=True)
    def perform_update(self, serializer):
        permission_classes = (IsAuthenticated,)
        if self.request.user == self.get_object().creator:
            serializer.save()
            logger.info(f"{self.request.user} updated article {self.request.data.get('name')}")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)
    def perform_destroy(self, instance):
        permission_classes = (IsAuthenticated,)
        if self.request.user == self.get_object().creator:
            logger.info(f"{self.request.user} deleted article {self.request.data.get('name')}")
            instance.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['POST'], detail=True)
    # def add(self, request):
    #     #favorites = FavoriteArticle.objects.filter(user=self.request.user)
    #     serializer = FavoriteArticleSerializer(data=request.data)
    #     return Response(serializer.data)

    # @action(methods=['GET'], detail=False)
    # def favorite(self, request):
    #     favorites = FavoriteArticle.objects.filter(user=self.request.user)
    #     serializer = self.get_serializer(favorites, many=True)
    #     return Response(serializer.data)
    #
    # @action(methods=['POST'], detail=False)
    # def favorite(self, request):
    #     serializer = FullArticleSerializer(data=request.data)
    #     logger.info(f"{self.request.user} adds to favorite list {self.request.data.get('name')}")
    #     return serializer.save(user=self.request.user)


class FavoriteArticleAPIView(APIView):
    #http_method_names = ['post', 'get']

    def get(self, request):
        favs = FavoriteArticle.objects.all()
        serializer = self.get_serializer(favs, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = FavoriteArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{self.request.user} adds to favorite")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)