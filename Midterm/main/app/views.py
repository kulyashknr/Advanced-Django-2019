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

from .serializers import UserSerializer, ProductSerializer, ServiceSerializer
from .models import Product, Service


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


class ProductViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdmin, )

    @action(methods=['GET'], detail=False)
    def meal(self, request):
        products = Product.objects.filter(type=4)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def all(self, request):
        products = Product.objects.filter(type=1)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ServiceViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = Service.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdmin, )

    @action(methods=['GET'], detail=False)
    def services(self, request):
        services = Service.objects.all()
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)