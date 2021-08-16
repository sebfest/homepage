import datetime
import random

from django.utils import timezone
from django.utils.text import slugify

from factory import LazyAttribute, SubFactory, Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from config import settings
from blog.models import Post


class UserFactory(DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = LazyAttribute(lambda obj: slugify(obj.first_name + '_' + obj.last_name))
    email = Faker('email')
    password = Faker('password')

    is_staff = Faker('boolean', chance_of_getting_true=10)
    is_superuser = Faker('boolean', chance_of_getting_true=0)
    is_active = Faker('boolean', chance_of_getting_true=90)

    date_joined = LazyAttribute(lambda obj: timezone.now() - datetime.timedelta(days=random.randint(5, 50)))
    last_login = LazyAttribute(lambda obj: obj.date_joined + datetime.timedelta(days=4))


class PostFactory(DjangoModelFactory):

    class Meta:
        model = Post
        django_get_or_create = ('title',)

    author = SubFactory(UserFactory)
    title = Faker('sentence', nb_words=4, variable_nb_words=True)
    subtitle = Faker('sentence', nb_words=10, variable_nb_words=True)
    tags = Faker('words')
    body = Faker('text')

    created_date = FuzzyDateTime(timezone.now() - datetime.timedelta(days=random.randint(5, 356)))
    modified_date = LazyAttribute(lambda obj: obj.created_date + datetime.timedelta(days=random.randint(1, 4)))

    start_publication = LazyAttribute(lambda obj: obj.created_date)
    end_publication = LazyAttribute(lambda obj: obj.start_publication + datetime.timedelta(days=random.randint(5, 356)))

    is_active = Faker('boolean', chance_of_getting_true=80)
    views = Faker('random_int', min=0, max=300, step=1)
    last_viewed = LazyAttribute(lambda obj: obj.created_date)



