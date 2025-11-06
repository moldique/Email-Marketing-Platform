from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)
