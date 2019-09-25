import mimetypes
import os
import string

from django.core.exceptions import ValidationError
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone

from homepage.settings import MEDIA_ROOT


def validate_pdf_extension(file):
    """
    Checks file for .pdf extension
    :param file: A file object
    :return: ValidationError if file not PDF
    """
    mime = mimetypes.guess_type(file.name)[0]
    allowed_mime = ['application/pdf']
    if mime not in allowed_mime:
        raise ValidationError('%(mime)s Please provide a PDF file.', params={'mime': mime}, code='pdf_error')


def rename_pdf(instance, filename):
    """
    Renames file to AuthorYear.pdf or AuthorYearLetter.pdf if already exists.pdf
    :param instance: A paper instance;
    :param filename: The current filename
    :return: A unique file path
    """
    author = instance.first_author
    year = timezone.now().strftime('%Y')
    file_ext = os.path.splitext(filename)[1]
    file_path = 'papers/{0}/{0}{1}{2}'.format(author, year, file_ext)
    iteration = 0
    while os.path.isfile(os.path.join(MEDIA_ROOT, file_path)) and iteration < len(string.ascii_lowercase):
        letter = string.ascii_lowercase[iteration]
        file_path = 'papers/{0}/{0}{1}{2}{3}'.format(author, year, letter, file_ext)
        iteration += 1
    return file_path


def model_to_dict(instance):
    """
    Converts model fields to dictionary
    :param instance: A model instance
    :return: a dictionary
    """
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data
