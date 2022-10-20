import contextlib
import os

import nbformat
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from nbconvert.exporters import HTMLExporter
from tagulous.models import TagField

import config.settings.base as settings
from config.basemodels import AbstractBaseModel


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
    notebook = models.FileField(
        help_text=_('A notebook file'),
        blank=True,
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['ipynb'])],
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


def convert_notebook(nb_file: File):
    """
    Convert notebook file to .html and extract all images to the same folder as the source file.

    :param nb_file: Notebook file
    :return: str, the .html content
    """
    nb_file_dirname = os.path.dirname(nb_file.name)
    nb_node = nbformat.read(nb_file, nbformat.NO_CONVERT)

    html_exporter = HTMLExporter()
    html_body, html_resources = html_exporter.from_notebook_node(nb_node)

    all_figures = html_resources.get('outputs', {})
    for figure_name, figure in all_figures.items():
        figure_path = os.path.join(nb_file_dirname, figure_name)
        with contextlib.suppress(FileNotFoundError):
            os.remove(figure_path)
        default_storage.save(figure_path, ContentFile(figure))

    return html_body
