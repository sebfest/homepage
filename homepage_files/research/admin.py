from django.contrib import admin
from django.db import models
from django.forms import Textarea, Select
from django.utils.html import format_html

from research.models import Paper


class PaperAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'title',
        'created_date',
        'is_active',
        'pdf_link'
    )
    list_filter = ('is_active',)
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)
    search_fields = ('title', 'authors__full_name',)
    actions_on_top = True
    actions_on_bottom = False

    fieldsets = [
        ('Main',
         {
             'fields':
             [
                 'status',
                 'title',
                 'authors',
                 'abstract',
                 'keywords',
             ]
         }
         ),
        ('Optional',
         {
             'fields':
             [
                 'pdf',
                 'project_link',
                 'binder_link',
                 'is_active'
             ],
             'classes': ['collapse']
         }
         ),
        ('Journal Info',
         {
             'fields': [
                 'papertype',
                 'institution',
                 'journal',
                 'pages',
                 'volume',
                 'number',
                 'link',
                 'note'
             ],
             'classes': ['collapse']
         }
         ),
        ('Meta',
         {
             'fields': [
                 'created_date',
                 'modified_date',
                 'slug',
             ],
             'classes': ['collapse']
         }
         ),
    ]
    readonly_fields = ('created_date', 'modified_date', 'mime', 'slug')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
        models.BooleanField: {'widget': Select(choices=((False, 'False'), (True, 'True')))},
    }

    @admin.action(description='PDF-link')
    def pdf_link(self, item):
        if pdf_url := item.get_absolute_url():
            return format_html('<a href="{url}" target="_blank">PDF</a>', url=pdf_url)


admin.site.register(Paper, PaperAdmin)
