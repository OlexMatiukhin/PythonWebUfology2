from django.contrib import admin

from posts.models import Category, BlogPost, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'total_likes', 'total_dislikes')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'

    def total_likes(self, obj):
        return obj.likes.count()

    total_likes.short_description = 'Кількість лайків'

    def total_dislikes(self, obj):
        return obj.dislikes.count()

    total_dislikes.short_description = 'Кількість дизлайків'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'likes_count', 'dislikes_count')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = '👍'

    def dislikes_count(self, obj):
        return obj.dislikes.count()
    dislikes_count.short_description = '👎'




