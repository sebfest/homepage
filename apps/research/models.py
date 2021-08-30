import mimetypes
import os
import string

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.html import format_html_join
from django.utils.translation import ugettext_lazy as _
from tagulous.models import TagField

import config.settings.base as settings
from config.basemodels import AbstractBaseModel
from research.managers import PaperQuerySet


def rename_pdf(paper, filename: str) -> str:
    """Renames file to AuthorYear.pdf or AuthorYearLetter.pdf if file already exists."""
    author = paper.first_author
    year = timezone.now().strftime('%Y')
    file_ext = os.path.splitext(filename)[1]
    file_path = f'papers/{author}/{author}{year}{file_ext}'
    iteration = 0
    while os.path.isfile(os.path.join(settings.MEDIA_ROOT, file_path)) and iteration < len(string.ascii_lowercase):
        letter = string.ascii_lowercase[iteration]
        file_path = f'papers/{author}/{author}{year}{letter}{file_ext}'
        iteration += 1
    return file_path


class Paper(AbstractBaseModel):
    ARTICLE = 'Article'
    UNPUBLISHED = 'Unpublished'
    TECHREPORT = 'Techreport'
    INPROCEEDINGS = 'Inproceedings'
    MISC = 'Misc'
    PUBLISHED = 'Published'
    REVISE = 'Revise'

    PAPERTYPE_CHOICES = [
        (ARTICLE, 'Published'),
        (UNPUBLISHED, 'Unpublished'),
        (TECHREPORT, 'Working paper'),
        (INPROCEEDINGS, 'Conference article'),
        (MISC, 'Miscellaneous'),
    ]

    STATUS_CHOICES = [
        (UNPUBLISHED, 'Unpublished'),
        (PUBLISHED, 'Published'),
        (REVISE, 'Revise & resubmit'),
    ]

    papertype = models.CharField(
        _('papertype'),
        max_length=64,
        choices=PAPERTYPE_CHOICES,
        default=UNPUBLISHED,
    )
    status = models.CharField(
        _('status'),
        max_length=64,
        choices=STATUS_CHOICES,
        default=UNPUBLISHED,
    )
    title = models.CharField(
        _('title'),
        max_length=256,
    )
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='papers',
    )
    abstract = models.TextField(
        _('abstract'),
    )
    version = models.DateTimeField(
        _('version date'),
        help_text=_('Date of version'),
        blank=True,
        null=True,
    )
    institution = models.CharField(
        _('institution'),
        max_length=256,
        blank=True,
    )
    keywords = TagField(
        force_lowercase=True,
        max_count=5,
    )
    project_link = models.URLField(
        _('Link to project'),
        blank=True,
    )
    binder_link = models.URLField(
        _('Link to binder'),
        blank=True,
    )
    journal = models.CharField(
        _('journal'),
        max_length=256,
        blank=True
    )
    pages = models.CharField(
        _('pages'),
        max_length=32,
        blank=True
    )
    volume = models.CharField(
        _('volume'),
        max_length=32,
        blank=True
    )
    number = models.CharField(
        _('number'),
        max_length=16,
        blank=True
    )
    link = models.URLField(
        _('Link to journal'),
        blank=True
    )
    note = models.CharField(
        _('note'),
        max_length=256,
        blank=True
    )
    pdf = models.FileField(
        verbose_name='PDF',
        # upload_to=rename_pdf,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=True
    )
    mime = models.CharField(
        _('mime'),
        max_length=64,
        blank=True,
        editable=False
    )

    class Meta:
        verbose_name = "Paper"
        verbose_name_plural = "Papers"

    def __str__(self):
        return f'{self.title}'

    def clean(self, *args, **kwargs):
        """Make sure mime type for paper is set."""
        super(Paper, self).clean()

        if self.pdf and not self.mime:
            self.mime = self.get_mime_type()

    def delete(self, *args, **kwargs):
        """Remove .pdf file from disk."""
        storage = self.pdf.storage
        if storage.exists(self.pdf.name):
            storage.delete(self.pdf.name)

        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        """Get link to object."""
        return self.pdf.url if self.pdf else None

    def get_mime_type(self):
        """Get mime type for .pdf file."""
        return mimetypes.guess_type(os.path.basename(self.pdf.name))[0]

    @property
    def first_author(self):
        """Get first author."""
        return self.authors.all().order_by('last_name')[0].last_name

    @property
    def author_names(self):
        """Get authors in alphabetical order."""
        all_authors = self.authors.all().order_by('last_name')
        return format_html_join(', ', '{}', ((a.get_full_name(),) for a in all_authors))

    @property
    def keyword_list(self):
        """Get keyword list string."""
        return format_html_join(', ', '{}', ((keyword.name,) for keyword in self.keywords.all()))

    def get_bibtex(self):
        """Generate a Bibtex key string for an Article type."""
        data = {
            'type': self.papertype,
            'title': self.title,
            'first_author': self.first_author,
            'author': ' and '.join(author.last_name + ', ' + author.first_name for author in self.authors.all()),
            'institution': self.institution,
            'year': self.modified_date.strftime("%Y"),
            'month': self.modified_date.strftime("%B"),
            'journal': self.journal,
            'pages': self.pages,
            'volume': self.volume,
            'number': self.number,
            'abstract': self.abstract,
            'note': self.note,
        }
        article_keys = [key for key in sorted(data) if key not in ['type', 'first_author']]
        bibtex = str()
        bibtex += '@' + data['type'] + '{' + data['first_author'] + data['year'] + ',\n'
        for key in article_keys:
            bibtex += ' ' + key + ' = {' + data[key] + '},\n'
        bibtex += '}\n\n'
        return bibtex
