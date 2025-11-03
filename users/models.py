
from django.contrib.auth.models import AbstractUser
from django.db import models

# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('blogger', 'Blogger'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    objects = CustomUserManager()
