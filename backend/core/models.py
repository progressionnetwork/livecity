from email.policy import default
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

class FileUpdateManager(models.Manager):
    def get_last_update(self, type_file):
        return self.filter(type_file=type_file).order_by('-date_upload').first()

class FileUpdate(models.Model):
    TYPES_FILES = (
        ('sn', 'sn'),
        ('smeta', 'smeta'),
        ('spgz', 'spgz')
    )

    TYPES_UPDATE = (
        ('full', 'full'),
        ('add', 'add'),
    )
    type_file = models.CharField(choices=TYPES_FILES, max_length=10)
    type_update = models.CharField(choices=TYPES_UPDATE, max_length=10, default='full')
    file = models.FileField(upload_to="files")
    date_upload = models.DateTimeField(auto_now=True)
    objects = FileUpdateManager()

    def __str__(self) -> str:
        return f"{self.file.url}"

    def send_rabbitmq(self):
        print(f"{self.type_file}")
        import pika
        connection = pika.BlockingConnection(
            parameters=pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=self.type_file.lower())
        channel.basic_publish(exchange='', routing_key=self.type_file.lower(), body=json.dumps(
            {'type_data': self.type_file, 'source': 'file', 'path': self.file.path, 'type_update': self.type_update}))
        connection.close()

    class Meta:
        verbose_name = "Файл обновления справочника"
        verbose_name_plural = "Файлы обновления справочника"


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


class SN(models.Model):
    ''' Сметные нормативы и территориальные сметные нормативы'''
    type_ref = models.CharField('Тип сбоника', max_length=250) #3
    advance = models.IntegerField("Дополнение", default=0) #4
    coef_ref = models.IntegerField("Номер сборника", default=0) #5
    coef_date = models.DateField("Дата сборника") #6
    sum = models.FloatField('Итого', default=0.0) #29
    tax = models.FloatField('НДС', default=0.0) #30
    sum_with_tax = models.FloatField('Итого с НДС', default=0.0) #31
    sum_with_ko = models.FloatField('Итого с коэф. фин. обеспеч.', default=0.0) #32

    def __str__(self) -> str:
        return f"{self.type_ref}"

    class Meta:
        verbose_name = "СН и ТСН"
        verbose_name_plural = "СН и ТСН"

class SNSection(models.Model):
    ''' Раздел СН и ТСН '''

    sn = models.ForeignKey('SN', on_delete=models.CASCADE, related_name='sections') 
    name = models.CharField('Наименование', max_length=250) #7
    sum = models.FloatField('Итого', default=0.0) #28

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Раздел"
        verbose_name_plural = "СН и ТСН: Разделы"

class SNSubsection(models.Model):
    ''' Подраздел СН и ТСН '''

    sn_section = models.ForeignKey('SNSection', on_delete=models.CASCADE, related_name='subsections')
    name = models.CharField('Наименование', max_length=250) #8
    sum = models.FloatField('Итого', default=0.0) #27

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Подраздел"
        verbose_name_plural = "СН и ТСН: Подразделы"

class SNRow(models.Model):
    ''' Строка СН и ТСН '''

    sn_subsection = models.ForeignKey('SNSubsection', on_delete=models.CASCADE, related_name='rows')
    code = models.CharField('Шифр', max_length=100) #2
    num = models.IntegerField('Номер п/п', default=0) #1
    name = models.TextField('Наименование') #9
    ei = models.ForeignKey('OKEI', on_delete=models.SET_NULL, null=True, blank=True) #10
    count = models.FloatField('Количество', default=0.0) #11
    sum = models.FloatField('Итого', default=0.0) #26

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Строка"
        verbose_name_plural = "СН и ТСН: Строки"

class SNSubRow(models.Model):
    ''' Статьи затрат по строке '''
    sn_row = models.ForeignKey('SNRow', on_delete=models.CASCADE, related_name='subrows')
    name = models.TextField('Наименование') #12, 19, 20, 21, 22, 23, 24, 25
    ei = models.ForeignKey('OKEI', on_delete=models.SET_NULL, null=True, blank=True) #10
    count = models.FloatField('Количество', default=0.0) #11
    amount = models.FloatField('Цена за единицу', default=1.0) #13
    coef_correct = models.FloatField('Корректировочный коэф', default=1.0) #14
    coef_winter = models.FloatField('Зимний коэф', default=1.0) #15
    coef_recalc = models.FloatField('Коэф. пересчета', default=1.0) #17
    sum_basic =  models.FloatField('Затраты в базисном уровне', default=0.0) #16
    sum_current =  models.FloatField('Затраты в текущем уровне', default=0.0) #18
    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Статья затрат"
        verbose_name_plural = "СН и ТСН: Статьи затрат"

class SPGZ(models.Model):
    ''' Справочник предметов государственного заказа '''
    id = models.IntegerField(default=0, primary_key=True)
    kpgz = models.ForeignKey('KPGZ', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)
    name = models.TextField('Наименование')
    ei = models.ManyToManyField('OKEI', related_name='spgz')
    okpd = models.ForeignKey('OKPD', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)
    okpd2 = models.ForeignKey('OKPD2', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СПГЗ"
        verbose_name_plural = "СПГЗ"