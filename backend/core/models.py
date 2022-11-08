from email.policy import default
import json
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms.models import model_to_dict

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
        ('spgz', 'spgz'),
        ('spgz_key', 'spgz_key'),
        ('tz', 'tz'),
    )

    TYPES_UPDATE = (
        ('full', 'full'),
        ('add', 'add'),
    )
    type_file = models.CharField(choices=TYPES_FILES, max_length=10)
    type_update = models.CharField(
        choices=TYPES_UPDATE, max_length=10, default='full')
    file = models.FileField(upload_to="files")
    date_upload = models.DateTimeField(auto_now=True)
    objects = FileUpdateManager()

    def __str__(self) -> str:
        return f"{self.file.url}"

    def send_rabbitmq(self):
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
    short_name = models.CharField(max_length=200)
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
    type_ref = models.CharField('Тип сбоника', max_length=250)  # 3
    advance = models.CharField("Дополнение", max_length=250, null=True, blank=True)  # 4
    coef_ref = models.CharField("Номер сборника", max_length=250, null=True, blank=True)  # 5
    coef_date = models.DateField("Дата сборника", null=True, blank=True)  # 6
    sum = models.FloatField('Итого', default=0.0)  # 29
    tax = models.FloatField('НДС', default=0.0)  # 30
    sum_with_tax = models.FloatField('Итого с НДС', default=0.0)  # 31
    sum_with_ko = models.FloatField(
        'Итого с коэф. фин. обеспеч.', default=0.0)  # 32

    def __str__(self) -> str:
        return f"{self.type_ref}"

    def get_dict(self):
        result = model_to_dict(self)
        result['sections'] = list()
        for section in self.sections.all():
            result['sections'].append(section.get_dict())
        return result

    class Meta:
        verbose_name = "СН и ТСН"
        verbose_name_plural = "СН и ТСН"


class SNSection(models.Model):
    ''' Раздел СН и ТСН '''

    sn = models.ForeignKey('SN', on_delete=models.CASCADE,
                           related_name='sections')
    name = models.CharField('Наименование', max_length=250, default='Без имени')  # 7

    def get_dict(self):
        result = model_to_dict(self)
        result['rows'] = list()
        for row in self.rows.all():
            result['rows'].append(model_to_dict(row))
        return result

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Раздел"
        verbose_name_plural = "СН и ТСН: Разделы"


class SNRow(models.Model):
    ''' Строка СН и ТСН '''

    sn_section = models.ForeignKey(
        'SNSection', on_delete=models.CASCADE, related_name='rows')
    code = models.CharField('Шифр', max_length=100)  # 2
    num = models.IntegerField('Номер п/п', default=0)  # 1
    name = models.TextField('Наименование')  # 9
    ei = models.ForeignKey(
        'OKEI', on_delete=models.SET_NULL, null=True, blank=True)  # 10
    count = models.FloatField('Количество', default=0.0)  # 11
    sum = models.FloatField('Итого', default=0.0)  # 26

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СН и ТСН: Строка"
        verbose_name_plural = "СН и ТСН: Строки"


class SNSubRow(models.Model):
    ''' Статьи затрат по строке '''
    sn_row = models.ForeignKey(
        'SNRow', on_delete=models.CASCADE, related_name='subrows')
    name = models.TextField('Наименование')  # 12, 19, 20, 21, 22, 23, 24, 25
    ei = models.ForeignKey(
        'OKEI', on_delete=models.SET_NULL, null=True, blank=True)  # 10
    count = models.FloatField('Количество', default=0.0)  # 11
    amount = models.FloatField('Цена за единицу', default=1.0)  # 13
    coef_correct = models.FloatField(
        'Корректировочный коэф', default=1.0)  # 14
    coef_winter = models.FloatField('Зимний коэф', default=1.0)  # 15
    coef_recalc = models.FloatField('Коэф. пересчета', default=1.0)  # 17
    sum_basic = models.FloatField(
        'Затраты в базисном уровне', default=0.0)  # 16
    sum_current = models.FloatField(
        'Затраты в текущем уровне', default=0.0)  # 18

    def __str__(self) -> str:
        return f"{self.name}"
            
    class Meta:
        verbose_name = "СН и ТСН: Статья затрат"
        verbose_name_plural = "СН и ТСН: Статьи затрат"


