# Generated by Django 4.1.2 on 2022-11-09 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_smetarowstatwords_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smeta',
            name='status_file',
            field=models.IntegerField(choices=[(-1, 'Ошибка'), (0, 'Загружен файл'), (1, 'Загружен в БД'), (2, 'Обрабатывается'), (3, 'Готов')], default=0, verbose_name='Статус сметы'),
        ),
    ]
