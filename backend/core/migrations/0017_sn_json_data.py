# Generated by Django 4.1.2 on 2022-11-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_tz_options_alter_tzrow_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='sn',
            name='json_data',
            field=models.TextField(default='', verbose_name='JSON'),
            preserve_default=False,
        ),
    ]