class SPGZ(models.Model):
    ''' Справочник предметов государственного заказа '''
    id = models.IntegerField(default=0, primary_key=True)
    kpgz = models.ForeignKey(
        'KPGZ', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)
    name = models.TextField('Наименование')
    ei = models.ManyToManyField('OKEI', related_name='spgz')
    okpd = models.ForeignKey(
        'OKPD', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)
    okpd2 = models.ForeignKey(
        'OKPD2', on_delete=models.SET_NULL, related_name='spgz', null=True, blank=True)
    key = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "СПГЗ"
        verbose_name_plural = "СПГЗ"
        ordering = ['key']


class TZ(models.Model):
    ''' Шаблон ТЗ '''
    name = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "ТЗ"
        verbose_name_plural = "ТЗ"


class TZRow(models.Model):
    ''' Строка шаблона ТЗ '''
    tz = models.ForeignKey(
        'TZ', on_delete=models.CASCADE, related_name='rows')
    kpgz = models.ForeignKey(
        'KPGZ', on_delete=models.CASCADE, related_name='tz')
    spgz = models.ForeignKey(
        'SPGZ', on_delete=models.CASCADE, related_name='tz')

    def __str__(self) -> str:
        return f"{self.kpgz.code} {self.kpgz.name} - {self.spgz.id} {self.spgz.name}"

    class Meta:
        verbose_name = "ТЗ: Строка"
        verbose_name_plural = "ТЗ: Строки"


