from django.contrib import admin
from .models import MainUser, Article, FavoriteArticle
from django.contrib.auth.admin import UserAdmin

@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'role', )


admin.site.register(Article)
admin.site.register(FavoriteArticle)