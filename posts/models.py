from django.db import models

# Create your models here.
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категорія")
    def __str__(self):
        return self.name
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст посту")
    preview_image = models.ImageField(upload_to="blog_previews/", blank=True, null=True, verbose_name="Прев'ю фото")
    created_at= models.DateTimeField(auto_now_add=True, verbose_name="Дата свторення")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_posts', blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категорія")
    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    likes = models.ManyToManyField(CustomUser, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_comments', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Коментар від {self.author.username} до '{self.post.title}'"

