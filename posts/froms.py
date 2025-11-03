from django import forms
from posts.models import BlogPost
from .models import Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content',  'preview_image', 'category']
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок...'}),
            'content': forms.Textarea(attrs={
                'class' : 'form-textarea',
                'placeholder': "Напишіть текст посту..."
            }),

        }
# models.py

from django.db import models
from users.models import CustomUser

# forms.py


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишіть свій коментар...'
            })
        }
