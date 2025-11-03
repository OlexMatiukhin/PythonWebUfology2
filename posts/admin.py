from django.contrib import admin

from posts.models import Category, BlogPost


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'likes', 'dislikes')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'