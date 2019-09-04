from rest_framework import serializers
from .models import Restaurant, Dish
from django.contrib.auth.models import User



class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'created_by')

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'restaurant')

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.get("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)