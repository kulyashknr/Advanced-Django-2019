from django.db import transaction
from rest_framework import serializers
from .models import MainUser, Product, Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_size(self, value):
        if value > 50 or value < 20:
            raise serializers.ValidationError('Range between 20 and 50')
        return value


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_approximate_duration(self, value):
        if value < 0:
            raise serializers.ValidationError('Not negative number')
        return value