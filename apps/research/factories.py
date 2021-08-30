import datetime
import io
import random

from django.utils import timezone
from factory import LazyAttribute, Faker, post_generation
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyDateTime
from reportlab.pdfgen import canvas

from blog.factories import UserFactory
from research.models import Paper


def make_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 100, "Hello world.")
    pdf.showPage()
    pdf.save()
    return buffer


class PaperFactory(DjangoModelFactory):
    class Meta:
        model = Paper
        django_get_or_create = ('title',)

    title = Faker('sentence', nb_words=4, variable_nb_words=True)
    abstract = Faker('text', max_nb_chars=300)
    status = random.choice(Paper.STATUS_CHOICES)[0]
    version = FuzzyDateTime(timezone.now())
    keywords = Faker('words', nb=3, ext_word_list=None, unique=False)
    pdf = FileField(
        from_func=make_pdf,
        filename='foobar.pdf'
    )
    project_link = Faker('url')
    binder_link = Faker('url')

    papertype = random.choice(Paper.PAPERTYPE_CHOICES)[0]
    institution = Faker('company')
    journal = Faker('sentence', nb_words=14, variable_nb_words=True)
    pages = Faker('pyint')
    volume = Faker('pyint')
    number = Faker('pyint')
    link = Faker('url') if random.randint(0, 100) < 90 else ''
    note = Faker('text', max_nb_chars=50)

    created_date = FuzzyDateTime(timezone.now() - datetime.timedelta(days=random.randint(5, 356)))
    modified_date = LazyAttribute(lambda o: o.created_date + datetime.timedelta(days=random.randint(1, 4)))
    is_active = LazyAttribute(lambda o: True if random.randint(0, 100) < 50 else False)

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)
            return
        for x in range(random.randint(1, 4)):
            if x == 0:
                author = UserFactory.create(**kwargs)
            else:
                author = UserFactory.create()
            self.authors.add(author)
