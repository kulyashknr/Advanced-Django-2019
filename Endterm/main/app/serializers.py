from django.db import transaction
from rest_framework import serializers
from .models import MainUser, Article, FavoriteArticle


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class ShortArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'name')


class FullArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

        def validate_price(self, value):
            if value < 0:
                raise serializers.ValidationError('Price > 0')
            return value


class FavoriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
