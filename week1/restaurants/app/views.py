from django.http import Http404
from django.shortcuts import render
from .models import Restaurant, Dish
from .serializers import RestaurantSerializer, DishSerializer, UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class RestaurantListView(APIView):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestaurantDetailView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurants = self.get_object(pk)
        serializer = RestaurantSerializer(restaurants)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurants = self.get_object(pk)
        serializer = RestaurantSerializer(instance=restaurants, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Register(CreateAPIView):
1
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        return serializer.save()