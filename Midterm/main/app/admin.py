from django.contrib import admin
from .models import MainUser, Profile, Product, Service
from django.contrib.auth.admin import UserAdmin


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    inlines = [InlineProfile, ]
    list_display = ('id', 'username', 'role', )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user',)

admin.site.register(Product)
admin.site.register(Service)