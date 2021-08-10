from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'username', 'password', 'is_superuser')