class Smeta(models.Model):
    ''' Сметные расчеты '''
    name = models.CharField(max_length=1000, default='Без имени')
    address = models.CharField(max_length=1000, default='Без адреса')
    type_ref = models.CharField('Тип сбоника', max_length=250, null=True, blank=True)  # 3
    advance = models.CharField("Дополнение", max_length=250, null=True, blank=True)  # 4
    coef_ref = models.CharField("Номер сборника", max_length=250, null=True, blank=True)  # 5
    coef_date = models.DateField("Дата сборника", null=True, blank=True)  # 6
    sum = models.FloatField('Итого', default=0.0)  # 29
    tax = models.FloatField('НДС', default=0.0)  # 30
    sum_with_tax = models.FloatField('Итого с НДС', default=0.0)  # 31
    sum_with_ko = models.FloatField(
        'Итого с коэф. фин. обеспеч.', default=0.0)  # 32
    status_file = models.IntegerField('Статус сметы', choices=((0,"Загружен файл"), (1, "Загружен в БД"), (2, "Обрабатывается"), (3, "Готов")), default=0)
    tz = models.ForeignKey('TZ', on_delete=models.CASCADE, related_name='smetes', null=True, blank=True)
    
    def get_dict(self):
        result = model_to_dict(self)
        result['sections'] = list()
        for section in self.sections.all():
            d_section = model_to_dict(section)
            d_section['subsections'] = list()
            for subsection in section.subsections.all():
                d_subsection = model_to_dict(subsection)
                d_subsection['rows'] = list()
                for row in subsection.rows.all():
                    d_subsection['rows'].append(model_to_dict(row))
                d_section['subsections'].append(d_subsection)
            result['sections'].append(d_section)
        return result

    def check_row_sum(self):
        sum = 0.0
        for section in self.sections.all():
            for subsection in section.subsections.all():
                for row in subsection.rows.all():
                    sum = sum + row.sum
        check = round(sum, 2) == self.sum
        return {"check": check, "value": round(sum, 2)}

    def check_keys_row_sum(self):
        sum = self.get_sum_keys()
        check = round(sum, 2) == self.sum
        return {"check": check, "value": round(sum, 2)}

    def get_sum_keys(self):
        sum = 0.0
        for section in self.sections.all():
            for subsection in section.subsections.all():
                for row in subsection.rows.filter(is_key=True):
                    sum = sum + row.sum_keys
        return sum

    def set_sum_keys(self):
        sum = 0.0
        current_key_row = None
        for section in self.sections.all():
            for subsection in section.subsections.all():
                if subsection.have_key_rows():
                    current_key_row = None
                    sum = 0.0
                for row in subsection.rows.all().order_by('name'):
                    row.sum_keys = 0
                    row.save()
                    if row.is_key:
                        # если мы нашли первую ключевую позицию
                        if current_key_row is None:
                            # суммируем все что было до нее в разделе
                            row.sum_keys = sum
                            row.save()
                            sum = 0.0
                        current_key_row = row
                        current_key_row.sum_keys += current_key_row.sum
                        current_key_row.save()
                        print(f"Ключевая строка в разделе с ключами: {row}. Сумма: {row.sum}. Ключевая сумма: {current_key_row.sum_keys}")
                    else:
                        # если ключевой позиции еще не было
                        if current_key_row is None:
                            sum += row.sum
                            print(f"Не ключевая строка в разделе с ключами: {row}. Сумма: {row.sum}")
                        # если найдена была складываем туба все
                        else:
                            current_key_row.sum_keys += row.sum
                            current_key_row.save()
                            print(f"Не ключевая строка в разделе без ключей: {row}. Сумма: {row.sum}. Ключевая сумма: {current_key_row.sum_keys}")

    def send_rabbitmq(self):
        import pika
        connection = pika.BlockingConnection(
            parameters=pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue="short_smeta")
        channel.basic_publish(exchange='', routing_key="short_smeta", body=json.dumps(
            {'type_data': "short_smeta", 'id': self.id}))
        connection.close()

    def get_excel(self):
        import io
        import xlsxwriter
        smeta = self
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        number_format = workbook.add_format({'num_format': '#,##0.00', 'align': 'left'})
        header_cell_format = workbook.add_format({'bg_color': '#C5D9F1', 'bold': True, 'border': 1, 'valign': 'vcenter', 'align': 'center'})
        header_cell_format_without_bg = workbook.add_format({'bold': True, 'border': 1, 'valign': 'vcenter', 'align': 'center'})
        cell_format_border = workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'left'})
        # Настройка ширины колонок
        worksheet.set_column(0,0, 6)
        worksheet.set_column(1,1, 12)
        worksheet.set_column(2,2, 35)
        worksheet.set_column(3,3, 45)
        worksheet.set_column(4,4, 18)
        worksheet.set_column(5,5, 40)
        worksheet.set_column(6,7, 12)
        worksheet.set_column(8,8, 15)
        worksheet.set_column(9,9, 40)
        # выводим шапку
        worksheet.merge_range('A1:C1', 'Название сметы:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D1:J1', self.name)
        
        worksheet.merge_range('A2:C2', 'Адрес:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D2:J2', self.address)
        
        worksheet.merge_range('A3:C3', 'Сумма без НДС:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D3:J3', self.sum, number_format)
        
        worksheet.merge_range('A4:C4', 'НДС:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D4:J4', self.sum * 0.2, number_format)
        
        worksheet.merge_range('A5:C5', 'Сумма с НДС:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D5:J5', self.sum * 1.2, number_format)
        
        worksheet.merge_range('A6:C6', 'Нормативный справочник:', workbook.add_format({'align':'right'}))
        worksheet.merge_range('D6:J6', self.type_ref)
        
        worksheet.merge_range('A7:C7', 'Контроль сумм по строкам:', workbook.add_format({'align':'right'}))
        check_sum = self.check_row_sum()
        worksheet.merge_range('D7:J7', f"Пройдена ({check_sum['value']})" if check_sum['check'] else f"Не пройдена ({check_sum['value']})")
        
        worksheet.merge_range('A8:C8', 'Контроль сумм по ключевым строкам:', workbook.add_format({'align':'right'}))
        check_sum = self.check_keys_row_sum()
        worksheet.merge_range('D8:J8', f"Пройдена ({check_sum['value']})" if check_sum['check'] else f"Не пройдена ({check_sum['value']})")
             
        worksheet.merge_range('A9:C9', 'Использованный шаблон:', workbook.add_format({'align':'right'}))
        if self.tz:
            name = self.tz.name
        else:
            name = 'шаблон ТЗ не использовался'
        worksheet.merge_range('D9:J9', name)
        row_num=11
        # шапка таблицы
        worksheet.write("A10", "Номер", header_cell_format)
        worksheet.write("B10", "ИД", header_cell_format)
        worksheet.write("C10", "КПГЗ", header_cell_format)
        worksheet.write("D10", "СПГЗ", header_cell_format)
        worksheet.write("E10", "Шифр", header_cell_format)
        worksheet.write("F10", "Наименование", header_cell_format)
        worksheet.write("G10", "ед. изм.", header_cell_format)
        worksheet.write("H10", "Количество", header_cell_format)
        worksheet.write("I10", "Сумма", header_cell_format)
        worksheet.write("J10", "Адрес", header_cell_format)
        worksheet.write("A11", "1", header_cell_format_without_bg)
        worksheet.write("B11", "2", header_cell_format_without_bg)
        worksheet.write("C11", "3", header_cell_format_without_bg)
        worksheet.write("D11", "4", header_cell_format_without_bg)
        worksheet.write("E11", "5", header_cell_format_without_bg)
        worksheet.write("F11", "6", header_cell_format_without_bg)
        worksheet.write("G11", "7", header_cell_format_without_bg)
        worksheet.write("H11", "8", header_cell_format_without_bg)
        worksheet.write("I11", "9", header_cell_format_without_bg)
        worksheet.write("J11", "10", header_cell_format_without_bg)
        for section in smeta.sections.all():
            for subsection in section.subsections.all():
                for row in subsection.rows.filter(is_key=True):
                    for row_stat in row.stats.all():
                        spgz = row_stat.fasttext_spgz
                        col = 0
                        worksheet.write(row_num, col+0, row.num, cell_format_border)
                        worksheet.write(row_num, col+1, spgz.id, cell_format_border)
                        worksheet.write(row_num, col+2, spgz.kpgz.name, cell_format_border)
                        worksheet.write(row_num, col+3, spgz.name, cell_format_border)
                        worksheet.write(row_num, col+4, row.code, cell_format_border)
                        worksheet.write(row_num, col+5, row.name, cell_format_border)
                        worksheet.write(row_num, col+6, row.ei.short_name if row.ei else "-", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'vcenter', 'align': 'center'}))
                        worksheet.write(row_num, col+7, row.count, workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'vcenter', 'align': 'center'}))
                        worksheet.write(row_num, col+8, row.sum, workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'vcenter', 'align': 'right','num_format': '#,##0.00'}))
                        worksheet.write(row_num, col+9, smeta.address, workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'left'}))
                        row_num += 1
        worksheet.merge_range(f"A{row_num+1}:H{row_num+1}", "ИТОГО без НДС:", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True}))
        worksheet.write(row_num, 8, f"=SUM(I12:I{row_num})", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True,'num_format': '#,##0.00'}))
        worksheet.merge_range(f"A{row_num+2}:H{row_num+2}", "НДС:", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True}))
        worksheet.write(row_num+1, 8, f"=I{row_num+1}*0.2", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True,'num_format': '#,##0.00'}))
        worksheet.merge_range(f"A{row_num+3}:H{row_num+3}", "ИТОГО без НДС:", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True}))
        worksheet.write(row_num+2, 8, f"=I{row_num+1}+I{row_num}", workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top', 'align': 'right', 'border': True,'num_format': '#,##0.00'}))
        workbook.close()
        buffer.seek(0)
        return buffer
    
    def __str__(self) -> str:
        return f"{self.name} ({self.address})"

    class Meta:
        verbose_name = "Смета"
        verbose_name_plural = "Сметы"
        ordering = ['-id']


class SmetaSection(models.Model):
    ''' Раздел сметы '''
    smeta = models.ForeignKey('Smeta', on_delete=models.CASCADE,
                           related_name='sections')
    name = models.CharField('Наименование', max_length=250, default='Без имени')  # 7
    sum = models.FloatField('Итого', default=0.0)  # 28
    address = models.CharField(max_length=1000, default='Без адреса')

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Смета: Раздел"
        verbose_name_plural = "Смета: Разделы"


class SmetaSubsection(models.Model):
    ''' Подраздел сметы '''

    smeta_section = models.ForeignKey('SmetaSection', on_delete=models.CASCADE,
                           related_name='subsections')
    
    name = models.CharField('Наименование', max_length=250, default='Без имени')  # 8
    sum = models.FloatField('Итого', default=0.0)  # 27

    def have_key_rows(self)->bool:
        return self.rows.filter(is_key=True).count() > 0

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Смета: Подраздел"
        verbose_name_plural = "Смета: Подразделы"


class SmetaRow(models.Model):
    ''' Строка сметы '''

    smeta_subsection = models.ForeignKey(
        'SmetaSubsection', on_delete=models.CASCADE, related_name='rows')
    code = models.CharField('Шифр', max_length=100, default='')  # 2
    num = models.IntegerField('Номер п/п', default=0)  # 1
    name = models.TextField('Наименование')  # 9
    ei = models.ForeignKey(
        'OKEI', on_delete=models.SET_NULL, null=True, blank=True)  # 10
    count = models.FloatField('Количество', default=0.0)  # 11
    sum = models.FloatField('Итого', default=0.0)  # 26
    is_key = models.BooleanField('Ключевая позиция', default=False)
    sum_keys = models.FloatField('Ключевая сумма', default=0.0)

    def get_color(self)->str:
        stat_rows = self.stats.all()
        count = stat_rows.count()
        coef = 1
        if count > 0:
            coef = sum([stat_row.key_percent for stat_row in stat_rows])/count
            #RGB
            r = int((1-coef)*255)
            g = int(coef*255)
            color = f"#{r:x}{g:x}00"
            return color
        return "#6e6b7b"

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Смета: Строка"
        verbose_name_plural = "Смета: Строки"
        ordering = ['num']


class SmetaSubRow(models.Model):
    ''' Статьи затрат по строке '''
    smeta_row = models.ForeignKey(
        'SmetaRow', on_delete=models.CASCADE, related_name='subrows')
    category = models.CharField(max_length=20, choices=(('material','material'),('expanse','expanse')), default='expanse')
    name = models.TextField('Наименование')  # 12, 19, 20, 21, 22, 23, 24, 25
    ei = models.ForeignKey(
        'OKEI', on_delete=models.SET_NULL, null=True, blank=True)  # 10
    count = models.FloatField('Количество', default=0.0)  # 11
    amount = models.FloatField('Цена за единицу', default=1.0)  # 13
    coef_correct = models.FloatField(
        'Корректировочный коэф', default=1.0)  # 14
    coef_winter = models.FloatField('Зимний коэф', default=1.0)  # 15
    coef_recalc = models.FloatField('Коэф. пересчета', default=1.0)  # 17
    sum_basic = models.FloatField(
        'Затраты в базисном уровне', default=0.0)  # 16
    sum_current = models.FloatField(
        'Затраты в текущем уровне', default=0.0)  # 18

    def __str__(self) -> str:
        return f"{self.name}"
    class Meta:
        verbose_name = "Смета: Статья затрат"
        verbose_name_plural = "Смета: Статьи затрат"

class SmetaRowStat(models.Model):
    sn = models.ForeignKey(SN, on_delete=models.CASCADE, null=True, blank=True, related_name='stats')
    smeta_row = models.ForeignKey(SmetaRow, on_delete=models.CASCADE, null=True, blank=True, related_name='stats')
    fasstext_percent = models.FloatField(default=0.0)
    fasttext_spgz = models.ForeignKey(SPGZ, on_delete=models.CASCADE, null=True, blank=True, related_name='fasttext_stats')
    key_phrases_spgz = models.ForeignKey(SPGZ, on_delete=models.CASCADE, null=True, blank=True, related_name='key_phrases_stats')
    key_phrases_percent = models.FloatField(default=0.0)
    levenst_ratio = models.FloatField(default=0.0)
    is_key = models.BooleanField(default=False)
    key_percent = models.FloatField(default=0.0)
    

    def __str__(self) -> str:
        return f"Статистика: {self.smeta_row}"
    
    class Meta:
        verbose_name = "Смета:Расширенная строка"
        verbose_name_plural = "Смета: Расширенные строки"

class SmetaRowStatWords(models.Model):
    smeta_row_stat = models.ForeignKey(SmetaRowStat, on_delete=models.SET_NULL, null=True, blank=True, related_name='stat_words')
    name = models.CharField(max_length=1000)
    percent = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Смета:Расширенная строка (тэги)"
        verbose_name_plural = "Смета: Расширенные строки (тэги)"
        ordering = ['-percent']