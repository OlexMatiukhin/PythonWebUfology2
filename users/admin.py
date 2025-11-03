from django.contrib import admin

from users.models import CustomUser


# Register your models here.



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'role', 'password')
    list_filter = ('first_name', 'last_name', 'username', 'email', 'role')
    search_fields = ('first_name', 'last_name', 'username', 'email', 'role')


