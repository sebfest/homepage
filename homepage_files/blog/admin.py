from django.contrib.admin import ModelAdmin
from django.db.models import BooleanField
from django.forms.widgets import Select
from django.utils.html import format_html

from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget
from tagulous import admin

from blog.models import Post


class PostAdmin(ModelAdmin):
    list_select_related = True
    list_display = (
       'title', 'created_date', 'modified_date', 'is_active',
       'enable_comments', 'start_publication', 'end_publication', 'get_object_link',
    )
    list_filter = ['is_active', ]
    search_fields = ('title', 'body')
    ordering = ('-created_date',)
    date_hierarchy = 'activation_date'
    actions = ('make_published', 'make_unpublished',)
    actions_on_top = True
    actions_on_bottom = False

    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget},
        BooleanField: {'widget': Select(choices=[(True, 'Yes'), (False, 'No')])},
    }
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_date', 'activation_date', 'modified_date', 'views')
    fieldsets = [
        ('Main', {
            'fields': ['author', 'title', 'subtitle', 'tags']
        }),
        ('Content', {
            'fields': ['body'],
            'classes': ('wide',),
        }),
        ('Publishing', {
            'fields': ['is_active', 'start_publication', 'end_publication'],
            'classes': ['collapse'],
        }),
        ('Misc.', {
            'fields': ['slug', 'enable_comments'],
            'classes': ['collapse'],
        }),
        ('Info', {
            'fields': ['views', 'created_date', 'modified_date', 'activation_date'],
            'classes': ['collapse'],
        }),
    ]

    def make_published(self, request, queryset):
        rows_updated = queryset.update(is_published=True)
        for item in queryset:
            item.save()
        if rows_updated == 1:
            message_bit = 'One post was'
        else:
            message_bit = '%s posts were' % rows_updated
        self.message_user(request, '%s successfully marked as published.' % message_bit)

    make_published.short_description = 'Publish selected Post'

    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(is_published=False)
        for item in queryset:
            item.save()
        if rows_updated == 1:
            message_bit = "One post was"
        else:
            message_bit = "%s posts were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    make_unpublished.short_description = "Unpublish selected Post"

    def get_object_link(self, item):
        current_url = item.get_absolute_url()
        return format_html('<a href="{url}">Open</a>', url=current_url)

    get_object_link.short_description = 'View on site'


admin.register(Post, PostAdmin)
