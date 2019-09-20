from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'

class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    address = models.CharField(max_length=255)
    web_site = models.CharField(max_length=255)
    #avatar =

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)

class Block(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    #creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
    #executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    order = models.IntegerField

class TaskDocument(models.Model):
    #document =
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)