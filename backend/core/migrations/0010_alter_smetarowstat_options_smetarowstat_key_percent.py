# Generated by Django 4.1.2 on 2022-11-06 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_smetarow_is_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smetarowstat',
            options={'verbose_name': 'Смета:Расширенная строка', 'verbose_name_plural': 'Смета: Расширенные строки'},
        ),
        migrations.AddField(
            model_name='smetarowstat',
            name='key_percent',
            field=models.FloatField(default=0.0),
        ),
    ]
