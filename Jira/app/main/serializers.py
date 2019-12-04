from rest_framework import serializers
from .models import MainUser, Project, Task, ProjectMember


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError('Positive number')
        return value

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class BlockChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('block', )

