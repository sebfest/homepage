from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from tagulous.models import TagField

from homepage import settings
from homepage.models import AbstractBaseModel


class Post(AbstractBaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        verbose_name=_('author'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(
        _('title'),
        max_length=256,
        help_text=_('The post title'),
    )
    subtitle = models.CharField(
        _('subtitle'),
        max_length=256,
        help_text=_('The post subtitle'),
    )
    body = MarkdownxField(
        _('body'),
        blank=True,
        help_text=_('The post content'),
    )
    tags = TagField(
        force_lowercase=True,
        max_count=5,
    )
    start_publication = models.DateTimeField(
        _('start publication'),
        blank=True,
        null=True,
        help_text=_('Start date of publication.')
    )
    end_publication = models.DateTimeField(
        _('end publication'),
        blank=True,
        null=True,
        help_text=_('End date of publication.'),
    )
    enable_comments = models.BooleanField(
        _('Commenting on/off'),
        default=True,
        help_text=_('Show commenting section'),
    )
    views = models.IntegerField(
        default=0,
        editable=False,
        help_text=_('Number of views'),
    )
    last_viewed = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        help_text=_('Last viewed'),
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created_date']
        get_latest_by = 'activation_date'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={"slug": self.slug})

    def clean(self, *args, **kwargs):

        super(Post, self).clean()

        if all([self.end_publication, self.start_publication]):
            if self.end_publication < self.start_publication:
                raise ValidationError(_('The publication start date must be before the publication end date.'))

    def is_viewed(self):
        self.last_viewed = timezone.now()
        self.views += 1
        self.save()

    def formatted_markdown(self):
        return markdownify(self.body)
