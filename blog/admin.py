from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at', 'published_at']
    list_filter = ['status']
    search_fields = ['title', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
