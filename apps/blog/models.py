from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from tagulous.models import TagField

import config.settings.base as settings


class AbstractBaseModel(models.Model):
    """Abstract base model for all models."""
    slug = models.SlugField(
        _('slug'),
        max_length=128,
        blank=True,
        unique=True,
        db_index=False,
        help_text=_('Slug for URL.')
    )
    created_date = models.DateTimeField(
        _('created at'),
        auto_now=False,
        auto_now_add=True,
        editable=False,
        help_text=_('Date of creation'),
    )
    modified_date = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        auto_now_add=False,
        help_text=_('Date of last modification'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Is active'),
    )
    activation_date = models.DateTimeField(
        _('activated at'),
        blank=True,
        null=True,
        help_text=_('Date of activation'),
    )

    def clean(self):

        if self.is_active and self.activation_date is None:
            self.activation_date = timezone.now()
        elif not self.is_active and self.activation_date is not None:
            self.activation_date = None

        if not self.slug:
            self.slug = slugify(self.__str__())

    def save(self, *args, **kwargs):
        self.clean()
        super(AbstractBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-activation_date', '-created_date']
        get_latest_by = 'activation_date'


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
    tags = TagField(
        force_lowercase=True,
        max_count=5,
        get_absolute_url=lambda tag: reverse('blog:post_tag_list', kwargs={'slug': tag.slug})
    )
    body = MarkdownxField(
        _('body'),
        blank=True,
        help_text=_('The post content'),
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
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={"slug": self.slug})

    def clean(self):
        if all([self.end_publication, self.start_publication]) and self.end_publication < self.start_publication:
            raise ValidationError(_('The publication start date must be before the publication end date.'))

        super().clean()

    def is_viewed(self):
        self.last_viewed = timezone.now()
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def formatted_markdown(self):
        return markdownify(self.body)
