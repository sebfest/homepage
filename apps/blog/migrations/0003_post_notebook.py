# Generated by Django 3.2.6 on 2021-08-30 08:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='notebook',
            field=models.FileField(blank=True, help_text='A notebook file', upload_to='uploads/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ipynb'])]),
        ),
    ]
