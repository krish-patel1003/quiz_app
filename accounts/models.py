from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.core.cache import cache


class CustomUserQuerySet(models.QuerySet):

    def all(self):
        cache_key = 'all_users'
        users = cache.get(cache_key)

        if users is None:
            users = list(super().all())
            cache.set(cache_key, users, timeout=60*60*24)
        
        return users


class CustomUserManager(BaseUserManager):

    def __create(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, password=password,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self.__create(username, password, **extra_fields)
    

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.__create(username, password, **extra_fields)
    

    # def get_queryset(self):
    #     return CustomUserQuerySet(self.model, using=self._db)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
        
    username = models.CharField(max_length=50, unique=True, null=False, db_index=True)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Unique related_name
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id} - {self.username}"
    
    def save(self, *args, **kwargs):
        cache.delete('all_posts')
        super().save(*args, **kwargs)