from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import USER_ROLES, USER_GUEST, COLORS, COLOR_BLACK
from utils.upload import article_image_path
from utils.validators import validate_file_size, validate_extension

from rest_framework.authtoken.models import Token
import datetime


class MainUser(AbstractUser):
    role = models.CharField(choices=USER_ROLES, default=USER_GUEST, max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{ self.id }: { self.username }, { self.role }'


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField
    price = models.IntegerField
    city = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    color = models.CharField(choices=COLORS, default=COLOR_BLACK, max_length=255)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    doc = models.FileField(upload_to=article_image_path, validators=[validate_file_size, validate_extension], blank=True, null=True)


class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name='fav_article')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='fav_user')