from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'title',
        'created_date',
        'modified_date',
        'is_active',
        'start_publication',
        'end_publication',
        'get_object_link',
    )
    search_fields = ('title', 'body')
    ordering = ('-created_date',)
    date_hierarchy = 'activation_date'
    actions_on_top = True
    actions_on_bottom = False
    actions = ('make_published', 'make_unpublished',)

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        'created_date',
        'activation_date',
        'modified_date',
        'views',
        'last_viewed',
    )
    fieldsets = [
        ('Main', {
            'fields': (
                'author',
                'title',
                'subtitle',
                'tags',
            )
        }),
        ('Content', {
            'fields': ['body'],
            'classes': ('wide',),
        }),
        ('Publishing', {
            'fields': (
                'is_active',
                'start_publication',
                'end_publication'
            ),
            'classes': ['collapse'],
        }),
        ('Info', {
            'fields': (
                'slug',
                'created_date',
                'modified_date',
                'activation_date',
                'views',
                'last_viewed',
            ),
            'classes': ['collapse'],
        }),
    ]

    @admin.action(description='View on site')
    def get_object_link(self, post: Post) -> str:
        item_url = post.get_absolute_url()
        return format_html('<a href="{url}">Open</a>', url=item_url)

    @admin.action(description='Publish selected Post')
    def make_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        rows_updated = queryset.update(is_published=True)
        for item in queryset:
            item.save()
        if rows_updated == 1:
            message_bit = 'One post was'
        else:
            message_bit = '%s posts were' % rows_updated
        self.message_user(request, f'{message_bit} successfully marked as published.', messages.SUCCESS)

    @admin.action(description='Un-publish selected Post')
    def make_unpublished(self, request: HttpRequest, queryset: QuerySet) -> None:
        rows_updated = queryset.update(is_published=False)
        for item in queryset:
            item.save()
        if rows_updated == 1:
            message_bit = "One post was"
        else:
            message_bit = "%s posts were" % rows_updated
        self.message_user(request, f'{message_bit} successfully marked as published.', messages.SUCCESS)


admin.site.register(Post, PostAdmin)
