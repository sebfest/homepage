# Generated by Django 2.2 on 2019-09-20 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagulous_Post_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, db_index=False, help_text='Slug for URL.', max_length=128, unique=True, verbose_name='slug')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date of creation', verbose_name='created at')),
                ('modified_date', models.DateTimeField(auto_now=True, help_text='Date of last modification', verbose_name='modified at')),
                ('is_active', models.BooleanField(default=False, help_text='Is active', verbose_name='active')),
                ('activation_date', models.DateTimeField(blank=True, help_text='Date of activation', null=True, verbose_name='activated at')),
                ('title', models.CharField(help_text='The post title', max_length=256, verbose_name='title')),
                ('subtitle', models.CharField(help_text='The post subtitle', max_length=256, verbose_name='subtitle')),
                ('body', markdownx.models.MarkdownxField(blank=True, help_text='The post content', verbose_name='body')),
                ('start_publication', models.DateTimeField(blank=True, help_text='Start date of publication.', null=True, verbose_name='start publication')),
                ('end_publication', models.DateTimeField(blank=True, help_text='End date of publication.', null=True, verbose_name='end publication')),
                ('enable_comments', models.BooleanField(default=True, help_text='Show commenting section', verbose_name='Commenting on/off')),
                ('views', models.IntegerField(default=0, editable=False, help_text='Number of views')),
                ('last_accessed', models.DateTimeField(blank=True, editable=False, help_text='Last accessed', null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('tags', tagulous.models.fields.TagField(_set_tag_meta=True, force_lowercase=True, help_text='Enter a comma-separated tag string', max_count=5, to='Blog.Tagulous_Post_tags')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_date'],
                'get_latest_by': 'activation_date',
            },
        ),
    ]
