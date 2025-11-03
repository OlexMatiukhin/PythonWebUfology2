from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть password'}))

    class Meta:
        model = CustomUser
        fields = ['username',  'password']





class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть surname'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть username'})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть пароль'})
    )

    # Добавляем поле role
    role = forms.ChoiceField(
        choices=[('user', 'User'), ('blogger', 'Blogger')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем роли только user и blogger, если надо динамически
        self.fields['role'].choices = [
            ('user', 'User'),
            ('blogger', 'Blogger'),
        ]
