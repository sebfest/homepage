# Generated by Django 2.2.5 on 2019-09-24 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0003_auto_20190924_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='downloaded',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='last_downloaded',
        ),
    ]
