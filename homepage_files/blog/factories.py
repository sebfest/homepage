import datetime
import random

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime
from faker import Faker
from faker.utils.text import slugify

from homepage import settings
from blog.models import Post

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    first_name = LazyAttribute(lambda o: fake.first_name())
    last_name = LazyAttribute(lambda o: fake.last_name())
    username = LazyAttribute(lambda o: slugify(o.first_name + '_' + o.last_name))
    email = LazyAttribute(lambda o: fake.email())
    password = LazyAttribute(lambda o: make_password(fake.password()))

    is_staff = LazyAttribute(lambda o: fake.boolean(chance_of_getting_true=10))
    is_superuser = LazyAttribute(lambda o: fake.boolean(chance_of_getting_true=1))
    is_active = LazyAttribute(lambda o: fake.boolean(chance_of_getting_true=90))

    date_joined = LazyAttribute(lambda o: timezone.now() - datetime.timedelta(days=random.randint(5, 50)))
    last_login = LazyAttribute(lambda o: o.date_joined + datetime.timedelta(days=4))


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ('title',)

    author = SubFactory(UserFactory)
    title = LazyAttribute(lambda o: fake.sentence(nb_words=4, variable_nb_words=True))
    subtitle = LazyAttribute(lambda o: fake.sentence(nb_words=10, variable_nb_words=True))
    body = LazyAttribute(lambda o: '<br>'.join([fake.text(max_nb_chars=1000)] * 5))

    created_date = FuzzyDateTime(timezone.now() - datetime.timedelta(days=random.randint(5, 356)))
    modified_date = LazyAttribute(lambda o: o.created_date + datetime.timedelta(days=random.randint(1, 4)))

    is_active = LazyAttribute(lambda o: fake.boolean(chance_of_getting_true=80))
    views = LazyAttribute(lambda o: random.randint(0, 100))
    last_accessed = LazyAttribute(lambda o: o.created_date + datetime.timedelta(days=random.randint(1, 4)))



