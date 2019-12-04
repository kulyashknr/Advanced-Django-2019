from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
from .constraints import TASK_STATUSES, NEW_TASKS, DONE_TASKS

from utils.upload import task_document_path
from utils.validators import validate_extension, validate_file_size


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


class TaskDoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=DONE_TASKS)

    def done_tasks(self):
        return self.filter(status=DONE_TASKS)

    def filter_by_status(self, status):
        return self.filter(status=status)


class TaskNewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=NEW_TASKS)

    def filter_by_status(self, status):
        return self.filter(status=status)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)


class Block(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    #status = models.PositiveSmallIntegerField(choices=TASK_STATUSES)


class Task(models.Model):
    name = models.CharField(max_length=255)
    task_description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='task_creator')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='task_executor')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    order = models.IntegerField
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='project_name')
    doc = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension], blank=True, null=True)

    objects = models.Manager()
    done_tasks = TaskDoneManager()
    new_tasks = TaskNewManager()

    class Meta:
       # ordering = ('name', 'status',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name

    def __repr__(self):
        pass


# class TaskDocument(models.Model):
#     document = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension], blank=True, null=True)
#     creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)


# class TaskComment(models.Model):
#     body = models.TextField(max_length=500)
#     creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)