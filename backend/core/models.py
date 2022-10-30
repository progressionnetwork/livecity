import json
from django.db import models
from django.conf import settings
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
    first_name = models.CharField(max_length=190, null=True, blank=True)
    last_name = models.CharField(max_length=190, null=True, blank=True)
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


class SharedManager(models.Manager):
    def update_from_internet(self):
        import pika
        type_data = self.model._meta.model_name
        connection = pika.BlockingConnection(
            parameters=pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=type_data.lower())
        channel.basic_publish(exchange='', routing_key=type_data.lower(), body=json.dumps(
            {'type_data': type_data.upper(), 'source': 'internet'}))
        connection.close()


class KPGZ(models.Model):
    ''' Классификатор предметов государственного заказа '''
    code = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=2000)
    objects = SharedManager()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "КПГЗ"
        verbose_name_plural = "КПГЗ"
        ordering = ['code']


class OKEI(models.Model):
    ''' Общероссийский классификатор единиц измерения '''
    code = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=2000)
    short_name = models.CharField(max_length=50)
    objects = SharedManager()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "ОКЕИ"
        verbose_name_plural = "ОКЕИ"
        ordering = ['code']


class OKPD(models.Model):
    ''' Общероссийский классификатор продукции по видам экономической деятельности '''
    code = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=2000)
    objects = SharedManager()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "ОКПД"
        verbose_name_plural = "ОКПД"
        ordering = ['code']

class OKPD2(models.Model):
    ''' Общероссийский классификатор продукции по видам экономической деятельности '''
    code = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=2000)
    objects = SharedManager()
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "ОКПД2"
        verbose_name_plural = "ОКПД2"
        ordering = ['code']