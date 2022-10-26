from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    ''' user manager  '''
    def create_user(self, email, password=None, **extra_fields):
        ''' create user '''
        if not email:
            raise ValueError('Email field is empty')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        ''' create superuser '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    verify_uuid = models.CharField(max_length=36, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return f"{self.username} - {self.email}"
