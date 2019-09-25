import mimetypes
import os

from django.db import models
from django.utils.html import format_html_join
from django.utils.translation import ugettext_lazy as _
from tagulous.models import TagField

from homepage import settings
from homepage.models import AbstractBaseModel

from research.managers import PaperQuerySet
from research.utils import validate_pdf_extension, rename_pdf


class Paper(AbstractBaseModel):
    PAPERTYPE_CHOICES = [
        ('Article', 'Published'),
        ('Unpublished', 'Unpublished'),
        ('Techreport', 'Working paper'),
        ('Inproceedings', 'Conference article'),
        ('Misc', 'Miscellaneous'),
    ]
    papertype = models.CharField(
        _('papertype'),
        max_length=64,
        choices=PAPERTYPE_CHOICES,
        default='Article',
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
        validators=[validate_pdf_extension],
        blank=True
    )
    mime = models.CharField(
        _('mime'),
        max_length=64,
        blank=True,
        editable=False
    )

    objects = PaperQuerySet.as_manager()

    class Meta:
        verbose_name = "Paper"
        verbose_name_plural = "Papers"

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):

        super(Paper, self).clean()

        if self.pdf and not self.mime:
            self.mime = self.get_mime_type()

    def get_absolute_url(self):
        return self.pdf.url if self.pdf else None

    def get_mime_type(self):
        return mimetypes.guess_type(os.path.basename(self.pdf.name))[0]

    @property
    def first_author(self):
        return self.authors.all().order_by('last_name')[0].last_name

    @property
    def author_names(self):
        all_authors = self.authors.all().order_by('last_name')
        return format_html_join(', ', '{}', ((a.get_full_name(),) for a in all_authors))

    @property
    def keyword_list(self):
        return format_html_join(', ', '{}', ((keyword.name,) for keyword in self.keywords.all()))

    def get_bibtex(self):
        """
        :return: A Bibtex key string for an Article type.
        """
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
