from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from .constants import USER_ROLES, USER_GUEST, USER_STOREADMIN, USER_SUPERADMIN, PRODUCT_TYPES, PRODUCT_TOYS, \
    PRODUCT_MEAL, PRODUCT_CLOTHES, PRODUCT_ALL, SERVICE_TYPES, SERVICE_ALL
from rest_framework.authtoken.models import Token
import datetime


# Create your models here.


class MainUser(AbstractUser):
    role (choices=USER_ROLES, default=USER_GUEST, max_length=255)= models.CharField

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{ self.id }: { self.username }, { self.role }'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class ProductServiceBase(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(ProductServiceBase):
    size = models.IntegerField()
    type = models.CharField(choices=PRODUCT_TYPES, default=PRODUCT_ALL, max_length=255)
    existence = models.BooleanField()

    def __str__(self):
        return f'{ self.name }: { self.price }, { self.existence }'


class Service(ProductServiceBase):
    service_type = models.CharField(choices=SERVICE_TYPES, default=SERVICE_ALL, max_length=255)
    approximate_duration = models.IntegerField()
