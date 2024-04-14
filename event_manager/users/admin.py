from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rating', 'is_staff')

admin.site.register(User, CustomUserAdmin)
