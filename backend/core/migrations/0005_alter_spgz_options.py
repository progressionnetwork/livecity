# Generated by Django 4.1.2 on 2022-11-06 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_smeta_json_data_remove_snsection_json_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spgz',
            options={'ordering': ['key'], 'verbose_name': 'СПГЗ', 'verbose_name_plural': 'СПГЗ'},
        ),
    ]
