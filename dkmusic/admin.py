from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ['available', 'genre']
    list_display = ['name', 'user', 'slug', 'genre', 'created', 'available']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name',]

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['','available']

admin.site.register(Comment)