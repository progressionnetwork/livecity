# Generated by Django 4.1.2 on 2022-10-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_kpgz_managers_alter_kpgz_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='OKEI',
            fields=[
                ('code', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('short_name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'ОКЕИ',
                'verbose_name_plural': 'ОКЕИ',
                'ordering': ['code'],
            },
        ),
        migrations.AlterModelOptions(
            name='kpgz',
            options={'ordering': ['code'], 'verbose_name': 'КПГЗ', 'verbose_name_plural': 'КПГЗ'},
        ),
    ]